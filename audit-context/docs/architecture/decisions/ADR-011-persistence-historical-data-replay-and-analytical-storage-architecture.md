ADR-011 — Persistence, Historical Data, Replay and Analytical Storage Architecture

Status: ACCEPTED
Date: 2026-08-29
Decision scope: Persistence boundaries, operational data, historical market data, derived analytical data, replay datasets, research storage, retention, partitioning, write path, reconstruction, point-in-time integrity and analytical database evolution
Supersedes: None
Superseded by: None

---

Terminology alignment notice (2026-08-29): Canonical implementation names, state namespaces, time-field names and cross-ADR vocabulary are consolidated in `docs/architecture/DOMAIN-LANGUAGE.md`. This notice is editorial and does not change this ADR's accepted decision semantics. Where this ADR uses a conceptual/legacy label, apply the canonical mapping only when semantics are equivalent.

---


1. Context

ADR-004 through ADR-010 established the primary DataMarket processing path:

Market Data
    ↓
Canonical Events
    ↓
Market State
    ↓
Feature Engine
    ↓
Market Engine
    ↓
Event Engine
    ↓
Derived Market Events
    ↓
Publication

The authoritative current Market State is held in memory.

Persistence is deliberately outside the critical analytical path.

DataMarket nevertheless requires historical information for fundamentally different purposes:

operational application data

market-data research

replay

feature validation

model research

event studies

lead-time analysis

Derived Market Event history

auditability

configuration/version history

observability

These workloads have different:

volume

write rate

query patterns

retention

consistency requirements

licensing restrictions

latency requirements

Trying to solve all of them with one undifferentiated database model would couple unrelated concerns and eventually create both performance and correctness problems.

---

2. Decision

DataMarket will use a:

«Multi-tier persistence architecture based on data purpose»

rather than treating persistence as one universal database.

Conceptually:

                    ┌───────────────────────┐
                    │      DataMarket       │
                    └───────────┬───────────┘
                                │
       ┌────────────────────────┼────────────────────────┐
       │                        │                        │
       ▼                        ▼                        ▼
Operational Data       Analytical History       Telemetry
       │                        │                        │
 users                  market observations        metrics
 auth                    derived events             logs
 config                  selected features          traces
 subscriptions           replay datasets
 entitlements            research metadata

Storage technologies may differ by tier.

---

3. Fundamental Persistence Rule

Persistence must not define real-time analytical truth.

The authoritative live path remains:

Canonical Event
      ↓
Market State
      ↓
Feature Engine
      ↓
Market Engine
      ↓
Event Engine

not:

Canonical Event
      ↓
Database
      ↓
SELECT
      ↓
Feature Engine

Database access is not part of the per-event analytical hot path.

---

4. Market State Remains In Memory

ADR-006 remains authoritative.

Current market state is:

in-memory
single-writer owned where practical
freshness-aware
quality-aware
reconstructable

Persistence is not the mechanism through which Feature Engine reads current market state.

---

5. Persistence Is Downstream

Preferred architecture:

Real-Time Processing
       │
       ├────────────► Publication
       │
       ├────────────► Alerting
       │
       └────────────► Persistence Boundary
                            ↓
                       async writers

Persistence failure must not automatically stop real-time analytical processing.

---

6. Storage Domains

DataMarket distinguishes at least five logical persistence domains:

1. OPERATIONAL DATA

2. MARKET HISTORY

3. DERIVED ANALYTICAL HISTORY

4. RESEARCH / REPLAY DATASETS

5. TELEMETRY

These domains may initially share physical infrastructure where appropriate.

Logical separation does not require premature physical separation.

---

7. Operational Data

Operational data includes information such as:

users

accounts

authentication metadata

subscriptions

devices

push registrations

entitlements

application configuration

provider configuration metadata

instrument metadata

feature configuration

Market Model configuration

Event Rule configuration

version activation history

audit records

This workload is conventional transactional application data.

---

8. Operational Database

The initial operational database will be:

«PostgreSQL»

PostgreSQL is ACCEPTED for operational application data.

This decision does not imply PostgreSQL must permanently store every historical market event.

---

9. Why PostgreSQL Operationally

The operational workload benefits from:

transactions

constraints

referential integrity

mature indexing

SQL

backup/recovery ecosystem

Java ecosystem support

operational familiarity

It is not sufficiently unusual to justify a specialized database initially.

---

10. Market History

Historical market information is conceptually different from operational application data.

Potential market history includes:

trades

quotes

book updates

statistics

market status

source timestamps

sequence metadata

data-quality events

However:

«The fact that DataMarket technically receives data does not automatically mean DataMarket is legally permitted to persist it indefinitely.»

---

11. Licensing Gate

Raw or normalized Market Data retention is conditional on:

B3 contract

provider contract

Product Development rights

historical-data rights

storage rights

derived-data rights

Therefore exact raw Market Data retention periods remain:

«PENDING LICENSING CONFIRMATION»

