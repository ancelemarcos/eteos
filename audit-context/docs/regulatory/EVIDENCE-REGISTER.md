# DataMarket / Éteos — External Evidence Register

**Status:** ACCEPTED / LIVING INDEX  
**Scope:** Repository-safe evidence that can authorize or block Market Data uses  
**Last updated:** 2026-09-14

## 1. Purpose

This register provides the auditable path from an external fact, rule or contract to a DataMarket qualification decision. It does not reproduce confidential contracts and does not constitute legal advice. It is the single repository authority for the Phase-1 public-evidence identifiers; downstream registers cite these identifiers rather than duplicating evidence records.

A technical capability, provider credential, public policy or commercial discussion is never a DataMarket entitlement or data right by itself.

Public evidence can reduce a named unknown. It does not by itself qualify an exact source or dataset, validate observed technical behavior, establish contract applicability, select a provider, or authorize DM-3A.

## 2. Evidence rule

A `PENDING` or `SOURCE_LINEAGE_DEPENDENT` cell in `DATA-USAGE-MATRIX.md` may become `ALLOWED` only when the applicable evidence is recorded here (or in an explicitly linked repository-safe compliance record) with sufficient scope to support that exact use.

For every evidence item record, where applicable:

- stable `evidenceId`;
- authority/source class (`B3`, `PROVIDER`, `OTHER_AUTHORITY`);
- public document, contract/policy reference or confidential-record locator that can be audited without committing confidential content;
- document/version/effective date;
- consultation/confirmation date;
- applicable provider/product/dataset;
- applicable uses (acquisition, retention, replay/research, model development, display, non-display, derived output, redistribution);
- explicit conclusion and limitations;
- validation state;
- reviewer/approval reference when the project governance process requires it;
- blockers resolved and blockers that remain.

## 3. Validation state

Use only:

- `UNVERIFIED` — discovered but not sufficient to authorize a use;
- `CONFIRMED` — scope/applicability have been checked and the evidence may support a usage-right decision;
- `SUPERSEDED` — newer evidence controls;
- `REJECTED` — not applicable or not sufficient.

Only `CONFIRMED` evidence can support promotion of a usage-right cell to `ALLOWED`. For public evidence, `CONFIRMED` means only that the cited public fact and its stated scope were checked on the retrieval date; it does not mean that a right, entitlement, product or dataset is qualified.

When a public item bears on a right, use one of these scoped conclusions without promoting the usage matrix:

- `PUBLIC_EVIDENCE_SUPPORTS_ALLOWED` — public text supports permission in its own stated scope, but exact applicability and entitlement still require the applicable contract/licensor/legal chain;
- `PUBLIC_EVIDENCE_SUPPORTS_PROHIBITED` — public text states a prohibition in its own stated scope;
- `PUBLIC_EVIDENCE_SUPPORTS_CONDITIONAL` — public text makes the use conditional on a category, approval, agreement or other condition;
- `PENDING_EXACT_CONTRACT`, `PENDING_LICENSOR`, `PENDING_LEGAL_REVIEW`, `UNKNOWN`, or `NOT_APPLICABLE` — the public material cannot close the applicable DataMarket conclusion.

## 4. Current register

The following official public items were retrieved and checked on **2026-09-05** or **2026-09-14**, as identified by the evidence row and the linked ProfitDLL Round-1 package. Each `CONFIRMED` state is confined to the exact fact stated in the row. All access, retention, replay, research, derived-output and publication rights in `DATA-USAGE-MATRIX.md` remain `PENDING` or `SOURCE_LINEAGE_DEPENDENT`.

