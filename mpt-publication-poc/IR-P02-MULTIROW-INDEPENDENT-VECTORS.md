# IR-P02 manual multirow vectors - order v2.9 / candidate0.26

## Order v3.0 - static recheck, worksheet and validity classification

READY_FOR_INDEPENDENT_VECTOR_REVIEW / NOT_RUN. Author-side recheck, not authenticated
independent review. No demonstrated frame/byte discrepancy found against current primary
contract/schema. No codec/oracle/emitter output used. Full-stream semantics remain PROPOSED.
Input vector291495390ffff92224b36997dd94caae5f1f5c3a038518af29f713e3e0dd51a3.
Input manifest8394e0b73f1dae47749ec393290414f90b5c340c3bfd3e5e56b47def4e42af11.
See [primary-source handoff](IR-P02-VECTOR-REVIEW-HANDOFF.md) for exact hashes and questions.

### Every case classified

| Case / constituent rows | Classification |
| --- | --- |
| P0 | WIRE_ONLY_SYNTHETIC |
| B0 | WIRE_ONLY_SYNTHETIC |
| A0-vector | WIRE_ONLY_SYNTHETIC |
| C0-vector | WIRE_ONLY_SYNTHETIC |
| P2 / PA,PB | WIRE_ONLY_SYNTHETIC |
| B2 / BD,BE | WIRE_ONLY_SYNTHETIC |
| A2 / AA,AB | WIRE_ONLY_SYNTHETIC |
| C2-vector / CC,CE | WIRE_ONLY_SYNTHETIC |
| Four empty streams combined | WIRE_ONLY_SYNTHETIC |
| Four two-row streams combined | WIRE_ONLY_SYNTHETIC |
| Mixed P0,B2,A0-vector,C0-vector | WIRE_ONLY_SYNTHETIC |
| Every input permutation and negative mutation | WIRE_ONLY_SYNTHETIC |

No case is RELATIONALLY_VALID. No SQL/FK/enum/fingerprint/publication-transition/MVCC
conformance is asserted, even for empty cases. No actual database state is represented.
MPT snapshot structure does not prove MIR temporal admissibility (availableAt <= decisionTime).

### Frame worksheet

Offsets are zero-based, inclusive, local to one stream. Sort keys are not serialized rows.
Only the r endpoint differs between empty and two-row variants.

| Table | v | t | s | c | Empty r | Two-row r | Discrepancy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| public_projection | 0..22 | 23..56 | 57..233 | 234..243 | 244..252 | 244..329 | None found |
| publication_barrier | 0..22 | 23..58 | 59..186 | 187..196 | 197..205 | 197..263 | None found |
| publication_batch | 0..22 | 23..56 | 57..595 | 596..605 | 606..614 | 606..848 | None found |
| publication_cut | 0..22 | 23..54 | 55..416 | 417..426 | 427..435 | 427..593 | None found |

| Table | G sum | F(p) payload/total | s payload decimal/hex | F(p) offsets within s | Nullable fields |
| --- | --- | --- | --- | --- | --- |
| public_projection | 139 | 20/29 | 168/a8 | 148..176 | position_version,plan_version |
| publication_barrier | 92 | 18/27 | 119/77 | 101..127 | None |
| publication_batch | 484 | 37/46 | 530/0212 | 493..538 | ordinal,failure_reason |
| publication_cut | 329 | 15/24 | 353/0161 | 338..361 | None |

All field names, declared order, text/bigint/boolean/xid8 types and nullable flags match
the primary schema. PKs respectively: position_id; domain_id; (position_id,batch_id); cut_id.
Descriptor c/t/b/p and enclosing s, scalars T/I/N/B/X and table v/t/s/c/r tags match contract.

| Rows | Payloads | Row totals | Container payload/hex/total | Framed key order |
| --- | --- | --- | --- | --- |
| PA,PB | 29,30 | 38,39 | 77/4d/86 | A(41) before B(42) |
| BD,BE | 20,20 | 29,29 | 58/3a/67 | D(44) before E(45) |
| AA,AB | 108,108 | 117,117 | 234/ea/243 | First A equal; second A before B |
| CC,CE | 70,70 | 79,79 | 158/9e/167 | C(43) before E(45) |

