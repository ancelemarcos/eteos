ADR-005 — Canonical Market Event Model and Time Semantics

Status: ACCEPTED
Date: 2026-08-29
Decision scope: Canonical Market Data model, event identity, sequencing, temporal semantics, numerical representation, data quality and replay semantics
Supersedes: None
Superseded by: None

---

Terminology alignment notice (2026-08-29): Canonical implementation names, state namespaces, time-field names and cross-ADR vocabulary are consolidated in `docs/architecture/DOMAIN-LANGUAGE.md`. This notice is editorial and does not change this ADR's accepted decision semantics. Where this ADR uses a conceptual/legacy label, apply the canonical mapping only when semantics are equivalent.

---


1. Context

DataMarket consumes heterogeneous financial information from multiple providers and markets.

Potential sources include:

- B3 Market Data;
- global exchanges;
- Market Data vendors;
- interest-rate markets;
- FX markets;
- equity-index markets;
- commodities;
- volatility markets;
- economic calendars;
- news/event providers.

Each provider may represent the same fundamental concept differently.

Examples:

Provider A
    symbol = "WDOU26"
    price = 5278.500
    timestamp = ...
    sequence = ...

Provider B
    instrumentId = 123456
    px = 5278500
    scale = 3
    ts = ...

Provider C
    ticker = "WDO Sep26"
    last = "5278.5"

The analytical core cannot depend directly on those representations.

DataMarket therefore requires a canonical internal model that preserves enough source information to support:

- live processing;
- temporal ordering;
- Market State reconstruction;
- data-quality detection;
- replay;
- quantitative research;
- lead-time analysis;
- provider comparison;
- deterministic testing;
- incident investigation.

The canonical model must not destroy information that may later prove analytically important.

---

2. Decision

DataMarket will define:

«A versioned, provider-independent Canonical Market Event Model.»

Provider adapters are responsible for translating external Market Data into canonical events.

Conceptually:

B3 Binary UMDF ────┐
B3 FIX/FAST ───────┤
Global Provider ───┤
FX Provider ───────┼──► Provider Adapter
Rates Provider ────┤          │
News Provider ─────┤          ▼
Macro Provider ────┘   Canonical Events
                              │
                              ▼
                       Analytical Core

The analytical core must not require knowledge of the original transport protocol.

---

3. Fundamental Principle

Canonicalization means:

«Normalize representation without erasing source semantics.»

It does not mean:

«Convert every provider into the smallest common denominator.»

If Provider A supplies information that Provider B does not, the canonical model must be capable of preserving that information where it is relevant.

---

4. Canonical Event Envelope

Every canonical event must contain or be associated with a common envelope.

Conceptually:

CanonicalMarketEvent

schemaVersion

eventId

source
provider
feed
channel

instrumentId
eventType

sourceSequence
instrumentSequence
internalSequence

eventTime
providerSendTime
ingestionTime
processingTime

timeQuality
dataQuality

flags

payload

Not every source will populate every field.

Missing information must remain explicitly unavailable rather than fabricated.

---

5. Event Types

The canonical model should distinguish semantic event categories.

Initial categories include:

TRADE

QUOTE

BOOK_ORDER_ADD
BOOK_ORDER_CHANGE
BOOK_ORDER_DELETE
BOOK_SIDE_CLEAR
BOOK_CLEAR

BOOK_SNAPSHOT_BEGIN
BOOK_SNAPSHOT_ENTRY
BOOK_SNAPSHOT_END

STATISTICS

MARKET_STATUS
TRADING_PHASE

INSTRUMENT_DEFINITION
INSTRUMENT_STATUS

SEQUENCE
HEARTBEAT

DATA_GAP
DATA_RECOVERY
DATA_RESET

ECONOMIC_EVENT

NEWS_EVENT

DERIVED_MARKET_EVENT

These categories may evolve.

Provider-specific events must not force unnecessary provider terminology into the analytical core.

---

6. Market Data and Derived Events Are Different Domains

Raw/canonical Market Data events and DataMarket-derived analytical events must remain distinct.

Canonical Market Event
        ↓
Market State
        ↓
Feature Engine
        ↓
Market Engine
        ↓
Derived Market Event

A "TRADE" is an observation.

A "VOLATILITY_EXPANSION" is an analytical conclusion.

They must never be confused.

---

7. Event Identity

Every canonical event must have an identity suitable for:

- diagnostics;
- replay;
- duplicate detection;
- persistence correlation;
- derived-event provenance.

However:

«"eventId" must not replace provider sequencing.»

An internal UUID does not prove Market Data continuity.

---

8. Event ID Strategy

The event model should support an internal event identifier.

The identifier may eventually be:

numeric sequence
UUID
time-sortable identifier
compound identity

The exact representation will be determined during implementation.

Hot-path allocation cost must be considered.

The analytical core must not require random UUID generation for every Market Data event if a cheaper deterministic identity is sufficient.

