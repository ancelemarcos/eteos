ADR-010 — Real-Time Publication, Client Gateway and WebSocket Protocol

Status: ACCEPTED
Date: 2026-08-29
Decision scope: Real-time publication, Client Gateway, WebSocket communication, subscriptions, snapshot/incremental protocol, sequencing, reconnection, gap recovery, backpressure, slow clients, authentication boundary, mobile delivery boundary and protocol evolution
Supersedes: None
Superseded by: None

---

Terminology alignment notice (2026-08-29): Canonical implementation names, state namespaces, time-field names and cross-ADR vocabulary are consolidated in `docs/architecture/DOMAIN-LANGUAGE.md`. This notice is editorial and does not change this ADR's accepted decision semantics. Where this ADR uses a conceptual/legacy label, apply the canonical mapping only when semantics are equivalent.

---


1. Context

The analytical pipeline established by ADR-004 through ADR-009 is:

Market Data Sources
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

This pipeline is intentionally server-side.

Clients must now receive useful real-time information without:

- consuming raw market-data feeds unnecessarily;
- knowing proprietary analytical formulas;
- interfering with analytical processing;
- depending on perfect network connectivity;
- requiring complete event replay after reconnection;
- receiving thousands of irrelevant internal updates;
- mistaking transport state for market state.

DataMarket therefore requires a publication architecture between the analytical core and:

Mobile
Web
Desktop

The architectural problem is not merely:

«How do we open a WebSocket?»

It is:

«How do we expose continuously changing analytical truth to unreliable and heterogeneous clients while preserving correctness, freshness, ordering, scalability and isolation?»

---

2. Decision

DataMarket will implement a dedicated:

«Client Gateway»

responsible for delivering current analytical intelligence and Derived Market Events to authenticated and authorized clients.

Conceptually:

Analytical Core
      │
      ├── Analytical State
      └── Derived Market Events
              │
              ▼
       Publication Boundary
              │
              ▼
      ┌──────────────────┐
      │  CLIENT GATEWAY  │
      └────────┬─────────┘
               │
       ┌───────┼─────────┐
       ▼       ▼         ▼
     Mobile    Web     Desktop

The initial real-time client transport will be:

«WebSocket over TLS — WSS»

for foreground/live applications.

Mobile background notification will use:

«Push Notification»

through the appropriate platform delivery infrastructure.

WebSocket and Push solve different problems and will not be treated as interchangeable transports.

---

3. Architectural Boundary

The Client Gateway is not part of the quantitative analytical core.

Correct dependency:

Analytical Core
       ↓
Publication Port
       ↓
Client Gateway
       ↓
Transport

Rejected:

Market Engine
       ↓
WebSocket session

and:

Event Engine
       ↓
Flutter client

The analytical core must not know:

WebSocket
Flutter
browser
APNs
FCM
JSON
mobile connection

---

4. Client Gateway Responsibilities

The Client Gateway is responsible for:

connection management

authentication integration

authorization / entitlement enforcement

subscriptions

protocol negotiation

snapshot publication

incremental publication

sequence tracking

connection liveness

client backpressure

slow-client handling

rate/conflation policy

reconnection support

protocol versioning

transport serialization

operational telemetry

It is not responsible for calculating market intelligence.

---

5. Publication Port

The analytical system will expose information to publication infrastructure through explicit application/core boundaries.

Conceptually:

AnalyticalSnapshot
DerivedMarketEvent
DataQualityChange

enter:

Publication Port

and become transport-specific representations only afterward.

The core must not create WebSocket DTOs directly.

---

6. Publication Is Asynchronous

Client publication must not block:

Market State

Feature Engine

Market Engine

Event Engine

A slow client must never increase analytical processing latency.

Conceptually:

Event Engine
      ↓
Derived Event
      ↓
bounded async publication
      ↓
Client Gateway

---

7. No Client Backpressure Into Market Engine

This is an architectural invariant.

Rejected:

Slow Mobile Client
        ↓
WebSocket send blocks
        ↓
Publication blocks
        ↓
Event Engine blocks
        ↓
Market Engine blocks

Correct:

Analytical Core
       ↓
bounded publication boundary
       ↓
Client Gateway
       ↓
per-client delivery control

Client overload is handled at or after the publication boundary.

---

8. WebSocket

WebSocket is selected for foreground real-time communication because DataMarket requires:

persistent connection

low-overhead incremental messages

server → client streaming

client → server commands

subscriptions

liveness detection

The selected application protocol runs over:

WSS

in production.

Plain "ws://" is not acceptable for Internet production traffic.

---

9. WebSocket Is a Transport

WebSocket itself does not provide DataMarket's application semantics.

DataMarket must define:

authentication semantics

subscription semantics

snapshot semantics

sequence semantics

message types

gap recovery

protocol versioning

error semantics

above WebSocket.

---

10. Application Protocol

DataMarket will define a versioned real-time application protocol.

Conceptually:

DataMarket Realtime Protocol
            ↓
         WebSocket
            ↓
           TLS
            ↓
           TCP

The protocol must remain sufficiently independent that another transport could theoretically implement the same logical semantics later.

