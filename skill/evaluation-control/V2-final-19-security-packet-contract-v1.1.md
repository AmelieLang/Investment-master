# Final execution handoff: 19 securities, historical packets and 152 view cells

Version 1.1; horizon-scoring clarification added after the immutable v1.0 handoff. Scope frozen 2026-10-13 UTC. This is the self-contained current contract for data acquisition and the two historical method runs; earlier current-date and 2024/2025 proposals are superseded. The destination is `https://github.com/AmelieLang/Investment-master`. No live bot, Feishu send, trade or portfolio execution is authorized.

## 1. Fixed dates and deliverable counts

- Decision-information cutoff: `2025-12-31T23:59:59Z`. Admit facts by actual public availability, not fiscal period alone.
- Outcome-observation freeze: `2026-10-13T16:15:00Z`. Later overnight acquisition must not advance this endpoint. Expected latest fully completed closes: 2026-10-12 for US listings; 2026-10-13 for Korean/HK/mainland listings if independently verified. Actual local session/calendar and close metadata govern.
- Entry convention: each exact security's first verified regular-session open in 2026. Do not presume January 2 for all markets. Keep the future entry price out of the pre-cutoff decision packet; it belongs to the separately held outcome path.
- Custom: 19 security bundles × 3 distinct appropriately routed masters = 57 view cells, plus 19 syntheses retaining disagreement and abstention.
- Comparator: 19 × its 5 native investor personas = 95 view cells. Total: 152 logical cells, with actual model calls, native pre-model abstentions, failures and completed views counted separately.
- Model: verified Sol 6.1 for both. Unknown model/provider/settings are explicit, never silently substituted.
- This is retrospective historical replay. Today's universe/method selection and later-trained model knowledge preclude a genuine prospective or guaranteed leakage-free out-of-sample claim.

## 2. Exact requested security mapping

The following codes are acquisition targets to verify against an authoritative security master or issuer/exchange source before freezing; do not equate this planning table with completed identifier verification.

| Stable ID | Requested company/security | Target listing | Quote currency | Key boundary |
|---|---|---|---|---|
| NVDA-US | NVIDIA | NASDAQ NVDA | USD | Verify class and splits |
| AMD-US | Advanced Micro Devices | NASDAQ AMD | USD | Common shares |
| AVGO-US | Broadcom | NASDAQ AVGO | USD | Verify split-adjusted basis |
| MRVL-US | Marvell Technology | NASDAQ MRVL | USD | Common shares |
| PLTR-US | Palantir Technologies | NASDAQ PLTR, Class A | USD | Preserve Class A |
| SKHYNIX-KR | SK Hynix | KRX 000660 | KRW | Ordinary, not substituted ADR |
| TSM-ADR-US | Taiwan Semiconductor ADR | NYSE TSM | USD | Verify dated ADR-to-ordinary ratio; issuer reports in TWD |
| GOOG-C-US | Alphabet Class C | NASDAQ GOOG | USD | Do not substitute GOOGL Class A |
| AMZN-US | Amazon | NASDAQ AMZN | USD | Common shares |
| PANW-US | Palo Alto Networks | NASDAQ PANW | USD | Verify split-adjusted basis |
| MSFT-US | Microsoft | NASDAQ MSFT | USD | Common shares |
| SMIC-A-CN | Semiconductor Manufacturing International A | SSE STAR 688981 | CNY | User explicitly confirmed SMIC A; not HK 0981 |
| NOW-US | ServiceNow | NYSE NOW | USD | Verify corporate actions |
| SAMSUNG-KR | Samsung Electronics | KRX 005930 | KRW | Verify ordinary versus preferred; do not substitute 005935 |
| CAMBRICON-A-CN | Cambricon Technologies A | SSE STAR 688256 | CNY | Preserve mainland A shares |
| CRWD-A-US | CrowdStrike Holdings Class A | NASDAQ CRWD | USD | User label CROWDSTRIKE HO-A |
| ALIBABA-W-HK | Alibaba Group BABA-W | HKEX 9988 | HKD | User requested HK, not NYSE BABA ADR; reports in CNY |
| TENCENT-HK | Tencent Holdings | HKEX 0700 | HKD | Verify HK ordinary, not OTC proxy; reports in CNY |
| SNOW-US | Snowflake Class A | NYSE SNOW | USD | Preserve Class A |

