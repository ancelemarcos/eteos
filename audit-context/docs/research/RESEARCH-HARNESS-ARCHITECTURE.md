# DataMarket Research Harness Architecture

Status: **ACCEPTED — RESEARCH INFRASTRUCTURE BASELINE**  
Phase: Research Phase 10  
Scope: Provider-independent scientific execution, replay-compatible validation and evidence production

## 1. Purpose

The Research Harness is the executable scientific laboratory of DataMarket. Its purpose is not to maximize backtest throughput or to create a parallel research-only implementation of market semantics. Its purpose is to execute frozen research contracts against synthetic or authorized datasets while reusing the same provider-independent semantic core intended for compatible live processing and replay.

The Harness must make a research claim reproducible from explicit inputs and must make invalid states difficult to express silently.

The governing chain is:

```text
Hypothesis
    -> ExperimentSpec (frozen)
    -> Dataset/Fixture Manifest
    -> ResearchRun
    -> MarketClock-driven semantic execution
    -> Target/Baseline/Candidate evaluation
    -> Oracle/Invariant validation
    -> EvidenceBundle
    -> EvidenceCard
    -> Registry update / ResearchDecision
```

The Harness is **not** the Market Engine, a provider adapter, a notebook collection, a production gateway, an order-routing system, or an alternate source of domain truth.

## 2. Architectural Thesis

DataMarket shall have **one semantic market-analysis core and multiple execution contexts**.

```text
                    +----------------------+
                    | Canonical semantics  |
                    | Market/Feature Core  |
                    +----------+-----------+
                               |
              +----------------+----------------+
              |                                 |
      +-------v--------+                +-------v--------+
      | Live execution |                | Research/Replay|
      | provider clock |                | MarketClock    |
      +----------------+                +----------------+
```

Research must not gain convenience by creating semantics that production cannot reproduce. Production must not gain speed by silently changing semantics proven in research. Where execution mechanics differ, the difference must be explicit and testable.

## 3. Scientific Architecture Principles

### RH-PR-001 — Semantic Core Reuse

Targets, canonical time semantics, quality semantics, feature definitions eligible for promotion, market-state transitions and derived-event semantics must use shared provider-independent implementations or shared contracts with equivalence tests.

### RH-PR-002 — Clock Is a Dependency

No research-relevant component may obtain wall-clock time implicitly. Time comes from `MarketClock`/controlled monotonic abstractions. Under the current RH-I1 replay contract, `MarketClock` is knowledge/replay time and advances by event `availableAt`; `eventTime` remains event-domain evidence and never rewinds the replay clock. A test or replay must be able to advance time deterministically.

### RH-PR-003 — Inputs Are Content-Addressed Evidence

Every promotion-relevant run references immutable/versioned specs, manifests, code revision and configuration hashes. File names are convenience; identity comes from declared IDs/versions and hashes.

### RH-PR-004 — No Hidden Experimental Choice

Material choices must be present in the Experiment Specification or referenced versioned configuration. Notebook cells, command-line history, local environment variables and analyst memory are not valid sources of confirmatory configuration.

### RH-PR-005 — Oracle Independence

Synthetic oracle truth should be declarative or independently implemented whenever practical. The same target implementation under test must not generate its own expected answer.

### RH-PR-006 — Fail Closed on Temporal Admissibility

Unknown availability time, ambiguous first-passage ordering, invalid freshness, unresolved gap semantics or missing required lineage must not be silently coerced into valid evidence.

### RH-PR-007 — Evidence Before Presentation

Charts and narrative are projections of an Evidence Bundle. They are not the primary result store.

### RH-PR-008 — Concise Conclusion, Deep Provenance

The Evidence Card is deliberately small. Every value on it must be traceable to deeper evidence.

### RH-PR-009 — Provider Independence

The Harness consumes canonical/fixture/replay sources through ports. Vendor SDK types must never enter target, baseline, feature, experiment or evidence modules.

### RH-PR-010 — Research Cannot Mutate Historical Truth

A run may derive new artifacts, but it may not modify the source dataset/fixture manifest it consumed.

## 4. Logical Components