---

9. Provider Identity

Canonical events must identify their origin.

Conceptually:

SourceDescriptor

providerId
feedId
channelId
connectionId
protocol
environment

Possible environments:

PRODUCTION
CERTIFICATION
SIMULATION
REPLAY
SYNTHETIC_TEST

Production and test events must never be indistinguishable.

---

10. Instrument Identity

Provider symbols must not be the canonical identity.

Use:

CanonicalInstrumentId

with provider mappings.

Example:

B3 securityID = 123456
Provider X symbol = WDOU26
Provider Y symbol = WDO-SEP26

             ↓

CanonicalInstrumentId

The canonical instrument record contains the semantics of the financial instrument.

---

11. Instrument Metadata

Instrument metadata may include:

instrumentId
exchange
market
assetClass
symbol
rootSymbol
contractCode
expiration
currency
priceScale
tickSize
contractMultiplier
tradingCalendar
timezone
providerMappings

Not all metadata belongs in every event.

Events should normally reference an instrument identity rather than copying the entire definition.

---

12. Instrument Definitions Are Versioned State

Instrument metadata can change.

Therefore:

«Instrument definition is state, not compile-time configuration.»

Historical replay must use instrument metadata valid at the historical instant being replayed.

Using today's instrument metadata while replaying historical Market Data may introduce incorrect results.

---

13. Price Representation

Prices in the canonical hot-path representation should preferably use:

«fixed-point integer representation»

rather than "double".

Conceptually:

priceMantissa = 5278500
priceScale    = 3

price = 5278.500

or an instrument-defined fixed scale:

priceRaw = 5278500
instrument.priceScale = 3

---

14. Why Fixed Point

Fixed-point integer representation provides:

- exact representation of decimal market prices;
- deterministic comparison;
- deterministic equality;
- efficient arithmetic;
- reduced allocation;
- predictable serialization.

Avoid relying on binary floating-point equality for market-price identity.

---

15. BigDecimal

"BigDecimal" remains appropriate for:

financial accounting
configuration
external APIs
precise decimal conversions
administrative calculations

It is not selected as the default representation for every price update in the hot path.

Creating and manipulating arbitrary-precision objects for hundreds of thousands of events may introduce unnecessary allocation and CPU cost.

---

16. double

"double" remains appropriate for many quantitative calculations such as:

returns
correlations
z-scores
regression
volatility
probabilities
normalized features
statistical models

Therefore DataMarket intentionally distinguishes:

MARKET DOMAIN VALUE
price / quantity / ticks
        ↓
exact integer/fixed-point where practical

from:

QUANTITATIVE FEATURE
correlation / variance / z-score
        ↓
double where numerically appropriate

---

17. No BigDecimal(double)

Conversion from binary floating point into decimal domain values must not accidentally introduce binary approximation artifacts.

When exact decimal conversion is required, use:

string representation
integer + scale
provider decimal representation

rather than constructing domain prices from arbitrary binary "double" values.

---

18. Tick-Based Representation

For instruments with stable tick size, DataMarket may additionally represent price movement in ticks.

Example:

currentPriceTicks
previousPriceTicks

deltaTicks =
    currentPriceTicks - previousPriceTicks

This can simplify:

- spread calculations;
- movement thresholds;
- book calculations;
- normalization across contracts.

Tick representation complements rather than necessarily replaces canonical price representation.

---

19. Quantity Representation

Quantities should use integer representation whenever provider/domain semantics permit.

Example:

long quantity

Fractional quantities require explicit scale.

Never assume all financial instruments use integer quantity.

---

20. Numerical Overflow

Fixed-point representation requires explicit overflow analysis.

The project must document valid ranges for:

price
quantity
notional
accumulated volume
sequence numbers

Multiplication such as:

price × quantity

must not silently overflow a "long".

Use wider/intermediate representation or checked arithmetic where required.

---

21. Null Semantics

Provider null values must remain distinguishable from zero.

These are different:

price = 0

and:

price = unavailable

Hot-path representation may use:

sentinel value
presence bit
event subtype

provided the representation is explicit and safe.

---

22. Time Is a Domain Dimension

DataMarket will not have one generic:

timestamp

field.

Financial events can have several different legitimate times.

These times answer different questions.

---

23. Canonical Time Model

The canonical model distinguishes at least:

eventTime
providerSendTime
ingestionTime
processingTime
publicationTime
clientReceiveTime

Additional provider-specific timing metadata may be retained when available.

---

24. Event Time

"eventTime" means:

«The best available timestamp representing when the underlying market/economic event occurred at its authoritative source.»

Examples:

trade matched at exchange
order-book mutation occurred
security status changed
economic statistic officially released

For B3 matching-engine events this may map to "transactTime" when the provider semantics establish that meaning.

---

25. Provider Send Time

"providerSendTime" means:

«The time at which the provider/exchange reports publishing or sending the data.»

