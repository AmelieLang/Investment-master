# Independent META arithmetic review

Generated: 2026-10-14T05:02:59.686298+00:00

Independent financial arithmetic only. No outside/current/outcome sources, no producer-code execution, no original-output edits. Source-value binding against frozen facts; all emitted scalar calculation outputs, conditional scenarios and reverse cash models independently recomputed. Report comparisons are explicitly enumerated line-bound claims.

## Results
- 4249 scalar/reference/structural checks; 0 failed.
- 142 explicitly enumerated report rounded-number claims; 1 failed.
- Numerical outputs and formula-documentation findings are distinguished below.

- buffett-base: 1750 checks (250 arithmetic scalar outputs); 67 report rounded claims.
- buffett-enriched: 821 checks (162 arithmetic scalar outputs); 25 report rounded claims.
- coleman-base: 857 checks (69 arithmetic scalar outputs); 29 report rounded claims.
- coleman-enriched: 803 checks (74 arithmetic scalar outputs); 21 report rounded claims.
- shared_inputs: 16 checks (0 arithmetic scalar outputs); 0 report rounded claims.
- paired_buffett: 2 checks (2 arithmetic scalar outputs); 0 report rounded claims.

## Findings
- coleman-enriched / ttm_company_fcf / identifier_documentation_issue: Calculation ID occurs 2 times: a TTM bridge and a CFO/PPE/lease reconciliation. Outputs agree, but ID-based lookup is ambiguous.
- coleman-base / stress_return / report_rounding_or_context_error: Stress CAGR is -8.523690872624346%, which rounds to -8.52%; frozen report says -8.53%. Difference is 0.01 percentage point in displayed rounding only; calculations and future price remain correct.

## Critical formula and unit coverage
- Reverse owner cash factors discount each year-end cash flow and the year-five terminal value; solved starting owner cash is a hypothetical equity-cash burden, not observed FCFF or owner earnings.
- Coleman terminal prices are undiscounted future scenario prices. Price-only CAGR is correctly calculated against historical price; dividends are excluded rather than silently labeled total return.
- Stale October actual shares are converted from shares to shares million before capitalization; Q3 diluted weighted-average share counts are explicitly proxy denominators.
- Company FCF and FCF-minus-SBC are never promoted by this audit to FCFF or complete removable equity cash. No enterprise-value bridge or excess cash credit is invented.
- Buffett enriched pre-freeze formula-percent documentation defects were corrected before freeze. The frozen output formulas include ×100 and numeric percent outputs agree.

## Audited snapshots
- buffett-base: calculations 53474ef4edb552dbc789da93ddceb9a0dd670a11600bac6668ee8b5c8e507cc5; report 245bf46d0de295723c421c69b032c29f53b130e8e80c28758edb137c90cb2397.
- buffett-enriched: calculations 3287021cd7527953ced240c30d4ca9c9d7be7f723d133bea36f52ebffa6003ab; report fce1f59c98ebc18514ad1496883cc0eedd4a90db4075eee787aad452cd82532b.
- coleman-base: calculations 9b9c6f62fb6d3ec4514e65a50204352437deff462dc72e4aebca8b0036234443; report ecd9e65cec027977bde14cbff79e9254a9c609b944d4cef6399c4ab52b125e45.
- coleman-enriched: calculations 4303da3125a5a4ee02a1314d7f9d5a2f5a0e123d8c8781b60c1ab82be80c32b0; report c3bfab4d491e556bba5a0faf4a5ea28b2640f601bd9b905c4b751f775c80325e.

## Counts by category
- source_binding: 2229
- structural: 322
- source_reference: 600
- unit_label: 292
- arithmetic: 557
- unit_dimension: 213
- reconciliation_boolean: 1
- scenario_scope: 12
- derived_anchor: 16
- freeze_hash: 7

## Skipped / outside scope
- all / original_primary_source_revalidation: Not within this independent arithmetic task; source facts were audited separately. Bindings here check run inputs against frozen facts.json.
- all / investment_meaning_or_assumption_plausibility: Separate qualitative reviewer handles assumptions and valuation meaning; this audit checks equations, units, historical anchors and explicit labels only.
- all / non-numeric_branch_assertions_and_metadata: Not arithmetic: provider identity, no future data claims, method selection, prose opinions, unmodeled branches and analyst chosen assumptions are not numerically independently proven.
- all / every_report_numeric_token: Reports contain dates, IDs, method thresholds, assumptions and external material claims. Exact line-bound rounded claims are enumerated; no claim of exhaustive numeric-token audit.

Full check-level observed/recomputed values and exact report contexts are in arithmetic-review.json. Reproduce with python audit/independentrecompute.py.