No implementation may silently assume indefinite retention rights.

---

12. Storage Classification

Every persisted market-related dataset should have an explicit classification.

Conceptually:

RAW_PROVIDER_DATA

NORMALIZED_MARKET_DATA

DERIVED_FEATURE_DATA

ANALYTICAL_STATE

DERIVED_MARKET_EVENT

RESEARCH_DATASET

OPERATIONAL_DATA

TELEMETRY

This classification supports:

retention policy

access control

licensing review

backup policy

deletion policy

---

13. Raw Provider Data

Raw provider messages are the closest representation of what arrived from the source.

Examples could include:

provider packet

provider callback payload

vendor-specific message

DataMarket does not automatically persist every raw provider message.

Raw persistence requires a demonstrated need and legal permission.

---

14. Normalized Market Data

Canonical Events represent normalized observations.

Persisting selected Canonical Events may provide:

provider-independent replay

research

debugging

algorithm validation

but the same licensing gate applies.

---

15. Derived Analytical History

Derived information may include:

feature snapshots

Analytical State

Derived Market Events

event evidence

regime states

quality transitions

These objects have substantially greater product value per byte than blindly persisting every transient internal calculation.

---

16. Persistence Priority

If licensing and cost prevent retaining everything, the initial priority should generally be:

Derived Market Events
        ↓
significant analytical state
        ↓
research observations
        ↓
selected feature state
        ↓
normalized Market Data where permitted
        ↓
raw provider payload where justified

This is an architectural preference, not a licensing interpretation.

---

17. Do Not Persist Every Feature Update

Rejected:

every tick
    ↓
hundreds of features
    ↓
INSERT hundreds of rows

unless a specific research dataset explicitly requires it.

Feature persistence must be intentional.

---

18. Research Capture

The system will support explicit:

«Research Capture Policies»

defining what information should be retained for a particular experiment.

Conceptually:

ResearchCapturePolicy

datasetId

instruments

time range

event types

feature set

sampling policy

quality requirements

retention policy

license classification

Exact representation remains pending.

---

19. Research Dataset

A research dataset must be treated as a versioned artifact.

Conceptually:

datasetId
datasetVersion

createdAt

source description

time range

instrument universe

provider information

canonical schema version

instrument metadata version

feature versions if included

quality policy

known gaps

licensing classification

content hash / integrity metadata

---

20. Dataset Immutability

Once a research dataset version is declared complete:

«its historical contents should be immutable.»

Corrections create a new dataset version.

Rejected:

silently change old research data

because experiments would cease to be reproducible.

---

21. Point-in-Time Truth

Historical research must preserve:

«what DataMarket could have known at that instant»

rather than merely storing today's corrected understanding of the past.

This is essential for preventing look-ahead bias.

---

22. Observed vs Revised Values

For information that may later be revised:

economic releases

statistics

reference data

news metadata

DataMarket should preserve, where available and legally permitted:

value observed then

time it became available

later revision

time revision became available

A replay at T must not see a revision published at T+1.

---

23. No Future Knowledge

Historical storage must never make it easy for production/replay code to accidentally consume:

future candles

end-of-day statistics before day end

future session high/low

revised macro values not yet published

future events

future normalization parameters

---

24. Event-Time Storage

Historical records should preserve the relevant temporal domains defined by ADR-005.

Depending on record type:

eventTime

providerSendTime

ingestionTime

processingTime

detectedAt

publicationTime

must not be collapsed into one generic:

timestamp

---

25. Trading Date

Historical market records should preserve:

tradingDate

separately from UTC timestamps where applicable.

Trading sessions are not equivalent to UTC calendar days.

---

26. Source Provenance

Historical observations must preserve sufficient provenance to identify:

provider

feed

environment

instrument mapping

schema version

quality state

where applicable.

---

27. Sequence Semantics

Provider sequence metadata described by ADR-005 must not be replaced by database insertion order.

Rejected:

ORDER BY database_id

as a substitute for market chronology.

---

28. Replay

DataMarket will provide a dedicated:

«Replay Engine»

for feeding historical Canonical Events into the same or compatible analytical pipeline used in production.

Conceptually:

Historical Dataset
       ↓
Replay Source
       ↓
Canonical Event Port
       ↓
Market State
       ↓
Feature Engine
       ↓
Market Engine
       ↓
Event Engine

---

29. Production and Replay Logic

The analytical logic must not have separate:

ProductionFeatureEngine
ResearchFeatureEngine

implementations containing independently maintained formulas.

Preferred:

                ┌── Live Source
Canonical Port ◄┤
                └── Replay Source
                      ↓
                same analytical logic

---

30. Replay Clock

Replay uses the "MarketClock" abstraction established previously.

Rejected:

Thread.sleep()
Instant.now()

as definitions of historical market time.

---

31. Replay Modes

Replay should support conceptually:

REAL_TIME

ACCELERATED

STEP

MAX_SPEED

