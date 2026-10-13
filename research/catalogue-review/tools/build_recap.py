#!/usr/bin/env python3
"""Rebuild the bounded catalogue recap from accepted source records.
Read-only inputs are supplied explicitly; output must be a separate directory.
"""
import argparse, csv, hashlib, json, re
from pathlib import Path

CRITERIA = {
    "C1": {"label": "Method completeness and analytical detail", "weight": 20},
    "C2": {"label": "Stock-specific thesis valuation and quantifiability", "weight": 30},
    "C3": {"label": "Differentiated causal mechanisms", "weight": 20},
    "C4": {"label": "Substance over persona and evidence discipline", "weight": 15},
}
SELECTED = ["finterm-ai/investment-skills", "xbtlin/ai-berkshire", "monarchjuno/vibe-investing"]
SOURCE_SPECS = [
    ("S01", "v1", "source21-consolidated.json", "Accepted 21-row subjective source scores and evidence rationales"),
    ("S02", "v1", "frozen-top20.json", "Frozen core membership and popularity order"),
    ("S03", "v1", "scoring-rubric.md", "Criterion anchors formula gates and separate C5 definition"),
    ("S04", "v1", "T1-metadata-correction1.json", "Accepted metadata-only rank correction"),
    ("S05", "v1", "acceptance-ledger.json", "V1 inventory replay and final-handoff acceptance state"),
    ("S06", "v1", "historical-benchmark-protocol.md", "Fixed comparable replay and authenticity design"),
    ("S07", "v1", "benchmark-run-approval.json", "Frozen condition composition and backend limitations"),
    ("S08", "v1", "T2-empirical-selection-acceptance.json", "Accepted V1 replay status and interpretation only"),
    ("S09", "v1", "T2-authenticity-acceptance.json", "Separate bounded historical-view evidence coverage"),
    ("S10", "v1", "T3-remote-pr-verified.json", "Previously verified V1 draft PR URL and exact head"),
    ("S11", "v1", "T3-publication-copy-acceptance.json", "V1 isolated source publication receipt"),
    ("S12", "projection", "registry/canonical-source-catalogue.json", "V2 expanded structural inventory and count definitions"),
    ("S13", "projection", "registry/project-adoption-coverage.json", "V2 21-project mechanism-adoption coverage"),
    ("S14", "projection", "README.md", "Current source-only publication limits"),
    ("S15", "projection", "PUBLIC-MANIFEST.json", "Existing complete public projection byte inventory"),
]

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p, value): p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
def sanitize_text(s):
    s=re.sub(r"Serenity \(@[^)]+\)", "Serenity", s)
    s=s.replace("Current S&P 500/FMP/Finviz inputs", "Current index, financial-provider and screener inputs")
    s=re.sub(r"SEC User-Agent contact is [^ ]+ rather than a real operator contact", "SEC User-Agent contact uses a placeholder rather than a real operator contact", s)
    s=re.sub(r"SKILL command hardcodes [^ ]+ rather than resolving current installation path", "SKILL command hardcodes an author-specific installation location rather than resolving the current installation path", s)
    return s

def sanitize(v):
    if isinstance(v, str): return sanitize_text(v)
    if isinstance(v, list): return [sanitize(x) for x in v]
    if isinstance(v, dict): return {k:sanitize(x) for k,x in v.items()}
    return v

def representative(r):
    return next(x for x in r["pinned_sources"] if x["path"].lower() not in ["license", "license.md", "readme.md"])

def escaped(v): return str(v).replace("|", "\\|").replace("\n", " ")
def number(v): return str(int(v)) if float(v).is_integer() else str(v)

