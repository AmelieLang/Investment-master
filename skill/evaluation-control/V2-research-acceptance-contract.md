# Multi-investor research expansion: bounded acceptance contract

Version 1.1, planning freeze 2026-10-13; roster amended from the parent's frozen execution assignment. Planning/review only; no implementation, publication, live data integration, trading, bot deployment, or Feishu sends are authorized by this document. The execution owner must separately retain the actual user authorization and chosen environment. Execution is Sol 6.1; independent planning/review is Astra as requested. Maximum three corrective rework rounds per independently scoped task.

## 1. What counts as success

Preserve the MIT finterm research backbone at commit `7235d3411601036cc79137fa0aec0d587f2c8e19` and the already-reviewed offline adapter, rather than replacing them with a giant personality prompt. Use the best auditable mechanisms from the pinned 20-project universe and the separately labelled finterm supplement. A source project's audit score or popularity is not evidence that its portrayal of an investor is true or that its strategy works.

Deliver three explicitly different levels of coverage:

1. **Canonical catalogue:** every distinct named investing/trading/valuation perspective found in the pinned top-20 source manifests. Deduplicate aliases but preserve provenance and ambiguity. Count verified implementations, filenames/mentions not fully read, historical figures, living managers, educators, VC investors and collective/anonymous personas separately. Include requested candidates outside the original universe as separately labelled extensions. Catalogue coverage is not deep-audit coverage.
2. **Ten assigned dossiers:** frozen roster is Warren Buffett, Duan Yongping, Li Lu, Cathie Wood, Ron Baron, Brad Gerstner, Philippe Laffont, Ray Dalio, George Soros and Stanley Druckenmiller. This covers Chinese, modern technology and macro perspectives. At least eight must reach deep-audit evidence gates for a useful first tranche; all ten require a returned dossier with an honest complete/incomplete status. The completed ten-dossier assignment requires all ten gates; eight passing cannot be called ten completed. Other catalogue entries, including Munger, Marks, Lynch and Templeton, are source-only/unvalidated until independently audited. The roster is a feasible first tranche, not a claim to exhaust modern investors or asset classes.
3. **Six deep case studies:** a preregistered selection across at least four audited investors, with at least three adverse/failure or thesis-invalidated cases and at least three successful cases. Include modern technology and China-linked businesses. Each case must search for pre-decision evidence; missing pre-decision evidence remains an explicit gap, never rewritten as a contemporary prediction. A greater number of lightweight anecdotes cannot substitute for these six.

Also deliver a reviewable actual `SKILL.md` orchestrator, modular master dossiers, a transparent evidence-aware fit router, a source/holdings audit assignment contract, a source-to-mechanism adoption matrix, regression fixtures, and an independent review ledger. These artifacts must remain compatible with the accepted offline package; generating them is not activation or permission to send. A research-only result may pass research gates while implementation remains unstarted. A partial result may be useful, but must name unmet gates and cannot be described as the completed expansion.

## 2. Frozen scope and catalogue reconciliation

The source universe is the existing `frozen-top20.json` plus the separately labelled finterm supplement, not all GitHub or the whole internet. Read relevant implementation bodies before treating a profile as substantive. Reconcile each source's names to stable IDs, including punctuation variants, English/Chinese aliases, surnames-only aliases, and pseudonyms. Never merge similar names without identity evidence. One investor appearing in ten repositories is one canonical person with ten source links, not ten independent methods.

Required registry fields:

- canonical ID, display name, aliases/language, person/collective/pseudonym/educator/manager role
- verified identity source and unresolved identity questions
- alive/deceased/unknown status with verification date, if used to determine research requirements
- source repo, exact commit, exact path and line/section; implementation status (`fully_read`, `partly_read`, `file_only`, `mention_only`)
- explicit method families, asset classes, business features, time horizon, geography/market, necessary inputs, documented scope exclusions
- primary-method evidence IDs and minimum evidence status
- catalogue/deep-dossier/research-ready/implementation-ready status, kept separate
- license/reuse status; original idea synthesis versus copied/adapted text or code
- former and current organization/mandate where relevant; no assumption of ongoing affiliation

