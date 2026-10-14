# Static source scoring method

This reproduces the accepted V1 source-audit anchors, unchanged. Scores are reviewer judgments at the frozen pins, not calibrated probabilities. All projects receive C1-C4; only previously tested finalists can receive an observed C5. Source inspection is distinct from native execution and from investor authenticity.

Static source base /100 = 100 × (20×C1 + 30×C2 + 20×C3 + 15×C4) / 425. C1-C4 each range from 0 to 5; half-points are allowed. The 20/30/20/15 weights sum to 85, so normalization is necessary before comparing the source base. Source ranking retains research-eligible but reuse-blocked projects. Quality ties use C2, C4, C1, C3 and sampled stars.

### C1 — Completeness and analytical detail (20%)
0: No usable investing method; placeholder or marketing only.
1: Quotes or general principles; few decision steps.
2: Several relevant concepts/checklists, but major gaps in inputs, economics, management, risk or valuation.
3: Structured workflow covers business, management, financials, valuation and downside, with some specifics and limits.
4: Detailed, source-grounded modules with input requirements, sector exceptions, missing-data handling and useful outputs.
5: Comprehensive but selective decision system, operational definitions, competing explanations, falsification/monitoring and traceable primary-source lineage. Extra pages alone earn nothing.

### C2 — Stock-specific thesis, valuation and quantifiable output (30%)
0: Cannot apply to an individual equity.
1: Qualitative company commentary or generic recommendation; unsupported confidence number is still 1.
2: Explicit company inputs plus partial fundamental tests, heuristic score or simple multiples, but no coherent value bridge.
3: Company-specific thesis and reproducible score OR defensible numerical valuation, with assumptions and material risks; the other component incomplete.
4: Company thesis + value bridge/range + transparent component scores/thresholds, with units, timing, sensitivity and invalidation conditions.
5: All of 4 plus sector-appropriate valuation, reconciliation to reported accounts, stress cases and missing-data abstention; outputs are calculable and decision-useful.
Important: numeric confidence is not valuation or a quality score. A disciplined analytic system that deliberately refuses aggregate investment scoring gets credit for valuation and thesis, but not imaginary scoring functionality.

### C3 — Differentiated, non-consensus mechanisms (20%)
0: Consensus/contrarian slogans or arbitrary opposite stance.
1: Identical generic factor list with investor labels.
2: Some investor-specific tools, but little causal linkage or evidence requirement.
3: Genuine mechanisms (e.g. owner earnings versus accounting earnings, incremental ROIC/reinvestment, forensic balance-sheet risk, reflexivity, credit cycle, six stock categories) linked to observations.
4: Mechanisms become tests, alternative hypotheses, expectations-versus-price analysis, disconfirming evidence and pass rules.
5: Competing hypotheses are operationalized, critical observable differences identified, valuation implication traced, and credible unresolved/consensus conclusions allowed.
Non-consensus is a hypothesis to demonstrate, not a requirement to invent novelty. Merely disagreeing with a mainstream view earns no points.

### C4 — Substance over persona and epistemic discipline (15%)
0: Impersonation/voice dominates; invented facts or authoritative claims encouraged.
1: Mostly roleplay/quotes; little evidence discipline.
2: Useful method mixed with persona; source/date/error controls weak.
3: Method dominates; explicitly separates public-framework inference from actual investor views; missing information and uncertainty acknowledged.
4: Facts, calculations and inference distinguished; primary evidence demanded; causal claims qualified; unavailable inputs stop affected branches.
5: All of 4 plus auditable source mapping, anti-injection/evidence boundary, counterevidence, material numerical checks and robust abstention rules.
Investor voice itself is neutral; it does not add points and cannot compensate for absent method. A fabricated financial fact, quote, action or source is a severe failure even when prose sounds persuasive.


## Evidence and eligibility

A positive source score needs an inspected, pinned implementation file and a rationale. A famous-name label, high star count, prose length or asserted historical return adds no points. Research eligibility requires accessible investor-derived implementation evidence beyond marketing, relevant scope, readable files and a distinct implementation lineage. Verified licensing, third-party rights and safe runtime permissions are separate reuse gates; a high score cannot override them.

No additional stand-alone evidence score is invented. Evidence traceability and epistemic controls contribute mainly to C4, while source-linked criterion rationales explain each C1-C4 judgment. Historical-readiness descriptions are not C5. See COMPARABLE-TESTS.md for C5 fidelity and the separate original-investor statement cross-check.
