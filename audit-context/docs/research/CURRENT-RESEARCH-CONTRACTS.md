# DataMarket — Current Research Contracts

**Status:** CURRENT / IMPLEMENTATION AUTHORITY
**Scope:** released Research Harness v1.0.0; completed post-v1 multi-instrument, canonical instrument-identity, bounded synthetic Canonical Market Ingestion & Capability, Market Intelligence Runtime Slice-1.1, real-market single-instrument Conformance Slice 1 foundations and H0 Optimization Conformance P1/P2.1/P2.2; materialized real-market H0 experimental protocol and B0-B3 ladder, plus the implemented provider-neutral H1 Activity-Arrival synthetic conformance over its frozen scientific protocol; Anticipatory Market Intelligence contracts, internal DM-2 process, Phase-1 public evidence and ProfitDLL external qualification Round 1
**Historical hardenings:** rationale only; see `../history/hardenings/`.

## Rule of authority

Implementation MUST use the current material contracts below. Historical hardenings explain why decisions changed but MUST NOT be composed as an executable specification. If historical prose conflicts with this authority map or a current material schema/model, the historical prose is non-executable.

## Implemented baselines

| Slice | Status | Current authority |
|---|---|---|
| RH-I0 Contract Skeleton | COMPLETED | `RESEARCH-HARNESS-CONTRACTS.md` for lifecycle/identity foundations, as narrowed by current RH-I3 contracts where bundle representation evolved |
| RH-I1 Fixture Source + MarketClock | COMPLETED | `SYNTHETIC-EVENT-REPLAY-CONTRACTS.md` |
| RH-I2 Target Semantic Slice | COMPLETED | `TARGET-FIRST-PASSAGE-CONTRACTS.md` + material target schemas/sidecars in the implementation repository |
| RH-I3 Evidence Pipeline | COMPLETED | files listed below; accepted completion evidence is recorded in `RH-I3-IMPLEMENTATION-HANDOFF.md` |
| RH-I4 Temporal Adversarial Controls | COMPLETED | `RESEARCH-HARNESS-SCAFFOLD-PLAN.md`, `RESEARCH-VALIDATION-PROTOCOL.md`, material `EXP-WDO-CTRL-001@1.0.0`, `SMF-LEAK-001@1`, schemas and conformance tests |
| RH-I5 Episode and Lead-Time Controls | COMPLETED | `EPISODE-LEAD-TIME-CONTRACTS.md`, material `EXP-WDO-CTRL-005@1.0.0`, `SMF-EP-001@1`, `SMF-LEAD-001@1`, schemas and conformance tests |
| RH-I6 Episode Characterization | COMPLETED | `EPISODE-CHARACTERIZATION-CONTRACTS.md`; material CTRL-011/012, SMF-EP-002/003, V4 schemas, verified bundles and conformance tests |
| RH-I7 Baseline and Incrementality | COMPLETED | `BASELINE-INCREMENTALITY-CONTRACTS.md`; executable row-level CTRL-006/013 inputs, RH-I2 sidecars, independent populations, exact comparisons, manifests/hashes and closed V5 evidence |
| RH-I8 Live/Replay Equivalence | COMPLETED | `LIVE-REPLAY-EQUIVALENCE-CONTRACTS.md`; executable CTRL-009, shared semantic processor, isolated causal/replay delivery and closed V6 evidence |
| RH-I9 Scientific Scope Certification | COMPLETED | `SCIENTIFIC-SCOPE-CERTIFICATION-CONTRACTS.md`; final result and provenance in `RH-I9-CERTIFICATION-HANDOFF.md` |
| Post-RH-I9 audit remediation AR-01..AR-06 | COMPLETED / V2 CERTIFIED | `POST-RH-I9-AUDIT-REMEDIATION-CONTRACTS.md`; execution provenance and final portability closure in `FINAL-PRE-V1-AUDIT-CLOSURE-HANDOFF.md` |
| Research Harness v1.0.0 | RELEASED | Tag `research-harness-v1.0.0` at `d400ed9ab049aa4f7a887113b4de646bf2d1e40e`; historical certification and portable-path closure remain immutable |
| Multi-Instrument Research Harness Generalization | IMPLEMENTED / VALIDATED | `MULTI-INSTRUMENT-RESEARCH-HARNESS-GENERALIZATION.md`; closed scope authority/registry/material resolver, TEST_INSTRUMENT architecture proof, Evidence V8 and Certification V3 |
| Instrument Identity & Resolution foundation | IMPLEMENTED / VALIDATED | `../architecture/INSTRUMENT-IDENTITY-AND-RESOLUTION-CONTRACTS.md`; canonical definition/registry/catalog, provider-boundary resolver, WDO/TEST authorities and typed mono-instrument guards; no scientific wire change |
| Canonical Market Ingestion & Capability Slice 1 | IMPLEMENTED / VALIDATED | `../architecture/CANONICAL-MARKET-INGESTION-AND-CAPABILITY-CONTRACTS.md` and ADR-013; provider-neutral Trade path, compact shared context/lineage, temporal/order/correction semantics, multidimensional capability admission and synthetic A/B/C/D plus Alpha/Beta proofs; no Evidence/Certification or historical material change |
| Market Intelligence Runtime Executable Slice 1.1 | IMPLEMENTED / VALIDATED | `../architecture/MARKET-INTELLIGENCE-RUNTIME-CONTRACTS.md`, ADR-014 and `../architecture/MARKET-INTELLIGENCE-RUNTIME-SLICE-1-1-REMEDIATION-HANDOFF.md`; hardened deterministic synthetic chain, PIT/correction, evidence/state/timeline/Why Now, destructive recheck and strong zero-core-change extension proof; no real candidate/provider/data authority |
| Real-market single-instrument research execution Conformance Slice 1.3 | IMPLEMENTED / VALIDATED | `../architecture/REAL-MARKET-SINGLE-INSTRUMENT-RESEARCH-EXECUTION-CONTRACTS.md`, ADR-015 and `../architecture/CONFORMANCE-SLICE-1-3-HANDOFF.md`; authority production is anchored at `9987f6c0edbf65c8e39bd6c6d31e9b17d4215aea` and validation completes in its descendant-aware F-03 proof-repair checkpoint, with explicit immutable Phase A/Phase B selection; AUTH-01/AUTH-02/CORR-01, F-02/F-03 and RM-A05..RM-A09 remain closed; real H0 performance remains a separate blocked benchmark/design gate and no real data/experiment authority follows |
| H0 Optimization Conformance P1 | IMPLEMENTED / VALIDATED | `../architecture/H0-OPTIMIZATION-CONFORMANCE-P1-HANDOFF.md`; immutable projection-scoped preparation removes linear anchor lookup and copied windows while retaining the one governed crossing core; reference/optimized equality and byte-identical identity hashing pass; `sum(W_i)` remains quadratic in broad windows, so real H0 performance is BLOCKED PENDING P2 |
| H0 Optimization Conformance P2.1 | IMPLEMENTED / VALIDATED | `../architecture/H0-OPTIMIZATION-CONFORMANCE-P2-1-HANDOFF.md`; exact immutable range summaries eliminate sequential full-window contextual/history scans while preserving invalidator precedence, window-local ordering, known-gap/history semantics and the unchanged crossing loop; `sum(W_i)` remains dominant, so real H0 performance stays BLOCKED |
| H0 Optimization Conformance P2.2 | IMPLEMENTED / VALIDATED | `../architecture/H0-OPTIMIZATION-CONFORMANCE-P2-2-HANDOFF.md`; an immutable event-time-aware left-first index eliminates supported-input sequential first-terminal traversal while preserving availableAt horizon authority, eventTime economic eligibility, P2.1 full-window precedence and complete reference equality; real H0 remains unauthorized and performance claims await a DM-2-qualified dataset benchmark |
| H0 Real-Market Experimental Protocol | CONTRACT MATERIALIZED / SYNTHETIC CONFORMANCE IDENTITY CLOSURE SLICE 1.3 IMPLEMENTED | `H0-REAL-MARKET-EXPERIMENTAL-PROTOCOL.md` and `../architecture/H0-SYNTHETIC-CONFORMANCE-IDENTITY-CLOSURE-SLICE-1-3-HANDOFF.md`; the exact 25-cell accounting now consumes an opaque branch/target-use authority, append-only attempt and holdout-access histories, mandatory characterization completion and lossless upstream UTF-16/UTF-8 canonical identities and process-scoped shared holdout material exposure over governed synthetic material; real data, benchmark, H0 and H1 remain separately gated |
| Real-Market Baseline Ladder B0-B3 | CONTRACT MATERIALIZED / SYNTHETIC CONFORMANCE SLICE 1.3 REMEDIATION IMPLEMENTED | `REAL-MARKET-BASELINE-LADDER-B0-B3-CONTRACTS.md`, its contract handoff and the Slice 1/1.1/1.2/1.3 handoffs; scientific B2 value/refs/lineage/row identity are stutter-invariant while raw provenance remains separate, fitting identity is cutoff-scoped and future-world non-interfering, and full-`PairingKey` universes reject contamination before returning either truth-bearing valid results or target-blind information-atomic invalid results; B1/B2/B3/PIT/corrections remain preserved and real configuration/data/H1 remain unauthorized |
| H1 Activity-Arrival + Lead Scientific Protocol | CONTRACT MATERIALIZED / SYNTHETIC CONFORMANCE SLICE 1.5 IMPLEMENTED / REAL IMPLEMENTATION NOT AUTHORIZED | `H1-ACTIVITY-ARRIVAL-LEAD-SCIENTIFIC-PROTOCOL.md`, its protocol handoff and the Slice 1/1.1/1.2/1.3/1.4/1.5 handoffs; provider-neutral conformance now requires a versioned governed synthetic-world resolver for correction-aware longitudinal exact PIT, qualification, opportunity and complete-candidate authority, an opaque target-blind match for H1 row authenticity, and prebound B3 opportunity ancestry; no empirical detector, real H1 configuration or execution is authorized |
| Anticipatory Market Intelligence direction | CONTRACT MATERIALIZED | `ANTICIPATORY-MARKET-INTELLIGENCE-CONTRACTS.md` and `../market-data/ANTICIPATORY-INTELLIGENCE-DM-2-HANDOFF.md`; research/product direction only, no detector, empirical claim or external DM-2 qualification |
| DM-2 internal source/right qualification contract | MATERIALIZED / VALIDATED; PROFITDLL ROUND 1 COMPLETED / BLOCKED | `../market-data/DM-2-SOURCE-AND-RIGHTS-QUALIFICATION-CONTRACTS.md`, `../market-data/DM-2-EXTERNAL-QUESTIONS.md` and `../market-data/DM-2-PROFITDLL-EXTERNAL-QUALIFICATION-ROUND-1.md`; official public evidence is materialized in `../regulatory/EVIDENCE-REGISTER.md`, but exact ProfitDLL product/version, temporal/correction/arrival/replay semantics and rights remain unresolved; no source/dataset qualification, selection, acquisition, probe, DM-3A or anticipatory-research authorization follows |

