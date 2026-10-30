-- PROPOSED / NOT EXECUTED. Review artifact, not a migration entry point.
-- Synthetic MPT publication only. No MIR, market-data schema, production roles or services.
-- Text IDs below are exact synthetic labels, not a proposed production ID grammar.
-- All writers must follow LOCK-ORDER.md. Constraints alone do not implement TP.
BEGIN;
-- Candidate bootstrap requires a separately approved migration administrator.
-- Deliberately not idempotent: existing roles/schema require manual inspection.
CREATE ROLE mpt_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
CREATE ROLE mpt_reader NOLOGIN;
CREATE ROLE mpt_writer NOLOGIN;
CREATE ROLE mpt_evaluator NOLOGIN;
CREATE ROLE mpt_publisher NOLOGIN;
CREATE ROLE mpt_dispatcher NOLOGIN;
CREATE ROLE mpt_recovery NOLOGIN;
CREATE SCHEMA mpt_poc AUTHORIZATION mpt_owner;
SET LOCAL ROLE mpt_owner;
SET LOCAL search_path = mpt_poc, pg_catalog;

CREATE TABLE publication_domain (
  domain_id text PRIMARY KEY,
  policy_version text NOT NULL
);
CREATE TABLE publication_barrier (
  domain_id text PRIMARY KEY REFERENCES publication_domain,
  committed_ordinal bigint NOT NULL DEFAULT 0 CHECK (committed_ordinal >= 0)
);
CREATE TABLE recipient_guard (
  tenant_id text NOT NULL, owner_id text NOT NULL,
  access_version bigint NOT NULL CHECK (access_version > 0),
  access_allowed boolean NOT NULL,
  PRIMARY KEY (tenant_id, owner_id)
);
CREATE TABLE position (
  position_id text PRIMARY KEY,
  domain_id text NOT NULL REFERENCES publication_domain,
  tenant_id text NOT NULL, owner_id text NOT NULL,
  instrument_label text NOT NULL CHECK (instrument_label LIKE 'SYNTH-%'),
  persisted_version bigint NOT NULL DEFAULT 0 CHECK (persisted_version >= 0),
  UNIQUE (position_id, domain_id),
  UNIQUE (position_id, tenant_id, owner_id),
  FOREIGN KEY (tenant_id, owner_id) REFERENCES recipient_guard
);
CREATE TABLE position_guard (
  position_id text PRIMARY KEY REFERENCES position,
  pending_close_command text
);
CREATE TABLE command_receipt (
  tenant_id text NOT NULL, owner_id text NOT NULL, command_id text NOT NULL,
  position_id text NOT NULL, actor_id text NOT NULL, action text NOT NULL,
  expected_position_version bigint CHECK (expected_position_version >= 0),
  expected_plan_version bigint CHECK (expected_plan_version >= 0),
  canonical_payload text NOT NULL,
  fingerprint text NOT NULL CHECK (fingerprint ~ '^[0-9a-f]{64}$'),
  response_code text NOT NULL CHECK (response_code = 'ACCEPTED_PENDING_PUBLICATION'),
  response_payload text NOT NULL,
  PRIMARY KEY (tenant_id, owner_id, command_id),
  UNIQUE (position_id, command_id),
  FOREIGN KEY (position_id, tenant_id, owner_id)
    REFERENCES position (position_id, tenant_id, owner_id)
);
ALTER TABLE position_guard ADD FOREIGN KEY (position_id, pending_close_command)
  REFERENCES command_receipt (position_id, command_id)
  DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE publication_batch (
  position_id text NOT NULL, batch_id text NOT NULL,
  domain_id text NOT NULL,
  origin_type text NOT NULL CHECK (origin_type IN ('POSITION_COMMAND','ASSESSMENT_RESULT')),
  origin_id text NOT NULL,
  fingerprint text NOT NULL CHECK (fingerprint ~ '^[0-9a-f]{64}$'),
  publication_status text NOT NULL CHECK (publication_status IN
    ('PERSISTED_PENDING_PUBLICATION','PUBLICATION_BLOCKED','PUBLISHED')),
  ordinal bigint CHECK (ordinal > 0), failure_reason text,
  content_frozen boolean NOT NULL DEFAULT false,
  state_version bigint NOT NULL DEFAULT 0 CHECK (state_version >= 0),
  PRIMARY KEY (position_id, batch_id),
  UNIQUE (domain_id, ordinal),
  UNIQUE (position_id, origin_type, origin_id),
  UNIQUE (position_id, batch_id, domain_id),
  UNIQUE (domain_id, ordinal, position_id, batch_id),
  FOREIGN KEY (position_id, domain_id) REFERENCES position (position_id, domain_id),
  CHECK ((publication_status = 'PUBLISHED') = (ordinal IS NOT NULL)),
  CHECK (publication_status <> 'PUBLICATION_BLOCKED' OR failure_reason IS NOT NULL)
);
-- No ordinal zero cut: empty-domain capture returns NO_PUBLISHED_FRONTIER.
CREATE TABLE publication_cut (
  cut_id text PRIMARY KEY,
  domain_id text NOT NULL, ordinal bigint NOT NULL CHECK (ordinal > 0),
  resolution_policy_version text NOT NULL,
  frontier_position_id text NOT NULL, frontier_batch_id text NOT NULL,
  capture_transaction xid8 NOT NULL DEFAULT pg_current_xact_id(),
  UNIQUE (domain_id, ordinal, resolution_policy_version),
  UNIQUE (cut_id, domain_id),
  FOREIGN KEY (domain_id, ordinal, frontier_position_id, frontier_batch_id)
    REFERENCES publication_batch (domain_id, ordinal, position_id, batch_id)
);
CREATE TABLE position_event (
  position_id text NOT NULL, event_id text NOT NULL, command_id text NOT NULL,
  event_type text NOT NULL, correction_of text,
  recorded_at_observed timestamptz NOT NULL,
  user_reported_execution_at timestamptz,
  PRIMARY KEY (position_id, event_id),
  FOREIGN KEY (position_id, command_id) REFERENCES command_receipt (position_id, command_id),
  FOREIGN KEY (position_id, correction_of) REFERENCES position_event (position_id, event_id),
  CHECK (correction_of IS NULL OR correction_of <> event_id)
);
CREATE TABLE position_revision (
  position_id text NOT NULL, version bigint NOT NULL CHECK (version > 0),
  predecessor_version bigint, event_id text NOT NULL, batch_id text NOT NULL,
  lifecycle text NOT NULL CHECK (lifecycle IN ('OPEN_DECLARED','CLOSED_DECLARED','CANCELLED')),
  side text NOT NULL CHECK (side IN ('LONG','SHORT')),
  remaining_quantity bigint NOT NULL CHECK (remaining_quantity >= 0),
  average_entry_price numeric NOT NULL,
  last_confirmed_at_observed timestamptz NOT NULL,
  PRIMARY KEY (position_id, version),
  UNIQUE (position_id, version, batch_id),
  FOREIGN KEY (position_id, predecessor_version) REFERENCES position_revision (position_id, version),
  FOREIGN KEY (position_id, event_id) REFERENCES position_event (position_id, event_id),
  FOREIGN KEY (position_id, batch_id) REFERENCES publication_batch,
  CHECK ((version = 1 AND predecessor_version IS NULL) OR
         (version > 1 AND predecessor_version IS NOT NULL AND predecessor_version = version - 1)),
  CHECK ((lifecycle = 'OPEN_DECLARED' AND remaining_quantity > 0) OR
         (lifecycle IN ('CLOSED_DECLARED','CANCELLED') AND remaining_quantity = 0)),
  CHECK (average_entry_price::text NOT IN ('NaN','Infinity','-Infinity'))
);
CREATE TABLE plan (
  position_id text PRIMARY KEY REFERENCES position,
  persisted_version bigint NOT NULL DEFAULT 0 CHECK (persisted_version >= 0)
);
CREATE TABLE plan_revision (
  position_id text NOT NULL, version bigint NOT NULL CHECK (version > 0),
  predecessor_version bigint, batch_id text NOT NULL, command_id text NOT NULL,
  stop_price numeric, target_price numeric, note text,
  PRIMARY KEY (position_id, version),
  UNIQUE (position_id, version, batch_id),
  FOREIGN KEY (position_id) REFERENCES plan,
  FOREIGN KEY (position_id, predecessor_version) REFERENCES plan_revision (position_id, version),
  FOREIGN KEY (position_id, command_id) REFERENCES command_receipt (position_id, command_id),
  FOREIGN KEY (position_id, batch_id) REFERENCES publication_batch,
  CHECK ((version = 1 AND predecessor_version IS NULL) OR
         (version > 1 AND predecessor_version IS NOT NULL AND predecessor_version = version - 1)),
  CHECK (stop_price IS NULL OR stop_price::text NOT IN ('NaN','Infinity','-Infinity')),
  CHECK (target_price IS NULL OR target_price::text NOT IN ('NaN','Infinity','-Infinity'))
);
CREATE TABLE personal_journal_entry (
  position_id text NOT NULL, entry_id text NOT NULL, event_id text NOT NULL,
  note text NOT NULL, recorded_at_observed timestamptz NOT NULL,
  PRIMARY KEY (position_id, entry_id),
  FOREIGN KEY (position_id, event_id) REFERENCES position_event
);
CREATE TABLE public_projection (
  position_id text PRIMARY KEY REFERENCES position,
  position_version bigint, plan_version bigint,
  FOREIGN KEY (position_id, position_version) REFERENCES position_revision,
  FOREIGN KEY (position_id, plan_version) REFERENCES plan_revision
);
CREATE TABLE assessment_attempt (
  position_id text NOT NULL, attempt_id text NOT NULL,
  domain_id text NOT NULL, cut_id text NOT NULL,
  position_version bigint NOT NULL, plan_version bigint,
  rule_id text NOT NULL, rule_version text NOT NULL,
  parameter_identity text NOT NULL,
  execution_status text NOT NULL CHECK (execution_status IN ('RUNNING','COMPLETED','FAILED','SKIPPED')),
  assessment_mode text NOT NULL CHECK (assessment_mode IN ('ONLINE','RETROSPECTIVE')),
  decision_time_observed timestamptz NOT NULL,
  reconstructed_at_observed timestamptz,
  failure_code text,
  PRIMARY KEY (position_id, attempt_id),
  FOREIGN KEY (position_id, domain_id) REFERENCES position (position_id, domain_id),
  FOREIGN KEY (cut_id, domain_id) REFERENCES publication_cut (cut_id, domain_id),
  FOREIGN KEY (position_id, position_version) REFERENCES position_revision,
  FOREIGN KEY (position_id, plan_version) REFERENCES plan_revision,
  CHECK (assessment_mode <> 'RETROSPECTIVE' OR reconstructed_at_observed IS NOT NULL)
);
CREATE TABLE assessment_result (
  position_id text NOT NULL, result_id text NOT NULL, attempt_id text NOT NULL,
  batch_id text NOT NULL, supersedes_result_id text,
  fingerprint text NOT NULL CHECK (fingerprint ~ '^[0-9a-f]{64}$'),
  evaluability text NOT NULL CHECK (evaluability IN ('EVALUABLE','NOT_EVALUABLE')),
  content_nature text CHECK (content_nature IN ('FACTUAL','USER_REFERENCE')),
  content_text text, limitation text NOT NULL,
  PRIMARY KEY (position_id, result_id),
  UNIQUE (position_id, attempt_id),
  UNIQUE (position_id, result_id, batch_id),
  FOREIGN KEY (position_id, attempt_id) REFERENCES assessment_attempt,
  FOREIGN KEY (position_id, batch_id) REFERENCES publication_batch,
  FOREIGN KEY (position_id, supersedes_result_id) REFERENCES assessment_result,
  CHECK (supersedes_result_id IS NULL OR supersedes_result_id <> result_id),
  CHECK ((evaluability = 'EVALUABLE' AND content_nature IS NOT NULL AND content_text IS NOT NULL)
      OR (evaluability = 'NOT_EVALUABLE' AND content_nature IS NULL AND content_text IS NULL))
);
CREATE TABLE notification_decision (
  position_id text NOT NULL, result_id text NOT NULL,
  policy_id text NOT NULL, policy_version text NOT NULL,
  decision text NOT NULL CHECK (decision IN ('NOTIFY','DO_NOT_NOTIFY')),
  reason text NOT NULL,
  PRIMARY KEY (position_id, result_id),
  FOREIGN KEY (position_id, result_id) REFERENCES assessment_result
);
-- Typed members avoid a free-form entity_id that bypasses referential integrity.
CREATE TABLE publication_member (
  position_id text NOT NULL, batch_id text NOT NULL, member_order integer NOT NULL CHECK (member_order > 0),
  position_version bigint, plan_version bigint, result_id text,
  PRIMARY KEY (position_id, batch_id, member_order),
  FOREIGN KEY (position_id, batch_id) REFERENCES publication_batch,
  FOREIGN KEY (position_id, position_version, batch_id)
    REFERENCES position_revision (position_id, version, batch_id),
  FOREIGN KEY (position_id, plan_version, batch_id)
    REFERENCES plan_revision (position_id, version, batch_id),
  FOREIGN KEY (position_id, result_id, batch_id)
    REFERENCES assessment_result (position_id, result_id, batch_id),
  CHECK (num_nonnulls(position_version, plan_version, result_id) = 1),
  UNIQUE (position_id, position_version),
  UNIQUE (position_id, plan_version),
  UNIQUE (position_id, result_id)
);
CREATE TABLE notification (
  position_id text NOT NULL, notification_id text NOT NULL, batch_id text NOT NULL,
  origin_type text NOT NULL CHECK (origin_type IN ('POSITION_COMMAND','ASSESSMENT_RESULT')),
  command_event_id text, result_id text,
  policy_id text NOT NULL, policy_version text NOT NULL,
  destination_id text NOT NULL CHECK (destination_id LIKE 'SYNTH-%'),
  dedup_key text NOT NULL,
  delivery_status text NOT NULL DEFAULT 'READY' CHECK (delivery_status IN
    ('READY','HOLD_PENDING_CLOSE','SEND_AUTHORIZED','SUPPRESSED_AFTER_AUTHORIZATION',
     'SUPPRESSED','DELIVERED','ACKED','EXPIRED')),
  PRIMARY KEY (position_id, notification_id),
  UNIQUE (position_id, result_id),
  UNIQUE (destination_id, dedup_key),
  FOREIGN KEY (position_id, batch_id) REFERENCES publication_batch,
  FOREIGN KEY (position_id, command_event_id) REFERENCES position_event,
  FOREIGN KEY (position_id, result_id) REFERENCES assessment_result,
  CHECK ((origin_type = 'POSITION_COMMAND' AND command_event_id IS NOT NULL AND result_id IS NULL)
      OR (origin_type = 'ASSESSMENT_RESULT' AND command_event_id IS NULL AND result_id IS NOT NULL))
);
CREATE TABLE outbox_event (
  position_id text NOT NULL, outbox_id text NOT NULL, batch_id text NOT NULL,
  command_event_id text, result_id text, notification_id text,
  dispatch_status text NOT NULL DEFAULT 'PENDING' CHECK (dispatch_status IN ('PENDING','CLAIMED','ACKED','SUPPRESSED')),
  lease_token text, lease_until_observed timestamptz,
  PRIMARY KEY (position_id, outbox_id),
  UNIQUE (position_id, notification_id),
  FOREIGN KEY (position_id, batch_id) REFERENCES publication_batch,
  FOREIGN KEY (position_id, command_event_id) REFERENCES position_event,
  FOREIGN KEY (position_id, result_id) REFERENCES assessment_result,
  FOREIGN KEY (position_id, notification_id) REFERENCES notification,
  CHECK (num_nonnulls(command_event_id, result_id) = 1),
  CHECK (dispatch_status <> 'CLAIMED' OR (lease_token IS NOT NULL AND lease_until_observed IS NOT NULL))
);
CREATE TABLE send_authorization (
  position_id text NOT NULL, authorization_id text NOT NULL, notification_id text NOT NULL,
  tenant_id text NOT NULL, owner_id text NOT NULL, access_version bigint NOT NULL,
  policy_version text NOT NULL, final_check_position_version bigint NOT NULL,
  PRIMARY KEY (position_id, authorization_id),
  UNIQUE (position_id, notification_id),
  FOREIGN KEY (position_id, notification_id) REFERENCES notification,
  FOREIGN KEY (position_id, tenant_id, owner_id) REFERENCES position (position_id, tenant_id, owner_id),
  FOREIGN KEY (position_id, final_check_position_version) REFERENCES position_revision
);
CREATE TABLE access_audit (
  tenant_id text NOT NULL, owner_id text NOT NULL, access_version bigint NOT NULL,
  allowed boolean NOT NULL, reason text NOT NULL,
  PRIMARY KEY (tenant_id, owner_id, access_version),
  FOREIGN KEY (tenant_id, owner_id) REFERENCES recipient_guard
);
ALTER TABLE send_authorization ADD FOREIGN KEY (tenant_id, owner_id, access_version)
  REFERENCES access_audit;
