# Quantitative decision outputs and compatibility

No new calculation engine is implemented in this bundle. Proposed extra math requires separate reviewed implementation and tests. The accepted R2 request/result schema bytes are preserved exactly. The separate research wrapper references the adapter result path and SHA-256; it never adds a field to that strict contract or fabricates an absent result.

## Required decision information when supported

- Exact dated price, currency and security/share unit; issuer-level versus class-level capitalizations.
- Reported-to-owner-cash bridge, normalized economics and input evidence, including estimates of maintenance/growth capex rather than invented facts.
- Bear/base/bull value range with dated cash flows, discount-rate assumptions, terminal contribution, enterprise-to-equity bridge, share/dilution denominator, ADR/class conversion and FX facts. Each model is conditional, not an investor endorsement.
- Price-versus-value sensitivity and expectations embedded in price. A reverse model can be nonidentified; do not force a unique answer.
- Full dated cash-flow return/IRR only under a reviewed definition. A geometric approximation is labelled as such; scenario likelihoods are authored assumptions, never model confidence or claimed investor probabilities.
- Funded downside, liquidity/collateral/currency stress, explicit falsifiers and observations that would revise the thesis. Position sizing is a separate authorized workflow.

If a prerequisite is absent, set output status to missing/not_computable/inapplicable with null values and named inputs. Do not turn missing into zero or substitute a peer multiple without declaring a different model. Respect R2 positive-domain, reconciliation, provenance, offline and missingness restrictions. Technical setups, peer pricing, macro context and portfolio risk do not become intrinsic value.

## Four panels

Quality refers to the accepted custom analysis rubric, not native Buffett output. Valuation retains its model and units. Evidence coverage is field/source availability, not investment attractiveness. Uncertainty contains assumptions, unresolved contradictions, hard risks and ineligible facts. If an adapter artifact is unavailable, all adapter panels are missing; independent qualitative research can still be returned without reconstructing a score.

For hypothetical decision conclusions use explicit initiate-long/do-not-initiate-long/watch/abstain plus rationale only when the research task asks for decision outputs. A favourable business finding or an existing-holder assessment does not automatically mean buy. Such conclusions belong to the wrapper extension and are not emitted by the finterm backbone. No order, exposure change or live action follows.

Ordinary, preferred and other economic claims must be allocated before dividing equity value by a listing/class denominator, including Samsung ordinary versus preference claims. TSM ADS ratios and Alibaba/Tencent reporting-to-quote currencies require verified dated conversions. Where the bridge cannot be supported, use an independently supported and explicitly different valuation method or honest missing valuation. No master is required to produce intrinsic price. Growth, discount and scenario assumptions are authored and frozen before outcomes are reviewed.

## Cash-flow semantics gate

Enterprise FCFF is not silently interchangeable with after-interest CFO minus capex, issuer-defined FCF, owner earnings or FCFE. Before an R2 enterprise FCFF forecast is admitted, show the operating-tax/reinvestment/cash-flow bridge and explicit treatment of net interest, leases and other claims. Inspect the issuer’s accounting cash-flow classification rather than assuming the label defines enterprise cash. Mark enterprise FCFF unavailable if the bridge is unsupported. Arithmetic and a valid numeric schema do not validate economic cash-flow semantics.

Maintenance capex, future operating taxes and all adjustments/forecasts are estimates or authored assumptions when not reported facts, with explicit missingness and source references. A supported owner-earnings/FCFE analysis stays separately labelled and does not become an R2 enterprise FCFF input. This is an external semantic input-admissibility gate; the accepted strict R2 schema is unchanged.