RH-I0 through RH-I9 and DM-1 are COMPLETED. The RH-I9 Scientific Contract Freeze remains authoritative under `SCIENTIFIC-SCOPE-CERTIFICATION-CONTRACTS.md`; the completed execution result is recorded separately in `RH-I9-CERTIFICATION-HANDOFF.md`. Control IDs remain independent, and DM-2 remains an independent source/rights gate.

The post-audit certification protocol strengthens assurance without reinterpreting V1. `SCIENTIFIC_SCOPE_CERTIFICATION_V2`, `DM-CERTIFICATION-SCIENTIFIC-PROJECTION-V2` and `DM-CERTIFICATION-INTEGRITY-V2` add a recomputable pre-execution-plan binding, derived child bindings, centralized scientific code-state discovery, a package-backed trusted API and stronger run-summary checks. The CertificationScope remains `WDO_SYNTHETIC_TRADE_FIRST_PASSAGE@1.0.0`. The authorized V2 execution is `CERTIFIED`; its immutable plan and scientific hashes are recorded in `FINAL-PRE-V1-AUDIT-CLOSURE-HANDOFF.md`. The completed portable-path closure and independent review led to the immutable `research-harness-v1.0.0` release.

The descendant Multi-Instrument Generalization is governed by `MULTI-INSTRUMENT-RESEARCH-HARNESS-GENERALIZATION.md`. Reusable machinery now consumes an exact registered scope authority rather than interpreting WDO/control-name patterns. Historical WDO V1/V2 truth remains immutable. `TEST_INSTRUMENT_SYNTHETIC_HARNESS_TRAVERSAL@1.0.0` is a synthetic architecture proof under independently versioned Evidence V8 and Certification V3; it is not WIN, does not inherit WDO certification and makes no empirical or production claim. WIN, external DM-2 qualification and DM-3 were not started by that activity.

