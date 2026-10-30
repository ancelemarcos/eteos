# Candidate package 0.9 - runner implementation 0.7

REQUIRES_HARDENING / NOT_RUN. EXEC-G1/PERS-G1 OPEN.
PUB-T13B PENDING_HUMAN_APPROVAL. No SQL/Python/runner/tests/install/preparation is authorized.

## Files and execution boundary

run.py owns transaction boundaries and scenario dispatch; coverage_controls.py supplies bounded
negative/lease/backend controls; operations.sql and oracles.sql provide named statements.
SCENARIO-MATRIX.md is the sole current scenario/status contract.
worker_controller_stub.py is NON-OPERATIONAL: every method rejects, with no OS/process/DB
primitives or target input. PROCESS-WORKER-BEFORE-COMMIT, PROCESS-WORKER-AFTER-COMMIT and
COMPOUND-MEMBER-SEAM unconditionally emit NOT_RUN/BLOCKING_EXECUTION_REVIEW before sessions.
Neither config flags nor a signature can enable these controls.

prepare.sql/cleanup.sql remain separately authorized manual lab candidates; runner never calls
them. Each materialized scenario requires an independently approved fresh disposable
mpt_poc_lab schema. No automatic database, container, role or dependency provisioning.

## Freeze and evidence

ENVIRONMENT-FREEZE.md maps each required value to approval, observation and current missing
evidence. Copy approval.example.json outside the package and approve its exact SHA-256 through
an independent channel. It remains false/UNRESOLVED. Freeze exact PostgreSQL/image, Python,
psycopg/cryptography/dependencies, extensions, settings, role inventories, controller/isolation,
collector/key/signature/freshness and clock evidence. No values have been fabricated.

environment_guard.py verifies independent config hash before the complete freeze structure;
then manifest/file inventory/HEAD and runtime dependencies, signed external image/cluster/freeze
evidence with bounded capture age, actual server and effective-role inventories.
All initial sessions validate before fixtures. Required unknown/missing/mismatched/expired
evidence blocks. Signatures bind attestations, not proof that an untrusted collector is honest.
Independent review of isolation/permissions/signing/clock evidence is required; no supervisor
implementation exists and external worker control remains blocked even after environment freeze.

Privilege fingerprints include current role, membership flags, ownership, column/function grants
and observed controller capabilities. Login separation and privileges are approved independently.
Owner is a trusted synthetic fixture/sink/termination controller exception; writer/dispatcher
negative tests use their actual runtime roles. No writer production role receives fault/kill rights.
DB termination control needs reviewed pg_signal_backend-equivalent authority for the specific
runtime backend; monitor pg_read_all_stats/pg_control_system and DDL owner capabilities must
be inventoried. Never use this as justification for broad runtime grants.

Hash encodings: dependency inventory is sorted lowercase name/version pairs with compact JSON;
privilege inventory is verify_privileges' observed dictionary with sorted keys and compact JSON;
both UTF-8/SHA-256. Freeze records require independently approved hashes/identities and exact match
inside the signed JSON. Raw Ed25519 signature verification policy ED25519-RAW-JSON-V1 requires
separate approval; example policy remains UNRESOLVED. No secret is part of logged inventory.

Future invocation syntax only, not permission:

    python -B run.py SCENARIO --approval APPROVED_CONFIG --approved-config-sha256 APPROVED_HASH --evidence NEW_JSONL

Use approved MPT_OWNER_DSN, MPT_PUBLISHER_DSN, MPT_WRITER_DSN, MPT_EVALUATOR_DSN,
MPT_DISPATCHER_DSN, MPT_RECOVERY_DSN and MPT_READER_DSN environment variables.
DSNs/private keys/collector credentials must stay outside logs and package.
Evidence files are opened exclusively outside the package; prior results are never overwritten.
JSONL start is NOT_RUN; verified provenance plus observed environment/roles precede fixtures.
No preflight was executed in this round. Refusal does not constitute a verified environment.

## Limits

H-02/H-04 controls remain authored/unexecuted. Backend termination is not worker/server failure;
simulated reply loss is not a broken network connection. Historical T4 response requires a
fresh RECHECK before send. Synthetic receipt is not provider confirmation.
The member seam and functional/expanded scope are proposals in SCOPE-PROPOSAL.md; no exclusion
is accepted. No physical exactly-once, universal deadlock or performance guarantee.


## Documentation-only revision 0.8 (order v0.5)

Executable SQL, Python, stub and approved-config example remain unchanged at implementation
policy version 0.7; no scenario is enabled. WORKER-CONTROLLER-CONTRACT.md (H01-CTRL@1)
specifies owned-child identity/IPC/exit/restart and independent future acceptance.
FULL-SNAPSHOT-CONTRACT.md (MPT-SNAPSHOT@1) defines the 30-table canonical snapshot, exact
columns/PKs/type encoding/digests and documentary oracles. That specification now exists;
its encoder/consistent collector/reference vectors remain unimplemented. Existing snapshot(lab)
JSONB equality is not that canonical algorithm or a guaranteed single MVCC snapshot.
INTRABATCH-SEAM-PROPOSAL.md specifies H05-SEAM-PENDING between v2/v3 logical validation,
with a fixed test-only hook and proposed PZ501; no active DDL, grant or SQL modification.
ENVIRONMENT-FREEZE.md assigns approval responsibilities and distinguishes observed values
from declarations and approval. All actual runtime evidence remains UNRESOLVED.


## Current order v0.7 / candidate 0.9 disposition

CODEC-MATERIALIZATION.md is the current implementation-boundary reference. New snapshot
encoder/reference parser/schema/static vectors and pure worker identity validators are
MATERIALIZED_NOT_RUN. They are not imported by run.py or wired into collection/process control.
Previous statements that these modules do not exist are superseded; statements that no
collector/supervisor is operational remain true. Stub, schema.sql, publication APIs, run.py,
preflight and config are unchanged. Runtime policy remains 0.7; package revision is 0.9.
No order v0.6 was located in the available attachments/candidate docs; its content is not assumed.
Full codec equivalence and compound independent vectors remain BLOCKED. No preflight or test
was executed; proposed seam remains DOCUMENTED/BLOCKED. Gates remain open.


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
