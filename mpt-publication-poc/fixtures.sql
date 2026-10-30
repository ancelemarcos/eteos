-- PROPOSED / NOT EXECUTED. Synthetic fixture fragments, not a production seed.
-- A future orchestrator selects named sections; do not execute the whole file blindly.
-- No DB, container, SQL or test was executed when authoring this artifact.
-- Fixed timestamps are observed synthetic metadata, never proof of publication time.
-- Reset means a fresh disposable schema under separately approved execution; no DROP here.

-- BEGIN FIXTURE F0@2: empty domains, two positions with same owner and one foreign owner.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
INSERT INTO publication_domain VALUES ('D-A','CUT-1'),('D-B','CUT-1');
-- F0 revision @2: supported synthetic policies are explicit, immutable pairs.
INSERT INTO domain_resolution_policy VALUES ('D-A','CUT-1'),('D-A','CUT-2'),('D-B','CUT-1');
INSERT INTO publication_barrier VALUES ('D-A',0),('D-B',0);
INSERT INTO recipient_guard VALUES ('T-A','U-A',1,true),('T-B','U-B',1,true);
INSERT INTO access_audit VALUES ('T-A','U-A',1,true,'synthetic initial grant'),
 ('T-B','U-B',1,true,'synthetic initial grant');
INSERT INTO position VALUES
 ('P-A','D-A','T-A','U-A','SYNTH-ALPHA',0),
 ('P-A2','D-A','T-A','U-A','SYNTH-ALPHA',0),
 ('P-B','D-B','T-B','U-B','SYNTH-BETA',0);
INSERT INTO position_guard(position_id) VALUES ('P-A'),('P-A2'),('P-B');
INSERT INTO plan(position_id) VALUES ('P-A'),('P-A2'),('P-B');
COMMIT;
-- END FIXTURE F0@2

-- BEGIN FIXTURE F1@1: requires F0. Prepare v1; NOT published.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
INSERT INTO command_receipt
 (tenant_id,owner_id,command_id,position_id,actor_id,action,expected_position_version,
 canonical_payload,fingerprint,response_code,response_payload)
VALUES ('T-A','U-A','CMD-1','P-A','U-A','DECLARE',0,
 'DECLARE|P-A|2|100.25|0',
 encode(sha256(convert_to('DECLARE|P-A|2|100.25|0','UTF8')),'hex'),
 'ACCEPTED_PENDING_PUBLICATION','CMD-1|B1');
INSERT INTO publication_batch
 (position_id,batch_id,domain_id,origin_type,origin_id,fingerprint,publication_status)
SELECT 'P-A','B1','D-A','POSITION_COMMAND','CMD-1',fingerprint,
 'PERSISTED_PENDING_PUBLICATION' FROM command_receipt WHERE command_id='CMD-1';
INSERT INTO position_event VALUES
 ('P-A','EV-1','CMD-1','DECLARE',NULL,'2026-01-01T10:00:00Z',NULL);
INSERT INTO position_revision VALUES
 ('P-A',1,NULL,'EV-1','B1','OPEN_DECLARED','LONG',2,100.25,'2026-01-01T10:00:00Z');
INSERT INTO publication_member VALUES ('P-A','B1',1,1,NULL,NULL);
UPDATE position SET persisted_version=1 WHERE position_id='P-A';
COMMIT;
-- END FIXTURE F1@1

-- BEGIN FIXTURE FCHAIN@1: requires F1; two pending successors, separate batches.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
INSERT INTO command_receipt
 (tenant_id,owner_id,command_id,position_id,actor_id,action,expected_position_version,
 canonical_payload,fingerprint,response_code,response_payload)
VALUES
 ('T-A','U-A','CMD-2','P-A','U-A','INCREASE',1,'INCREASE|P-A|1|101|1',
 encode(sha256(convert_to('INCREASE|P-A|1|101|1','UTF8')),'hex'),
 'ACCEPTED_PENDING_PUBLICATION','CMD-2|B2'),
 ('T-A','U-A','CMD-3','P-A','U-A','REDUCE',2,'REDUCE|P-A|1|2',
 encode(sha256(convert_to('REDUCE|P-A|1|2','UTF8')),'hex'),
 'ACCEPTED_PENDING_PUBLICATION','CMD-3|B3');