CREATE TABLE delivery_audit (
  position_id text NOT NULL, audit_id text NOT NULL, notification_id text NOT NULL,
  authorization_id text, reason text NOT NULL, checkpoint text NOT NULL,
  PRIMARY KEY (position_id, audit_id),
  FOREIGN KEY (position_id, notification_id) REFERENCES notification,
  FOREIGN KEY (position_id, authorization_id) REFERENCES send_authorization
);
-- Candidate model for the independent synthetic destination only.
-- Do NOT use this in the sender's transaction: ACK-loss scenarios require independent commit.
CREATE TABLE synthetic_destination_receipt (
  destination_id text NOT NULL, dedup_key text NOT NULL,
  authorization_id text NOT NULL, payload_fingerprint text NOT NULL,
  PRIMARY KEY (destination_id, dedup_key)
);
CREATE TABLE synthetic_destination_call (
  call_id text PRIMARY KEY, destination_id text NOT NULL, dedup_key text NOT NULL,
  authorization_id text NOT NULL, checkpoint text NOT NULL
);
CREATE INDEX revision_batch_idx ON position_revision(position_id, batch_id, version);
CREATE INDEX plan_batch_idx ON plan_revision(position_id, batch_id, version);
CREATE INDEX pending_batch_idx ON publication_batch(domain_id, publication_status, batch_id);
CREATE INDEX outbox_dispatch_idx ON outbox_event(dispatch_status, position_id, batch_id);
CREATE INDEX attempt_cut_idx ON assessment_attempt(domain_id, cut_id);

