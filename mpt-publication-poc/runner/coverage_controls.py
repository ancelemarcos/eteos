"""Candidate 0.6 controls. MATERIALIZED_NOT_RUN; never execute without separate approval."""
import concurrent.futures
import time
import psycopg

NAMES = {"SESSION-BEFORE-COMMIT", "SESSION-AFTER-COMMIT", "LEASE-LIFECYCLE",
         "COMPOUND-ROLLBACK", "ACK-NEGATIVE", "T2-SAME-TRANSACTION", "IMMUTABLE-NEGATIVE"}
NAMES |= {"ACK-RECEIPT-NO-CALL", "T4-LEASE-LIFECYCLE", "WRITER-DELIVERY-BYPASS"}
NAMES |= {f"T4-BACKEND-{phase}-{boundary}" for phase in ("AUTHORIZE","RECHECK")
          for boundary in ("BEFORE","AFTER")}


def snapshot(lab):
    # Full rows, deterministic JSON ordering; includes every candidate table, not views.
    tables = lab.sql(lab.owner, """SELECT tablename FROM pg_tables
        WHERE schemaname='mpt_poc' ORDER BY tablename""")
    return {name: lab.sql(lab.owner,
        'SELECT coalesce(jsonb_agg(rowdata ORDER BY rowdata::text),\'[]\'::jsonb) '
        'FROM (SELECT to_jsonb(t) rowdata FROM mpt_poc."' + name.replace('"','""') + '" t) s')
        for (name,) in tables}


def unchanged(lab, before):
    if snapshot(lab) != before:
        raise AssertionError("negative control changed stored content")
    lab.log("FULL_CONTENT_UNCHANGED")


