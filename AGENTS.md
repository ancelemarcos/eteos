DataMarket — Agent Instructions

1. Purpose

DataMarket is a financial market intelligence platform.

The system is intended to collect, normalize, process, correlate, and analyze financial market information in near real time and transform it into contextual and derived market intelligence.

The initial product focus is the Brazilian financial market, especially:

- WDO / DOL
- WIN / IND
- DI futures

The platform may correlate Brazilian market behavior with international markets, macroeconomic events, market microstructure, and other legally licensed information sources.

DataMarket is initially an analytics and market-intelligence platform.

It is not an order-routing or automated trading platform unless a future architecture decision explicitly changes this constraint.

---

2. Repository Knowledge Model

"AGENTS.md" is the operational map for AI coding agents.

It must remain concise.

Detailed product, architecture, research, regulatory, and implementation knowledge belongs in the repository documentation.

Before making significant architectural or product decisions, inspect the relevant documentation under "docs/".
For end-to-end delivery decisions, also inspect `docs/architecture/DELIVERY-ROADMAP.md`; for canonical ingestion, normalization, source lineage, capability or admission work, begin with `docs/architecture/CANONICAL-MARKET-INGESTION-AND-CAPABILITY-CONTRACTS.md`; for source/provider/licensing work, begin with `docs/market-data/DM-2-SOURCE-AND-RIGHTS-QUALIFICATION-CONTRACTS.md`, then use `docs/market-data/SOURCE-QUALIFICATION-REGISTER.md` and `docs/regulatory/EVIDENCE-REGISTER.md` for evolving state and evidence.

Expected documentation structure will progressively include:

docs/
├── product/
├── architecture/
│   └── decisions/
├── market-data/
├── research/
└── regulatory/

Do not duplicate large amounts of documentation inside "AGENTS.md".

---

3. Source of Truth

Repository documentation is the persistent source of truth for the project.

When information conflicts, use the following precedence:

1. Explicit instructions from the current task.
2. Applicable "AGENTS.md" or deeper scoped agent instructions.
3. Accepted Architecture Decision Records (ADRs) for decision semantics.
4. "docs/architecture/DECISION-REGISTER.md" for the implementation status of decisions contained inside accepted ADRs; an ACCEPTED ADR does not make every PROPOSED/PENDING item inside it accepted.
5. "docs/architecture/DOMAIN-LANGUAGE.md" for canonical cross-document names, state namespaces, identifiers, time semantics, and type vocabulary, provided it does not alter an ADR decision.
6. Current architecture documentation.
7. Current product documentation.
8. Existing implementation.
9. Assumptions.

If documentation and implementation disagree, do not silently choose one.

Identify the inconsistency and determine whether the code or documentation is outdated.

---

4. Decision Classification

Do not treat every idea described in the repository as an established requirement.

Important technical and product statements should be distinguishable as:

ACCEPTED

A decision that has been approved and may be implemented.

PROPOSED

A candidate decision that has not yet been approved.

Do not introduce significant architectural dependencies based solely on a PROPOSED decision.

EXPERIMENTAL

An implementation or approach being evaluated.

It may be changed or removed.

HYPOTHESIS

A proposition that must be validated empirically.

This classification is especially important for quantitative market relationships.

PENDING

A decision blocked by external information, licensing, regulation, market-data provider constraints, or another unresolved dependency.

Do not silently convert PENDING decisions into assumptions.

Before implementing a significant architectural choice, consult `docs/architecture/DECISION-REGISTER.md`. An ADR-level status of ACCEPTED means the ADR's normative accepted decisions are approved; alternatives and items explicitly marked PROPOSED, EXPERIMENTAL, HYPOTHESIS, PENDING, BENCHMARK REQUIRED, or RESEARCH REQUIRED remain non-accepted until promoted explicitly.

Use `docs/architecture/TRACEABILITY.md` to identify the requirements governed by an architectural decision.

