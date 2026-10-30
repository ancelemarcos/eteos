# DataMarket — End-to-End Delivery Roadmap

**Status:** ACCEPTED
**Scope:** Delivery path from current Research Harness implementation to initial production MVP
**Last updated:** 2026-09-14

## 1. Purpose

The research program is an instrument for building DataMarket; it is not the final product. This roadmap prevents the project from optimizing only the laboratory while leaving the production/client/compliance path implicit.

The roadmap does not promote pending provider, licensing, technology or quantitative decisions. It assigns each unresolved decision to the milestone that requires it.

## 2. Delivery tracks

Five tracks progress with explicit dependencies:

- **R — Research & scientific validation:** targets, baselines, evidence families, replication, replay equivalence.
- **D — Data/source/compliance:** target/context source qualification, provider/product capabilities, licensing and data-use rights.
- **P — Production analytical platform:** provider adapter, canonical live path, MarketState, Feature/Market/Event engines, persistence boundary.
- **C — Client/product experience:** Gateway, snapshot/incremental protocol, one initial client surface, freshness/explanation UX.
- **O — Security/operations:** auth/entitlements, observability, SLOs, capacity, recovery, DR and release operations.

Provider/licensing work may run in parallel with provider-independent research. Do not wait for RH-I9 to begin evidence collection from B3/provider commercial/legal channels.

## 3. Milestones

| Milestone | State | Primary objective | Exit evidence |
| --- | --- | --- | --- |
| DM-0 — Documentation/architecture baseline | COMPLETED | Product, requirements, ADRs, domain language, research governance and readiness gates are coherent | accepted docs + consistency validation |
| DM-1 - Provider-independent Research Laboratory | COMPLETED | Complete RH-I0..RH-I9 for the declared synthetic scope and prove deterministic evidence/replay controls | strict Maven build, laboratory controls, evidence bundles, verified scope certification |
| DM-2 - Source & Rights Qualification | PROFITDLL ROUND 1 COMPLETED / BLOCKED; qualification incomplete | Qualify the target-market source and the minimum context-source set required by declared capabilities, closing temporal, sequence, fidelity and use-specific rights questions | `DM-2-SOURCE-AND-RIGHTS-QUALIFICATION-CONTRACTS.md`, `DM-2-EXTERNAL-QUESTIONS.md`, `DM-2-PROFITDLL-EXTERNAL-QUALIFICATION-ROUND-1.md`, Anticipatory handoff, Source Qualification Register, provider evaluation/certification, Evidence Register, authoritative rights evidence and Data Usage Matrix update |
| DM-3 — WDO Empirical Characterization | BLOCKED until applicable DM-1/DM-2 gates | Preserve the milestone while sequencing DM-3A target/data characterization, DM-3B empirical baselines and DM-3C candidate evidence/replication on authorized research-certified data | target/baseline reports, preregistered experiments, replication, research decision log |
| DM-4 — Production Scaffold Freeze | OPEN | Freeze exact production JDK/build/Spring/provider adapter mode, module boundaries, bounded handoff baseline, PostgreSQL/migrations, config/secrets and CI | accepted decisions + architecture tests + benchmark/provider evidence |
| DM-5 — WDO Analytical Vertical Slice | OPEN | Run authorized live/replay WDO through Provider Adapter -> CanonicalEvent -> MarketState -> accepted Feature/Market/Event slice with explicit quality/freshness | provider certification, E2E deterministic/quality tests, replay/live equivalence for supported scope |
| DM-6 — Client Alpha & Publication Readiness | BLOCKED by rights/security decisions | Expose coherent derived intelligence through Gateway to one selected client surface with snapshot/resync, explanation and freshness semantics | auth/entitlement design, publication-rights evidence, client contract tests, UX/failure-state acceptance |
| DM-7 — Production MVP Readiness | OPEN | Satisfy MVP-001..010, applicable MUST requirements, success-metric thresholds, SLO/capacity/security/operations gates | objective coverage PASS, production readiness review, runbooks, monitoring, recovery/DR evidence |
| DM-8 — Production MVP Release | NOT STARTED | Release the initial DataMarket intelligence product for the approved scope | explicit release decision + no required BLOCKED gates |
| DM-9 — Expansion / advanced research | FUTURE | Additional instruments, client surfaces, richer models and validated anticipatory/predictive capabilities | new research/product/architecture decisions |

## 4. Current critical path

**DM-1 is completed.** RH-I0 through RH-I9 are completed, and the real `WDO_SYNTHETIC_TRADE_FIRST_PASSAGE@1.0.0` Certification Package verified offline with `CertificationVerdict=CERTIFIED`; the exact bounded result is recorded in `docs/research/RH-I9-CERTIFICATION-HANDOFF.md`.