INSERT INTO publication_batch
 (position_id,batch_id,domain_id,origin_type,origin_id,fingerprint,publication_status)
SELECT 'P-A',CASE command_id WHEN 'CMD-2' THEN 'B2' ELSE 'B3' END,
 'D-A','POSITION_COMMAND',command_id,fingerprint,'PERSISTED_PENDING_PUBLICATION'
 FROM command_receipt WHERE command_id IN ('CMD-2','CMD-3');
INSERT INTO position_event VALUES
 ('P-A','EV-2','CMD-2','INCREASE',NULL,'2026-01-01T10:01:00Z',NULL),
 ('P-A','EV-3','CMD-3','REDUCE',NULL,'2026-01-01T10:02:00Z',NULL);
-- Independent declarative oracle: (2*100.25 + 1*101)/3 = 100.5; reduction keeps average.
INSERT INTO position_revision VALUES
 ('P-A',2,1,'EV-2','B2','OPEN_DECLARED','LONG',3,100.5,'2026-01-01T10:01:00Z'),
 ('P-A',3,2,'EV-3','B3','OPEN_DECLARED','LONG',2,100.5,'2026-01-01T10:02:00Z');
INSERT INTO publication_member VALUES
 ('P-A','B2',1,2,NULL,NULL),('P-A','B3',1,3,NULL,NULL);
UPDATE position SET persisted_version=3 WHERE position_id='P-A';
COMMIT;
-- END FIXTURE FCHAIN@1

-- BEGIN FIXTURE FBLOCK@2: requires FCHAIN; recovery role API, not a TP outcome.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
SELECT mpt_poc.block_batch('P-A','B2',0,'SYNTHETIC_INTEGRITY_BLOCK');
COMMIT;
-- END FIXTURE FBLOCK@2

-- BEGIN FIXTURE FPLAN@1: requires F1; first plan revision, pending.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
INSERT INTO command_receipt
 (tenant_id,owner_id,command_id,position_id,actor_id,action,expected_plan_version,
 canonical_payload,fingerprint,response_code,response_payload)
VALUES ('T-A','U-A','CMD-PLAN','P-A','U-A','REVISE_PLAN',0,'PLAN|P-A|99|105|0',
 encode(sha256(convert_to('PLAN|P-A|99|105|0','UTF8')),'hex'),
 'ACCEPTED_PENDING_PUBLICATION','CMD-PLAN|BP1');
INSERT INTO publication_batch
 (position_id,batch_id,domain_id,origin_type,origin_id,fingerprint,publication_status)
SELECT 'P-A','BP1','D-A','POSITION_COMMAND','CMD-PLAN',fingerprint,
 'PERSISTED_PENDING_PUBLICATION' FROM command_receipt WHERE command_id='CMD-PLAN';
INSERT INTO plan_revision VALUES ('P-A',1,NULL,'BP1','CMD-PLAN',99,105,'synthetic note');
INSERT INTO publication_member VALUES ('P-A','BP1',1,NULL,1,NULL);
UPDATE plan SET persisted_version=1 WHERE position_id='P-A';
COMMIT;
-- END FIXTURE FPLAN@1

-- BEGIN FIXTURE FNOTICE@2: writer supplies payload only; READY/PENDING are database defaults.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
INSERT INTO notification(position_id,notification_id,batch_id,origin_type,command_event_id,result_id,
 policy_id,policy_version,destination_id,dedup_key) VALUES
 ('P-A','N-OLD','B1','POSITION_COMMAND','EV-1',NULL,
 'SYNTH-DELIVERY','1','SYNTH-INBOX','N-OLD-KEY');
INSERT INTO outbox_event
 (position_id,outbox_id,batch_id,command_event_id,notification_id)
