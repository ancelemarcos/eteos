"""Candidate only. NOT_RUN. No database creation, migrations or cleanup here."""
import argparse
import concurrent.futures
import json
import os
import re
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import psycopg
from worker_controller_stub import BLOCKED_SCENARIOS
from coverage_controls import NAMES as COVERAGE_SCENARIOS, run as run_coverage
from environment_guard import verify_files, verify_attestation, verify_server, verify_privileges, PreflightBlocked

ROOT = Path(__file__).resolve().parent
ROLES = {"owner", "publisher", "writer", "evaluator", "dispatcher", "recovery", "reader"}
SCENARIOS = {
    "blocked_recovery", "stale_worker", "concurrent_publish", "concurrent_cut",
    "compound", "ack_loss", "t25a", "t25b", "t13a", "t13b",
    "notify", "quiet", "privileges",
    "DELIVERY-FORGE-01", "T4-ACK-AUTH", "T4-ACK-RECHECK", "T2-TP-FK-CYCLE",
    "POC-T24", "HOLD-PENDING-CLOSE", "FIXED-CUT",
}
SCENARIOS |= COVERAGE_SCENARIOS
SCENARIOS |= set(BLOCKED_SCENARIOS)


def sections(path, fixture=False):
    text = path.read_text(encoding="utf-8-sig")
    prefix = r"FIXTURE " if fixture else ""
    pattern = r"-- BEGIN " + prefix + r"([A-Z0-9_]+)(?:@\d+)?[^\n]*\n(.*?)-- END " + prefix + r"\1(?:@\d+)?"
    return dict(re.findall(pattern, text, re.S))