All names from the prior manifests must resolve to a registry entry or a reasoned exclusion. Review excluded educators, VC figures and anonymous personas visibly; do not silently discard them or fabricate a public-equity track record. Finite success metric: 100% of extracted source-name occurrences are accounted for, with duplicate groups and unresolved identities listed. The final distinct-person count is an output of reconciliation, not a planning assumption.

## 3. Evidence contract: provenance and timing are different axes

Use independent fields rather than one confidence number.

**Provenance:** P1 = original investor writing/speech/verified account; original regulator/fund/company filing for the factual claim it actually establishes. P2 = authorized publisher transcript, faithful archive, fund-hosted republished original, with archive and speaker verification. S1 = reputable contemporaneous independent report quoting or observing the investor. S2 = later biography, interview recollection, compilation, translation or analytical reconstruction. U = unverified attribution, social repost, inaccessible or missing source. A filing proves its reported facts, not private motivation; a personal post proves a statement, not audited performance.

**Timing:** T0 = demonstrably public before the actual decision; T1 = contemporaneous within a bounded decision/holding interval but not proved pre-trade; T2 = later retrospective explanation; TU = publication/event timing unknown. Store event date, publication date, archive/upload date and retrieval date separately. A recording uploaded years later may preserve an older speech; its content time and public-availability time must not be conflated.

**Claim kind:** direct statement, regulatory holding, reported transaction, inferred method, analyst reconstruction, hypothetical application, valuation assumption or realized outcome. State the claim's scope: speaker, organization, security, position side, decision type, horizon and qualifiers.

Each substantive claim needs a source ID, precise locator/page/timestamp, a short supporting excerpt or faithful paraphrase, and an explanation of what the source cannot establish. Original-language wording must be retained where translation changes investment meaning. Later evidence may evaluate an outcome but must not enter a historical decision packet. A primary source can still be self-serving or wrong; evidence authority is not truth certainty.

No unattributed exact quotes, fabricated book-page references, invented returns, synthetic holdings, or inference promoted into a verified personal decision. Public sources and lawfully available excerpts are sufficient; full copyrighted books/memos are not to be copied into the deliverable.

## 4. Ten assigned dossiers, eight-dossier minimum first tranche and coverage disclosure

Each dossier requires:

1. Identity, career/mandate periods and bounded source search log.
2. At least three substantive source items from at least two source families, including one direct-method primary/authorized source and one practice-oriented source (holding, transaction discussion, shareholder letter, fund report or case). If unavailable after a documented search, mark the dossier incomplete rather than manufacturing the quota.
3. Causal method, decision sequence, valuation/risk/portfolio mechanisms, necessary data, falsifiers, exclusions and periods of change. Separate faithful interpretation from implementation choices. Do not invent fixed thresholds, point weights, expected returns or stop-loss rules attributed to a master.
4. Specific modern relevance and limits. A method can inspect business quality without producing a price target. A growth-oriented lens can reject an expensive technology stock; a value-oriented lens can understand and accept a technology business.
5. For each living practicing manager with public disclosures, at least two compatible dated holding snapshots when available, plus at least two tested statement/practice pairs, ideally one apparent fit and one apparent mismatch. If no legal public holdings exist, explicitly record that and use verified practice evidence without labelling it a complete portfolio.
6. A contradictions/uncertainties table and the source coverage denominator. Count sources found/read/unavailable by type; do not promise all lifetime books, speeches, posts or private positions.

Chinese investors require original-language and original-author verification where possible. A curated Xueqiu/WeChat compilation is not automatically an authenticated original post. Overseas filings may describe only one vehicle or market, not the investor's entire capital. Distinguish private personal investing from a regulated fund mandate.

## 5. Holdings-versus-comments contradiction procedure

For each pair, first establish whether comparison is valid:

- Same person or proven decision-maker? Fund/company/manager filings are not automatically the named star's personal choices. Preserve shared discretion and attribution uncertainty.
- Same security/class/vehicle, side, currency and period? Options, swaps, private stakes, ADRs and ordinary shares must not be collapsed.
- Same decision and horizon? Admiring a product, criticizing a valuation, holding a legacy stake, adding to a position and recommending a trade are different claims.
- Could statement-to-observation timing, mandate, redemptions, taxes, capacity, portfolio hedges, risk reduction, employee decisions or changed facts explain the difference? Such explanations are hypotheses unless sourced.