def run(lab, name):
    if name.startswith("T4-BACKEND-"):
        return t4_backend(lab,name)
    if name == "T4-LEASE-LIFECYCLE":
        return t4_lease(lab)
    if name == "ACK-RECEIPT-NO-CALL":
        lab.notice()
        lab.deliver("AUTHORIZE","RECEIPT-AUTH")
        lab.sql(lab.owner,"""INSERT INTO synthetic_destination_receipt
            VALUES('SYNTH-INBOX','N-OLD-KEY','AUTH-N-OLD','synthetic-payload-v1')""")
        lab.check("DELIVERY",[("SEND_AUTHORIZED",1,0,1)])
        before = snapshot(lab)
        lab.expect_error(lab.dispatch,"P0001",lab.ops["T4"],
                         ("P-A","N-OLD","DISP",lab.depoch,"ACK","NO-CALL"))
        unchanged(lab,before)
        return
    if name == "WRITER-DELIVERY-BYPASS":
        lab.notice()
        lab.deliver("AUTHORIZE","BYPASS-AUTH")
        lab.destination("BYPASS-CALL")
        before = snapshot(lab)
        for table in ("send_authorization","synthetic_destination_call",
                      "synthetic_destination_receipt","t4_operation_receipt"):
            for sql in (f"INSERT INTO {table} SELECT * FROM {table}",f"DELETE FROM {table}"):
                lab.expect_error(lab.writer,"42501",sql)
                unchanged(lab,before)
        for sql in ("UPDATE notification SET delivery_status='ACKED'",
                    "UPDATE outbox_event SET dispatch_status='ACKED'",
                    "UPDATE outbox_event SET lease_token='FORGED'",
                    "UPDATE send_authorization SET policy_version='FORGED'",
                    "UPDATE t4_operation_receipt SET response='ACKED'",
                    "UPDATE synthetic_destination_receipt SET authorization_id='FORGED'",
                    "UPDATE synthetic_destination_call SET authorization_id='FORGED'",
                    "SET ROLE mpt_owner", "SET ROLE mpt_dispatcher"):
            lab.expect_error(lab.writer,"42501",sql)
            unchanged(lab,before)
        lab.expect_error(lab.writer,"42501",lab.ops["T4"],
                         ("P-A","N-OLD","DISP",lab.depoch,"ACK","BYPASS"))
        unchanged(lab,before)
        return
    if name.startswith("SESSION-"):
        # Owner is a separately approved control connection; runtime role remains publisher.
        victim = lab.session("publisher")
        lab.begin(victim)
        lab.op(victim, "TP", "P-A", "B1", "PUB", lab.epoch)
        committed = name == "SESSION-AFTER-COMMIT"
        if committed:
            lab.commit(victim)
        lab.log("TERMINATION_CHECKPOINT", committed=committed, victim_pid=victim.info.backend_pid)
        killed = lab.sql(lab.owner, "SELECT pg_terminate_backend(%s,5000)", (victim.info.backend_pid,))
        if killed != [(True,)]:
            raise AssertionError("backend termination not confirmed")
        if lab.sql(lab.owner, "SELECT count(*) FROM pg_stat_activity WHERE pid=%s",
                   (victim.info.backend_pid,)) != [(0,)]:
            raise AssertionError("terminated backend still present")
        lab.check("FRONTIER", [(1 if committed else 0,)])
        replacement = lab.session("publisher")
        if lab.call(replacement,"TP","P-A","B1","PUB",lab.epoch) != 1:
            raise AssertionError("publication recovery duplicated ordinal")
        recovered = snapshot(lab)
        lab.call(replacement,"TP","P-A","B1","PUB",lab.epoch)
        unchanged(lab,recovered)
        lab.check("FRONTIER", [(1,)])
        lab.check("PROJECTION", [(1,)])
        lab.log("REAL_BACKEND_TERMINATED", committed=committed)
    elif name == "LEASE-LIFECYCLE":
        before = lab.sql(lab.owner, "SELECT expires_at FROM worker_lease WHERE purpose='TP'")
        lab.call(lab.pub,"TP_RENEW","P-A","PUB",lab.epoch,lab.config["lease_ttl"])
        after = lab.sql(lab.owner, "SELECT expires_at FROM worker_lease WHERE purpose='TP'")
        if after[0][0] <= before[0][0]:
            raise AssertionError("renewal did not extend expiry")
        lab.call(lab.pub,"TP_RELEASE","P-A","PUB",lab.epoch)
        winner, loser = lab.session("publisher"), lab.session("publisher")
        lab.begin(winner)
        epoch = lab.op(winner,"TP_ACQUIRE","P-A","WINNER",lab.config["lease_ttl"])[0][0]
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(lab.expect_error,loser,"P0001",lab.ops["TP_ACQUIRE"],
                                 ("P-A","LOSER",lab.config["lease_ttl"]))
            try:
                lab.wait_blocked(loser,winner)
                lab.commit(winner)
                future.result(timeout=lab.config["checkpoint_timeout_seconds"])
            except Exception:
                winner.rollback()
                loser.cancel()
                raise
        lab.expect_error(lab.pub,"P0001",lab.ops["TP"],("P-A","B1","PUB",lab.epoch))
        lab.call(winner,"TP_RELEASE","P-A","WINNER",epoch)
        short = lab.call(winner,"TP_ACQUIRE","P-A","ABANDONED","200 milliseconds")
        # Observe DB expiry directly. Deadline bounds failure; elapsed sleep is not an oracle.
        deadline = time.monotonic()+lab.config["checkpoint_timeout_seconds"]
        while True:
            observed = lab.sql(lab.owner,"""SELECT epoch,expires_at,clock_timestamp(),
                expires_at<=clock_timestamp() FROM worker_lease WHERE purpose='TP'""")[0]
            if observed[3]:
                lab.log("EXPIRY_OBSERVED", row=observed)
                break
            if time.monotonic() >= deadline:
                raise TimeoutError("expiry not observed")
        lab.expect_error(winner,"P0001",lab.ops["TP_RENEW"],
                         ("P-A","ABANDONED",short,lab.config["lease_ttl"]))
        takeover = lab.call(loser,"TP_ACQUIRE","P-A","RECOVERED",lab.config["lease_ttl"])
        if not lab.epoch < epoch < short < takeover:
            raise AssertionError("nonmonotonic fencing")
        lab.expect_error(winner,"P0001",lab.ops["TP"],("P-A","B1","ABANDONED",short))
        lab.call(loser,"TP","P-A","B1","RECOVERED",takeover)
        lab.check("FRONTIER",[(1,)])
    elif name == "COMPOUND-ROLLBACK":
        lab.publish()
        lab.fixture("FB23",lab.writer)
        before = snapshot(lab)
        # Trusted lab owner injects a constraint, NOT a production API or per-member commit.
        lab.sql(lab.owner,"""ALTER TABLE mpt_poc.public_projection ADD CONSTRAINT
            lab_fail_projection CHECK (position_version<>3) NOT VALID""")
        try:
            lab.expect_error(lab.pub,"23514",lab.ops["TP"],("P-A","B23","PUB",lab.epoch))
            unchanged(lab,before)
            lab.check("FRONTIER",[(1,)])
            lab.check("PROJECTION",[(1,)])
        finally:
            lab.sql(lab.owner,"ALTER TABLE mpt_poc.public_projection DROP CONSTRAINT lab_fail_projection")
        lab.publish("B23")
        lab.check("FRONTIER",[(2,)])
        lab.check("PROJECTION",[(3,)])
    elif name == "ACK-NEGATIVE":
        lab.notice()
        for stage in ("NO_AUTH","NO_CALL_OR_RECEIPT","CALL_ONLY"):
            if stage == "NO_CALL_OR_RECEIPT":
                lab.deliver("AUTHORIZE","AUTH-NEG")
            if stage == "CALL_ONLY":
                lab.sql(lab.owner,"""INSERT INTO synthetic_destination_call
                    VALUES('NEG-CALL','SYNTH-INBOX','N-OLD-KEY','AUTH-N-OLD','E_CALL')""")
            before = snapshot(lab)
            lab.expect_error(lab.dispatch,"P0001",lab.ops["T4"],
                             ("P-A","N-OLD","DISP",lab.depoch,"ACK",stage))
            unchanged(lab,before)
    elif name == "T2-SAME-TRANSACTION":
        lab.publish()
        evaluator = lab.session("evaluator")
        before = snapshot(lab)
        lab.begin(evaluator)
        try:
            lab.op(evaluator,"CUT","P-A","CUT-1","C-NEG")
            lab.op(evaluator,"T2B","ATT-NEG","P-A","C-NEG")
            lab.commit(evaluator)
        except psycopg.Error as exc:
            evaluator.rollback()
            if exc.sqlstate != "P0001":
                raise
            lab.log("expected_rejection",sqlstate=exc.sqlstate,role="evaluator",
                    control="T2_SPLIT_REQUIRED")
        else:
            raise AssertionError("same-transaction attempt accepted")
        unchanged(lab,before)
        cut = lab.call(evaluator,"CUT","P-A","CUT-1","C-OK")
        lab.call(evaluator,"T2B","ATT-OK","P-A",cut)
        lab.check("SHARED_ATTEMPTS",[(1,1,1,1)])
    elif name == "IMMUTABLE-NEGATIVE":
        lab.notice()
        evaluator = lab.session("evaluator")
        cut = lab.call(evaluator,"CUT","P-A","CUT-1","C-IMM")
        lab.call(evaluator,"T2B","ATT-IMM","P-A",cut)
        lab.call(lab.writer,"T3","P-A","ATT-IMM","RES-IMM","BR1","a"*64,False)
        lab.publish("BR1")
        lab.deliver("AUTHORIZE","IMM-AUTH")
        lab.destination("IMM-CALL")
        lab.fixture("FCHAIN",lab.writer)
        recovery = lab.session("recovery")
        lab.call(recovery,"BLOCK","P-A","B2",0,"negative matrix")
        before = snapshot(lab)
        # Run as the ordinary writer, not as owner; check full rows after EVERY denial.
        for table in ("publication_batch","publication_member","publication_cut","assessment_attempt",
                      "assessment_result","send_authorization","t4_operation_receipt",
                      "synthetic_destination_receipt","synthetic_destination_call"):
            lab.expect_error(lab.writer,"42501",f"DELETE FROM mpt_poc.{table}")
            unchanged(lab,before)
        for table,column in (("publication_batch","fingerprint"),("publication_member","member_order"),
                             ("publication_cut","resolution_policy_version"),
                             ("assessment_attempt","parameter_identity"),
                             ("assessment_result","fingerprint"),("send_authorization","policy_version"),
                             ("t4_operation_receipt","response"),
                             ("synthetic_destination_receipt","payload_fingerprint"),
                             ("synthetic_destination_call","call_id")):
            lab.expect_error(lab.writer,"42501",f"UPDATE mpt_poc.{table} SET {column}={column}")
            unchanged(lab,before)
        for batch in ("B1","B2"):
            lab.expect_error(lab.writer,"P0001",
                "INSERT INTO publication_member VALUES('P-A',%s,99,NULL,999,NULL)",(batch,))
            unchanged(lab,before)
        for table in ("publication_cut","assessment_attempt","send_authorization",
                      "t4_operation_receipt","synthetic_destination_receipt","synthetic_destination_call"):
            lab.expect_error(lab.writer,"42501",f"INSERT INTO mpt_poc.{table} SELECT * FROM mpt_poc.{table}")
            unchanged(lab,before)
    else:
        raise AssertionError("unknown control")