---

11. Protocol Version

Every connection must operate under an explicit compatible protocol version.

Conceptually:

protocolVersion = 1

Protocol version is distinct from:

Canonical Event schema version

FeatureSet version

MarketModel version

EventRule version

---

12. Version Negotiation

The client and server must establish a compatible protocol version during connection establishment or initial protocol handshake.

If no compatible version exists:

connection rejected

with a machine-readable reason where practical.

Silent incompatible interpretation is prohibited.

---

13. Message Envelope

Application messages should share a stable logical envelope.

Conceptually:

RealtimeMessage

protocolVersion

messageType

messageId

streamId

sequence

serverTime

payloadVersion

payload

Additional fields may be introduced when implementation requires them.

---

14. Message Types

Initial logical message types may include:

WELCOME

AUTHENTICATED

SUBSCRIBE

SUBSCRIBED

UNSUBSCRIBE

SNAPSHOT

STATE_UPDATE

MARKET_EVENT

DATA_QUALITY

HEARTBEAT

ERROR

RESYNC_REQUIRED

The exact wire representation remains an implementation decision.

---

15. Control vs Data Messages

The protocol distinguishes:

CONTROL MESSAGES

from:

DATA MESSAGES

Control examples:

SUBSCRIBE
UNSUBSCRIBE
RESYNC_REQUIRED
ERROR

Data examples:

SNAPSHOT
STATE_UPDATE
MARKET_EVENT

This separation improves protocol clarity and evolution.

---

16. Snapshot + Incremental Model

The fundamental client synchronization model is:

«Snapshot followed by incremental updates.»

Conceptually:

connect
   ↓
authenticate
   ↓
subscribe
   ↓
SNAPSHOT
   ↓
STATE_UPDATE
   ↓
STATE_UPDATE
   ↓
MARKET_EVENT
   ↓
...

---

17. Snapshot Defines Current Truth

A snapshot represents a coherent view of the current publishable state for a subscription.

Example:

WDO

Current analytical state
Active events
Data freshness
Connection/data quality
Relevant context
Versions

The snapshot is not merely a collection of arbitrary recent messages.

---

18. Reconnection

After connection loss:

Client
   ↓
reconnect
   ↓
authenticate
   ↓
resubscribe
   ↓
receive coherent snapshot
   ↓
resume incremental updates

The client does not need every message it missed while disconnected to understand the current market state.

---

19. Why Snapshot Recovery

Consider:

client disconnects at 10:00

pressure strengthens
pressure confirms
pressure weakens
pressure ends

client reconnects at 10:03

Replaying every transition may be unnecessary for the live UI.

The client primarily needs:

What is true now?

Historical event timeline is a separate capability.

---

20. Snapshot Is Not Historical Replay

These remain separate:

REAL-TIME SYNCHRONIZATION
    snapshot + incrementals

HISTORICAL TIMELINE
    persisted event/history query

The real-time protocol must not require the historical database to recover current state.

---

21. Snapshot Consistency

A snapshot must represent a coherent publication state.

It must not accidentally combine:

pressure from version 100

with:

confirmation from version 97

when those values are expected to belong to one coherent analytical view.

Snapshot construction must therefore respect state/version boundaries defined by the analytical system.

---

22. Snapshot Version

Snapshots should contain sufficient version information for clients to reason about subsequent updates.

Conceptually:

snapshotVersion

or equivalent stream/version metadata.

---

23. Incremental Updates

After snapshot synchronization, clients receive only material changes relevant to their subscription.

Example:

STATE_UPDATE

target = WDO

pressure:
    BUILDING → STRONG

The exact delta representation remains pending.

---

24. Full-State vs Delta Update

Incremental publication may use:

partial delta

or:

small complete component state

depending on component semantics.

The implementation should prefer correctness and recovery simplicity over saving a few bytes prematurely.

---

25. Streams

Publication is logically organized into streams.

Examples:

WDO analytical state

WDO market events

WIN analytical state

global context

system/data quality

A stream defines an ordering domain for published messages.

---

26. Stream Identity

Each stream requires stable logical identity:

streamId

Example conceptually:

market:WDO:state
market:WDO:events
context:global

Exact naming is pending.

---

27. Publication Sequence

Each ordered stream must expose a monotonically increasing:

sequence

for published application messages.

Example:

101
102
103
104

This is a DataMarket publication sequence.

---

28. Publication Sequence Is Not Provider Sequence

Never confuse:

B3 packet sequence

B3 RptSeq

internal analytical sequence

eventVersion

publication sequence

They represent different ordering domains.

ADR-005 remains authoritative for source sequence semantics.

---

29. Gap Detection

If a client receives:

sequence 101

sequence 102

sequence 105

it knows that:

103
104

were not observed.

The client must not silently assume synchronization remains valid.

---

30. Gap Recovery

On a detected gap, the client should normally:

mark stream unsynchronized
        ↓
request/resubscribe for snapshot
        ↓
receive current snapshot
        ↓
resume incrementals

rather than attempting arbitrary reconstruction.

---

31. RESYNC_REQUIRED

The server may explicitly send:

RESYNC_REQUIRED

when it knows the client can no longer safely continue from its current stream state.

Examples:

client backlog exceeded

server discarded conflatable updates

subscription changed materially

protocol state lost

---

32. Sequence Does Not Guarantee Durable Replay

Publication sequence provides:

ordering
gap detection
synchronization support

It does not automatically imply:

durable event log

or:

replay every sequence forever

Those are separate architectural concerns.

---

33. Delivery Semantics

The real-time protocol does not promise exactly-once delivery.

Clients must tolerate:

duplicate messages

reconnection

repeated snapshots

late network delivery

where applicable.

---

34. Idempotency

Where messages represent event revisions:

eventId + eventVersion

provides logical idempotency.

State updates additionally use stream/version semantics.

---

35. Client Must Not Regress State

If the client currently holds:

event E100 version 5

and receives:

event E100 version 4

it must not regress to the older state.

Similarly, obsolete state updates must be rejectable through appropriate version/sequence semantics.

---

36. Subscription Model

Clients explicitly subscribe to the information they require.

Conceptually:

SUBSCRIBE

targets:
    WDO
    WIN

streams:
    analyticalState
    events
    dataQuality

The exact request schema remains pending.

---

37. Server-Side Subscription Filtering

Filtering must occur server-side.

Rejected:

server sends every instrument
client discards 99%

This wastes:

bandwidth
CPU
battery
serialization
mobile data

and can create licensing/security problems.

---

38. Subscription Authorization

A subscription request is subject to:

authentication

entitlements

product plan

instrument permissions

data licensing constraints

A valid authenticated connection does not automatically grant every stream.

---

39. Subscription Acknowledgement

Successful subscription should produce explicit acknowledgement:

SUBSCRIBED

followed by synchronization state/snapshot.

Clients must not infer successful subscription merely because the socket remains open.

---

40. Authentication Boundary

Authentication occurs at the external application boundary.

The analytical core remains unaware of user credentials.

Conceptually:

Client
   ↓
Authentication
   ↓
Client Gateway
   ↓
authorized subscriptions

---

41. Short-Lived Credentials

Real-time connections should use short-lived authentication credentials or session mechanisms compatible with the broader security architecture.

Long-lived permanent secrets embedded in clients are prohibited.

---

42. Authentication Tokens

The exact token mechanism remains a security implementation decision.

A likely architecture is:

HTTPS authentication
       ↓
short-lived access token
       ↓
WebSocket authentication

but this ADR does not mandate JWT specifically.

---

43. Avoid Credentials in URLs

Sensitive bearer credentials should not normally be placed in WebSocket query strings because URLs may be captured by:

reverse proxies

access logs

monitoring systems

diagnostics

Preferred authentication mechanisms must minimize credential exposure.

---

44. Browser Constraints

Browser WebSocket APIs impose different connection/header capabilities from native applications.

Therefore authentication design must work across:

Flutter native

browser

desktop

without weakening security.

The exact handshake mechanism will be selected during protocol implementation.

---

45. Origin Validation

Browser-facing WebSocket endpoints must enforce appropriate Origin validation and cross-site protections.

Authentication alone must not be assumed to eliminate cross-site WebSocket risks.

---

46. Authorization Is Continuous Enough

Authorization must not exist only at login time.

Changes such as:

subscription revoked

plan expired

user disabled

entitlement changed

must eventually affect active real-time access according to security policy.

Exact propagation mechanism remains pending.

---

47. Connection Lifecycle

Conceptually:

DISCONNECTED
     ↓
CONNECTING
     ↓
CONNECTED
     ↓
AUTHENTICATING
     ↓
READY
     ↓
SUBSCRIBED
     ↓
SYNCHRONIZED

Failures may transition to:

RECONNECTING
UNAUTHORIZED
DEGRADED

Exact client state machine may evolve.

---

48. Connection != Data Live

A WebSocket connection can be healthy while upstream market data is stale.

Therefore clients must separately display:

TRANSPORT STATUS

and:

MARKET DATA STATUS

Example:

WebSocket: CONNECTED

WDO Data: STALE

This distinction is mandatory.

---

49. Heartbeat

WebSocket Ping/Pong or an equivalent application-level liveness mechanism will be used to detect dead connections and keep intermediaries aware of active connections.

Heartbeat intervals are operational configuration, not hard-coded architectural constants.

---

50. Protocol Ping/Pong vs Market Heartbeat

Do not confuse:

WebSocket Ping/Pong

with:

Market Data heartbeat

WebSocket Ping/Pong answers:

«Is the network peer responsive?»

Market Data heartbeat answers:

«Is the market-data source alive/current?»

Both are needed.

---

51. Idle Infrastructure

Load balancers, proxies and mobile networks may terminate apparently idle connections.

Heartbeat configuration must therefore be compatible with:

proxy idle timeout

load balancer timeout

mobile network behavior

server timeout

Exact values require deployment testing.

---

52. Reconnection

Clients must automatically reconnect after unexpected connection loss.

Reconnection should use:

exponential backoff

with:

jitter

to avoid reconnect storms.

---

53. Reconnect Storm