Record reporting period end and actual filing/publication time. Form 13F is a delayed and partial holdings disclosure: it does not disclose the full portfolio or ordinary transaction cost basis, and short equities/short options are not reported there. SEC guidance gives standard quarterly filing deadlines generally 45 days after quarter end, adjusted when applicable. Inspect actual filings and amendments rather than assuming a deadline is the filing time. Source: [SEC Form 13F FAQ](https://www.sec.gov/rules-regulations/staff-guidance/frequently-asked-questions-about-form-13f); discretion attribution fields: [official Form 13F](https://www.sec.gov/info/edgar/forms/form13f.pdf).

Outcomes are `consistent`, `apparent_tension`, `resolved_change`, `attribution_uncertain`, `not_comparable`, or `unresolved`. Strong inconsistency language requires comparable direct evidence and examination of reasonable alternatives. A missing long holding does not prove a short or negative view. The presence of a holding does not prove unlimited conviction or a profitable trade.

Do not calculate realized profit from quarter-end market-value differences. Separate security total return, fund return, trade-level P&L, reported manager estimate and reconstructed interval proxy. Any proxy needs entry/exit window, price range, corporate actions/dividends, currency, benchmark, leverage and fees treatment. If unavailable, profit is unknown.

## 6. Routing contract: choose by traits before seeing recommendations

Routing is not a popularity vote. Freeze observable inputs and candidate eligibility before viewing bullish/bearish outputs or later returns. The company/asset packet must identify asset type, security structure, business model, maturity, profitability/cash generation, reinvestment economics, cyclicality, balance-sheet stress, catalysts, valuation data, geographic/accounting constraints, requested horizon and missing facts.

Apply these steps:

1. **Asset gate:** corporate equity, bank/insurer, sovereign/corporate credit, distressed claim, commodity/futures, FX, index/portfolio, crypto or private venture. Reject formula transfers that do not match the claim type.
2. **Business and data gate:** stable cash generation, growth/reinvestment, pre-profit innovation, cyclicality/commodities, distress, event/catalyst, macro sensitivity, technical/trend data or systematic-factor data. A sector label alone is insufficient.
3. **Method eligibility:** use evidence-backed scope and required inputs. Quant/technical strategies lacking their data and execution definition can provide bounded risk questions but cannot pretend to recreate an investor's proprietary returns or signals.
4. **Primary lens:** one or two strongest fits, with positive fit rationale and specific exclusions. Ordinal eligibility or applicability scores must be labelled adapter design, never investor-native truth.
5. **Complementary challenge:** one genuinely different perspective focused on valuation, financing, cycle, execution or invalidation. Do not add similar value profiles as artificial independent votes.
6. **Requested-master override:** always preserve an explicit named-master request. Label `requested` versus `recommended` lenses. The requested lens may offer partial questions, a bounded method application, or abstention with missing evidence; supplement suitable lenses without replacing or falsifying the requested view.
7. **Synthesis:** preserve disagreement, horizons and evidence gaps. Do not average incomparable target prices, produce a universal master score, or route again to obtain a bullish conclusion. A unanimous set may still be wrong.

Illustrative route families, pending dossier verification:

- Durable profitable compounder: business economics/owner earnings/quality plus valuation and capital allocation.
- High-reinvestment or pre-profit technology: adoption/unit economics/scenario and dilution/funding analysis, with cash-flow durability and price discipline as a challenge. Technology enthusiasm alone is no eligibility criterion.
- Cyclical/commodity equity: normalized economics and balance-sheet survival, supplemented by supply/demand and cycle sensitivity. Commodity futures are a separate instrument problem.
- Credit/distress: recovery, covenants, seniority, default/refinancing and capital structure; equity owner-earnings ratios cannot be the core decision engine.
- Macro/FX/rates: regime, policy, positioning and asymmetric risk; business valuation only where an actual equity exposure is being analysed.
- Catalyst/turnaround: probability-weighted scenarios, financing and downside, only with explicit estimates and catalyst evidence.
- Banks/insurers: sector-specific capital, asset/liability risks and accounting before general quality scoring.
- Systematic/trend: reproducible rules, point-in-time data, transaction costs and drawdown controls; historical celebrity association is insufficient.

The router must support `no_eligible_method` and `insufficient_data`. The display must call an analysis a source-grounded method application, not the investor's actual current view unless a matching direct statement establishes that view.

## 7. Case selection and hindsight controls

Before detailed outcome writing, save a candidate universe, the selected six cases, selection rule and reasons for exclusions. Draw from practice evidence found during dossier work, not only celebrity best-trade lists. Choose diversity in mechanism, asset/business type, geography and outcome. Record that this is purposive case research, not a statistically representative performance study.

For each case, separate four packets:

A. **Decision context available then:** known facts, price/valuation if auditable, original thesis, identifiable decision-maker, portfolio/mandate context, disconfirming information and alternatives. Include only sources known available by the cutoff; quote the evidence boundary.
B. **Timing and attribution:** actual trade date if known, otherwise bounded entry interval; statement publication relative to entry; the difference between demonstrated pre-trade thought and a later explanation.
C. **Outcome:** dated observation endpoint, appropriate benchmark, adverse path/drawdown if defensible, realized versus unrealized versus security-return measure, and what remains unknown.
D. **Mechanism assessment:** what was predicted correctly, what failed, luck/valuation/regime/selection alternatives, what would invalidate the lesson, and whether a defensible next decision follows.

Include unsuccessful investments even when the investor describes them as mistakes, and successful investments whose thesis was partly wrong. Do not select endpoints at local peaks/troughs without a predeclared reason. No success-rate, alpha or repeatability claim from six selected cases. A retrospective anecdote may remain useful but does not satisfy a verified pre-trade-thesis gate. Report the exact number of cases with T0, T1, T2 and missing evidence. A case can pass honesty/provenance while remain incomplete for the requested pre-trade reconstruction.

## 8. Source-to-mechanism synthesis and reuse

Map the existing 20 audits to reusable mechanisms: data provenance, accounting checks, valuation bridges, financial-statement rigor, scenario design, falsifiers, original-source citations, portfolio/risk context, business classification, distinct horizons and abstention. For each proposed adoption show exact pinned source, license, strengths, known weakness, chosen adaptation and test.

Do not copy from `not_found` or `readme_claim_only` license rows. Reading to understand ideas is not permission to redistribute code or expressive text. Preserve MIT notices and attribution when adapting eligible source. Rewrite independently where necessary and retain evidence that the mechanism is grounded in original investor sources. Keep research quality scores, company quality scores and method-applicability judgments separate.

## 9. Measurable review tests

Hard-gate tests must all pass; do not hide one by averaging scores.

**Catalogue and provenance**
- C01: every source-name occurrence accounted for; no unresolved alias silently merged.
- C02: each deep dossier meets source minimums or is explicitly incomplete; all core method claims have precise supported locators.
- C03: source availability/copyright/license labels match actual access and reuse.
- C04: audited-project implementation does not count as original-master evidence.

**Attribution and chronology**
- E01: inject a post-cutoff source; historical packet rejects it while outcome packet may retain it.
- E02: unknown date stays unknown; upload/event/publication dates remain distinct.
- E03: fund 13F cannot become personal trade, exact cost basis, full portfolio or realized profit.
- E04: alleged holdings/comment contradiction lacking comparable speaker/security/horizon becomes uncertain or not comparable.
- E05: anonymous alleged young-researcher failure, mistaken book authorship and oversimplified master/asset labels remain unverified or corrected from evidence, never silently canonized.

**Routing**
- R01: mature consumer compounder, profitable technology, pre-profit technology, cyclical producer, bank, insurer, distressed debt, sovereign bond, commodity future, FX and crypto fixtures show domain-appropriate handling or abstention.
- R02: explicit Buffett + NVDA/TSLA keeps Buffett requested lens; supplemental lens is separately labelled; no claim that Buffett never invests in technology.
- R03: unknown master and insufficient company evidence do not fabricate a profile or recommendation.
- R04: two otherwise identical companies with different current prices retain the same basic method eligibility; valuation conclusions may differ.
- R05: bullish/bearish output labels and future returns are absent from route inputs. Changing them after the route freeze does not change selected lenses.
- R06: same inputs and registry version produce reproducible route; explanations reference actual traits. A low valuation, bearish conclusion or later missed gain is not by itself evidence of a wrong method.
- R07: opposition and abstention survive synthesis; no majority vote, universal master score or mandatory buy.
- R08: missing private/proprietary strategy inputs prevent a claimed Simons/quant replication.

**Cases and outputs**
- K01: six selected cases include required negative outcomes and mechanism/geography diversity; preselection log is present.
- K02: all case evidence classified T0/T1/T2/TU; ex-ante coverage denominator explicit.
- K03: security returns and manager/trade P&L are not conflated; unknown profit is null.
- K04: no cherry-picked outcome endpoint or hindsight fact enters decision context.
- K05: independent reviewer checks every core recommendation/routing rule, every material holding/contradiction and every selected case; samples additional catalogue claims and escalates systematic errors.

**Existing adapter nonregression if implemented**
- Preserve existing separate quality, valuation, evidence and uncertainty panels, null handling, unit/currency/security-class checks, chronology gate, deterministic calculations, HTML/input safety and offline no-network/no-send/no-trade constraints.
- Run existing tests plus new router/registry fixtures on the exact final commit. Distinguish tests run, passed, failed and blocked.
- No live bot, Feishu sending, trading, production deployment or external communication appears in the diff or executable path.

## 10. Review and maximum-three-rework ledger

Freeze task IDs before implementation: V2-A catalogue/reuse map; V2-B ten assigned dossiers/holdings audit; V2-C six cases; V2-D router/specification/tests; V2-E implementation/nonregression only if separately authorized. The parent has assigned V2-B as fundamental, technology and macro workstreams and a separate identity check; retain distinct stable IDs and the same per-task cap. A task's scope may be split before execution for parallel ownership, but must not be renamed/reset to evade its rework ceiling.

For each submission capture task ID, artifact path/hash or exact commit, scope version, author/model, reviewer/model, review date, review number, defects with evidence and severity, pass/fail/partial verdict, and changes required. Initial independent review is review 0. Each subsequent corrective submission is rework 1, 2 or 3; a failed third rework ends acceptance attempts for that task and produces a clear unresolved-defect report. Clarify this convention to the parent before work if a stricter three-total-submission interpretation is desired.

One consolidated defect list per review, prioritizing blockers over polish. Blockers include wrong identity, invented/false-attributed evidence, lookahead, unlicensed copying, fabricated profit, recommendation-shopping, misleading full-coverage claims and any live-send/trade regression. Major defects include missing mandatory evidence/fixtures or mismatched units. Minor presentation issues do not justify endless rounds.

Stop when all agreed deliverables and hard gates pass, when a third corrective rework still fails, or when a verified source/access/authorization blocker prevents the required evidence. Preserve useful passed work and name the remaining gap. Never call missing evidence a pass solely to meet an overnight deadline.

## Review receipt expectations

Return a concise summary first, then artifact paths/links, frozen roster and counts, evidence limits, unresolved blockers, exact validation commands/results if code exists, and the current review ledger. Historical research and offline fixtures do not establish predictive skill, profitable trading, a complete private portfolio or the investor's endorsement.

## 11. Orchestrator acceptance shape

The proposed skill package must include, whether as separate files or clearly separated sections:

- Main SKILL.md: purpose, permitted inputs, offline/non-executing boundary, routing sequence, evidence collection handoff, output contract, abstention and explicit-master override.
- Canonical registry: source-to-canonical-name mapping and eligibility state. `catalogue_only` and `unvalidated` entries must not be invoked as research-ready master agents.
- Modular dossiers: exact method evidence, operational questions, prerequisites, conflicts, inference labels and links to holdings/case records.
- Fit router specification or deterministic implementation: traceable trait-to-lens decisions with requested versus suggested lenses separated. Never a generic list of all names for every stock.
- Research assignment contract: who/what to investigate, source hierarchy, cutoff, required company/security units, holdings attribution and limitations, and expected response schema. A research assignment cannot grant a worker sending/trading authority.
- Output: company/asset profile; route rationale; requested lens result; suitable complementary results; valuation ranges only when supported; unresolved disagreement; missing evidence; concrete invalidators; claim-level source links and timing.
- Validation: the named fixtures in section 9 and compatibility evidence against the accepted offline output/data contract.

If the final deliverable contains only a long comparative report, the research may pass but the requested reusable skill package does not. If it contains only prompts without the evidence/provenance and routing gates, neither authenticity nor routing acceptance passes. Any newly implemented calculation or quality weight is explicitly an adapter choice, not an investor's own quantitative rule.