This is not the same as event time.

Conceptually:

eventTime
    │
    │ exchange processing
    ▼
providerSendTime

The difference may represent part of exchange/provider processing latency.

---

26. Ingestion Time

"ingestionTime" means:

«The instant DataMarket observes the event entering the controlled ingestion boundary.»

This timestamp must be captured as close as practical to receipt.

Avoid assigning ingestion time after:

deserialization
normalization
queueing
business processing

if an earlier capture point is available.

---

27. Processing Time

"processingTime" means:

«The time DataMarket's analytical processing begins or completes a defined stage.»

Rather than one ambiguous processing timestamp, latency instrumentation may capture stage-specific timing.

Example:

ingestion
normalizationStart
normalizationEnd
marketEngineStart
marketEngineEnd
publication

These detailed measurements need not all exist inside the canonical domain object.

They may belong to an associated telemetry structure.

---

28. Publication Time

"publicationTime" means:

«The instant derived intelligence becomes available to an external DataMarket consumer boundary.»

This allows measurement of:

eventTime → publicationTime

and:

ingestionTime → publicationTime

which answer different performance questions.

---

29. Client Receive Time

Where clients report it, "clientReceiveTime" represents:

«The time the client application received the DataMarket publication.»

This enables approximate end-to-end measurements.

It must not be blindly compared with server timestamps unless clock synchronization quality is understood.

---

30. B3 PUMA Time Mapping

For B3 PUMA Market Data, provider semantics must be preserved.

Relevant concepts include:

T5
    matching-engine transaction/book event time

T10
    Market Data message assembly time for applicable
    statistical messages

T11
    time immediately before publication of the
    Market Data packet to UDP multicast

When available:

B3 transactTime
        ↓
canonical eventTime

B3 packetHeader.sendingTime
        ↓
canonical providerSendTime

Provider-specific timestamps not directly mapped into canonical semantics may be retained as source metadata.

---

31. Do Not Rename Without Understanding

A provider field named:

timestamp

must not automatically map to:

eventTime

The adapter must document the actual provider semantics.

Similarly:

sendingTime
transactTime
entryTime
receivedTime

are not interchangeable.

---

32. UTC Internal Timeline

Absolute timestamps inside DataMarket should be normalized to an UTC-based instant representation where source semantics permit.

Business display timezone is separate.

Example:

Internal:
2026-08-28T13:02:15.123456789Z

Display São Paulo:
2026-08-28 10:02:15.123456789

Analytical calculations must not depend on UI timezone.

---

33. Trading Timezone

Each market/instrument must also retain its authoritative trading timezone/calendar.

For B3 this is relevant for:

trading session boundaries
business dates
holidays
expiration
opening/closing phases

Do not derive trading date solely from UTC calendar date.

---

34. Trading Date

A canonical event may require a:

tradingDate

or equivalent session identity.

This is distinct from:

UTC date

An overnight market session may cross civil-date boundaries.

Session semantics belong to the exchange calendar.

---

35. Timestamp Precision

Canonical timestamp representation must preserve provider precision whenever practical.

If the provider supplies nanosecond-resolution timestamps, DataMarket must not truncate them to milliseconds during normalization.

Avoid:

nanoseconds
     ↓
milliseconds
     ↓
database

unless the loss is deliberate and documented.

---

36. Precision Is Not Accuracy

A timestamp containing nine decimal digits does not imply nanosecond accuracy.

DataMarket must distinguish:

resolution
precision
accuracy

Provider documentation determines what guarantees are actually available.

---

37. Time Quality

Timestamp metadata should eventually support a quality classification.

Conceptually:

EXCHANGE_AUTHORITATIVE
PROVIDER_AUTHORITATIVE
LOCALLY_CAPTURED_SYNCED
LOCALLY_CAPTURED_UNVERIFIED
SYNTHETIC
ESTIMATED
UNKNOWN

Exact enum names may change.

This becomes especially important when comparing events from different sources.

---

38. Clock Synchronization

Production hosts should eventually maintain synchronized wall clocks.

Possible mechanisms include:

NTP
PTP
cloud/provider time synchronization

depending on infrastructure and latency requirements.

Clock synchronization quality must be monitored.

---

39. Wall Clock vs Monotonic Clock

DataMarket requires two distinct concepts.

Wall Clock

Answers:

«What absolute instant is it?»

Used for:

event timestamps
ingestion timestamps
publication timestamps
logs
cross-system correlation
historical records

Monotonic Clock

Answers:

«How much time elapsed locally?»

Used for:

processing duration
queue residence duration
timeouts
benchmark latency
internal stage timing

These must not be confused.

---

40. Java Wall Clock

Java "Instant" / "Clock" may represent absolute application time.

However:

«Nanosecond representation does not guarantee nanosecond clock accuracy.»

Therefore DataMarket must never infer clock quality from Java type precision alone.

---

41. Java Monotonic Time

