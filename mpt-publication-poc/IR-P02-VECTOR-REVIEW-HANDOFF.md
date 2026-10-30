# IR-P02 independent vector review handoff - order v3.0

READY_FOR_INDEPENDENT_VECTOR_REVIEW / NOT_RUN. Review request only, not an independent
review certificate. Reviewer/signature UNRESOLVED; assessment REQUIRES_REVIEW.

## Exact primary material

Paths are relative to this candidate directory. Verify SHA-256 before review.
Earlier opinions and candidate implementation outputs are not normative proof.

| Role | File | SHA-256 |
| --- | --- | --- |
| Target and frame worksheet | IR-P02-MULTIROW-INDEPENDENT-VECTORS.md | 3526aa1093d9eb95cc33c0d9bdcc6a16b3542c675f0ceb95c1d79146f758287d |
| Proposed byte contract | FULL-SNAPSHOT-CONTRACT.md | a6581f905501f73614ae4344bb40f100bfed654abfa2850b52f89fa788a75d10 |
| Exact schema inventory | runner/snapshot_schema.json | 1e64e5e28444b41f4e9bad62db930286810cb62c7769f243a45566d8eb47017a |
| Candidate DDL, static context | schema.sql | e1feebaf8b6cdce323fd4c7b95bdd08c2d1b0907f9d43f673e3cfd1933f6542a |

## Bounded review questions

Use the target's v3.0 offset/descriptor/row worksheet and original field expansions.
Independently expand ASCII literals, F(p) frames, nullable/type fields, scalar/count/row
frames and framed-PK order. Check1510/2037 both by stream sums and527 added row bytes.
Return exact frame/offset/stated-versus-expected bytes for any discrepancy, or a bounded
no-discrepancy finding. The author-side recheck must not replace your independent derivation.
Check every negative, especially composite-PK duplicates versus a shared first component
and permuted input versus descending serialized wire.

All cases WIRE_ONLY_SYNTHETIC; none RELATIONALLY_VALID. No SQL/FK/enum/fingerprint/
publication/MVCC or MIR availableAt conformance follows. Open: authenticated reviewer,
historical approved/consumed @1 semantics, coverage beyond equal-length ASCII keys and
observed rejection behavior. Compatibility UNRESOLVED; no automatic @2.
No Python/SQL/tests/runner/database/capsule or428-slot generation/freeze/comparison is
authorized. Do not promote gates or treat hashes as functional validation.
