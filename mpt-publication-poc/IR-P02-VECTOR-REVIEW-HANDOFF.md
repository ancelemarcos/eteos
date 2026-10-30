# IR-P02 independent vector review handoff - current order v3.2

READY_FOR_FOCUSED_INDEPENDENT_RECHECK / NOT_RUN. Review request only, not an independent
review certificate. Reviewer/signature UNRESOLVED; assessment REQUIRES_REVIEW.

## Exact primary material

Paths are relative to this candidate directory. Verify SHA-256 before review.
Earlier opinions and candidate implementation outputs are not normative proof.

| Role | File | SHA-256 |
| --- | --- | --- |
| Target and frame worksheet | IR-P02-MULTIROW-INDEPENDENT-VECTORS.md | c7e76a320284046ec06b996b3786ffbb4d1e3e9701b7d5d2728b1d681503024c |
| Proposed byte contract | FULL-SNAPSHOT-CONTRACT.md | 0327a68f911db4e5271589e63d1e7522f268242da8618863570b58c325778c5d |
| Exact schema inventory | runner/snapshot_schema.json | 1e64e5e28444b41f4e9bad62db930286810cb62c7769f243a45566d8eb47017a |
| Candidate DDL, static context | schema.sql | e1feebaf8b6cdce323fd4c7b95bdd08c2d1b0907f9d43f673e3cfd1933f6542a |

## Bounded review questions

Use the target's v3.2 adversarials and negative-maturity table, v3.0 worksheet and original expansions.
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
