-- CANDIDATE / NOT_RUN. Named psycopg parameterized statements; no whole-file execution.
-- BEGIN T4_RENEW
SELECT mpt_poc.t4_renew(%s,%s,%s,%s::interval);
-- END T4_RENEW
-- BEGIN T4_RELEASE
SELECT mpt_poc.t4_release(%s,%s,%s);
-- END T4_RELEASE
-- BEGIN TP_RENEW
SELECT mpt_poc.tp_renew(%s,%s,%s,%s::interval);
-- END TP_RENEW
-- BEGIN BLOCK
SELECT mpt_poc.block_batch(%s,%s,%s,%s);
-- END BLOCK
-- BEGIN TP_ACQUIRE
SELECT mpt_poc.tp_acquire(%s,%s,%s::interval);
-- END TP_ACQUIRE
-- BEGIN TP
SELECT mpt_poc.publish_batch(%s,%s,%s,%s);
-- END TP
-- BEGIN TP_RELEASE
SELECT mpt_poc.tp_release(%s,%s,%s);
-- END TP_RELEASE
-- BEGIN T4_ACQUIRE
SELECT mpt_poc.t4_acquire(%s,%s,%s::interval);
-- END T4_ACQUIRE
-- BEGIN T4
SELECT mpt_poc.delivery_step(%s,%s,%s,%s,%s,%s);
-- END T4
-- BEGIN CUT
SELECT mpt_poc.capture_cut(%s,%s,%s);
-- END CUT
-- BEGIN RECOVER
SELECT mpt_poc.recover_batch(%s,%s,%s,%s,%s);
-- END RECOVER
-- BEGIN REVOKE
SELECT mpt_poc.revoke_access(%s,%s,%s,%s);
-- END REVOKE
-- BEGIN LOCK
SELECT mpt_poc.lock_position(%s);
-- END LOCK
-- BEGIN FORCE_CONSTRAINTS
SET CONSTRAINTS ALL IMMEDIATE;
-- END FORCE_CONSTRAINTS
-- BEGIN T3
SELECT mpt_poc.finalize_synthetic(%s,%s,%s,%s,%s,%s);
-- END T3
-- BEGIN T2B
INSERT INTO mpt_poc.assessment_attempt
(position_id,attempt_id,domain_id,cut_id,position_version,plan_version,rule_id,rule_version,
 parameter_identity,execution_status,assessment_mode,decision_time_observed)
SELECT pos.position_id,%s,c.domain_id,c.cut_id,
 (SELECT max(r.version) FROM mpt_poc.position_revision r JOIN mpt_poc.publication_batch b USING(position_id,batch_id)
  WHERE r.position_id=pos.position_id AND b.publication_status='PUBLISHED' AND b.ordinal<=c.ordinal),
 (SELECT max(r.version) FROM mpt_poc.plan_revision r JOIN mpt_poc.publication_batch b USING(position_id,batch_id)
  WHERE r.position_id=pos.position_id AND b.publication_status='PUBLISHED' AND b.ordinal<=c.ordinal),
 'RULE','1','PARAM','RUNNING','ONLINE','2026-01-01T10:05:00Z'
FROM mpt_poc.position pos JOIN mpt_poc.publication_cut c ON c.domain_id=pos.domain_id
WHERE pos.position_id=%s AND c.cut_id=%s RETURNING attempt_id;
-- END T2B