Local elapsed-duration measurements should use a monotonic source such as:

System.nanoTime()

rather than subtracting wall-clock timestamps.

Preferred:

start = monotonicNow()
...
elapsed = monotonicNow() - start

Avoid:

elapsed =
    Instant.now() - previousInstant

for internal performance measurement.

---

42. Why Monotonic Time Matters

Wall clocks may be adjusted by:

NTP correction
manual clock changes
virtualization
system synchronization

Elapsed-duration calculations must not become negative or distorted because civil time changed.

---

43. MarketClock

The analytical core will use an explicit time abstraction.

Conceptually:

interface MarketClock {

    Instant currentInstant();

}

Exact API remains implementation-specific.

Production may use a real clock.

Replay uses event-controlled time.

Tests use deterministic time.

---

44. Performance Clock

Latency measurement should use a separate monotonic abstraction.

Conceptually:

interface MonotonicClock {

    long nanoTime();

}

Do not overload "MarketClock" with both absolute-time and elapsed-time semantics.

---

45. Three Clock Domains

DataMarket therefore recognizes at least:

SOURCE / MARKET CLOCK

    when provider says something occurred


DATAMARKET WALL CLOCK

    when DataMarket received/published it


LOCAL MONOTONIC CLOCK

    how long local processing took

These domains answer different questions.

---

46. Clock Correlation

A difference such as:

ingestionTime - eventTime

is meaningful only to the degree that the two wall clocks are synchronized and semantically comparable.

Therefore it should be treated as:

observed source-to-ingestion delay

rather than unquestioned physical network latency.

---

47. Internal Sequence

DataMarket should assign an internal processing sequence where useful.

Conceptually:

internalSequence

This sequence represents DataMarket processing order within a defined ordering domain.

It does not replace:

provider sequence
instrument sequence

---

48. Provider Sequence

Provider sequence values must be preserved whenever supplied.

They are required for:

- gap detection;
- duplicate detection;
- recovery;
- diagnostics.

Never discard them after normalization.

---

49. Multiple Sequence Domains

A provider may expose more than one sequence.

For example:

packet/channel sequence
instrument report sequence
order priority sequence
application sequence

These are different semantic concepts.

The canonical model must not collapse them into one generic:

sequence

---

50. B3 Sequence Mapping

For B3 Binary UMDF, DataMarket must preserve at least the relevant semantics of:

Packet SequenceNumber
RptSeq
LastRptSeq
SecondaryOrderID
SequenceVersion

where present and relevant.

They serve different purposes.

---

51. Channel Sequence

A channel/packet sequence can indicate transport continuity.

Conceptually:

100
101
102
104

indicates a possible missing packet/message domain.

The adapter/recovery layer must react according to provider rules.

---

52. Instrument Sequence

An instrument-level sequence such as B3 "RptSeq" can detect missing incremental updates for an instrument.

Example:

WDO:
6998
6999
7001

The gap cannot be ignored merely because another channel-level sequence appears valid.

---

53. Order Priority Identity

A field used to express book priority must not be treated as transport sequence.

For B3 MBO, "secondaryOrderID" carries order identity/priority semantics.

Its meaning belongs to book reconstruction, not generic transport continuity.

---

54. Duplicate Detection

Duplicate detection must use provider-specific semantics where available.

Do not assume:

same timestamp = duplicate

Multiple legitimate events may share the same timestamp.

Do not assume:

same price + quantity = duplicate

Multiple identical trades/orders may legitimately occur.

---

55. Ordering

Canonical processing must explicitly distinguish:

SOURCE ORDER
EVENT-TIME ORDER
INGESTION ORDER
PROCESSING ORDER
PUBLICATION ORDER

These orders may differ.

---

56. No Universal Global Order

Events arriving from independent providers do not have a naturally authoritative total order.

Example:

DXY Provider
US Treasury Provider
B3 Provider

may have:

- different clocks;
- different network delays;
- different timestamp precision;
- different batching behavior.

DataMarket must not fabricate certainty that does not exist.

---

57. Merge Semantics

When multiple independent feeds are merged, DataMarket should process them according to:

arrival/processing order

while preserving their authoritative event timestamps.

Algorithms may then reason about temporal proximity using source times and freshness.

---

58. Do Not Globally Sort Live Events by Event Time

The live engine should not generally hold events indefinitely attempting to produce a perfect global event-time order.

Doing so would add latency and still could not guarantee correctness because future packets may arrive late.

Instead:

process available information
+
preserve timestamps
+
measure lateness
+
apply algorithm-specific tolerance

---

59. Optional Reordering Window

Specific algorithms may define a bounded reordering window if research demonstrates value.

Example:

accept events up to X milliseconds late

This is an algorithmic decision.

There is no global reordering window in this ADR.

---

60. Out-of-Order Events

The system must detect and classify out-of-order events where ordering semantics exist.

Possible behavior:

accept
ignore
apply correction
trigger recovery
mark degraded

depends on event/provider semantics.

No silent correction is allowed.

---

61. Late Events

A valid event arriving late is different from a duplicate or corrupted event.

Canonical metadata should allow later research to identify:

eventTime
ingestionTime
lateness

This may reveal provider/network quality and prevent false analytical conclusions.

---

62. Data Quality Is Part of the Event Model

Canonical events must carry or inherit data-quality state.

Possible dimensions include:

VALID
STALE
GAP_DETECTED
RECOVERING
RECOVERED
OUT_OF_ORDER
DUPLICATE
SUSPECT
INVALID
SYNTHETIC

A single enum may not ultimately be sufficient; bit flags or structured quality metadata may be more appropriate.

---

63. Quality Flags

Multiple conditions may exist simultaneously.

Example:

RECOVERED
+
LATE
+
SOURCE_TIMESTAMP_UNVERIFIED

Therefore the implementation should support composable quality attributes rather than assuming every event has exactly one quality state.

---

64. Invalid Data

Provider payload validation should occur before corrupted data reaches analytical state.

Examples:

invalid instrument
invalid sequence
impossible price encoding
negative quantity where prohibited
malformed timestamp
unsupported schema version

Invalid events should generate diagnostics and quality events.

---

65. Schema Version

Every persisted/replayed canonical event representation must be associated with a schema version.

Example:

schemaVersion = 1

This enables future evolution without silently changing historical meaning.

---

66. Provider Schema Version

Provider schema version and DataMarket canonical schema version are separate.

Example:

provider:
B3 Binary UMDF 2.3.1

canonical:
DataMarket Market Event Schema 1

Both may be required for diagnostics.

---

67. Schema Evolution

Canonical schema evolution should prefer:

additive compatible changes

where practical.

Breaking semantic changes require explicit version transition.

A field must never silently change meaning while retaining the same schema semantics.

---

68. Unknown Provider Fields

Adapters should tolerate provider schema evolution according to the provider's compatibility rules.

Unknown optional fields should not necessarily stop processing.

Unknown required semantics affecting correctness should fail explicitly.

---

69. Market State Reconstruction

The canonical model must contain enough information to reconstruct required Market State from:

snapshot
+
subsequent incremental events

where the provider supports this model.

This is particularly important for order-book processing.

---

70. Snapshot Is Not an Ordinary Incremental Event

Snapshot data must be explicitly distinguishable.

Conceptually:

SNAPSHOT_BEGIN
SNAPSHOT_ENTRY...
SNAPSHOT_END

or an equivalent atomic representation.

The state engine must know when a coherent snapshot has been completed.

---

71. Snapshot Consistency

A partially received snapshot must never be presented as a complete LIVE book.

State should transition conceptually:

UNAVAILABLE
     ↓
RECOVERING
     ↓
SNAPSHOT_BUILDING
     ↓
SYNCHRONIZING_INCREMENTALS
     ↓
LIVE

---

72. Recovery

Recovery is part of Market Data semantics, not merely networking.

When a gap is detected:

gap
 ↓
state quality degraded
 ↓
provider recovery procedure
 ↓
snapshot/replay
 ↓
incremental reconciliation
 ↓
validated state
 ↓
LIVE

The exact procedure depends on provider.

---

73. B3 Recovery Semantics

For B3 feeds, adapter behavior must respect official recovery rules involving:

incremental stream
snapshot recovery stream
TCP Replayer where applicable
SequenceNumber
RptSeq
LastRptSeq

DataMarket must not invent a generic recovery algorithm that contradicts provider semantics.

---

74. Recovery Provenance

Recovered events should remain identifiable as recovered/replayed source data when the provider exposes this information.

Research may need to distinguish:

received live

from:

received through recovery

even when both describe the same market event.

---

75. Book Model

Order-book state must not be reconstructed from trade messages unless the provider specification explicitly requires it.

Book mutation events and trade events have distinct semantics.

The provider adapter/book engine must follow exchange rules.

---

76. MBO and MBP

Canonical representation must not assume all providers expose the same book depth model.

Possible models:

MBO
Market By Order

MBP
Market By Price

TOB
Top Of Book

The canonical model should preserve the level of information actually supplied.

Do not manufacture MBO from MBP.

---

77. Book Side

Book events must explicitly identify side:

BID
ASK

Avoid boolean representations such as:

true = buy
false = sell

that obscure semantics.

---

78. Book Action

Canonical book mutation semantics should explicitly represent actions such as:

ADD
CHANGE
DELETE
DELETE_THRU
CLEAR

where applicable.

Provider adapters map native update actions into these canonical operations.

---

79. Trade Model

Canonical trade events should be capable of representing:

instrument
price
quantity
eventTime
tradeId where available
aggressor side where authoritative
conditions
source sequences
correction/bust relation

Do not infer aggressor side merely because the provider does not supply it unless an explicit analytical inference is being made.