class Lab:
    def __init__(self, config, output):
        self.config = config
        self.output = output
        self.log_lock = threading.Lock()
        self.seq = 0
        self.connections = []
        self.mutations_started = False
        self.ops = sections(ROOT / "operations.sql")
        self.oracles = sections(ROOT / "oracles.sql")
        self.fixtures = sections(ROOT.parent / "fixtures.sql", True)

    def log(self, event, **data):
        with self.log_lock:
            self.seq += 1
            self.output.write(json.dumps({"seq": self.seq, "event": event,
                "observed_at_utc": datetime.now(timezone.utc).isoformat(), **data}, default=str) + "\n")
            self.output.flush()

    def session(self, role):
        if role not in ROLES:
            raise ValueError("unknown role")
        # Separate approved logins; DSNs never written to evidence.
        conn = psycopg.connect(os.environ["MPT_" + role.upper() + "_DSN"], autocommit=True)
        self.connections.append(conn)
        database, login, superuser = conn.execute(
            "SELECT current_database(),session_user,(SELECT rolsuper FROM pg_roles WHERE rolname=session_user)"
        ).fetchone()
        if database != "mpt_poc_lab" or (role != "owner" and superuser):
            raise RuntimeError("wrong database or privileged runtime login")
        conn.execute("SET ROLE mpt_" + role)  # fixed allowlist only
        conn.execute("SET search_path=mpt_poc,pg_catalog")
        conn.execute("SET TIME ZONE 'UTC'")
        conn.execute("SELECT set_config('statement_timeout',%s,false)",
                     (str(self.config["statement_timeout_ms"]),))
        # Owner monitor privilege for pg_control_system must be provisioned separately.
        # Validate all sessions' settings; cluster identity is checked on the owner before fixtures.
        if role == "owner":
            observed=verify_server(conn,self.config,psycopg.__version__)
            self.log("observed_environment",**observed)
        else:
            expected=self.config["server_settings"]
            for key,value in expected.items():
                if conn.execute("SELECT current_setting(%s)",(key,)).fetchone()[0]!=value:
                    raise PreflightBlocked("runtime session differs from approved settings")
        self.log("session", role=role, login=login, pid=conn.info.backend_pid)
        self.log("observed_privileges",role=role,**verify_privileges(conn,self.config,role))
        return conn

    def sql(self, conn, statement, args=()):
        self.log("statement", pid=conn.info.backend_pid, sql=statement, parameters=args)
        try:
            cur = conn.execute(statement, args or None)
            rows = cur.fetchall() if cur.description else []
            self.log("result", pid=conn.info.backend_pid, rows=rows)
            return rows
        except psycopg.Error as exc:
            self.log("sql_error", pid=conn.info.backend_pid, sqlstate=exc.sqlstate)
            raise

    def op(self, conn, name, *args):
        return self.sql(conn, self.ops[name], args)

    def begin(self, conn):
        self.sql(conn, "BEGIN ISOLATION LEVEL READ COMMITTED")

    def commit(self, conn, ack=True):
        self.sql(conn, "SET CONSTRAINTS ALL IMMEDIATE")
        self.sql(conn, "COMMIT")
        self.log("COMMITTED" if ack else "COMMITTED_ACK_DROPPED", pid=conn.info.backend_pid)

    def call(self, conn, name, *args, ack=True):
        self.begin(conn)
        try:
            rows = self.op(conn, name, *args)
            self.commit(conn, ack)
            return rows[0][0] if rows else None
        except Exception:
            conn.rollback()
            raise

    def expect_error(self, conn, state, statement, args=()):
        self.begin(conn)
        try:
            self.sql(conn, statement, args)
            self.commit(conn)
        except psycopg.Error as exc:
            conn.rollback()
            if exc.sqlstate != state:
                raise AssertionError((state, exc.sqlstate)) from exc
            self.log("expected_rejection", sqlstate=state)
            return
        raise AssertionError("mutation unexpectedly committed")

    def fixture(self, name, conn=None):
        conn = conn or self.owner
        fragment = self.fixtures[name]
        # Fragments are local reviewed text. Strip only top-level transaction lines.
        fragment = re.sub(r"(?m)^(BEGIN;|COMMIT;)\s*$", "", fragment)
        self.begin(conn)
        if conn is not self.owner:
            self.op(conn, "LOCK", "P-A")
        try:
            self.sql(conn, fragment)
            self.commit(conn)
        except Exception:
            conn.rollback()
            raise

    def check(self, name, expected):
        actual = self.sql(self.owner, self.oracles[name])
        if actual != expected:
            raise AssertionError({"oracle": name, "expected": expected, "actual": actual})
        self.log("oracle_matched", name=name)

    def wait_blocked(self, waiter, holder):
        # Observe actual PostgreSQL lock dependency; time budget is failure bound, not ordering oracle.
        deadline = time.monotonic() + self.config["checkpoint_timeout_seconds"]
        while time.monotonic() < deadline:
            blocking = self.owner.execute("SELECT pg_blocking_pids(%s)",
                                          (waiter.info.backend_pid,)).fetchone()[0]
            if holder.info.backend_pid in blocking:
                self.log("CHECKPOINT_BLOCKED", waiter=waiter.info.backend_pid,
                         holder=holder.info.backend_pid)
                return
        raise TimeoutError("required database wait edge not observed")

    def race(self, a, b, op, args_a, args_b):
        self.begin(a)
        first = self.op(a, op, *args_a)[0][0]
        self.log("A_MUTATED_BEFORE_COMMIT")
        started = threading.Event()

        def competitor():
            self.begin(b)
            started.set()
            result = self.op(b, op, *args_b)[0][0]
            self.commit(b)
            return result

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(competitor)
            try:
                if not started.wait(self.config["checkpoint_timeout_seconds"]):
                    raise TimeoutError("B did not reach query submission")
                self.wait_blocked(b, a)
                self.commit(a)
                second = future.result(timeout=self.config["checkpoint_timeout_seconds"])
            except Exception:
                a.rollback()
                b.cancel()
                raise
        return first, second

    def publish(self, batch="B1", ack=True):
        return self.call(self.pub, "TP", "P-A", batch, "PUB", self.epoch, ack=ack)

    def setup(self):
        # Validate every required role/session before any fixture mutation.
        prepared={role:self.session(role) for role in sorted(ROLES)}
        self.owner = prepared["owner"]
        if self.owner.execute("SELECT count(*) FROM mpt_poc.position").fetchone()[0] != 0:
            raise RuntimeError("requires fresh prepared empty schema; runner never cleans it")
        self.mutations_started = True
        self.fixture("F0")
        self.writer = prepared["writer"]
        self.fixture("F1", self.writer)
        self.pub = prepared["publisher"]
        self.epoch = self.call(self.pub, "TP_ACQUIRE", "P-A", "PUB", self.config["lease_ttl"])

    def notice(self, ack=True):
        self.fixture("FNOTICE", self.writer)
        self.publish(ack=ack)
        self.dispatch = self.session("dispatcher")
        self.depoch = self.call(self.dispatch, "T4_ACQUIRE", "P-A", "DISP", self.config["lease_ttl"])

    def deliver(self, phase, key):
        return self.call(self.dispatch, "T4", "P-A", "N-OLD", "DISP", self.depoch, phase, key)

    def close(self):
        self.fixture("FCLOSE", self.writer)
        self.publish("BC")

    def destination(self, call_id):
        # E is a separate connection/commit and a synthetic SQL sink only; no network send API.
        e = self.session("owner")
        self.begin(e)
        self.sql(e, "INSERT INTO mpt_poc.synthetic_destination_call VALUES(%s,'SYNTH-INBOX','N-OLD-KEY','AUTH-N-OLD','E_CALL')", (call_id,))
        self.sql(e, """INSERT INTO mpt_poc.synthetic_destination_receipt
                   VALUES('SYNTH-INBOX','N-OLD-KEY','AUTH-N-OLD','synthetic-payload-v1')
                   ON CONFLICT(destination_id,dedup_key) DO NOTHING""")
        row = self.sql(e, """SELECT authorization_id,payload_fingerprint FROM
                       mpt_poc.synthetic_destination_receipt WHERE destination_id='SYNTH-INBOX'
                       AND dedup_key='N-OLD-KEY'""")
        if row != [("AUTH-N-OLD", "synthetic-payload-v1")]:
            e.rollback()
            raise AssertionError("destination identity conflict")
        self.commit(e)

    def scenario(self, name):
        if name in COVERAGE_SCENARIOS:
            run_coverage(self,name)
            return
        if name == "DELIVERY-FORGE-01":
            forged_notice = """INSERT INTO mpt_poc.notification
                VALUES('P-A','N-FAKE','B1','POSITION_COMMAND','EV-1',NULL,
                'SYNTH-DELIVERY','1','SYNTH-INBOX','FAKE','ACKED')"""
            self.expect_error(self.writer,"42501",forged_notice)
            # Exercise the trigger separately as fixture owner, without runtime grant denial masking it.
            self.expect_error(self.owner,"P0001",forged_notice)
            forged_outbox = """INSERT INTO mpt_poc.outbox_event
                (position_id,outbox_id,batch_id,command_event_id,notification_id,dispatch_status)
                VALUES('P-A','OB-FAKE','B1','EV-1','N-FAKE','ACKED')"""
            self.expect_error(self.writer,"42501",forged_outbox)
            self.expect_error(self.owner,"P0001",forged_outbox)
            self.check("NO_DELIVERY",[(0,0,0,0,0,0)])
            self.fixture("FNOTICE",self.writer)
            rows=self.sql(self.owner,"SELECT delivery_status FROM notification")
            if rows != [("READY",)]: raise AssertionError("legitimate initial notification")
            rows=self.sql(self.owner,"SELECT dispatch_status,lease_token FROM outbox_event")
            if rows != [("PENDING",None)]: raise AssertionError("legitimate initial outbox")
            self.check("FRONTIER",[(0,)])
        elif name in {"T4-ACK-AUTH","T4-ACK-RECHECK"}:
            self.notice()
            phase="AUTHORIZE" if name=="T4-ACK-AUTH" else "RECHECK"
            if phase=="RECHECK": self.deliver("AUTHORIZE","BASE-AUTH")
            self.call(self.dispatch,"T4","P-A","N-OLD","DISP",self.depoch,phase,"LOST-OP",ack=False)
            # State changes after the original decision must not retrospectively change its receipt.
            self.close()
            reply=self.call(self.dispatch,"T4","P-A","N-OLD","DISP",self.depoch,phase,"LOST-OP")
            if reply!="SEND_AUTHORIZED": raise AssertionError("historical response changed")
            self.expect_error(self.dispatch,"P0001",self.ops["T4"],
                ("P-A","N-OLD","OTHER-WORKER",self.depoch,phase,"LOST-OP"))
            count=self.sql(self.owner,"SELECT count(*) FROM delivery_audit WHERE audit_id='LOST-OP'")
            if count!=[(1,)]: raise AssertionError("duplicate operation audit")
            count=self.sql(self.owner,"SELECT count(*) FROM t4_operation_receipt WHERE operation_id='LOST-OP'")
            if count!=[(1,)]: raise AssertionError("duplicate operation receipt")
            self.check("DELIVERY",[("SEND_AUTHORIZED",1,0,0)])
            # A replay response is not a new permission to call. A fresh check observes closure.
            self.deliver("RECHECK","FRESH-CHECK")
            self.check("DELIVERY",[("SUPPRESSED_AFTER_AUTHORIZATION",1,0,0)])
        elif name in {"POC-T24","HOLD-PENDING-CLOSE"}:
            self.notice()
            self.fixture("FCLOSE",self.writer)
            if name=="POC-T24": self.publish("BC")
            self.deliver("AUTHORIZE","CLOSE-BEFORE-AUTH")
            status="SUPPRESSED" if name=="POC-T24" else "HOLD_PENDING_CLOSE"
            self.check("DELIVERY",[(status,0,0,0)])
        elif name == "FIXED-CUT":
            self.publish()
            evaluator=self.session("evaluator")
            cut=self.call(evaluator,"CUT","P-A","CUT-1","C-FIXED")
            self.fixture("FCHAIN",self.writer)
            self.begin(evaluator)
            before=self.sql(evaluator,self.oracles["HISTORICAL"],(cut,))
            self.publish("B2")  # distinct publisher connection commits between READ COMMITTED reads
            after=self.sql(evaluator,self.oracles["HISTORICAL"],(cut,))
            if before!=[(1,)] or after!=before: raise AssertionError("fixed cut changed")
            self.commit(evaluator)
            self.call(evaluator,"T2B","ATT-FIXED","P-A",cut)
        elif name == "T2-TP-FK-CYCLE":
            self.publish()
            evaluator=self.session("evaluator")
            cut=self.call(evaluator,"CUT","P-A","CUT-1","C-CYCLE") # committed T2a
            self.begin(self.pub)
            self.op(self.pub,"TP","P-A","B1","PUB",self.epoch)
            def t2b():
                return self.call(evaluator,"T2B","ATT-CYCLE","P-A",cut)
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                future=pool.submit(t2b)
                try:
                    self.wait_blocked(evaluator,self.pub)
                    self.commit(self.pub)
                    if future.result(timeout=self.config["checkpoint_timeout_seconds"])!="ATT-CYCLE":
                        raise AssertionError("attempt missing")
                except Exception:
                    self.pub.rollback()
                    evaluator.cancel()
                    raise
            self.check("SHARED_ATTEMPTS",[(1,1,1,1)])
        elif name == "blocked_recovery":
            self.publish()
            self.fixture("FCHAIN", self.writer)
            content_before=self.sql(self.owner,self.oracles["CONTENT"])
            recovery = self.session("recovery")
            self.begin(recovery)
            self.sql(recovery, "SELECT mpt_poc.block_batch('P-A','B2',0,'synthetic block')")
            self.commit(recovery)
            insert = "INSERT INTO mpt_poc.publication_member VALUES('P-A','B2',2,NULL,999,NULL)"
            self.expect_error(self.writer, "P0001", insert)
            self.expect_error(self.writer, "42501", self.ops["RECOVER"], ("P-A","B2",1,"REC1","retry unchanged"))
            self.expect_error(self.pub, "P0001", self.ops["TP"], ("P-A","B3","PUB",self.epoch))
            self.call(recovery, "RECOVER", "P-A","B2",1,"REC1","retry unchanged")
            self.call(recovery, "RECOVER", "P-A","B2",1,"REC1","retry unchanged")
            self.check("RECOVERY_COUNT", [(1,)])
            self.expect_error(self.writer, "P0001", insert)  # recovery never unfreezes content
            self.publish("B2")
            self.publish("B3")
            self.check("FRONTIER", [(3,)])
            self.check("PROJECTION", [(3,)])
            self.check("BLOCKED", [("PUBLISHED", True, 3)])
            if self.sql(self.owner,self.oracles["CONTENT"])!=content_before:
                raise AssertionError("recovery/publication changed batch content")
        elif name == "stale_worker":
            self.call(self.pub, "TP_RELEASE", "P-A","PUB",self.epoch)
            new = self.session("publisher")
            epoch2 = self.call(new, "TP_ACQUIRE", "P-A","PUB2",self.config["lease_ttl"])
            if epoch2 <= self.epoch:
                raise AssertionError("epoch did not advance")
            self.expect_error(self.pub, "P0001", self.ops["TP"], ("P-A","B1","PUB",self.epoch))
            self.expect_error(new, "P0001", self.ops["TP"], ("P-A","B1","PUB2",epoch2+1))
            self.check("FRONTIER", [(0,)])
            self.call(new, "TP", "P-A","B1","PUB2",epoch2)
            self.check("FRONTIER", [(1,)])
        elif name == "concurrent_publish":
            other = self.session("publisher")
            a, b = self.race(self.pub, other, "TP", ("P-A","B1","PUB",self.epoch),
                             ("P-A","B1","PUB",self.epoch))
            if (a,b) != (1,1):
                raise AssertionError("publication retry diverged")
            self.check("FRONTIER", [(1,)])
        elif name == "concurrent_cut":
            self.publish()
            a, b = self.session("evaluator"), self.session("evaluator")
            first, second = self.race(a,b,"CUT",("P-A","CUT-1","CUT-A"),("P-A","CUT-1","CUT-B"))
            if first != second:
                raise AssertionError("canonical cut IDs differ")
            self.check("CUT_COUNT", [(1,)])
            self.call(a,"T2B","ATT-A","P-A",first)
            self.call(b,"T2B","ATT-B","P-A",second)
            self.check("SHARED_ATTEMPTS",[(2,1,1,1)])
            self.fixture("FCHAIN",self.writer)
            self.publish("B2")
            self.check("SHARED_ATTEMPTS",[(2,1,1,1)])
            if self.sql(self.owner,self.oracles["HISTORICAL"],(first,)) != [(1,)]:
                raise AssertionError("concurrent attempts lost their historical cut")
        elif name == "compound":
            self.publish()
            self.fixture("FB23", self.writer)
            self.publish("B23")
            self.check("FRONTIER", [(2,)])
            self.check("PROJECTION", [(3,)])
        elif name == "ack_loss":
            self.notice(ack=False)
            if self.publish() != 1:
                raise AssertionError("TP retry")
            self.deliver("AUTHORIZE","AUTH1")
            if self.deliver("RECHECK","CHECK1") != "SEND_AUTHORIZED":
                raise AssertionError("send not authorized")
            self.destination("CALL1")
            self.log("DESTINATION_COMMITTED_ACK_DROPPED")
            self.destination("CALL2")
            self.deliver("ACK","ACK1")
            self.check("DELIVERY", [("ACKED",1,2,1)])
        elif name in {"t25a","t25b","t13a"}:
            self.notice()
            if name == "t13a":
                r = self.session("recovery")
                self.call(r,"REVOKE","T-A","U-A",1,"synthetic revocation")
                self.deliver("AUTHORIZE","REVOKED")
                self.check("DELIVERY", [("SUPPRESSED",0,0,0)])
            else:
                self.deliver("AUTHORIZE","AUTH1")
                if name == "t25a":
                    self.close()
                    self.deliver("RECHECK","CHECK1")
                    self.check("DELIVERY", [("SUPPRESSED_AFTER_AUTHORIZATION",1,0,0)])
                else:
                    if self.deliver("RECHECK","CHECK1") != "SEND_AUTHORIZED":
                        raise AssertionError("last check failed")
                    self.log("LAST_CHECK_COMMITTED")
                    self.close()
                    self.destination("CALL1")
                    self.deliver("ACK","ACK1")
                    self.check("DELIVERY", [("ACKED",1,1,1)])
        elif name in {"notify","quiet"}:
            self.publish()
            evaluator = self.session("evaluator")
            cut = self.call(evaluator,"CUT","P-A","CUT-1","C-RUN")
            self.call(evaluator,"T2B","ATT-RUN","P-A",cut)
            self.call(self.writer,"T3","P-A","ATT-RUN","RES-RUN","BR1","a"*64,name=="notify",ack=False)
            self.call(self.writer,"T3","P-A","ATT-RUN","RES-RUN","BR1","a"*64,name=="notify")
            self.expect_error(self.writer,"P0001",self.ops["T3"],
                ("P-A","ATT-RUN","RES-RUN","BR1","b"*64,name=="notify"))
            decision = "NOTIFY" if name=="notify" else "DO_NOT_NOTIFY"
            count = 1 if name=="notify" else 0
            self.check("RESULT", [("PERSISTED_PENDING_PUBLICATION",decision,count,count)])
            self.publish("BR1")
            self.check("RESULT", [("PUBLISHED",decision,count,count)])
        elif name == "privileges":
            reader = self.session("reader")
            self.expect_error(reader, "42501", "SELECT * FROM mpt_poc.publication_batch")
            self.expect_error(self.writer, "42501", self.ops["TP"], ("P-A","B1","PUB",self.epoch))
            self.expect_error(self.writer, "42501", "UPDATE mpt_poc.public_projection SET position_version=99")
            self.expect_error(self.writer, "42501", "TRUNCATE mpt_poc.publication_member")
            self.publish()
            if self.sql(reader, "SELECT count(*) FROM mpt_poc.published_positions") != [(1,)]:
                raise AssertionError("public view must expose one published row")
        else:
            raise RuntimeError("scenario is blocked or unsupported")

    def close_connections(self):
        for conn in self.connections:
            conn.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=sorted(SCENARIOS))
    parser.add_argument("--approval", type=Path, required=True)
    parser.add_argument("--approved-config-sha256", required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.approval.read_text(encoding="utf-8"))
    # Output opened exclusively: never overwrite prior FAIL/INCONCLUSIVE evidence.
    with args.evidence.open("x", encoding="utf-8") as output:
        lab = Lab(config, output)
        lab.log("start", scenario=args.scenario, execution_status="NOT_RUN")
        if args.scenario in BLOCKED_SCENARIOS:
            lab.log("blocked",reason=BLOCKED_SCENARIOS[args.scenario],
                    coverage_status="BLOCKING_EXECUTION_REVIEW",execution_status="NOT_RUN")
            return  # no connection, fixture or process operation, regardless of config flags
        if args.scenario == "t13b":
            lab.log("blocked", reason="PENDING_HUMAN_APPROVAL", execution_status="NOT_RUN",
                    proposed_sequence=["AUTH_COMMITTED","REVOKE_COMMITTED","RECHECK","ZERO_CALLS"],
                    proposed_state="SUPPRESSED_AFTER_AUTHORIZATION")
            return
        if (not config.get("execution_authorized") or not config.get("environment_frozen")
                or args.scenario not in config.get("approved_scenarios", [])
                or any(config.get(k) in (None,"UNRESOLVED","") for k in
                       ("image_digest","architecture","driver_version","python_version",
                        "cryptography_version","manifest_sha256","attestation_sha256"))):
            lab.log("blocked", reason="approval/environment not frozen", execution_status="NOT_RUN")
            return
        scenario_started=False
        try:
            provenance=verify_files(ROOT.parent,args.approval,args.approved_config_sha256,config)
            attestation=verify_attestation(config)
            lab.log("provenance",execution_status="NOT_RUN",**provenance,**attestation)
            lab.setup()
            scenario_started=True
            lab.scenario(args.scenario)
            lab.sql(lab.owner, lab.oracles["EVIDENCE"])
            lab.log("verdict", execution_status="PASS")
        except PreflightBlocked as exc:
            lab.log("blocked",execution_status="INCONCLUSIVE" if lab.mutations_started else "NOT_RUN",reason=str(exc))
            raise
        except (TimeoutError, psycopg.OperationalError) as exc:
            lab.log("verdict", execution_status="INCONCLUSIVE" if lab.mutations_started else "NOT_RUN", error=type(exc).__name__)
            raise
        except Exception as exc:
            lab.log("verdict", execution_status="FAIL" if lab.mutations_started else "NOT_RUN",
                    error=type(exc).__name__)
            raise
        finally:
            lab.close_connections()


if __name__ == "__main__":
    main()
