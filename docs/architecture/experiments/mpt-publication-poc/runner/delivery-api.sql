-- CANDIDATE / NOT_RUN. Apply only after schema.sql with separately authorized migration identity.
BEGIN;
SET LOCAL ROLE mpt_owner;
SET LOCAL search_path=mpt_poc,pg_catalog;
CREATE TABLE t4_operation_receipt (
 position_id text NOT NULL, operation_id text NOT NULL,
 notification_id text NOT NULL, request_payload jsonb NOT NULL,
 request_fingerprint text NOT NULL, response text NOT NULL,
 PRIMARY KEY(position_id,operation_id),
 FOREIGN KEY(position_id,operation_id) REFERENCES delivery_audit(position_id,audit_id),
 FOREIGN KEY(position_id,notification_id) REFERENCES notification
);
CREATE TRIGGER t4_receipt_immutable BEFORE UPDATE OR DELETE ON t4_operation_receipt
 FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
REVOKE ALL ON t4_operation_receipt FROM PUBLIC;
GRANT SELECT ON t4_operation_receipt TO mpt_dispatcher;
-- Synthetic sink proof is separate from sender transaction, but queryable in this lab.
CREATE FUNCTION has_delivery_proof(p text,n text) RETURNS boolean
LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog,mpt_poc,pg_temp AS $$
 SELECT EXISTS (
 SELECT 1 FROM mpt_poc.notification nt
 JOIN mpt_poc.send_authorization a USING(position_id,notification_id)
 JOIN mpt_poc.synthetic_destination_receipt r ON r.destination_id=nt.destination_id
   AND r.dedup_key=nt.dedup_key AND r.authorization_id=a.authorization_id
 JOIN mpt_poc.synthetic_destination_call c ON c.destination_id=r.destination_id
   AND c.dedup_key=r.dedup_key AND c.authorization_id=r.authorization_id
 WHERE nt.position_id=p AND nt.notification_id=n)
$$;
REVOKE ALL ON FUNCTION has_delivery_proof(text,text) FROM PUBLIC;
CREATE FUNCTION guard_delivery_transition() RETURNS trigger
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,mpt_poc,pg_temp AS $$
DECLARE has_auth boolean;
BEGIN
 SELECT EXISTS(SELECT 1 FROM mpt_poc.send_authorization
   WHERE position_id=NEW.position_id AND notification_id=NEW.notification_id) INTO has_auth;
 IF TG_TABLE_NAME='notification' THEN
   IF OLD.delivery_status IN ('ACKED','SUPPRESSED','SUPPRESSED_AFTER_AUTHORIZATION','EXPIRED')
     AND NEW.delivery_status<>OLD.delivery_status THEN RAISE EXCEPTION 'terminal delivery'; END IF;
   IF NEW.delivery_status IN ('SEND_AUTHORIZED','SUPPRESSED_AFTER_AUTHORIZATION','ACKED') AND NOT has_auth THEN
     RAISE EXCEPTION 'authorization required'; END IF;
   IF NEW.delivery_status='SUPPRESSED' AND has_auth THEN RAISE EXCEPTION 'preserve prior authorization'; END IF;
   IF NEW.delivery_status='DELIVERED' THEN RAISE EXCEPTION 'DELIVERED transition unsupported by candidate'; END IF;
   IF NEW.delivery_status='ACKED' AND NOT mpt_poc.has_delivery_proof(NEW.position_id,NEW.notification_id) THEN
     RAISE EXCEPTION 'committed synthetic call and receipt required'; END IF;
 ELSE
   IF OLD.dispatch_status IN ('ACKED','SUPPRESSED') AND NEW.dispatch_status<>OLD.dispatch_status THEN
     RAISE EXCEPTION 'terminal outbox'; END IF;
   IF NEW.dispatch_status IN ('CLAIMED','ACKED') AND NOT has_auth THEN RAISE EXCEPTION 'authorization required'; END IF;
   IF NEW.dispatch_status='ACKED' AND (NOT mpt_poc.has_delivery_proof(NEW.position_id,NEW.notification_id)
     OR NOT EXISTS(SELECT 1 FROM mpt_poc.notification WHERE position_id=NEW.position_id
       AND notification_id=NEW.notification_id AND delivery_status='ACKED')) THEN
     RAISE EXCEPTION 'outbox flag is not delivery proof'; END IF;
 END IF;
 RETURN NEW;
END;
$$;
REVOKE ALL ON FUNCTION guard_delivery_transition() FROM PUBLIC;
CREATE TRIGGER delivery_transition BEFORE UPDATE ON notification
 FOR EACH ROW EXECUTE FUNCTION guard_delivery_transition();
CREATE TRIGGER outbox_transition BEFORE UPDATE ON outbox_event
 FOR EACH ROW EXECUTE FUNCTION guard_delivery_transition();
CREATE FUNCTION delivery_step(p text,n text,w text,e bigint,phase text,audit_key text)
RETURNS text LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,mpt_poc,pg_temp AS $$
DECLARE nt mpt_poc.notification%ROWTYPE; pos mpt_poc.position%ROWTYPE;
  rg mpt_poc.recipient_guard%ROWTYPE; life text; ver bigint; closing text; outcome text;
  auth text; ob text; payload jsonb; digest text; prior mpt_poc.t4_operation_receipt%ROWTYPE;
