#!/usr/bin/env python3
"""Build a separate source-only projection from exact audited inputs. Stdlib only."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

VERSION = '1.0-source-only'
SNAPSHOT = 'skill-bundle-snapshots/source-integration-rework2-v1.1-review'
ARCHIVE_ROOT = 'Investment-master-public-source-projection-v1'
TOOL_NAMES = ('build_public_projection.py', 'verify_public_projection.py', 'test_public_projection.py')
RECEIPTS = (
    'investment-master-skill-source-rework2-v1.1-acceptance-receipt.json',
    'reviews/V2-D-source-integration-rework2-review-3.json',
    'reviews/V2-B-technology-historical-extension-review-0.json',
    'reviews/V2-B-native-baseline-method-ledger-review-0.json',
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def pointer_get(obj, pointer):
    for part in pointer.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        obj = obj[int(part)] if isinstance(obj, list) else obj[part]
    return obj


def pointer_set(obj, pointer, value):
    parts = pointer.split('/')[1:]
    for part in parts[:-1]:
        part = part.replace('~1', '/').replace('~0', '~')
        obj = obj[int(part)] if isinstance(obj, list) else obj[part]
    key = parts[-1].replace('~1', '/').replace('~0', '~')
    if isinstance(obj, list):
        obj[int(key)] = value
    else:
        obj[key] = value


def projected_path(source_path):
    prefix = SNAPSHOT + '/'
    if source_path.startswith(prefix):
        relative = source_path[len(prefix):]
        if relative == 'bundle-manifest.json':
            return 'provenance/accepted-source-bundle-manifest.json'
        return relative
    return source_path


def safe_relative(value):
    path = Path(value)
    assert not path.is_absolute() and '..' not in path.parts, 'unsafe relative path'
    return path


def deterministic_zip(directory, target):
    assert not target.exists(), 'archive target already exists'
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(directory.rglob('*')):
            if not path.is_file():
                continue
            assert not path.is_symlink(), 'symlink prohibited'
            name = ARCHIVE_ROOT + '/' + path.relative_to(directory).as_posix()
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 13, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100644 << 16)
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def build(base, output, generated_at):
    assert not output.exists(), 'output already exists; use a new directory'
    audit_dir = base / 'rights-publication-audit'
    audit_names = ('report.json', 'proposed-redaction-manifest.json', 'minimal-allowlist.json',
                   'quotation-inventory.json', 'input-hashes.json', 'projection-verification.json')
    audit = {name: json.loads((audit_dir / name).read_text(encoding='utf-8')) for name in audit_names}
    audit_hashes = {name: sha((audit_dir / name).read_bytes()) for name in audit_names}
    allow = audit['minimal-allowlist.json']
    proposal = audit['proposed-redaction-manifest.json']
    assert len(allow['files']) == 181
    assert allow['source_roots'] == [SNAPSHOT, 'tech-historical-extension', 'benchmark/baseline-method-sources']
    assert len(proposal['transforms']) == 13
    assert len({t['path'] for t in proposal['transforms']}) == 6
    assert proposal['input_manifest_sha256'] == '583f7cb49ae1725afca280808a9f28c278a03c5d14e64b0521378827a08518af'
    source_manifest = base / SNAPSHOT / 'bundle-manifest.json'
    assert sha(source_manifest.read_bytes()) == proposal['input_manifest_sha256']
    assert {r['path']: (r['sha256'], r['bytes']) for r in allow['files']} == {
        r['path']: (r['sha256'], r['bytes']) for r in audit['input-hashes.json']['files']}
    output.mkdir(parents=True)
    source_bytes = {}
    for record in allow['files']:
        source_path = record['path']
        source = base / safe_relative(source_path)
        assert not source.is_symlink() and source.is_file(), 'missing or symlink input'
        data = source.read_bytes()
        assert len(data) == record['bytes'] and sha(data) == record['sha256'], 'audit input changed: ' + source_path
        source_bytes[source_path] = data
        destination = output / safe_relative(projected_path(source_path))
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)

    transforms = []
    by_file = {}
    for index, transform in enumerate(proposal['transforms'], 1):
        assert transform['path'] in source_bytes
        assert transform['json_pointer'].endswith('/locator')
        assert not projected_path(transform['path']).startswith('historical-methods/')
        record = {
            'transform_id': 'LOC-' + str(index).zfill(2),
            'source_path': transform['path'],
            'projected_path': projected_path(transform['path']),
            'json_pointer': transform['json_pointer'],
            'original_value_sha256': transform['original_value_sha256'],
            'replacement': transform['replacement'],
            'replacement_sha256': sha(transform['replacement'].encode('utf-8')),
            'source_ids': transform['source_ids'],
            'priority': transform['priority'],
            'operation': 'locator-only public-copy replacement',
        }
        transforms.append(record)
        by_file.setdefault(transform['path'], []).append(record)
    for source_path, changes in by_file.items():
        original_text = source_bytes[source_path].decode('utf-8')
        document = json.loads(original_text)
        assert original_text == json.dumps(document, indent=2, ensure_ascii=False) + '\n', 'unexpected serialization'
        for change in changes:
            before = pointer_get(document, change['json_pointer'])
            assert isinstance(before, str) and sha(before.encode('utf-8')) == change['original_value_sha256']
            pointer_set(document, change['json_pointer'], change['replacement'])
        write_json(output / projected_path(source_path), document)

    mapping = []
    for record in allow['files']:
        target = projected_path(record['path'])
        data = (output / target).read_bytes()
        mapping.append({
            'source_path': record['path'], 'projected_path': target,
            'source_sha256': record['sha256'], 'source_bytes': record['bytes'],
            'projected_sha256': sha(data), 'projected_bytes': len(data),
            'content_changed': sha(data) != record['sha256'],
            'path_changed': target != record['path'],
            'transform_ids': [t['transform_id'] for t in transforms if t['source_path'] == record['path']],
            'publication_condition': record['publication_condition'],
        })
    assert sum(r['content_changed'] for r in mapping) == 6
    write_json(output / 'provenance/source-to-public-hashes.json', {
        'schema_version': 'source-to-public-hash-map.v1', 'projection_version': VERSION,
        'scope': 'Exactly the 181 audited allowlist files; no additional upstream code or research.',
        'files': mapping,
    })
    write_json(output / 'provenance/locator-transforms.json', {
        'schema_version': 'applied-public-locator-projection.v1',
        'audit_proposal_sha256': audit_hashes['proposed-redaction-manifest.json'],
        'transform_count': 13, 'affected_files_count': 6, 'transforms': transforms,
        'original_expression_not_duplicated': True,
    })
    receipt_info = []
    for name in RECEIPTS:
        path = base / safe_relative(name)
        data = path.read_bytes()
        document = json.loads(data)
        receipt_info.append({
            'source_receipt': name, 'sha256': sha(data),
            'status': document.get('final_status', document.get('status', document.get('verdict'))),
            'source_scope_only': True,
        })
    write_json(output / 'provenance/source-acceptance-summary.json', {
        'schema_version': 'source-acceptance-provenance.v1',
        'receipts': receipt_info,
        'immutable_source_manifest_sha256': proposal['input_manifest_sha256'],
        'technology_extension_manifest_sha256': sha((base / 'tech-historical-extension/manifest.json').read_bytes()),
        'baseline_ledger_sha256': sha((base / 'benchmark/baseline-method-sources/ledger.json').read_bytes()),
        'accepted_source_counters_preserved': True,
        'status_labels_in_copied_sources': 'Frozen historical build metadata; exact-hash external receipts establish bounded source acceptance.',
        'technology_extension_scope': 'Ten qualitative bounded ARK research-team/Ron Baron rules. Version uncertainty, named authorship, case limits and independently authored application design remain unchanged. No routing or runtime activation.',
        'baseline_ledger_scope': 'Bounded concept/software-attribution evidence only; exact thresholds and confidence scales remain repository-author choices. Not a production method freeze.',
        'publication_authorization': 'Source receipts are evidence of bounded research acceptance, not authorization to publish or deploy.',
    })
    dry = audit['projection-verification.json']
    inventory = audit['quotation-inventory.json']
    quote_summary = []
    for record in inventory['source_totals']:
        ids = record['source_ids']
        projected_words = 0 if ('DRU-03' in ids or 'DAL-10' in ids) else record['unlicensed_direct_prose_words_occurrence_sensitive']
        quote_summary.append({
            'original_url': record['original_url'], 'source_ids': ids,
            'projected_direct_prose_words': projected_words, 'operational_cap_words': 25,
            'measurement_scope': 'Bounded occurrence-sensitive direct-prose inventory from the audit, preserved except the 13 locator replacements.',
        })
    write_json(output / 'provenance/quote-budget-summary.json', {
        'schema_version': 'public-projection-quote-budget.v1',
        'audit_inventory_sha256': audit_hashes['quotation-inventory.json'],
        'source_totals': quote_summary,
        'identified_removed_fragment_digests': [
            {'fragment_id': f['fragment_id'], 'sha256': f['fragment_sha256'], 'words_per_occurrence': f['words_per_occurrence']}
            for s in inventory['source_totals'] if any(i in ('DRU-03', 'DAL-10') for i in s['source_ids'])
            for f in s['fragment_counts']
        ],
        'limits': 'This operational excerpt check is bounded; it is not a blanket copyright clearance or the legal definition of fair use.',
        'all_audit_dry_run_conditions_passed': dry['all_13_pointers_exist_and_hash_match'] and dry['all_identified_Dru_03_and_Dal_10_body_fragments_removed_in_simulation'],
    })
    write_json(output / 'PUBLIC-PROJECTION.json', {
        'schema_version': 'investment-master-public-source-projection.v1',
        'projection_version': VERSION, 'generated_at_utc': generated_at,
        'destination_repository': 'AmelieLang/Investment-master',
        'artifact_state': 'local source-only packaging candidate awaiting independent projection acceptance; no remote publication performed',
        'accepted_source_snapshot': SNAPSHOT,
        'immutable_source_manifest_sha256': proposal['input_manifest_sha256'],
        'archived_original_manifest': 'provenance/accepted-source-bundle-manifest.json',
        'archived_original_manifest_scope': 'Original accepted snapshot bytes only. It is historical provenance and does not index this public projection.',
        'public_inventory': 'PUBLIC-MANIFEST.json',
        'hash_map': 'provenance/source-to-public-hashes.json',
        'applied_locator_transforms': 'provenance/locator-transforms.json',
        'audit_inputs_sha256': audit_hashes,
        'audited_input_file_count': 181,
        'source_root_counts': {SNAPSHOT: 160, 'tech-historical-extension': 17, 'benchmark/baseline-method-sources': 4},
        'locator_replacements': 13, 'source_files_changed': 6, 'source_files_content_unchanged': 175,
        'historical_methods_files_changed': 0,
        'accepted_research_files_mutated': False, 'research_rework_counters_changed': False,
        'native_baseline_code_included': False,
        'no_financial_outcome_dataset_or_result_included': True,
        'FMP_release_gate': 'Exclude all raw FMP payloads and FMP-derived numeric outcomes, summaries and displays. Redistribution rights remain unresolved; this projection includes no such data.',
        'FMP_terms_url': 'https://site.financialmodelingprep.com/terms-of-service',
        'source_attribution_boundary': 'Independent issuer observations retain their original provenance; no FMP-origin value is relabelled as independently sourced.',
        'excluded_materials': ['Private paths and personal tax identifiers', 'Credentials and authentication files', 'Private collaboration links', 'Raw or FMP-derived financial results', 'Full books, reports, transcripts, images and downloaded source attachments', 'ARK workbooks, model code and reproduced formula/layout expression', 'Native baseline code not enumerated in the audited allowlist'],
        'license_scope': 'Exact upstream licenses and source attributions retained. No new blanket license for third-party publications or data is asserted.',
        'scope_limit': 'Separate packaging projection only; original investment rules, source claims, historical methods, activation gates and research acceptance remain unchanged.',
    })
    license_paths = sorted(r['projected_path'] for r in mapping if r['projected_path'].endswith('LICENSE'))
    notices = '''# Third-party notices and rights boundaries\n\nThis is a separate public source projection of an independently assembled research Skill. It changes only 13 source locators in six files. It does not establish a new investor-authored algorithm, accept a runtime, activate routes, or relicense external investor publications.\n\n## Software notices\n\n- finterm.ai: Copyright (c) 2026 finterm.ai. Exact MIT license retained at vendor/finterm/LICENSE and licenses/finterm-ai__investment-skills__LICENSE. Its adapted software/documentation remains within that notice's scope.\n- Virat Singh: Copyright (c) 2024 Virat Singh. Exact MIT notice retained at licenses/virattt__ai-hedge-fund__LICENSE. The conceptual baseline ledger records the native repository pin and software-author attribution; native baseline code is not included here.\n- The independently written wrappers, questions and application designs retain explicit auditor/repository-author labels. Metric proxies, thresholds, prompts and confidence scales are not thereby certified as named investors' own procedures.\n- Other verified upstream mechanism-lineage notices are retained unchanged at the paths listed below. Retaining a notice does not imply that all upstream code, dependencies or expressive works are included or cleared.\n\n## Research and data rights\n\nLinked books, letters, articles, interviews, fund research and issuer filings remain subject to their owners' applicable rights. Public access and an upstream MIT software license do not relicense underlying prose, reports, data, graphics or logos. Only the audited bounded facts, paraphrases, source locators and brief authentication anchors are included.\n\nARK's source-specific CC BY-NC workbook/model materials remain noncommercial; no workbook, model code, translated formula or reproduced layout is included. ARK research-team and named-author attribution, Ron Baron's signed-letter limits and all source-version caveats are retained.\n\nNo raw FMP payloads or FMP-derived numerical results, returns, success-rate summaries or displays are included. Applicable public-display and derived-data redistribution rights remain unresolved. Independently obtained issuer facts retain their original issuer-source provenance.\n\nThere is no affiliation with, approval by, or endorsement from any named investor, firm or upstream software author. Historical provenance manifests describe their original snapshots only; PUBLIC-MANIFEST.json is the inventory for these projected bytes.\n\n## Exact retained license locations\n\n'''
    notices += '\n'.join('- ' + path for path in license_paths) + '\n'
    (output / 'THIRD-PARTY-NOTICES.md').write_text(notices, encoding='utf-8')
    publication = '''# Public source projection v1\n\nThis directory is a source-only packaging candidate, separate from its immutable accepted research snapshot. No remote write, release, runtime activation, stock opinion or financial outcome has been produced by this build.\n\n## Inventory and provenance\n\n- PUBLIC-MANIFEST.json indexes every delivered file except itself with freshly computed SHA-256 and byte lengths.\n- PUBLIC-PROJECTION.json records the immutable accepted source manifest, audit input hashes, scope and rights gates.\n- provenance/source-to-public-hashes.json maps all 181 audited input files to their public locations and hashes. Exactly six source files have changed content, solely at the 13 recorded locator pointers.\n- provenance/accepted-source-bundle-manifest.json is an unchanged archived original manifest. Its hashes apply only to the accepted original snapshot, never the projected files. It is not a second release inventory.\n- The technology extension and conceptual baseline ledger remain separate source scopes. Their old candidate labels are immutable historical build metadata; the hashed external source-acceptance receipts are identified in provenance/source-acceptance-summary.json. No source-acceptance receipt grants publication or runtime authorization.\n\nAll historical-methods files, investment rules outside the locator fields, licenses and attributions remain unchanged. FMP data and numeric results remain excluded pending applicable rights verification. The numeric observations, metadata, heuristic thresholds and synthetic examples already in the exact audited source allowlist retain their existing meaning; they are not a newly generated real-world financial result.\n\n## Verify\n\nUse Python 3.10 or later. No third-party packages, network connection or authentication are needed.\n\n    python tools/verify_public_projection.py --projection .\n    python tools/test_public_projection.py --projection .\n\nTo verify original-source immutability and the exact semantic differences, supply the directory holding the original relative input trees and rights-publication-audit as --source-base. It is a local command-line argument; no machine path is embedded in this package. Add --zip to verify archive contents. Verification writes nothing unless an explicit --json-output path is supplied.\n\n## Reproduce\n\nThe builder reads only the exact audited allowlist files, the audit metadata and four source-acceptance receipts. It creates a new output directory and refuses an existing output or archive. It does not mutate any original input. Use the same generated-at value recorded in PUBLIC-PROJECTION.json for byte-for-byte metadata reproduction.\n\n    python tools/build_public_projection.py --source-base INPUT_BASE --output NEW_DIRECTORY --generated-at RECORDED_UTC --zip NEW_ARCHIVE.zip\n\nZIP entries are sorted, use fixed timestamps and ordinary read-only data-file modes, and contain one stable top-level directory. The archive itself is excluded from the projection inventory. A transport receipt must hash the final ZIP after creation. Independently review and re-scan the exact staging tree before any later authorized publication.\n'''
    (output / 'PUBLICATION.md').write_text(publication, encoding='utf-8')
    tool_dir = Path(__file__).resolve().parent
    for name in TOOL_NAMES:
        destination = output / 'tools' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(tool_dir / name, destination)
    # Recheck all source bytes after packaging; no mutation is permitted.
    for path, data in source_bytes.items():
        assert (base / path).read_bytes() == data, 'source mutated during build'
    entries = []
    for path in sorted(output.rglob('*')):
        if path.is_file():
            data = path.read_bytes()
            entries.append({'path': path.relative_to(output).as_posix(), 'bytes': len(data), 'sha256': sha(data)})
    write_json(output / 'PUBLIC-MANIFEST.json', {
        'schema_version': 'investment-master-public-inventory.v1', 'projection_version': VERSION,
        'generated_at_utc': generated_at, 'index_scope': 'All delivered files except this manifest; the archive is separate.',
        'file_count_including_manifest': len(entries) + 1, 'files': entries,
        'original_source_manifest_is_provenance_only': True,
    })
    return {'projection_file_count': len(entries) + 1, 'audited_input_files': len(mapping),
            'changed_source_files': 6, 'locator_replacements': 13,
            'public_manifest_sha256': sha((output / 'PUBLIC-MANIFEST.json').read_bytes())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-base', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--generated-at', required=True)
    parser.add_argument('--zip', type=Path)
    args = parser.parse_args()
    result = build(args.source_base.resolve(), args.output.resolve(), args.generated_at)
    if args.zip:
        deterministic_zip(args.output.resolve(), args.zip.resolve())
        result.update({'zip_sha256': sha(args.zip.read_bytes()), 'zip_bytes': args.zip.stat().st_size})
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