After server restart or network recovery, thousands of clients may attempt reconnection simultaneously.

Jitter and controlled retry policies are required to prevent:

thundering herd

behavior.

---

54. Reconnection Is Normal

Mobile connectivity changes routinely because of:

Wi-Fi ↔ cellular

radio suspension

network handoff

temporary signal loss

device sleep

The protocol must treat reconnection as expected behavior rather than exceptional failure.

---

55. Session Continuity

Initial architecture prioritizes:

fast resynchronization

over preserving an indefinitely resumable transport session.

A reconnect may create a new connection/session and restore state through subscriptions + snapshots.

---

56. Mobile Foreground

When the mobile application is active:

WebSocket

is the primary real-time channel.

It provides:

live analytical state

Derived Market Events

data-quality state

interactive subscriptions

---

57. Mobile Background

DataMarket must not depend on maintaining a WebSocket continuously while the mobile application is backgrounded or suspended.

Operating systems control background execution.

Therefore:

foreground
    → WebSocket

background / suspended / closed
    → Push Notification

is the architectural model.

---

58. Push Is a Wake/Attention Channel

Push is primarily used to tell the user:

«Something relevant occurred.»

It is not the authoritative synchronization mechanism for current analytical state.

---

59. Push Payload

Push payloads should remain small.

Conceptually:

eventId
eventVersion
target
eventType
severity
short presentation metadata

The app should obtain authoritative current state after activation.

---

60. Push Does Not Replace Snapshot

When the user taps a notification:

Push
   ↓
open app
   ↓
authenticate/restore session
   ↓
WebSocket connect
   ↓
subscribe
   ↓
SNAPSHOT

The push payload is not assumed to contain current complete market truth.

---

61. Push Is Best-Effort

Push delivery must not be treated as:

exactly once

perfectly ordered

guaranteed immediate

Therefore the analytical system must never use push receipt as proof that an event was delivered or seen.

---

62. Push Deduplication

Notification processing should use:

eventId
eventVersion

or another stable notification identity to reduce duplicate presentation.

---

63. Alert Decision vs Delivery

Maintain separate timestamps:

eventDetectedAt

alertDecisionAt

notificationQueuedAt

notificationProviderAcceptedAt

clientReceivedAt

where available.

This allows us to measure where latency actually occurred.

---

64. Client Update Rate

The analytical engine may process information at much higher frequency than a human interface can usefully render.

Therefore:

backend processing frequency

is independent from:

client publication frequency

which is independent from:

UI rendering frequency

---

65. Conflation

For current-state updates, intermediate values may sometimes be conflated.

Example:

pressure 41
pressure 42
pressure 44
pressure 47
pressure 51

A slow client may only need:

pressure 51

provided synchronization/version semantics remain correct.

---

66. Events Are Different From State

Conflation policy differs by message semantics.

CURRENT STATE
    may often be conflatable

SIGNIFICANT DERIVED EVENT
    may require explicit delivery semantics

A "PRESSURE_STARTED" event cannot automatically be treated like an obsolete UI value.

---

67. Conflation Must Be Intentional

Every publication type must define whether it is:

LOSSLESS_REQUIRED

CONFLATABLE

RECONSTRUCTABLE_FROM_SNAPSHOT

BEST_EFFORT

or an equivalent explicit policy.

There is no global drop policy.

---

68. Slow Client

Each connection must have bounded outbound buffering.

Unbounded:

client outbound queue

is rejected.

Otherwise one slow device can consume unbounded server memory.

---

69. Slow-Client Policy

When a client cannot keep up, the Gateway may:

conflate state

drop obsolete conflatable updates

mark resync required

disconnect pathological client

according to message semantics and configured policy.

---

70. Never Slow the Market Engine

The final fallback for a persistently slow client is:

disconnect client

not:

slow analytical processing

This is a critical architectural invariant.

---

71. Queue Age

Gateway monitoring must measure not only:

queue depth

but:

oldest message age

because a small queue of stale information can still represent unacceptable latency.

---

72. Publication Freshness

Messages should expose sufficient temporal metadata for clients to understand freshness.

Potential fields include:

evaluatedAt

detectedAt

publishedAt

serverTime

depending on message type.

---

73. Client Receive Time

The client may additionally record:

clientReceivedAt

using its local clock.

This is useful for telemetry but must not replace authoritative server/source times.

---

74. Clock Difference

Client/server clock differences mean:

clientReceivedAt - serverTime

must not automatically be interpreted as exact network latency unless clock synchronization assumptions are known.

ADR-005 temporal rules remain applicable.

---

75. Data Quality Publication

Clients must receive explicit market-data quality/freshness state.

Examples:

LIVE

DELAYED

STALE

RECONNECTING

UNAVAILABLE

A UI must not continue displaying stale intelligence as if it were live.

---

76. Analytical Quality Publication

Where relevant, clients may separately receive:

evidenceStrength

dataQuality

modelReadiness

model/domain status

according to product design.

These must not be collapsed into one misleading percentage.

---

77. Client Truth Model

A client should conceptually maintain:

Connection State

Subscription State

Synchronization State

Current Snapshot State