The immutable historical V1 result remains valid. Independent audit findings AR-01..AR-06 were remediated by the independently versioned V2 certification protocol, the authorized V2 recertification is `CERTIFIED`, and portable-path closure is included in the released `research-harness-v1.0.0` tag at `d400ed9ab049aa4f7a887113b4de646bf2d1e40e`. This release does not change the CertificationScope or reopen historical DM-1 completion.

The descendant `MULTI-INSTRUMENT RESEARCH HARNESS GENERALIZATION` activity is `IMPLEMENTED / VALIDATED`. `TEST_INSTRUMENT` traverses the instrument-neutral pipeline under its own closed scope authority, Evidence V8 and Certification V3 without modifying the immutable pre-v1 candidate or transferring WDO certification. This is architectural proof only; WIN and third-instrument science remain not started and require independent materials and certification. The separate `BEFORE-FIRST-SUBMODULE` gate must be completed before the repository adopts a Git submodule.

Instrument Identity & Resolution is `IMPLEMENTED / VALIDATED / COMMITTED`. The approved Anticipatory Market Intelligence direction is now materialized in `docs/research/ANTICIPATORY-MARKET-INTELLIGENCE-CONTRACTS.md`; it is a research/product contract, not an empirical performance claim or detector authorization.

Canonical Market Ingestion & Capability is the current additive post-v1 foundation preceding Market Intelligence Runtime. Its contract and ADR-013 are materialized, and bounded executable Slice 1 is implemented and validated with synthetic sources A/B/C/D and synthetic instruments Alpha/Beta. Source D required zero neutral-core production changes and Beta required zero neutral ingestion/semantic algorithm changes. A real adapter, real dataset, DM-3A and production Market Intelligence remain gated. This checkpoint does not renumber DM-0..DM-9.

The Market Intelligence Runtime contract and ADR-014 are `MATERIALIZED / VALIDATED`, and bounded Executable Slice 1.1 is `IMPLEMENTED / VALIDATED` in `research-analytics`. It proves the provider- and instrument-neutral epistemic, temporal, evidence, analytical-state, timeline and explanation boundaries through hardened deterministic synthetic semantics, including a strong zero-neutral-core-change definition extension proof. It adds no empirical behavior, score, trading semantics, real candidate, provider or Market Data.

ADR-015 Conformance Slice 1 is `IMPLEMENTED / VALIDATED`: legitimate TARGET-only analytics executes without fake context; historical synthetic and canonical-shaped synthetic observations retain distinct identities while sharing one scientific trade view, first-passage implementation, target-blind episode path, H0 and B0. The H0 performance foundation is frozen at `h0-optimization-v1.0.0`; `docs/research/H0-REAL-MARKET-EXPERIMENTAL-PROTOCOL.md` materializes the target-blind population, complete 25-cell characterization, H0-only target selection and H0-to-H1 freeze; and `docs/research/REAL-MARKET-BASELINE-LADDER-B0-B3-CONTRACTS.md` freezes one population/pairing, PIT/correction authority and the real-market B0 prevalence, B1 session/time, B2 price/self-history and B3 price-confirmation roles. Synthetic B1-B3 Conformance Slice 1.3 now validates atomic full-`PairingKey` universes with target-blind information-atomic invalid results, cutoff-scoped future-world-non-interfering fitting identity, typed missingness, B1 session isolation, B2 causal price-state value/lineage/identity stutter invariance with separate raw provenance, and B3 no-backdating without empirical defaults. Qualified-data benchmarking, real H0, real B1-B3 configuration/parameters and H1 remain separately gated. This does not start or renumber DM-3; DM-2 qualification continues independently.

`docs/research/H1-ACTIVITY-ARRIVAL-LEAD-SCIENTIFIC-PROTOCOL.md` materializes the scientific boundary for the future H1 stage: non-directional occurrence/timing, independent predictive/change-specific/temporal claims, source-qualified arrival and deduplication, target-blind clocks and comparable detection opportunities, lead taxonomy, exact population/pairing and holdout/multiplicity. Provider-neutral Synthetic Conformance Slice 1 now validates that boundary with test-only policies and no empirical algorithm. It selects no real activity parameter and authorizes no real H1 implementation, preregistration, data use or execution.