subject to dataset availability and licensing.

Logical analytical results must not depend on replay wall-clock speed.

---

32. Deterministic Replay

Given identical:

dataset

Canonical schema

instrument metadata

FeatureSet

Market Model

Event Rules

configuration

event ordering

a deterministic pipeline should produce equivalent logical outputs.

---

33. Replay Session

Every experiment/replay run should have an identity.

Conceptually:

replayRunId

datasetId
datasetVersion

codeVersion

featureSetVersion

marketModelVersion

eventRuleVersion

configurationVersion

startedAt
completedAt

resultSummary

---

34. Reproducibility

A result such as:

"Model detected pressure 18 seconds before target movement"

is insufficient by itself.

DataMarket should be able to answer:

Which dataset?

Which dataset version?

Which code version?

Which FeatureSet?

Which Market Model?

Which Event Rules?

Which configuration?

Which target definition?

---

35. Experiment Definition

Research experiments should be explicit artifacts.

Conceptually:

ExperimentDefinition

experimentId
version

dataset

target definition

features

model

event rules

metrics

evaluation windows

regime segmentation

---

36. Experiment Result

Results should also be versioned artifacts.

Conceptually:

ExperimentResult

experimentId
runId

metrics

event count

lead-time distribution

false positives

false negatives

regime breakdown

quality breakdown

execution metadata

---

37. Research Is Not Production State

Research runs must not mutate:

live Market State

live Feature State

production Event Engine state

user alerts

Research resources remain isolated from production processing.

---

38. Research Resource Isolation

Large replay jobs may consume substantial:

CPU

memory

disk bandwidth

database bandwidth

They must not degrade live market processing.

ADR-002 already allows research/replay to execute as a separate process.

That separation is strongly recommended.

---

39. Persistence Write Path

Real-time processing should hand persistence work to an asynchronous bounded boundary.

Conceptually:

Analytical Core
       ↓
Persistence Record
       ↓
bounded queue
       ↓
Persistence Writer
       ↓
Storage

---

40. No Transaction Per Tick

Rejected:

Canonical Event
       ↓
@Transactional
       ↓
INSERT
       ↓
COMMIT

for every individual high-frequency event.

---

41. Batch Writes

Historical persistence should support batching where appropriate.

Conceptually:

events
events
events
events
   ↓
bounded batch
   ↓
storage write

Batch size and flush interval require benchmarking.

---

42. Batching Must Not Redefine Event Time

The fact that 1,000 observations are written together does not mean they occurred at the same time.

Original temporal metadata remains authoritative.

---

43. Persistence Queue

Persistence queues must be:

bounded

observable

semantically governed

Unbounded queues are rejected.

---

44. Persistence Backlog

Measure:

queue depth

oldest item age

write throughput

batch size

write latency

failure rate

A persistence backlog must not remain invisible.

---

45. Persistence Failure

If analytical-history persistence becomes unavailable:

Market Engine
Event Engine
Client publication

should continue where safe.

The system must clearly report:

HISTORICAL_PERSISTENCE_DEGRADED

or equivalent operational state.

---

46. Data Loss Policy

The system must explicitly define, per persistence class, whether temporary inability to write allows:

retry

bounded buffering

spill to local durable storage

drop

stop capture

There is no universal policy.

---

47. Never Pretend Persistence Succeeded

If research capture data was lost, the resulting dataset must be marked:

INCOMPLETE

or equivalent.

It must not silently become a valid research dataset.

---

48. Dataset Quality

Research datasets should track:

COMPLETE

INCOMPLETE

GAPPED

DEGRADED

INVALID

or equivalent quality states.

---

49. Gap Metadata

Known gaps must be persisted as metadata.

Example:

WDO

2026-08-28
10:14:32.150 → 10:14:34.420

reason:
provider reconnect

Research code must be able to discover this.

---

50. Gap Is Data

Absence of observations and known data loss are different things.

Therefore:

no trades occurred

must not be confused with:

feed unavailable

Historical datasets must preserve this distinction.

---

51. PostgreSQL Historical Role

PostgreSQL is an ACCEPTED initial candidate for:

Derived Market Events

research metadata

experiment metadata

configuration/version history

moderate-volume analytical history

and may initially store selected normalized market observations if benchmark and licensing permit.

---

52. PostgreSQL Is Not Automatically the Permanent Tick Store

This ADR explicitly avoids the decision:

«All historical Market Data will permanently live in PostgreSQL.»

That conclusion requires:

actual event rates

retention

query workload

storage cost

write throughput

research patterns

licensing

---

53. PostgreSQL Partitioning

For large time-oriented historical tables, PostgreSQL declarative partitioning is a strong candidate.

Likely primary dimension:

time / trading date

Exact granularity remains pending.

Examples:

daily

weekly

monthly

must be selected from measured volume and operational requirements.

---

54. Partition Key

Partition keys must reflect:

query patterns

retention operations

data volume

maintenance

pruning effectiveness

