# Complete persisted-state snapshot MPT-SNAPSHOT@1 - candidate 0.8

PROPOSED / NOT_RUN. Deterministic specification, not an implemented or executed encoder.
Existing snapshot(lab) compares JSONB table values over separate queries; it is NOT this
canonical algorithm and does not claim a single MVCC snapshot or these hashes.
Implementing the encoder/collector and freezing independent vectors requires later authorization.

## Exact schema coverage

Scope is ALL rows of the following 30 mpt_poc tables, all listed columns in listed order.
PK order is explicit. No filter by test position, published state or current cut may omit rows.
Validate actual catalog table/column/type/nullability/PK identity against these declarations and
schema.sql plus runner/delivery-api.sql bound by manifest; unknown/missing fields/tables fail closed.

| Table | PK | Ordered columns |
| --- | --- | --- |
| publication_domain | domain_id | domain_id, policy_version |
| publication_barrier | domain_id | domain_id, committed_ordinal |
| recipient_guard | tenant_id,owner_id | tenant_id, owner_id, access_version, access_allowed |
| position | position_id | position_id, domain_id, tenant_id, owner_id, instrument_label, persisted_version |
| position_guard | position_id | position_id, pending_close_command |
| command_receipt | tenant_id,owner_id,command_id | tenant_id, owner_id, command_id, position_id, actor_id, action, expected_position_version, expected_plan_version, canonical_payload, fingerprint, response_code, response_payload |
| publication_batch | position_id,batch_id | position_id, batch_id, domain_id, origin_type, origin_id, fingerprint, publication_status, ordinal, failure_reason, content_frozen, state_version |
| publication_cut | cut_id | cut_id, domain_id, ordinal, resolution_policy_version, frontier_position_id, frontier_batch_id, capture_transaction |
| position_event | position_id,event_id | position_id, event_id, command_id, event_type, correction_of, recorded_at_observed, user_reported_execution_at |
| position_revision | position_id,version | position_id, version, predecessor_version, event_id, batch_id, lifecycle, side, remaining_quantity, average_entry_price, last_confirmed_at_observed |
| plan | position_id | position_id, persisted_version |
| plan_revision | position_id,version | position_id, version, predecessor_version, batch_id, command_id, stop_price, target_price, note |
| personal_journal_entry | position_id,entry_id | position_id, entry_id, event_id, note, recorded_at_observed |
| public_projection | position_id | position_id, position_version, plan_version |
| assessment_attempt | position_id,attempt_id | position_id, attempt_id, domain_id, cut_id, position_version, plan_version, rule_id, rule_version, parameter_identity, execution_status, assessment_mode, decision_time_observed, reconstructed_at_observed, failure_code |
| assessment_result | position_id,result_id | position_id, result_id, attempt_id, batch_id, supersedes_result_id, fingerprint, evaluability, content_nature, content_text, limitation |
| notification_decision | position_id,result_id | position_id, result_id, policy_id, policy_version, decision, reason |
| publication_member | position_id,batch_id,member_order | position_id, batch_id, member_order, position_version, plan_version, result_id |
| notification | position_id,notification_id | position_id, notification_id, batch_id, origin_type, command_event_id, result_id, policy_id, policy_version, destination_id, dedup_key, delivery_status |
| outbox_event | position_id,outbox_id | position_id, outbox_id, batch_id, command_event_id, result_id, notification_id, dispatch_status, lease_token, lease_until_observed |
| send_authorization | position_id,authorization_id | position_id, authorization_id, notification_id, tenant_id, owner_id, access_version, policy_version, final_check_position_version |
| access_audit | tenant_id,owner_id,access_version | tenant_id, owner_id, access_version, allowed, reason |
| delivery_audit | position_id,audit_id | position_id, audit_id, notification_id, authorization_id, reason, checkpoint |
| synthetic_destination_receipt | destination_id,dedup_key | destination_id, dedup_key, authorization_id, payload_fingerprint |
| synthetic_destination_call | call_id | call_id, destination_id, dedup_key, authorization_id, checkpoint |
| domain_resolution_policy | domain_id,policy_version | domain_id, policy_version |
| batch_recovery_audit | request_id | request_id, position_id, batch_id, expected_version, actor, reason, observed_at |
| worker_lease | position_id,purpose | position_id, purpose, epoch, worker_id, expires_at |
| worker_lease_audit | position_id,purpose,epoch | position_id, purpose, epoch, worker_id, actor, observed_at |
| t4_operation_receipt | position_id,operation_id | position_id, operation_id, notification_id, request_payload, request_fingerprint, response |

The enumerated set above is normative (30 tables); count assertions must equal 30.
No persisted columns are excluded: lease expiry, audit observation times and capture_transaction
remain included even if different across independent runs. Equality is within a controlled run;
never zero volatile values to force hashes to match.