All compared keys have equal length within each case, so the shown first differing payload
byte decides order after equal framed headers. Qualified UTF-8 stream order is projection,
barrier,batch,cut. Empty253+206+615+436=1510; row contributions77+58+234+158=527;
1510+527=2037 agrees with330+264+849+594. No arithmetic was adjusted to force agreement.
No mismatch offset or changed expected byte is reported because no such defect was found.
Editorial table repair only: + denotes raw concatenation in empty-case expression cells,
avoiding unescaped Markdown pipes; it changes no specified wire bytes.

### Negative-oracle recheck and evidence boundaries

AA/AA duplicates the entire composite PK; AA/AB merely shares its first component.
C0 with two row frames contradicts cardinality. Missing, duplicate and extra streams violate
the exact inventory. The extra-table example is an inventory mutation, not a derived fifth
table vector; an individually valid extra stream would still be rejected by inventory.
Swapping serialized table order or PA/PB row order rejects, whereas permuting supplied input
rows is admitted with canonical output. Descriptor rejection requires the bound schema,
not merely valid generic framing; nullable-flag drift rejects even for nonnull rows.
@2 is only an incompatible-version negative, not a version selection. Removing the final
byte violates payload length. Rows-only lacks version/name/schema/count/container structure.
These conclusions cover every listed negative as a documentary criterion, not observed
implementation rejection. No execution or relational fixture was produced.

Conclusion: no demonstrated descriptor/frame/length/order defect. Reused hypothesis:
the proposed v2.8 full-stream interpretation. Missing evidence: authenticated independent
review, observed negative outcomes, relational/MVCC/deployed-DDL proof and historical @1 use.
Equal-length ASCII keys do not cover all adversarial length-prefix or Unicode ordering.
Compatibility stays UNRESOLVED, @2 unselected, independent adoption REQUIRES_REVIEW.
IR-P03 unchanged: lifecycle, conditional static proof and eight negatives NOT_RUN.
File hash integrity is not functional conformance.


READY_FOR_INDEPENDENT_VECTOR_REVIEW / NOT_RUN. PROPOSED; review REQUIRES_REVIEW.
Independent textual derivation from FULL-SNAPSHOT-CONTRACT canonical byte algorithm and
runner/snapshot_schema.json, not from encoder/oracle/emitter outputs. The full-stream
interpretation is inherited from the PROPOSED v2.8 contract, not independently approved here.
No human independence, signature, execution, digest or frozen expected value is claimed.
Input manifest: adc65884b5514fa45a025dd4fae7a0ecc9fc3385848ebdaf39a3a3f03ee35ae9.
Source contract SHA256: a6581f905501f73614ae4344bb40f100bfed654abfa2850b52f89fa788a75d10.
Source schema SHA256: 1e64e5e28444b41f4e9bad62db930286810cb62c7769f243a45566d8eb47017a.

## Exact byte notation (not executable code)

U("literal") denotes exactly the UTF-8 bytes between quotes; no quotes, BOM, separators or
newlines enter the bytes. Every literal in these vectors is ASCII. This factored notation
specifies every byte without a repetitive monolithic hex dump; no payload is an ellipsis.
Concatenation is ||. Empty denotes zero bytes. F(tag,P)=tag byte || u64be(length(P)) || P.
The eight-byte length is unsigned big-endian. All displayed hex pairs are bytes.
ASCII dictionary, sufficient to expand every literal below by hand:

| Characters in order | Hex bytes in the same order |
| --- | --- |
| abcdefghijklmnopqrstuvwxyz | 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 78 79 7a |
| ABCDEFGHIJKLMNOPQRSTUVWXYZ | 41 42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f 50 51 52 53 54 55 56 57 58 59 5a |
| 0123456789 | 30 31 32 33 34 35 36 37 38 39 |
| . - @ _ | 2e 2d 40 5f |

Frames: text T=54, integer I=49, xid8 X=58, boolean B=42, SQL NULL N=4e;
version v=76, table/type t=74, schema s=73, column/count c=63, nullable b=62,
PK descriptor p=70, sort key k=6b, row/container r=72.
T(A)=54 0000000000000001 41; T(B) substitutes42; T(C)43; T(D)44; T(E)45;
T(F)46; T(I)49; T(O)4f; T(S)53; T(V)56. Each is10 bytes, payload1.
I(0)=49 0000000000000001 30; I(1) ends31; I(2)32; I(3)33: each10 bytes.
X(1)=58 0000000000000001 31; X(2) ends32: each10 bytes.
B(false)=42 0000000000000001 30:10 bytes. N=4e 0000000000000000:9 bytes.
SQL NULL is not the text "NULL". No value normalization or scalar type inference is allowed.