-- Immutable facts: ordinal and public status live on the batch, not on revision payload.
CREATE FUNCTION deny_fact_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'immutable synthetic MPT fact: %', TG_TABLE_NAME;
END;
$$;
CREATE TRIGGER position_revision_immutable BEFORE UPDATE OR DELETE ON position_revision
  FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TRIGGER plan_revision_immutable BEFORE UPDATE OR DELETE ON plan_revision
  FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TRIGGER event_immutable BEFORE UPDATE OR DELETE ON position_event
  FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TRIGGER cut_immutable BEFORE UPDATE OR DELETE ON publication_cut
  FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TRIGGER result_immutable BEFORE UPDATE OR DELETE ON assessment_result
  FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TRIGGER decision_immutable BEFORE UPDATE OR DELETE ON notification_decision
  FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TRIGGER receipt_immutable BEFORE UPDATE OR DELETE ON command_receipt
  FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();

-- Candidate deferred cross-table assertion; catches T3a partial terminal states.
CREATE FUNCTION assert_attempt_result() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE p text; a text; s text; n bigint; d bigint;
BEGIN
  p := NEW.position_id;
  IF TG_TABLE_NAME = 'assessment_attempt' THEN a := NEW.attempt_id;
  ELSIF TG_TABLE_NAME = 'assessment_result' THEN a := NEW.attempt_id;
  ELSE
    SELECT attempt_id INTO a FROM mpt_poc.assessment_result
      WHERE position_id = p AND result_id = NEW.result_id;
  END IF;
  SELECT execution_status INTO s FROM mpt_poc.assessment_attempt
    WHERE position_id = p AND attempt_id = a;
  SELECT count(*) INTO n FROM mpt_poc.assessment_result
    WHERE position_id = p AND attempt_id = a;
  SELECT count(*) INTO d FROM mpt_poc.notification_decision nd
    JOIN mpt_poc.assessment_result r USING (position_id, result_id)
    WHERE r.position_id = p AND r.attempt_id = a;
  IF (s = 'COMPLETED' AND (n <> 1 OR d <> 1)) OR
     (s <> 'COMPLETED' AND n <> 0) THEN
    RAISE EXCEPTION 'attempt/result/decision mismatch';
  END IF;
  RETURN NULL;
END;
$$;
CREATE CONSTRAINT TRIGGER attempt_result_consistency
  AFTER INSERT OR UPDATE ON assessment_attempt DEFERRABLE INITIALLY DEFERRED
  FOR EACH ROW EXECUTE FUNCTION assert_attempt_result();
CREATE CONSTRAINT TRIGGER result_attempt_consistency
  AFTER INSERT ON assessment_result DEFERRABLE INITIALLY DEFERRED
  FOR EACH ROW EXECUTE FUNCTION assert_attempt_result();
CREATE CONSTRAINT TRIGGER decision_attempt_consistency
  AFTER INSERT ON notification_decision DEFERRABLE INITIALLY DEFERRED
  FOR EACH ROW EXECUTE FUNCTION assert_attempt_result();

-- Hardening candidate v0.2. Physical constraints below are NOT execution evidence.
CREATE TABLE domain_resolution_policy (
  domain_id text NOT NULL REFERENCES publication_domain,
  policy_version text NOT NULL,
  PRIMARY KEY (domain_id, policy_version)
);
ALTER TABLE publication_cut ADD FOREIGN KEY (domain_id, resolution_policy_version)
  REFERENCES domain_resolution_policy;
ALTER TABLE notification ADD FOREIGN KEY (position_id, result_id, batch_id)
  REFERENCES assessment_result (position_id, result_id, batch_id);
ALTER TABLE send_authorization ADD UNIQUE (position_id, authorization_id, notification_id);
ALTER TABLE delivery_audit ADD FOREIGN KEY (position_id, authorization_id, notification_id)
  REFERENCES send_authorization (position_id, authorization_id, notification_id);