not arbitrary convention.

---

55. Avoid Excessive Partitions

Creating one partition for every:

instrument
×
day
×
event type

could create excessive database objects.

Partition design must remain operationally manageable.

---

56. Retention by Partition

Where time-based retention applies, dropping/detaching entire old partitions is preferable to massive row-by-row DELETE operations when schema design permits it.

---

57. PostgreSQL BRIN

BRIN indexes are a strong candidate for very large append-oriented historical tables where timestamp or another indexed column correlates with physical row order.

BRIN does not automatically replace B-tree indexes.

Index selection depends on query patterns.

---

58. Avoid Index Explosion

Every index increases:

storage

write cost

maintenance

WAL volume

Historical tables must not receive indexes merely because a column might someday be queried.

---

59. Hot and Cold Historical Data

Historical storage may evolve into tiers:

HOT
recent, frequently queried

WARM
older, occasionally queried

COLD
research/archive

The exact age boundaries remain pending.

---

60. Cold Analytical Files

Columnar files are a strong candidate for immutable research/archive datasets.

Initial preferred candidate:

«Apache Parquet»

Parquet is ACCEPTED as a candidate format, not yet as mandatory production infrastructure.

---

61. Why Parquet

Parquet is attractive for:

column-oriented analytical reads

compression

bulk research

portable datasets

language interoperability

selective column access

It is especially suitable for immutable or append-produced analytical datasets rather than transactional application state.

---

62. Parquet Is Not Market State

Rejected:

Feature Engine
    ↓
read Parquet

during live processing.

Parquet belongs to:

research

historical analytics

archive

dataset interchange

---

63. Parquet Dataset Layout

A future layout may organize files by dimensions such as:

dataset

trading date

instrument family

event category

Exact partition layout requires research-query benchmarking.

Avoid generating huge numbers of tiny files.

---

64. Small-File Problem

Research capture should not blindly write:

one Parquet file per second

or:

one file per event

File sizing and compaction strategy must be intentional.

---

65. Object Storage

Object storage is a natural future candidate for cold/research datasets.

Examples of compatible architectural concepts include:

S3-compatible storage
cloud object storage
on-prem object storage

No provider is selected by this ADR.

---

66. Object Storage Is Not Required for MVP

Initial research may use:

local filesystem

attached storage

controlled development storage

if volume, durability and team size permit.

Do not introduce distributed object storage before it solves a demonstrated problem.

---

67. ClickHouse

ClickHouse remains:

«PROPOSED / BENCHMARK REQUIRED»

for high-volume historical analytical workloads.

It is not required for the first DataMarket implementation.

---

68. When ClickHouse Becomes Relevant

A specialized columnar analytical database becomes attractive if measured workloads demonstrate that PostgreSQL is materially inadequate for workloads such as:

billions of observations

large time-range scans

cross-instrument aggregations

feature research

event studies

interactive analytical queries

high ingestion plus analytical scans

---

69. Technology Promotion Rule

ClickHouse or another analytical database may be introduced only after:

1. representative dataset exists

2. representative queries exist

3. PostgreSQL baseline is benchmarked

4. bottleneck is identified

5. candidate technology is benchmarked

6. operational cost is considered

7. measurable advantage justifies complexity

---

70. No Database Fashion Decisions

Rejected:

market data → therefore ClickHouse

and:

real time → therefore Kafka

and:

state → therefore Redis

Technology follows requirements and measurements.

---

71. Redis

Redis is not selected as historical storage.

It may later serve:

distributed cache

Gateway state

coordination

ephemeral application data

if required.

ADR-006 remains authoritative that Redis is not the authoritative per-tick Market State.

---

72. Kafka / Message Broker

A durable event broker is not required by persistence itself.

The initial modular-monolith architecture may persist asynchronously through in-process bounded handoff.

A broker becomes justified only if requirements emerge for:

cross-process durable buffering

multiple independent consumers

replayable infrastructure streams

service extraction

failure isolation

---

73. WAL Is Not Application Event History

PostgreSQL WAL exists for database durability/recovery.

It must not be treated as DataMarket's research replay format.

Database recovery logs and market-event replay solve different problems.

---

74. Historical Schema

Historical schemas should favor:

append-oriented writes

explicit versions

explicit timestamps

explicit instrument identity

explicit provenance

efficient time-range access

Updates to historical observations should be exceptional.

---

75. Append-Oriented Model

Market observations naturally favor append-oriented persistence.

Corrections should preferably be represented explicitly rather than silently rewriting historical truth where point-in-time semantics matter.

---

76. Corrections

If a provider issues:

trade bust

correction

revised statistic

historical representation should preserve both:

original observation

correction/revision

where source semantics and licensing allow.

Replay then applies the correction at the time it became available.

---

77. Derived Market Event Persistence

Derived Market Events should preserve:

eventId

eventVersion

eventType

target

lifecycle

candidateAt

detectedAt

confirmedAt