Use `docs/architecture/MVP-READINESS-GATE.md` to distinguish what must be resolved before research, during research, before implementation, and before production.

Use `docs/architecture/READINESS-STATUS.md` as the live instance of those gates and blockers.

Use `docs/product/OBJECTIVE-COMPLETION-CONTRACT.md` to protect the final product objective from scope drift, and `docs/architecture/DELIVERY-ROADMAP.md` / `OBJECTIVE-COVERAGE-MATRIX.md` to understand how current work contributes to the production MVP. Research Harness completion is a delivery milestone, not the final product objective.

For quantitative research, historical evaluation, target definition, lead-time claims, feature/model experiments, or promotion of research hypotheses, consult `docs/research/RESEARCH-METHODOLOGY.md` before creating or interpreting results.

For any research dataset, replay dataset, historical capture, macro vintage, continuous-futures artifact, or dataset certification, consult `docs/research/DATASET-POLICY.md`.

Before confirmatory quantitative experimentation or promoting a market relationship, consult `docs/research/HYPOTHESIS-FRAMEWORK.md`. Exploratory findings must remain labeled exploratory until preregistered and independently evaluated according to that framework.

For WDO movement labels, target timestamps, lead-time evaluation, target magnitudes/horizons, overlap/censoring, contract/roll semantics, or target selection, consult `docs/research/WDO-TARGET-DEFINITION.md`. Do not invent numeric WDO target parameters outside a declared research plan.

For the WDO quantitative research program, evidence-family selection, baseline hierarchy, experiment ordering, incremental-information/ablation work, regime research, promotion criteria, or Pressure-related research, consult `docs/research/WDO-RESEARCH-PLAN.md`. Treat every evidence family and backlog relationship as a research candidate until validated; do not infer weights, thresholds, predictive value, or causality from its inclusion in the plan.

---

5. Financial Market Research Rules

Financial relationships must not be assumed to be stable or causal.

Examples:

US Treasury yields ↑
USD strength ↑
WDO ↑

may represent a useful hypothesis but must not automatically become a hard-coded trading rule.

Any quantitative relationship used by the system should eventually be supported by empirical validation.

When implementing research or quantitative analysis:

- separate correlation from causation;
- avoid look-ahead bias;
- avoid survivorship bias where applicable;
- preserve event timestamps;
- distinguish event time from processing time;
- avoid using information that would not have been available at the evaluated instant;
- measure false positives and false negatives;
- measure lead time when evaluating predictive or anticipatory indicators;
- test behavior across different market regimes;
- document assumptions;
- prefer reproducible experiments;
- distinguish exploratory discovery from confirmatory evaluation;
- preregister confirmatory hypotheses before inspecting their evaluation data;
- preserve rejected, inconclusive and invalid research results;
- declare search spaces and material researcher degrees of freedom;
- never convert a compelling market narrative directly into production logic.

A model that performs well historically must not automatically be considered predictive.

---

6. Time Is a First-Class Concept

Market systems are extremely sensitive to time.

Never casually discard timestamp precision.

Where relevant, distinguish:

- source timestamp;
- exchange timestamp;
- provider timestamp;
- ingestion timestamp;
- processing timestamp;
- publication timestamp;
- client receipt timestamp.

Use UTC internally unless a documented component requires otherwise.

User interfaces may convert timestamps to the user's configured timezone.

Never infer event ordering solely from database insertion order.

---

7. Market Data Integrity

Market Data must be treated as an auditable data stream.

Processing pipelines should preserve enough metadata to determine:

- source;
- instrument;
- timestamp;
- sequence when available;
- processing stage;
- data quality;
- stale-data condition.

The system must never silently present stale information as current information.

Components consuming real-time or near-real-time data should consider:

- disconnections;
- delayed feeds;
- duplicated events;
- missing events;
- out-of-order events;
- clock differences;
- reconnection;
- recovery;
- provider throttling.