---

80. Observed vs Inferred Fields

Canonical source events must distinguish:

OBSERVED

from:

INFERRED

Example:

If the exchange provides aggressor side:

OBSERVED

If DataMarket derives aggressor side from quote position:

INFERRED

Inferred information belongs to derived processing or must carry explicit provenance.

---

81. Trade Corrections and Busts

Trade cancellation/bust/correction events must not be represented as ordinary new trades.

They require explicit semantics so historical statistics can be corrected.

---

82. Market Status

Market phase/state events are first-class events.

Examples:

PRE_OPEN
OPEN
AUCTION
HALTED
RESERVED
CLOSED

Exact states are exchange-specific and may map into a canonical state plus provider metadata.

Algorithms must know whether ordinary trading conditions apply.

---

83. Session Boundaries

Session start/end/reset must be explicit.

Stateful calculations must define behavior at:

start of session
auction transition
market close
contract rollover
trading-date transition

Do not rely on process restart to reset analytical state.

---

84. Heartbeats

Heartbeat/sequence messages are operational Market Data events.

They may not modify price state but are important for:

connection health
feed liveness
sequence continuity
freshness

A feed can be alive even when no trades occur.

---

85. Liveness vs Activity

These are different:

NO MARKET ACTIVITY

and:

DEAD FEED

Heartbeat/provider sequencing is required to distinguish them where supported.

---

86. Freshness

Freshness must be evaluated per source/instrument/domain.

A global:

marketIsLive = true

is insufficient.

Example:

WDO        LIVE
WIN        LIVE
DI         LIVE
DXY        STALE
US2Y       LIVE
NEWS       UNAVAILABLE

Derived intelligence must account for affected dependencies.

---

87. Freshness Thresholds

Freshness thresholds may differ by source.

Example:

high-frequency Market Data
        ≠
economic calendar
        ≠
news

Thresholds must be configurable and semantically justified.

---

88. Dependency Freshness

A derived feature must know whether its dependencies are trustworthy.

Example:

WDO       LIVE
DXY       STALE
US2Y      LIVE

Then:

ExternalDollarPressure

must not automatically remain fully LIVE.

Quality propagates through the analytical graph.

---

89. Provenance

Derived intelligence must eventually be traceable to its relevant inputs.

This does not require storing every source event forever.

Conceptually:

Derived Event
    │
    ├── algorithmVersion
    ├── featureVersions
    ├── source states
    ├── observation window
    └── data quality

This supports explainability and research.

---

90. Event-Time Windows

Quantitative windows must explicitly state which time domain they use.

Example:

5-second return

could mean:

5 seconds of event time

or:

5 seconds of processing time

These are not interchangeable.

Market analytics should generally use market/event-time semantics where appropriate.

---

91. Processing-Time Windows

Processing-time windows may be appropriate for operational concerns such as:

queue rate
throughput
timeout
health monitoring

They must not silently substitute for event-time quantitative windows.

---

92. Replay Principle

Historical replay must preserve original canonical event semantics.

Replay changes:

delivery schedule

not:

historical eventTime
provider sequence
source identity
market semantics

---

93. Replay Clock

During replay:

MarketClock.currentInstant()

should advance according to replay event time or explicitly defined simulation semantics.

Algorithms must not accidentally observe today's wall clock.

---

94. Replay Speed

Replay speed may be:

REAL_TIME
2X
10X
100X
MAXIMUM
STEP

Analytical output must not change merely because wall-clock replay speed changes, unless the algorithm explicitly depends on processing-time behavior.

---

95. Deterministic Replay

Given:

same canonical input
same order
same algorithm versions
same configuration
same MarketClock semantics

the engine should produce the same logical analytical outputs where practical.

This is a critical DataMarket property.

---

96. Look-Ahead Prevention

Replay infrastructure must make future data inaccessible to analytical code.

At replay instant:

10:02:15

the engine must not be able to query:

10:02:16+

through:

database
precomputed candle
daily aggregate
future revised value

This must be enforced architecturally.

---

97. Candle Data

Candles are derived data.

A candle such as:

10:02:00 → 10:02:59

is not fully known at:

10:02:20

Research must never provide the completed candle to an algorithm operating at 10:02:20.

---

98. Economic Events

Economic releases require temporal semantics beyond a single timestamp.

Potential fields include:

scheduledTime
actualReleaseTime
providerReceiveTime
DataMarketIngestionTime

expectedValue
actualValue
previousValue
revision

The scheduled time and actual publication time are different concepts.

---

99. Economic Revisions

Historical macroeconomic datasets may contain revised values.

Replay must use:

«the value available at that historical instant»

rather than the latest revised value.

Otherwise look-ahead bias is introduced.

---

100. News Events

News also requires multiple temporal concepts.

Potentially:

eventOccurredTime
publisherTime
providerTime
ingestionTime

Not every source supplies all of them.

