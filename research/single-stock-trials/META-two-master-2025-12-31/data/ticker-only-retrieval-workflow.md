# Minimal portable ticker-only host retrieval

## Inputs

The human supplies ticker META. The research run supplies its decision cutoff, here 2025-12-31T23:59:59Z; that is an evaluation setting, not an extra company-data burden on the human. A different date must be explicit. The host resolves Meta Platforms, Inc., Nasdaq Class A ticker META, SEC CIK 1326801, fiscal year-end December 31. Do not confuse Meta Materials or Canadian depositary receipts with this security.

## Required host capabilities

- Public web search and read/open of official HTML and PDF sources, or an equivalent SEC/IR retrieval connector
- Date/period-aware extraction, basic arithmetic and citations
- Local/context storage of a factual packet and optional output files
- A historical OHLC source distinguishing raw close from adjusted close, when valuation depends on price

Concrete tools used here were web.search_query/open/find through web__run and local file writing. Other hosts may map their equivalent tools. No proprietary finance API, paid research subscription, brokerage account, API key, executable from an unknown source, or FCFF adapter is required. Ticker-only means retrieval is done by the host after receiving the ticker; it does not mean a tool-less text model can fetch live documents.

## Retrieval steps

1. Resolve issuer and fiscal calendar from official IR/SEC. Discover dated annual/interim filing URLs, release dates and SEC filing indexes; distinguish fiscal period end, acceptance time and publication date.
2. Read the last annual filing public before cutoff and latest interim filing/release public before cutoff. For this reconstruction these are FY2024 10-K, Q3 2025 10-Q and October 29 release. FY2025 annual results published January 2026 are inadmissible even though their accounting period ended before cutoff. Read older annual comparatives where the investor method needs multiyear history; here FY2022 supplies 2020-2022.
3. Extract income, CFO, cash PPE, finance-lease principal, company FCF reconciliation, SBC, balance-sheet scope, A+B share counts and dilution, segments and disclosed operating metrics. Store each with fact ID, source URL/date, fiscal scope, units and locator. Keep missing values null/unknown and nonapplicable metrics N/A. Do not manufacture subscription retention for an advertising platform.
4. Check material events between the last quarter and cutoff. The November 3 bond offering is separately dated; it does not reveal December cash. Keep lease commitments and conditional guarantees distinct from booked debt. Do not sum overlapping commitment categories automatically.
5. Fetch raw historical close on or before cutoff. Here December 31 raw close is $660.09. Record exchange/security, timestamp/date and raw-versus-adjusted basis. If a host cannot verify price, continue business analysis, make price a variable P, and label valuation comparisons conditional.
6. Reconcile periods. Revenue and cash TTM = annual + current YTD − prior YTD. Weighted-average shares are duration averages, not additive flows. CFO less cash PPE and lease principal reproduces company FCF, not automatically owner earnings or FCFF. Explicitly classify any normalization, maintenance-capex estimate and discount rate as a method assumption.
7. Freeze one base packet and give precisely that base to each independently callable method. Use the same facts for base/enriched comparisons; only append genuine dated enrichment. Keep method analyses and valuations separate. No consensus pipeline is needed.

## Retrieval record and limitations

The accompanying facts.json and base-public-data.md show this retrieval working from the ticker for the shared evidence layer, with source links and published dates. Their existence alone does not prove either installed investor Skill invoked a retrieval tool in its own run; log those individual calls separately. No old complete-financial-model or archived-web-availability gate is imposed.

The SEC subprocess download was cancelled by automatic approval review, but official documents were read through web tools. Yahoo full-page open failed; publicly indexed historical OHLC extracts on UK and AU mirrors agree on raw close, with this limitation disclosed. No restricted access was bypassed. No market or operating outcome from 2026 is admitted.