Data-quality state should be explicit whenever technically possible.

---

8. Licensing and Regulatory Boundaries

Market Data usage is subject to licensing agreements and regulatory constraints.

Do not assume that data technically accessible to the system may legally be:

- stored indefinitely;
- redistributed;
- displayed;
- exposed through an API;
- used for model training;
- used for backtesting;
- commercialized;
- reconstructed from derived outputs.

Before implementing functionality that materially changes how licensed Market Data is consumed, stored, displayed, distributed, or commercialized, inspect the relevant documentation under:

docs/regulatory/
docs/market-data/

If the applicable rule is unresolved, classify the implementation decision as PENDING rather than inventing a policy.

Never commit credentials, API keys, certificates, tokens, private feeds, licensed datasets, or confidential provider documentation to the repository.

---

9. Derived Intelligence

The long-term value of DataMarket should come primarily from processing and interpretation rather than simple replication of raw Market Data.

Examples may include:

- contextual indicators;
- statistical measurements;
- market-state classifications;
- volatility analysis;
- divergence detection;
- regime detection;
- event detection;
- cross-market relationships;
- alerts;
- derived scores;
- explanatory context.

Exact proprietary formulas, weights, models, and signal-generation methodologies should be treated as sensitive intellectual property.

Do not expose proprietary algorithms unnecessarily through:

- client applications;
- logs;
- public APIs;
- documentation intended for external audiences;
- error messages.

Prefer server-side execution for proprietary analytical logic unless an accepted architecture decision explicitly requires otherwise.

---

10. Architecture Principles

Prefer:

- clear component boundaries;
- explicit contracts;
- deterministic behavior where possible;
- immutable event representations where practical;
- observability;
- testability;
- graceful degradation;
- fault isolation;
- horizontal scalability where justified;
- measurable performance.

Avoid premature distributed-system complexity.

Do not introduce a new:

- database;
- message broker;
- programming language;
- framework;
- infrastructure service;
- cloud dependency;

without a concrete requirement or accepted architecture decision.

Performance-sensitive components must be benchmarked before being rewritten solely for theoretical performance gains.

---

11. Real-Time Processing

The real-time processing path must remain predictable and lightweight.

Avoid unnecessary operations in latency-sensitive paths, including:

- synchronous remote calls;
- blocking persistence;
- excessive object allocation;
- unnecessary serialization/deserialization;
- AI/LLM inference;
- expensive logging.

AI-based interpretation must not be placed in the critical market-data processing path unless explicitly approved by an architecture decision.

Detection should not depend on waiting for natural-language news interpretation when observable market behavior can provide an earlier signal.

---

12. Client Applications

Client applications should primarily consume processed market intelligence rather than unnecessarily reproducing the complete raw processing pipeline.

User interfaces should prioritize:

- responsiveness;
- clarity;
- low cognitive load;
- explicit data freshness;
- connection status;
- event timing;
- graceful reconnection.

Desktop, mobile, and web interfaces may present different information densities while sharing domain contracts where appropriate.

Do not assume that every server event needs to produce a UI render.

High-frequency server data should be appropriately aggregated or sampled for human visualization.

---

13. Security

Apply secure-by-default practices.

Never commit:

- passwords;
- secrets;
- private keys;
- production certificates;
- access tokens;
- provider credentials;
- customer information.

Secrets must be supplied through approved external configuration mechanisms.

Validate external inputs.

Treat Market Data providers, news providers, APIs, WebSockets, files, and message brokers as external trust boundaries.

Avoid logging sensitive credentials or licensed raw payloads unnecessarily.

---

14. Implementation Discipline

Before implementing a task:

1. Read the applicable repository instructions.
2. Inspect relevant documentation.
3. Inspect existing implementation before proposing replacements.
4. Identify whether the requested behavior is ACCEPTED, PROPOSED, EXPERIMENTAL, HYPOTHESIS, or PENDING.
   For architectural choices, an implementation-authorizing decision must have a Decision ID in `docs/architecture/DECISION-REGISTER.md`; absence is not permission to implement.
