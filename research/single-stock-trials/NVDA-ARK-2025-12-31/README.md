# NVDA + ARK: one completed static research trial

Completed 2026-10-14. Decision-information cutoff: 2025-12-31.

Read [the Chinese opinion](output/raw-opinion.md), [scenario table](output/NVDA-ARK-scenarios.csv), and [independent review](audit/independent-review.md).

A fresh native task requested gpt-6.1-sol with xhigh reasoning and isolated supplied inputs. Astra independently reviewed the result. This is a manual static case, not acceptance of the old execution runtime, UI or 152-cell benchmark. No historical raw output was overwritten. No 2026 outcome comparison is included.

The completed analysis uses public-source financial facts, qualitative ARK method rules, explicit analyst-created revenue/net-income/share-count/P-E scenarios, and manager-level lagged holdings checks. Future targets are conditional; they are not ARK forecasts or current intrinsic values. Full learning curves and owner-cash valuation remain unsupported.

The source method selection is preserved under input/method with its original license and source receipts. Complete FMP/raw financial packets are deliberately not redistributed in this public artifact. Public-source facts and links needed for the calculation appear in the report and scenarios. The original internal input manifest was verified by the reviewer, but is not reproduced as a claim that this public subset is the complete inference input.

Run python audit/recompute.py from any directory to independently check the scenario arithmetic; 58 checks passed. Inputs and original opinion are preserved. No trades, production activation or deployment occurred.