VALUES ('P-A','OB-OLD','B1','EV-1','N-OLD');
COMMIT;
-- END FIXTURE FNOTICE@2

-- BEGIN FIXTURE FCLOSE@1: requires F1, no FCHAIN; simulate accepted CLOSE v2.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
INSERT INTO command_receipt
 (tenant_id,owner_id,command_id,position_id,actor_id,action,expected_position_version,
 canonical_payload,fingerprint,response_code,response_payload)
VALUES ('T-A','U-A','CMD-CLOSE','P-A','U-A','CLOSE',1,'CLOSE|P-A|1',
 encode(sha256(convert_to('CLOSE|P-A|1','UTF8')),'hex'),
 'ACCEPTED_PENDING_PUBLICATION','CMD-CLOSE|BC');
INSERT INTO publication_batch
 (position_id,batch_id,domain_id,origin_type,origin_id,fingerprint,publication_status)
SELECT 'P-A','BC','D-A','POSITION_COMMAND','CMD-CLOSE',fingerprint,
 'PERSISTED_PENDING_PUBLICATION' FROM command_receipt WHERE command_id='CMD-CLOSE';
INSERT INTO position_event VALUES
 ('P-A','EV-CLOSE','CMD-CLOSE','CLOSE',NULL,'2026-01-01T10:03:00Z',NULL);
INSERT INTO position_revision VALUES
 ('P-A',2,1,'EV-CLOSE','BC','CLOSED_DECLARED','LONG',0,100.25,'2026-01-01T10:03:00Z');
INSERT INTO publication_member VALUES ('P-A','BC',1,2,NULL,NULL);
UPDATE position SET persisted_version=2 WHERE position_id='P-A';
UPDATE position_guard SET pending_close_command='CMD-CLOSE' WHERE position_id='P-A';
COMMIT;
-- END FIXTURE FCLOSE@1

-- BEGIN FIXTURE FREVOKE@1: requires F0; apply under recipient guard in concurrent scenarios.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
SELECT 1 FROM recipient_guard WHERE tenant_id='T-A' AND owner_id='U-A' FOR UPDATE;
UPDATE recipient_guard SET access_version=2,access_allowed=false WHERE tenant_id='T-A' AND owner_id='U-A';
INSERT INTO access_audit VALUES ('T-A','U-A',2,false,'REV-1 synthetic revocation');
COMMIT;
-- END FIXTURE FREVOKE@1

-- Derived fixture recipes are declarative, not blind executable suffixes:
-- FPUBLISHED@1 = F0 + F1 [+ FNOTICE] then future TP(B1), C1=T2 capture.
-- FRESULT@2 = FPUBLISHED + committed FCUT + separate T2b ATT-1 + result RES-1, batch BR1,
--   evaluability EVALUABLE, content USER_REFERENCE/"synthetic reference",
--   limitation "synthetic only", policy SYNTH-NOTIFY/1; NOTIFY -> N-R1 + OB-R1.
-- FQUIET@2 = same with policy SYNTH-QUIET/1 and DO_NOT_NOTIFY; no notification/outbox.
-- FB23@1 = F0+F1 then approved preparer inserts CMD-23 and EV-2/EV-3,
--   B23 with versions 2/3, quantities 3/2, averages 100.5, member_order 1/2.
--   This is alternative to FCHAIN, never an UPDATE of immutable revisions.
-- Cross-position fixture changes only a reference to P-A2; expected FK rejection.
-- Divergent-command fixture reuses CMD-1 but changes action/target/payload;
--   no fabricated hash: future SQL computes SHA-256 over exact canonical UTF-8 bytes.
-- These recipes require materialized transaction scripts before execution;
-- see REVIEW-NOTES OPEN-02. They are not claimed as completed runnable fixtures.

