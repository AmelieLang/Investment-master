#!/usr/bin/env python3
"""Coverage tests; optional exact accepted-source comparison uses read-only inputs."""
import argparse, csv, hashlib, json, math, re, sys
from pathlib import Path
from urllib.parse import urlsplit
sys.dont_write_bytecode=True
from build_recap import CRITERIA, SELECTED, SOURCE_SPECS, sanitize, representative

checks=[]
def check(name, condition, detail=None):
    checks.append({"check":name,"passed":bool(condition), **({"detail":detail} if detail is not None else {})})
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--candidate-dir",type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument("--source-v1-dir",type=Path);ap.add_argument("--projection-dir",type=Path);ap.add_argument("--report",type=Path);args=ap.parse_args()
    root=args.candidate_dir
    data=read(root/"catalogue.json"); rows=data["rows"]; core=[r for r in rows if r["popularity_rank_top20"] is not None]; supplements=[r for r in rows if r["popularity_rank_top20"] is None]
    check("21 distinct reviewed repositories",len(rows)==21 and len({r["repo"] for r in rows})==21)
    check("exact 20 plus separate finterm supplement",len(core)==20 and len(supplements)==1 and supplements[0]["repo"]=="finterm-ai/investment-skills")
    check("popularity ranks one through twenty",[r["popularity_rank_top20"] for r in core]==list(range(1,21)))
    check("sampled stars descending",[r["stars"] for r in core]==sorted((r["stars"] for r in core),reverse=True))
    check("finterm separate discovered-universe rank 29",supplements[0]["popularity_rank_discovered_universe"]==29)
    check("snapshot window exact",data["snapshot_window_utc"]==["2026-10-12T16:22:00Z","2026-10-12T16:25:00Z"])
    quality=sorted(rows,key=lambda r:(-sum(r["scores"][k]*v["weight"] for k,v in CRITERIA.items()),-r["scores"]["C2"],-r["scores"]["C4"],-r["scores"]["C1"],-r["scores"]["C3"],-r["stars"]))
    check("all 21 original quality ranks recompute",all(r["raw_source_quality_rank"]==i for i,r in enumerate(quality,1)))
    eligible=[r for r in quality if r["license_status"]=="verified_mit"]
    check("18 license-eligible ranks recompute",len(eligible)==18 and all(r["reuse_eligible_source_quality_rank"]==i for i,r in enumerate(eligible,1)))
    check("frozen finalists equal top three license-eligible",data["frozen_finalists_before_results"]==SELECTED and [r["repo"] for r in eligible[:3]]==SELECTED)
    blocked={r["repo"] for r in rows if r["reuse_eligible_source_quality_rank"] is None}
    check("three distinct research-versus-reuse gates preserved",blocked=={"agi-now/buffett-skills","LI-Jialu/investor-panel-skill","Wechat-ggGitHub/investment-masters-skill"})
    for r in rows:
        name=r["repo"]
        check(name+" criterion scores and 100-point formula",set(r["scores"])==set(CRITERIA) and all(0<=v<=5 for v in r["scores"].values()) and abs(100*sum(r["scores"][k]*v["weight"] for k,v in CRITERIA.items())/425-r["source_score_100"])<=0.0051)
        check(name+" complete criterion rationale and covered roster",set(r["criteria_evidence"])==set(CRITERIA) and all(r["criteria_evidence"].values()) and bool(r["implemented_masters"]) and bool(r["master_coverage_note"]))
        check(name+" exact pinned public source URLs",bool(r["pinned_sources"]) and all(x["url"].startswith("https://github.com/"+name+"/blob/"+r["commit_sha"]+"/") and x["url"].endswith(x["path"]) for x in r["pinned_sources"]))
        check(name+" representative is a substantive file",representative(r)["path"].lower() not in ["license","license.md","readme.md"])
        check(name+" no C5 or returns outcomes republished",r["empirical_C5_published_value"] is None and r["returns_backtest_published_value"] is None)
    with (root/"top20-and-supplement.csv").open(encoding="utf-8",newline="") as f:csvrows=list(csv.DictReader(f))
    check("CSV covers all 21 projects in same order",[r["repo"] for r in csvrows]==[r["repo"] for r in rows])
    check("CSV scalar scores agree",all(float(c[k])==r["scores"][k] for c,r in zip(csvrows,rows) for k in CRITERIA))
    check("CSV full investor roster agrees",all(c["investors_covered"]=="; ".join(r["implemented_masters"]) for c,r in zip(csvrows,rows)))
    md=(root/"README.md").read_text(encoding="utf-8");dt=(root/"DETAILED-REVIEWS.md").read_text(encoding="utf-8");ts=(root/"COMPARABLE-TESTS.md").read_text(encoding="utf-8")
    check("readable main table has exactly 20 ranked rows",len(re.findall(r"^\| [0-9]+ \|",md,re.M))==20)
    check("details cover all 21 with four criterion sections each",all("## "+r["repo"] in dt for r in rows) and all(dt.count("### "+k+" ")==21 for k in CRITERIA))
    check("C5 and authentic historical views are distinct",data["comparable_tests"]["C5_published_values"] is None and data["comparable_tests"]["authenticity"]["equity_alignment_percentage"] is None and "separate authenticity axis" in md)
    check("bounded historical view coverage does not imply disagreement",data["comparable_tests"]["authenticity"]["strict_primary_equity_decision_comparators_found"]==0 and data["comparable_tests"]["authenticity"]["unique_actual_investor_company_cells"]==12 and "not 0% agreement" in ts)
    check("accepted replay coverage and conditions exact",data["comparable_tests"]["condition_count"]==4 and data["comparable_tests"]["planned_cells"]==12 and data["comparable_tests"]["accepted_valid_first_pass_cells"]==12 and len(data["comparable_tests"]["conditions"])==4)
    check("source only and no V2 outcome claim",not data["comparable_tests"]["numeric_run_outputs_published"] and not data["comparable_tests"]["returns_outcomes_published"] and "unfinished gates" in ts)
    check("same V1 V2 repository scope",sorted(r["repo"] for r in rows)==data["v2_reconciliation"]["same_repository_set"])
    check("V2 structural counts not investor validity",data["v2_reconciliation"]["coverage_counts"]["canonical_entities"]==121 and data["v2_reconciliation"]["coverage_counts"]["investor_and_framework_source_files_indexed"]==162 and "not 121 authenticated" in data["v2_reconciliation"]["rank_interpretation"])
    audit=read(root/"PROJECTION-COVERAGE-AUDIT.json")
    check("projection gap explicitly recorded",audit["exact_requested_catalogue_present"] is False)
    # Split pattern pieces keep the test source free of real private locators and secrets.
    patterns={"absolute workspace locator":r"/work"+r"space/", "absolute user locator":r"/Us"+r"ers/", "windows user locator":r"[A-Z]:[\\/]+Us"+r"ers[\\/]", "private chat-service link":r"https?://[^\s\"]*(?:fei"+r"shu|la"+r"rksuite)", "private attachment identifier":r"lib"+r"file_[a-z0-9]+", "room message identifier":r"Senti"+r"nel_[a-z0-9]+", "credential shaped key":r"s"+r"k-(?:proj-)?[A-Za-z0-9_-]{20,}", "contact email":r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"}
    for label,pat in patterns.items():
        offenders=[]
        for f in root.rglob("*"):
            if f.is_file() and f.suffix in [".md",".json",".csv",".py"] and re.search(pat,f.read_text(encoding="utf-8")):offenders.append(str(f.relative_to(root)))
        check("publication scan "+label,not offenders,offenders)
    check("no private PDFs provider payloads or raw model outputs",not any(p.suffix.lower() in [".pdf",".docx",".xlsx"] or p.name in ["report.md","result.json","historical-company-packet.json","historical-price-fixture.json"] for p in root.rglob("*") if p.is_file()))
    manifest=read(root/"SOURCE-MANIFEST.json")
    check("15 exact source hashes and no raw sources copied",len(manifest["input_records"] )==15 and all(re.fullmatch(r"[a-f0-9]{64}",x["sha256"]) and not x["source_bytes_republished"] for x in manifest["input_records"]))
    preservation=read(root/"PROJECTION-PRESERVATION.json")
    check("original projection complete byte-preservation report",preservation["status"]=="PASS" and preservation["exact_path_set"] and preservation["all_recorded_hashes_and_lengths_match"] and preservation["expected_file_count"]==192 and preservation["recorded_files_checked"]==191)
    source_comparison=False
    if args.source_v1_dir and args.projection_dir:
        source_comparison=True
        bases={"v1":args.source_v1_dir,"projection":args.projection_dir}
        byid={x["source_id"]:x for x in manifest["input_records"]}
        for ident,origin,name,purpose in SOURCE_SPECS:
            f=bases[origin]/name
            check(ident+" accepted input bytes hash match",f.is_file() and sha(f)==byid[ident]["sha256"] and f.stat().st_size==byid[ident]["bytes"])
        corrected=read(args.source_v1_dir/"T1-metadata-correction1.json")
        check("source corpus matches accepted metadata-corrected hash",sha(args.source_v1_dir/"source21-consolidated.json")==corrected["new_hashes"]["source21-consolidated.json"])
        accepted=read(args.source_v1_dir/"acceptance-ledger.json")
        check("V1 T1 and T2 accepted completion basis",all(next(t for t in accepted["tasks"] if t["task_id"]==ident)["status"]=="accepted_and_delivered" for ident in ["T1","T2"]))
        original=read(args.source_v1_dir/"source21-consolidated.json")
        check("exact source row order",[r["repo"] for r in original["rows"]]==[r["repo"] for r in rows])
        for r,o in zip(rows,original["rows"]):
            compare_fields=["repo","repo_url","stars","star_snapshot_window_utc","commit_sha","implemented_masters","scores","criteria_evidence","strength","material_gaps","license_status","reuse_license_gate","source_score_100","raw_source_quality_rank","reuse_eligible_source_quality_rank","popularity_rank_top20","inventory_class","popularity_rank_discovered_universe","pinned_sources"]
            check(r["repo"]+" exact accepted fields after disclosed redactions",all(r[k]==sanitize(o.get(k)) for k in compare_fields))
        frozen=read(args.source_v1_dir/"frozen-top20.json")
        check("exact frozen membership pins and popularity",all(r["repo"]==o["repo"] and r["commit_sha"]==o["commit_sha"] and r["stars"]==o["stars"] and r["popularity_rank_top20"]==o["popularity_rank"] for r,o in zip(core,frozen)) and len(frozen)==20)
        original_v2=read(args.projection_dir/"registry/canonical-source-catalogue.json")
        check("same V1 V2 exact commit pins",{r["repo"]:r["commit_sha"] for r in rows}=={r["repo"]:r["commit"] for r in original_v2["repositories_and_license_reuse"]})
        projection_text=[p.read_text(encoding="utf-8") for p in args.projection_dir.rglob("*") if p.is_file() and p.suffix in [".md",".json"]]
        check("missing original scored catalogue fields verified",all(not any(field in x for x in projection_text) for field in audit["observed_missing_exact_field_names"]))
        pm=read(args.projection_dir/"PUBLIC-MANIFEST.json")
        check("existing full projection still matches original public inventory",all(sha(args.projection_dir/x["path"])==x["sha256"] and (args.projection_dir/x["path"]).stat().st_size==x["bytes"] for x in pm["files"]))
        rubric=(args.source_v1_dir/"scoring-rubric.md").read_text(encoding="utf-8")
        anchors="### C1"+rubric.split("### C1",1)[1].split("### C5",1)[0]
        check("scoring anchors reproduced exactly",anchors in (root/"SCORING-METHOD.md").read_text(encoding="utf-8"))
        prior=read(args.source_v1_dir/"T3-remote-pr-verified.json")
        check("V1 public link matches existing verified receipt",data["previous_publication"]["v1"]["pr_url"]==prior["url"] and data["previous_publication"]["v1"]["head_sha"]==prior["head_sha"] and data["previous_publication"]["v1"]["verified_at_utc"]==prior["verified_at_utc"])
    package=root/"CANDIDATE-MANIFEST.json"
    if package.exists():
        pkg=read(package);records=pkg["files"]
        check("all candidate file hashes match",all((root/x["path"]).is_file() and sha(root/x["path"])==x["sha256"] for x in records))
        actual={str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and p.name not in ["CANDIDATE-MANIFEST.json","TEST-RESULTS.json"] and "__pycache__" not in p.parts}
        check("candidate manifest complete",{x["path"] for x in records}==actual)
    report={"schema_version":"catalogue-recap-test-results.v1","status":"PASS" if all(x["passed"] for x in checks) else "FAIL","checks":len(checks),"passed":sum(x["passed"] for x in checks),"source_aware_comparison":source_comparison,"tests":checks,"scope":"Static coverage and data-provenance tests only; no model native runtime public-site fetch or backtest executed"}
    if args.report:args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k!="tests"}))
    for x in checks:
        if not x["passed"]:print(json.dumps(x))
    return 0 if report["status"]=="PASS" else 1
if __name__=="__main__":raise SystemExit(main())