V=F(v,U("MPT-SNAPSHOT@1"))=76 000000000000000e
4d50542d534e415053484f544031 (14 payload,23 total).
C0=63 0000000000000001 30; C2=63 0000000000000001 32 (1 payload,10 total).
R0=72 0000000000000000 (0 payload,9 total).

## Descriptors, field by field

For each ordered row in the following tables, G(name,type,q)=F(c,U(name)) || F(t,U(type))
|| F(b,U(q)). q is ASCII0 for NOT nullable and ASCII1 for nullable; F(b) always10 bytes.
The name/type literals and the ASCII dictionary above specify their exact UTF-8 payloads.
Lengths below show payload -> frame; each frame independently includes its own9-byte header.

| public_projection column | Name bytes -> F(c) | Type bytes -> F(t) | q | G bytes |
| --- | --- | --- | --- | --- |
| position_id | 11 ->20 | text:4 ->13 | 0 | 43 |
| position_version | 16 ->25 | bigint:6 ->15 | 1 | 50 |
| plan_version | 12 ->21 | bigint:6 ->15 | 1 | 46 |

PKp=F(p,F(c,U("position_id")))=70 0000000000000014 || 63 000000000000000b
|| U("position_id"):20 payload,29 total. G sum139; schema payload139+29=168.
Sp=73 00000000000000a8 || G(position_id,text,0) || G(position_version,bigint,1)
|| G(plan_version,bigint,1) || PKp:177 total.

| publication_barrier column | Name bytes -> F(c) | Type bytes -> F(t) | q | G bytes |
| --- | --- | --- | --- | --- |
| domain_id | 9 ->18 | text:4 ->13 | 0 | 41 |
| committed_ordinal | 17 ->26 | bigint:6 ->15 | 0 | 51 |

PKb=70 0000000000000012 || 63 0000000000000009 || U("domain_id"):
18 payload,27 total. G sum92; schema payload92+27=119.
Sb=73 0000000000000077 || G(domain_id,text,0) || G(committed_ordinal,bigint,0)
|| PKb:128 total.

| publication_batch column | Name bytes -> F(c) | Type bytes -> F(t) | q | G bytes |
| --- | --- | --- | --- | --- |
| position_id | 11 ->20 | text:4 ->13 | 0 | 43 |
| batch_id | 8 ->17 | text:4 ->13 | 0 | 40 |
| domain_id | 9 ->18 | text:4 ->13 | 0 | 41 |
| origin_type | 11 ->20 | text:4 ->13 | 0 | 43 |
| origin_id | 9 ->18 | text:4 ->13 | 0 | 41 |
| fingerprint | 11 ->20 | text:4 ->13 | 0 | 43 |
| publication_status | 18 ->27 | text:4 ->13 | 0 | 50 |
| ordinal | 7 ->16 | bigint:6 ->15 | 1 | 41 |
| failure_reason | 14 ->23 | text:4 ->13 | 1 | 46 |
| content_frozen | 14 ->23 | boolean:7 ->16 | 0 | 49 |
| state_version | 13 ->22 | bigint:6 ->15 | 0 | 47 |

PKa=70 0000000000000025 || 63 000000000000000b || U("position_id")
|| 63 0000000000000008 || U("batch_id"):37 payload,46 total.
G sum43+40+41+43+41+43+50+41+46+49+47=484; schema payload484+46=530.
Sa=73 0000000000000212 || the eleven G frames in the exact table order || PKa:
539 total. This reference means all eleven fully specified groups above, not omitted bytes.

| publication_cut column | Name bytes -> F(c) | Type bytes -> F(t) | q | G bytes |
| --- | --- | --- | --- | --- |
| cut_id | 6 ->15 | text:4 ->13 | 0 | 38 |
| domain_id | 9 ->18 | text:4 ->13 | 0 | 41 |
| ordinal | 7 ->16 | bigint:6 ->15 | 0 | 41 |
| resolution_policy_version | 25 ->34 | text:4 ->13 | 0 | 57 |
| frontier_position_id | 20 ->29 | text:4 ->13 | 0 | 52 |
| frontier_batch_id | 17 ->26 | text:4 ->13 | 0 | 49 |
| capture_transaction | 19 ->28 | xid8:4 ->13 | 0 | 51 |