CREATE FUNCTION guard_batch() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF TG_OP = 'DELETE' THEN RAISE EXCEPTION 'batch deletion forbidden'; END IF;
  IF TG_OP = 'INSERT' THEN
    IF NEW.publication_status <> 'PERSISTED_PENDING_PUBLICATION'
       OR NEW.content_frozen OR NEW.state_version<>0 THEN
      RAISE EXCEPTION 'batch must start pending';
    END IF;
  ELSE
    IF OLD.publication_status = 'PUBLISHED' OR
       (to_jsonb(NEW) - ARRAY['publication_status','ordinal','failure_reason','content_frozen','state_version']) IS DISTINCT FROM
       (to_jsonb(OLD) - ARRAY['publication_status','ordinal','failure_reason','content_frozen','state_version']) THEN
      RAISE EXCEPTION 'sealed batch or changed batch identity';
    END IF;
    IF OLD.publication_status = 'PUBLICATION_BLOCKED' AND NEW.publication_status = 'PUBLISHED' THEN
      RAISE EXCEPTION 'blocked batch requires explicit recovery to pending';
    END IF;
    IF OLD.content_frozen AND NOT NEW.content_frozen THEN
      RAISE EXCEPTION 'content freeze is permanent';
    END IF;
    IF NEW.state_version <> OLD.state_version + 1 THEN
      RAISE EXCEPTION 'batch state version must increment';
    END IF;
    IF OLD.publication_status='PUBLICATION_BLOCKED'
       AND NEW.publication_status='PERSISTED_PENDING_PUBLICATION'
       AND NOT EXISTS (SELECT 1 FROM mpt_poc.batch_recovery_audit a
         WHERE a.position_id=OLD.position_id AND a.batch_id=OLD.batch_id
           AND a.expected_version=OLD.state_version) THEN
      RAISE EXCEPTION 'recovery audit required';
    END IF;
  END IF;
  IF NEW.publication_status IN ('PUBLICATION_BLOCKED','PUBLISHED') THEN
    NEW.content_frozen := true;
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER batch_guard BEFORE INSERT OR UPDATE OR DELETE ON publication_batch
  FOR EACH ROW EXECUTE FUNCTION guard_batch();

-- The parent row lock makes late insertion compete with TP sealing.
-- Trusted writers must acquire the global guards BEFORE triggering this lock.
CREATE FUNCTION guard_batch_child() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE s text;
BEGIN
  SELECT publication_status INTO s FROM mpt_poc.publication_batch
    WHERE position_id = NEW.position_id AND batch_id = NEW.batch_id FOR UPDATE;
  IF s IS DISTINCT FROM 'PERSISTED_PENDING_PUBLICATION' OR EXISTS (
    SELECT 1 FROM mpt_poc.publication_batch
      WHERE position_id=NEW.position_id AND batch_id=NEW.batch_id AND content_frozen
  ) THEN RAISE EXCEPTION 'parent is not editable'; END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER revision_parent BEFORE INSERT ON position_revision FOR EACH ROW EXECUTE FUNCTION guard_batch_child();
CREATE TRIGGER plan_parent BEFORE INSERT ON plan_revision FOR EACH ROW EXECUTE FUNCTION guard_batch_child();
CREATE TRIGGER result_parent BEFORE INSERT ON assessment_result FOR EACH ROW EXECUTE FUNCTION guard_batch_child();
CREATE TRIGGER member_parent BEFORE INSERT ON publication_member FOR EACH ROW EXECUTE FUNCTION guard_batch_child();
CREATE TRIGGER notification_parent BEFORE INSERT ON notification FOR EACH ROW EXECUTE FUNCTION guard_batch_child();
CREATE TRIGGER outbox_parent BEFORE INSERT ON outbox_event FOR EACH ROW EXECUTE FUNCTION guard_batch_child();
CREATE TRIGGER member_immutable BEFORE UPDATE OR DELETE ON publication_member FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TRIGGER authorization_immutable BEFORE UPDATE OR DELETE ON send_authorization FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TRIGGER access_audit_immutable BEFORE UPDATE OR DELETE ON access_audit FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TRIGGER delivery_audit_immutable BEFORE UPDATE OR DELETE ON delivery_audit FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TRIGGER destination_receipt_immutable BEFORE UPDATE OR DELETE ON synthetic_destination_receipt FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TRIGGER policy_immutable BEFORE UPDATE OR DELETE ON domain_resolution_policy FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();

CREATE FUNCTION guard_delivery_identity() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE ignored text[];
BEGIN
  IF TG_OP = 'DELETE' THEN RAISE EXCEPTION 'delivery fact deletion forbidden'; END IF;
  ignored := CASE WHEN TG_TABLE_NAME = 'notification' THEN ARRAY['delivery_status']
    ELSE ARRAY['dispatch_status','lease_token','lease_until_observed'] END;
  IF (to_jsonb(NEW) - ignored) IS DISTINCT FROM (to_jsonb(OLD) - ignored) THEN
    RAISE EXCEPTION 'delivery origin/payload is immutable';
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER notification_identity BEFORE UPDATE OR DELETE ON notification FOR EACH ROW EXECUTE FUNCTION guard_delivery_identity();
CREATE TRIGGER outbox_identity BEFORE UPDATE OR DELETE ON outbox_event FOR EACH ROW EXECUTE FUNCTION guard_delivery_identity();

CREATE FUNCTION guard_attempt() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE c bigint; pv bigint; lv bigint;
BEGIN
  IF TG_OP = 'DELETE' THEN RAISE EXCEPTION 'attempt deletion forbidden'; END IF;
  IF TG_OP = 'UPDATE' THEN
    IF OLD.execution_status <> 'RUNNING' OR
       (to_jsonb(NEW) - ARRAY['execution_status','failure_code']) IS DISTINCT FROM
       (to_jsonb(OLD) - ARRAY['execution_status','failure_code']) THEN
      RAISE EXCEPTION 'terminal attempt or changed captured inputs';
    END IF;
    RETURN NEW;
  END IF;
  SELECT ordinal INTO c FROM mpt_poc.publication_cut WHERE cut_id = NEW.cut_id AND domain_id = NEW.domain_id;
  IF EXISTS(SELECT 1 FROM mpt_poc.publication_cut WHERE cut_id=NEW.cut_id
    AND capture_transaction=pg_current_xact_id()) THEN
    RAISE EXCEPTION 'T2_SPLIT_REQUIRED: commit capture before attempt';
  END IF;
  SELECT max(r.version) INTO pv FROM mpt_poc.position_revision r
    JOIN mpt_poc.publication_batch b USING (position_id,batch_id)
    WHERE r.position_id = NEW.position_id AND b.domain_id = NEW.domain_id
      AND b.publication_status = 'PUBLISHED' AND b.ordinal <= c;
  SELECT max(r.version) INTO lv FROM mpt_poc.plan_revision r
    JOIN mpt_poc.publication_batch b USING (position_id,batch_id)
    WHERE r.position_id = NEW.position_id AND b.domain_id = NEW.domain_id
      AND b.publication_status = 'PUBLISHED' AND b.ordinal <= c;
  IF c IS NULL OR pv IS NULL OR NEW.position_version IS DISTINCT FROM pv
      OR NEW.plan_version IS DISTINCT FROM lv THEN
    RAISE EXCEPTION 'inputs are not latest eligible immutable revisions at cut';
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER attempt_guard BEFORE INSERT OR UPDATE OR DELETE ON assessment_attempt FOR EACH ROW EXECUTE FUNCTION guard_attempt();

