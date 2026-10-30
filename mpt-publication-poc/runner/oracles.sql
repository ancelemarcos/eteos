-- CANDIDATE / NOT_RUN. Named queries; expected values defined by scenarios.
-- BEGIN FRONTIER
SELECT committed_ordinal FROM mpt_poc.publication_barrier WHERE domain_id='D-A';
-- END FRONTIER
-- BEGIN PROJECTION
SELECT position_version FROM mpt_poc.public_projection WHERE position_id='P-A';
-- END PROJECTION
-- BEGIN BLOCKED
SELECT publication_status,content_frozen,state_version FROM mpt_poc.publication_batch
WHERE position_id='P-A' AND batch_id='B2';
-- END BLOCKED
-- BEGIN CUT_COUNT
SELECT count(*) FROM mpt_poc.publication_cut WHERE domain_id='D-A' AND ordinal=1
AND resolution_policy_version='CUT-1';
-- END CUT_COUNT
-- BEGIN DELIVERY
SELECT n.delivery_status,(SELECT count(*) FROM mpt_poc.send_authorization),
(SELECT count(*) FROM mpt_poc.synthetic_destination_call),
(SELECT count(*) FROM mpt_poc.synthetic_destination_receipt)
FROM mpt_poc.notification n WHERE n.position_id='P-A' AND n.notification_id='N-OLD';
-- END DELIVERY
-- BEGIN RESULT
SELECT b.publication_status,d.decision,
(SELECT count(*) FROM mpt_poc.notification WHERE result_id=r.result_id),
(SELECT count(*) FROM mpt_poc.outbox_event WHERE result_id=r.result_id)
FROM mpt_poc.assessment_result r JOIN mpt_poc.publication_batch b USING(position_id,batch_id)
JOIN mpt_poc.notification_decision d USING(position_id,result_id);
-- END RESULT
-- BEGIN EVIDENCE
SELECT jsonb_build_object(
 'batches',(SELECT coalesce(jsonb_agg(to_jsonb(x) ORDER BY x.position_id,x.batch_id),'[]')
            FROM mpt_poc.publication_batch x),
 'recovery',(SELECT coalesce(jsonb_agg(to_jsonb(x) ORDER BY x.request_id),'[]')
            FROM mpt_poc.batch_recovery_audit x),
 'leases',(SELECT coalesce(jsonb_agg(to_jsonb(x) ORDER BY x.position_id,x.purpose),'[]')
            FROM mpt_poc.worker_lease x),
 'authorizations',(SELECT coalesce(jsonb_agg(to_jsonb(x) ORDER BY x.position_id,x.authorization_id),'[]')
            FROM mpt_poc.send_authorization x),
 'audit',(SELECT coalesce(jsonb_agg(to_jsonb(x) ORDER BY x.position_id,x.audit_id),'[]')
            FROM mpt_poc.delivery_audit x));
-- END EVIDENCE
-- BEGIN RECOVERY_COUNT
SELECT count(*) FROM mpt_poc.batch_recovery_audit WHERE request_id='REC1';
-- END RECOVERY_COUNT
-- BEGIN NO_DELIVERY
SELECT (SELECT count(*) FROM mpt_poc.notification),
 (SELECT count(*) FROM mpt_poc.outbox_event),(SELECT count(*) FROM mpt_poc.send_authorization),
 (SELECT count(*) FROM mpt_poc.synthetic_destination_call),(SELECT count(*) FROM mpt_poc.synthetic_destination_receipt),
 (SELECT count(*) FROM mpt_poc.published_positions);
-- END NO_DELIVERY
-- BEGIN T4_OPERATIONS
SELECT operation_id,response FROM mpt_poc.t4_operation_receipt ORDER BY operation_id;
-- END T4_OPERATIONS
-- BEGIN SHARED_ATTEMPTS
SELECT count(*),count(DISTINCT cut_id),min(position_version),max(position_version)
FROM mpt_poc.assessment_attempt;
-- END SHARED_ATTEMPTS
-- BEGIN HISTORICAL
SELECT max(r.version) FROM mpt_poc.position_revision r JOIN mpt_poc.publication_batch b USING(position_id,batch_id)
JOIN mpt_poc.publication_cut c ON c.domain_id=b.domain_id
WHERE r.position_id='P-A' AND c.cut_id=%s AND b.publication_status='PUBLISHED' AND b.ordinal<=c.ordinal;
-- END HISTORICAL
-- BEGIN CONTENT
SELECT b.batch_id,b.fingerprint,
 (SELECT jsonb_agg(to_jsonb(m) ORDER BY member_order) FROM mpt_poc.publication_member m
  WHERE m.position_id=b.position_id AND m.batch_id=b.batch_id)
FROM mpt_poc.publication_batch b WHERE b.position_id='P-A' ORDER BY b.batch_id;
-- END CONTENT