The canonical instrument identity foundation preserves the existing exact `InstrumentId` contract and all historical WDO/TEST material bytes. Runtime scientific strings are adapted to typed identities and validated by exact scope membership. Evidence V3-V8 and Certification V1-V3 remain unchanged; Evidence V9 and Certification V4 were not required. Provider namespaces/mappings, real Market Data, persistence, UI/API, rollover, production WDO/WIN identities, external DM-2 qualification and DM-3 remain outside that implementation.

The additive Canonical Market Ingestion & Capability authority is `../architecture/CANONICAL-MARKET-INGESTION-AND-CAPABILITY-CONTRACTS.md`. Its bounded executable Slice 1 is implemented and validated as synthetic conformance inside existing modules: A/B/C establish the neutral architecture, Source D adds without neutral-core production changes, and Beta traverses A/B/C/D without neutral ingestion/semantic algorithm changes. Historical scientific fixtures/materials, Evidence V3-V8 and Certification V1-V3 remain unchanged. Real providers, real data, DM-3A, Anticipatory research and real analytical candidates remain unauthorized.

The additive Market Intelligence Runtime authority is `../architecture/MARKET-INTELLIGENCE-RUNTIME-CONTRACTS.md` with ADR-014. Bounded Executable Slice 1.1 is implemented and validated in `research-analytics`; its hardening, destructive recheck and limitations are recorded in `../architecture/MARKET-INTELLIGENCE-RUNTIME-SLICE-1-1-REMEDIATION-HANDOFF.md`. It changes no historical scientific material, Evidence V3-V8 or Certification V1-V3 and creates no Evidence V9 or Certification V4. Real candidates, empirical behavior, provider/data integration and further executable scope remain separately gated.

