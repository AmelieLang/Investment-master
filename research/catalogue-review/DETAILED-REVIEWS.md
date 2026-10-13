# Detailed accepted source reviews

The scores, rationale wording and material gaps below are preserved from the accepted V1 static review. That review predates the later V1 replay. The historical-readiness field describes the source freeze rather than today's completion state. Display-only redactions remove an account handle, an author-specific installation path and a placeholder contact address; data-provider labels are generalized. Most review text is English; a few original review summaries remain Chinese.

Pinned evidence means a precise inspected file and commit. The linked source set is the repository-level evidence set for these criterion rationales. It does not assert that every linked file supports every sentence. File-backed lenses are not automatically authenticated original-investor methods.

<a id="project-1"></a>
## virattt/ai-hedge-fund

[Repository](https://github.com/virattt/ai-hedge-fund) · commit 78b779c1389e2d1452dc29606d2c4126d859b964 · sampled stars 63,955

Popularity rank: 1. Raw source-quality rank: 18 of 21. License-eligible source rank: 16.

Investors or lenses: Warren Buffett, Benjamin Graham, Charlie Munger, Peter Lynch, Stanley Druckenmiller.

Coverage limit: Named methods verified in substantive reviewed source.

### C1 Method completeness and analytical detail

Accepted score: 2.5/5. Five investor-specific prompts cover competence, balance-sheet quality, growth and price. Each is roughly 2–3 KB and requests only 2–4 thesis sentences; no primary-source distilled corpus is provided.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 2/5. FundamentalsSnapshot computes ROE, margins, BVPS growth and FCF history. Outputs are bullish/bearish/neutral plus uncalibrated confidence. Signed confidence is neither intrinsic value nor a transparent stock-quality score.

### C3 Differentiated causal mechanisms

Accepted score: 2.5/5. Graham uses earning power and book value; Lynch uses PEG and categories; Munger uses inversion; Druckenmiller uses fundamental inflections. These qualitative checklists share the same input snapshot.

### C4 Substance over persona and evidence discipline

Accepted score: 3.5/5. Hard point-in-time input rule, neutral/abstention for insufficient history, schema validation, persisted prompts and responses, and documented approximation/impersonation limits. Missing individual numerical fields are not systematically prevented.

Static base: 50.00/100.

Review conclusion: Best engineering separation of investor views, data snapshot, cache, and trading mechanics among this subset.

### Material limitations

- No calculated intrinsic value, sector-specific valuation, primary-source profile lineage, or component-quality score.
- Druckenmiller intentionally lacks macro, rates, price-action inputs.
- MIN_PERIODS counts metric rows, not semantic field coverage; stock-specific important fields may still be absent.

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

Explicit filing-date PIT snapshot, blind backtest prompts and persisted call cache; latest company sector/industry admitted as approximation. Generic backtest fills same-day closes and trade-settlement equity, so no inference of master fidelity/performance.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [hedge_fund/signals/buffett.py](https://github.com/virattt/ai-hedge-fund/blob/78b779c1389e2d1452dc29606d2c4126d859b964/hedge_fund/signals/buffett.py)
- [hedge_fund/signals/graham.py](https://github.com/virattt/ai-hedge-fund/blob/78b779c1389e2d1452dc29606d2c4126d859b964/hedge_fund/signals/graham.py)
- [hedge_fund/signals/munger.py](https://github.com/virattt/ai-hedge-fund/blob/78b779c1389e2d1452dc29606d2c4126d859b964/hedge_fund/signals/munger.py)
- [hedge_fund/signals/lynch.py](https://github.com/virattt/ai-hedge-fund/blob/78b779c1389e2d1452dc29606d2c4126d859b964/hedge_fund/signals/lynch.py)
- [hedge_fund/signals/druckenmiller.py](https://github.com/virattt/ai-hedge-fund/blob/78b779c1389e2d1452dc29606d2c4126d859b964/hedge_fund/signals/druckenmiller.py)
- [hedge_fund/signals/llm_agent.py](https://github.com/virattt/ai-hedge-fund/blob/78b779c1389e2d1452dc29606d2c4126d859b964/hedge_fund/signals/llm_agent.py)
- [hedge_fund/features/snapshot.py](https://github.com/virattt/ai-hedge-fund/blob/78b779c1389e2d1452dc29606d2c4126d859b964/hedge_fund/features/snapshot.py)
- [hedge_fund/backtesting/engine.py](https://github.com/virattt/ai-hedge-fund/blob/78b779c1389e2d1452dc29606d2c4126d859b964/hedge_fund/backtesting/engine.py)
- [hedge_fund/signals/test_llm_agents.py](https://github.com/virattt/ai-hedge-fund/blob/78b779c1389e2d1452dc29606d2c4126d859b964/hedge_fund/signals/test_llm_agents.py)
- [LICENSE](https://github.com/virattt/ai-hedge-fund/blob/78b779c1389e2d1452dc29606d2c4126d859b964/LICENSE)

<a id="project-2"></a>
## xbtlin/ai-berkshire

[Repository](https://github.com/xbtlin/ai-berkshire) · commit ab56abcb31ef8e3a92d925f1b18fb339341ac9d3 · sampled stars 16,719

Popularity rank: 2. Raw source-quality rank: 2 of 21. License-eligible source rank: 2.

Investors or lenses: Warren Buffett, Charlie Munger, Duan Yongping, Li Lu.

Coverage limit: Named methods verified in substantive reviewed source.

### C1 Method completeness and analytical detail

Accepted score: 4/5. Seven-module research workflow and parallel four-role team cover business, moat, inversion, management, industry structure, valuation, bear arguments and monitoring. Financial, REIT and cyclical screens include exceptions and unknown-data branches.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 4/5. Explicit 1–5 checklist anchors, seven-factor exclusion screen, programmatic market-cap/multiple/three-scenario valuation, reinvestment-based terminal P/E and ten-year IRR sensitivity. Scores are categorical anchors rather than validated forecasts.

### C3 Differentiated causal mechanisms

Accepted score: 4/5. Pricing-power tests, competitor replication challenges, reverse DCF, failure-path inversion, incremental versus legacy ROIC and discrete tail-risk treatment provide substantive causal mechanisms.

### C4 Substance over persona and evidence discipline

Accepted score: 3.5/5. Two-source cross-checks, fact/inference separation, network-failure disclosure and audit gates are strong. dyp-ask encourages first-person impersonation. financial_rigor reports verification failure but exits zero; exact_calc uses binary-float eval despite its exact label.

Static base: 78.24/100.

Review conclusion: Strongest combined thesis, transparent screen and valuation implementation in this seven-project subset.

### Material limitations

- No fully sourced master-profile corpus; branded four-lens research partly uses general analyst workflows.
- financial_rigor.py ignores the False verification return; its test explicitly expects exit zero for a gross mismatch.
- cross_validate defaults to 2%, while the workflow specifies 1%; exact_calc does not use Decimal arithmetic.
- Terminal IRR adds annual payout to geometric terminal capital gain. This is a disclosed approximation rather than a full cash-flow IRR.

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

No 2015 point-in-time mode found in the reviewed prompt paths: they request latest filings and prices. terminal_value presets and rate bands are dated 2026. A benchmark must inject frozen 2015 inputs and avoid those presets; generic momentum backtests do not establish master reasoning.

Later comparable replay status: V1 accepted wrapped replay; numeric run results not republished.

### Exact inspected public files

- [skills/investment-team.md](https://github.com/xbtlin/ai-berkshire/blob/ab56abcb31ef8e3a92d925f1b18fb339341ac9d3/skills/investment-team.md)
- [skills/dyp-ask.md](https://github.com/xbtlin/ai-berkshire/blob/ab56abcb31ef8e3a92d925f1b18fb339341ac9d3/skills/dyp-ask.md)
- [skills/investment-research.md](https://github.com/xbtlin/ai-berkshire/blob/ab56abcb31ef8e3a92d925f1b18fb339341ac9d3/skills/investment-research.md)
- [skills/investment-checklist.md](https://github.com/xbtlin/ai-berkshire/blob/ab56abcb31ef8e3a92d925f1b18fb339341ac9d3/skills/investment-checklist.md)
- [skills/quality-screen.md](https://github.com/xbtlin/ai-berkshire/blob/ab56abcb31ef8e3a92d925f1b18fb339341ac9d3/skills/quality-screen.md)
- [tools/financial_rigor.py](https://github.com/xbtlin/ai-berkshire/blob/ab56abcb31ef8e3a92d925f1b18fb339341ac9d3/tools/financial_rigor.py)
- [tools/terminal_value.py](https://github.com/xbtlin/ai-berkshire/blob/ab56abcb31ef8e3a92d925f1b18fb339341ac9d3/tools/terminal_value.py)
- [tests/test_financial_rigor.py](https://github.com/xbtlin/ai-berkshire/blob/ab56abcb31ef8e3a92d925f1b18fb339341ac9d3/tests/test_financial_rigor.py)
- [LICENSE](https://github.com/xbtlin/ai-berkshire/blob/ab56abcb31ef8e3a92d925f1b18fb339341ac9d3/LICENSE)
- [skills/financial-data.md](https://github.com/xbtlin/ai-berkshire/blob/ab56abcb31ef8e3a92d925f1b18fb339341ac9d3/skills/financial-data.md)

<a id="project-3"></a>
## wbh604/UZI-Skill

[Repository](https://github.com/wbh604/UZI-Skill) · commit 650788c54a9b2e042bf7f983f16dbf8d727fce1d · sampled stars 7,215

Popularity rank: 3. Raw source-quality rank: 7 of 21. License-eligible source rank: 5.

Investors or lenses: Warren Buffett, Benjamin Graham, Philip Fisher, Charlie Munger, John Templeton, Seth Klarman, Peter Lynch, William O’Neil, Cathie Wood, Marc Andreessen, Peter Thiel, Bill Gurley, Naval Ravikant, Brad Gerstner, Chamath Palihapitiya, George Soros, Ray Dalio, Howard Marks, Stanley Druckenmiller, Julian Robertson, Michael Burry, Jim Chanos, Jesse Livermore, Mark Minervini, Nicolas Darvas, W.D.Gann, Duan Yongping, Zhang Kun, Zhu Shaoxing, Xie Zhiyu, Feng Liu, Deng Xiaofeng, Zhang Lei, Jim Simons, Ed Thorp, David Shaw, Cliff Asness, Serenity.

Coverage limit: Named investor methods and group-default profiles coexist. The 66-person metadata roster also includes executives, trading collectives and anonymous traders; it is not a count of 66 distinct authentic investment-master methods.

### C1 Method completeness and analytical detail

Accepted score: 4/5. Nineteen-dimension analysis, 66 metadata personas, a quantitative rule engine, decision profiles and DCF/comps/three-statement/LBO/accretion models. Many named people share group-default profiles rather than unique deep methods.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 3.5/5. Real weighted rule-pass scores and intermediate model logs; two-stage DCF, debt/equity bridge and sensitivity. Caveats include a 0.8×net-income FCF proxy, missing-share defaults of one and a safety_margin field that measures upside/price rather than margin of safety/intrinsic value.

### C3 Differentiated causal mechanisms

Accepted score: 3/5. Investor-specific screens, inversion, forensic/risk lenses and supply-chain bottleneck analysis exist. Many thresholds are author-created proxies rather than verified original-investor rules.

### C4 Substance over persona and evidence discipline

Accepted score: 2.5/5. Data-integrity controls exist, but current-known holdings can override signals. Confidence counts configured rules, not evaluated-rule coverage. Several absent fields default to zero and fail rather than abstain; roleplay and synthetic quotations are required.

Static base: 66.47/100.

Review conclusion: Substantive actual quantitative implementation; useful detachable finance models and rule explanations.

### Material limitations

- Documentation alternates between 50, 51, 65 and 66 personas; investor_db defines 66, including traders, executives and collectives.
- known_holding and override_signal can defeat independent rule analysis and introduce historical leakage.
- Confidence uses n_rules=len(rules), while missing rules are excluded from weight_total.
- DCF defaults use A-share risk-free-rate and equity-risk-premium assumptions despite broader market scope; the reviewed wrapper does not route those overrides into compute_wacc.
- Missing net debt yields an annotated EV≈equity value; missing shares default to one when price is unavailable.

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

Requires a dated feature packet and removal of undated investor_knowledge holding boosts. The 66-person roster includes later figures and post-2015 traders. No authentic 2015 master-comparator benchmark was found in the reviewed paths.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [skills/investor-panel/SKILL.md](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/skills/investor-panel/SKILL.md)
- [skills/investor-panel/references/group-a-classic-value.md](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/skills/investor-panel/references/group-a-classic-value.md)
- [skills/deep-analysis/references/task2-dimension-scoring.md](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/skills/deep-analysis/references/task2-dimension-scoring.md)
- [skills/deep-analysis/scripts/lib/investor_evaluator.py](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/skills/deep-analysis/scripts/lib/investor_evaluator.py)
- [skills/deep-analysis/scripts/lib/fin_models.py](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/skills/deep-analysis/scripts/lib/fin_models.py)
- [LICENSE](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/LICENSE)
- [skills/deep-analysis/SKILL.md](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/skills/deep-analysis/SKILL.md)
- [skills/deep-analysis/scripts/lib/investor_db.py](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/skills/deep-analysis/scripts/lib/investor_db.py)
- [skills/deep-analysis/scripts/lib/data_integrity.py](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/skills/deep-analysis/scripts/lib/data_integrity.py)
- [skills/deep-analysis/scripts/lib/investor_criteria.py](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/skills/deep-analysis/scripts/lib/investor_criteria.py)
- [skills/deep-analysis/scripts/lib/investor_knowledge.py](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/skills/deep-analysis/scripts/lib/investor_knowledge.py)
- [skills/deep-analysis/scripts/lib/investor_profile.py](https://github.com/wbh604/UZI-Skill/blob/650788c54a9b2e042bf7f983f16dbf8d727fce1d/skills/deep-analysis/scripts/lib/investor_profile.py)

<a id="project-4"></a>
## tradermonty/claude-trading-skills

[Repository](https://github.com/tradermonty/claude-trading-skills) · commit d92c667b332b9fd64c58f30945485b2269999c3d · sampled stars 2,988

Popularity rank: 4. Raw source-quality rank: 6 of 21. License-eligible source rank: 4.

Investors or lenses: William O'Neil, Mark Minervini, Stanley Druckenmiller.

Coverage limit: Three methods verified through substantive audited implementation files. Other packages may refer to additional investors; no unreviewed master names are counted here.

### C1 Method completeness and analytical detail

Accepted score: 4/5. Detailed seven-component CAN SLIM screener, VCP trend/template/contraction pipeline and an eight-input Druckenmiller synthesizer with risk and market gates. Substantive methods rather than celebrity-role prompts.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 3/5. Transparent 0–100 component weights, thresholds, market-bear overrides and setup-quality/execution-state separation. Audited master methods do not require intrinsic equity valuation: their score represents setup quality.

### C3 Differentiated causal mechanisms

Accepted score: 3.5/5. Growth acceleration, earnings versus buyback distortion, relative leadership, institutional accumulation, volatility contraction and liquidity/market-state synthesis encode distinct measurable hypotheses.

### C4 Substance over persona and evidence discipline

Accepted score: 3/5. Documented fallback penalties and data flags. Claims of original O'Neil weights and conviction-based aggressive sizing are not authenticated or calibrated in this review; current-data reliability remains a dependency.

Static base: 67.06/100.

Review conclusion: Most comprehensive deterministic trading-method implementation in this subset; extractable rules rather than personality imitation.

### Material limitations

- Trading-screen score does not supply a value-investment thesis or DCF.
- Claimed original weights were not verified against primary O'Neil material; treat them as authored proxies.
- Immediate-buy rules can recommend a 15–20% position from a stock score.
- Current index, financial-provider and screener inputs lack demonstrated 2015 vintage, ownership and restatement controls.

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

VCP offers historical single-ticker walking with forward-outcome fields and state filtering, but this is not an authentic master-comparator test. Druckenmiller loads recent (<72-hour) JSON reports and needs a controlled adapter for historical replay.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [skills/canslim-screener/SKILL.md](https://github.com/tradermonty/claude-trading-skills/blob/d92c667b332b9fd64c58f30945485b2269999c3d/skills/canslim-screener/SKILL.md)
- [skills/canslim-screener/scripts/scorer.py](https://github.com/tradermonty/claude-trading-skills/blob/d92c667b332b9fd64c58f30945485b2269999c3d/skills/canslim-screener/scripts/scorer.py)
- [skills/stanley-druckenmiller-investment/SKILL.md](https://github.com/tradermonty/claude-trading-skills/blob/d92c667b332b9fd64c58f30945485b2269999c3d/skills/stanley-druckenmiller-investment/SKILL.md)
- [skills/stanley-druckenmiller-investment/scripts/strategy_synthesizer.py](https://github.com/tradermonty/claude-trading-skills/blob/d92c667b332b9fd64c58f30945485b2269999c3d/skills/stanley-druckenmiller-investment/scripts/strategy_synthesizer.py)
- [skills/vcp-screener/SKILL.md](https://github.com/tradermonty/claude-trading-skills/blob/d92c667b332b9fd64c58f30945485b2269999c3d/skills/vcp-screener/SKILL.md)
- [LICENSE](https://github.com/tradermonty/claude-trading-skills/blob/d92c667b332b9fd64c58f30945485b2269999c3d/LICENSE)
- [skills/canslim-screener/references/scoring_system.md](https://github.com/tradermonty/claude-trading-skills/blob/d92c667b332b9fd64c58f30945485b2269999c3d/skills/canslim-screener/references/scoring_system.md)

<a id="project-5"></a>
## questflowai/investorskills

[Repository](https://github.com/questflowai/investorskills) · commit 2844d7809a73c01e769c8c1c7ae8189788db4d9e · sampled stars 1,905

Popularity rank: 5. Raw source-quality rank: 11 of 21. License-eligible source rank: 9.

Investors or lenses: Buffett, Munger, Graham, Lynch, Dalio, Marks, Druckenmiller, Soros, Burry, Greenblatt, Li Lu, Nick Sleep, Klarman, Templeton.

Coverage limit: The repository has 63 SKILL packages, including crypto/VC and composite frameworks. This is not 63 classic investment masters. Listed names are a non-exhaustive file-backed investor roster; Buffett, Lynch, Dalio and Marks method bodies were read.

### C1 Method completeness and analytical detail

Accepted score: 3.5/5. 63 packages with structured universe, inputs, process, risk, monitoring and guardrails; significant generic template repetition.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 2.5/5. Company memo and valuation ranges requested; qualitative weights and broad valuation guidance do not yield reproducible stock scores.

### C3 Differentiated causal mechanisms

Accepted score: 3/5. Recognizable Lynch stock categories, Buffett owner earnings, Marks expectations/cycles and Dalio regime/risk contribution; limited concrete tests.

### C4 Substance over persona and evidence discipline

Accepted score: 3.5/5. Primary-source preference, Too Hard/missing inputs and no-optimism guardrails; general reading lists rather than claim-level mappings.

Static base: 60.59/100.

Review conclusion: 覆盖广、可组合；不是可复算的投资评分/估值引擎

### Material limitations

- 63包很多使用同一模板；high/medium权重非数值；多数估值只是要求而无计算细节；来源多为书目与案例总称

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

Canonical past cases and source reading lists available; no explicit as-of publication controls or native historical engine in inspected modules.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [skills/buffett/SKILL.md](https://github.com/questflowai/investorskills/blob/2844d7809a73c01e769c8c1c7ae8189788db4d9e/skills/buffett/SKILL.md)
- [skills/buffett/invest.md](https://github.com/questflowai/investorskills/blob/2844d7809a73c01e769c8c1c7ae8189788db4d9e/skills/buffett/invest.md)
- [skills/lynch-growth/invest.md](https://github.com/questflowai/investorskills/blob/2844d7809a73c01e769c8c1c7ae8189788db4d9e/skills/lynch-growth/invest.md)
- [skills/dalio-principles-allweather/invest.md](https://github.com/questflowai/investorskills/blob/2844d7809a73c01e769c8c1c7ae8189788db4d9e/skills/dalio-principles-allweather/invest.md)
- [skills/marks-cycles/invest.md](https://github.com/questflowai/investorskills/blob/2844d7809a73c01e769c8c1c7ae8189788db4d9e/skills/marks-cycles/invest.md)
- [LICENSE](https://github.com/questflowai/investorskills/blob/2844d7809a73c01e769c8c1c7ae8189788db4d9e/LICENSE)

<a id="project-6"></a>
## agi-now/buffett-skills

[Repository](https://github.com/agi-now/buffett-skills) · commit aeeae92c22c4770cd1277a35d37294c9c2435475 · sampled stars 821

Popularity rank: 6. Raw source-quality rank: 4 of 21. License-eligible source rank: blocked at pin.

Investors or lenses: Warren Buffett.

Coverage limit: File-backed implemented methods; source audit samples are enumerated in pinned_sources. Corroborating influences are separately described, not separate agents.

### C1 Method completeness and analytical detail

Accepted score: 4.5/5. Eight large domain modules, progressive loading, mandatory financial/risk/monitoring outputs and industry playbooks.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 3.5/5. Owner earnings formula, earnings multiples/DCF/cyclical normalization, safety tiers and stock-specific output; no aggregate score.

### C3 Differentiated causal mechanisms

Accepted score: 3.5/5. Maintenance-vs-growth capex, look-through earnings, capital allocation, institutional imperative and industry-specific risks.

### C4 Substance over persona and evidence discipline

Accepted score: 2.5/5. Circle-of-competence refusal useful, but voice/embodiment instructions and unsupported author thresholds framed as Buffett standards; weak fact-date receipt.

Static base: 71.18/100.

Review conclusion: Buffett教学内容深入；阈值来源和复用授权需核验

### Material limitations

- 15%ROIC/ROE、分档倍数与20–50%安全边际常写成大师标准，未映射原文支持；依赖语气仿真；无总评分/执行器

License at pin: not_found. blocked pending explicit reuse permission or verified license

### Historical readiness at the source freeze

Many dated shareholder-letter examples including later-than-2015 events; no explicit publication-date cutoff or point-in-time engine. Must freeze supplied historical dossier.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [skills/buffett/SKILL.md](https://github.com/agi-now/buffett-skills/blob/aeeae92c22c4770cd1277a35d37294c9c2435475/skills/buffett/SKILL.md)
- [skills/buffett/references/06-valuation-capital.md](https://github.com/agi-now/buffett-skills/blob/aeeae92c22c4770cd1277a35d37294c9c2435475/skills/buffett/references/06-valuation-capital.md)
- [skills/buffett/references/05-financial-metrics.md](https://github.com/agi-now/buffett-skills/blob/aeeae92c22c4770cd1277a35d37294c9c2435475/skills/buffett/references/05-financial-metrics.md)

<a id="project-7"></a>
## AlphaGBM/investment-masters

[Repository](https://github.com/AlphaGBM/investment-masters) · commit b1a304fca0f28c365f5821f4f7e36935dd4d4c2e · sampled stars 638

Popularity rank: 7. Raw source-quality rank: 16 of 21. License-eligible source rank: 14.

Investors or lenses: Ray Dalio, Warren Buffett, Jim Simons, Cliff Asness, David Tepper, George Soros, Bill Ackman, Howard Marks, Zhang Lei, Cathie Wood, Duan Yongping, Peter Lynch, Stanley Druckenmiller, Liang Wenfeng, Linda Raschke.

Coverage limit: Fifteen file-backed method profiles. Five master bodies and the entrypoint/catalogue were fully reviewed.

### C1 Method completeness and analytical detail

Accepted score: 2.5/5. Fifteen structured local profiles cover stock/portfolio principles, sizing, exits and bibliography. Useful short syntheses, with limited detailed fiscal reconciliation or workflows.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 2/5. Buffett ROE/growth/debt screens, Lynch PEG/categories and Marks credit-cycle thresholds. No local market-data runner, automatic aggregate score or instantiated DCF.

### C3 Differentiated causal mechanisms

Accepted score: 3/5. Risk parity, value, reflexivity, credit cycles and six stock categories differ meaningfully. Hypothesis validation and valuation implications remain mostly prose.

### C4 Substance over persona and evidence discipline

Accepted score: 3.5/5. Entrypoint prohibits impersonation and invented figures, requires source dates, and warns that 13F is not a live portfolio or statement of intent. Profiles nevertheless contain undated latest-holdings tables and post-2015 examples.

Static base: 52.35/100.

Review conclusion: Portable readable master-method catalogue with unusually clear evidence/permission boundaries.

### Material limitations

- Systematic equivalents refer to separate AlphaGBM features; they are not implemented scoring code in this repository.
- Undated latest-holdings tables, such as Buffett AAPL near 45%, must not be used as current fact or 2015 evidence.
- Bibliographies are not mapped to individual method claims.

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

Entrypoint requires filing-period/publication/amendment discipline, but no 2015 fixtures, chronology isolation or run harness was found. Later books and undated profile tables must be excluded from historical evidence.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [SKILL.md](https://github.com/AlphaGBM/investment-masters/blob/b1a304fca0f28c365f5821f4f7e36935dd4d4c2e/SKILL.md)
- [catalog.json](https://github.com/AlphaGBM/investment-masters/blob/b1a304fca0f28c365f5821f4f7e36935dd4d4c2e/catalog.json)
- [masters/buffett.md](https://github.com/AlphaGBM/investment-masters/blob/b1a304fca0f28c365f5821f4f7e36935dd4d4c2e/masters/buffett.md)
- [masters/bridgewater.md](https://github.com/AlphaGBM/investment-masters/blob/b1a304fca0f28c365f5821f4f7e36935dd4d4c2e/masters/bridgewater.md)
- [masters/howard_marks.md](https://github.com/AlphaGBM/investment-masters/blob/b1a304fca0f28c365f5821f4f7e36935dd4d4c2e/masters/howard_marks.md)
- [masters/soros.md](https://github.com/AlphaGBM/investment-masters/blob/b1a304fca0f28c365f5821f4f7e36935dd4d4c2e/masters/soros.md)
- [masters/lynch.md](https://github.com/AlphaGBM/investment-masters/blob/b1a304fca0f28c365f5821f4f7e36935dd4d4c2e/masters/lynch.md)
- [LICENSE](https://github.com/AlphaGBM/investment-masters/blob/b1a304fca0f28c365f5821f4f7e36935dd4d4c2e/LICENSE)

<a id="project-8"></a>
## alchaincyf/munger-skill

[Repository](https://github.com/alchaincyf/munger-skill) · commit 12d582ce4a97bcfff1cac032ecef436406feb1c2 · sampled stars 380

Popularity rank: 8. Raw source-quality rank: 19 of 21. License-eligible source rank: 17.

Investors or lenses: Charlie Munger.

Coverage limit: Coverage is limited to the accepted inspected repository files; investor labels are not authenticated original methods.

### C1 Method completeness and analytical detail

Accepted score: 2.5/5. SKILL Step 2 requires moat, management incentives, financial trends, competition, current PE/PB and inverse downside; checkpoints demand counterevidence and Too Hard. It lacks operating-account reconciliation and comprehensive stock valuation.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 2/5. Individual-company application and current market-cap/PE/PB comparison are real, but there is no intrinsic-value formula, component stock score, sensitivity model or valuation range generator.

### C3 Differentiated causal mechanisms

Accepted score: 3/5. Incentive mapping (who earns/who bears risk), inverse failure paths, equal-time Darwin counterevidence and combined biases are implemented. These are causal decision checks, though not a quantified expectations-versus-price model.

### C4 Substance over persona and evidence discipline

Accepted score: 2/5. Live search and uncertainty/Too Hard are useful. However, explicit first-person impersonation, one-time disclaimer, prohibition on framework attribution and pruning argument after four paragraphs prioritize immersion; facts are internally hidden rather than auditable citations.

Static base: 47.06/100.

Review conclusion: Useful as an inversion/incentives overlay after stripping persona-first rules. Not a top stock-valuation engine or 2015 benchmark priority.

### Material limitations

- No calculable stock-quality score or value bridge
- Presentation rules can suppress reasoning and qualification; first-person persona can imply actual investor views
- Research index references private-looking absolute document paths not present in the repository; references are summaries, not primary-source corpus
- No publication-date cutoff, source-date ledger or financial-data validation

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

- 2015_route: A supplied frozen 2015 dossier could test the public Munger framework, but live-search workflow must be constrained. No native as-of control or dated fixture.
- leakage: Contains post-2015 Alibaba/AI and late-life interpretations; modern training/source summaries can leak hindsight. Authentic Munger comparator must be separate.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [SKILL.md](https://github.com/alchaincyf/munger-skill/blob/12d582ce4a97bcfff1cac032ecef436406feb1c2/SKILL.md)
- [LICENSE](https://github.com/alchaincyf/munger-skill/blob/12d582ce4a97bcfff1cac032ecef436406feb1c2/LICENSE)
- [README.md](https://github.com/alchaincyf/munger-skill/blob/12d582ce4a97bcfff1cac032ecef436406feb1c2/README.md)
- [references/research.md](https://github.com/alchaincyf/munger-skill/blob/12d582ce4a97bcfff1cac032ecef436406feb1c2/references/research.md)

<a id="project-9"></a>
## monarchjuno/vibe-investing

[Repository](https://github.com/monarchjuno/vibe-investing) · commit 15954a68fcf9c5368955f935a899e9c80ad48d5c · sampled stars 300

Popularity rank: 9. Raw source-quality rank: 5 of 21. License-eligible source rank: 3.

Investors or lenses: Aswath Damodaran, Benjamin Graham, Bill Ackman, Cathie Wood, Charlie Munger, Michael Burry, Mohnish Pabrai, Nassim Nicholas Taleb, Peter Lynch, Philip Fisher, Rakesh Jhunjhunwala, Stanley Druckenmiller, Warren Buffett.

Coverage limit: Thirteen file-backed lenses. Buffett, Graham, Munger and Damodaran plus the company-analysis workflow were fully reviewed.

### C1 Method completeness and analytical detail

Accepted score: 3.5/5. Thirteen investor-lens skills plus company-analysis routing, narrative→reverse DCF→forward DCF, comps/SOTP/scenarios and deal radar. Required inputs and uncertainty rules are sensible; profile references are thin.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 3/5. Requires per-share probability-weighted fair value, growth/margin/reinvestment expectations and unit labels. No native stock-quality aggregate score; calculations are delegated to the agent rather than a deterministic model.

### C3 Differentiated causal mechanisms

Accepted score: 3.5/5. Expectation gaps and stories translated into operating drivers differentiate the approach. Graham NCAV/earning power, Munger incentives/too-hard and Damodaran lifecycle/risk are separate mechanisms.

### C4 Substance over persona and evidence discipline

Accepted score: 4/5. Numbers are tagged Actual/Estimated/Assumption. Verified facts, no invented peers/deals, explicit uncertainty and missing-data limits. No claim of literal investor endorsement.

Static base: 68.24/100.

Review conclusion: Clean modular chatbot lens library with better epistemic/output contract than celebrity imitation.

### Material limitations

- No numerical component-quality score or deterministic DCF/reconciliation implementation in the reviewed company method.
- Primary-source claim mapping is missing from the investor entrypoints.
- Always inferring company identity without clarification may misresolve an ambiguous prompt; an integration wrapper should validate identity.

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

Defaults to current web research and deal radar; no as-of gate or historical master-comparator run was found. Frozen packets can be used after restricting retrieval to the cutoff.

Later comparable replay status: V1 accepted wrapped replay; numeric run results not republished.

### Exact inspected public files

- [skills/investor-personas/warren-buffett/SKILL.md](https://github.com/monarchjuno/vibe-investing/blob/15954a68fcf9c5368955f935a899e9c80ad48d5c/skills/investor-personas/warren-buffett/SKILL.md)
- [skills/investor-personas/ben-graham/SKILL.md](https://github.com/monarchjuno/vibe-investing/blob/15954a68fcf9c5368955f935a899e9c80ad48d5c/skills/investor-personas/ben-graham/SKILL.md)
- [skills/investor-personas/charlie-munger/SKILL.md](https://github.com/monarchjuno/vibe-investing/blob/15954a68fcf9c5368955f935a899e9c80ad48d5c/skills/investor-personas/charlie-munger/SKILL.md)
- [skills/investor-personas/aswath-damodaran/SKILL.md](https://github.com/monarchjuno/vibe-investing/blob/15954a68fcf9c5368955f935a899e9c80ad48d5c/skills/investor-personas/aswath-damodaran/SKILL.md)
- [skills/fundamental-analysis/company-analysis/SKILL.md](https://github.com/monarchjuno/vibe-investing/blob/15954a68fcf9c5368955f935a899e9c80ad48d5c/skills/fundamental-analysis/company-analysis/SKILL.md)
- [skills/fundamental-analysis/company-analysis/references/output-contract.md](https://github.com/monarchjuno/vibe-investing/blob/15954a68fcf9c5368955f935a899e9c80ad48d5c/skills/fundamental-analysis/company-analysis/references/output-contract.md)
- [skills/fundamental-analysis/company-analysis/references/data-integrity-and-deal-radar.md](https://github.com/monarchjuno/vibe-investing/blob/15954a68fcf9c5368955f935a899e9c80ad48d5c/skills/fundamental-analysis/company-analysis/references/data-integrity-and-deal-radar.md)
- [LICENSE](https://github.com/monarchjuno/vibe-investing/blob/15954a68fcf9c5368955f935a899e9c80ad48d5c/LICENSE)
- [skills/fundamental-analysis/company-analysis/references/analysis-orchestration.md](https://github.com/monarchjuno/vibe-investing/blob/15954a68fcf9c5368955f935a899e9c80ad48d5c/skills/fundamental-analysis/company-analysis/references/analysis-orchestration.md)

<a id="project-10"></a>
## LLMQuant/skills

[Repository](https://github.com/LLMQuant/skills) · commit 1918237467c2dff4cc97a18ebc0892dfd46e8129 · sampled stars 232

Popularity rank: 10. Raw source-quality rank: 10 of 21. License-eligible source rank: 8.

Investors or lenses: Buffett, Graham, Munger, Pabrai, Jhunjhunwala, Lynch, Fisher, Wood, Druckenmiller, Ackman, Burry, Taleb, Damodaran, Duan Yongping, Marks, Tepper.

Coverage limit: File-backed implemented methods; source audit samples are enumerated in pinned_sources. Corroborating influences are separately described, not separate agents.

### C1 Method completeness and analytical detail

Accepted score: 3.5/5. Router plus17 investor-lens workflows; company facts, mental models, signals and boundaries covered but no executable financial engine.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 3/5. Weighted Lynch score and qualitative Buffett scorecard; equations/thresholds partial, subscore mapping and defensible value bridge incomplete.

### C3 Differentiated causal mechanisms

Accepted score: 3/5. Owner cash, six-stock-category Lynch and differentiated value/growth/macro lenses; largely principle-level tests.

### C4 Substance over persona and evidence discipline

Accepted score: 2.5/5. Good dates/data-used/missing-data contract, but identity paragraphs contradict router and use sweeping/unsourced persona claims.

Static base: 60.59/100.

Review conclusion: 接数据方便；人设冲突、子分定义和估值细节需改

### Material limitations

- Buffett总分无分项权重；Lynch有30/25/20/15/10权重但无各子分映射；路由反人设而工作流直接角色扮演；无金融执行代码

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

Workflow mandates filing, observation, price and holdings dates plus stale notices. No historical-reasoning benchmark or cutoff control found. Provider 2015 vintage coverage must be verified.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [skills/llmquant-investor-lenses/SKILL.md](https://github.com/LLMQuant/skills/blob/1918237467c2dff4cc97a18ebc0892dfd46e8129/skills/llmquant-investor-lenses/SKILL.md)
- [skills/llmquant-investor-lenses/workflows/warren-buffett.md](https://github.com/LLMQuant/skills/blob/1918237467c2dff4cc97a18ebc0892dfd46e8129/skills/llmquant-investor-lenses/workflows/warren-buffett.md)
- [skills/llmquant-investor-lenses/workflows/warren-buffett-scorecard.md](https://github.com/LLMQuant/skills/blob/1918237467c2dff4cc97a18ebc0892dfd46e8129/skills/llmquant-investor-lenses/workflows/warren-buffett-scorecard.md)
- [skills/llmquant-investor-lenses/workflows/peter-lynch.md](https://github.com/LLMQuant/skills/blob/1918237467c2dff4cc97a18ebc0892dfd46e8129/skills/llmquant-investor-lenses/workflows/peter-lynch.md)
- [README.md](https://github.com/LLMQuant/skills/blob/1918237467c2dff4cc97a18ebc0892dfd46e8129/README.md)
- [LICENSE](https://github.com/LLMQuant/skills/blob/1918237467c2dff4cc97a18ebc0892dfd46e8129/LICENSE)

<a id="project-11"></a>
## will2025btc/buffett-perspective

[Repository](https://github.com/will2025btc/buffett-perspective) · commit e18afcfc208f0cb144dfc2a11276e2eaafb9bdbd · sampled stars 215

Popularity rank: 11. Raw source-quality rank: 21 of 21. License-eligible source rank: 18.

Investors or lenses: Warren Buffett.

Coverage limit: Coverage is limited to the accepted inspected repository files; investor labels are not authenticated original methods.

### C1 Method completeness and analytical detail

Accepted score: 2/5. Six mental models and eight heuristics cover moat, competence, ownership, institutional imperative, safety and management, but there is no required company research sequence, data schema or complete financial workflow.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 1/5. Owner earnings and intrinsic value are named, but there is no owner-earnings calculation, DCF/multiple formula, score breakdown or stock-specific numerical output template.

### C3 Differentiated causal mechanisms

Accepted score: 2/5. Moat durability, retained-owner economics and institutional imperative have causal explanations, but mostly illustrative historical stories rather than discriminating tests tied to company evidence.

### C4 Substance over persona and evidence discipline

Accepted score: 1.5/5. Roleplay rules are labeled most important and insist on first-person Buffett. One-time disclosure and honesty boundaries help, but no citations/date controls are required for new analysis. A hard source contradiction lowers reliability.

Static base: 31.18/100.

Review conclusion: Lowest utility in this eight-project group for substantive stock research. Avoid using it as an analysis engine; public Buffett references are safer than the persona module.

### Material limitations

- SKILL says See's raised prices 10% annually for 50 years. Buffett's 1986 letter describes minimal price increases that year and modest intended increases, contradicting the universal annual claim: https://www.berkshirehathaway.com/letters/1986.html
- Most sources are named generically without direct primary links or claim-by-claim traceability
- No autonomous retrieval discipline for contemporary company facts
- Biographical identity/latest holdings and imagined first-person explanations are vulnerable to stale information and invented intent

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

- 2015_route: Frozen dossier and separate Buffett contemporaneous evidence required; prompt does not enforce cutoff.
- leakage: Contains 2016 Apple, 2020 Japan, 2024 sales, 2025 retirement and 2026 state; includes later outcomes of Tesco/Kraft Heinz/airlines.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [SKILL.md](https://github.com/will2025btc/buffett-perspective/blob/e18afcfc208f0cb144dfc2a11276e2eaafb9bdbd/SKILL.md)
- [LICENSE](https://github.com/will2025btc/buffett-perspective/blob/e18afcfc208f0cb144dfc2a11276e2eaafb9bdbd/LICENSE)
- [README.md](https://github.com/will2025btc/buffett-perspective/blob/e18afcfc208f0cb144dfc2a11276e2eaafb9bdbd/README.md)
- [references/research/01-writings.md](https://github.com/will2025btc/buffett-perspective/blob/e18afcfc208f0cb144dfc2a11276e2eaafb9bdbd/references/research/01-writings.md)
- [references/research/05-decisions.md](https://github.com/will2025btc/buffett-perspective/blob/e18afcfc208f0cb144dfc2a11276e2eaafb9bdbd/references/research/05-decisions.md)

<a id="project-12"></a>
## kangarooking/buffett-letters-skill

[Repository](https://github.com/kangarooking/buffett-letters-skill) · commit 5b1fbe1d93f155fcf4acf236841bf8e1b5951c91 · sampled stars 105

Popularity rank: 12. Raw source-quality rank: 12 of 21. License-eligible source rank: 10.

Investors or lenses: Warren Buffett.

Coverage limit: Coverage is limited to the accepted inspected repository files; investor labels are not authenticated original methods.

### C1 Method completeness and analytical detail

Accepted score: 3/5. Actual modules cover business, moat, accounting/owner earnings, capital allocation, float, crisis survival and competence. Completion criteria and stop rules are real, but module orchestration/data inputs/sector reconciliation remain incomplete.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 3/5. Aesop requires 5-10-year cash-flow ranges, discounting and price comparison. Margin-of-safety requires pessimistic/base/optimistic values and (value lower bound-price)/value lower bound, with suggested 25%/40% gates. There is no aggregate stock-quality score or executable DCF.

### C3 Differentiated causal mechanisms

Accepted score: 3/5. Incremental capital needed for profit growth, look-through retained earnings, price-dependent repurchases, underwriting float and financial resilience are investor-specific mechanisms. Tests are concrete but sometimes over-generalized.

### C4 Substance over persona and evidence discipline

Accepted score: 2.5/5. Separates original excerpt, interpretation, past application and future execution; names letter year and boundaries. Validation badges are author-generated reasoning/trigger tests, not actual financial experiments. Material formula drift prevents a high evidence score.

Static base: 58.24/100.

Review conclusion: Modular Buffett toolkit worth a controlled behavior test, especially valuation/accounting modules. For direct reuse, correct float and owner-earnings omissions and label modern suggested thresholds as author heuristics.

### Material limitations

- float-thinking execution uses total service cost / float as funding cost. Buffett's 2000 primary letter defines underwriting loss as float cost, not total claims/service cost: https://www.berkshirehathaway.com/2000ar/2000letter.html
- look-through-earnings owner-earnings shorthand omits maintenance working-capital additions and other noncash adjustments described in Buffett's 1986 appendix: https://www.berkshirehathaway.com/letters/1986.html
- Generic combined-ratio 100-107 cutoff ignores insurer-specific float duration/premium-to-float relationship
- Circle-of-competence requires past 5-10-year personal prediction records above coin-flip accuracy; a general assistant often lacks that evidence and should abstain rather than manufacture records
- Initial owner-earnings/SKILL.md snapshot was an empty missing-path artifact. Correct implementation is look-through-earnings/SKILL.md
- Test-prompts check activation/expected prose; no dated equity fixture or realized benchmark

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

- 2015_route: Among this group, a reasonable conditional Buffett benchmark candidate with a frozen pre-cutoff dossier. Pre-2015 modules must be selected in advance, not by eventual outcome.
- leakage: Modules cite 2021 Apple, 2022 doctrine and later outcomes; source-year labels are not an as-of enforcement system. No publication-date ledger.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [LICENSE](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/LICENSE)
- [README.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/README.md)
- [INDEX.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/INDEX.md)
- [verified.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/verified.md)
- [aesop-three-questions/SKILL.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/aesop-three-questions/SKILL.md)
- [business-picker/SKILL.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/business-picker/SKILL.md)
- [economic-moat/SKILL.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/economic-moat/SKILL.md)
- [look-through-earnings/SKILL.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/look-through-earnings/SKILL.md)
- [first-law-of-capital-allocation/SKILL.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/first-law-of-capital-allocation/SKILL.md)
- [float-thinking/SKILL.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/float-thinking/SKILL.md)
- [margin-of-safety/SKILL.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/margin-of-safety/SKILL.md)
- [circle-of-competence/SKILL.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/circle-of-competence/SKILL.md)
- [ceo-as-risk-officer/SKILL.md](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/ceo-as-risk-officer/SKILL.md)
- [aesop-three-questions/test-prompts.json](https://github.com/kangarooking/buffett-letters-skill/blob/5b1fbe1d93f155fcf4acf236841bf8e1b5951c91/aesop-three-questions/test-prompts.json)

<a id="project-13"></a>
## lanfuli/aleabito-serenity-skills

[Repository](https://github.com/lanfuli/aleabito-serenity-skills) · commit bb71df12a7529b96178f85c2f66b6b5d57a704f6 · sampled stars 95

Popularity rank: 13. Raw source-quality rank: 9 of 21. License-eligible source rank: 7.

Investors or lenses: Serenity.

Coverage limit: Coverage is limited to the accepted inspected repository files; investor labels are not authenticated original methods.

### C1 Method completeness and analytical detail

Accepted score: 3/5. Five-step framework explicitly maps mandatory demand, scarce supply, design-in, pricing, capital intensity and geopolitics, with source hierarchy, field gates, verify-next and worked examples. It is intentionally a research-map system, not full management/accounting/valuation coverage.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 2/5. Individual-ticker thesis and market-cap/opportunity checks exist. No DCF, intrinsic-value range or company investment-score arithmetic is implemented. Numeric radar outputs measure attention, not company quality or value.

### C3 Differentiated causal mechanisms

Accepted score: 4/5. Certification + slow capacity growth + must-have capability cause pricing power; design-out, second sourcing, substitution, dilution and capex can falsify it. Separates structural economics from re-rating/index flows and makes missing links observable.

### C4 Substance over persona and evidence discipline

Accepted score: 4/5. All moat/profitability/replacement fields start unverified; tweet alone cannot prove company quality. Never invent facts/links, separate inferred angle from source post, and default research-map. Explicit survivorship/reply-noise/single-account warnings. Few-shot examples still occasionally elevate fields using only post claims, so native instructions are stronger than their examples.

Static base: 61.18/100.

Review conclusion: Best evidence/abstention design in this eight-project group and useful as a research-lead module. A strong supplemental missing-data/falsification test candidate; not a 2015 authentic-Serenity comparator or standalone valuation engine.

### Material limitations

- No native value bridge or transparent investment score. Buffett value/capital modules rely on an optional local $buffett skill absent from this repo
- Radar --asof filters events correctly, but modern theme taxonomy and full-corpus pattern rules can leak later learned categories
- Radar code labels theme rotation by raw count delta, while SKILL describes mention-share change; those are not equivalent when volume changes
- Exemplar SIVE assigns moat medium and replacement risk medium-low based on posts/undisclosed contracts despite primary-evidence gate
- The raw 6,120-post training archive and report dossiers are not included in tree; quoted source posts are linked but independent financial verification is still required

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

- 2015_route: Can test transfer of general chokepoint reasoning on a frozen 2015 dossier, but cannot validate authentic Serenity fidelity for 2015: source history starts 2025-07-02.
- leakage: Corpus and exemplars encode 2025-26 positions/outcomes; analysis patterns trained on full archive must not be represented as known in 2015. --asof concerns attention events, not financial publication vintage.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [LICENSE](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/LICENSE)
- [README.md](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/README.md)
- [skills/serenity-method/SKILL.md](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/skills/serenity-method/SKILL.md)
- [skills/serenity-method/references/framework.md](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/skills/serenity-method/references/framework.md)
- [skills/serenity-method/references/exemplars.md](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/skills/serenity-method/references/exemplars.md)
- [skills/serenity-radar/SKILL.md](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/skills/serenity-radar/SKILL.md)
- [skills/serenity-radar/references/patterns.md](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/skills/serenity-radar/references/patterns.md)
- [skills/serenity-radar/scripts/radar.js](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/skills/serenity-radar/scripts/radar.js)
- [skills/follow-aleabito/SKILL.md](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/skills/follow-aleabito/SKILL.md)
- [skills/follow-aleabito/scripts/fetch-updates.js](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/skills/follow-aleabito/scripts/fetch-updates.js)
- [skills/follow-aleabito/scripts/send-imessage.js](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/skills/follow-aleabito/scripts/send-imessage.js)
- [skills/follow-aleabito/scripts/setup-config.js](https://github.com/lanfuli/aleabito-serenity-skills/blob/bb71df12a7529b96178f85c2f66b6b5d57a704f6/skills/follow-aleabito/scripts/setup-config.js)

<a id="project-14"></a>
## freenowill/stock-fish

[Repository](https://github.com/freenowill/stock-fish) · commit f1feea00238ba39804551d144e5a9ac7ee88f443 · sampled stars 81

Popularity rank: 14. Raw source-quality rank: 13 of 21. License-eligible source rank: 11.

Investors or lenses: Benjamin Graham, Warren Buffett, Philip Fisher, Peter Lynch, John Templeton, George Soros, Ray Dalio.

Coverage limit: Named methods verified in substantive reviewed source.

### C1 Method completeness and analytical detail

Accepted score: 3.5/5. Eight analyst employees plus a CIO, seven philosophies, evidence chain, scenario/order/monitoring schema, quantitative factor selection and an outcome tracker. Extensive, but rigid output demands can exceed available evidence.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 2.5/5. Actual -5…+5 technical/fundamental/sentiment scores and PE/PB/risk-premium valuation rules. Scenarios exist; the reviewed valuation agent's DCF docstring is not backed by a DCF implementation.

### C3 Differentiated causal mechanisms

Accepted score: 2.5/5. CIO weights differ by investor and filter incompatible arguments. Stage-two value/quality/growth dimensions are OHLCV proxies, including negative two-year price return as a book/price proxy, rather than authentic master fundamentals.

### C4 Substance over persona and evidence discipline

Accepted score: 3/5. Distinguishes missing cash flow, NA and zero and checks financial-unit anomalies. It describes simulation rather than literal investors, but demands qualitative inference with missing data and fixed forecast slots; attribution mostly relies on slogans.

Static base: 56.47/100.

Review conclusion: Substantive analyst orchestration and prediction tracking rather than README-only master labels.

### Material limitations

- Stage-two value/quality/growth use price-volume proxies; a backtest gain would not validate Graham NCAV, Buffett moat or Fisher growth reasoning.
- Valuation fallback pe_pct = value or 50 discards a valid zero percentile.
- Required targets and short-term forecast slots can force unsupported precision.
- Accuracy tracking measures directional agreement over 14/90/365 days, not master fidelity; holidays and split-adjusted prices need attention.

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

Qlib stage two masks dates to as-of and uses prior-day regime data. Factor-IC calibration still needs a train/test-separation review. Its 365-day prediction-history fallback cannot reconstruct 2015. No authentic 2015 master opinions were established.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [analysis/agents/valuation_agent.py](https://github.com/freenowill/stock-fish/blob/f1feea00238ba39804551d144e5a9ac7ee88f443/analysis/agents/valuation_agent.py)
- [memory/masters/accuracy.py](https://github.com/freenowill/stock-fish/blob/f1feea00238ba39804551d144e5a9ac7ee88f443/memory/masters/accuracy.py)
- [LICENSE](https://github.com/freenowill/stock-fish/blob/f1feea00238ba39804551d144e5a9ac7ee88f443/LICENSE)
- [analysis/agents/cio_prompts.py](https://github.com/freenowill/stock-fish/blob/f1feea00238ba39804551d144e5a9ac7ee88f443/analysis/agents/cio_prompts.py)
- [analysis/scoring.py](https://github.com/freenowill/stock-fish/blob/f1feea00238ba39804551d144e5a9ac7ee88f443/analysis/scoring.py)
- [qlib-zh/scripts/practice/stage2_master_strategy.py](https://github.com/freenowill/stock-fish/blob/f1feea00238ba39804551d144e5a9ac7ee88f443/qlib-zh/scripts/practice/stage2_master_strategy.py)

<a id="project-15"></a>
## MichaelRochonnn/buffett-investment-research

[Repository](https://github.com/MichaelRochonnn/buffett-investment-research) · commit a3a1e9ff5ff5807333ffeb75a314ee093afd95a0 · sampled stars 64

Popularity rank: 15. Raw source-quality rank: 8 of 21. License-eligible source rank: 6.

Investors or lenses: Warren Buffett.

Coverage limit: Coverage is limited to the accepted inspected repository files; investor labels are not authenticated original methods.

### C1 Method completeness and analytical detail

Accepted score: 3.5/5. Primary-source-first workflow covers exact entity, business, moat, management incentives/candor, capital allocation, financing, normalized owner earnings, valuation, confidence/missing facts and kill criteria. SEC helper gives concrete raw inputs. Sector exceptions and precise account reconciliation are missing.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 2.5/5. Seven dimensions scored 0-5 and CFO-maintenance-capex proxy are native; memo demands a conservative value range, assumptions and margin of safety. But component anchors/aggregation/thresholds, discount-growth-horizon equations and sensitivity arithmetic are absent; score is heuristic rather than reproducible.

### C3 Differentiated causal mechanisms

Accepted score: 3/5. Moat must show in unit economics, incremental retained returns, cash conversion and pricing/customer retention; compares per-share capital allocation and one-year frozen capital markets. Good company causality, though little explicit competing-hypothesis discrimination or price-implied expectations.

### C4 Substance over persona and evidence discipline

Accepted score: 4/5. Framework-based verdict, no impersonation, primary evidence preferred, source links, explicit missing facts, outside-competence/insufficient-evidence pass modes and normalized earnings assumptions. Helper warnings correctly call owner-earnings proxy a shortcut.

Static base: 62.35/100.

Review conclusion: First controlled Buffett-company benchmark choice among these eight. Use supplied point-in-time facts, verify entity/durations/debt manually, and require the native 0-5 ratings to expose reasons instead of pretending they are calibrated.

### Material limitations

- Seven 0-5 dimensions have no anchors, total weights or hard numeric bands; high total cannot override hard-filter failures but reproducibility is not specified
- Valuation asks for a conservative range but does not implement DCF, earnings capitalization, equity/enterprise-value bridge or sector-specific formula
- SKILL command hardcodes an author-specific installation location rather than resolving the current installation path
- SEC choose_fact sorts by FY, filed date, frame across tags with no as-of bound, end/start-duration checks or same-accession reconciliation; latest fiscal-year comparative figures can represent a prior period
- Debt fields may overlap depending on issuer/tag and missing components default to zero; net cash/debt and CFO-capex can combine mismatched fiscal periods
- Fuzzy/partial name matching silently selects one entity; SEC User-Agent contact uses a placeholder rather than a real operator contact

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

- 2015_route: Strongest practical company-research candidate in this group, conditional on frozen inputs and bypassing or correcting latest-only SEC helper. Separate primary Buffett comparator needed.
- leakage: Current ticker universe causes survivorship bias; recent submissions may omit older pages; annual facts can include later restatements. No cutoff argument; timeline includes post-2015 decisions/lessons.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [SKILL.md](https://github.com/MichaelRochonnn/buffett-investment-research/blob/a3a1e9ff5ff5807333ffeb75a314ee093afd95a0/SKILL.md)
- [LICENSE](https://github.com/MichaelRochonnn/buffett-investment-research/blob/a3a1e9ff5ff5807333ffeb75a314ee093afd95a0/LICENSE)
- [README.md](https://github.com/MichaelRochonnn/buffett-investment-research/blob/a3a1e9ff5ff5807333ffeb75a314ee093afd95a0/README.md)
- [references/framework.md](https://github.com/MichaelRochonnn/buffett-investment-research/blob/a3a1e9ff5ff5807333ffeb75a314ee093afd95a0/references/framework.md)
- [references/memo-template.md](https://github.com/MichaelRochonnn/buffett-investment-research/blob/a3a1e9ff5ff5807333ffeb75a314ee093afd95a0/references/memo-template.md)
- [references/timeline.md](https://github.com/MichaelRochonnn/buffett-investment-research/blob/a3a1e9ff5ff5807333ffeb75a314ee093afd95a0/references/timeline.md)
- [scripts/sec_company_snapshot.py](https://github.com/MichaelRochonnn/buffett-investment-research/blob/a3a1e9ff5ff5807333ffeb75a314ee093afd95a0/scripts/sec_company_snapshot.py)

<a id="project-16"></a>
## AskRoundtable/expert-skills

[Repository](https://github.com/AskRoundtable/expert-skills) · commit a7ea0121e88d6fcbf6ffc57833b0cac7cf9cab74 · sampled stars 54

Popularity rank: 16. Raw source-quality rank: 14 of 21. License-eligible source rank: 12.

Investors or lenses: Charlie Munger.

Coverage limit: Coverage is limited to the accepted inspected repository files; investor labels are not authenticated original methods.

### C1 Method completeness and analytical detail

Accepted score: 2.5/5. Detailed general decision pipeline with prereq feasibility, chain-of-consequences, case-specific anomalies, mitigations and blind spots; not a full stock accounting/management/valuation workflow.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 1.5/5. Investing margin-of-safety examples and opportunity-cost comparisons exist, but no required financial inputs, owner earnings, equity valuation equations or stock-quality score. Confidence values measure evidence/situation quality, not expected investment return.

### C3 Differentiated causal mechanisms

Accepted score: 4/5. Engine forces alternative pattern, specific supporting cue, model relevance, second/third-order causal chains, falsification and at least two case-specific anomalies. Judgment filters explicitly demand a differentiated reason rather than opposite-to-consensus slogans.

### C4 Substance over persona and evidence discipline

Accepted score: 3.5/5. Method dominates roleplay and admits domain limits; evidence-confidence matrix and hammer check reduce projection. However primary-source facts/dates are not demanded systematically, references mix biographical inference with attributed quotes, and numeric calibration rules are subjective.

Static base: 53.53/100.

Review conclusion: Useful challenger/auditor module for assumptions and falsification. Do not pick it as the main quantitative stock engine; distinguish Paul Graham and confidence scores.

### Material limitations

- Do not count expert-graham as Benjamin Graham; module explicitly displays Paul Graham and startups/growth
- judgment_filter_score=7 is module metadata, not a 7-point company investment score; 0-1 values are confidence
- Claimed +18% to +41% Munger improvement in README has no raw outputs/runs/test harness in pinned tree; not independently verified
- Required terminology smoke-test policy can reward naming Inversion/MOS/Incentive/Competence without proving economic reasoning
- References to expert-taleb/expert-duke/expert-housel/expert-martin/quotes.md occur but those modules/files are absent from this repository tree
- No point-in-time financial data tooling, source ledger or valuation engine

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

- 2015_route: Can test Munger decision/falsification reasoning with frozen evidence, but not a native valuation benchmark.
- leakage: References include Apple-era hindsight and modern allied books; no cutoff or dated fixtures; authentic investor view must not be inferred from generic model outputs.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [LICENSE](https://github.com/AskRoundtable/expert-skills/blob/a7ea0121e88d6fcbf6ffc57833b0cac7cf9cab74/LICENSE)
- [README.md](https://github.com/AskRoundtable/expert-skills/blob/a7ea0121e88d6fcbf6ffc57833b0cac7cf9cab74/README.md)
- [skills/expert-munger/SKILL.md](https://github.com/AskRoundtable/expert-skills/blob/a7ea0121e88d6fcbf6ffc57833b0cac7cf9cab74/skills/expert-munger/SKILL.md)
- [skills/expert-engine/SKILL.md](https://github.com/AskRoundtable/expert-skills/blob/a7ea0121e88d6fcbf6ffc57833b0cac7cf9cab74/skills/expert-engine/SKILL.md)
- [skills/expert-engine/references/epistemic-audit.md](https://github.com/AskRoundtable/expert-skills/blob/a7ea0121e88d6fcbf6ffc57833b0cac7cf9cab74/skills/expert-engine/references/epistemic-audit.md)
- [skills/expert-munger/references/models-core.md](https://github.com/AskRoundtable/expert-skills/blob/a7ea0121e88d6fcbf6ffc57833b0cac7cf9cab74/skills/expert-munger/references/models-core.md)
- [skills/expert-munger/references/judgment-filters.md](https://github.com/AskRoundtable/expert-skills/blob/a7ea0121e88d6fcbf6ffc57833b0cac7cf9cab74/skills/expert-munger/references/judgment-filters.md)
- [skills/expert-munger/references/blind-spots.md](https://github.com/AskRoundtable/expert-skills/blob/a7ea0121e88d6fcbf6ffc57833b0cac7cf9cab74/skills/expert-munger/references/blind-spots.md)
- [skills/expert-munger/references/sources.md](https://github.com/AskRoundtable/expert-skills/blob/a7ea0121e88d6fcbf6ffc57833b0cac7cf9cab74/skills/expert-munger/references/sources.md)
- [skills/expert-graham/SKILL.md](https://github.com/AskRoundtable/expert-skills/blob/a7ea0121e88d6fcbf6ffc57833b0cac7cf9cab74/skills/expert-graham/SKILL.md)

<a id="project-17"></a>
## kangarooking/poor-charlies-almanack-skill

[Repository](https://github.com/kangarooking/poor-charlies-almanack-skill) · commit d477e516920995b6e54d66c7441f17048188303a · sampled stars 44

Popularity rank: 17. Raw source-quality rank: 15 of 21. License-eligible source rank: 13.

Investors or lenses: Charlie Munger.

Coverage limit: Coverage is limited to the accepted inspected repository files; investor labels are not authenticated original methods.

### C1 Method completeness and analytical detail

Accepted score: 2.5/5. Structured inversion, value assessment, incentives, scale economics, dual-track analysis and mandatory pass/fail/more-info checklist. Company financial-statement inputs, debt analysis and valuation detail are major gaps.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 2/5. Value assessment explicitly requires safety-margin percentage and three ways thesis could be wrong, but supplies no intrinsic-value calculation, financial dataset, score component rules or numeric valuation bridge.

### C3 Differentiated causal mechanisms

Accepted score: 3.5/5. Inversion mandates at least five observable failure paths/severity/mitigation; Darwin method uses 1-3 falsifiable assumptions and >=3 counterarguments each; dual-track checks rational economics versus personal/incentive bias and pauses at >=2 biases. Scale module weighs advantage against bureaucracy.

### C4 Substance over persona and evidence discipline

Accepted score: 3/5. Reading/interpretation/application/execution/boundary separation, unknown branches and explicit survivorship/method limitations help. Source attribution is chapter-level book material without a primary-evidence retrieval protocol; self-generated V1/V2/V3 claims are not empirical performance.

Static base: 52.94/100.

Review conclusion: Useful source-structured Munger risk/falsification toolkit. More substantive than persona-only prompts, but a supplementary reviewer rather than a valuation engine.

### Material limitations

- No true stock valuation model or transparent investment score despite value-assessment title
- test-prompts.json tests activation/expected behavior; many success rates explicitly pending. V2 predictive-power means author-derived example answers, not held-out investment validation
- Five failure paths/three counterarguments/two bias pause rules are modern author heuristics and may force low-quality extra examples if evidence is thin
- Some source-context distortions: Darwinian example presents Harvard-school performance as historical instead of a likely counterfactual; requires checking original book before quote reuse
- No publication-date cutoff, finance APIs, company fixtures or runnable benchmark

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

- 2015_route: Good Munger falsification/decision adjunct if supplied frozen company data; cannot independently deliver reproducible 2015 stock value.
- leakage: Past success cases and modern interpretations can leak outcomes; no native as-of control or authentic comparator.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [LICENSE](https://github.com/kangarooking/poor-charlies-almanack-skill/blob/d477e516920995b6e54d66c7441f17048188303a/LICENSE)
- [README.md](https://github.com/kangarooking/poor-charlies-almanack-skill/blob/d477e516920995b6e54d66c7441f17048188303a/README.md)
- [inversion-thinking/SKILL.md](https://github.com/kangarooking/poor-charlies-almanack-skill/blob/d477e516920995b6e54d66c7441f17048188303a/inversion-thinking/SKILL.md)
- [value-assessment/SKILL.md](https://github.com/kangarooking/poor-charlies-almanack-skill/blob/d477e516920995b6e54d66c7441f17048188303a/value-assessment/SKILL.md)
- [dual-track-analysis/SKILL.md](https://github.com/kangarooking/poor-charlies-almanack-skill/blob/d477e516920995b6e54d66c7441f17048188303a/dual-track-analysis/SKILL.md)
- [checklist-decision/SKILL.md](https://github.com/kangarooking/poor-charlies-almanack-skill/blob/d477e516920995b6e54d66c7441f17048188303a/checklist-decision/SKILL.md)
- [darwinian-objectivity/SKILL.md](https://github.com/kangarooking/poor-charlies-almanack-skill/blob/d477e516920995b6e54d66c7441f17048188303a/darwinian-objectivity/SKILL.md)
- [incentive-analysis/SKILL.md](https://github.com/kangarooking/poor-charlies-almanack-skill/blob/d477e516920995b6e54d66c7441f17048188303a/incentive-analysis/SKILL.md)
- [scale-advantage-analysis/SKILL.md](https://github.com/kangarooking/poor-charlies-almanack-skill/blob/d477e516920995b6e54d66c7441f17048188303a/scale-advantage-analysis/SKILL.md)
- [verified.md](https://github.com/kangarooking/poor-charlies-almanack-skill/blob/d477e516920995b6e54d66c7441f17048188303a/verified.md)
- [value-assessment/test-prompts.json](https://github.com/kangarooking/poor-charlies-almanack-skill/blob/d477e516920995b6e54d66c7441f17048188303a/value-assessment/test-prompts.json)

<a id="project-18"></a>
## Wechat-ggGitHub/investment-masters-skill

[Repository](https://github.com/Wechat-ggGitHub/investment-masters-skill) · commit 0f99e98f49f3ffb050134195829f7569c554b450 · sampled stars 42

Popularity rank: 18. Raw source-quality rank: 20 of 21. License-eligible source rank: blocked at pin.

Investors or lenses: Buffett, Munger, Lynch, Marks, Dalio.

Coverage limit: File-backed implemented methods; source audit samples are enumerated in pinned_sources. Corroborating influences are separately described, not separate agents.

### C1 Method completeness and analytical detail

Accepted score: 3/5. Substantial five-master Chinese reference compendium and cross-master checklist; operational inputs/calculation steps/missing-data rules limited.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 1.5/5. PEG/checklist mechanics partial and the deep Lynch formula multiplies PE/G by100, failing standard units; no score/value bridge.

### C3 Differentiated causal mechanisms

Accepted score: 2.5/5. Recognizable six categories, moat/cycle/inversion, but mostly summaries and successful-case lessons rather than falsifiable mechanisms.

### C4 Substance over persona and evidence discipline

Accepted score: 2/5. References are overwhelmingly secondary/social/quote collections; unsupported certainty, little current-fact/evidence separation, malformed frontmatter.

Static base: 43.53/100.

Review conclusion: 适合中文概念参考；算式/来源/import风险较大

### Material limitations

- PEG公式×100错误；多为二手文章/语录与事后成功叙述；无时点约束/数值评分；SKILL frontmatter无法用安全YAML解析

License at pin: readme_claim_only. blocked pending explicit reuse permission or verified license

### Historical readiness at the source freeze

Historical case narratives, many2025/2026 secondary citations and current-view sections. No source publication cutoff or native benchmark. Strong hindsight/attribution controls would be needed.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [SKILL.md](https://github.com/Wechat-ggGitHub/investment-masters-skill/blob/0f99e98f49f3ffb050134195829f7569c554b450/SKILL.md)
- [references/lynch.md](https://github.com/Wechat-ggGitHub/investment-masters-skill/blob/0f99e98f49f3ffb050134195829f7569c554b450/references/lynch.md)
- [references/buffett.md](https://github.com/Wechat-ggGitHub/investment-masters-skill/blob/0f99e98f49f3ffb050134195829f7569c554b450/references/buffett.md)

<a id="project-19"></a>
## videGavin/serenity-analyst

[Repository](https://github.com/videGavin/serenity-analyst) · commit 3475c9ade62efc69774c2785589c1a75fe031c13 · sampled stars 36

Popularity rank: 19. Raw source-quality rank: 17 of 21. License-eligible source rank: 15.

Investors or lenses: Serenity.

Coverage limit: Coverage is limited to the accepted inspected repository files; investor labels are not authenticated original methods.

### C1 Method completeness and analytical detail

Accepted score: 3/5. Seven-step supply-chain workflow, eleven-layer graph, 4 chokepoint criteria, sizing tiers, invalidation and packaging example are detailed sector research. Traditional balance-sheet/accounting/management and sector cash-value bridge are sparse.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 2/5. Individual ticker output and ASP x forward capacity/peer market-cap mismatch exist; output score is Strong/Weak/Fake/Avoid categorical, not transparent numeric component score. Revenue-capacity opportunity lacks the profit/cash/sharecount bridge to intrinsic value.

### C3 Differentiated causal mechanisms

Accepted score: 3.5/5. Recursive upstream mapping, qualification barriers, supplier concentration, material revenue/design-out failure tests and cyclical capex timing are concrete causal tools. Entry criterion of unanimous negativity risks substituting contrarian sentiment for demonstrated mispricing.

### C4 Substance over persona and evidence discipline

Accepted score: 2/5. Demands date/number/quote evidence and labels self-reported returns, but treats post-based graph edges as confirmed facts without URLs and unverifiable source archive. Uses imagined What Serenity would do, assertive entry/LEAPS/short instructions and rigid anti-PE rules. Internal pipeline/revenue drift is a substantial reliability gap.

Static base: 51.76/100.

Review conclusion: Sector idea-generation reference with high data-integrity risk. Prefer lanfuli evidence gate; do not shortlist for authentic 2015 testing or use static graph as verified financial facts.

### Material limitations

- Graph SIVE importance says first 3 months revenue +77%; lanfuli exemplar and this repo methodology elsewhere refer to pipeline growth. These concepts are economically different; source claim needs re-verification
- confirmed_supply_edges use tweet text only, no individual source URL/date or independent customer/regulatory evidence; multi-hop supplier implication is not transitive proof of actual orders
- verification.md claims grep of tweets_original.md and no major hallucination, but underlying archive is absent from tree; author verification is not independently reproducible
- Static positions/market caps through May 2026, mixed price vs market-cap units, no corporate-action checks
- SKILL presents <$1B institutional threshold and unanimity of bearish sentiment as entry evidence without fund-specific mandate support
- X lookup takes only one page, lacks end_time cutoff and defaults --since 2025-07-01; recent fallback drops historical start constraint

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

- 2015_route: Cannot supply authentic Serenity 2015 comparator: this source corpus/account starts July 2025. Only an explicitly later-framework transfer exercise is possible.
- leakage: Modern static graph/positions/winners must be excluded from a 2015 dossier; script has no end_time and could retrieve later posts even with an early since date.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [SKILL.md](https://github.com/videGavin/serenity-analyst/blob/3475c9ade62efc69774c2785589c1a75fe031c13/SKILL.md)
- [LICENSE](https://github.com/videGavin/serenity-analyst/blob/3475c9ade62efc69774c2785589c1a75fe031c13/LICENSE)
- [README.md](https://github.com/videGavin/serenity-analyst/blob/3475c9ade62efc69774c2785589c1a75fe031c13/README.md)
- [.env.example](https://github.com/videGavin/serenity-analyst/blob/3475c9ade62efc69774c2785589c1a75fe031c13/.env.example)
- [references/methodology.md](https://github.com/videGavin/serenity-analyst/blob/3475c9ade62efc69774c2785589c1a75fe031c13/references/methodology.md)
- [references/verification.md](https://github.com/videGavin/serenity-analyst/blob/3475c9ade62efc69774c2785589c1a75fe031c13/references/verification.md)
- [references/supply_chain_graph.json](https://github.com/videGavin/serenity-analyst/blob/3475c9ade62efc69774c2785589c1a75fe031c13/references/supply_chain_graph.json)
- [scripts/search_serenity.mjs](https://github.com/videGavin/serenity-analyst/blob/3475c9ade62efc69774c2785589c1a75fe031c13/scripts/search_serenity.mjs)
- [examples/advanced-packaging-case.md](https://github.com/videGavin/serenity-analyst/blob/3475c9ade62efc69774c2785589c1a75fe031c13/examples/advanced-packaging-case.md)

<a id="project-20"></a>
## LI-Jialu/investor-panel-skill

[Repository](https://github.com/LI-Jialu/investor-panel-skill) · commit 858ede0115f7387dd0ad825a563deec09d29bd1d · sampled stars 33

Popularity rank: 20. Raw source-quality rank: 3 of 21. License-eligible source rank: blocked at pin.

Investors or lenses: Buffett, Munger, Graham, Lynch, Fisher, Damodaran, Ackman, Wood, Burry, Pabrai, Druckenmiller, Taleb, Simons, Greenblatt, Klarman, Marks, Soros, Tepper, Templeton, Li Lu, Nick Sleep, Terry Smith, Swensen, Robertson, Jhunjhunwala, Serenity.

Coverage limit: File-backed implemented methods; source audit samples are enumerated in pinned_sources. Corroborating influences are separately described, not separate agents.

### C1 Method completeness and analytical detail

Accepted score: 4/5. 26 investor profiles, six request modes, evidence pack and detailed output contracts; some deep-profile paragraphs are repeated templates.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 3/5. Company thesis, DCF/reverse-DCF and implied-expectation discipline, but no concrete native financial scoring/math engine.

### C3 Differentiated causal mechanisms

Accepted score: 4/5. Distinct competing quality, value, macro, forensic, tail and scarcity lenses; vetoes and kill criteria.

### C4 Substance over persona and evidence discipline

Accepted score: 4/5. No impersonation/endorsement, evidence grading, dated-data confidence caps, explicit missing facts; broad source map rather than precise lineage.

Static base: 72.94/100.

Review conclusion: 多视角研究设计好；直接复用前需厘清授权

### Material limitations

- 深档案有较多通用模板；来源地图多为目标类型而非逐条可定位出处；置信分不是投资评分；无执行代码/2015实证

License at pin: not_found. blocked pending explicit reuse permission or verified license

### Historical readiness at the source freeze

Evidence pack demands filing/price dates and confidence caps; prompt suite tests missing facts and named-lens distinctiveness. These are proposed regression cases, not observed 2015 tests.

Later comparable replay status: Not tested in the accepted V1 three-project replay.

### Exact inspected public files

- [skills/investor-panel/SKILL.md](https://github.com/LI-Jialu/investor-panel-skill/blob/858ede0115f7387dd0ad825a563deec09d29bd1d/skills/investor-panel/SKILL.md)
- [skills/investor-panel/references/output-contract.md](https://github.com/LI-Jialu/investor-panel-skill/blob/858ede0115f7387dd0ad825a563deec09d29bd1d/skills/investor-panel/references/output-contract.md)
- [skills/investor-panel/references/evidence-pack.md](https://github.com/LI-Jialu/investor-panel-skill/blob/858ede0115f7387dd0ad825a563deec09d29bd1d/skills/investor-panel/references/evidence-pack.md)
- [skills/investor-panel/references/people/deep/warren-buffett.md](https://github.com/LI-Jialu/investor-panel-skill/blob/858ede0115f7387dd0ad825a563deec09d29bd1d/skills/investor-panel/references/people/deep/warren-buffett.md)
- [skills/investor-panel/references/people/deep/aswath-damodaran.md](https://github.com/LI-Jialu/investor-panel-skill/blob/858ede0115f7387dd0ad825a563deec09d29bd1d/skills/investor-panel/references/people/deep/aswath-damodaran.md)
- [skills/investor-panel/references/evals/prompt-test-suite.md](https://github.com/LI-Jialu/investor-panel-skill/blob/858ede0115f7387dd0ad825a563deec09d29bd1d/skills/investor-panel/references/evals/prompt-test-suite.md)
- [skills/investor-panel/references/evals/persona-fidelity-benchmark.md](https://github.com/LI-Jialu/investor-panel-skill/blob/858ede0115f7387dd0ad825a563deec09d29bd1d/skills/investor-panel/references/evals/persona-fidelity-benchmark.md)

<a id="supplement"></a>
## finterm-ai/investment-skills

[Repository](https://github.com/finterm-ai/investment-skills) · commit 7235d3411601036cc79137fa0aec0d587f2c8e19 · sampled stars 4

Popularity rank: supplement outside top20. Raw source-quality rank: 1 of 21. License-eligible source rank: 1.

Investors or lenses: Warren Buffett.

Coverage limit: File-backed implemented methods; source audit samples are enumerated in pinned_sources. Corroborating influences are separately described, not separate agents.

### C1 Method completeness and analytical detail

Accepted score: 5/5. All8modules fully inspected:65 cards implement concrete decision actions, outputs, limits and source lineage, including accounting, governance, capital allocation, correlated stress and12industry/instrument overlays. Native stock scoring scope still limited as recorded under C2.

### C2 Stock-specific thesis valuation and quantifiability

Accepted score: 3.5/5. Thesis evaluation and defendable owner-cash valuation range/sensitivity; expressly no aggregate investment score or thesis invention.

### C3 Differentiated causal mechanisms

Accepted score: 4.5/5. Causal moat attack tests, capital-trap alternatives, incremental-return runway and disconfirming evidence.

### C4 Substance over persona and evidence discipline

Accepted score: 5/5. All8modules preserve missing-data blocked branches, causal alternatives and qualifications; entrypoint separates facts/calculations/inference, primary evidence receipt and anti-injection. Guidance lineage is distinct from proof.

Static base: 87.06/100.

Review conclusion: 证据约束最强；适合研究机器人底层，缺原生总评分

### Material limitations

- 仅Buffett主框架；明确禁止凭空造论点、汇总买卖建议；无原生投资评分；路由器不是估值执行器

License at pin: verified_mit. pass with notice preservation and third-party-rights caveats

### Historical readiness at the source freeze

Exact periods, sources and blocked calculations demanded. Source corpus includes post-2015 lessons; case input cutoff must be enforced separately. No historical stock-reasoning benchmark found.

Later comparable replay status: V1 accepted wrapped replay; numeric run results not republished.

### Exact inspected public files

- [skills/buffett-investment-framework/SKILL.md](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/skills/buffett-investment-framework/SKILL.md)
- [skills/buffett-investment-framework/references/05-valuation.md](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/skills/buffett-investment-framework/references/05-valuation.md)
- [skills/buffett-investment-framework/references/02-business-economics.md](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/skills/buffett-investment-framework/references/02-business-economics.md)
- [skills/buffett-investment-framework/references/00-source-key.md](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/skills/buffett-investment-framework/references/00-source-key.md)
- [skills/buffett-investment-framework/scripts/framework.py](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/skills/buffett-investment-framework/scripts/framework.py)
- [LICENSE](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/LICENSE)
- [skills/buffett-investment-framework/references/01-decision-posture.md](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/skills/buffett-investment-framework/references/01-decision-posture.md)
- [skills/buffett-investment-framework/references/03-management-governance.md](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/skills/buffett-investment-framework/references/03-management-governance.md)
- [skills/buffett-investment-framework/references/04-financial-reality.md](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/skills/buffett-investment-framework/references/04-financial-reality.md)
- [skills/buffett-investment-framework/references/06-capital-allocation.md](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/skills/buffett-investment-framework/references/06-capital-allocation.md)
- [skills/buffett-investment-framework/references/07-risk-monitoring.md](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/skills/buffett-investment-framework/references/07-risk-monitoring.md)
- [skills/buffett-investment-framework/references/08-specialized-overlays.md](https://github.com/finterm-ai/investment-skills/blob/7235d3411601036cc79137fa0aec0d587f2c8e19/skills/buffett-investment-framework/references/08-specialized-overlays.md)