-- Reject forward references, including same-statement cyclic graphs.
-- Existing targets are immutable, so induction prevents longer cycles.
CREATE FUNCTION guard_predecessor_fact() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE old_a mpt_poc.assessment_attempt%ROWTYPE; new_a mpt_poc.assessment_attempt%ROWTYPE;
BEGIN
  IF TG_TABLE_NAME = 'position_event' THEN
    IF NEW.correction_of IS NOT NULL AND NOT EXISTS (
      SELECT 1 FROM mpt_poc.position_event WHERE position_id=NEW.position_id AND event_id=NEW.correction_of
    ) THEN RAISE EXCEPTION 'correction requires existing immutable target'; END IF;
  ELSE
    IF NEW.supersedes_result_id IS NOT NULL THEN
      SELECT a.* INTO old_a FROM mpt_poc.assessment_result r JOIN mpt_poc.assessment_attempt a
        USING (position_id,attempt_id) WHERE r.position_id=NEW.position_id AND r.result_id=NEW.supersedes_result_id;
      SELECT * INTO new_a FROM mpt_poc.assessment_attempt WHERE position_id=NEW.position_id AND attempt_id=NEW.attempt_id;
      IF old_a.attempt_id IS NULL OR
        ROW(old_a.rule_id,old_a.rule_version,old_a.parameter_identity,old_a.domain_id)
          IS DISTINCT FROM ROW(new_a.rule_id,new_a.rule_version,new_a.parameter_identity,new_a.domain_id)
      THEN RAISE EXCEPTION 'supersession target missing or outside rule scope'; END IF;
    END IF;
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER correction_guard BEFORE INSERT ON position_event FOR EACH ROW EXECUTE FUNCTION guard_predecessor_fact();
CREATE TRIGGER supersession_guard BEFORE INSERT ON assessment_result FOR EACH ROW EXECUTE FUNCTION guard_predecessor_fact();

-- Deferred assertion permits assembly in one transaction, never partial committed batches.
CREATE FUNCTION assert_batch_complete() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE p text; bid text; b mpt_poc.publication_batch%ROWTYPE; expected bigint; actual bigint;
BEGIN
  p := NEW.position_id; bid := NEW.batch_id;
  SELECT * INTO b FROM mpt_poc.publication_batch WHERE position_id=p AND batch_id=bid;
  SELECT (SELECT count(*) FROM mpt_poc.position_revision WHERE position_id=p AND batch_id=bid)
       + (SELECT count(*) FROM mpt_poc.plan_revision WHERE position_id=p AND batch_id=bid)
       + (SELECT count(*) FROM mpt_poc.assessment_result WHERE position_id=p AND batch_id=bid) INTO expected;
  SELECT count(*) INTO actual FROM mpt_poc.publication_member WHERE position_id=p AND batch_id=bid;
  IF actual=0 OR actual<>expected THEN RAISE EXCEPTION 'incomplete batch membership'; END IF;
  IF b.origin_type='POSITION_COMMAND' THEN
    IF NOT EXISTS (SELECT 1 FROM mpt_poc.command_receipt WHERE position_id=p AND command_id=b.origin_id)
      OR EXISTS (SELECT 1 FROM mpt_poc.assessment_result WHERE position_id=p AND batch_id=bid)
      OR EXISTS (SELECT 1 FROM mpt_poc.position_revision r JOIN mpt_poc.position_event e USING(position_id,event_id)
        WHERE r.position_id=p AND r.batch_id=bid AND e.command_id<>b.origin_id)
      OR EXISTS (SELECT 1 FROM mpt_poc.plan_revision WHERE position_id=p AND batch_id=bid AND command_id<>b.origin_id)
    THEN RAISE EXCEPTION 'command batch origin mismatch'; END IF;
  ELSE
    IF expected<>1 OR NOT EXISTS (SELECT 1 FROM mpt_poc.assessment_result
      WHERE position_id=p AND batch_id=bid AND result_id=b.origin_id)
    THEN RAISE EXCEPTION 'result batch origin mismatch'; END IF;
  END IF;
  IF EXISTS (
    SELECT 1 FROM mpt_poc.assessment_result r JOIN mpt_poc.notification_decision d USING(position_id,result_id)
    WHERE r.position_id=p AND r.batch_id=bid AND (
      (d.decision='NOTIFY' AND
        ((SELECT count(*) FROM mpt_poc.notification n WHERE n.position_id=p AND n.result_id=r.result_id
          AND n.policy_id=d.policy_id AND n.policy_version=d.policy_version)<>1 OR
         (SELECT count(*) FROM mpt_poc.outbox_event o WHERE o.position_id=p AND o.result_id=r.result_id)<>1))
      OR (d.decision='DO_NOT_NOTIFY' AND
        (EXISTS(SELECT 1 FROM mpt_poc.notification n WHERE n.position_id=p AND n.result_id=r.result_id)
         OR EXISTS(SELECT 1 FROM mpt_poc.outbox_event o WHERE o.position_id=p AND o.result_id=r.result_id)))
    )
  ) THEN RAISE EXCEPTION 'decision/intent cardinality mismatch'; END IF;
  IF EXISTS (SELECT 1 FROM mpt_poc.notification n LEFT JOIN mpt_poc.position_event e
      ON e.position_id=n.position_id AND e.event_id=n.command_event_id
    WHERE n.position_id=p AND n.batch_id=bid AND n.origin_type='POSITION_COMMAND'
      AND (b.origin_type<>'POSITION_COMMAND' OR e.command_id IS DISTINCT FROM b.origin_id))
    OR EXISTS (SELECT 1 FROM mpt_poc.outbox_event o LEFT JOIN mpt_poc.notification n USING(position_id,notification_id)
      WHERE o.position_id=p AND o.batch_id=bid AND
       (n.notification_id IS NULL OR n.batch_id<>bid OR n.command_event_id IS DISTINCT FROM o.command_event_id
        OR n.result_id IS DISTINCT FROM o.result_id))
  THEN RAISE EXCEPTION 'delivery origin/batch mismatch'; END IF;
  IF b.publication_status='PUBLISHED' AND EXISTS (
    SELECT 1 FROM (
      SELECT r.predecessor_version, r.batch_id, m.member_order, 'P' AS kind
        FROM mpt_poc.position_revision r JOIN mpt_poc.publication_member m
          ON m.position_id=r.position_id AND m.position_version=r.version
        WHERE r.position_id=p AND r.batch_id=bid
      UNION ALL
      SELECT r.predecessor_version,r.batch_id,m.member_order,'L'
        FROM mpt_poc.plan_revision r JOIN mpt_poc.publication_member m
          ON m.position_id=r.position_id AND m.plan_version=r.version
        WHERE r.position_id=p AND r.batch_id=bid
    ) x LEFT JOIN mpt_poc.publication_member pm ON pm.position_id=p AND
      ((x.kind='P' AND pm.position_version=x.predecessor_version) OR
       (x.kind='L' AND pm.plan_version=x.predecessor_version))
    LEFT JOIN mpt_poc.publication_batch pb ON pb.position_id=pm.position_id AND pb.batch_id=pm.batch_id
    WHERE x.predecessor_version IS NOT NULL AND
      (pm.batch_id IS NULL OR
       (pm.batch_id=bid AND pm.member_order>=x.member_order) OR
       (pm.batch_id<>bid AND (pb.publication_status<>'PUBLISHED' OR pb.ordinal>=b.ordinal)))
  ) THEN RAISE EXCEPTION 'unpublished or unordered predecessor'; END IF;
  RETURN NULL;
END;
$$;
CREATE CONSTRAINT TRIGGER batch_complete AFTER INSERT OR UPDATE ON publication_batch
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_batch_complete();
CREATE CONSTRAINT TRIGGER member_complete AFTER INSERT ON publication_member
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_batch_complete();
CREATE CONSTRAINT TRIGGER revision_complete AFTER INSERT ON position_revision
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_batch_complete();
CREATE CONSTRAINT TRIGGER plan_complete AFTER INSERT ON plan_revision
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_batch_complete();
CREATE CONSTRAINT TRIGGER result_complete AFTER INSERT ON assessment_result
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_batch_complete();
CREATE CONSTRAINT TRIGGER notification_complete AFTER INSERT ON notification
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_batch_complete();
CREATE CONSTRAINT TRIGGER outbox_complete AFTER INSERT ON outbox_event
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_batch_complete();