The real-market single-instrument execution authority is `../architecture/REAL-MARKET-SINGLE-INSTRUMENT-RESEARCH-EXECUTION-CONTRACTS.md` with ADR-015. Its bounded synthetic Conformance Slice 1 is implemented and validated as recorded in `../architecture/REAL-MARKET-SINGLE-INSTRUMENT-RESEARCH-EXECUTION-CONFORMANCE-SLICE-1-HANDOFF.md`: TARGET-only analytics requires no fake context; historical synthetic and canonical-shaped synthetic inputs retain distinct identities and reach shared target, target-blind episode, H0 and B0 semantics. Real instruments, sessions, datasets, H0/H1 execution, empirical B1-B3 and DM-3A remain unauthorized.

The real-market H0 scientific protocol is `H0-REAL-MARKET-EXPERIMENTAL-PROTOCOL.md`. It freezes one exact target-blind population and anchor authority, complete execution or inadmissibility accounting for the 25-cell `ABSOLUTE_FIRST_PASSAGE_V1` Phase-A grid, H0-only admissibility/selection without a composite score, a complete attempt ledger and an immutable H0-to-H1 freeze with a sealed H1 confirmatory holdout. Synthetic Conformance Identity Closure Slice 1.3 is recorded in `../architecture/H0-SYNTHETIC-CONFORMANCE-IDENTITY-CLOSURE-SLICE-1-3-HANDOFF.md`; its opaque branch/target-use authority and append-only attempt/access histories plus shared material exposure and lossless upstream and local canonical text close H0-RA-01/02 while reusing the existing target/H0/B0/episode path. It does not supply provider/dataset/instrument facts, qualify DM-2, authorize the qualified-data benchmark or authorize real H0/H1 execution.