Record raw user label, canonical legal issuer, ISIN or other authoritative security identifier where available, exchange MIC, listing code, class, quote currency, reporting currency, share unit and dated conversion factors. If instrument verification contradicts a proposed target, report the discrepancy before substituting.

## 3. Acquisition order and source boundaries

Use existing authorized FMP access and public issuer/regulator/exchange sources first. The parent reports authorization for low-frequency reading of the user's already accessible GS/JPM/MS/BofA terminals through the user's Chrome; that does not authorize restricted research PDF publication, new credentials or access expansion.

1. Verify instrument identities, fiscal calendars and pre-cutoff filing inventory.
2. Acquire raw annual/quarterly financials and original publication metadata. FMP is a provider input, not proof that a currently returned historical value was unrevised and public at the cutoff.
3. Resolve core figures against issuer/regulatory originals, especially restatements, share counts, FCF bridges and per-share units.
4. Build and validate historical facts and derived metrics, then freeze shared packets.
5. Separately acquire 2026 outcome prices/dividends/splits, owned by the outcome reviewer/root. Do not place those paths or post-cutoff narratives in decision-worker inputs.

Target four most recent annual periods actually published by the cutoff, plus enough quarter-spaced observations to support the baseline. Its native `build_snapshot` requests **up to 20 TTM rows**, requires at least **4 quarter-spaced TTM rows**, and needs at least **5** for its t-0/t-4 EPS-growth calculation. Four annual rows are not interchangeable with four quarterly TTM rows. Target the available 20; minimum-five usable TTM rows is desirable but unavailable rows remain missing. Raw construction of five trailing-four-quarter TTM observations generally needs eight quarters of flows, or equivalent verified annual-plus-YTD bridges. Preserve each flow's actual fiscal length and cumulative/standalone status.

Do not coerce missing quarterly disclosure into imaginary quarters. A genuinely insufficient baseline dataset should produce its native abstention and remain visibly incomplete. Distinguish a failed acquisition from a genuinely undisclosed item.

## 4. Shared historical packet schema

One immutable JSON packet per security. Fields below are normative requirements, not claims that data has been collected.

### Packet metadata

`schema_version`, `packet_id`, `security_id`, `created_at_utc`, `decision_cutoff_utc`, `packet_sha256`, `security_identity`, `source_manifest`, `company_profile_asof`, `decision_market_observation`, `annual_financials`, `quarterly_financials`, `facts`, `calculations`, `native_projection`, `uncertainties`, `point_in_time_validation`, `rights_manifest`.

### Source record

`source_id`, `url_or_access_locator`, `publisher`, `document_title`, `source_type`, `report_period`, `event_date`, `publication_datetime`, `publication_timezone`, `publication_precision`, `available_by_cutoff` (true/false/unknown), `retrieved_at_utc`, `original_or_restatement`, `supersedes_source_id`, `source_version_or_hash`, `exact_locator` (page/section/table), `access_status`, `redistribution_status`.

A date-only publication near the cutoff needs conservative timezone handling. Unknown public availability is quarantined rather than automatically passing. Retrieval today does not itself disqualify an original historical filing, but the original publication/version must be established. A restricted terminal report can support a permitted internal read; public output must disclose the public-replay gap and avoid reproducing restricted text.

### Fact record

`fact_id`, `metric`, `value` (number/string/null), `unit`, `currency`, `security_unit`, `period_start`, `period_end`, `period_type` (annual/quarter/YTD/TTM/instant), `as_of_datetime`, `accounting_basis`, `consolidation_scope`, `value_kind` (reported/derived/estimate/assumption), `source_ids`, `source_locators`, `available_by_cutoff`, `missing_reason`, `conflict_group_id`.

Null is never zero. Estimate/assumption values do not become reported data. Preserve conflicting values and explain the selected treatment. Financial amounts, shares, per-share values and ratios must have explicit units. Cash-flow flow periods and balance-sheet instants are distinct.