CREATE FUNCTION assert_domain_frontier() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE d text; n bigint; hi bigint; frontier bigint;
BEGIN
  d:=NEW.domain_id;
  SELECT committed_ordinal INTO frontier FROM mpt_poc.publication_barrier WHERE domain_id=d;
  SELECT count(*),coalesce(max(ordinal),0) INTO n,hi FROM mpt_poc.publication_batch
    WHERE domain_id=d AND publication_status='PUBLISHED';
  IF frontier IS NULL OR frontier<>hi OR n<>hi THEN RAISE EXCEPTION 'noncontiguous domain frontier'; END IF;
  RETURN NULL;
END;
$$;
CREATE CONSTRAINT TRIGGER barrier_frontier AFTER INSERT OR UPDATE ON publication_barrier
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_domain_frontier();
CREATE CONSTRAINT TRIGGER batch_frontier AFTER INSERT OR UPDATE ON publication_batch
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_domain_frontier();

-- Remaining OPEN-01 boundary: trusted writers serialize projection/barrier changes
-- and enforce delivery state transitions, authorization eligibility and access state.
-- Candidate role/API definitions follow; no production permission proof is claimed.
CREATE FUNCTION guard_aggregate_identity() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF TG_OP='DELETE' THEN RAISE EXCEPTION 'aggregate deletion forbidden'; END IF;
  IF (to_jsonb(NEW)-'persisted_version') IS DISTINCT FROM (to_jsonb(OLD)-'persisted_version')
    OR NEW.persisted_version<OLD.persisted_version THEN RAISE EXCEPTION 'aggregate identity/version rewrite'; END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER position_identity BEFORE UPDATE OR DELETE ON position FOR EACH ROW EXECUTE FUNCTION guard_aggregate_identity();
CREATE TRIGGER plan_identity BEFORE UPDATE OR DELETE ON plan FOR EACH ROW EXECUTE FUNCTION guard_aggregate_identity();
CREATE FUNCTION guard_barrier() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF TG_OP='DELETE' THEN RAISE EXCEPTION 'barrier deletion forbidden'; END IF;
  IF NEW.domain_id<>OLD.domain_id OR NEW.committed_ordinal<OLD.committed_ordinal THEN
    RAISE EXCEPTION 'frontier rewrite';
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER barrier_guard BEFORE UPDATE OR DELETE ON publication_barrier FOR EACH ROW EXECUTE FUNCTION guard_barrier();
CREATE FUNCTION assert_projection() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE p text; pv bigint; lv bigint; actual mpt_poc.public_projection%ROWTYPE;
BEGIN
  p:=CASE WHEN TG_OP='DELETE' THEN OLD.position_id ELSE NEW.position_id END;
  SELECT max(r.version) INTO pv FROM mpt_poc.position_revision r JOIN mpt_poc.publication_batch b
    USING(position_id,batch_id) WHERE r.position_id=p AND b.publication_status='PUBLISHED';
  SELECT max(r.version) INTO lv FROM mpt_poc.plan_revision r JOIN mpt_poc.publication_batch b
    USING(position_id,batch_id) WHERE r.position_id=p AND b.publication_status='PUBLISHED';
  SELECT * INTO actual FROM mpt_poc.public_projection WHERE position_id=p;
  IF actual.position_version IS DISTINCT FROM pv OR actual.plan_version IS DISTINCT FROM lv THEN
    RAISE EXCEPTION 'projection differs from published frontier';
  END IF;
  RETURN NULL;
END;
$$;
CREATE CONSTRAINT TRIGGER projection_consistency AFTER INSERT OR UPDATE OR DELETE ON public_projection
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_projection();
CREATE CONSTRAINT TRIGGER batch_projection AFTER INSERT OR UPDATE ON publication_batch
  DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION assert_projection();
-- Hardening 0.3 candidate APIs. No function or role has been executed/verified.
CREATE TABLE batch_recovery_audit (
  request_id text PRIMARY KEY, position_id text NOT NULL, batch_id text NOT NULL,
  expected_version bigint NOT NULL, actor text NOT NULL, reason text NOT NULL CHECK (length(reason)>0),
  observed_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  UNIQUE(position_id,batch_id,expected_version),
  FOREIGN KEY(position_id,batch_id) REFERENCES publication_batch
);
CREATE TRIGGER recovery_immutable BEFORE UPDATE OR DELETE ON batch_recovery_audit
  FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
CREATE TABLE worker_lease (
  position_id text NOT NULL REFERENCES position,
  purpose text NOT NULL CHECK(purpose IN ('TP','T4')),
  epoch bigint NOT NULL CHECK(epoch>0), worker_id text NOT NULL,
  expires_at timestamptz NOT NULL,
  PRIMARY KEY(position_id,purpose)
);
CREATE TABLE worker_lease_audit (
  position_id text NOT NULL, purpose text NOT NULL, epoch bigint NOT NULL,
  worker_id text NOT NULL, actor text NOT NULL,
  observed_at timestamptz NOT NULL DEFAULT clock_timestamp(),
  PRIMARY KEY(position_id,purpose,epoch)
);
CREATE TRIGGER lease_audit_immutable BEFORE UPDATE OR DELETE ON worker_lease_audit
  FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();

-- Always lock from the root. Internal helpers have no runtime EXECUTE grant.
CREATE FUNCTION lock_position(p text) RETURNS void LANGUAGE plpgsql AS $$
DECLARE t text; o text;
BEGIN
  SELECT tenant_id,owner_id INTO STRICT t,o FROM mpt_poc.position WHERE position_id=p;
  PERFORM 1 FROM mpt_poc.recipient_guard WHERE tenant_id=t AND owner_id=o FOR UPDATE;
  PERFORM 1 FROM mpt_poc.position_guard WHERE position_id=p FOR UPDATE;
  PERFORM 1 FROM mpt_poc.position WHERE position_id=p FOR UPDATE;
  PERFORM 1 FROM mpt_poc.plan WHERE position_id=p FOR UPDATE;
END;
$$;
CREATE FUNCTION acquire_lease(p text, kind text, worker text, ttl interval) RETURNS bigint
LANGUAGE plpgsql AS $$
DECLARE e bigint;
BEGIN
  IF worker IS NULL OR worker='' OR ttl IS NULL OR ttl<=interval '0' THEN
    RAISE EXCEPTION 'invalid lease arguments'; END IF;
  PERFORM mpt_poc.lock_position(p);
  SELECT epoch INTO e FROM mpt_poc.worker_lease WHERE position_id=p AND purpose=kind FOR UPDATE;
  IF FOUND AND EXISTS(SELECT 1 FROM mpt_poc.worker_lease WHERE position_id=p AND purpose=kind
    AND expires_at>clock_timestamp()) THEN RAISE EXCEPTION 'lease still held'; END IF;
  e:=coalesce(e,0)+1;
  INSERT INTO mpt_poc.worker_lease VALUES(p,kind,e,worker,clock_timestamp()+ttl)
    ON CONFLICT(position_id,purpose) DO UPDATE SET epoch=EXCLUDED.epoch,
      worker_id=EXCLUDED.worker_id,expires_at=EXCLUDED.expires_at;
  INSERT INTO mpt_poc.worker_lease_audit(position_id,purpose,epoch,worker_id,actor)
    VALUES(p,kind,e,worker,session_user);
  RETURN e;
