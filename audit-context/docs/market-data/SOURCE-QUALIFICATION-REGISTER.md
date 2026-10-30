# DataMarket — Source Qualification Register

**Status:** ACCEPTED / LIVING INDEX  
**Scope:** Data-source slots required by the initial DataMarket product path  
**Last updated:** 2026-09-14

## 1. Purpose

This register prevents the project from treating “a provider exists” as equivalent to having the sources, fidelity, rights and certification required by the product objective.

A source is production-qualified only when its technical capabilities, temporal semantics, recovery behavior, licensing evidence and certification status are sufficient for the released capability that depends on it.

`DM-2-SOURCE-AND-RIGHTS-QUALIFICATION-CONTRACTS.md` is the principal DM-2 process authority. It defines independent qualification dimensions, evidence classes, purpose-specific verdicts and the DM-3A/anticipatory/live gates. `ANTICIPATORY-INTELLIGENCE-DM-2-HANDOFF.md` is its capability-driven input. This register records evolving source-slot outcomes; neither document selects or qualifies a provider.

## 2. Qualification dimensions

For each source slot record:

- stable source-slot ID and analytical role;
- exact provider/product/dataset once selected;
- `decisionStatus` and blockers;
- instruments/domains supplied;
- supported fidelity (`TRADE`, `TOB`, `MBP`, `MBO`, macro/event/news fields as applicable);
- timestamp/sequence/provenance semantics;
- snapshot/gap/recovery behavior;
- representative event/burst measurements when relevant;
- regulatory/licensing evidence references;
- provider certification evidence;
- delivery milestones that require the source.

Provider capability, exact-dataset fit, technical validation, licensing right, live equivalence and scientific-use authorization are independent dimensions. Passing one never implies another, and they need not progress in one fixed order.

## 3. Initial source slots

| Source slot | Analytical role | Selection state | Blockers | Minimum purpose | Required by |
| --- | --- | --- | --- | --- | --- |
| `SRC-B3-TARGET-PRIMARY` | Authoritative target-market source | PENDING | PROVIDER, B3, LICENSING | WDO target-market trades plus only the book fidelity truthfully supported/authorized by the selected vertical slice | DM-2, DM-4, DM-5, DM-7 |
| `SRC-CONTEXT-MARKET-01` | Cross-market confirmation/divergence context | PENDING | PROVIDER, LICENSING, RESEARCH | At least one analytically relevant authorized context-market source for the released MVP scope; it may be supplied by the same provider if rights/capabilities permit | DM-2, DM-3, DM-5, DM-7 |
| `SRC-SCHEDULED-CONTEXT-01` | Scheduled macro/event context | PENDING | PROVIDER, LICENSING, RESEARCH | Point-in-time event/calendar context when included in the released scope | DM-2/DM-3 when selected; DM-6 if published |
| `SRC-NEWS-CONTEXT-01` | Optional news/context enrichment | PENDING | PROVIDER, LICENSING, RESEARCH | Non-authoritative contextual enrichment only; not required for deterministic hot-path detection | Future/selected scope only |

`SRC-CONTEXT-MARKET-01` is a product role, not a commitment to an international vendor. It can be satisfied by any authorized analytically relevant market source that supports the released cross-market claim.

### Public-evidence and external-qualification candidate state

Public evidence retrieved through 2026-09-14 is indexed in `../regulatory/EVIDENCE-REGISTER.md`. The first recipient-filtered ProfitDLL external-qualification round is recorded in `DM-2-PROFITDLL-EXTERNAL-QUALIFICATION-ROUND-1.md`. It narrows the exact questions but does not promote `SRC-B3-TARGET-PRIMARY` or create a selected source:

| Candidate | Current verdict | Relevant evidence | Qualification still missing |
| --- | --- | --- | --- |
| Nelogica / ProfitDLL | `EXTERNAL QUALIFICATION ROUND 1 COMPLETED` / `BLOCKED` / `NOT SELECTED` | `DM-2-PROFITDLL-EXTERNAL-QUALIFICATION-ROUND-1.md`, `PUB-B3-DIST-001`, `PUB-NELO-PROD-001`, `PUB-NELO-TECH-001`, `PUB-NELO-HIST-001`, `PUB-NELO-BOOK-001`, `PUB-NELO-VERSION-001`, `PUB-NELO-RUNTIME-002`, `PUB-NELO-ACCESS-002`, `PUB-NELO-INSTRUMENT-002`, `PUB-NELO-RIGHTS-001` | exact commercial SKU/entitlement/package/build/interface, concrete listed-WDO mapping, `availableAt`, ordering/corrections/gaps/batching/replay semantics, contractual rights, authorized probe evidence and scientific fit |
| B3 direct | `CONTINUE AS FUTURE CANDIDATE` / `NOT SELECTED` | `PUB-B3-WDO-001`, `PUB-B3-WDO-002`, `PUB-B3-UMDF-001`, `PUB-B3-MR-001`, `PUB-B3-TS-001`, `PUB-B3-FIX-001`, `PUB-B3-HIST-001`, `PUB-B3-RIGHTS-001`, `PUB-B3-RIGHTS-002` | exact direct product/dataset/access/entitlement, technical behavior, rights, operational fit and scientific fit |

The first target-source slot remains `PENDING [PROVIDER,B3,LICENSING]`. The ProfitDLL candidate additionally requires recipient-specific contractual confirmation and, if later authorized and lawfully enabled, a bounded technical probe. Context-market, scheduled-context and news-context slots were not evaluated in this round.

## 4. Promotion rule

A source slot moves from `PENDING` toward production qualification only when all applicable evidence exists:

```text
exact product/dataset selected
+ capability record complete
+ temporal/sequence/recovery behavior characterized
+ required usage rights CONFIRMED
+ representative certification tests passed
+ dependent analytical scope accepts the source quality
= qualified for the named release scope
```

Qualification is scope-specific. A provider certified for trades is not automatically certified for MBP/MBO; a source authorized for server-side non-display processing is not automatically authorized for client display.

For historical TRADE-only characterization, a defensible coverage/gap model is mandatory, but book snapshot/recovery and live reconnect mechanisms are not gates unless the declared purpose consumes book or live data.

## 5. Relationship to the product objective

The initial MVP must not reach `DM-7 — Production MVP Readiness` with a mandatory analytical capability depending on an unqualified source slot. Optional sources may remain pending only when the released product scope and requirements explicitly permit their absence.