### Calculation record

`calculation_id`, `output_fact_id`, `formula`, `input_fact_ids`, `period_alignment`, `security_unit_alignment`, `currency_conversion_fact_ids`, `rounding`, `assumptions`, `validator_result`.

FCF must identify its CFO/capex or other bridge; EBITDA and CFO are not renamed FCF. EPS and book-value/share denominators identify basic/diluted/weighted-average/end-period shares. Market capitalization is issuer-level versus security/class-level as stated, not an unexamined ADR count multiplication.

### Company profile and market observation

The historical company profile contains only pre-cutoff supported business model, segment/customer/geographic mix, maturity, profitability/cash-generation, reinvestment/capex, balance-sheet stress, cyclicality, catalysts and risks. No 2026 success narrative, current holding, present-day classification change or later target price may enter.

The decision market observation is the latest verified regular-session price available before the decision cutoff, with its own timestamp, currency, price type and corporate-action basis. It is not the first 2026 open or the October endpoint. The gap between last known price and hypothetical execution price is evaluated later, not leaked back into the decision.

### Point-in-time validation

For every input: check actual public availability, source/version, comparable period, valid unit, restatement risk and later-data leakage. Produce explicit allowed and excluded fact-ID lists plus reasons. `historical_packet_pass=true` only if every supplied decision fact is admitted; exclusions remain outside the model packet. A provider value with unresolved historical version is missing/quarantined, not quietly accepted.

## 5. Exact native projection and known limitations

The baseline DataClient adapter may read only the shared historical packet and return a deterministic projection. It must not fetch latest-only data during prediction. Save source packet hash, projection hash, renderer hash and the exact rendered text.

Permitted company facts: `ticker`, `sector`, `industry`. The pinned native source explicitly treats latest sector/industry as a point-in-time approximation; prefer a verified pre-cutoff descriptor from the shared packet, otherwise mark the native approximation or leave missing. Do not use later company facts silently.

Permitted per-TTM-row fields from native `PeriodFundamentals`:

- `report_period`, `filing_date`
- `market_cap`, `price_to_earnings_ratio`, `return_on_equity`
- `gross_margin`, `operating_margin`, `net_margin`
- `debt_to_equity`, `current_ratio`, `revenue_growth`
- `earnings_per_share`, `book_value_per_share`, `free_cash_flow_per_share`

Rows must be newest first and quarter-spaced, with actual publication-time gates. Each projected value links to its original/derived fact IDs and field semantics. Do not insert today's market cap or ratios into a historical metrics row. Preserve the pinned baseline's choice to use the most recent filed metrics row for market cap rather than a latest-only company-facts value. If this causes information projection differences from the custom Skill, show them explicitly as a native architecture limitation.

Native derived fields `roe_avg`, `net_margin_avg`, `gross_margin_trend`, `bvps_cagr`, `debt_to_equity_latest`, `market_cap_latest`, `eps_growth_yoy` must be computed by the reviewed pinned source, with observed results logged. `size_percentile` stays null unless a verified historical compatible breakpoints table is provided; do not apply US equity breakpoints as an unlabelled global metric.

Known pinned-source issue: `_cagr` discards missing BVPS rows before estimating elapsed years from the remaining count. Gaps can therefore compress time. Preserve and flag this native behavior; do not secretly fix only the baseline or silently call its result a verified economic growth rate. A corrected formula, if tested, is a separate adapted sensitivity branch. Likewise do not relabel its uncalibrated confidence as probability.

The custom Skill may consume the richer same-packet facts under its declared contract. If the native renderer drops facts, save the exact dropped-field list. This is a transparent method-package/architecture comparison, not proof that both models literally received identical tokens. Any strict same-projected-input sensitivity is a separate preregistered test, not a replacement chosen after results.

## 6. Forbidden decision inputs and outcome ownership