Active Derived Events

These are distinct.

---

78. Synchronization State

A stream may be:

UNSUBSCRIBED

SYNCING

SYNCHRONIZED

GAP_DETECTED

RESYNCING

or equivalent.

A client with a live socket but unsynchronized stream must not pretend its state is current.

---

79. Initial Connection

Preferred sequence:

1. Open WSS

2. Authenticate / establish identity

3. Server accepts protocol

4. Client sends subscriptions

5. Server validates entitlements

6. Server acknowledges subscription

7. Server sends coherent snapshot

8. Client marks stream synchronized

9. Incremental updates begin

---

80. Race Between Snapshot and Incrementals

The implementation must explicitly prevent a race where:

snapshot captured
       ↓
updates occur
       ↓
client receives updates incorrectly around snapshot

and loses changes.

Snapshot synchronization must establish a precise sequence boundary.

---

81. Snapshot Sequence Boundary

Conceptually:

snapshot represents stream through sequence 500

SNAPSHOT
    baseSequence = 500

next incremental:
    sequence = 501

This makes synchronization deterministic.

---

82. Buffered Synchronization

One implementation strategy may temporarily buffer post-snapshot changes while snapshot serialization occurs.

Another may use immutable publication state/versioning.

Exact mechanism remains pending.

The invariant is:

«No update may disappear between snapshot state and incremental delivery.»

---

83. Subscription Change

Changing subscriptions may require new synchronization.

Example:

WDO only
   ↓
add WIN

The newly added stream must receive its own coherent snapshot before being considered synchronized.

---

84. Unsubscribe

After successful unsubscribe, the server should stop publishing that stream to the client.

Already in-flight messages may exist and must be safely ignored using subscription/stream generation semantics if required.

---

85. Subscription Generation

If races around rapid subscribe/unsubscribe/resubscribe become relevant, the protocol may introduce:

subscriptionId

or:

subscriptionGeneration

to distinguish old and current subscription instances.

This is PROPOSED.

---

86. Serialization

The protocol initially prioritizes:

correctness
observability
debuggability
evolution

over premature wire optimization.

JSON is an acceptable initial candidate.

It is not permanently mandated.

---

87. JSON Initial Candidate

JSON offers:

easy inspection

easy browser support

easy Flutter support

easy debugging

simple protocol development

For the expected derived-intelligence volume, it may be entirely sufficient.

It must be benchmarked.

---

88. Binary Protocol

Binary serialization such as:

Protocol Buffers

MessagePack

custom binary

may be considered later if measurements show material benefits in:

bandwidth

CPU

allocation

mobile battery

latency

No binary protocol is selected by this ADR.

---

89. Do Not Optimize the Wrong Stream

DataMarket clients should normally consume derived intelligence rather than the raw B3 tick stream.

Therefore the external publication volume should be dramatically smaller than internal market-data processing volume.

This reduces the likelihood that highly specialized serialization is required initially.

---

90. Compression

WebSocket compression may reduce bandwidth but consumes CPU and can introduce latency/complexity.

Compression must be benchmarked against realistic message sizes before becoming default.

---

91. Large Messages

Very large WebSocket messages should be avoided.

Snapshots should remain purpose-specific.

Rejected:

send entire internal Market State

to every client.

---

92. Purpose-Specific DTOs

Client DTOs expose only what each product surface needs.

They are not serialized copies of internal canonical/domain objects.

This preserves:

security

licensing boundary

protocol stability

IP protection

payload efficiency

---

93. Raw Market Data Boundary

The Client Gateway must not accidentally become a raw Market Data redistribution mechanism.

Publication DTOs must respect licensing decisions and provider/B3 contractual restrictions.

---

94. Intellectual Property Boundary

Clients must not receive proprietary implementation details unnecessarily, including:

internal weights

complete feature vectors

model parameters

private thresholds

training artifacts

algorithm implementation

They receive intentional derived intelligence and explainability.

---

95. Explainability Without Formula Disclosure

The client may receive:

External USD pressure strengthened

Confirming:
    US rates
    global USD

Contradicting:
    domestic rates

without receiving:

w1 = 0.18372
w2 = 0.27311
...

---

96. Gateway Scalability

Client Gateway should be architecturally extractable from the main DataMarket process if client scale later requires independent scaling.

Initially it may remain in the same deployable application under ADR-002.

---

97. Same Process Initially

Initial topology may be:

┌─────────────────────────────────┐
│       DataMarket Application    │
│                                 │
│ Analytical Core                 │
│       ↓                         │
│ Publication Boundary            │
│       ↓                         │
│ Client Gateway                  │
└──────────────┬──────────────────┘
               │
              WSS

This minimizes premature operational complexity.

---

98. Future Extraction

If needed:

Analytical Backend
        ↓
publication infrastructure
        ↓
Client Gateway instances
        ↓
clients

may become a future topology.

Extraction requires a concrete scaling/fault-isolation reason.

---

99. Horizontal Gateway Scaling

Multiple Gateway instances must eventually support:

client distributed connections

consistent authorization

publication fan-out

subscription ownership

instance failure

The exact mechanism is not selected yet.

