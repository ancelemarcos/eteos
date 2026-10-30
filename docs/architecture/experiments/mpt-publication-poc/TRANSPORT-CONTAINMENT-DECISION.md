# Transport containment decision - candidate 0.14 / order v1.2

## Order v1.3 - separate containment gates

A0 remains default. No implementation, activation or reinterpretation of a guarantee occurs.

| Requirement | Evidence necessary | Residual risk | Separate gate / current state |
| --- | --- | --- | --- |
| C-FIELD | All field/protocol lengths admitted before full client allocation, independently audited and fault-tested | Cursor/process limits do not provide this property | Field-admission design approval; BLOCKING_EXECUTION_REVIEW |
| C-NATIVE | Native allocation instrumentation, one oversized field and fragmented protocol/buffer cases | Driver/TLS overhead and hidden copies | Pinned transport-build review; UNRESOLVED |
| C-PROCESS | Approved OS accounting metric and tested memory isolation including escape/overshoot | Accounted memory differs from per-field rejection and RSS promises | Owned-worker isolation approval; UNRESOLVED |
| C-CALL | Parent monotonic wait deadline with declared scheduling tolerance and blocked-call experiment | OS stalls and cleanup after timeout | Deadline/failure-model approval; UNRESOLVED |
| C-CANCEL | Cancellation request, acknowledgement and independent query/session state observation | Request may be ignored or race completion | Driver/build cancellation review; UNRESOLVED |
| C-CHILD | Owned handle/capability and creation identity; no arbitrary PID; containment before workload | Handle leaks, parent death, escape or mistaken ownership | Separate owned-child controller authorization; BLOCKING_EXECUTION_REVIEW |
| C-CLEANUP | Primary/cleanup errors plus local exit and separately observed server rollback | Lost connection leaves server state uncertain | Cleanup/quarantine authority; UNRESOLVED |

Replacing C-FIELD with C-PROCESS would change a requirement, not satisfy it by equivalence.
A human decision must explicitly describe the relaxed property, failure/overshoot tolerance,
version/contract effects and invalid-result handling. No such change is approved here.
Offline codec authorization cannot open any gate in this table. No supervisor or process action.

PROPOSED / DOCUMENTED / NOT_RUN. Decision pending; no mechanism installed or activated.
Baseline driver family is synchronous Psycopg 3 in runner/run.py. Exact Python, psycopg, libpq,
PostgreSQL, OS and isolation builds/digests are UNRESOLVED. Sources below describe mechanisms,
not evidence about the current machine. SNAP-P01..05 and all accepted decisions are unchanged.

## Distinct obligations

C-FIELD: reject an oversized field before allocating its full representation on the client.
C-NATIVE: bound native driver/network buffers, including one row and protocol overhead.
C-PROCESS: bound the worker's accounted memory, with explicit accounting/overshoot semantics.
C-CALL: bound how long the parent waits for a blocked operation, independently of that operation.
C-CANCEL: request cancellation, observe its outcome, and never infer termination from the request.
C-CHILD: terminate only the owned isolated child if separately authorized and identity is verified.
C-CLEANUP: preserve primary/cleanup errors and distinguish local termination from server rollback.
No one of these obligations implies the others. Strict wall-clock guarantees need a declared OS
scheduling tolerance and failure model; a general-purpose OS is not a real-time proof.

## Alternatives

| Alternative / mechanism | Trust boundary and build dependency | Contains | Does not contain | Proof needed | Cost | Human authorization |
| --- | --- | --- | --- | --- | --- | --- |
| A0 Refuse collection | Existing candidate admission, artifact integrity | All collection exposure while refusal is preserved | Provides no collected result | Static guard review; future no-call negative test | No data progress | Current default; retain |
| A1 Named Psycopg ServerCursor + fetchmany | PostgreSQL/driver/libpq, exact versions and row factories | Incremental row retrieval instead of whole-result client buffering | C-FIELD, strict C-NATIVE/C-PROCESS/C-CALL; one field may be large | Native allocation and large-field measurements, actual fetch behavior | Low/moderate code complexity | Separate experiment approval; insufficient alone |
| A2 libpq nonblocking send/consume/get-result with owned event loop | Native libpq and reviewed socket/event integration | Parent event-loop scheduling and readiness checks | Full field allocation inside libpq, Python expansion, total process memory; polling is not hard termination | Instrument all allocation/blocking paths; cancellation/loss tests against pinned build | High integration/review cost | Separate transport design/build approval |
| A3 Trusted server-side size admission before transfer | Approved query semantics, unchanged MVCC snapshot, trusted server/DDL/privilege quiescence | Can refuse known oversize stored representations before sending those values | Malicious server/protocol, server memory, alternate transfer encoding/expansion, metadata responses, native buffer peaks | Prove all data/catalog projections, encoding expansion and zero omission under one snapshot | Extra scans and query complexity | Explicit query/semantic review; no SQL changes here |
| A4 Owned Windows child in restricted Job Object plus parent deadline | Kernel/job rights, exact OS, handles and containment before workload starts | Job-accounted memory and owned-child lifetime; parent can abandon invalid run | Field-level preallocation rejection, proof of server rollback, perfect real-time deadlines | Accounting scope, nested-job/breakaway/handle tests, memory pressure, blocked child and parent-death tests | Platform-specific implementation and operations | Separate isolation and owned-child termination approval |
| A5 Owned Linux worker in dedicated cgroup v2 plus external deadline | Kernel/controllers/delegation/swap policy and trusted parent | Accounted group resources and isolated workload lifetime | Exact field rejection, instantaneous zero-overshoot bound, server rollback, real-time scheduling | memory.max/accounting/swap/OOM behavior, membership and escape tests, deadline/termination evidence | Platform deployment and privilege cost | Separate Linux environment and containment approval |
| A6 Bounded protocol-aware gateway or custom native transport | New trusted parser/gateway, TLS and framing boundary | Potential C-FIELD/C-NATIVE if length admission precedes buffering | Not automatically C-PROCESS/C-CALL; gateway itself can allocate/block | Independent parser/allocator audit, fragmentation/length/TLS/adversarial protocol evidence | Highest maintenance and new dependency surface | New architectural authorization required; not introduced |