Decision workers receive only the historical packet allowlist, a historical-method allowlist, exact method instructions and fixed output schema. Forbidden inputs include all 2026 security paths/returns/drawdowns, later filings/restatements that were not public, present holdings, post-cutoff broker reports, retrospective case narratives, current winner labels, prior method outputs and reviewer scores. Do not place outcome metrics in filenames, dossier summaries or transport instructions.

Current research dossiers can remain rich and up to date, but export a sanitized pre-cutoff method subset for the replay. The outcome owner calculates local-currency price/verified total return and daily-close maximum drawdown after the initial opinions are committed. Preserve raw/adjusted prices, corporate-action basis, entry/endpoint calendars and arithmetic checks. Never advance the observation freeze to October 14 Asia merely because execution continues overnight.

## 7. Baseline, Sol execution and result records

Comparator: `virattt/ai-hedge-fund`, pinned commit `78b779c1389e2d1452dc29606d2c4126d859b964`, verified MIT; star snapshots 63,955 on October 12 and updated 63,971 separately dated. Native five personas: Buffett, Graham, Munger, Lynch, Druckenmiller. Preserve original short signal/confidence/reasoning outputs and data/parse abstention behavior.

Do not pass an unrecognized `gpt-6.1-sol` CLI string into the baseline's provider fallback: the reported path can route to Anthropic. The reviewed fallback is native source prompt export → fresh verified Sol contexts → raw response archive → exact-prompt-hash offline LLMClient → native parser/predict replay. Fail closed on unknown model, mismatch or missing response; no network fallback. Archive the actual outer worker prompt and disclose message-role/settings differences. Label it native source processing with externally executed Sol calls/offline replay, not unmodified native end-to-end runtime.

Every view-cell record includes security ID, master ID, method/source version, packet and prompt hashes, route-freeze ID, requested/actual model identity, observable settings, raw response path/hash, parsed response, status, abstention/error reason, retries and separate source-calculation/model-invocation/native-orchestration execution fields. All 152 cells must be accounted for without inventing an opinion for a legitimate native gate abstention.

Keep the accepted `adapter_result_v1_1` schema unchanged. A separate research wrapper references its hash and preserves four separate quality/valuation/evidence/uncertainty panels; no universal master vote or fabricated native score.

## 8. Reporting and optional overlay

Main outputs: each security's 3 custom and 5 baseline views, matched factual/causal/uncertainty evaluation, exact limitations, and independently measured 2026 security return/drawdown. Preserve the forecast horizon on every view: a five-year scenario value or long-duration intrinsic value is not an October 2026 price target. Grade factual/causal decision quality, observed security path, any explicitly horizon-matched directional forecast, and forecast calibration separately. Mark unmatured horizons as not yet evaluable; rising prices do not establish authentic or correct reasoning. Use source-grounded analysis rather than vocal impersonation. Those stock paths are not method P&L. Do not award points merely for longer custom prose or custom-only sections the baseline never produces.

Optional per-view static long/cash illustration only if preregistered: explicit native bullish → long; bearish/neutral/abstention → separately labelled cash statuses. Custom long requires an explicit unambiguous initiate-long conclusion; quality/hold/support labels do not automatically map to buy. Otherwise mark overlay unmappable. Normalize each independent view/security to 1, use first tradable 2026 open, no rebalance/leverage/short/exit invention, zero cash interest and a disclosed frictionless primary case. Any cost grid is frozen and hypothetical. Never combine unequal viewpoint sets into a claimed skill portfolio alpha.

## 9. Immediate acquisition gate and stopping condition

Data acquisition may begin now on verified instruments and pre-cutoff public/FMP sources without waiting for all current dossiers. Do not begin opinion generation until identities, historical packets, method allowlists, routes, model transport and evaluation rules are frozen and independently preflighted. Source review must precede code acceptance. Retain max three corrective reworks per stable task.

Final completion requires all 19 identities, all 152 accounted-for view cells, validated stock paths, preserved baseline limitations, honest runtime labels and the reviewed files verified at an exact commit in AmelieLang/Investment-master. Missing data, unresolved public availability, unavailable model identity or blocked runtime remains partial/blocked, not a fabricated pass. No promise of invincibility, future alpha or investor endorsement.