def terminate_dispatcher(lab, victim, boundary):
    pid = victim.info.backend_pid
    lab.log("T4_TERMINATION_CHECKPOINT",boundary=boundary,pid=pid)
    if lab.sql(lab.owner,"SELECT pg_terminate_backend(%s,5000)",(pid,)) != [(True,)]:
        raise AssertionError("dispatcher backend not terminated")
    if lab.sql(lab.owner,"SELECT count(*) FROM pg_stat_activity WHERE pid=%s",(pid,)) != [(0,)]:
        raise AssertionError("dispatcher backend remains")
    lab.log("T4_BACKEND_ABSENT",pid=pid)


def t4_backend(lab, name):
    phase,boundary = name.removeprefix("T4-BACKEND-").split("-")
    lab.notice()
    if phase == "RECHECK":
        lab.deliver("AUTHORIZE","BASE")
    before = snapshot(lab)
    victim = lab.dispatch
    lab.begin(victim)
    lab.op(victim,"T4","P-A","N-OLD","DISP",lab.depoch,phase,"CRASH-OP")
    if boundary == "AFTER":
        lab.commit(victim)
    terminate_dispatcher(lab,victim,boundary)
    if boundary == "BEFORE":
        unchanged(lab,before)  # authorization, audit and receipt all rolled back
    lab.dispatch = lab.session("dispatcher")  # same approved login, same logical worker/epoch
    if lab.deliver(phase,"CRASH-OP") != "SEND_AUTHORIZED":
        raise AssertionError("recovery response mismatch")
    recovered = snapshot(lab)
    if lab.deliver(phase,"CRASH-OP") != "SEND_AUTHORIZED":
        raise AssertionError("retry response mismatch")
    unchanged(lab,recovered)
    for table,key in (("delivery_audit","audit_id"),("t4_operation_receipt","operation_id")):
        if lab.sql(lab.owner,f"SELECT count(*) FROM {table} WHERE {key}='CRASH-OP'") != [(1,)]:
            raise AssertionError("duplicate or missing T4 audit/receipt")
    lab.close()
    historical = snapshot(lab)
    if lab.deliver(phase,"CRASH-OP") != "SEND_AUTHORIZED":
        raise AssertionError("historical response changed")
    unchanged(lab,historical)
    lab.deliver("RECHECK","FRESH-AFTER-RECOVERY")
    lab.check("DELIVERY",[("SUPPRESSED_AFTER_AUTHORIZATION",1,0,0)])