PKc=70 000000000000000f || 63 0000000000000006 || U("cut_id"):
15 payload,24 total. G sum38+41+41+57+52+49+51=329; payload329+24=353.
Sc=73 0000000000000161 || the seven G frames in the exact table order || PKc:
362 total. Every G expands using the explicit name/type/q row above.

## Four empty cases

Names: Np=74 0000000000000019 || U("mpt_poc.public_projection"):25+9=34;
Nb=74 000000000000001b || U("mpt_poc.publication_barrier"):27+9=36;
Na=74 0000000000000019 || U("mpt_poc.publication_batch"):25+9=34;
Nc=74 0000000000000017 || U("mpt_poc.publication_cut"):23+9=32.
Every empty case has zero rows and uses its complete unchanged descriptor and PK frame.

| Case | Exact stream expression | Length derivation |
| --- | --- | --- |
| P0 | V + Np + Sp + C0 + R0 | 23+34+177+10+9=253 |
| B0 | V + Nb + Sb + C0 + R0 | 23+36+128+10+9=206 |
| A0-vector | V + Na + Sa + C0 + R0 | 23+34+539+10+9=615 |
| C0-vector | V + Nc + Sc + C0 + R0 | 23+32+362+10+9=436 |

The label A0-vector is only a local example, not the A0 fail-closed gate.
Empty metadata=P0||B0||A0-vector||C0-vector,253+206+615+436=1510 bytes.

## Four two-row cases (synthetic wire ONLY)

These deliberately short literal values are invented wire examples, NOT observed database
values or relationally valid fixtures. In particular batch O/S violate enum constraints,
fingerprint F violates its format; referenced domain/position/event relations are not supplied.
capture_transaction X(1)/X(2) are illustrative unsigned scalars, not observed transaction IDs.
No SQL acceptance or publication transition is inferred from wire structural validity.

### P2 - public_projection

| Field in order | Row PA scalar | Row PB scalar |
| --- | --- | --- |
| position_id | T(A):payload1,total10 | T(B):payload1,total10 |
| position_version | I(1):1,10 | I(2):1,10 |
| plan_version | N:0,9 | I(3):1,10 |

PA=72 000000000000001d || T(A)||I(1)||N:payload29,total38.
PB=72 000000000000001e || T(B)||I(2)||I(3):payload30,total39.
Keys: KPA=6b 000000000000000a || T(A), KPB substitutes T(B); both19 bytes.
Equal headers and text lengths;41<42 implies PA before PB. Keys are sort aids, not row bytes.
RP=72 000000000000004d || PA||PB:payload38+39=77,total86.
P2=V||Np||Sp||C2||RP:23+34+177+10+86=330 bytes.

### B2 - publication_barrier

| Field in order | Row BD scalar | Row BE scalar |
| --- | --- | --- |
| domain_id | T(D):1,10 | T(E):1,10 |
| committed_ordinal | I(0):1,10 | I(1):1,10 |

BD=72 0000000000000014 || T(D)||I(0); BE substitutes T(E)||I(1).
Each payload20,total29. Keys=6b 000000000000000a || T(D) or T(E),19 bytes;
44<45 orders BD before BE. RB=72 000000000000003a || BD||BE:payload58,total67.
B2=V||Nb||Sb||C2||RB:23+36+128+10+67=264 bytes.

### A2 - publication_batch, composite PK

| Field in order | Row AA scalar | Row AB scalar |
| --- | --- | --- |
| position_id | T(A):1,10 | T(A):1,10 |
| batch_id | T(A):1,10 | T(B):1,10 |
| domain_id | T(D):1,10 | T(D):1,10 |
| origin_type | T(O):1,10 | T(O):1,10 |
| origin_id | T(I):1,10 | T(I):1,10 |
| fingerprint | T(F):1,10 | T(F):1,10 |
| publication_status | T(S):1,10 | T(S):1,10 |
| ordinal | N:0,9 | N:0,9 |
| failure_reason | N:0,9 | N:0,9 |
| content_frozen | B(false):1,10 | B(false):1,10 |
| state_version | I(0):1,10 | I(0):1,10 |