The downstream real-market B0-B3 specialization is `REAL-MARKET-BASELINE-LADDER-B0-B3-CONTRACTS.md`. It freezes B0 unconditional prevalence, B1 governed session/time prevalence, B2 causal target-instrument price/self-history and B3 simple deterministic causal price confirmation over one preserved H0 population. Primary future H1 predictive incrementality is against nested `B0+B1+B2`; B3 is the primary price-confirmation timing control. Synthetic Conformance Slice 1.3 preserves that science and completes the Slice-1.2 transitive boundary: B2 scientific refs/lineage/row identity ignore redundant raw arrivals while raw provenance remains authoritative but separate, fitting identity depends only on the knowable cutoff view, and pairing validates exact full-`PairingKey` universes atomically before returning a truth-bearing valid result or a target-blind invalid result without scientific coverage or decisions. Real B1-B3 configuration, empirical parameters and real execution remain unauthorized.

The H1 specialization is `H1-ACTIVITY-ARRIVAL-LEAD-SCIENTIFIC-PROTOCOL.md`. It freezes a non-directional occurrence/timing-only first H1, separates activity level from activity change, keeps predictive incrementality against `B0+B1+B2` distinct from temporal advantage against B3, and governs source-specific arrival/deduplication, detection opportunities, clocks, lead, target blindness, population/pairing, fitting and multiplicity. Provider-neutral Synthetic Conformance Slice 1.5 now proves the narrow arrival boundary, dedup/correction isolation, H1-L/H1-DELTA typing, clocks, lead taxonomy, fitting/holdout and full-PairingKey reuse through a versioned governed synthetic world: exact PIT completeness is correction-aware across frontiers and reconciled against one canonical source history through the existing correction ledger; qualification and opportunity authority remain resolver-issued, complete candidates cannot be caller-selected, target-blind matches remain opaque row authority and B3 opportunity ancestry remains prebound. It is algorithm-neutral laboratory instrumentation; no real H1 detector, preregistration, empirical parameter, data use or execution is authorized.

The current forward research direction is governed by `ANTICIPATORY-MARKET-INTELLIGENCE-CONTRACTS.md`. It preserves point-in-time admissibility, RH-I5 lead-time semantics, RH-I7 incrementality and CTRL-002 selection resistance while adding no empirical market truth. Its capability-driven input is `../market-data/ANTICIPATORY-INTELLIGENCE-DM-2-HANDOFF.md`; the materialized qualification process is `../market-data/DM-2-SOURCE-AND-RIGHTS-QUALIFICATION-CONTRACTS.md`. ProfitDLL external qualification Round 1 is completed from official public evidence, but the candidate is `BLOCKED / NOT SELECTED`: exact product/version, critical scientific semantics and applicable rights remain unresolved. Source/dataset qualification is incomplete; acquisition/probing, DM-3A, anticipatory research and WIN are not started or authorized.

## RH-I9 contract boundary