```text
Research CLI / Test Driver
        |
        v
Experiment Loader -----> Spec Validator -----> Freeze Guard
        |                                         |
        +------------------+----------------------+
                           v
                     Run Coordinator
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
 Dataset/Fixture Source                MarketClock
          |                                 |
          +---------------+-----------------+
                          v
                  Canonical Event Stream
                          |
                          v
                    Semantic Pipeline
          MarketState -> Features -> Analytical/Event state
                          |
          +---------------+------------------+
          |               |                  |
          v               v                  v
     Target Engine   Baseline Engine   Candidate Evaluator
          |               |                  |
          +---------------+------------------+
                          v
                   Evaluation Engine
                          |
                 +--------+--------+
                 |                 |
                 v                 v
          Oracle/Invariant    Metrics/Diagnostics
              Validator             |
                 +---------+--------+
                           v
                     Evidence Writer
                           |
             EvidenceBundle + EvidenceCard
                           |
                           v
                 Experiment Registry projection
```

## 5. Module Boundaries

The names below are conceptual module names; exact Java package/module names remain an implementation decision before scaffold freeze.

### 5.1 `research-contract`

Owns immutable research contracts and validation rules:

- `ExperimentSpec`
- `HypothesisRef`
- `TargetSpecRef`
- `BaselineSpecRef`
- `DatasetRef`
- `FixtureRef`
- `SearchSpaceSpec`
- `SplitSpec`
- `MetricSpec`
- `AcceptanceSpec`
- `RunIdentity`
- `EvidenceCard`
- research verdict/evidence-strength types

It must not depend on Spring, provider SDKs, persistence frameworks or UI.

### 5.2 `research-source`

Ports for deterministic sources:

- synthetic fixture source;
- canonical event dataset source;
- future authorized replay source;
- macro-vintage/context source when applicable.

Responsibilities include manifest validation, hash verification, ordered iteration, explicit quality metadata and declared capabilities.

It does not normalize vendor payloads. Provider normalization belongs to Provider Adapters outside the Harness.

### 5.3 `research-clock`

Controlled time infrastructure:

- replay `MarketClock`;
- monotonic progression rules;
- scheduled callbacks/timers in market time;
- deterministic time advancement;
- no implicit `System.currentTimeMillis()` in research semantics.

Wall-clock runtime telemetry may use system time, but it must remain separate from market/research time.

### 5.4 `research-runner`

Orchestrates one immutable `ResearchRun`:

1. resolve spec;
2. validate freeze and references;
3. resolve source manifests;
4. verify hashes/rights/scope gates;
5. create controlled clock;
6. create fresh semantic state;
7. stream events;
8. evaluate targets/baselines/candidates;
9. run controls/oracles/invariants;
10. finalize metrics;
11. write Evidence Bundle atomically;
12. derive Evidence Card;
13. emit registry projection/update proposal.

The runner coordinates; it must not contain quantitative formulas that belong to engines.

### 5.5 `research-target`

Executes versioned target semantics defined by `WDO-TARGET-DEFINITION.md` and `TARGET-CANDIDATE-GRID.md`.

It must explicitly represent:

- anchor;
- reference price;
- horizon;
- magnitude;
- direction;
- first-passage time;
- persistence when applicable;
- censoring;
- ambiguity;
- invalidity;
- episode relationship.

No fabricated crossing time is allowed.

### 5.6 `research-baseline`

Executes B0–B4 comparator contracts. Baselines use the same admissible observation universe as the candidate comparison unless a frozen spec explicitly documents another design.

### 5.7 `research-evaluation`

Owns paired evaluation semantics:

- matching detections and targets;
- lead time;
- false-positive burden;
- false negatives;
- prevalence-aware metrics;
- incremental information;
- ablation comparison;
- episode-aware accounting;
- regime stratification;
- uncertainty summaries;
- sensitivity/search-space reporting.

It must not choose the winning model after observing holdout results.

### 5.8 `research-oracle`

Validates synthetic known truth and invariant expectations. Oracle results are first-class evidence.

A fixture may contain:

- expected canonical event order;
- expected admissibility at time `t`;
- expected target crossings;
- expected censored/ambiguous outcomes;
- expected episode count;
- expected baseline/candidate relation;
- expected failure class.

### 5.9 `research-evidence`