endedAt

severity

quality

regime

MarketModelVersion

FeatureSetVersion

EventRuleVersion

evidence summary

where applicable.

---

78. Event History Is Valuable

Derived Market Events provide a compact historical representation of:

«what DataMarket believed was meaningful at the time.»

This supports:

user timeline

research

lead-time studies

false-positive analysis

model comparison

product analytics

---

79. Analytical State Persistence

Continuous Analytical State persistence is optional.

Potential strategies include:

event-driven capture

periodic snapshots

threshold-based capture

research-only full capture

No universal strategy is selected.

---

80. Feature Persistence

Features may be persisted:

around significant events

for selected research sessions

at defined intervals

for model-training datasets

rather than indiscriminately.

---

81. Event-Centered Capture

A strong future research strategy is:

             event
               │
      ┌────────┴────────┐
      ▼                 ▼
pre-event window   post-event window

capturing richer state around significant market episodes.

This is PROPOSED.

---

82. Circular Research Buffer

The live system may eventually maintain a bounded recent research buffer so that when an important event occurs it can preserve:

N seconds/minutes before event

plus subsequent observations.

This is PROPOSED and requires memory/licensing evaluation.

---

83. Pre-Event Capture

Pre-event capture must contain only information that genuinely existed before detection.

The fact that capture is triggered afterward does not permit adding future-derived information into the pre-event records.

---

84. Model Training Dataset

Training datasets, if machine learning is later introduced, must be independently versioned.

They should record:

source datasets

feature versions

label definition

label horizon

sampling

exclusions

normalization

train/validation/test periods

---

85. Labels

Predictive labels are research artifacts.

Examples:

future return

future volatility

target movement reached

They must never leak into production Feature Engine inputs.

---

86. Feature/Label Boundary

Research tooling must explicitly distinguish:

X = information available at T

Y = outcome observed after T

This boundary is fundamental.

---

87. Dataset Splitting

Time-series research should generally respect chronology.

Random row-level splitting may create leakage through temporally related observations.

Exact validation methodology belongs to research documentation rather than this ADR.

---

88. Walk-Forward Research

DataMarket research infrastructure should support chronological evaluation such as:

train
   ↓
validate later period
   ↓
move window
   ↓
repeat

when appropriate to the research question.

---

89. Research Query Isolation

Heavy analytical queries must not run against production operational tables in ways that threaten live-system reliability.

As volume grows, research workload should be isolated physically as well as logically.

---

90. Read Replicas

A PostgreSQL read replica may become useful for:

reporting

historical queries

research metadata

but is not required initially.

A replica does not automatically solve large-scale analytical storage.

---

91. Backups

Operational data requires conventional backup and recovery.

Historical/research datasets may require different protection based on:

reconstructability

cost

licensing

uniqueness

experiment importance

Not every byte necessarily requires the same backup policy.

---

92. Reconstructable Data

Some data may be reconstructable from an authoritative retained source.

Other data may be unique, for example:

what the system detected live

specific latency measurements

production event decisions

user alert decisions

Backup priority should consider reconstructability.

---

93. Disaster Recovery

Disaster recovery objectives:

RPO

RTO

remain pending until product availability requirements are defined.

No arbitrary RPO/RTO is invented.

---

94. Retention Policy

Retention must be explicit per data class.

Conceptually:

DataClass
    ↓
RetentionPolicy
    ↓
HOT duration
WARM duration
COLD duration
DELETE/ARCHIVE action

Exact durations remain pending.

---

95. Retention Is Not One Number

Rejected:

keep everything for five years

as a universal policy.

Operational accounts, raw Market Data, Derived Market Events and telemetry have different requirements.

---

96. Retention Factors

Retention decisions depend on:

licensing

regulation

research value

storage cost

privacy

reconstructability

product requirements

---

97. Deletion

Data deletion should be deterministic and auditable where required.

For time-partitioned history, partition-level lifecycle management is preferred when practical.

---

98. User Data vs Market Data

User/account data and market/research data have different privacy and lifecycle requirements.

They should not be unnecessarily coupled.

---

99. Research Dataset Access

Research datasets may contain commercially sensitive or licensed information.

Access must be controlled separately from ordinary application users.

---

100. Least Privilege

Production application, research jobs and administrative tools should use separate database/storage permissions where practical.

Example:

production runtime:
    operational read/write
    historical append

research:
    historical read
    research result write

admin:
    controlled maintenance

Exact roles remain implementation decisions.

---

101. Encryption

Sensitive persistent data should be protected:

in transit

at rest

according to deployment/security policy.

Provider credentials and secrets should not be stored as ordinary plaintext configuration rows.

---

102. Auditability

Changes to analytically significant configuration should preserve:

who/what changed it

when

previous version

new version

activation time

where applicable.

This includes:

FeatureSet

Market Model

Event Rules

research configuration

---

103. Configuration Version Activation

Historical replay must be able to distinguish:

configuration existed