5. Identify regulatory or Market Data implications when applicable.
6. Make the smallest coherent change that satisfies the task.

Do not perform unrelated refactors while implementing a focused task.

Do not replace working components merely because another technology is preferred.

---

15. Testing

New behavior should be testable.

Prefer automated tests for:

- domain calculations;
- event normalization;
- timestamp handling;
- state transitions;
- reconnection behavior;
- duplicate handling;
- ordering behavior;
- quantitative calculations;
- API contracts.

Quantitative algorithms should use deterministic datasets whenever possible.

Regression datasets should preserve important historical market scenarios without embedding licensed data when such storage is not permitted.

Never fabricate test success.

If a test cannot be executed, report that explicitly.

---

## Agent Execution Efficiency

Repository authority and scientific rigor take precedence over execution
speed. Performance optimizations must never weaken fail-closed behavior,
reproducibility, validation, or milestone exit gates.

During implementation:

- read the smallest applicable current authority set first; begin with
  `CURRENT-RESEARCH-CONTRACTS.md` for Research Harness work and follow its
  normative references on demand;
- do not recursively reread historical hardenings or reviews unless needed
  to investigate a specific conflict;
- prefer the narrowest Maven test that covers the current change; when using
  Maven reactor selection, include required upstream modules when necessary
  (for example through `-pl` / `-am`) rather than rebuilding the entire reactor;
- when selecting a specific test across a reactor build, account for upstream
  modules that do not contain that test instead of treating their absence as
  a test failure;
- expand validation progressively from specific test → affected module →
  affected dependency set;
- do not run `clean` on every iteration;
- reserve the complete normative `mvnw clean verify` for milestone/final exit
  gates or when a full clean validation is specifically required;
- independent non-mutating validators may run in parallel when they do not
  share mutable outputs;
- do not run concurrent Maven builds against the same `target/` directories;
- Maven offline mode may be used for intermediate validation only when all
  required artifacts are already available locally; it is an optimization,
  never a requirement;
- prefer targeted Git inspection over repository-wide ignored-file scans;
- never skip required final validation because an incremental validation
  already passed.
- do not rerun an expensive full validation solely for an administrative
  operation such as staging or committing when the exact tracked content was
  already fully validated and has not changed; if tracked content changes,
  the applicable validation must be re-established;

Environment-specific command workarounds, filesystem paths, antivirus
configuration, SSD placement, and local cache tuning are local operational
concerns and should not become portable project requirements.

---

16. Observability

Important processing stages should eventually expose sufficient telemetry to diagnose:

- feed latency;
- processing latency;
- event throughput;
- dropped events;
- reconnects;
- stale feeds;
- queue pressure;
- processing errors.

Observability must not significantly degrade the latency-sensitive path.

---

17. Documentation

Update documentation when a change modifies:

- architecture;
- public contracts;
- significant domain behavior;
- infrastructure;
- Market Data usage;
- regulatory assumptions;
- development procedures.

Architecture decisions with long-term consequences should be recorded as ADRs rather than hidden in code comments.

Comments should explain why, not restate obvious code behavior.

---

18. Git Practices

Keep commits focused and understandable.

Do not mix unrelated changes in the same commit.

Do not commit:

- generated build artifacts;
- local IDE state;
- temporary files;
- credentials;
- raw licensed Market Data;
- debugging dumps.

Before considering a task complete:

1. inspect the diff;
2. run applicable tests;
3. run applicable formatting/linting checks;
4. verify no secrets or unintended files were introduced;
5. report any validation that could not be performed.

---

19. Do Not Guess Critical Requirements

When an implementation depends on unresolved information involving:

- B3 licensing;
- Market Data rights;
- provider contracts;
- regulatory classification;
- financial methodology;
- security;
- proprietary algorithms;

do not silently invent the missing requirement.

Prefer documenting the uncertainty and requesting a decision.

---


20. Canonical Domain Language

Before introducing or implementing a new domain term, state, enum, identifier, timestamp, quality flag, readiness value, lifecycle value, or cross-component contract, inspect:

docs/architecture/DOMAIN-LANGUAGE.md

Reuse an existing canonical concept when semantics match.

Do not create a generic Status, State, Quality, or ConnectionState enum that merges unrelated domains.

In particular, keep separate:

- FreshnessState;
- DataQuality / DataValidity / DataQualityFlag;
- MarketStateLifecycle;
- FeatureReadiness;
- ModelReadiness;
- ProviderConnectionState;
- ProviderSubscriptionState;
- ClientConnectionState;
- EventLifecycle.

If an accepted ADR and DOMAIN-LANGUAGE.md appear to conflict semantically, the ADR decision is authoritative and the inconsistency must be reported rather than silently normalized.

---

21. Guiding Principle

DataMarket should help users understand market context faster and more clearly.

Correctness, temporal integrity, data quality, explainability, security, and regulatory compliance take precedence over adding features quickly.

Optimize only after measuring.

Validate market hypotheses before treating them as facts.

Protect proprietary intelligence.

Keep the system understandable. 

## Research Phase 6 — WDO Target Candidate Grid

For any WDO target-characterization, baseline, lead-time, evidence-family or predictive experiment, consult `docs/research/TARGET-CANDIDATE-GRID.md` after the governing research methodology, dataset policy, hypothesis framework, target definition and WDO research plan.

For any WDO baseline characterization, candidate-vs-baseline comparison, incremental-information claim, ablation study, or model/evidence promotion, consult `docs/research/BASELINE-DEFINITION.md`. Never claim predictive value from standalone accuracy, correlation, AUC, lead time or significance without the declared baseline stack and equivalent point-in-time evaluation.

The Phase A numeric grid is a frozen **research hypothesis space**, not a set of accepted production thresholds. Do not optimize, densify or change its magnitudes/horizons after inspecting predictor performance. Any expansion requires a new preregistered experiment/version. Actual characterization requires an authorized dataset with sufficient certification and temporal fidelity.

## Research Phase 8 — Experiment Specification and Evidence Contract

For every formal quantitative experiment, consult `docs/research/EXPERIMENT-SPECIFICATION.md` and register the experiment in `docs/research/EXPERIMENT-REGISTRY.md` before confirmatory execution.

Use the Research Evidence Contract: hypothesis → frozen specification → immutable run → evidence bundle → evidence card → research decision. Do not leave material experiment choices only in code, notebooks, command lines or narrative prose.

Every evaluated formal experiment must produce a concise Evidence Card with verdict, baseline-relative result, lead-time/failure burden when applicable, robustness, regime dependence, uncertainty, limitations, evidence strength and next action. The card summarizes evidence; it never replaces the auditable result bundle.

Never change preregistered target, primary metric, baseline, split, search space, regime definition or acceptance rule after inspecting confirmatory outcomes without creating a new experiment/specification version. Preserve FAIL, INCONCLUSIVE and INVALID results.


## Research Phase 9 — Synthetic Fixtures and Laboratory Validation

Before implementing or running provider-independent research controls, synthetic target tests, temporal-admissibility tests, replay-equivalence tests, null controls, or research-infrastructure validation, consult `docs/research/SYNTHETIC-MARKET-FIXTURES.md` and `docs/research/RESEARCH-VALIDATION-PROTOCOL.md`.

Treat synthetic fixtures as scientific instrumentation, not as evidence of real-market predictive power. Every promotion-relevant fixture must have a stable ID/version, manifest, deterministic or seeded generation, explicit oracle truth, allowed assertions and forbidden claims. Do not derive the oracle from the same implementation path being validated when an independent declarative/reference oracle is practical.