These are alternatives for review, not implemented guarantees.
A1 follows [Psycopg cursor storage semantics](https://www.psycopg.org/psycopg3/docs/advanced/cursors.html).
A2 follows [libpq asynchronous command processing](https://www.postgresql.org/docs/current/libpq-async.html).
A4 relies on [Windows Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects);
A5 relies on [cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html).
The table's containment assessment is a design inference, requiring independent validation.

## Timeout, cancellation and cleanup are separate controls

PostgreSQL [statement_timeout](https://www.postgresql.org/docs/current/runtime-config-client.html)
concerns server statement duration; it is not a client memory or blocked-network deadline.
Psycopg [connection cancellation APIs](https://www.psycopg.org/psycopg3/docs/api/connections.html)
must be checked against the exact build. Cancellation alone does not establish session rollback.
A future parent must retain immutable child identity (owned handle/capability, generation,
creation identity and nonce), apply a monotonic deadline, invalidate incomplete evidence, and
record cleanup outcome. No lookup/kill by an arbitrary PID, name or matching command line.
No controller, spawn, kill, signal, job object or cgroup operation is materialized by this order.
The existing operational controller remains blocked.

After lost connection or forced child exit, local resources and server transaction state must
be evidenced separately. Unknown rollback remains unknown; do not reuse the session or publish
partial rows. Server cleanup observation requires independent read-only authority and a deadline.
No automatic destructive cleanup or killing unrelated database sessions is proposed.

## Conditional recommendation and formal contract decision

Retain A0 now. Conditional direction: evaluate A1 plus an owned isolated worker (A4 on an
approved Windows environment, or A5 on an approved Linux environment) and independent parent
deadlines. This may provide bounded failure containment rather than guaranteed successful
cleanup of every request. It does NOT satisfy C-FIELD merely by bounding process memory.
Do not adopt a platform, new gateway, dependency or supervisor from this document alone.

No currently verified option satisfies the complete existing strict transport contract.
Status: BLOCKING_EXECUTION_REVIEW. If C-FIELD is mandatory, retain it and investigate A3/A6
only under new explicit design authority and evidence. If reviewers instead want process-level
containment, they must formally revise the requirement: distinguish field rejection before
allocation from terminating an over-budget owned worker; specify accounted-memory metric,
allowed transient overshoot, maximum parent-wait tolerance, invalid-result handling and
uncertain server cleanup. That revision must not be silently represented as satisfying C-FIELD.
Until an explicit decision and proof exist, do not enable the collector or close EXEC-G1/PERS-G1.

## Connected activation and effective-role review

| Boundary | Current source/configuration | Required proof | State |
| --- | --- | --- | --- |
| Collector activation | collect enabled=False; approval collector_authorized=false; bound config and guard.admission before connection ownership | Independent verifier of artifact/config/guard; a self-reported hash is insufficient | DOCUMENTED; actual approval UNRESOLVED |
| Concrete transport | Candidate admission always raises; no raw fallback | Any replacement must be separately reviewed and prove native guarantees | BLOCKING_EXECUTION_REVIEW |
| Harness | prepare returns plan; dispatch calls concrete refusal before provider | Separate scheduler/isolation authorization | BLOCKING_EXECUTION_REVIEW |
| Observer | Dedicated direct mpt_snapshot_reader; no memberships/SET ROLE paths, no owner/super/BYPASSRLS/create/write | Effective direct/PUBLIC/transitive privileges and default grants across schemas/functions/sequences/extensions | UNRESOLVED |
| Fixture writer/admin | Separate isolated role only for approved adversarial cases; never observer privileges | Identity, rights, bounded fixture lifetime and immutable before-state | UNRESOLVED |
| Catalog/view/ACL | Existing 30-table/191-field checks, view/security digests, RLS/temp refusal | DDL and privilege quiescence for session; live catalog observations | UNRESOLVED |
| Versions and resource limits | All driver/environment digests and numerical limits unresolved | Pinned binaries, approved numbers, clock and actual enforcement evidence | UNRESOLVED |
| Injection boundary | Collector accepts an externally supplied guard; Python is not a hostile-code sandbox | Trusted caller/code integrity; reject unreviewed implementation before authorizing call | BLOCKING_EXECUTION_REVIEW |

No configuration alone proves authorization. Existing false examples and code remain unchanged.