Writes immutable run artifacts and derives concise Evidence Cards.

It owns evidence schema/versioning, not the scientific semantics that generated values.

### 5.10 `research-registry`

Maintains the living index of experiments. The Markdown registry is a human-readable projection in the current phase; future machine-readable registry storage may be introduced without changing experiment identity semantics.

## 6. Ports

Minimum conceptual ports:

```java
interface ResearchEventSource {
    SourceManifest manifest();
    void replay(EventConsumer consumer, MarketClock clock);
}

interface ExperimentSpecRepository {
    ExperimentSpec load(ExperimentId id, SpecVersion version);
}

interface EvidenceRepository {
    EvidenceLocation commit(EvidenceBundle bundle);
}

interface OracleValidator {
    OracleResult validate(RunContext run, OracleManifest oracle);
}
```

These are illustrative contracts, not frozen Java signatures.

## 7. ResearchRun State Machine

`RESEARCH-HARNESS-CONTRACTS.md` separates technical execution from scientific disposition.

```text
CREATED
  -> VALIDATING
  -> READY
  -> RUNNING
  -> FINALIZING
  -> COMPLETED

VALIDATING -> INPUT_INVALID
Any non-terminal stage -> FAILED
Any active stage -> CANCELLED (reserved)
```

`RunStatus` is technical only. `INVALID` is **not** a run state. A technically `COMPLETED` run may produce `ResearchVerdict.INVALID` when a CRITICAL oracle, temporal-admissibility or invariant failure makes the scientific result uninterpretable. `INPUT_INVALID` means execution was rejected before scientific evaluation and therefore has no `ResearchVerdict`.

## 8. Determinism Contract

For a deterministic experiment, the tuple:

```text
(spec hash,
 dataset/fixture manifest hashes,
 code revision,
 config hash,
 declared seeds,
 semantic engine versions)
```

must be sufficient to reproduce the same semantic result within explicitly documented numeric tolerances.

Non-deterministic algorithms must declare seeds and sources of nondeterminism. If exact reproducibility is impossible, the spec must define the reproducibility envelope and why.

## 9. Event Ordering Contract

The Harness must not create a fictitious global provider sequence. Ordering uses canonical event semantics and source-specific sequence domains defined by ADR-005.

For equal or incomparable timestamps, deterministic tie-breaking may be required for execution reproducibility, but such tie-breaking must not be misrepresented as original market ordering.

When original ordering is scientifically necessary and unavailable, the relevant conclusion is `AMBIGUOUS`, `CENSORED`, `DATA_LIMITED` or `INVALID` according to the governing target/dataset policy.

## 10. Clock and Scheduling Semantics

Three time domains must remain conceptually separate:

1. market/event time;
2. availability/decision time;
3. wall-clock execution time.

Research timers such as horizon expiry, persistence and freshness use controlled market/research time. Benchmark runtime uses wall/monotonic execution time and cannot alter semantic results.

## 11. Dataset Admission Gate

Before `READY`, the runner validates:

- dataset/fixture identity and version;
- manifest schema;
- content hashes;
- declared capabilities;
- required timestamps;
- quality/gap policy compatibility;
- instrument/contract identity;
- applicable research certification level;
- applicable rights status for real licensed data;
- target/baseline capability requirements.

A dataset being physically readable is not sufficient admission.

## 12. Experiment Freeze Guard

The runner must compare the requested run with the frozen Experiment Specification.

Material mismatches cause refusal or a new spec/run lineage. Examples:

- target changed;
- baseline changed;
- primary metric changed;
- period/split changed;
- search space expanded;
- regime definition changed;
- acceptance threshold changed;
- dataset changed outside permitted frozen family/version rule.

Operational parameters that do not affect scientific interpretation may remain runtime parameters, but their classification must be explicit.

## 13. Synthetic Fixture Execution

Synthetic fixtures enter through the same canonical source port expected by replay-compatible research. Test-only shortcuts may exist to inspect internal invariants, but promotion-relevant fixture execution must exercise the relevant production-compatible semantic path.

Fixture generation and fixture consumption are separate phases:

```text
FixtureDefinition + seed
       -> generator
       -> immutable fixture + manifest + oracle
       -> independent Harness run
```