DataMarket must not fabricate missing timestamps.

---

101. Unknown Time

If source event time is unavailable:

eventTime = unavailable

is preferable to pretending:

eventTime = ingestionTime

The latter destroys provenance.

An analytical fallback may explicitly choose ingestion time, but the underlying source model remains honest.

---

102. Time Fallback Policy

Algorithms may define:

use eventTime if authoritative
else providerSendTime
else ingestionTime

if appropriate.

But this is an explicit algorithm policy.

Canonicalization itself must not silently merge these fields.

---

103. Lead Time

DataMarket's lead-time research requires precise temporal semantics.

Conceptually:

T_external
    external condition observable

T_detection
    DataMarket detects condition

T_target
    target market movement begins

Potential measurements:

processing latency =
    T_detection - T_ingestion

observed lead time =
    T_target - T_detection

These metrics must state which clocks and timestamps they use.

---

104. Causal Claims

Timestamp precedence alone does not prove causality.

Example:

DXY moves
    ↓
20 ms
    ↓
WDO moves

supports temporal precedence.

It does not by itself prove:

DXY caused WDO

The event model must preserve evidence without encoding causal conclusions into source events.

---

105. Storage Representation

Persisted timestamps should preserve sufficient precision for the original source.

Avoid database schemas that automatically truncate:

nanoseconds → milliseconds

without deliberate justification.

Storage technology must be evaluated for actual precision guarantees.

---

106. Serialization

External serialization formats must preserve:

integer precision
timestamp precision
sequence precision
null semantics
schema version

JavaScript clients require special attention to integers larger than the exact safe integer range of JavaScript "Number".

Do not blindly serialize every "long" as JSON numeric value.

---

107. Client Representation

Clients do not necessarily need every canonical field.

The Client Gateway may publish a purpose-specific representation.

Example:

Internal Canonical Event
        ↓
Intelligence
        ↓
Client DTO

Do not expose internal provider sequencing or proprietary details unless the product requires them.

---

108. Canonical Model Is Internal

The canonical event schema is not automatically a public API contract.

Internal evolution requirements differ from external client compatibility requirements.

---

109. Hot-Path Representation

The logical canonical schema and physical hot-path representation need not be identical.

Example:

Logical:
CanonicalTradeEvent

Physical:
preallocated ring-buffer slot
primitive fields

The architecture defines semantics.

Implementation may optimize representation without changing meaning.

---

110. Avoid Strings in Hot Path

Frequently repeated categorical values should preferably use:

numeric IDs
enums
interned/static metadata references

rather than allocating repeated strings.

Example:

Prefer:

instrumentId = 1842

over copying:

"WDOU26"

into every event.

---

111. Avoid Generic Maps

The hot-path canonical model must not use generic structures such as:

Map<String, Object>

for ordinary Market Data fields.

Use strongly typed schemas.

Generic extension metadata may exist outside the critical representation where necessary.

---

112. Avoid Reflection-Based Processing

Per-event analytical processing should not depend on reflection for ordinary field access.

Explicit typed access provides:

- better performance;
- compiler safety;
- clearer semantics.

---

113. Event Immutability

Logical canonical events should be treated as immutable once published into analytical processing.

If physical ring-buffer slots are reused, ownership rules must guarantee that consumers do not retain references beyond slot lifetime.

This distinction must be documented carefully.

---

114. Event Ownership

At every hot-path stage, ownership of mutable event storage must be explicit.

Avoid retaining:

ringBufferEventReference

after the sequence has been released.

If downstream asynchronous consumers require the data, create an appropriate stable representation.

---

115. Derived Event Stability

Derived events sent across asynchronous boundaries should generally be stable/immutable representations.

This prevents later mutation of Market State from altering previously published conclusions.

---

116. Canonical Schema Testing

Provider adapters require contract tests.

Given provider input:

known raw message

the adapter must produce:

expected canonical event

including:

price
quantity
instrument
timestamps
sequences
flags
quality

---

117. Golden Market Data Samples

Where licensing permits, the project should maintain representative sanitized or authorized samples for adapter testing.

Examples:

trade
new order
change order
delete
trade bust
auction
session change
gap
snapshot recovery
heartbeat

Provider PCAP/sample files may also be used according to applicable rights.

---

118. Temporal Tests

Tests must include:

same timestamp / multiple events
out-of-order arrival
late event
clock adjustment
session boundary
UTC date transition
local timezone transition
gap and recovery
replay at different speeds

---

119. Precision Tests

Tests must verify:

decimal prices
tick conversion
large sequence values
large quantities
overflow boundaries
nanosecond timestamp preservation
serialization round-trip

---

120. Data Quality Tests

Tests must prove that:

gap

does not silently remain:

LIVE

and that recovery only restores LIVE after coherent state has been established.

---

121. Canonical Event Example

Conceptual example:

CanonicalTradeEvent

schemaVersion:
    1

