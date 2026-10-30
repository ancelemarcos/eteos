# Owned-child controller contract H01-CTRL@1 - candidate 0.8

PROPOSED / BLOCKING_EXECUTION_REVIEW / NOT_RUN. Specification only.
runner/worker_controller_stub.py stays byte-for-byte unchanged and non-operational.
No OS primitive, process signal, executable supervisor or new scenario is enabled.

## Identity, capabilities and lifecycle

One supervisor instance belongs to one run_id, approved config hash, manifest hash and sandbox
identity. It spawns only a fixed, independently approved synthetic worker executable/image with
a fixed argument schema; no shell, arbitrary executable/path/command, kill-by-name, PID selector,
attach-to-existing-process, host service or PostgreSQL server targeting is permitted.
The supervisor holds an OS child capability from creation through confirmed exit. PID plus
creation metadata is audit information, never targeting authority. Never reacquire by PID.
Creation identity = sandbox instance + supervisor nonce + child generation + OS creation token;
reuse of any component across a restart is rejected. Log only an opaque capability evidence ID,
not raw handles or secrets. A replacement requires a NEW retained handle and generation.

| State | Required transition / checkpoint | Failure closes with |
| --- | --- | --- |
| DISABLED | Independent human implementation authorization and approved OS/sandbox/capability contract | No spawn if approval or evidence missing |
| SPAWNED | Atomic constrained child creation; inherited dedicated IPC; record handle/PID/creation/sandbox and executable/config hash | No fallback to general process API |
| IDENTITY_CONFIRMED | Verify child capability and IPC peer identity against spawned child, run nonce and generation | Reject any mismatch or unknown peer |
| CHECKPOINT_OPEN | Child executes AUTHORIZE; sends OPEN only after SQL returns and before commit; waits for supervisor | Unknown outcome on disconnect; never infer rollback |
| CHECKPOINT_COMMITTED | Alternative schedule: commit authorization/audit/receipt, receive DB acknowledgement, send COMMITTED; wait without calling destination | Commit uncertainty requires identity-based recovery |
| TERMINATING | Supervisor interrupts ONLY its retained child capability at selected checkpoint | Cannot target a replacement PID |
| EXIT_CONFIRMED | OS wait confirms child exit; record exit kind/code and generation; separately confirm its DB backend gone/rollback completed | No restart/read oracle before bounded confirmation |
| RESTARTED | Create new isolated child with same logical operation/approved login, new OS identity/IPC nonce | No adoption of surviving/unrelated process |
| REPLAYED | Recover/retry same operation ID/payload; compare snapshot and unique audit/receipt counts | Payload divergence must reject; no duplicate writes |
| REVALIDATED | Fresh RECHECK operation immediately before any synthetic call | Historical replay never grants fresh permission |
| COMPLETE | Persist signed-independent provenance references and observed outcomes | No PASS until approved execution and verified evidence |

Process death is not proof DB transaction rollback has completed. Observer must confirm backend
absence and then acquire a new consistent read snapshot. Never snapshot while asynchronous
rollback remains possible. A crash between DB commit and IPC is explicitly UNKNOWN, recovered
from durable operation identity, not an invented COMMITTED/ROLLED_BACK label.

## IPC, timeouts and privileges

Proposed channel: private inherited duplex OS pipe/socket pair created by the supervisor,
no TCP listener/discoverable shared path. Only child endpoint inherited; no general handle
inheritance. OS isolation/peer attribution and channel confidentiality require platform-specific
human review before implementation. This specification does not claim portability by itself.
Bound message size, allowed states and schema. Each message binds run_id, supervisor nonce,
child generation/creation identity, sequence, phase and operation ID. Reject duplicate,
out-of-order, wrong-generation, unknown-field and unauthenticated messages. Secrets never in IPC logs.
A missing, malformed or stale message triggers refusal/unknown-outcome handling, not successful kill.

Spawn, identity handshake, checkpoint, exit, DB-backend disappearance and restart deadlines are
separate positive bounded durations approved in external config; numeric values UNRESOLVED.
Monotonic supervisor time measures deadline only, never market/commit time. No sleep is an oracle.
If exit is unconfirmed, stop the control and preserve evidence; never widen kill scope.
Cleanup may act only on retained owned-child capabilities under explicit approved policy.

Supervisor gets create/wait/terminate rights only for its sandbox child. No host administrator,
server restart, broad signal capability or arbitrary database DDL. Child uses approved dispatcher
login only. Independent observer uses narrowly reviewed read/monitor access and cannot approve
configuration or produce collector signatures. Credential handoff uses approved external secret
mechanism/inherited channel, not command line or evidence. Signer/private keys stay outside worker.

## Acceptance matrix for future specifically authorized implementation

| Test ID | Schedule / future evidence | Required result | Current status |
| --- | --- | --- | --- |
| CTRL-IDENTITY | Wrong nonce/generation/creation token, PID reuse, fabricated metadata | No signal/spawn outside retained capability; refusal logged | BLOCKING_EXECUTION_REVIEW |
| CTRL-IPC | Duplicate/out-of-order frame, timeout, disconnect, unknown commit outcome | Fail closed; recover durable identity, never infer outcome | BLOCKING_EXECUTION_REVIEW |
| PROCESS-WORKER-BEFORE-COMMIT | OPEN checkpoint then actual child exit; independent DB rollback confirmation | Full stored-state hash equals before; restart produces one auth/audit/receipt, calls0 | BLOCKING_EXECUTION_REVIEW |
| PROCESS-WORKER-AFTER-COMMIT | COMMITTED checkpoint then actual child exit/restart/replay | Post-commit stored-state hash unchanged by replay; auth/audit/receipt1, calls0 | BLOCKING_EXECUTION_REVIEW |
| CTRL-CLOSE-RECHECK | Close after original auth and before fresh recheck on restarted child | SUPPRESSED_AFTER_AUTHORIZATION, prior auth preserved, calls0 | BLOCKING_EXECUTION_REVIEW |
| CTRL-CONTENT-CONFLICT | Same operation ID with different canonical payload | P0001 plus complete state equality | BLOCKING_EXECUTION_REVIEW |
| CTRL-ISOLATION | Independently measured sandbox/capabilities/executable hashes | Cannot address host/service/server/other run; human approval | BLOCKING_EXECUTION_REVIEW |

Snapshots follow FULL-SNAPSHOT-CONTRACT.md; process observations are separate evidence.
Backend termination tests already authored do not satisfy process/IPC acceptance rows.
Server crash/network failure remain OUT_OF_SCOPE_PROPOSED exclusions, not approved omissions.
Implementation order: review OS isolation/capabilities -> approve IPC/timeouts/secret handoff ->
authorize code implementation -> review source -> separately authorize execution. This order
does not authorize any of those implementation/execution transitions.

## Pure validation checkpoint 0.9 (order v0.7)

runner/worker_identity.py materializes Identity/Binding/CheckState and pure validate_identity,
validate_restart, validate_checkpoint functions. They check internal run/sandbox/capability-token,
generation, nonce, sequence/phase and deadline consistency without OS or IO operations.
No actual peer authentication, spawn/exit or capability ownership is established by these inputs.
Acceptance cases are documented in CODEC-MATERIALIZATION.md; all remain MATERIALIZED_NOT_RUN.
runner/worker_controller_stub.py stays byte-identical and all operational scenarios remain
blocked. No process API or runtime integration has been added; real supervisor remains BLOCKED.


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