def build(v1, projection, out):
    v1, projection, out = v1.resolve(), projection.resolve(), out.resolve()
    if out == v1 or out == projection or v1 in out.parents or projection in out.parents:
        raise ValueError("Output must be separate from both read-only source trees")
    out.mkdir(parents=True, exist_ok=True)
    source=load(v1/"source21-consolidated.json")
    canonical=load(projection/"registry/canonical-source-catalogue.json")
    approval=load(v1/"benchmark-run-approval.json")
    review=load(v1/"T2-empirical-selection-acceptance.json")
    authentic=load(v1/"T2-authenticity-acceptance.json")
    v1pr=load(v1/"T3-remote-pr-verified.json")
    rows=[]
    for r in source["rows"]:
        row={k:r.get(k) for k in ["repo","repo_url","stars","star_snapshot_window_utc","commit_sha","implemented_masters","scores","criteria_evidence","strength","material_gaps","license_status","reuse_license_gate","source_score_100","raw_source_quality_rank","reuse_eligible_source_quality_rank","popularity_rank_top20","inventory_class","popularity_rank_discovered_universe","pinned_sources"]}
        row["master_coverage_note"]=r.get("master_coverage_note", "Coverage is limited to the accepted inspected repository files; investor labels are not authenticated original methods.")
        row["historical_readiness_at_source_freeze"]=r["historical_readiness"]
        row["comparable_replay_status"] = "V1 accepted wrapped replay; numeric run results not republished" if r["repo"] in SELECTED else "Not tested in the accepted V1 three-project replay"
        row["empirical_C5_published_value"]=None
        row["returns_backtest_published_value"]=None
        row["evidence_source_ids"]=["S01","S02","S03"]
        rows.append(sanitize(row))
    counts=canonical["coverage_counts"]
    data={
        "schema_version":"bounded-project-catalogue-recap.v1-candidate",
        "status":"Candidate for independent review; not published or merged by this recap",
        "scope":source["scope"],
        "snapshot_window_utc":source["snapshot_window_utc"],
        "core_count":20,"supplement_count":1,"candidate_universe_count":29,
        "criteria":CRITERIA,
        "score_scale":"Each C1-C4 is a subjective static source-review judgment from 0 to 5",
        "source_score_formula":"100*(20*C1+30*C2+20*C3+15*C4)/425",
        "quality_rank_scope":"21 reviewed projects including the supplemental backbone; not GitHub popularity",
        "quality_rank_tie_break":source["quality_rank_tie_break"],
        "selected_reusable_foundation":review["selected_reusable_foundation"],
        "frozen_finalists_before_results":source["proposed_finalists_before_results"],
        "rows":rows,
        "v2_reconciliation":{
            "same_repository_set":sorted(x["repo"] for x in canonical["repositories_and_license_reuse"]),
            "coverage_counts":counts,
            "coverage_interpretation":canonical["coverage_interpretation"],
            "rank_interpretation":"V2 structurally inventories more files at the same pins; it does not rescore or rerank this V1 sample. 121 entities includes organizations collectives pseudonyms and adjacent operating perspectives. It is not 121 authenticated masters.",
            "finterm_position":"Supplemental quality backbone; not substituted into the frozen popularity top20; discovered eligible-universe popularity rank 29",
        },
        "comparable_tests":{
            "v1_status":"Accepted completed wrapped source-method replay; no native repository end-to-end execution and no returns study",
            "decision_cutoff":"2015-12-31 16:00 America/New_York",
            "companies":["NVDA","TSLA","VIPS"],
            "condition_count":4,"planned_cells":review["planned_cells"],"accepted_valid_first_pass_cells":review["valid_first_pass_cells"],
            "conditions":[{"condition_id":x["condition_id"],"repo":x["repo"],"commit_sha":x["commit_sha"],"method_mode":x["method_mode"],"master_roles":x["master_roles"]} for x in approval["conditions"]]+[{"condition_id":"no-skill-control","repo":None,"method_mode":"Identical frozen packet and query without an investor skill; diagnostic control"}],
            "backend":"gpt-6.1-sol with xhigh reasoning was explicitly selected; exact backend snapshot temperature and seed were not exposed",
            "C5_definition":"Observed rubric-based method fidelity only; B is the mean of three required valid company scores and C5=B/20. Historical readiness and authentic-view evidence are separate fields.",
            "C5_published_values":None,"numeric_run_outputs_published":False,"returns_outcomes_published":False,
            "authenticity":{
                "strict_primary_equity_decision_comparators_found":authentic["coverage"]["strict_precutoff_primary_equity_decision_comparators_found"],
                "unique_actual_investor_company_cells":authentic["coverage"]["unique_actual_investor_company_cells"],
                "equity_alignment_percentage":None,
                "finding":"No matched primary stock-decision statement was found within the bounded search. All equity-decision alignments remain unknown. One shared grade-C Munger Tesla business-risk record supports only narrow partial compatibility in two outputs; no valuation price action horizon or purchase thesis is established.",
            },
            "limitations":["One first pass per condition and company; no repeated-run or anonymized control executed", "Selected historical stocks and current model/skill knowledge permit hindsight and survivorship bias", "Native output scopes differ; correct abstention is valid and cannot be converted into an invented valuation or buy/sell score", "Fidelity is not stock-picking accuracy investor endorsement causal uplift predictive alpha or realized returns", "A holdings filing proves disclosed exposure at a reporting date not purchase price intent or a personal thesis", "V2 security-level comparisons model opinions numeric runtime and outcome evaluation remain separate unfinished gates; this recap contains no V2 opinions or numeric outcomes"],
            "source_ids":["S06","S07","S08","S09"],
        },
        "previous_publication":{
            "v1":{"pr_url":v1pr["url"],"head_sha":v1pr["head_sha"],"verified_at_utc":v1pr["verified_at_utc"],"status_at_verification":"draft open unmerged","source_ids":["S10","S11"]},
            "v2_source_only":{"pr_url":"https://github.com/AmelieLang/Investment-master/pull/1","status":"Draft source-only PR provided for this audit; current PR state not independently refreshed by this read-only file audit"},
        },
        "publication_boundaries":{"includes":["Original review commentary", "Static subjective catalogue scores", "Pinned public repository evidence links", "Comparable test design status and limitations"],"excludes":["Raw model outputs", "Numeric historical returns or investment success rates", "Actual V2 investment opinions", "Restricted financial-provider payloads", "Private research documents", "Personal contact account or device identifiers", "Absolute internal filesystem locators"]},
    }
    dump(out/"catalogue.json", data)
    manifest=[]
    for ident,origin,name,purpose in SOURCE_SPECS:
        f=(v1 if origin=="v1" else projection)/name
        manifest.append({"source_id":ident,"source_record_name":f.name,"source_kind":"accepted V1 research record" if origin=="v1" else "existing V2 public projection record","sha256":sha(f),"bytes":f.stat().st_size,"purpose":purpose,"source_bytes_republished":False})
    dump(out/"SOURCE-MANIFEST.json",{"schema_version":"catalogue-recap-source-manifest.v1","input_records":manifest,"locator_policy":"Source record basenames and exact hashes are provided without absolute paths; upstream evidence links are preserved in catalogue.json. Original input files are not included.","transformations":[{"operation":"omit","fields":["runtime_constraints","actual_run_status","empirical_C5"],"reason":"Avoid private execution details and obsolete pre-run status; publish no empirical score values"},{"operation":"display_redaction","field":"implemented_masters","rule":"Public pseudonym is displayed as Serenity without an account handle"},{"operation":"display_redaction","field":"material_gaps","rule":"An author-specific absolute installation path, a placeholder contact address and provider labels are replaced by generic descriptions; no financial-provider data is copied"}],"acceptance_basis":"Accepted V1 T1 and T2 records plus static accepted V2 structural inventory. This new recap still needs independent review."})
    fields=["popularity_rank_top20","repo","repo_url","stars","investors_covered","C1","C2","C3","C4","source_score_100","raw_source_quality_rank","reuse_eligible_source_quality_rank","license_status","commit_sha","comparable_replay_status","evidence_url"]
    with (out/"top20-and-supplement.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in rows:
            z={k:r[k] for k in fields if k in r};z["investors_covered"]="; ".join(r["implemented_masters"]);z.update(r["scores"]);z["evidence_url"]=representative(r)["url"]; w.writerow(z)
    main=["# GitHub investment method project catalogue", "", "This candidate restores the readable 20-project comparison omitted from the current source-only bundle. It preserves the accepted V1 source scores and ranks. It is prepared for independent review and has not been published by this audit.", "", "## Scope and dates", "", "The popularity table is the highest-star 20 in a bounded, eligible, accessible and lineage-deduplicated research sample. The review admitted 29 eligible projects from 71 metadata-verified and scope-screened repositories. The 483 first-page search hits were discovery leads. This is not an exhaustive or current global GitHub ranking.", "", "Stars were sampled from 2026-10-12 16:22 to 16:25 UTC. Scores are subjective judgments from static inspection of the pinned commits shown in each detailed record. Stars measure popularity, not method quality. Source-quality ranks cover 21 reviewed projects, including one separately labelled supplemental backbone. They are not performance ranks.", "", "## Scores and interpretation", "", "Each criterion is 0–5: C1 method completeness/detail; C2 stock thesis, valuation and quantifiability; C3 differentiated causal mechanisms; C4 substance over persona and evidence discipline. Evidence is given as a rationale plus exact pinned public files in the detailed review. C4 is not a stand-alone count of citations. C3 does not reward contrarianism without a testable mechanism.", "", "Static base /100 = 100 × (20×C1 + 30×C2 + 20×C3 + 15×C4) / 425. The score column reports C1/C2/C3/C4 in that order. Ties use C2, then C4, C1, C3 and stars. These scores do not establish authentic investor views, stock-picking accuracy, or realized returns.", "", "## Frozen popularity top20", "", "The investor column is a compact list from the accepted source review. A +N entry links to the full roster and its inspection limits. A listed label does not imply an authenticated independent method. Large persona or package rosters mix individuals with shared frameworks and adjacent perspectives.", "", "| Popularity rank | Project | Sampled stars | Investors or lenses covered | C1/C2/C3/C4 | Static base /100 | Source quality rank | Pinned evidence |", "|---:|---|---:|---|---|---:|---:|---|"]
    for r in rows:
        if r["popularity_rank_top20"] is None:continue
        rank=r["popularity_rank_top20"]; names=r["implemented_masters"]
        coverage=", ".join(names[:5])+(f" [+{len(names)-5}](DETAILED-REVIEWS.md#project-{rank})" if len(names)>5 else "")
        ss="/".join(number(r["scores"][x]) for x in CRITERIA)
        evidence=representative(r)
        main.append(f"| {rank} | [{r['repo']}]({r['repo_url']}) | {r['stars']:,} | {coverage} | {ss} | {r['source_score_100']:.2f} | {r['raw_source_quality_rank']} | [Reviewed file]({evidence['url']}) |")
    supplement=next(r for r in rows if r["popularity_rank_top20"] is None)
    main += ["", "## Supplemental quality backbone", "", f"[{supplement['repo']}]({supplement['repo_url']}) has {supplement['stars']} sampled stars and is rank {supplement['popularity_rank_discovered_universe']} among the 29 eligible discovered projects. It is outside the frozen popularity top20. Its accepted C1/C2/C3/C4 scores are 5/3.5/4.5/5, static base 87.06/100 and source-quality rank 1. [Pinned framework source]({supplement['pinned_sources'][0]['url']}).", "", "## Selection rationale", "", "The accepted reusable research foundation is finterm. Its strength is evidence-bounded card routing, missing-data stops, causal alternatives and research-output discipline. It is a research backbone, and does not provide a native aggregate investment score or unrestricted buy/sell decision. Its title and routing should not be mistaken for an executable intrinsic-value calculator.", "", "The frozen three-project comparison selected finterm, xbtlin and monarchjuno using source quality plus the reuse gate. xbtlin offers detailed company analysis and numerical valuation/checklist mechanisms, with known arithmetic/verification caveats. monarchjuno offers modular company research, distinct lenses and explicit Actual/Estimated/Assumption labelling. It was the third highest source-ranked license-eligible project.", "", "LI-Jialu was raw source rank 3 and agi-now rank 4, ahead of monarchjuno rank 5. Both lacked a verified reusable license at the reviewed pin. Wechat had a README license claim without the corresponding verified license file. Research eligibility permits inspection; it does not authorize direct prompt/code reuse. None of these license gates changes their original research scores or removes them from the popularity table.", "", "MIT verification only covers the repository notice at the reviewed commit. Third-party extracts, data/API rights and trademarks still require separate review. No unlicensed upstream implementation is copied in this recap.", "", "## V1 and V2 reconciliation", "", "V1 scored the 20 frozen projects plus finterm. V2 retained the same 21 repositories and commits, then expanded structural coverage to 162 source files and 121 canonical entities. Those entities include organizations, collectives, pseudonyms and operating perspectives; 70 are categorized person names excluding executive perspectives. These are inventory definitions, not 121 authenticated investors or independent strategies.", "", "V2 adds identity reconciliation and mechanism-transfer decisions. It does not supply a new C1–C4 leaderboard, so the V1 source ranks remain unchanged here. UZI's 66 roster records contain shared rule generators, and Questflow's 63 packages include institutions and pseudonyms. Neither package/persona count is a count of independently validated master methods.", "", "## Comparable tests and historical attribution", "", "[COMPARABLE-TESTS.md](COMPARABLE-TESTS.md) gives the previously accepted common-data replay design and the separate historical-view cross-check. V1 completed one first pass for each of three wrapped methods and one no-skill control on NVDA, TSLA and VIPS. This recap republishes no numerical C5/run results or return series. V2 method opinions, security-level comparison and outcome evaluation remain separate unfinished gates.", "", "C5 measures observed method fidelity under a fixed rubric. A contemporaneous original-investor stock-thesis cross-check is a separate authenticity axis. No matched primary stock-decision statement was found in the bounded search, leaving equity alignment unknown. Holdings, generic philosophy and a shared qualified business-risk comment do not fill that gap.", "", "## Existing public source links", "", f"The prior V1 draft source PR is [investment-skills PR 1]({v1pr['url']}). The accepted receipt verified exact head {v1pr['head_sha']} on {v1pr['verified_at_utc']}; that receipt reported it draft, open and unmerged. This audit did not refresh its current state.", "", "The V2 source-only draft PR supplied for this audit is [Investment-master PR 1](https://github.com/AmelieLang/Investment-master/pull/1). This candidate does not change its source bundle or imply a merge, activation or completed benchmark.", "", "## Review and reproducibility", "", "[catalogue.json](catalogue.json) contains all 21 complete rows. [top20-and-supplement.csv](top20-and-supplement.csv) is the sortable table. [DETAILED-REVIEWS.md](DETAILED-REVIEWS.md) provides all criterion rationales, limitations and source links. [SCORING-METHOD.md](SCORING-METHOD.md) preserves all static scoring anchors. [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json) records exact accepted input hashes without republishing those files. The supplied read-only tests check coverage, ranks, formulas, score/evidence preservation and publication boundaries. Exact source comparison requires the original accepted inputs; bundled tests alone can verify only their hashes and the recap's internal consistency.", ""]
    (out/"README.md").write_text("\n".join(main),encoding="utf-8")
    details=["# Detailed accepted source reviews", "", "The scores, rationale wording and material gaps below are preserved from the accepted V1 static review. That review predates the later V1 replay. The historical-readiness field describes the source freeze rather than today's completion state. Display-only redactions remove an account handle, an author-specific installation path and a placeholder contact address; data-provider labels are generalized. Most review text is English; a few original review summaries remain Chinese.", "", "Pinned evidence means a precise inspected file and commit. The linked source set is the repository-level evidence set for these criterion rationales. It does not assert that every linked file supports every sentence. File-backed lenses are not automatically authenticated original-investor methods.", ""]
    for r in rows:
        anchor=f"project-{r['popularity_rank_top20']}" if r["popularity_rank_top20"] else "supplement"
        details += [f'<a id="{anchor}"></a>', f"## {r['repo']}", "", f"[Repository]({r['repo_url']}) · commit {r['commit_sha']} · sampled stars {r['stars']:,}", "", f"Popularity rank: {r['popularity_rank_top20'] if r['popularity_rank_top20'] else 'supplement outside top20'}. Raw source-quality rank: {r['raw_source_quality_rank']} of 21. License-eligible source rank: {r['reuse_eligible_source_quality_rank'] if r['reuse_eligible_source_quality_rank'] else 'blocked at pin'}.", "", "Investors or lenses: "+", ".join(r["implemented_masters"])+".", "", "Coverage limit: "+r["master_coverage_note"], ""]
        for key,info in CRITERIA.items():
            details += [f"### {key} {info['label']}", "", f"Accepted score: {number(r['scores'][key])}/5. "+r["criteria_evidence"][key], ""]
        details += [f"Static base: {r['source_score_100']:.2f}/100.", "", "Review conclusion: "+r["strength"], "", "### Material limitations", ""]
        details += ["- "+x for x in r["material_gaps"]]
        details += ["", "License at pin: "+r["license_status"]+". "+r["reuse_license_gate"], "", "### Historical readiness at the source freeze", ""]
        hist=r["historical_readiness_at_source_freeze"]
        if isinstance(hist,dict): details += ["- "+k+": "+str(v) for k,v in hist.items() if k!="historical_run"]
        else:details += [hist]
        details += ["", "Later comparable replay status: "+r["comparable_replay_status"]+".", "", "### Exact inspected public files", ""]
        details += [f"- [{x['path']}]({x['url']})" for x in r["pinned_sources"]]
        details += [""]
    (out/"DETAILED-REVIEWS.md").write_text("\n".join(details),encoding="utf-8")
    tests=["# Comparable replay design and evidence limits", "", "This is a source and design recap of the accepted V1 experiment, not a new experiment. Numerical model outputs, historical returns and actual V2 opinions are outside this candidate.", "", "## Common design", "", "Decision information cutoff: 2015-12-31 16:00 America/New_York, after the close. The three cases were NVDA, TSLA and VIPS. Every method and control received the same frozen company packet and query for a case. Filings were admitted by publication date rather than fiscal-period label. Later stock outcomes and the authentic-comparator evidence were withheld during initial analysis.", "", "Three method conditions plus the no-skill control produced 12 first-pass cells. The accepted review confirms 12 valid first passes, no hard-invalid cells and no replacement reruns. These are acceptance/coverage counts, not return or accuracy scores. Repository software was not installed or run end-to-end: the test wrapped or composed pinned method text in fresh contexts.", "", "The explicitly selected backend was gpt-6.1-sol with xhigh reasoning. The exact backend snapshot, temperature and seed were not exposed. There was one first pass per cell; no repeated-run stability trial or anonymized control was executed.", "", "## Frozen conditions", "", "| Condition | Composition | Native output boundary |", "|---|---|---|", "| finterm | Buffett financial-analysis entrypoint with exactly 12 complete router-selected cards per company | Research checks; Munger is corroborating influence, not an independent scored lens. Native scope can abstain from aggregate investment action and numerical intrinsic value. |", "| xbtlin | Integrated four-lens workflow: Buffett, Munger, Duan Yongping and Li Lu | A composed workflow, not a Buffett-only method or native end-to-end runtime. |", "| monarchjuno | Fixed Buffett and Munger lenses plus generic company-analysis workflow | A composed research method, not one native investor valuation engine. |", "| No-skill control | Same query and company packet with no investor skill | Diagnostic baseline; not a project-quality score. |", "", "## C5 method fidelity", "", "Five fixed dimensions score method application (30), arithmetic/security/currency/period consistency (25), thesis/countercase/accounting evidence (20), reproducible assumptions/sensitivity or justified abstention (15), and calibration/falsifiability/native-scope compliance (10). B is the mean of a finalist's three required valid company scores; C5 = B/20. A combined score is defined only after all required cells are valid, using 85% unrounded static source base plus 15% B. This recap does not republish B, C5 or combined empirical scores.", "", "Decision-use of post-cutoff facts, fabricated quotes/sources, and material currency/share/ADS/split mismatches invalidate a cell. INVALID is not zero, cannot be offset by other dimensions, and cannot be silently removed from the mean. Correct missing-data or native-scope abstention earns method credit without inventing a stock score or recommendation.", "", "C5 measures adherence to this evidence/method rubric. It does not measure agreement with a real investor, correct stock decisions, returns, alpha or general model uplift. A strong no-skill control, unequal native output scope, subjective grading and rubric ceilings limit comparative inference.", "", "## Separate original investor view cross check", "", "A matched comparator requires the company, public date, decision type and horizon to match. A primary dated investor statement is stronger than second-hand attendee notes. A quality comment does not establish a valuation or trade decision. A 13F establishes disclosed exposure at the report date, not intent, purchase price, personal authorship or a universal investment rule.", "", "The accepted bounded search found no strict pre-cutoff primary stock-decision comparator across 12 actual investor–company cells. Evidence coverage is 0/12, while the equity-alignment percentage is undefined. That is a search-coverage result, not 0% agreement, 0% accuracy or proof that those investors never commented.", "", "One shared grade-C source concerns Munger's Tesla business-risk discussion. It is attendee reporting rather than a verified verbatim transcript. Narrow risk components in two method outputs were partially compatible with it; this is not two independent confirmations. It establishes no stock price, action, horizon, disclosed holding or December 31 opinion.", "", "## Further comparable tests remain proposals", "", "The following are reproducible test requirements, not claims of executed experiments: rerun fixed inputs in fresh contexts to measure variance; use anonymized and no-skill controls; test missing fields and conflicting evidence; perturb units, currencies and publication dates; hold out companies; verify source-induced mechanisms against primary dated material; and evaluate post-decision outcomes only in a separate ex-post ledger after any decision and execution mapping are frozen.", "", "Current models and 2026 method packages can encode later knowledge even with a frozen 2015 packet. The three selected stocks have hindsight and survivorship bias. V2's historical transport, numerical runtime, security-level comparisons and model opinions require their own acceptance. These are unfinished gates. No V2 investment opinion, native-program execution, realized trade or successful returns backtest is claimed here.", ""]
    (out/"COMPARABLE-TESTS.md").write_text("\n".join(tests),encoding="utf-8")
    dump(out/"PROJECTION-COVERAGE-AUDIT.json",{
        "schema_version":"catalogue-projection-coverage-audit.v1",
        "projection":"Existing source-only public bundle supplied for read-only inspection",
        "exact_requested_catalogue_present":False,
        "present":["21-repository structural catalogue", "Investor/source identity inventory", "162 indexed implementation source files", "39-feature synthesis adoption inventory with 21-project coverage", "Source pins and license gates"],
        "absent":["Readable frozen top20 project table", "Sampled stars and popularity ranks", "Accepted static C1-C4 scores", "Static source-base and source-quality ranks", "Per-criterion scored comparison rationales", "V1 comparable-test recap with separate C5 and authentic-view limits"],
        "observed_missing_exact_field_names":["source_score_100","raw_source_quality_rank","criteria_evidence","popularity_rank_top20"],
        "candidate_remedy":"Separate recap files only; no existing accepted input or public projection is edited",
    })
    rubric=(v1/"scoring-rubric.md").read_text(encoding="utf-8")
    anchors=rubric.split("### C1",1)[1].split("### C5",1)[0]
    scoring=["# Static source scoring method", "", "This reproduces the accepted V1 source-audit anchors, unchanged. Scores are reviewer judgments at the frozen pins, not calibrated probabilities. All projects receive C1-C4; only previously tested finalists can receive an observed C5. Source inspection is distinct from native execution and from investor authenticity.", "", "Static source base /100 = 100 × (20×C1 + 30×C2 + 20×C3 + 15×C4) / 425. C1-C4 each range from 0 to 5; half-points are allowed. The 20/30/20/15 weights sum to 85, so normalization is necessary before comparing the source base. Source ranking retains research-eligible but reuse-blocked projects. Quality ties use C2, C4, C1, C3 and sampled stars.", "", "### C1"+anchors, "## Evidence and eligibility", "", "A positive source score needs an inspected, pinned implementation file and a rationale. A famous-name label, high star count, prose length or asserted historical return adds no points. Research eligibility requires accessible investor-derived implementation evidence beyond marketing, relevant scope, readable files and a distinct implementation lineage. Verified licensing, third-party rights and safe runtime permissions are separate reuse gates; a high score cannot override them.", "", "No additional stand-alone evidence score is invented. Evidence traceability and epistemic controls contribute mainly to C4, while source-linked criterion rationales explain each C1-C4 judgment. Historical-readiness descriptions are not C5. See COMPARABLE-TESTS.md for C5 fidelity and the separate original-investor statement cross-check.", ""]
    (out/"SCORING-METHOD.md").write_text("\n".join(scoring),encoding="utf-8")
    public_manifest=load(projection/"PUBLIC-MANIFEST.json")
    recorded=public_manifest["files"]
    verified=[{"path":x["path"],"sha256":sha(projection/x["path"]),"bytes":(projection/x["path"]).stat().st_size,"matches":sha(projection/x["path"])==x["sha256"] and (projection/x["path"]).stat().st_size==x["bytes"]} for x in recorded]
    expected={x["path"] for x in recorded}|{"PUBLIC-MANIFEST.json"}
    actual={str(p.relative_to(projection)) for p in projection.rglob("*") if p.is_file()}
    dump(out/"PROJECTION-PRESERVATION.json",{"schema_version":"projection-preservation-check.v1","status":"PASS" if all(x["matches"] for x in verified) and actual==expected else "FAIL","manifest_sha256":sha(projection/"PUBLIC-MANIFEST.json"),"expected_file_count":len(expected),"actual_file_count":len(actual),"recorded_files_checked":len(verified),"exact_path_set":actual==expected,"all_recorded_hashes_and_lengths_match":all(x["matches"] for x in verified),"scope":"All existing projection files match its original public manifest. Original projection files are read-only inputs and are not regenerated or edited.","files":verified})
    return data

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--source-v1-dir",type=Path,required=True);ap.add_argument("--projection-dir",type=Path,required=True);ap.add_argument("--out",type=Path,required=True);args=ap.parse_args()
    result=build(args.source_v1_dir,args.projection_dir,args.out)
    print(json.dumps({"rows":len(result["rows"]),"core_count":result["core_count"],"supplement_count":result["supplement_count"],"status":result["status"]}))