- `SCIENTIFIC-SCOPE-CERTIFICATION-CONTRACTS.md` is the current normative RH-I9 freeze authority.
- Material `WDO_SYNTHETIC_TRADE_FIRST_PASSAGE@1.0.0`, its declarative Certification Oracle, certification-specific schemas, and `CERT-CTRL-POS-001@1.0.0` / `CERT-CTRL-ADV-001@1.0.0` are frozen and validated by `tools/validate_rh_i9_materials.py`.
- The scope requires exactly CTRL-001/002/003/005/006/009/011/012/013, each with one predeclared PRIMARY and WITNESS under one clean code state.
- Certification is a composition domain using `DM-CERTIFICATION-SCIENTIFIC-PROJECTION-V1` and `DM-CERTIFICATION-INTEGRITY-V1`; it is not Evidence V8 and never rewrites V3-V7 children.
- Executable Phase-A machinery now consumes these frozen contracts through `research-harness/research-certification` and the certification CLI. It does not rerun controls by itself.
- The final 18 PRIMARY/WITNESS bundles verified under one clean code state; all nine `ControlConformance` values are PASS, all eight capabilities are SATISFIED, all twelve limitations are preserved, the real package verifies offline, and the deterministic certification rerun matches. `CertificationVerdict=CERTIFIED`; see `RH-I9-CERTIFICATION-HANDOFF.md` for the bounded claim and provenance.
- Historical V1 remains independently verifiable under explicit V1 dispatch. Future V2 packages use explicit V2 dispatch and MUST bind every physical child to the predeclared plan; V2 rules are never inferred from field presence or applied retroactively.
- All published Evidence and Certification Package paths use the host-independent namespace frozen by `PORTABLE-PACKAGE-PATH-POLICY.md`; this physical rule does not change historical scientific identities.

## CTRL-002 contract boundary

- NULL-ENSEMBLE-INTEGRITY-CONTRACTS.md freezes EXP-WDO-CTRL-002@1.0.0 as a NEGATIVE_CONTROL of complete finite null-ensemble preservation and post-hoc-selection resistance.
- SMF-NULL-001@1, its eight RH-I2 TargetSpecs, NULL-CONSTRUCTION-COMPLETE-BALANCED-BINARY-N4-K2@1.0.0, six ordered members and declarative oracle are materialized and independently validator-checkable.
- INV-NULL-001@1.0.0 is CRITICAL. Positive, zero and negative member deltas are all preserved; conformance depends on complete-ensemble/oracle agreement and canonical selectedMember=NONE, not on a statistical threshold.
- NULL_ENSEMBLE_V1, DM-SCIENTIFIC-PROJECTION-V7 and DM-BUNDLE-INTEGRITY-V7 are frozen as a new, separately dispatched Evidence domain. V3/V4/V5/V6 remain immutable.
- CTRL-002 executable Java, V7 runtime writer/verifier, deterministic rerun and tamper/anti-selection conformance tests are complete. RH-I9 consumed the frozen CTRL-002 truth without reinterpretation and completed certification.

## RH-I7 contract boundary

- `BASELINE-INCREMENTALITY-CONTRACTS.md` freezes common B0-B3 scientific semantics, material `PREVALENCE_BASELINE_V1@1.0.0`, raw-anchor pairing, exact categorical-match incrementality and `INV-BSL-001/002/003@1.0.0`.
- `REAL-MARKET-BASELINE-LADDER-B0-B3-CONTRACTS.md` specializes the future real-market ladder without changing the immutable RH-I7 synthetic control or treating it as market evidence.
- `EXP-WDO-CTRL-006@1.0.0` is the positive machinery-control contract and `EXP-WDO-CTRL-013@1.0.0` is the expected-INVALID adversarial baseline-selection contract.
- `SMF-BSL-001/002/003@1` have Amendment-1-frozen row-level materials, RH-I2 target sidecars, canonical manifests and independent case populations consumed by the executable controls.
- `BASELINE_INCREMENTALITY_V1`, `DM-SCIENTIFIC-PROJECTION-V5` and `DM-BUNDLE-INTEGRITY-V5` are implemented through explicit Evidence Pipeline dispatch. V3/V4 remain immutable and verifiable.
- The RH-I7 freeze remains `COMPLETED - AMENDED FOR EXECUTABLE MATERIALIZATION`; Java behavior, CTRL-006/013 runners and the V5 writer/verifier are implemented and verified.

## RH-I8 contract boundary

