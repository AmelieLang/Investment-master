# Investment-master

Research repository for the Investment-master Skill and two planned historical replay collections.

The reviewed source-only checkpoint is preserved under [skill/](skill/), with all 192 files and internal relative paths unchanged. Start with [SKILL.md](skill/SKILL.md); [PUBLICATION.md](skill/PUBLICATION.md) documents verification and scope, and [PUBLIC-MANIFEST.json](skill/PUBLIC-MANIFEST.json) hashes the current source inventory. Packaging metadata inside the checkpoint retains its historical pre-publication state.

Research catalogue: [frozen top20 comparison and finterm supplement](research/catalogue-review/README.md).

Stage handoff: [Investment-master V2 phase report](research/phase-handoff/Investment-master-V2-phase-handoff.zh-CN.md).

Source archive: `investment-master-public-source-projection-v1.zip`, SHA-256 `c2675e5abf8db00d636ca1e99217628bda2ddb1271015f6077cda8b1eb9fab1e`.

Historical data is accepted for five securities and held for fourteen; there are zero actual V2 opinions; the final runtime and adapter were not accepted after the three-round limit; no completed backtest or activation is claimed. No completed backtests, financial performance results, investor endorsements, or activated chatbot are claimed.

Source and future eligible results must retain their attribution and applicable rights. FMP publication rights remain unresolved; raw FMP data and FMP-derived financial outcomes are excluded.

Original software licenses and research attributions remain in the source tree. Their scopes differ; see [THIRD-PARTY-NOTICES.md](skill/THIRD-PARTY-NOTICES.md). This repository makes no blanket MIT claim over third-party publications or data.

## Latest manual trial (2026-10-14)

One separate manual static [NVDA + ARK trial](research/single-stock-trials/NVDA-ARK-2025-12-31/README.md) was completed on 2026-10-14. It used an extracted subset of nine procedural cards from the [finterm framework](https://github.com/AmelieLang/Investment-master/blob/12472e955a58bd873338ac068088df5cd25ee014/skill/vendor/finterm/SKILL.md) and three selected [ARK method rules](https://github.com/AmelieLang/Investment-master/blob/12472e955a58bd873338ac068088df5cd25ee014/skill/tech-historical-extension/ark-research-team.json), within the research scope of the [Skill entrypoint](https://github.com/AmelieLang/Investment-master/blob/12472e955a58bd873338ac068088df5cd25ee014/skill/SKILL.md). A separate, explicit analyst-created earnings/P-E scenario calculation produced the numerical outputs; it did not execute the old full runtime or replicate ARK's complete quantitative model.

The earlier phase-status paragraph remains the preserved historical snapshot; this new static case is counted separately. No complete benchmark, runtime/UI acceptance, runtime activation, trades or deployment is claimed.

## META two-framework case (2026-10-14)

The [META case](research/single-stock-trials/META-two-master-2025-12-31/README.md) preserves two independent frameworks: finterm Buffett and community Coleman. Four initial calls plus two controlled Coleman repeats were completed for a historical 2025-12-31 analysis, with separate judgments and no unified score. Future-price outputs are conditional analyst scenarios, not the investors' actual forecasts.

The case retains six original reports, calculations, exact Skill sources/licenses and independent audits. Neither Skill contains its own data-fetching client; the host supplies the public-data inputs. No production Feishu @ chain, runtime activation or complete benchmark is claimed.