from:

configuration was active in production

These are different facts.

---

104. Code Version

Research and important production decisions should be attributable to a code/build version.

Potential identity:

Git commit

build version

release version

Exact mechanism remains pending.

---

105. Schema Evolution

Historical schemas must evolve without destroying reproducibility.

Preferred principles:

version schemas

favor additive changes

retain interpretation metadata

migrate intentionally

avoid silently reinterpreting old columns

---

106. Canonical Schema Evolution

Canonical Event schema version from ADR-005 must be preserved with historical datasets.

A replay reader must know how to interpret the stored version.

---

107. Migration vs Adapter

Old datasets need not necessarily be physically rewritten whenever the canonical schema evolves.

Possible strategies:

migrate dataset

read old schema through adapter

materialize new dataset version

Selection depends on cost and compatibility.

---

108. Storage Precision

Persistence must preserve the precision required by canonical semantics.

Do not reduce:

nanosecond-capable source timestamp

to:

whole seconds

merely because a convenient database field was chosen.

---

109. Fixed-Point Values

Where canonical prices use fixed-point integer representation, historical storage should preserve:

mantissa/value

scale

or an equivalent exact representation.

Avoid unnecessary floating-point conversion at the persistence boundary.

---

110. Numeric Reproducibility

Derived floating-point feature results may be persisted when useful, but research should preferably retain enough source information to recompute important features using their versioned algorithms.

---

111. Storage Does Not Replace Algorithms

Persisted feature values are observations of an algorithm version.

They are not the definition of the feature.

The versioned Feature Engine remains the source of feature semantics.

---

112. Materialized Research Views

Frequently used historical transformations may eventually be materialized for research performance.

Examples:

1-second market states

event-centered windows

cross-market aligned observations

session summaries

These are derived datasets and must retain lineage.

---

113. Lineage

Derived datasets must be traceable to their sources.

Conceptually:

Derived Dataset
       ↓
source dataset IDs
       ↓
source versions
       ↓
transformation version

---

114. Continuous Contracts

Research may use continuous futures series.

Such series are derived artifacts.

They must explicitly record:

roll methodology

roll dates

adjustment methodology

source contracts

A continuous WDO series must not masquerade as an actual traded instrument.

---

115. Contract-Level Truth

Where possible, raw/normalized historical observations should retain actual contract identity:

WDOU26

rather than only:

WDO

Continuous symbols belong to derived research datasets.

---

116. Instrument Metadata History

Instrument metadata must be point-in-time versioned where changes affect interpretation.

Replay must use metadata appropriate to the historical period.

---

117. Calendars

Trading calendars and session definitions used by replay must also be versionable.

Changing today's holiday calendar must not silently alter an old experiment.

---

118. Time Zone

Persistent timestamps should use UTC internally where appropriate.

Exchange timezone and trading calendar remain explicit metadata.

---

119. Query APIs

Research code should access historical data through deliberate repository/dataset abstractions rather than embedding storage-engine-specific SQL throughout the analytical core.

This preserves storage evolution.

---

120. Core Independence

Rejected:

Feature Engine imports ClickHouse client

or:

Market Engine queries PostgreSQL repository

The analytical core remains storage-independent.

---

121. HistoricalStore Port

Architecture may define a conceptual:

HistoricalStore

port.

However, it should not become one giant generic abstraction pretending PostgreSQL, Parquet and future analytical databases have identical semantics.

Use purpose-specific boundaries.

---

122. Dataset Reader

Replay should consume a:

HistoricalDatasetReader

or equivalent abstraction that emits Canonical Events and metadata in deterministic order.

Exact Java API remains pending.

---

123. Dataset Writer

Research capture may use a separate:

HistoricalDatasetWriter

responsible for:

batching

schema

metadata

integrity

completion status

---

124. Completion Marker

A dataset should not be considered valid merely because files/rows exist.

Dataset lifecycle may include:

CREATING

COMPLETE

INCOMPLETE

INVALID

A completion marker/transactional metadata record is strongly recommended.

---

125. Integrity

Datasets may use:

row counts

event counts

time bounds

checksums

file hashes

sequence/gap summaries

to detect corruption or incomplete generation.

Exact mechanisms depend on storage.

---

126. Compaction

Append-oriented capture may produce fragments requiring later compaction.

Compaction must preserve:

logical ordering

timestamps

event identity

dataset lineage

and produce a new physical representation without changing logical historical truth.

---

127. Research Cache

Research tooling may use caches for expensive derived computations.

Cached results must include sufficient version identity so that:

FeatureSet v3

does not accidentally reuse results from:

FeatureSet v2

---

128. Query Result Cache

Caching must not obscure reproducibility.

A cached result is valid only for the exact dataset/configuration/version identity it represents.

---

129. Telemetry Storage

Metrics, logs and traces belong to observability infrastructure.

They should not normally share the same high-volume historical market tables.

---

130. Logs Are Not Market History

Rejected:

log every tick

and later use log files as the research dataset.

Logs describe software behavior.

Historical Market Data describes market observations.

---

131. Telemetry Retention

Telemetry retention should be shorter and operationally driven unless specific diagnostic/research needs justify otherwise.

Exact duration remains pending.

---

132. Sensitive Logging

Logs must not unnecessarily copy:

raw licensed Market Data

authentication tokens

provider credentials

proprietary feature vectors

---

133. Observability

Persistence metrics should include:

records accepted

records written

bytes written

batch size

batch latency

write throughput

queue depth

queue age

write failures

retry count

dataset gaps

dataset completion failures

storage capacity

partition count

query latency

research replay throughput

---

134. Replay Observability

Replay should measure:

events/sec

logical market time processed

wall-clock duration

speed multiplier

CPU

memory

allocation

Feature Engine latency

Market Engine latency

Event Engine latency

This also makes replay a valuable performance benchmark.

---

135. Maximum-Speed Replay

"MAX_SPEED" replay is especially valuable for:

stress testing

profiling

benchmarking

regression detection

because the same real market sequence can be driven faster than wall-clock time.

---

136. Production Capture Benchmark

Before deciding the permanent historical store, benchmark:

normal market session

high-volatility session

opening burst

macro announcement

extreme burst

multiple instruments simultaneously

---

137. Representative Queries

Storage benchmarking must include actual intended research queries.

Examples:

all WDO events for one session

WDO + DXY + US2Y around event T ± 5 minutes

feature values preceding target movement

event frequency by regime

lead-time distribution over several months

cross-market aligned observations

all candidate events that failed confirmation

---

138. Write Benchmark

Measure:

rows/events per second

MB/sec

batch latency

CPU

memory

WAL/write amplification

storage growth

index overhead

---

139. Read Benchmark

Measure:

time-range scan

single-instrument scan

multi-instrument scan

event-centered query

aggregation

research export

replay sequential read

---

140. Cost Benchmark

Storage architecture decisions must include:

disk usage

compression

backup size

cloud/object-storage cost if applicable

operational complexity

engineering cost

not only query latency.

---

141. Initial Physical Architecture

The recommended initial architecture is intentionally simple:

                 DataMarket Application
                         │
            ┌────────────┴────────────┐
            │                         │
            ▼                         ▼
       PostgreSQL              Research Storage
            │                         │
 operational data               initially optional
 derived events                 filesystem / Parquet
 research metadata
 selected history

Exact physical separation may evolve.

---

142. Initial PostgreSQL Use

Initial PostgreSQL scope may include:

users

accounts

subscriptions

entitlements

devices

configuration

instrument metadata

FeatureSet metadata

Market Model metadata

Event Rule metadata

Derived Market Events

research experiments

dataset catalog

audit information

---

143. Initial Historical Capture

Before raw long-term Market Data rights are confirmed, DataMarket development should rely on:

legally permitted provider samples

synthetic datasets

test fixtures

authorized historical datasets

explicitly permitted research captures

No architecture decision overrides licensing.

---

144. Synthetic Data

Synthetic datasets are useful for:

state-machine tests

gap handling

book behavior

feature validation

regime scenarios

event-rule testing

performance benchmarks

but cannot establish real predictive value.

---

145. Real Historical Data

Real historical data is required for empirical evaluation of:

cross-market relationships

regime stability

lead time

false positives

event usefulness

predictive hypotheses

once legal access is established.

---

146. Historical Vendor Independence

Research datasets should preserve source identity but aim to expose Canonical Events to analytical code.

This allows:

Nelogica dataset

and potentially:

another provider dataset

to drive the same analytical pipeline while retaining their different source capabilities.

---

147. Capability Metadata

Every dataset must document source capabilities.

Examples:

trades available

TOB available

MBP available

MBO available

aggressor available

source timestamp available

sequence available

snapshot recovery available

Research must not compare models as if datasets with different fidelity were equivalent.

---

148. Dataset Comparability

If one dataset contains MBO and another only MBP, a feature requiring order identity cannot be treated as equally available in both.

Feature capability rules from ADR-007 remain applicable.

---

149. Vendor-Derived Fields

If a vendor provides calculated/inferred fields, historical metadata should distinguish:

exchange-originated

provider-originated

DataMarket-derived

where known.

---

150. No Silent Provider Mixing

Historical observations from multiple providers for the same instrument must not be silently merged into one apparently homogeneous stream.

Any fusion requires an explicit methodology.

---

151. Research Event Case

The 2026-08-28 WDO macro movement is an example of a future event-study dataset.

Conceptually:

Case:
2026-08-28 WDO macro movement

Capture:
external markets
WDO
WIN
DI
macro context
Analytical State
Derived Events

Question:
Using only information available at each T,
when could DataMarket first detect
a meaningful regime/pressure transition?

The research infrastructure defined here is intended to make such experiments reproducible.

---

152. Accepted Decisions