source:
    B3

feed:
    BINARY_UMDF

channel:
    DERIVATIVES_x

instrumentId:
    <canonical WDO contract id>

eventType:
    TRADE

price:
    mantissa = 5278500
    scale = 3

quantity:
    10

eventTime:
    2026-08-28T13:02:15.123456789Z

providerSendTime:
    2026-08-28T13:02:15.123470000Z

ingestionTime:
    2026-08-28T13:02:15.124010000Z

providerSequence:
    ...

instrumentSequence:
    ...

dataQuality:
    VALID | LIVE

provenance:
    OBSERVED

Values are illustrative.

---

122. Derived Event Example

DerivedMarketEvent

type:
    EXTERNAL_PRESSURE_CHANGE

target:
    WDO

detectedAt:
    ...

marketEventTime:
    ...

severity:
    HIGH

algorithmVersion:
    ...

quality:
    LIVE

dependencies:
    WDO LIVE
    DXY LIVE
    US2Y LIVE
    WIN LIVE

evidence:
    structured feature contributions

This is fundamentally different from a source Market Data event.

---

123. Data Lineage

The architecture should allow the conceptual lineage:

Provider Packet
      ↓
Canonical Event
      ↓
Market State
      ↓
Feature v3
      ↓
Market Model v7
      ↓
Derived Event
      ↓
Alert

This does not imply that every intermediate object must be permanently stored.

It defines traceability semantics.

---

124. Performance Constraint

Canonicalization must be benchmarked as part of the hot path.

Measure:

decode latency
canonicalization latency
allocation rate
events/sec
p99/p99.9 latency

A beautifully generic model that cannot sustain required Market Data rates is unacceptable.

---

125. Correctness Constraint

Performance optimization must not discard:

timestamp semantics
sequence semantics
quality
source provenance
instrument identity
precision

without explicit justification.

A faster model that destroys analytical evidence is also unacceptable.

---

126. Accepted Decisions

The following are ACCEPTED:

Provider-independent canonical model

Versioned canonical schema

Strongly typed events

Canonical instrument identity

Provider provenance preserved

Multiple timestamp domains preserved

eventTime != providerSendTime
          != ingestionTime
          != processingTime
          != publicationTime

UTC-based absolute internal timeline

Trading timezone/calendar preserved separately

Provider timestamp precision preserved

Wall clock separated from monotonic clock

MarketClock abstraction

Monotonic performance clock

Provider sequences preserved

Multiple sequence domains preserved

No fabricated global event ordering

No silent event-time fallback

Fixed-point integer prices in hot path
where domain permits

double for appropriate quantitative features

BigDecimal not default per-tick representation

Explicit null semantics

Explicit data-quality semantics

Explicit snapshot/recovery semantics

Live and replay share canonical semantics

Look-ahead prevention

Derived events separate from observed events

Observed vs inferred provenance

Canonical model internal, not automatically public API

---

127. Explicitly Rejected

The following are REJECTED:

one generic timestamp field

one generic sequence field

double as universal price identity

BigDecimal for every hot-path field

Map<String,Object> canonical events

provider symbol as canonical instrument identity

silently replacing missing eventTime with ingestionTime

globally sorting all live providers by eventTime

assuming nanosecond resolution means nanosecond accuracy

using wall clock for local elapsed-time measurement

using today's clock during replay

using completed future candles during historical replay

treating recovered state as LIVE before synchronization completes

silently ignoring sequence gaps

assuming connected socket means fresh Market Data

mixing inferred analytics with observed source data

---

128. Pending Implementation Decisions

The following remain open:

exact Java class hierarchy

sealed interfaces vs records vs mutable transport structs

event ID representation

internal sequence representation

exact fixed-point abstraction

sentinel vs presence-bit null representation

canonical schema serialization format

persistent event representation

database timestamp representation

canonical schema registry strategy

exact MarketClock API

monotonic clock abstraction implementation

provider-specific adapter structures

reordering policy for specific algorithms

event retention policy

raw Market Data retention rights

These require implementation benchmarks, provider selection and licensing clarification.

---

129. Architectural Invariant

For any market observation, DataMarket should be able to answer where information exists:

WHAT happened?

WHICH instrument?

WHERE did the information come from?

WHEN did the market/source say it happened?

WHEN did the provider send it?

WHEN did DataMarket receive it?

IN WHAT ORDER did the provider send it?

IN WHAT ORDER did DataMarket process it?

WAS the feed trustworthy?

WAS the event live, late, duplicated or recovered?

WHAT numerical precision did the source provide?

WAS the value observed or inferred?

If the canonical model cannot answer these questions, information may have been lost too early.

---

130. Guiding Decision

«Never trade temporal truth for modeling convenience. Preserve what happened, where it came from, when it happened, how it arrived, in what sequence it belonged, and how trustworthy that information was. Everything DataMarket learns later depends on getting these facts right first.»