A failing CRITICAL laboratory control blocks confirmatory research in the affected scope. Do not weaken a fixture oracle, point-in-time rule, target semantic or experiment freeze rule merely to make an implementation pass. Preserve failing validation runs and lineage.

Research-laboratory readiness is scope-specific. `LAB_VALIDATED_FOR_SCOPE` for trade-only WDO first-passage semantics does not imply readiness for MBP/MBO, macro-vintage, provider-recovery or other research scopes.

## Research Phase 10 — Research Harness Architecture

Before implementing provider-independent research infrastructure, replay runners, fixture executors, target evaluators, Evidence Bundle writers or experiment orchestration, consult `docs/research/RESEARCH-HARNESS-ARCHITECTURE.md`.

Maintain one provider-independent semantic market-analysis core across compatible live and research/replay execution. Do not create research-only target, feature, market-state or event semantics merely for convenience. Differences in execution mechanics must remain explicit and equivalence-testable.

The first Harness scope is `WDO_SYNTHETIC_TRADE_FIRST_PASSAGE_V1`. Do not expand it to MBP/MBO, concrete provider SDKs, licensed Market Data, news/LLM, distributed research infrastructure or production client concerns unless a later task explicitly changes the scope.

Research-semantic code must use controlled `MarketClock` time. Do not access system wall-clock time as market/decision time. Evidence Cards must be derived from immutable Evidence Bundles; notebooks are exploratory/projection tools, not the authoritative confirmatory execution path.

## Research Phase 11 — Research Harness Scaffold Plan

Before creating or modifying Research Harness Java modules, build files, schemas, fixtures, CLI commands, architecture tests or Evidence Bundle filesystem layout, consult `docs/research/RESEARCH-HARNESS-SCAFFOLD-PLAN.md` after `RESEARCH-HARNESS-ARCHITECTURE.md`.

The first implementation scope is frozen to `WDO_SYNTHETIC_TRADE_FIRST_PASSAGE_V1`. Implement milestones RH-I0 through RH-I9 incrementally; do not add Spring Boot, provider SDKs, databases, licensed Market Data, MBP/MBO, predictive WDO features or Pressure Engine logic merely to make the scaffold look production-complete.

For RH-I0+ use vendor-neutral Java 25 LTS and the Maven Wrapper multi-module baseline. Oracle JDK 25.0.3 is the current DEV baseline; do not enforce a JDK vendor. Pin actual tool/dependency patch versions in the root build, record exact runtime vendor/version in `RunEnvironment`, and make `./mvnw clean verify` succeed without external services. Architecture/conformance tests are part of the scaffold contract, not optional cleanup.

RH-I0 through RH-I9 are completed implementation baselines. CTRL-002
Null / No-Information Control is also EVALUATED / COMPLETED.

Preserve all accepted scientific/material contracts and Evidence profiles
through V7. The RH-I9 Scientific Contract Freeze is completed under
`docs/research/SCIENTIFIC-SCOPE-CERTIFICATION-CONTRACTS.md`. RH-I9 Scientific
Scope Certification is completed for
`WDO_SYNTHETIC_TRADE_FIRST_PASSAGE@1.0.0` with
`CertificationVerdict=CERTIFIED`; the bounded result and provenance are
recorded in `docs/research/RH-I9-CERTIFICATION-HANDOFF.md`. DM-1 is completed.
DM-2 remains an independent source/rights qualification track, and DM-3
remains gated by its applicable DM-1/DM-2 conditions and authorized data.

Post-RH-I9 audit remediation AR-01 through AR-06 is implemented under
`docs/research/POST-RH-I9-AUDIT-REMEDIATION-CONTRACTS.md`; its separately
authorized V2 certification execution is `CERTIFIED`. Historical certification
V1 remains immutable and verifiable. Portable package paths are governed by
`docs/research/PORTABLE-PACKAGE-PATH-POLICY.md`; that assurance closure is
included in the released `research-harness-v1.0.0` tag at
`d400ed9ab049aa4f7a887113b4de646bf2d1e40e`.

