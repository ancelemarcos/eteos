-- CANDIDATE / NOT_RUN. psql script. Requires approved disposable DB already created.
-- Candidate 0.4: independently verify environment/provenance before any future DDL.
-- Session flags are safeguards, not approval evidence. Runner never invokes this file.
\set ON_ERROR_STOP on
DO $$ BEGIN
 IF current_database()<>'mpt_poc_lab' THEN RAISE EXCEPTION 'disposable database required'; END IF;
 IF current_setting('mpt.execution_authorized',true) IS DISTINCT FROM 'yes' THEN
   RAISE EXCEPTION 'separate execution authorization required'; END IF;
END $$;
\ir ../schema.sql
\ir delivery-api.sql
-- Role memberships for actual logins MUST be provisioned separately by reviewed security plan.
-- No CREATE DATABASE, credentials, Docker, networking or automatic grants to current login.