END;
$$;
CREATE FUNCTION check_lease(p text, kind text, worker text, token bigint) RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
  PERFORM 1 FROM mpt_poc.worker_lease WHERE position_id=p AND purpose=kind FOR UPDATE;
  IF NOT EXISTS(SELECT 1 FROM mpt_poc.worker_lease WHERE position_id=p AND purpose=kind
    AND worker_id=worker AND epoch=token AND expires_at>clock_timestamp()) THEN
    RAISE EXCEPTION 'STALE_FENCE' USING ERRCODE='P0001';
  END IF;
END;
$$;
CREATE FUNCTION renew_lease(p text, kind text, worker text, token bigint, ttl interval)
RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  IF ttl IS NULL OR ttl<=interval '0' THEN RAISE EXCEPTION 'invalid ttl'; END IF;
  PERFORM mpt_poc.lock_position(p);
  PERFORM mpt_poc.check_lease(p,kind,worker,token);
  UPDATE mpt_poc.worker_lease SET expires_at=clock_timestamp()+ttl
    WHERE position_id=p AND purpose=kind;
END;
$$;
CREATE FUNCTION release_lease(p text, kind text, worker text, token bigint)
RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  PERFORM mpt_poc.lock_position(p);
  PERFORM mpt_poc.check_lease(p,kind,worker,token);
  UPDATE mpt_poc.worker_lease SET expires_at=clock_timestamp() WHERE position_id=p AND purpose=kind;
END;
$$;
-- Role-specific wrappers prevent a dispatcher taking a publisher lease.
CREATE FUNCTION tp_acquire(p text,w text,ttl interval) RETURNS bigint LANGUAGE sql
AS $$ SELECT mpt_poc.acquire_lease(p,'TP',w,ttl) $$;
CREATE FUNCTION t4_acquire(p text,w text,ttl interval) RETURNS bigint LANGUAGE sql
AS $$ SELECT mpt_poc.acquire_lease(p,'T4',w,ttl) $$;
CREATE FUNCTION tp_release(p text,w text,e bigint) RETURNS void LANGUAGE sql
AS $$ SELECT mpt_poc.release_lease(p,'TP',w,e) $$;
CREATE FUNCTION t4_release(p text,w text,e bigint) RETURNS void LANGUAGE sql
AS $$ SELECT mpt_poc.release_lease(p,'T4',w,e) $$;
CREATE FUNCTION tp_renew(p text,w text,e bigint,ttl interval) RETURNS void LANGUAGE sql
AS $$ SELECT mpt_poc.renew_lease(p,'TP',w,e,ttl) $$;
CREATE FUNCTION t4_renew(p text,w text,e bigint,ttl interval) RETURNS void LANGUAGE sql
AS $$ SELECT mpt_poc.renew_lease(p,'T4',w,e,ttl) $$;

CREATE FUNCTION block_batch(p text,b text,expected bigint,why text) RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  IF why IS NULL OR why='' THEN RAISE EXCEPTION 'reason required'; END IF;
  PERFORM mpt_poc.lock_position(p);
  PERFORM 1 FROM mpt_poc.publication_batch WHERE position_id=p AND batch_id=b FOR UPDATE;
  UPDATE mpt_poc.publication_batch SET publication_status='PUBLICATION_BLOCKED',
    failure_reason=why,state_version=state_version+1
    WHERE position_id=p AND batch_id=b AND state_version=expected
      AND publication_status='PERSISTED_PENDING_PUBLICATION';
  IF NOT FOUND THEN RAISE EXCEPTION 'batch CAS conflict'; END IF;
END;
$$;
CREATE FUNCTION recover_batch(p text,b text,expected bigint,request text,why text) RETURNS bigint
LANGUAGE plpgsql AS $$
DECLARE prior mpt_poc.batch_recovery_audit%ROWTYPE;
BEGIN
  PERFORM mpt_poc.lock_position(p);
  SELECT * INTO prior FROM mpt_poc.batch_recovery_audit WHERE request_id=request;
  IF FOUND THEN
    IF ROW(prior.position_id,prior.batch_id,prior.expected_version,prior.actor,prior.reason)
      IS DISTINCT FROM ROW(p,b,expected,session_user::text,why) THEN
      RAISE EXCEPTION 'recovery idempotency conflict'; END IF;
    RETURN expected+1;
  END IF;
  PERFORM 1 FROM mpt_poc.publication_batch WHERE position_id=p AND batch_id=b FOR UPDATE;
  IF NOT EXISTS(SELECT 1 FROM mpt_poc.publication_batch WHERE position_id=p AND batch_id=b
    AND state_version=expected AND publication_status='PUBLICATION_BLOCKED') THEN
    RAISE EXCEPTION 'recovery CAS conflict'; END IF;
  INSERT INTO mpt_poc.batch_recovery_audit(request_id,position_id,batch_id,expected_version,actor,reason)
    VALUES(request,p,b,expected,session_user,why);
  UPDATE mpt_poc.publication_batch SET publication_status='PERSISTED_PENDING_PUBLICATION',
    failure_reason=NULL,state_version=state_version+1 WHERE position_id=p AND batch_id=b;
  RETURN expected+1;
END;
$$;

CREATE FUNCTION publish_batch(p text,b text,worker text,token bigint) RETURNS bigint
LANGUAGE plpgsql AS $$
DECLARE item mpt_poc.publication_batch%ROWTYPE; n bigint; pv bigint; lv bigint;
BEGIN
  PERFORM mpt_poc.lock_position(p);
  PERFORM mpt_poc.check_lease(p,'TP',worker,token);
  SELECT * INTO STRICT item FROM mpt_poc.publication_batch WHERE position_id=p AND batch_id=b FOR UPDATE;
  IF item.publication_status='PUBLISHED' THEN RETURN item.ordinal; END IF;
  IF item.publication_status<>'PERSISTED_PENDING_PUBLICATION' THEN RAISE EXCEPTION 'batch blocked'; END IF;
  SELECT committed_ordinal+1 INTO STRICT n FROM mpt_poc.publication_barrier
    WHERE domain_id=item.domain_id FOR UPDATE;
  UPDATE mpt_poc.publication_batch SET publication_status='PUBLISHED',ordinal=n,
    failure_reason=NULL,state_version=state_version+1 WHERE position_id=p AND batch_id=b;
  UPDATE mpt_poc.publication_barrier SET committed_ordinal=n WHERE domain_id=item.domain_id;
  SELECT max(r.version) INTO pv FROM mpt_poc.position_revision r JOIN mpt_poc.publication_batch pb
    USING(position_id,batch_id) WHERE r.position_id=p AND pb.publication_status='PUBLISHED';
  SELECT max(r.version) INTO lv FROM mpt_poc.plan_revision r JOIN mpt_poc.publication_batch pb
    USING(position_id,batch_id) WHERE r.position_id=p AND pb.publication_status='PUBLISHED';
  INSERT INTO mpt_poc.public_projection VALUES(p,pv,lv)
    ON CONFLICT(position_id) DO UPDATE SET position_version=EXCLUDED.position_version,plan_version=EXCLUDED.plan_version;
  UPDATE mpt_poc.position_guard SET pending_close_command=NULL
    WHERE position_id=p AND pending_close_command=item.origin_id AND item.origin_type='POSITION_COMMAND';
  -- Deferred predecessor/completeness/projection assertions run in caller's transaction.
  -- No reacquisition of earlier locks: lease is still held from check_lease.
  IF NOT EXISTS(SELECT 1 FROM mpt_poc.worker_lease WHERE position_id=p AND purpose='TP'
    AND epoch=token AND worker_id=worker AND expires_at>clock_timestamp()) THEN
    RAISE EXCEPTION 'STALE_FENCE'; END IF;
  RETURN n;