| evidenceId | authority / public item | official URL | exact confirmed public fact and scope | DM-2 questions | limitations, dependencies and requalification |
| --- | --- | --- | --- | --- | --- |
| `PUB-B3-WDO-001` | B3, Mini U.S. Dollar Futures product page and contract specification | [product](https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/moedas/futuro-mini-de-taxa-de-cambio-de-reais-por-dolar-comercial.htm); [contract PDF](https://www.b3.com.br/lumis/portal/file/fileDownload.jsp?fileId=8A828D2951C9C3770152217147854FA8) | `CONFIRMED`: public WDO family metadata includes ticker `WDO`, USD 10,000 contract size, BRL per USD 1,000 quotation, BRL 0.50 per USD 1,000 minimum variation, one-contract lot and monthly maturities. | `DM2-Q002` partial | Does not identify a concrete listed contract/effective dataset or create an `InstrumentDefinition`; requalify on B3 specification change. |
| `PUB-B3-WDO-002` | B3, Foreign exchange and dollar spot trading hours | [official page](https://www.b3.com.br/en_us/solutions/platforms/puma-trading-system/for-members-and-traders/trading-hours/derivatives/foreign-exchange-and-dollar-spot/) | `CONFIRMED`: current public page observed on the retrieval date lists FUT WDO trading 09:00–18:30, pre-open beginning five minutes earlier and trade correction through 19:00. | `DM2-Q009` partial | `CURRENT_PUBLIC_FACT`, not historical-session authority and not proof of provider status delivery; recheck for every evaluated date/rule version. |
| `PUB-B3-UMDF-001` | B3, Binary UMDF Message Specification Guidelines v2.3.1, 2026-06-18 | [PDF](https://www.b3.com.br/data/files/BE/B7/9F/07/C706F910CEC024F9AC094EA8/BinaryUMDF-MessageSpecificationGuidelines-v.2.3.1-enUS.pdf) | `CONFIRMED`: B3 direct-feed specification documents security definitions, incremental/snapshot channels, `SequenceNumber` and `RptSeq`, gap/recovery procedures, trade/trade-bust and security-status messages, price/size, `sendingTime`, `transactTime`, and MBO/order-identity concepts; `TradeID` is scoped by instrument and trading date. | `DM2-Q002`, `Q005-Q009`, `Q016-Q017` partial | Applies to described Binary UMDF direct-feed semantics, not ProfitDLL or an entitled DataMarket connection. Recovery state is not a complete historical event log. Documented exceptional/manual Market Operations handling means timestamps must not be assumed to originate through one purely automated path. Requalify on protocol version. |
| `PUB-B3-MR-001` | B3, Binary UMDF Message Reference v2.3.1, 2026-06-18 | [PDF](https://www.b3.com.br/data/files/5C/B7/2E/07/C706F910CEC024F9AC094EA8/BinaryUMDF-MessageReference-v.2.3.1-enUS.pdf) | `CONFIRMED`: public field/message reference exists for the v2.3.1 Binary UMDF schema and complements the guideline semantics. | `DM2-Q004-Q009`, `Q016-Q017` partial | Direct B3 protocol reference only; exact channel, product, dataset and observed behavior remain unqualified. Requalify on schema version. |
| `PUB-B3-TS-001` | B3, PUMA Trading System Timestamps v1.0.4, 2024-12-10 | [PDF](https://www.b3.com.br/data/files/9F/05/35/01/B1F8491029BEEC39AC094EA8/B3-PUMA-Timestamps-1.0.4-enUS.pdf) | `CONFIRMED`: B3 publishes a versioned PUMA timestamp reference that distinguishes exchange timestamp concepts. | `DM2-Q005` partial | Does not establish ProfitDLL clocks, DataMarket receipt time, historical availability time or point-in-time admissibility. Requalify on timestamp-reference version. |
| `PUB-B3-FIX-001` | B3, FIX/FAST UMDF developer page and Market Data Specification v2.2.2, 2026-07-09 | [developer page](https://www.b3.com.br/pt_br/solucoes/plataformas/puma-trading-system/para-desenvolvedores-e-vendors/fix-fast-umdf/); [PDF](https://www.b3.com.br/data/files/EC/B1/9A/AD/2E86F910FC0436F9AC094EA8/UMDF_MarketDataSpecification_v2.2.2.pdf) | `CONFIRMED`: B3 maintains a public FIX/FAST UMDF specification family distinct from Binary UMDF. | `DM2-Q004-Q010`, `Q016-Q017` partial | Protocol-family evidence only; the candidate feed/product and version must be fixed before use. Requalify on specification version. |
| `PUB-B3-HIST-001` | B3, UP2DATA Available Data | [official page](https://www.b3.com.br/en_us/market-data-and-indices/data-services/up2data/available-data/) | `CONFIRMED`: WDO appears in the Currency future data family and B3 publicly lists available daily/security/open-position/consolidated information categories. | `DM2-Q001-Q002`, `Q004`, `Q010` partial | Does not establish an entitled tick-by-tick dataset, live-equivalent event semantics, delivery horizon or research rights. Exact dataset qualification remains required. |
| `PUB-B3-RIGHTS-001` | B3, Market Data Consumption Policy v1.0, current through 2026-10-31 | [PDF](https://www.b3.com.br/data/files/66/82/D8/17/973699100A29E189AC094EA8/Politica%20de%20Consumo%20Market%20Data%20B3.pdf) | `CONFIRMED`: the public policy distinguishes direct/indirect access, display/non-display and named consumption categories including distribution, trading platform, product development and internal use; use outside the applicable license requires B3 approval. Rights conclusion: `PUBLIC_EVIDENCE_SUPPORTS_CONDITIONAL`. | `DM2-Q011-Q013`, `Q017` partial | Does not assign DataMarket a category, entitlement or right. `PENDING_EXACT_CONTRACT`, `PENDING_LICENSOR`, `PENDING_LEGAL_REVIEW`. Supersede/requalify at the policy transition. |
| `PUB-B3-RIGHTS-002` | B3, Commercial policy and contracts landing page | [official page](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/distribuidores/politica-comercial-e-contratos/) | `CONFIRMED`: public page states the current policy applies through 2026-10-31 and a new policy becomes effective 2026-11-01. | `DM2-Q011-Q013` partial | Explicit time-based requalification trigger: reassess before any use on or after 2026-11-01 and whenever the page/policy changes. No right granted. |
| `PUB-B3-DIST-001` | B3, Licensed distributors | [official page](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/distribuidores/distribuidores-licenciados/) | `CONFIRMED`: B3's public list includes Nelogica for the Futures & FX segment. | `DM2-Q001`, `Q011` partial | Distributor listing is not proof of the exact ProfitDLL product, DataMarket entitlement, permitted use or downstream distribution right. Requalify when list or relationship changes. |
| `PUB-NELO-PROD-001` | Nelogica, Introdução ao Produto DLL Real Time | [official help](https://ajuda.nelogica.com.br/hc/pt-br/articles/11166353435035-Introdu%C3%A7%C3%A3o-ao-Produto-DLL-Real-Time) | `CONFIRMED`: public family description names live quotes, book and time-and-trades access and states up to 30 days of tick history for BM&F/Bovespa coverage. | `DM2-Q001`, `Q004`, `Q010`, `Q016` partial | Family description, not an exact contracted package, version, symbol entitlement or historical/live equivalence result. |
| `PUB-NELO-RUNTIME-002` | Nelogica, Ecossistema ProfitDLL e primeiros passos; retrieved 2026-09-14 | [official help](https://ajuda.nelogica.com.br/hc/pt-br/articles/22396517026203-Ecossistema-ProfitDLL-e-primeiros-passos) | `CONFIRMED`: public ProfitDLL-family documentation distinguishes Market Data and routing modes, describes Win32/Win64 native libraries, connection-state callbacks and automatic reconnect, and states that callbacks execute on a ConnectorThread whose queue is delayed when callbacks block. | `DM2-Q001`, `Q005-Q007`, `Q010`, `Q014`, `Q016` partial | Family/unversioned page only. Callback/thread behavior is evidence that delivery cadence can depend on client processing, not proof of market-arrival time, completeness, gap recovery or a specific package. The Win32/Win64 description must be reconciled with the older 64-bit-only public requirement for the exact offer. |
| `PUB-NELO-ACCESS-002` | Nelogica, Como obter acesso à ProfitDLL; retrieved 2026-09-14 | [official help](https://ajuda.nelogica.com.br/hc/pt-br/articles/51583791325211-Como-obter-acesso-%C3%A0-ProfitDLL) | `CONFIRMED`: the public access flow describes a post-contract subscription named `DLL Feed`, download archive `ProfitDLL.zip`, 32/64-bit test programs and an included PDF manual. | `DM2-Q001`, `Q014` partial | No acquisition occurred. It does not identify a DataMarket SKU/tier, entitlement, library build/interface, manual/header/changelog version, hash, exact dataset or right. |
| `PUB-NELO-INSTRUMENT-002` | Nelogica, Minicontrato e Contrato Cheio; retrieved 2026-09-14 | [official help](https://ajuda.nelogica.com.br/hc/pt-br/articles/360040136132-Minicontrato-e-Contrato-Cheio) | `CONFIRMED`: public Nelogica material describes WDO/WIN listed-contract ticker construction by family, expiry month and year, and distinguishes expiring listed contracts from aggregate/index-like study/history instruments. | `DM2-Q002-Q003`, `Q009-Q010` partial | Terminology/family evidence only. It does not establish the exact ProfitDLL provider mapping, feed/exchange codes, mapping effective intervals, symbol reuse, roll behavior or a DataMarket InstrumentDefinition. |
| `PUB-NELO-TECH-001` | Nelogica, Como requisitar trades históricos and Funções Real Time DLL | [historical trades](https://ajuda.nelogica.com.br/hc/pt-br/articles/11973319153563-Como-requisitar-trades-hist%C3%B3ricos-com-a-ProfitDLL); [real-time functions](https://ajuda.nelogica.com.br/hc/pt-br/articles/11168755650459-Fun%C3%A7%C3%B5es-Real-Time-DLL) | `CONFIRMED`: public API documentation describes `GetHistoryTrades`, historical trade/progress callbacks, `SubscribeTicker` live subscription, trade date/time, `TradeNumber`, `Price`, `Volume`, `Quantity`, `BuyAgent`, `SellAgent` and `TradeType`, with a ten-day maximum per historical request. | `DM2-Q003-Q010`, `Q015` partial | Per-request maximum is not total availability. Units, timestamp authority, flag/edit semantics, corrections, gaps, clocks, live/history parity and observed exact-version behavior require package evidence and probe. |
| `PUB-NELO-HIST-001` | Nelogica, public historical-access statements | [product page](https://ajuda.nelogica.com.br/hc/pt-br/articles/11166353435035-Introdu%C3%A7%C3%A3o-ao-Produto-DLL-Real-Time); [request page](https://ajuda.nelogica.com.br/hc/pt-br/articles/11973319153563-Como-requisitar-trades-hist%C3%B3ricos-com-a-ProfitDLL) | `CONFIRMED`: the product-family page states 30 days of tick history while the API page limits one request to ten days. | `DM2-Q004`, `Q007`, `Q010` partial | These are different concepts, not a contradiction and not completeness proof. Exact entitlement, retention horizon, gaps and historical population remain unqualified. |
| `PUB-NELO-BOOK-001` | Nelogica, real-time functions and Price Depth documentation | [real-time functions](https://ajuda.nelogica.com.br/hc/pt-br/articles/11168755650459-Fun%C3%A7%C3%B5es-Real-Time-DLL); [Price Depth](https://ajuda.nelogica.com.br/hc/pt-br/articles/50587290263835-Como-utilizar-o-Livro-de-Profundidade-Price-Depth-via-DLL-Real-Time) | `CONFIRMED`: public documentation distinguishes TinyBook top-level updates, aggregated PriceDepth levels and an offer-book interface with agent, side, position, price, quantity and add/edit/delete actions. | `DM2-Q016-Q017` partial | Does not scientifically qualify TOB/MBP/MBO completeness, sequence, recovery, participant stability or rights; optional for the first TRADE slice. |
| `PUB-NELO-VERSION-001` | Nelogica, ProfitDLL no Linux tutorial; tutorial update 2026-08-24 | [official help](https://ajuda.nelogica.com.br/hc/pt-br/articles/54973527417243-ProfitDLL-no-Linux-Saiba-como-acessar-e-utilizar) | `CONFIRMED`: the public tutorial states its binding was checked with ProfitDLL 4.0.0.41, illustrates trade fields/flags and derives an `is_edit` value from example flags. | `DM2-Q001`, `Q004`, `Q008`, `Q014-Q015` partial | `EXACT_VERSION_PUBLIC_FACT` for that tutorial example only, not the DataMarket contracted version, a contractual package/version freeze or behavioral validation. No contracted package exists. |
| `PUB-NELO-RIGHTS-001` | Nelogica, Termo de Responsabilidade do Usuário | [official page](https://www.nelogica.com.br/termo-responsabilidade-usuario) | `CONFIRMED`: public user terms state a personal/non-transferable license and restrictions on third-party use, redistribution/resale and specified generated reports/documents/databases. Rights conclusion: `PUBLIC_EVIDENCE_SUPPORTS_PROHIBITED` for the text's stated user scope and `PUBLIC_EVIDENCE_SUPPORTS_CONDITIONAL` for any different negotiated scope. | `DM2-Q011-Q013`, `Q017` partial | Applicability to a future B2B ProfitDLL/Data Solution agreement is unknown. `PENDING_EXACT_CONTRACT`, `PENDING_LICENSOR`, `PENDING_LEGAL_REVIEW`; no matrix promotion. |

## 5. Phase-1 synthesis

- The public evidence closes **0 of 18** DM-2 questions fully and reduces **15 of 18** to partial unknowns.
- `DM2-Q012` and `DM2-Q018` remain publicly unresolved; `DM2-Q014` remains not evaluated because no technical probe was authorized.
- ProfitDLL: `EXTERNAL QUALIFICATION ROUND 1 COMPLETED` / `BLOCKED` / not selected.
- B3 direct: `CONTINUE AS FUTURE CANDIDATE` / not selected.
- No source, dataset, right, technical behavior, provider mapping or real WDO instrument is qualified.
- DM-2 source/dataset qualification is not complete; DM-3A, anticipatory research and outreach/probing remain unauthorized.

## 5.1 ProfitDLL external qualification Round 1

The official-public Round-1 assessment is recorded in `../market-data/DM-2-PROFITDLL-EXTERNAL-QUALIFICATION-ROUND-1.md`. It classifies the ProfitDLL candidate for `SRC-B3-TARGET-PRIMARY` as `BLOCKED / NOT SELECTED`: exact product/version is incomplete; temporal semantics are partial; `availableAt`, corrections, batching/arrival fidelity and replay scientific fidelity remain unknown; and research, retention, replay and derived-artifact rights require recipient-specific contractual confirmation. No source, right or technical behavior is promoted, and no contact, package acquisition or probe occurred.

## 6. Confidentiality

Do not commit confidential provider contracts, credentials, private commercial terms or licensed payloads merely to satisfy this register. Store a repository-safe reference and the minimum conclusion needed for engineering governance. The authoritative confidential source must remain retrievable by the authorized project/legal process.

## 7. Gate relationship

This register is consumed by:

- `docs/regulatory/DATA-USAGE-MATRIX.md`;
- `docs/market-data/SOURCE-QUALIFICATION-REGISTER.md`;
- `docs/architecture/READINESS-STATUS.md`;
- `docs/architecture/DELIVERY-ROADMAP.md`;
- the `EXTERNAL_PUBLICATION` and `PRODUCTION` release gates.

Absence of qualifying evidence means the dependent right remains unresolved; it is never interpreted as permission.