BEGIN
  IF phase IS NULL OR phase NOT IN ('AUTHORIZE','RECHECK','ACK') OR audit_key IS NULL OR audit_key='' THEN
    RAISE EXCEPTION 'invalid phase or operation ID'; END IF;
  PERFORM mpt_poc.lock_position(p);
  payload:=jsonb_build_array('T4-v1',p,n,w,e,phase,session_user::text);
  digest:=encode(sha256(convert_to(payload::text,'UTF8')),'hex');
  SELECT * INTO prior FROM mpt_poc.t4_operation_receipt WHERE position_id=p AND operation_id=audit_key;
  IF FOUND THEN
    IF prior.request_payload IS DISTINCT FROM payload OR prior.request_fingerprint<>digest THEN
      RAISE EXCEPTION 'T4_IDEMPOTENCY_CONFLICT'; END IF;
    -- Historical response only: never re-evaluate policy or refresh a lease on retry.
    RETURN prior.response;
  END IF;
  PERFORM mpt_poc.check_lease(p,'T4',w,e);
  SELECT * INTO STRICT pos FROM mpt_poc.position WHERE position_id=p;
  SELECT * INTO STRICT rg FROM mpt_poc.recipient_guard
    WHERE tenant_id=pos.tenant_id AND owner_id=pos.owner_id;
  SELECT * INTO STRICT nt FROM mpt_poc.notification WHERE position_id=p AND notification_id=n FOR UPDATE;
  SELECT outbox_id INTO STRICT ob FROM mpt_poc.outbox_event
    WHERE position_id=p AND notification_id=n FOR UPDATE;
  IF NOT EXISTS(SELECT 1 FROM mpt_poc.publication_batch
    WHERE position_id=p AND batch_id=nt.batch_id AND publication_status='PUBLISHED') THEN
    RAISE EXCEPTION 'notification not published'; END IF;
  SELECT authorization_id INTO auth FROM mpt_poc.send_authorization WHERE position_id=p AND notification_id=n;
  SELECT r.lifecycle,r.version INTO life,ver FROM mpt_poc.public_projection pp
    JOIN mpt_poc.position_revision r ON r.position_id=pp.position_id AND r.version=pp.position_version
    WHERE pp.position_id=p;
  SELECT pending_close_command INTO closing FROM mpt_poc.position_guard WHERE position_id=p;
  IF nt.delivery_status IN ('ACKED','SUPPRESSED','SUPPRESSED_AFTER_AUTHORIZATION','EXPIRED') THEN
    INSERT INTO mpt_poc.delivery_audit VALUES(p,audit_key,n,auth,nt.delivery_status,phase);
    INSERT INTO mpt_poc.t4_operation_receipt VALUES(p,audit_key,n,payload,digest,nt.delivery_status);
    RETURN nt.delivery_status;
  END IF;
  IF phase='ACK' THEN
    IF auth IS NULL OR NOT EXISTS(SELECT 1 FROM mpt_poc.outbox_event WHERE position_id=p
      AND outbox_id=ob AND lease_token=w||':'||e::text AND dispatch_status='CLAIMED') THEN
      RAISE EXCEPTION 'stale ACK or missing authorization'; END IF;
    IF NOT mpt_poc.has_delivery_proof(p,n) THEN RAISE EXCEPTION 'ACK_WITHOUT_RECEIPT'; END IF;
    outcome:='ACKED';
  ELSIF auth IS NOT NULL AND NOT rg.access_allowed THEN
    -- Do not silently approve PUB-T13B. Proposed zero-call branch remains gated.
    RAISE EXCEPTION 'PENDING_HUMAN_APPROVAL: PUB-T13B';
  ELSIF life IS DISTINCT FROM 'OPEN_DECLARED' OR NOT rg.access_allowed THEN
    outcome:=CASE WHEN auth IS NULL THEN 'SUPPRESSED' ELSE 'SUPPRESSED_AFTER_AUTHORIZATION' END;
  ELSIF closing IS NOT NULL THEN
    -- Hold cannot authorize a call, even if an earlier historical authorization exists.
    outcome:='HOLD_PENDING_CLOSE';
  ELSE
    IF auth IS NULL THEN
      IF phase<>'AUTHORIZE' THEN RAISE EXCEPTION 'missing authorization'; END IF;
      auth:='AUTH-'||n;
      INSERT INTO mpt_poc.send_authorization VALUES
        (p,auth,n,pos.tenant_id,pos.owner_id,rg.access_version,nt.policy_version,ver);
    END IF;
    outcome:='SEND_AUTHORIZED';
  END IF;
  UPDATE mpt_poc.notification SET delivery_status=outcome WHERE position_id=p AND notification_id=n;
  UPDATE mpt_poc.outbox_event SET dispatch_status=
      CASE WHEN outcome='ACKED' THEN 'ACKED'
           WHEN outcome IN ('SUPPRESSED','SUPPRESSED_AFTER_AUTHORIZATION') THEN 'SUPPRESSED'
           WHEN outcome='HOLD_PENDING_CLOSE' THEN 'PENDING' ELSE 'CLAIMED' END,
    lease_token=w||':'||e::text,
    lease_until_observed=(SELECT expires_at FROM mpt_poc.worker_lease WHERE position_id=p AND purpose='T4')
    WHERE position_id=p AND outbox_id=ob;
  INSERT INTO mpt_poc.delivery_audit VALUES(p,audit_key,n,auth,outcome,phase);
  INSERT INTO mpt_poc.t4_operation_receipt VALUES(p,audit_key,n,payload,digest,outcome);
  RETURN outcome;