The following are ACCEPTED:

Multi-tier persistence by data purpose

Persistence outside analytical hot path

Market State remains authoritative in memory

Asynchronous persistence

Operational PostgreSQL

Logical separation of operational/history/research/telemetry

Explicit market-data storage classification

Licensing gate before raw/normalized retention

Research Capture Policies

Versioned research datasets

Immutable completed dataset versions

Point-in-time historical truth

Preserve revisions temporally

No future knowledge in replay

Preserve multiple timestamp domains

Preserve source provenance

Database insertion order != market ordering

Dedicated Replay Engine

Production and replay share analytical logic

MarketClock for replay

Multiple replay speeds

Replay speed does not alter logical output

Deterministic replay goal

Versioned replay runs

Versioned experiments/results

Research isolated from production state

Bounded asynchronous persistence

No transaction per market tick

Batch persistence allowed

Persistence backlog observable

Dataset gaps explicit

PostgreSQL candidate for moderate historical workloads

Time partitioning candidate for large PostgreSQL history

BRIN candidate for correlated append-oriented history

Avoid index explosion

Hot/warm/cold storage concept

Parquet candidate for immutable analytical/research datasets

ClickHouse not initially required

ClickHouse requires benchmark justification

Redis not authoritative market state/history

Broker not required merely for persistence

WAL != research replay

Append-oriented historical model

Corrections preserved temporally where possible

Derived Market Event persistence

Selective Feature persistence

Explicit retention per data class

Research access control

Schema/version lineage

Storage-independent analytical core

Historical dataset reader abstraction

Dataset lifecycle/completion state

Integrity metadata

Telemetry separate from market history

Representative storage benchmarks before specialization

---

153. Proposed / Research Required

The following are PROPOSED / RESEARCH REQUIRED:

exact raw Market Data retention

exact normalized Market Data retention

PostgreSQL partition granularity

historical PostgreSQL schema

Parquet physical layout

object storage

ClickHouse

read replica

local durable spill

event-centered capture

pre-event circular research buffer

continuous futures methodology

research materialized views

dataset compaction

research cache

checkpointing

exact backup strategy

RPO/RTO

exact hot/warm/cold boundaries

---

154. Rejected Decisions

The following are REJECTED:

Database as authoritative live Market State

Feature Engine querying database per update

Market Engine querying database per evaluation

Synchronous persistence in analytical hot path

Transaction/commit per tick

Unbounded persistence queue

Silent loss of research capture

Database insertion ID as market sequence

One universal timestamp column

Silent rewriting of point-in-time history

Future data in replay

Separate independently maintained production/research formulas

Research jobs sharing unrestricted production resources

Persist every feature on every tick by default

Persist every raw provider payload by default

Assume indefinite Market Data storage rights

One retention period for every data class

ClickHouse merely because this is market data

Kafka merely because this is real time

Redis merely because state exists

PostgreSQL WAL as research event log

Log files as historical market dataset

Random technology selection before benchmarks

Raw internal storage exposed directly to clients

---

155. Pending Implementation Decisions

The following remain intentionally undecided:

exact PostgreSQL version

schema/migration tool

JDBC strategy

Spring Data usage for operational data

historical writer implementation

batch size

flush interval

persistence queue implementation

partition key/granularity

index definitions

BRIN configuration

Parquet library

Parquet compression codec

Parquet row-group sizing

object-storage provider

ClickHouse adoption

ClickHouse schema

historical retention periods

raw Market Data storage rights

normalized Market Data storage rights

feature retention

checkpoint format

dataset catalog implementation

backup tooling

disaster-recovery targets

research process deployment

continuous-contract methodology

---

156. Architectural Invariant

For every persisted analytical or market dataset, DataMarket must be capable of answering:

What is this data?

Why was it stored?

Where did it come from?

Which provider/source produced it?

Which instrument does it represent?

Which source capabilities were available?

When did the underlying information become available?

Which timestamps are source timestamps?

Which timestamps are DataMarket timestamps?

Were there known gaps?

Were there corrections?

Which schema version represents it?

Which dataset version contains it?

Is the dataset complete?

Is the dataset immutable?

Which licensing classification applies?

How long may it be retained?

Can it be replayed?

Can the analytical result be reproduced?

Which FeatureSet was used?

Which Market Model was used?

Which Event Rules were used?

Was any future information accidentally available?

Can this data be deleted or archived safely?

Can research use it without affecting production?

If these questions cannot be answered, the historical data is not sufficiently governed for trustworthy quantitative research.

---

157. Guiding Decision

«Persist deliberately, not reflexively. The real-time analytical engine owns current market truth; persistence preserves only the history required for product, research, audit and recovery purposes. Historical data must preserve temporal truth, provenance, quality, versions and licensing boundaries so that replay can reproduce what DataMarket could actually have known at each instant — never what became known afterward. Specialized storage technology will be introduced only when representative data and measured workloads prove that the simpler architecture is insufficient.»