The DM-2 process is materialized in `docs/market-data/DM-2-SOURCE-AND-RIGHTS-QUALIFICATION-CONTRACTS.md`, with official public evidence in `docs/regulatory/EVIDENCE-REGISTER.md` and recipient-routed questions in `DM-2-EXTERNAL-QUESTIONS.md`. ProfitDLL external qualification Round 1 is recorded in `docs/market-data/DM-2-PROFITDLL-EXTERNAL-QUALIFICATION-ROUND-1.md`: the candidate is `BLOCKED / NOT SELECTED` because exact product/version, critical temporal/correction/arrival/replay semantics and recipient-specific rights remain unresolved. B3 direct remains a future candidate without selection. **No provider, source, dataset, right, technical behavior or real mapping is qualified.** DM-1 completion and public evidence do not satisfy DM-2. **DM-3 remains BLOCKED** until its applicable DM-2 conditions, authorized research-certified data and separate execution authorization are available; within that milestone, the intended order remains DM-3A target/data characterization, DM-3B empirical baselines, then DM-3C candidate evidence/replication. DM-5, DM-6 and production release also remain gated.

## 5. Milestone dependency graph

The delivery sequence is not a single serial queue. Provider-independent research and external source/rights qualification progress in parallel, but later promotion gates have explicit dependencies:

```text
DM-0
 ├──> DM-1 Research Laboratory -------------------┐
 └──> DM-2 Source & Rights Qualification ---------┼──> DM-3 WDO Empirical Characterization
                                                   │
DM-2 + provider measurements + accepted scaffold decisions
                         └─────────────────────────> DM-4 Production Scaffold Freeze

DM-3 + DM-4 --------------------------------------> DM-5 WDO Analytical Vertical Slice
DM-2 publication rights + DM-5 + security --------> DM-6 Client Alpha / Publication Readiness
DM-5 + DM-6 + success metrics + SLO/ops ----------> DM-7 Production MVP Readiness
DM-7 ----------------------------------------------> DM-8 Production MVP Release
```

A milestone may perform preparatory work before all incoming dependencies are satisfied, but it cannot claim its exit state until the required evidence exists.

The current pre-DM-3 convergence is explicitly parallel:

```text
EXTERNAL: DM-2 -> source/dataset/rights -> real instrument/mapping -> qualified dataset --┐
                                                                                          +-> real H0 execution
INTERNAL: ADR-015 contract -> executable canonical port -> H0/B0-B3 contracts ----------┘
```

The H1 scientific protocol is materialized, but H1 preregistration/execution remains after real H0 target/population and B0-B3 characterization; H2, H3 and H4 remain later research stages.

## 6. Promotion boundaries

- RH-I3 completion does not authorize real Market Data or production publication.
- Research success does not authorize a provider capability or licensing right.
- Provider access does not authorize retention, model development or external display unless those rights are evidenced.
- A research feature does not enter production merely because it performs well; it must satisfy promotion requirements and operational semantics.
- A functioning endpoint/client does not satisfy the product objective unless temporal integrity, freshness, explainability, failure behavior and user-value gates are also met.

## 7. Completion relationship

`docs/product/OBJECTIVE-COMPLETION-CONTRACT.md` defines the final initial-product completion rule. `OBJECTIVE-COVERAGE-MATRIX.md` maps the objective to requirements/architecture/milestones. `READINESS-STATUS.md` is the live state.

## H1 Slice 1.1 temporal-authority closure

The provider-neutral Slice 1.1 checkpoint adds validated exact PIT world/evaluation binding, cutoff-scoped scientific identity and lineage, structurally comparable opportunity authority and monotonic material qualification to the algorithm-neutral H1 conformance surface. It selects no real activity parameter and authorizes no real H1 implementation, preregistration, data use or execution.

## H1 Slice 1.2 scientific-view and result-ancestry closure

The provider-neutral Slice 1.2 checkpoint makes H1 and B3 opportunity ancestry self-binding and non-transplantable, projects native opportunities and detection candidates to complete cutoff-scoped scientific views, and preserves full stream/timeline/ledger provenance only for audit. This closes H1-S1.1-AUD-F05..F07 without changing H0, B1-B3, PIT/corrections, empirical configuration or the independent DM-2 gate.

## H1 Slice 1.3 candidate and opportunity authority closure

The provider-neutral Slice 1.3 checkpoint closes H1-S1.2-AUD-F08..F10. A designated synthetic execution issuer now derives a complete target-blind candidate universe from every governed opportunity through T; B3 lead ancestry is established during B3 evaluation; and native-event lead arithmetic requires structural fairness over the actual H1/B3 opportunity views. It selects no empirical H1 rule and leaves real execution and DM-2 unauthorized.

## H1 Slice 1.4 governed-world authority closure

The provider-neutral Slice 1.4 checkpoint closes H1-S1.3-AUD-F11..F14 by replacing declaration-wrapping issuers with one versioned governed synthetic-world resolver. Exact `worldAt(T)` material drives the complete target-blind candidate universe; an opaque match is required for H1 row production; B3 opportunity ancestry is prebound in the governed B3 execution; and qualification, opportunity and native-fairness authority are resolver-issued. It selects no empirical H1 rule and leaves real H0/H1 execution and DM-2 unauthorized.