---

100. No Sticky-Session Dependency for Truth

Sticky sessions may be operationally useful, but correctness should not depend on a particular Gateway instance containing irreplaceable market truth.

Authoritative analytical truth remains upstream.

---

101. Gateway Restart

After Gateway restart:

clients reconnect
       ↓
resubscribe
       ↓
receive snapshots
       ↓
continue

The system should not require recovery of every prior WebSocket session.

---

102. Analytical Backend Restart

If the analytical backend restarts, publication readiness must reflect:

Market State rebuilding

Feature warm-up

Market Model readiness

Event Engine readiness

Clients must not be told the system is LIVE before the analytical state is actually trustworthy.

---

103. Readiness

Gateway process readiness and market-intelligence readiness are separate.

Example:

Gateway:
    READY

WDO intelligence:
    WARMING_UP

is valid.

---

104. Graceful Shutdown

During planned shutdown, Gateway should where practical:

stop accepting new work

close connections cleanly

allow clients to reconnect elsewhere

Exact close codes and deployment behavior remain implementation decisions.

---

105. Error Messages

Protocol errors must be machine-readable.

Conceptually:

ERROR

code
message
recoverable
streamId
requestId

where appropriate.

---

106. Error Taxonomy

Potential errors include:

UNAUTHORIZED

FORBIDDEN

INVALID_MESSAGE

UNSUPPORTED_PROTOCOL

INVALID_SUBSCRIPTION

RATE_LIMITED

RESYNC_REQUIRED

SERVER_UNAVAILABLE

Exact taxonomy remains pending.

---

107. Do Not Leak Internals

Client errors must not expose:

stack traces

SQL

internal hostnames

credentials

model internals

provider secrets

Detailed diagnostics belong to server observability.

---

108. Client Commands

Client-to-server messages should be narrowly defined.

Examples:

SUBSCRIBE

UNSUBSCRIBE

RESYNC

PING/application heartbeat if needed

The WebSocket connection is not a generic remote command bus.

---

109. Request Correlation

Control requests may include:

requestId

allowing responses/errors to be correlated with client requests.

---

110. Rate Limiting

Gateway must protect itself from abusive or defective clients.

Potential controls include:

connection rate

authentication attempts

subscription changes

messages/sec

snapshot requests

Exact limits are operational decisions.

---

111. Snapshot Abuse

A client must not be allowed to repeatedly request expensive snapshots at unlimited frequency.

Snapshot requests may require:

rate limiting

coalescing

server-controlled resynchronization

---

112. Connection Limits

Per-user/device/account connection limits may be introduced according to product and licensing requirements.

Exact limits remain pending.

---

113. Device Identity

Mobile push registration requires device/application-instance identity distinct from the authenticated user.

A user may have:

phone

tablet

desktop

browser

simultaneously.

Authentication identity and device identity must not be conflated.

---

114. Multiple Connections

The architecture supports multiple legitimate client connections for the same user, subject to:

product policy

security

licensing

resource limits

---

115. Security

Production real-time transport requires:

TLS

authenticated identity

authorization

input validation

message-size limits

connection limits

Origin protection for browser clients

safe error handling

credential protection

observability

---

116. WebSocket Input Validation

All client messages are untrusted input.

Validate:

message type

payload structure

field limits

subscription targets

message size

protocol version

before processing.

---

117. Message Size Limit

Both inbound and outbound protocol messages must have configured maximum sizes.

Unlimited message size is rejected.

---

118. Authentication Logging

Logs may record:

connection ID

user/account identifier where policy permits

authentication result

subscription metadata

but must not record raw bearer tokens.

---

119. Connection ID

Each WebSocket connection should have an operational:

connectionId

used for:

logging

metrics

diagnostics

lifecycle tracking

It is not necessarily a security credential.

---

120. Observability

Gateway metrics should include:

active connections

connection attempts

authentication failures

subscriptions

messages published

bytes published

messages received

snapshot count

snapshot latency

resync count

sequence gaps

outbound queue depth

outbound queue age

conflated updates

dropped messages by explicit policy

slow-client disconnects

reconnect rate

WebSocket send latency

serialization latency

with controlled cardinality.

---

121. End-to-End Latency

Where practical, DataMarket should measure stages such as:

eventDetectedAt
        ↓
publicationAcceptedAt
        ↓
serializedAt
        ↓
socketWriteAt
        ↓
clientReceivedAt

subject to clock-domain limitations.

This helps distinguish analytical latency from publication/network/UI latency.

---

122. Client Telemetry

Clients may optionally report coarse telemetry such as:

connection quality

received sequence

resync occurrence

render latency

app version

protocol version

subject to privacy/product policy.

Telemetry must not become required for market correctness.

---

123. UI Rendering

Clients should separate:

network receive

from:

state application

from:

UI rendering

A high message rate should not trigger unnecessary full-screen rebuilds.

---

124. Flutter Consideration

If Flutter is selected by a future client-technology ADR, it should maintain a client-side state layer between:

WebSocket

and:

widgets

so that transport events do not directly control widget rendering.

Flutter itself is not selected by this ADR.

---