END;
$$;
CREATE FUNCTION revoke_access(t text,o text,expected bigint,why text) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,mpt_poc,pg_temp AS $$
BEGIN
  PERFORM 1 FROM mpt_poc.recipient_guard WHERE tenant_id=t AND owner_id=o FOR UPDATE;
  UPDATE mpt_poc.recipient_guard SET access_version=access_version+1,access_allowed=false
    WHERE tenant_id=t AND owner_id=o AND access_version=expected;
  IF NOT FOUND THEN RAISE EXCEPTION 'revocation CAS conflict'; END IF;
  INSERT INTO mpt_poc.access_audit VALUES(t,o,expected+1,false,why);
END;
$$;
REVOKE ALL ON FUNCTION delivery_step(text,text,text,bigint,text,text),revoke_access(text,text,bigint,text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION delivery_step(text,text,text,bigint,text,text) TO mpt_dispatcher;
GRANT EXECUTE ON FUNCTION revoke_access(text,text,bigint,text) TO mpt_recovery;
CREATE FUNCTION finalize_synthetic(p text,a text,r text,b text,fp text,notify boolean)
RETURNS text LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,mpt_poc,pg_temp AS $$
DECLARE attempt mpt_poc.assessment_attempt%ROWTYPE; prior mpt_poc.assessment_result%ROWTYPE;
  v_decision text; v_policy text;
BEGIN
  IF notify IS NULL THEN RAISE EXCEPTION 'decision required'; END IF;
  v_decision:=CASE WHEN notify THEN 'NOTIFY' ELSE 'DO_NOT_NOTIFY' END;
  v_policy:=CASE WHEN notify THEN 'SYNTH-NOTIFY' ELSE 'SYNTH-QUIET' END;
  PERFORM mpt_poc.lock_position(p);
  SELECT * INTO STRICT attempt FROM mpt_poc.assessment_attempt WHERE position_id=p AND attempt_id=a FOR UPDATE;
  SELECT * INTO prior FROM mpt_poc.assessment_result WHERE position_id=p AND attempt_id=a;
  IF FOUND THEN
    IF ROW(prior.result_id,prior.batch_id,prior.fingerprint) IS DISTINCT FROM ROW(r,b,fp)
      OR NOT EXISTS(SELECT 1 FROM mpt_poc.notification_decision d
        WHERE d.position_id=p AND d.result_id=r AND d.decision=v_decision AND d.policy_id=v_policy
        AND d.policy_version='1') THEN RAISE EXCEPTION 'RESULT_CONFLICT'; END IF;
    RETURN prior.batch_id;
  END IF;
  IF attempt.execution_status<>'RUNNING' THEN RAISE EXCEPTION 'terminal attempt'; END IF;
  INSERT INTO mpt_poc.publication_batch(position_id,batch_id,domain_id,origin_type,origin_id,fingerprint,publication_status)
    VALUES(p,b,attempt.domain_id,'ASSESSMENT_RESULT',r,fp,'PERSISTED_PENDING_PUBLICATION');
  INSERT INTO mpt_poc.assessment_result VALUES(p,r,a,b,NULL,fp,'EVALUABLE','USER_REFERENCE',
    'synthetic reference','synthetic only; no market claim');
  INSERT INTO mpt_poc.notification_decision VALUES(p,r,v_policy,'1',v_decision,'synthetic policy');
  INSERT INTO mpt_poc.publication_member VALUES(p,b,1,NULL,NULL,r);
  IF notify THEN
    INSERT INTO mpt_poc.notification VALUES(p,'N-'||r,b,'ASSESSMENT_RESULT',NULL,r,v_policy,'1',
      'SYNTH-INBOX','KEY-'||p||'-'||r,'READY');
    INSERT INTO mpt_poc.outbox_event(position_id,outbox_id,batch_id,result_id,notification_id,dispatch_status)
      VALUES(p,'OB-'||r,b,r,'N-'||r,'PENDING');
  END IF;
  UPDATE mpt_poc.assessment_attempt SET execution_status='COMPLETED' WHERE position_id=p AND attempt_id=a;
  RETURN b;
END;
$$;
REVOKE ALL ON FUNCTION finalize_synthetic(text,text,text,text,text,boolean) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION finalize_synthetic(text,text,text,text,text,boolean) TO mpt_writer;
COMMIT;