-- BEGIN FIXTURE FRESULT@2: requires FPUBLISHED, committed FCUT, and no ATT-1.
-- Precondition: B1 published at ordinal 1; candidate factory only, not proof of T3a.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
-- Requires FCUT committed separately (T2a); this fragment never captures a cut.
INSERT INTO assessment_attempt
 (position_id,attempt_id,domain_id,cut_id,position_version,rule_id,rule_version,
 parameter_identity,execution_status,assessment_mode,decision_time_observed)
SELECT 'P-A','ATT-1','D-A',cut_id,1,'SYNTH-REFERENCE','1','PARAM-1',
 'COMPLETED','ONLINE','2026-01-01T10:05:00Z'
FROM publication_cut WHERE domain_id='D-A' AND ordinal=1 AND resolution_policy_version='CUT-1';
INSERT INTO publication_batch
 (position_id,batch_id,domain_id,origin_type,origin_id,fingerprint,publication_status)
VALUES ('P-A','BR1','D-A','ASSESSMENT_RESULT','RES-1',
 encode(sha256(convert_to('ATT-1|C1|v1|NOTIFY|SYNTH-NOTIFY-1','UTF8')),'hex'),
 'PERSISTED_PENDING_PUBLICATION');
INSERT INTO assessment_result VALUES
 ('P-A','RES-1','ATT-1','BR1',NULL,
 encode(sha256(convert_to('ATT-1|C1|v1|NOTIFY|SYNTH-NOTIFY-1','UTF8')),'hex'),
 'EVALUABLE','USER_REFERENCE','synthetic reference','synthetic only; no market claim');
INSERT INTO notification_decision VALUES ('P-A','RES-1','SYNTH-NOTIFY','1','NOTIFY','synthetic oracle');
INSERT INTO publication_member VALUES ('P-A','BR1',1,NULL,NULL,'RES-1');
INSERT INTO notification(position_id,notification_id,batch_id,origin_type,command_event_id,result_id,
 policy_id,policy_version,destination_id,dedup_key) VALUES
 ('P-A','N-R1','BR1','ASSESSMENT_RESULT',NULL,'RES-1',
 'SYNTH-NOTIFY','1','SYNTH-INBOX','N-R1-KEY');
INSERT INTO outbox_event
 (position_id,outbox_id,batch_id,result_id,notification_id)
VALUES ('P-A','OB-R1','BR1','RES-1','N-R1');
COMMIT;
-- END FIXTURE FRESULT@2

-- BEGIN FIXTURE FQUIET@2: alternative to FRESULT; requires committed FCUT.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
-- Requires FCUT committed separately (T2a); this fragment never captures a cut.
INSERT INTO assessment_attempt
 (position_id,attempt_id,domain_id,cut_id,position_version,rule_id,rule_version,
 parameter_identity,execution_status,assessment_mode,decision_time_observed)
SELECT 'P-A','ATT-1','D-A',cut_id,1,'SYNTH-REFERENCE','1','PARAM-1',
 'COMPLETED','ONLINE','2026-01-01T10:05:00Z'
FROM publication_cut WHERE domain_id='D-A' AND ordinal=1 AND resolution_policy_version='CUT-1';
INSERT INTO publication_batch
 (position_id,batch_id,domain_id,origin_type,origin_id,fingerprint,publication_status)
VALUES ('P-A','BR1','D-A','ASSESSMENT_RESULT','RES-1',
 encode(sha256(convert_to('ATT-1|C1|v1|DO_NOT_NOTIFY|SYNTH-QUIET-1','UTF8')),'hex'),
 'PERSISTED_PENDING_PUBLICATION');
INSERT INTO assessment_result VALUES
 ('P-A','RES-1','ATT-1','BR1',NULL,
 encode(sha256(convert_to('ATT-1|C1|v1|DO_NOT_NOTIFY|SYNTH-QUIET-1','UTF8')),'hex'),
 'EVALUABLE','USER_REFERENCE','synthetic quiet reference','synthetic only; no market claim');
INSERT INTO notification_decision VALUES
 ('P-A','RES-1','SYNTH-QUIET','1','DO_NOT_NOTIFY','no synthetic alert condition');
