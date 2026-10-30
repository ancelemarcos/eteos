-- CANDIDATE / NOT_RUN. Never invoked automatically by run.py.
-- Candidate 0.4: separate approved teardown only; preserve evidence outside the schema.
\set ON_ERROR_STOP on
DO $$ BEGIN
 IF current_database()<>'mpt_poc_lab'
   OR current_setting('mpt.cleanup_authorized',true) IS DISTINCT FROM 'yes' THEN
   RAISE EXCEPTION 'explicit disposable cleanup authorization required';
 END IF;
END $$;
DROP SCHEMA mpt_poc CASCADE;
-- Cluster roles deliberately retained. Re-preparing requires reviewed role/schema bootstrap,
-- or a fresh isolated cluster. Do not drop roles shared with any other database.
