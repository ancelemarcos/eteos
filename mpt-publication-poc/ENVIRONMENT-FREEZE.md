# Verifiable environment freeze checklist - candidate 0.8

CANDIDATE_EDIT_ONLY / NOT_RUN. No preflight, collector or experimental command was executed.
Every observed/approved value below remains UNRESOLVED until independently evidenced.
MPT-POC-0.7 identifies this candidate policy, not an approval.

| Required item | Approved config / evidence | Future observation and fail-closed check | Current status |
| --- | --- | --- | --- |
| Actual HEAD and package bytes | git_head, manifest_sha256, external config hash | rev-parse; manifest table SHA-256 and exact inventory | HEAD/file hashes inspected only; runtime approval UNRESOLVED |
| PostgreSQL exact patch and parameters | server_settings | actual current_setting values; exact match; READ COMMITTED | UNRESOLVED |
| Image/digest/container/architecture | image_digest, container_id, architecture | signed raw inspect chain and actual pg_control_system identity | UNRESOLVED |
| Python/driver/verifier and installed dependencies | python_version, driver_version, cryptography_version, installed_dependencies_sha256 | platform, psycopg, cryptography and complete installed metadata inventory | UNRESOLVED |
| Extensions | extensions | pg_extension exact inventory | UNRESOLVED |
| Runtime roles/grants/inheritance/ownership/functions | privilege_inventory_sha256 per role | memberships/flags, effective column/function privileges and owner/control capabilities | UNRESOLVED |
| Controller identity and permissions | freeze.controller_identity / controller_permissions_sha256 | independently reviewed signed freeze record; actual DB controller capabilities also in role inventory | UNRESOLVED |
| Process isolation | freeze.process_isolation_identity / process_isolation_evidence_sha256 | signed external measurements under separately trusted collector; no local supervisor validation implemented | UNRESOLVED |
| Supervisor capability/target policy | freeze.supervisor_policy_sha256 | independently reviewed policy forbidding arbitrary PID/host-service/server targets | UNRESOLVED |
| Collector identity and credentials | collector_identity; freeze.collector_authorization_sha256 | signed identity and independently approved authorization evidence; credentials never logged | UNRESOLVED |
| Public verification key and signature | attestation_public_key_sha256, attestation_signature_sha256, attestation_sha256 | exact hashes, raw Ed25519 key/signature verification on JSON bytes | UNRESOLVED |
| Signature policy | freeze.signature_policy_identity | must be ED25519-RAW-JSON-V1; no alternative inferred | UNRESOLVED |
| Capture freshness | attestation_captured_at_utc, max_age_seconds, clock_skew_seconds | signed timestamp, approved positive max age, bounded skew, current UTC age | UNRESOLVED |
| Clock measurement/trust | freeze.clock_evidence_sha256 | independently reviewed signed clock evidence; local clock accuracy is not self-proved | UNRESOLVED |
| Independent approval | freeze.approval_identity and separately supplied config SHA-256 | approved config digest checked first; all freeze keys must resolve and equal signed record | UNRESOLVED |

All fields in freeze must be nonempty/non-UNRESOLVED; evidence hashes must be lowercase SHA-256.
Missing, malformed, mismatched, expired or unauthorized evidence blocks before fixtures.
No config flag can enable blocked stub scenarios. This checklist does not create authority.

The signed freeze object binds the above identities/evidence hashes, not the private evidence
contents. Independent reviewers must inspect those referenced documents/measurements and trust
the signer/collector before approving the config. A valid signature does not itself prove OS
isolation, privilege minimization, clock accuracy or an honest collector. Those remain prerequisites.
There is no implemented process supervisor; neither signed values nor hash approval enables it.

Future JSONL starts NOT_RUN, records scenario, manifest/config hashes, actual HEAD and artifact
inventory, versions/settings/extensions, role observations, signature/collector identity,
capture age and signed controller/isolation freeze record before initial fixture mutation.
A refusal before completed preflight has no claim of verified provenance. Secrets/DSNs/private
keys are never logged. Store config, attestations and evidence outside the candidate package.
Separate read-only independent collection and approval are prerequisites, not self-approval by
copying a failed runner output. EXEC-G1/PERS-G1 OPEN; no test result or performance claim.


## Approval ownership and evidence classification (order v0.5)

Roles below are required accountable reviewers, not appointed people or granted permissions.
Actual identities/signatures remain UNRESOLVED. One runner-produced declaration is not approval.

| Area | Evidence producer | Required independent approver | Evidence to retain |
| --- | --- | --- | --- |
| PostgreSQL exact build/image digest/extensions/settings | Lab operator + trusted collector | Database/runtime reviewer | Server version/build output, signed raw image/container inspections, extension/config inventory |
| OS, sandbox and child capability model | Isolation operator/collector | Security + lab supervisor reviewer | Exact OS build, namespace/job boundary, target capability restrictions, privilege observations |
| Python/driver/dependency lock | Build/runtime collector | Reproducibility reviewer | Complete installed versions/hash versus approved lock; executable/build identity |
| Roles, inheritance, grants, owners, SECURITY DEFINER | DB permission collector | Database security reviewer | Effective runtime/login inventories and controller-specific rights |
| Supervisor/IPC/timeouts/secret handoff | Controller designer | Security and experiment owner | H01-CTRL@1 acceptance mapping, capability/IPC contract, bounded deadlines |
| Collector identity/key/authorization/signature policy | Independent evidence custodian | Evidence trust owner | Key fingerprint, signer authorization, signed record, non-secret credential policy evidence |
| Freshness/clock tolerance | Clock/collector operator | Time-integrity reviewer | Measured clock evidence, chosen max age/skew and rationale |
| Snapshot canonicalization/reference vectors | Independent encoder/reference author | Evidence-contract reviewer | MPT-SNAPSHOT@1 implementation review and independent vectors, schema inventory |
| Member seam | Architecture/lab designer | Architecture decision owner + DB reviewer | Accepted complementary decision ID, equivalence/lock/grant review |
| Final execution authorization | Experiment owner | Explicit human task authorization | Exact scenario/environment/config/manifest scope and approved evidence chain |

DECLARED = a proposed or supplied value without independent measurement. OBSERVED = value
actually collected with provenance, no approval implied. APPROVED = named independent reviewer
accepted exact evidence/config identity. UNRESOLVED = any required link missing. These are
review classifications, not new persisted application states. No field becomes APPROVED because
it matches a self-authored example. Only checkout HEAD/file hashes were observed this round;
all runtime/version/build/OS/digest/identity/permission/freshness values remain UNRESOLVED.

## Static preflight ordering assessment (not executed)

run.py rejects blocked scenarios and false/unresolved authorization before setup. verify_files
checks independently supplied config hash and verify_freeze before DB connections. Signature,
expiry and external binding are checked next. setup then opens runtime sessions solely for
identity/SET ROLE/session settings/SELECT observations and validates all initial roles before
F0/F1 or any application mutation. Database-only observations cannot be obtained with zero
connections: those are preflight connections, not mutating fixture connections. Missing role/
server approval is detected there and closes sessions without fixtures. No mutating scenario
must start before completion of those checks; signed declarations alone are insufficient.

This confirms source ordering only, not tested fail-closed behavior. Exact OS/build/isolation
measurements are externally approved signed evidence references, not independently remeasured
by the Python helper. Actual process supervisor validation is absent; blocked scenarios remain
unconditionally disabled even with resolved fields. Runtime stays at policy/implementation
version 0.7 in this documentation-only 0.8 package; no configuration was promoted or enabled.