- `LIVE-REPLAY-EQUIVALENCE-CONTRACTS.md` freezes causal live-compatible and controlled replay delivery over one shared semantic processor.
- Material `EXP-WDO-CTRL-009@1.0.0`, `SMF-REPLAY-001@1`, target sidecars, independent oracle and Evidence V6 schemas exist.
- CTRL-009 is `SHADOW_REPLAY` positive equivalence machinery and requires checkpoint-level live/oracle, replay/oracle and live/replay equality.
- `LIVE_REPLAY_EQUIVALENCE_V1`, `DM-SCIENTIFIC-PROJECTION-V6` and `DM-BUNDLE-INTEGRITY-V6` are implemented through explicit version dispatch while V3/V4/V5 remain unchanged.
- RH-I8 executable implementation is complete. RH-I9 consumed the frozen CTRL-009 truth without reinterpretation and completed certification.

## RH-I6 contract boundary

- `EPISODE-CHARACTERIZATION-CONTRACTS.md` freezes target-blind, direction-agnostic descriptive characterization and `INV-EP-002@1.0.0`.
- `EXP-WDO-CTRL-011@1.0.0`, `EXP-WDO-CTRL-012@1.0.0`, `SMF-EP-002@1` and `SMF-EP-003@1` are materialized.
- The Evidence Pipeline V4 episode-characterization profile is implemented through explicit dispatch; existing V3 bundles remain unchanged and verifiable.
- CTRL-011 is `COMPLETED/PASS`; CTRL-012 is the expected `COMPLETED/INVALID` with CRITICAL `INV-EP-002`; V4 verification, deterministic rerun and tamper rejection pass.

## RH-I5 completion boundary

- `EXP-WDO-CTRL-005@1.0.0` is `COMPLETED` with `ResearchVerdict=PASS`; `INV-EP-001` and `INV-LEAD-001` both pass.
- `SMF-EP-001@1` preserves five raw anchors and maps them to one episode under its explicitly synthetic fixture-scoped policy.
- `SMF-LEAD-001@1` exactly reproduces positive, zero, negative, unknown-target and missing-detection truth using RH-I2 `T_target`.
- Equivalent CTRL-005 runs have identical `scientificHash`; closed-bundle verification and tamper rejection pass.
- CTRL-001 remains `COMPLETED/INVALID`; CTRL-003 remains `COMPLETED/PASS`.

## RH-I4 completion boundary

- The material CTRL-001 adversarial run is technically `COMPLETED` with the expected CRITICAL temporal finding and `ResearchVerdict=INVALID`; RH-I9 may derive `ControlConformance=PASS` only when that result exactly matches the frozen Certification Oracle.
- Point-in-time admissibility is governed by knowledge/availability time. Timestamp laundering with `eventTime <= decisionTime` and `availableAt > decisionTime` remains inadmissible.
- Both deterministic CTRL-001 acceptance runs verified with scientific hash `sha256:982516e8e140a485b8c04cf9be9a148e01a0f8ad97f138aced09968c4bc80a24` across distinct run identities.
- The CTRL-003 regression remains `COMPLETED` with `ResearchVerdict=PASS` and closed-bundle verification PASS.
- Temporary acceptance-run `bundleIntegrityHash` values are operational evidence and are not normative constants.

## RH-I3 executable authority

1. `EVIDENCE-CANONICAL-MODELS.md` — canonical logical/scientific representations, ordering and hashing projections.
2. `schemas/*.schema.json` — material wire contracts.
3. `EVIDENCE-IDENTITY-VALIDATION-PUBLICATION-CONTRACTS.md` — lifecycle, lineage, validation, physical serialization, publication and verifier behavior.
4. `RESEARCH-HARNESS-SCAFFOLD-PLAN.md` — module/build/CLI scaffold only where it references the current contracts; it MUST NOT redefine canonical fields or hashes.
5. `../../experiments/EXP-WDO-CTRL-003/1.0.0/experiment-spec.yaml` — material executable experiment.
6. `RH-I3-IMPLEMENTATION-HANDOFF.md` — implementation gate and final convergence decisions.

## Frozen RH-I3 rules