INSERT INTO publication_member VALUES ('P-A','BR1',1,NULL,NULL,'RES-1');
COMMIT;
-- END FIXTURE FQUIET@2

-- BEGIN FIXTURE FB23@1: requires F1, alternative to FCHAIN.
-- Synthetic compound command CMD-23 is test-only and still needs scope approval.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
INSERT INTO command_receipt
 (tenant_id,owner_id,command_id,position_id,actor_id,action,expected_position_version,
 canonical_payload,fingerprint,response_code,response_payload)
VALUES ('T-A','U-A','CMD-23','P-A','U-A','SYNTHETIC_COMPOUND',1,
 'SYNTHETIC_COMPOUND|P-A|v2:3:100.5|v3:2:100.5|1',
 encode(sha256(convert_to('SYNTHETIC_COMPOUND|P-A|v2:3:100.5|v3:2:100.5|1','UTF8')),'hex'),
 'ACCEPTED_PENDING_PUBLICATION','CMD-23|B23');
INSERT INTO publication_batch
 (position_id,batch_id,domain_id,origin_type,origin_id,fingerprint,publication_status)
SELECT 'P-A','B23','D-A','POSITION_COMMAND','CMD-23',fingerprint,
 'PERSISTED_PENDING_PUBLICATION' FROM command_receipt WHERE command_id='CMD-23';
INSERT INTO position_event VALUES
 ('P-A','EV-2','CMD-23','INCREASE',NULL,'2026-01-01T10:01:00Z',NULL),
 ('P-A','EV-3','CMD-23','REDUCE',NULL,'2026-01-01T10:02:00Z',NULL);
INSERT INTO position_revision VALUES
 ('P-A',2,1,'EV-2','B23','OPEN_DECLARED','LONG',3,100.5,'2026-01-01T10:01:00Z'),
 ('P-A',3,2,'EV-3','B23','OPEN_DECLARED','LONG',2,100.5,'2026-01-01T10:02:00Z');
INSERT INTO publication_member VALUES
 ('P-A','B23',1,2,NULL,NULL),('P-A','B23',2,3,NULL,NULL);
UPDATE position SET persisted_version=3 WHERE position_id='P-A';
COMMIT;
-- END FIXTURE FB23@1
-- Candidate 0.4: F0/FBLOCK/FNOTICE/FRESULT/FQUIET use @2; FCUT uses @1.
-- Other fragments retain their payload version. Do not combine mutually exclusive
-- branches. FRESULT/FQUIET require no published plan, otherwise capture that plan too.
-- H10 candidate fragments, requires B1 PUBLISHED ordinal 1; independent transactions.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
INSERT INTO publication_cut
 (cut_id,domain_id,ordinal,resolution_policy_version,frontier_position_id,frontier_batch_id)
VALUES ('C-POLICY-2','D-A',1,'CUT-2','P-A','B1')
ON CONFLICT (domain_id,ordinal,resolution_policy_version) DO NOTHING;
COMMIT;
-- Negative H10, EXPECT 23503; orchestrator must ROLLBACK on error, not run onward.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
INSERT INTO publication_cut
 (cut_id,domain_id,ordinal,resolution_policy_version,frontier_position_id,frontier_batch_id)
VALUES ('C-UNSUPPORTED','D-A',1,'CUT-99','P-A','B1');
ROLLBACK;
-- Negative H11, requires committed B1 and FCHAIN v2 pending; EXPECT P0001.
BEGIN;
SET LOCAL search_path=mpt_poc,pg_catalog;
UPDATE public_projection SET position_version=2 WHERE position_id='P-A';
SET CONSTRAINTS ALL IMMEDIATE;
ROLLBACK;
-- All fragments NOT_RUN. No new market data, randomness, runner or service.
-- BEGIN FIXTURE FCUT@1: requires B1 published; separate committed T2a.
BEGIN;
SELECT mpt_poc.capture_cut('P-A','CUT-1','C1');
COMMIT;
-- END FIXTURE FCUT@1