125. Web/Desktop

Web and desktop clients should follow the same logical synchronization semantics:

authenticate
subscribe
snapshot
incrementals
gap detection
resync

even if platform implementations differ.

---

126. Protocol Compatibility

A server deployment should support a defined compatibility window where practical.

The exact policy may be:

current protocol

previous protocol

or another version strategy.

No specific compatibility window is accepted yet.

---

127. Additive Evolution

Protocol evolution should prefer additive compatible changes where practical.

Clients must tolerate unknown optional fields.

Breaking semantic changes require protocol/payload version changes.

---

128. Payload Version

Complex payload types may carry their own:

payloadVersion

separate from the overall transport protocol.

This permits targeted evolution.

---

129. Contract Tests

The real-time protocol requires automated contract tests covering:

handshake

authentication

subscription

snapshot

incremental update

gap

resync

duplicate

out-of-order

unsubscribe

reconnect

unsupported version

authorization failure

slow client

---

130. Client State-Machine Tests

Clients must be tested against scenarios such as:

disconnect during snapshot

duplicate snapshot

gap after snapshot

out-of-order event revision

subscription revoked

server restart

network switch

rapid reconnect

stale market data with healthy WebSocket

---

131. Load Tests

Gateway load tests should measure:

concurrent connections

subscriptions

fan-out

message throughput

serialization

memory per connection

CPU

GC

p50/p95/p99/p99.9 publication latency

slow clients

reconnect storm

snapshot storm

No production capacity number is invented before measurement.

---

132. Chaos / Failure Tests

Relevant scenarios include:

Gateway process killed

analytical backend unavailable

network partition

load balancer closes idle connections

client stops reading

client sends malformed data

authentication service unavailable

push provider unavailable

---

133. Push Provider Failure

Failure of:

FCM

or:

APNs

must not stop:

Market State

Feature Engine

Market Engine

Event Engine

WebSocket publication

Push infrastructure is asynchronous and isolated.

---

134. WebSocket Failure

Failure of the Client Gateway must not stop analytical market processing.

This follows the same isolation principle.

---

135. Publication Overload

If publication infrastructure becomes overloaded, the system must prefer:

preserving analytical correctness

over:

keeping every client update

Current state can be resynchronized.

The Market Engine cannot reconstruct processing time lost because clients blocked it.

---

136. Licensing Boundary

The Client Gateway is an important technical enforcement point for Market Data licensing.

It should support enforcement of:

authorized products

authorized users

authorized instruments

allowed derived information

display/non-display distinctions where applicable

according to final contractual requirements.

This ADR does not make the legal classification itself.

---

137. Entitlements

Entitlements should be represented independently from UI code.

Conceptually:

User
   ↓
Product Entitlements
   ↓
Allowed Subscriptions

This allows licensing/product rules to evolve without changing analytical algorithms.

---

138. No Trust in Client Filtering

Licensing/security restrictions must never depend on:

client receives forbidden data
then hides it

Unauthorized data must not be sent.

---

139. Derived Intelligence Boundary

DataMarket should publish the minimum information required to deliver useful intelligence.

The Gateway must not expose internal source events merely because they exist in memory.

---

140. Initial Wire Strategy

Initial implementation recommendation:

Transport:
    WSS

Application protocol:
    versioned DataMarket protocol

Serialization:
    JSON initially

Synchronization:
    snapshot + incrementals

Ordering:
    per-stream publication sequence

Recovery:
    resnapshot

Foreground mobile:
    WebSocket

Background mobile:
    push

Authentication:
    short-lived authenticated session/token

Slow client:
    bounded buffer + conflation/resync/disconnect

JSON remains subject to benchmark before becoming a permanent decision.

---

141. Initial Message Flow

Conceptually:

CLIENT                          SERVER

   ───── WSS CONNECT ─────────────►

   ◄──── WELCOME ─────────────────

   ───── AUTH ────────────────────►

   ◄──── AUTHENTICATED ───────────

   ───── SUBSCRIBE WDO ───────────►

   ◄──── SUBSCRIBED ──────────────

   ◄──── SNAPSHOT seq=100 ─────────

   ◄──── UPDATE seq=101 ───────────

   ◄──── EVENT seq=102 ────────────

   ◄──── UPDATE seq=103 ───────────

Exact authentication placement may differ depending on the selected security mechanism.

---

142. Gap Example

Client receives:

100 SNAPSHOT
101 UPDATE
102 EVENT
105 UPDATE

Client detects:

expected = 103
received = 105

Then:

SYNCHRONIZED
      ↓
GAP_DETECTED
      ↓
RESYNC
      ↓
SNAPSHOT baseSequence=120
      ↓
SYNCHRONIZED

No guessing.

---

143. Slow Client Example

Server produces:

pressure 41
pressure 43
pressure 46
pressure 51
pressure 55

Client cannot keep up.

For a conflatable current-state stream, Gateway may retain only:

pressure 55

and maintain valid synchronization semantics.

But if during the same interval:

PRESSURE_STARTED

occurred, its event semantics are handled separately.

---

144. Mobile Push Example

Event Engine
     ↓