- Exactly four scientific CTRL-003 invariants. Evidence/scientific-hash and bundle-integrity recomputation are technical verifier/publication controls, not scientific invariants.
- `scientificHash` uses `DM-SCIENTIFIC-PROJECTION-V3`; `bundleIntegrityHash` uses `DM-BUNDLE-INTEGRITY-V3`.
- Physical JSON artifacts use `DM-CANONICAL-JSON-V1` plus exactly one terminal LF. Each `target-results.jsonl` line is one `DM-CANONICAL-JSON-V1` object plus LF.
- A COMPLETED RH-I3 bundle has the exact closed eleven-file set defined by the evidence contract. No `RESULT.md`, fixture snapshot, diagnostics directory or extension artifact is permitted.
- Publication destination is `<evidence-root>/runs/<runId>/`; `run-summary.bundlePath` is the relative `runs/<runId>`.
- `verify-bundle <bundle-dir>` is closed-bundle verification. It MUST NOT discover or require a repository, CWD ancestry, Git state, original fixtures or external sidecars.
- `validate-fixture` uses `--fixture-dir`.
- Evidence Card scientific fields are exactly those defined by the material schema/canonical model. Source/target lineage is in RunIdentity; baseline identity is outside RH-I3.
- Oracle PASS has `findingRefs=[]`. Oracle FAIL has exactly the deterministic mismatch finding reference. Orphan findings are invalid.
- Pre-publication hash/integrity recomputation failure is technical `FAILED`, without completed ResearchVerdict/bundle.

## Change discipline

A change to scientific meaning, canonical projection membership, hash derivation, lineage identity, verdict derivation, or publication safety requires an explicit contract change. Formatting, internal class decomposition and other deterministic implementation choices that preserve these contracts belong in code/tests rather than new pre-implementation hardenings.

## H1 Slice 1.1 temporal-authority closure

Provider-neutral Slice 1.1 closes H1-S1-AUD-F01..F04 as one authority boundary: every decision at T requires the exact `AS_KNOWN_AT(T)` world, cutoff-scoped scientific identity and lineage, structurally comparable opportunity authority and one non-contradictory verdict per governed material. The validated bounded evidence is recorded in `../architecture/H1-ACTIVITY-ARRIVAL-SYNTHETIC-CONFORMANCE-SLICE-1-1-TEMPORAL-AUTHORITY-HANDOFF.md`. No empirical detector, real H1 configuration, provider fact, data use or execution is authorized.

## H1 Slice 1.2 scientific-view and result-ancestry closure

Provider-neutral Slice 1.2 closes H1-S1.1-AUD-F05..F07 by separating full audit histories from complete scientific views at T and binding H1/B3 results to the exact opportunity ancestry that produced them. Lead comparison no longer accepts convenient caller authority; native opportunity suffixes and future detection-ledger suffixes cannot enter historical result, lineage, match or row identities. The bounded evidence is recorded in `../architecture/H1-ACTIVITY-ARRIVAL-SYNTHETIC-CONFORMANCE-SLICE-1-2-SCIENTIFIC-VIEW-ANCESTRY-HANDOFF.md`. F03/F04, H0, B1-B3 and historical material remain preserved; no empirical detector, real H1 configuration, provider fact, data use or execution is authorized.

## H1 Slice 1.3 candidate and opportunity authority closure

Provider-neutral Slice 1.3 closes H1-S1.2-AUD-F08..F10. Complete H1 candidate views are now produced by executing the frozen synthetic policy over every governed opportunity through T rather than accepting caller-selected results; B3 opportunity ancestry is bound during evaluation; and native-event lead requires structural fairness over the result-carried opportunity views. The bounded evidence is recorded in `../architecture/H1-ACTIVITY-ARRIVAL-SYNTHETIC-CONFORMANCE-SLICE-1-3-CANDIDATE-OPPORTUNITY-AUTHORITY-HANDOFF.md`. F03-F07, H0, B1-B3 and historical material remain preserved; no empirical detector, real H1 configuration, provider fact, data use or execution is authorized.