Views are not base tables. published_positions is separately encoded with columns
position_id, version, lifecycle, side, remaining_quantity, average_entry_price, domain_id, ordinal;
key position_id. Catalogs, indexes, WAL, sequences/internal MVCC tuple headers, DB transaction
snapshot ID and process observations are excluded from stored-row hash because they are not
these logical persisted rows; bind schema and environment evidence separately. Logical xid8
capture_transaction IS included, unlike internal xmin/xmax.

## Collection boundary

Future observer uses a NEW read-only REPEATABLE READ transaction after explicit checkpoint and
confirmed completion/rollback. All table scans, view and metadata are from that SAME MVCC
snapshot; no writers may mutate during intended equality boundaries. This observer isolation
does not change application READ COMMITTED or T2a/T2b. Controller observes stable barriers and
records backend identity/snapshot transaction separately. Time passing alone is not a row mutation.
If lease renewal/recovery is intentionally interleaved, compare explicit permitted row deltas
rather than claiming complete-state equality. Fail on incomplete scans or insufficient privileges.

## Canonical byte algorithm

Define F(tag,payload) as ASCII tag (exactly one byte), followed by unsigned 64-bit BIG-ENDIAN
payload byte length, followed by payload bytes. Reject lengths exceeding 2^64-1. Concatenation
below means raw bytes, no delimiters/BOM/newlines. SHA-256 outputs lowercase hex externally;
nested digests use their raw 32 bytes. All text UTF-8, no Unicode normalization, no locale collation.

Each scalar is F(tag,payload):
- SQL NULL: tag N, empty payload. Distinct from JSON null or empty text.
- text: T, exact stored UTF-8 bytes, including spaces/escapes/newlines.
- bool: B, ASCII 0 or 1.
- integer/int8/int4: I, signed base-10 with no plus/leading zeros, zero = 0.
- xid8: X, unsigned base-10, never converted to float or truncated.
- numeric: D, ASCII coefficient followed by colon followed by scale. Use exact base-10
  unscaled coefficient and stored dscale, no exponent/binary float; 1.00 -> 100:2,
  1.0 -> 10:1, -0.00 -> 0:2. Stored scale is retained; nonfinite values reject.
- bytea: Y, exact bytes (not hex-string text). No bytea column currently exists; any schema
  addition still requires inventory/version review even though encoding is defined.
- timestamptz: Z, signed integer microseconds since 1970-01-01T00:00:00Z, computed exactly,
  never via floating epoch or milliseconds. Infinity rejects. Retain PostgreSQL's complete
  stored microsecond precision. Original submitted timezone/sub-microsecond precision is
  not recoverable if storage already discarded it; make no preservation claim for that.
- jsonb: J, recursively encode stored parsed value: null F(n,empty), bool F(b,0/1),
  string F(s,exact UTF-8), number F(d,coefficient:scale), array F(a,concatenated child frames),
  object F(o,concatenated F(k,key UTF-8)+value frames sorted by unsigned UTF-8 key bytes).
  Parse numbers losslessly retaining stored decimal scale. Original input whitespace/order/
  duplicate keys were already lost by jsonb; do not reconstruct them. String "null" differs
  from JSON null, which differs from SQL NULL. Reject unsupported/nonfinite values.

Row = F(r,concatenated column scalar frames in declared order).
PK bytes = F(k,concatenated PK scalar frames in declared PK order).
Sort rows by unsigned lexicographic PK bytes (not SQL locale/numeric ordering); reject duplicate
PK bytes. This sort may put version10 before version2; canonical identity, not event chronology.
Schema descriptor = F(s,for each column: F(c,name UTF-8)+F(t,canonical PostgreSQL type name)
+F(b,ASCII nullable 0/1), followed by F(p,concatenated F(c,PK column name))).
Use exact type names text, boolean, integer, bigint, numeric, timestamp with time zone, xid8,
jsonb as declared, not unstable OIDs. Descriptor values validated from manifest-bound DDL.

Table digest = SHA256(F(v,"MPT-SNAPSHOT@1") + F(t,qualified table name) + descriptor
+F(c,ASCII row count)+F(r,concatenated Row frames)).
All persisted tables sorted by unsigned qualified-name UTF-8 bytes.
Persisted global digest = SHA256(F(v,"MPT-SNAPSHOT@1/PERSISTED")
+ concatenated F(t,qualified name)+F(h,raw table digest)).
Empty tables still contribute their descriptor/count/empty rows digest.