After `research-harness-v1.0.0`, Multi-Instrument Research Harness
Generalization is the mandatory first substantive development activity. No WIN
or third-instrument scientific implementation may begin before a second
synthetic test instrument traverses the reusable core without core changes.
Certification and scientific validation never inherit across instruments.
Before adopting the first Git submodule, complete the separately documented
`BEFORE-FIRST-SUBMODULE` canonicalization gate. These gates do not begin DM-2,
DM-3, or WIN.

For current implementation authority, do not reconstruct behavior by layering
historical hardening documents. Read
`docs/research/CURRENT-RESEARCH-CONTRACTS.md` first and follow its normative
references as needed. Historical hardenings are rationale/audit history only.

Completed Harness work does not authorize providers, databases, persistence,
BAR/OHLC, empirical baseline research, prediction, licensed Market Data,
Pressure Engine logic, or production scope unless explicitly authorized by a
later accepted decision.

## Canonical Market Ingestion and Capability Foundation

Before work involving canonical/native separation, source lineage,
observation context, multiple source clocks or ordering domains, corrections,
source quality/control, capability negotiation, purpose-specific admission,
provider switching or ingestion rights handoff, consult
`docs/architecture/CANONICAL-MARKET-INGESTION-AND-CAPABILITY-CONTRACTS.md`.

The contract is `MATERIALIZED`; executable Slice 1 is `IMPLEMENTED / VALIDATED`
as a bounded synthetic conformance foundation. The first provider must not become the ontology
of DataMarket. Missing semantics remain missing, richer qualified semantics
must not be erased, adapters cannot self-certify capability, provider
scientific equivalence never inherits, and SourceLineage/ObservationContext
are logical models that permit compact references rather than mandatory
per-event context duplication.

The completed first ingestion slice is synthetic conformance only. It does not
authorize a real provider, real Market Data, real WDO/WIN identity, DM-3A,
Anticipatory research or real analytical candidates.

## Market Intelligence Runtime Contract

Before work involving derived observables, candidate evidence, analytical
state, evidence contradiction/abstention, analytical relationships, Evidence
Timeline or structured "Why Now?", consult
`docs/architecture/MARKET-INTELLIGENCE-RUNTIME-CONTRACTS.md` and ADR-014.

The contract is `MATERIALIZED / VALIDATED`; bounded Executable Slice 1 is
`IMPLEMENTED / VALIDATED` in `research-harness/research-analytics` as deterministic
synthetic architecture conformance. `MarketState` is factual; `AnalyticalState`
is interpretive. The checkpoint adds no real candidate, empirical claim, Evidence
V9, Certification V4, universal score or trading semantic. Consult
`docs/architecture/MARKET-INTELLIGENCE-RUNTIME-SLICE-1-HANDOFF.md` for the
implementation boundary. Further runtime, provider, data or candidate work
requires separate explicit authorization.

## Anticipatory Market Intelligence Direction

Before work involving anticipatory evidence, lead-time characterization,
AnalyticalState transitions, pressure/absorption/exhaustion hypotheses,
liquidity withdrawal, evidence confluence/contradiction, cross-market
lead/lag, participant activity, Evidence Timeline or "Why Now?", consult
`docs/research/ANTICIPATORY-MARKET-INTELLIGENCE-CONTRACTS.md`.

For DM-2 source/provider/rights qualification supporting those capabilities,
also consult
`docs/market-data/ANTICIPATORY-INTELLIGENCE-DM-2-HANDOFF.md`. The contract is a
research/product direction, not an empirical performance claim. It does not
authorize detectors, scores, provider integration, Market Data acquisition or
DM-2/DM-3 execution.