WDO_EXTERNAL_PRESSURE_STARTED
     ↓
Alert Engine
     ↓
user eligible?
     ↓ yes
Push Delivery
     ↓
device notification

When user opens:

App
 ↓
WSS
 ↓
SUBSCRIBE WDO
 ↓
SNAPSHOT

The app receives what is true now rather than assuming the push still describes current market conditions.

---

145. Accepted Decisions

The following are ACCEPTED:

Dedicated Client Gateway

Client Gateway outside analytical core

Asynchronous publication boundary

Client backpressure never reaches Market Engine

WSS for foreground real-time communication

Push for background mobile attention

Push not authoritative state synchronization

Snapshot + incremental synchronization

Snapshot defines current truth

Reconnect through resubscribe + snapshot

No complete missed-message replay required for current state

Per-stream publication sequencing

Publication sequence distinct from provider sequences

Gap detection

Resnapshot as primary gap recovery

RESYNC_REQUIRED support

No exactly-once assumption

Idempotent event revisions

Explicit subscriptions

Server-side filtering

Subscription authorization

Entitlement enforcement

Connection state != market-data state

Heartbeat/liveness

Automatic reconnect

Exponential backoff + jitter

Reconnection treated as normal

Bounded client outbound queues

Intentional conflation for eligible state

Events and current state have different loss semantics

Slow clients may be disconnected

Queue age observable

Explicit data freshness publication

Snapshot sequence boundary

Protocol versioning

Purpose-specific client DTOs

No raw internal domain serialization

No proprietary model internals unnecessarily exposed

Same Gateway logical protocol across mobile/web/desktop

Gateway initially may share DataMarket deployable

Gateway extractable later

Gateway restart recovered by reconnect + snapshot

Push provider failure isolated

Gateway failure isolated from analytics

Server-side licensing/security enforcement

Contract/load/failure testing

---

146. Proposed / Benchmark Required

The following are PROPOSED / BENCHMARK REQUIRED:

JSON as initial serialization

permessage-deflate / compression

exact heartbeat interval

exact reconnect backoff

exact outbound queue size

exact conflation interval

subscription generation

exact stream taxonomy

exact snapshot representation

exact delta representation

protocol compatibility window

Gateway horizontal fan-out mechanism

client connection limits

snapshot rate limits

---

147. Rejected Decisions

The following are REJECTED:

Market Engine writing directly to WebSocket

Event Engine sending push notifications directly

Client network speed affecting analytical processing

Unbounded outbound client queues

Raw B3 tick stream as normal client protocol

Client-side filtering as security/licensing control

Push as authoritative synchronization

Assuming Push exactly-once

Assuming Push perfectly ordered

Assuming WebSocket connection means market data LIVE

Complete historical replay required after every reconnect

Exactly-once transport requirement

One global message-drop policy

Dropping significant events as if they were state updates

Blocking socket writes in analytical hot path

Permanent secrets embedded in clients

Bearer credentials casually exposed in URLs

Client DTO = internal Market State object

Client DTO = Canonical Event object

Sending proprietary model weights unnecessarily

Unlimited snapshot requests

Unlimited message sizes

Gateway instance holding irreplaceable market truth

Premature binary protocol without measurement

---

148. Pending Implementation Decisions

The following remain intentionally undecided:

Spring MVC vs WebFlux for Gateway

Spring WebSocket vs Reactor Netty vs direct Netty

exact authentication mechanism

JWT vs alternative token format

exact browser authentication handshake

exact WebSocket subprotocol name

exact JSON schema

binary protocol alternative

serialization library

stream IDs

sequence representation

snapshot construction strategy

publication queue technology

Gateway extraction timing

horizontal scaling technology

Redis involvement

broker involvement

FCM implementation

APNs implementation

Flutter selection

desktop technology

web technology

load balancer

reverse proxy

cloud provider

connection capacity targets

publication latency targets

---

149. Architectural Invariant

For every real-time client stream, DataMarket must be capable of answering:

Who is connected?

Is the connection authenticated?

What is the client authorized to receive?

What is it subscribed to?

Which protocol version is in use?

Has the client received a coherent snapshot?

Is the stream synchronized?

What publication sequence is current?

Has a gap occurred?

How is the gap recovered?

How old is queued information?

Is the client keeping up?

Which messages may be conflated?

Which messages must preserve event semantics?

Is market data actually LIVE?

What happens if the client disconnects?

What happens if the Gateway restarts?

What happens if the mobile app is suspended?

What happens if push is delayed or lost?

Can the client recover current truth without replaying everything?

Can a slow client affect the Market Engine?

Can unauthorized or licensed-restricted data leak through this stream?

If any of these answers depends on luck, implicit timing or perfect network behavior, the protocol is insufficiently specified.

---

150. Guiding Decision

«The analytical core determines market truth; the Client Gateway delivers that truth without owning it. Clients synchronize from coherent snapshots and then consume versioned incremental changes. Networks may disconnect, messages may be duplicated, clients may become slow and mobile applications may be suspended — none of these conditions may compromise analytical correctness. When synchronization becomes uncertain, DataMarket must recover current truth rather than guess it.»