Aggregate digests: partition whole rows of each position_id-bearing table by exact position_id.
For each position, same table framing/count/rows but prefix version "MPT-SNAPSHOT@1/POSITION"
and include F(p,position_id). Tables without position_id form one GLOBAL partition using version
"MPT-SNAPSHOT@1/GLOBAL". synthetic_destination_* remain GLOBAL, not heuristically assigned.
Hash partition table digests using the same sorted-name recipe. Include empty position-scoped
tables for every position present in ANY position_id-bearing table. Aggregate digests aid
localization; full persisted digest remains authoritative.

Published digest uses the view table recipe with version "MPT-SNAPSHOT@1/PUBLISHED".
Publication metadata = same-snapshot encoded rows of publication_barrier, publication_cut,
publication_batch and public_projection in table-name order (all rows, no hidden exclusions).
Envelope digest = SHA256(F(v,"MPT-SNAPSHOT@1/ENVELOPE")+F(h,persisted global raw digest)
+F(h,published raw digest)+F(h,SHA256(publication metadata))
+F(m,raw manifest digest)+F(c,raw approved config digest)+F(r,run_id UTF-8)).
Process observation digest is separate and not part of persisted/envelope equality; it records
checkpoint/OS identity/exit evidence and observation time with a separately approved schema.
Different run/config/manifest changes envelope even for identical rows. Comparison reports
both persisted digest equality and provenance; never compares only selected member fingerprints.

## Documentary fixtures/oracles (not executed; no fabricated hash values)

| Fixture ID | Arrangement and boundary | Required oracle |
| --- | --- | --- |
| SNAP-ROLLBACK-1 | Snapshot S0; AUTHORIZE uncommitted; own worker exits; confirm backend rollback; S1 | All table digests/global/published equal S0; auth/audit/operation receipt absent; process evidence differs |
| SNAP-ACK-LOSS-1 | S0; AUTHORIZE commits; S1; reply lost; replay same ID; S2 | S1 differs S0 only in declared delivery/auth/audit/receipt rows; S2 equals S1 completely |
| SNAP-REPLAY-1 | Same valid worker/epoch, no unrelated writers or renewals; replay RECHECK | Table/global/published/envelope equal; no new audit/receipt |
| SNAP-DIVERGENCE-1 | Reuse operation ID with changed payload; P0001 | Full snapshot unchanged; error evidence separate |
| SNAP-CONTENT-1 | Independent encoded copy changes one non-key text byte or numeric stored scale | Relevant row/table/aggregate/global digest changes; inventory/count unchanged |
| SNAP-ORDER-1 | Same stored rows delivered in reverse scan order | Identical canonical bytes/digests |
| SNAP-TYPES-1 | SQL NULL, JSON null, empty text/bytea, numeric1.0/1.00, timestamps 1 microsecond apart | Distinct typed bytes; no binary-float rounding |

Require independent reference vectors and encoder review before promotion; no expected hash literal
was invented here. A hash detects byte equality under this contract, not temporal admissibility,
actual worker execution, authorization, external delivery or MIR availableAt <= decisionTime.

## Materialization checkpoint 0.9 (order v0.7)

Candidate source now exists in runner/snapshot_codec.py and independent parser in
runner/snapshot_reference.py; metadata in snapshot_schema.json and manually authored bytes
in snapshot_vectors.json. See CODEC-MATERIALIZATION.md for explicit framing interpretations,
caller trust and oracle gaps. No module was imported, executed, compiled or collected against DB.
Scalar/table implementations are MATERIALIZED_NOT_RUN; full contract conformance is BLOCKED
pending independent compound vectors and review of partition/metadata/view descriptor choices.
The existing separate-query JSONB snapshot helper is unchanged and is NOT this implementation.
Future MVCC collector remains DOCUMENTED/BLOCKED, with read-only consistent observer contract.


## Order v0.8 / candidate 0.10 current checkpoint

CODEC-CONFORMANCE-MATRIX.md is the current field/byte/oracle map and explicitly resolves
candidate partition placement, metadata streams, view semantic nullability, key ordering and
value precision. New snapshot_compound_vectors.json carries manual structure/byte expectations;
intermediate/full digest oracles remain UNRESOLVED. Codec/ref parser parity guards and strict
worker identity field typing were tightened; none were executed. No encoding helper is shared
with the independent reference parser.

SNAPSHOT-COLLECTOR-DESIGN.md and runner/snapshot_collector.py now provide a disabled-by-default,
unintegrated read-only MVCC collector candidate. Earlier statements that no collector source
exists are superseded; no collection/connection/test actually occurred. It requires approved
manifest/schema/config bytes, dedicated read-only connection/role, exact catalog/version and
one REPEATABLE READ READ ONLY snapshot, with rollback/close. No connect(), main or runner hook.
collector-approval.example.json remains false/UNRESOLVED. Safety/conformance validation BLOCKED.
No SQL publication function, active seam, operational supervisor or gate was changed.