AA=72 000000000000006c || T(A)||T(A)||T(D)||T(O)||T(I)||T(F)||T(S)
||N||N||B(false)||I(0). AB substitutes only the second scalar with T(B).
Each row payload7*10+9+9+10+10=108,total117.
KAA=6b 0000000000000014 || T(A)||T(A);
KAB=6b 0000000000000014 || T(A)||T(B):payload20,total29.
First key component equal; second41<42 => AA before AB. Same position is NOT duplicate PK.
RA=72 00000000000000ea || AA||AB:payload234,total243.
A2=V||Na||Sa||C2||RA:23+34+539+10+243=849 bytes.

### C2-vector - publication_cut

| Field in order | Row CC scalar | Row CE scalar |
| --- | --- | --- |
| cut_id | T(C):1,10 | T(E):1,10 |
| domain_id | T(D):1,10 | T(D):1,10 |
| ordinal | I(1):1,10 | I(2):1,10 |
| resolution_policy_version | T(V):1,10 | T(V):1,10 |
| frontier_position_id | T(A):1,10 | T(A):1,10 |
| frontier_batch_id | T(A):1,10 | T(B):1,10 |
| capture_transaction | X(1):1,10 | X(2):1,10 |

CC=72 0000000000000046 || T(C)||T(D)||I(1)||T(V)||T(A)||T(A)||X(1).
CE=72 0000000000000046 || T(E)||T(D)||I(2)||T(V)||T(A)||T(B)||X(2).
Each payload70,total79. Keys=6b 000000000000000a || T(C) or T(E),19 bytes;
43<45 orders CC before CE. RC=72 000000000000009e || CC||CE:payload158,total167.
C2-vector=V||Nc||Sc||C2||RC:23+32+362+10+167=594 bytes.
Combined two-row metadata=P2||B2||A2||C2-vector:330+264+849+594=2037 bytes.
This is a new manual illustrative expression, not a populated slot in the428-slot template.

## Documentary oracles for later independent review

All outcomes below are expected by the proposed contract, never observed test outcomes.
Positive: for each two-row input, [second,first] and [first,second] encode the same exact
stream expressions above. Each empty input encodes its corresponding full empty stream.
Combining all four uses projection,barrier,batch,cut order; no metadata-level wrapper.
Mixed case P0||B2||A0-vector||C0-vector has253+264+615+436=1568 bytes.

| Negative mutation (one per case) | Documentary expected disposition |
| --- | --- |
| Duplicate the first row replacing second, including AA/AA for composite PK | Reject duplicate framed PK, even if non-PK fields differ |
| Replace C2 count with C0 without changing row container | Reject count/row cardinality mismatch |
| Omit B2 from combined metadata | Reject missing required stream |
| Append a second B2 | Reject duplicated stream / inventory mismatch |
| Append F(v,..) stream for mpt_poc.publication_domain | Reject extra table, even if individually valid |
| Swap P2 and B2 in serialized bytes | Reject qualified-name order; input row permutation is a different positive case |
| Serialize PB||PA instead of PA||PB with same count | Reject descending framed-PK wire order |
| Flip projection position_version nullable flag ASCII1 to0 in Sp, leaving name/type unchanged | Reject descriptor mismatch against bound schema, even with all nonnull row values |
| Change declared type/name/PK order in Sa while maintaining valid frame lengths | Reject descriptor mismatch; never accept an alternative schema implicitly |
| Replace version payload @1 with @2 (same length) | Reject incompatible version under selected @1 recipe; not approval of @2 |
| Remove final byte of C2-vector without adjusting headers | Reject truncated payload; never silently discard row |
| Keep only PA||PB||BD||BE||AA||AB||CC||CE | Reject rows-only metadata; lacks version/name/schema/count/containers |

Byte expansion and arithmetic above are complete in factored form; none uses generated wire.
Independent reviewer must check every ASCII literal/header/sum/ordering against original
sources. Review authenticity and semantic adoption remain REQUIRES_REVIEW. Digests are
intentionally not calculated; real DB validity, deployed constraints and external historical
compatibility remain outside these vectors. DCR/ICR assignments are UNRESOLVED; no signature.