The run must never regenerate expected truth from observed outputs.

## 14. Target Evaluation Pipeline

For each admissible anchor:

```text
anchor(t)
  -> reference price known at t
  -> open target horizon
  -> consume only admissible subsequent observations
  -> classify first passage / no hit / ambiguity / censoring
  -> persistence qualification if specified
  -> episode association
  -> target observation
```

The target engine must preserve both `T_cross` and `T_target` when persistence changes the time at which the target becomes knowable.

## 15. Baseline and Candidate Pairing

Candidate and baseline evaluation should be paired by a stable observation key such as:

```text
(datasetId, instrumentId, tradingDate, anchorId, targetDefinitionId)
```

The exact key is implementation-specific but must prevent accidental comparison over different universes.

Missing candidate evidence is not automatically zero. Missingness policy is frozen in the spec.

## 16. Episode Accounting

The Harness maintains both anchor-level and episode-level views. It must never silently use anchor count as the effective independent sample size.

Evidence must expose at least:

- anchors evaluated;
- positive/negative anchors;
- clustered episodes;
- trading days;
- contracts;
- regime distribution;
- excluded/censored/ambiguous observations.

## 17. Evidence Bundle

A promotion-relevant run produces a directory/object logically equivalent to:

```text
evidence/
  manifest.json
  experiment-spec.snapshot.yaml
  dataset-manifests/
  run-environment.json
  metrics.json
  paired-results.*
  target-characterization.*
  regime-results.*
  uncertainty.*
  oracle-results.json
  invariant-results.json
  exclusions.json
  search-space.json
  diagnostics/
  evidence-card.yaml
  checksums.sha256
```

Exact physical formats are not frozen. The logical contents and traceability are.

Raw licensed payloads must not be copied into Evidence Bundles unless rights explicitly permit it and the bundle classification/retention policy allows it.

## 18. Evidence Card Contract

The Evidence Card is a projection, never an independent manually edited conclusion.

It must answer concisely:

- what claim was tested;
- against which target and primary baseline;
- on what effective sample;
- what the primary and incremental result were;
- what lead-time/failure burden was observed;
- whether behavior depends materially on regime;
- what uncertainty and limitations remain;
- verdict;
- evidence strength;
- next action.

A card without a resolvable finalized Evidence Bundle is scientifically invalid. The canonical Evidence Card and bundle/hash contracts are defined by `RESEARCH-HARNESS-CONTRACTS.md`.

## 19. Research Decision Boundary

The Harness computes evidence; it does not autonomously promote architecture or product behavior.

Possible research outcomes include:

- reject hypothesis;
- revise and preregister new hypothesis;
- replicate;
- candidate for validation;
- promotion candidate.

Promotion into Feature/Market/Event Engine configuration remains an explicit governed decision with traceability to evidence.

## 20. Failure Taxonomy

At minimum distinguish:

- `SPEC_INVALID`
- `DATASET_INVALID`
- `RIGHTS_BLOCKED`
- `CAPABILITY_MISMATCH`
- `TEMPORAL_ADMISSIBILITY_FAILURE`
- `ORACLE_FAILURE`
- `INVARIANT_FAILURE`
- `REPLAY_DIVERGENCE`
- `NUMERIC_FAILURE`
- `EXECUTION_FAILURE`
- `EVIDENCE_COMMIT_FAILURE`

Failure classes are evidence and must be preserved.

## 21. No-Lookahead Enforcement Points

Look-ahead protection is defense in depth:

1. dataset manifest declares temporal fields;
2. source exposes observations with availability semantics;
3. runner advances controlled clock;
4. feature access checks admissibility;
5. target labels remain isolated from candidate feature computation;
6. split/search-space guard prevents holdout feedback;
7. synthetic future-leak controls test the whole path.

No single timestamp comparison is considered sufficient protection.

## 22. Live/Replay Equivalence Boundary

Equivalence means semantic equivalence for the validated scope, not byte-identical runtime behavior.

Must be equivalent where applicable:

- canonical input interpretation;
- market-state transitions;
- feature calculations;
- quality/freshness propagation;
- analytical/event semantics;
- deterministic target-independent outputs.

May differ:

- transport;
- wall-clock latency;
- batching mechanics that do not change semantics;
- persistence mechanics;
- operational telemetry.

`EXP-WDO-CTRL-009` validates this boundary.

The constructive RH-I8 freeze is `LIVE-REPLAY-EQUIVALENCE-CONTRACTS.md`. It closes causal delivery, controlled replay, ReleaseFrontier/DecisionKnowledge, checkpoint-level three-way oracle equality, EOS/coverage, first divergence and Evidence V6 without creating a second semantic core.

## 23. Performance Philosophy

Correctness precedes throughput for the Research Harness. Nevertheless, the Harness should support efficient sequential replay and controlled parallelism across **independent runs**, datasets or partitions where scientific semantics permit it.

Do not parallelize within a single stateful market stream merely for speed if it changes ordering/ownership semantics.

Initial optimization order:

1. semantic correctness;
2. deterministic reproducibility;
3. observability;
4. efficient sequential replay;
5. safe run-level parallelism;
6. specialized optimization only from measurements.

## 24. Parallelism Model

Preferred initial model:

```text
Run A -> one deterministic stream/state ownership
Run B -> one deterministic stream/state ownership
Run C -> one deterministic stream/state ownership
```

Runs may execute concurrently if resources permit. Within a run, state ownership follows ADR-004.

Virtual threads, worker pools, vectorization, off-heap storage or specialized queues are implementation candidates, not research semantics.

## 25. Memory and Artifact Discipline

The Harness should stream large datasets rather than require full-file loading. Rolling state belongs in memory; large result tables may be written incrementally to run-scoped temporary artifacts and committed atomically at finalization.

Partial outputs from failed runs must not masquerade as completed Evidence Bundles.

## 26. Atomic Evidence Commit

Evidence publication follows:

```text
RUNNING -> temporary run area
FINALIZING -> validate bundle completeness + hashes
COMPLETED -> atomic/transactional publish of immutable bundle
```

If commit fails, the run is not `COMPLETED` even if computation finished.

## 27. Schema and Versioning

Machine-readable contracts require explicit schema versions:

- experiment spec schema;
- dataset/fixture manifest schema;
- evidence bundle schema;
- evidence card schema;
- oracle schema;
- metric/result schemas where material.

Readers must reject incompatible major versions rather than guess.

## 28. Numerical Integrity

Price-domain calculations follow canonical fixed-point semantics where applicable. Statistical calculations may use floating point, but conversions must be explicit.

The Harness must record:

- units;
- normalization definition;
- missing-value policy;
- numeric tolerance where oracle comparison uses floating point;
- library/version where algorithmic differences can alter results.

## 29. Rights and Data Isolation

The Harness must be capable of running fully with synthetic fixtures and must not require licensed Market Data for infrastructure validation.

For real data:

- rights profile is checked before admission;
- evidence artifacts inherit lineage restrictions;
- raw-data export is disabled unless explicitly authorized;
- logs must not accidentally dump licensed payloads;
- external publication is a separate gate.

## 30. Security Boundary

Research convenience does not justify embedding provider credentials or secrets in specs/manifests. Secrets are runtime configuration outside immutable scientific specs; the spec may reference a credential profile identifier but never contain secret material.

## 31. Observability

Each run should expose two telemetry planes.

### Scientific telemetry

- input counts;
- exclusions;
- gaps/duplicates/reorders;
- targets opened/resolved/censored;
- episode counts;
- metric progress;
- oracle/invariant results;
- evidence artifacts.

### Operational telemetry

- wall-clock duration;
- events/sec;
- CPU;
- memory/GC;
- I/O;
- queue/backlog where applicable.

Operational performance must not be confused with market-time latency or lead time.

## 32. CLI / Invocation Boundary

A minimal future invocation may conceptually resemble:

```text
datamarket research validate-fixture SMF-TIME-001@1

datamarket research run EXP-WDO-CTRL-001@1

datamarket research verify <run-id>

datamarket research card <run-id>
```

Exact command syntax is PENDING_IMPLEMENTATION. The key requirement is non-interactive reproducibility suitable for CI.

## 33. CI Role

Provider-independent controls should eventually run in CI in tiers:

- fast invariant/unit suite on normal changes;
- deterministic fixture suite on research/core changes;
- extended adversarial/metamorphic suite on scheduled or gated builds;
- real-data shadow tests only where rights and environment permit.

A CRITICAL synthetic control regression must block promotion of affected research/core changes.

## 34. Notebook Policy

Notebooks may be used for exploration and visualization. They are not the authoritative execution path for confirmatory results.

A notebook may consume an Evidence Bundle. A confirmatory Evidence Bundle must be reproducible without relying on notebook execution order or hidden notebook state.

## 35. Research Storage Boundary

Initial Harness operation should prefer simple immutable filesystem/artifact storage for fixtures/specs/evidence where practical. PostgreSQL may index operational metadata later. ClickHouse, object storage, workflow engines or distributed compute are not required for the first validated scope.

Do not add infrastructure merely because research platforms often use it.

## 36. Initial Validated Scope

The first implementation target is intentionally narrow:

```text
Scope: WDO_SYNTHETIC_TRADE_FIRST_PASSAGE_V1

Includes:
- canonical trade-like synthetic events;
- controlled MarketClock;
- absolute first-passage target semantics;
- gaps/duplicates/reorder controls relevant to trade stream;
- anchor/episode accounting;
- lead-time accounting;
- common B0-B3 baseline semantics required by controls, with only synthetic B0 materially configured initially;
- null/redundant/incremental candidate controls;
- immutable ExperimentSpec/Run/EvidenceBundle/EvidenceCard;
- CTRL-001 through applicable CTRL-010 fixture-backed tests.

Excludes initially:
- MBP/MBO reconstruction;
- concrete provider SDK;
- licensed B3 payloads;
- news/LLM;
- production WebSocket gateway;
- production persistence topology;
- ML frameworks;
- distributed research compute.
```

## 37. Minimum Vertical Slice

The first executable vertical slice should prove this chain end-to-end:

```text
SMF fixture
 -> manifest/hash validation
 -> controlled source
 -> MarketClock
 -> canonical event processing
 -> target evaluation
 -> oracle comparison
 -> Evidence Bundle
 -> Evidence Card
```

Only after that should baseline/candidate statistical controls be layered in.

## 38. Implementation Sequence

### RH-I0 — Contract skeleton

Implement machine-readable schemas/types for fixture manifest, experiment spec snapshot, run identity, oracle result, evidence bundle manifest and Evidence Card.

### RH-I1 — Deterministic fixture source + clock

Implement synthetic source, controlled clock and manifest/hash verification.

### RH-I2 — Target semantic slice

Implement absolute first-passage target evaluation and independent oracle fixtures for crossing/no-crossing/ambiguity/gap/persistence boundary cases.

### RH-I3 — Evidence pipeline

Implement run lifecycle, invariant results, atomic Evidence Bundle and derived Evidence Card.

### RH-I4 — Temporal adversarial controls

Execute leakage/admissibility controls, including `EXP-WDO-CTRL-001`.

### RH-I5 — Episode/lead-time controls

Implement anchor clustering/episode accounting and lead-time validation.

### RH-I6 - Episode characterization

Characterize declared synthetic anchor populations under predeclared direction-agnostic target-blind policies. The normative contract is `EPISODE-CHARACTERIZATION-CONTRACTS.md`; implementation remains separately gated.

### RH-I7 - Baseline/incrementality controls

The current contract, amended with complete executable input material, is frozen by `BASELINE-INCREMENTALITY-CONTRACTS.md`. The completed implementation executes synthetic B0 and common B0-B3 comparison semantics for redundancy/incrementality controls without selecting empirical B1-B3 parameters. CTRL-002 separately owns finite null-ensemble integrity under NULL-ENSEMBLE-INTEGRITY-CONTRACTS.md. Evidence uses explicit V5 dispatch; RH-I8 subsequently completed without altering it.

### RH-I8 - Replay equivalence

The contract, material `EXP-WDO-CTRL-009@1.0.0`, `SMF-REPLAY-001@1`, independent oracle and V6 schemas are frozen by `LIVE-REPLAY-EQUIVALENCE-CONTRACTS.md`. Executable Java, closed V6 publication and verification are complete. RH-I9 subsequently consumed this frozen truth and completed the bounded scope certification without changing RH-I8 semantics.