def t4_lease(lab):
    lab.notice()
    before = lab.sql(lab.owner,"SELECT expires_at FROM worker_lease WHERE purpose='T4'")
    lab.call(lab.dispatch,"T4_RENEW","P-A","DISP",lab.depoch,lab.config["lease_ttl"])
    after = lab.sql(lab.owner,"SELECT expires_at FROM worker_lease WHERE purpose='T4'")
    if after[0][0] <= before[0][0]:
        raise AssertionError("dispatcher renewal did not extend expiry")
    lab.call(lab.dispatch,"T4_RELEASE","P-A","DISP",lab.depoch)
    winner,loser = lab.session("dispatcher"),lab.session("dispatcher")
    lab.begin(winner)
    epoch = lab.op(winner,"T4_ACQUIRE","P-A","WIN",lab.config["lease_ttl"])[0][0]
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(lab.expect_error,loser,"P0001",lab.ops["T4_ACQUIRE"],
                             ("P-A","LOSE",lab.config["lease_ttl"]))
        try:
            lab.wait_blocked(loser,winner)
            lab.commit(winner)
            future.result(timeout=lab.config["checkpoint_timeout_seconds"])
        except Exception:
            winner.rollback()
            loser.cancel()
            raise
    lab.expect_error(lab.dispatch,"P0001",lab.ops["T4"],
                     ("P-A","N-OLD","DISP",lab.depoch,"AUTHORIZE","STALE-AUTH"))
    lab.call(winner,"T4","P-A","N-OLD","WIN",epoch,"AUTHORIZE","WIN-AUTH")
    lab.call(winner,"T4_RELEASE","P-A","WIN",epoch)
    short = lab.call(winner,"T4_ACQUIRE","P-A","ABANDON","200 milliseconds")
    deadline = time.monotonic()+lab.config["checkpoint_timeout_seconds"]
    while True:
        row = lab.sql(lab.owner,"""SELECT epoch,expires_at,clock_timestamp(),
            expires_at<=clock_timestamp() FROM worker_lease WHERE purpose='T4'""")[0]
        if row[3]:
            lab.log("T4_EXPIRY_OBSERVED",row=row)
            break
        if time.monotonic() >= deadline:
            raise TimeoutError("dispatcher expiry not observed")
    lab.expect_error(winner,"P0001",lab.ops["T4_RENEW"],
                     ("P-A","ABANDON",short,lab.config["lease_ttl"]))
    current = lab.call(loser,"T4_ACQUIRE","P-A","RECOVERED",lab.config["lease_ttl"])
    if not lab.depoch < epoch < short < current:
        raise AssertionError("dispatcher epoch not monotonic")
    lab.expect_error(winner,"P0001",lab.ops["T4"],
                     ("P-A","N-OLD","ABANDON",short,"RECHECK","STALE-CHECK"))
    if lab.call(loser,"T4","P-A","N-OLD","RECOVERED",current,"RECHECK","PRE-SEND") != "SEND_AUTHORIZED":
        raise AssertionError("fresh permission missing")
    lab.log("FRESH_RECHECK_COMMITTED",worker="RECOVERED",epoch=current)
    lab.destination("RECOVERED-CALL")
    lab.expect_error(winner,"P0001",lab.ops["T4"],
                     ("P-A","N-OLD","ABANDON",short,"ACK","STALE-ACK"))
    lab.call(loser,"T4","P-A","N-OLD","RECOVERED",current,"ACK","FINAL-ACK")
    lab.check("DELIVERY",[("ACKED",1,1,1)])