END;
$$;

CREATE FUNCTION capture_cut(p text,policy text,candidate text) RETURNS text LANGUAGE plpgsql AS $$
DECLARE d text; n bigint; fp text; fb text; result text;
BEGIN
  SELECT pos.domain_id,bar.committed_ordinal,pb.position_id,pb.batch_id INTO d,n,fp,fb
    FROM mpt_poc.position pos JOIN mpt_poc.publication_barrier bar USING(domain_id)
    LEFT JOIN mpt_poc.publication_batch pb ON pb.domain_id=bar.domain_id AND pb.ordinal=bar.committed_ordinal
    WHERE pos.position_id=p;
  IF n IS NULL OR n=0 THEN RAISE EXCEPTION 'NO_PUBLISHED_FRONTIER'; END IF;
  INSERT INTO mpt_poc.publication_cut
    (cut_id,domain_id,ordinal,resolution_policy_version,frontier_position_id,frontier_batch_id)
    VALUES(candidate,d,n,policy,fp,fb)
    ON CONFLICT(domain_id,ordinal,resolution_policy_version) DO NOTHING;
  SELECT cut_id INTO STRICT result FROM mpt_poc.publication_cut
    WHERE domain_id=d AND ordinal=n AND resolution_policy_version=policy;
  RETURN result;
END;
$$;

-- Candidate public surface: published synthetic position facts only, no internal tables.
-- Not a tenant-authorized production endpoint; real tenant access remains BLOCKED.
CREATE VIEW published_positions WITH (security_barrier=true) AS
 SELECT r.position_id,r.version,r.lifecycle,r.side,r.remaining_quantity,r.average_entry_price,
   b.domain_id,b.ordinal FROM public_projection pp
 JOIN position_revision r ON r.position_id=pp.position_id AND r.version=pp.position_version
 JOIN publication_batch b ON b.position_id=r.position_id AND b.batch_id=r.batch_id
 WHERE b.publication_status='PUBLISHED';

-- Command events/journal are also content: blocked or recovered command batches reject append.
CREATE FUNCTION guard_command_content() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE cmd text; s text; frozen boolean;
BEGIN
  IF TG_TABLE_NAME='position_event' THEN cmd:=NEW.command_id;
  ELSE
    SELECT command_id INTO cmd FROM mpt_poc.position_event
      WHERE position_id=NEW.position_id AND event_id=NEW.event_id;
  END IF;
  SELECT publication_status,content_frozen INTO s,frozen FROM mpt_poc.publication_batch
    WHERE position_id=NEW.position_id AND origin_type='POSITION_COMMAND' AND origin_id=cmd FOR UPDATE;
  IF s IS DISTINCT FROM 'PERSISTED_PENDING_PUBLICATION' OR frozen THEN
    RAISE EXCEPTION 'command content is sealed or missing parent';
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER command_content_guard BEFORE INSERT ON position_event
  FOR EACH ROW EXECUTE FUNCTION guard_command_content();
CREATE TRIGGER journal_content_guard BEFORE INSERT ON personal_journal_entry
  FOR EACH ROW EXECUTE FUNCTION guard_command_content();
CREATE TRIGGER journal_immutable BEFORE UPDATE OR DELETE ON personal_journal_entry
  FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
-- Initial-state defense applies even to API-owner INSERTs; runtime grants below
-- additionally deny caller-supplied state and lease columns.
CREATE FUNCTION guard_initial_delivery() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF TG_TABLE_NAME='notification' THEN
    IF NEW.delivery_status<>'READY' THEN RAISE EXCEPTION 'initial notification must be READY'; END IF;
  ELSE
    IF NEW.dispatch_status<>'PENDING' OR NEW.lease_token IS NOT NULL OR NEW.lease_until_observed IS NOT NULL THEN
      RAISE EXCEPTION 'initial outbox must be PENDING without lease';
    END IF;
  END IF;
  RETURN NEW;
END;
$$;
CREATE TRIGGER initial_notification BEFORE INSERT ON notification FOR EACH ROW EXECUTE FUNCTION guard_initial_delivery();
CREATE TRIGGER initial_outbox BEFORE INSERT ON outbox_event FOR EACH ROW EXECUTE FUNCTION guard_initial_delivery();
CREATE TRIGGER destination_call_immutable BEFORE UPDATE OR DELETE ON synthetic_destination_call
  FOR EACH ROW EXECUTE FUNCTION deny_fact_mutation();
-- All candidate functions are owned by the NOLOGIN migration owner. Fixed trusted
-- search_path; pg_temp last; no dynamic user-supplied SQL; no PUBLIC EXECUTE.
DO $$
DECLARE f record;
BEGIN
 FOR f IN SELECT oid::regprocedure AS signature FROM pg_proc
   WHERE pronamespace='mpt_poc'::regnamespace LOOP
   EXECUTE format('ALTER FUNCTION %s SECURITY DEFINER',f.signature);
   EXECUTE format('ALTER FUNCTION %s SET search_path TO pg_catalog, mpt_poc, pg_temp',f.signature);
 END LOOP;
END;
$$;
REVOKE ALL ON SCHEMA mpt_poc FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA mpt_poc FROM PUBLIC;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA mpt_poc FROM PUBLIC;
GRANT USAGE ON SCHEMA mpt_poc TO mpt_reader,mpt_writer,mpt_evaluator,mpt_publisher,mpt_dispatcher,mpt_recovery;
GRANT SELECT ON published_positions TO mpt_reader;
-- Trusted internal writers can read synthetic state; no production RLS claim.
GRANT SELECT ON ALL TABLES IN SCHEMA mpt_poc TO mpt_writer,mpt_evaluator,mpt_publisher,mpt_dispatcher,mpt_recovery;
GRANT INSERT ON command_receipt,position_event,position_revision,plan_revision,personal_journal_entry,
 publication_batch,publication_member,assessment_result,notification_decision TO mpt_writer;
GRANT INSERT(position_id,notification_id,batch_id,origin_type,command_event_id,result_id,
 policy_id,policy_version,destination_id,dedup_key) ON notification TO mpt_writer;
GRANT INSERT(position_id,outbox_id,batch_id,command_event_id,result_id,notification_id)
 ON outbox_event TO mpt_writer;
GRANT UPDATE(persisted_version) ON position,plan TO mpt_writer;
GRANT UPDATE(pending_close_command) ON position_guard TO mpt_writer;
GRANT UPDATE(execution_status,failure_code) ON assessment_attempt TO mpt_writer;
GRANT INSERT ON assessment_attempt TO mpt_evaluator;
GRANT EXECUTE ON FUNCTION lock_position(text) TO mpt_writer;
GRANT EXECUTE ON FUNCTION capture_cut(text,text,text) TO mpt_evaluator;
GRANT EXECUTE ON FUNCTION publish_batch(text,text,text,bigint),tp_acquire(text,text,interval),
 tp_release(text,text,bigint),tp_renew(text,text,bigint,interval) TO mpt_publisher;
GRANT EXECUTE ON FUNCTION block_batch(text,text,bigint,text),recover_batch(text,text,bigint,text,text) TO mpt_recovery;
GRANT EXECUTE ON FUNCTION t4_acquire(text,text,interval),t4_release(text,text,bigint),
 t4_renew(text,text,bigint,interval) TO mpt_dispatcher;
-- No direct mutation grants to publisher/dispatcher/recovery, nor TP grants to writer/evaluator.
-- T4 API follows in runner/delivery-api.sql; it is candidate-only and subject to review.
COMMIT;