### RH-I9 - Scope certification

The closed scope-certification package defined by `SCIENTIFIC-SCOPE-CERTIFICATION-CONTRACTS.md` has been composed and recursively verified. All nine required controls have `ControlConformance=PASS`, including exact Oracle matches for expected adversarial child CRITICAL failures, and `CertificationVerdict=CERTIFIED`. The bounded result and provenance are recorded in `RH-I9-CERTIFICATION-HANDOFF.md`; no empirical or production scope is implied.

## 39. Implementation Gate Before Coding

Before creating production-oriented Java modules, resolve only the choices needed to make the scaffold reproducible:

- exact JDK distribution/version;
- build tool;
- module/package naming;
- test framework;
- serialization format/library for machine-readable research contracts;
- hash algorithm and canonicalization rules;
- artifact directory convention;
- architecture-conformance rules.

Do **not** require provider selection, B3 rights, production queue technology, client framework or production SLOs to implement the provider-independent Harness.

## 40. Architecture Conformance Rules

The future build should enforce at least:

1. research contracts/core have no Spring dependency;
2. research target/baseline/evaluation have no provider SDK dependency;
3. semantic core has no filesystem/database dependency;
4. evidence storage depends inward through ports;
5. notebooks are not dependencies of production/research core;
6. target labels cannot be imported into candidate feature computation packages;
7. system clock access is forbidden in research-semantic packages except explicitly approved operational adapters;
8. provider types cannot cross Provider Adapter boundary.

ArchUnit or equivalent may enforce applicable Java rules after scaffold selection.

## 41. Definition of Done — Architecture

This architecture baseline is complete when:

- the logical components and boundaries are understood;
- the initial validated scope is explicit;
- the first vertical slice is explicit;
- implementation order is explicit;
- unresolved technology choices remain visibly pending;
- no licensed-data assumption is introduced;
- no duplicate research-only market semantics are authorized.

The provider-independent laboratory and its first bounded synthetic CertificationScope are implemented and certified as recorded in `RH-I9-CERTIFICATION-HANDOFF.md`. This does not claim empirical WDO behavior, provider/data rights, predictive value or production readiness.

## 42. Definition of Done — First Harness Scope

`WDO_SYNTHETIC_TRADE_FIRST_PASSAGE@1.0.0` may be certified only when:

- all nine required controls have `ControlConformance=PASS`, including exact expected adversarial `ResearchVerdict=INVALID` truth;
- future leakage controls fail closed as expected;
- target oracle fixtures match expected semantics;
- gaps/ambiguity do not fabricate exact truth;
- episode and lead-time accounting match oracle truth;
- null/redundancy/incrementality controls behave as designed;
- deterministic reruns reproduce within declared tolerance;
- Evidence Bundles are immutable/complete/verifiable;
- Evidence Cards are derived from bundles;
- live/replay equivalence passes for the shared semantics in scope;
- the validation report identifies exclusions and unresolved scopes.

## 43. Non-Goals

This phase does not:

- implement the Harness;
- choose a B3 provider;
- authorize licensed data;
- choose predictive WDO features;
- choose Pressure Engine formula;
- choose ML model;
- choose production infrastructure;
- optimize for maximum replay throughput;
- certify MBP/MBO research;
- certify macro/news research.

## 44. Next Artifact

The next implementation-facing artifact should be:

`docs/research/RESEARCH-HARNESS-SCAFFOLD-PLAN.md`

It should convert this architecture into a reproducible Java scaffold plan: modules, package boundaries, build/test commands, schema locations, first fixture IDs, first executable control, conformance tests and acceptance checklist — without yet freezing production infrastructure unrelated to the Harness.

## RH-I2 target semantic specialization

`TARGET-FIRST-PASSAGE-CONTRACTS.md` specializes the first target implementation to deterministic trade-only `ABSOLUTE_FIRST_PASSAGE_V1`. The accepted architecture remains unchanged: target semantics stay provider-independent and reusable. For this slice, first passage is decided in knowledge/replay order, target state is minimal trade-only state, and observation coverage is explicit rather than inferred from stream termination. See `TARGET-FIRST-PASSAGE-CONTRACTS.md`.
