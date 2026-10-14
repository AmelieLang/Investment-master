#!/usr/bin/env python3
"""Verify exact public inventory and optionally compare immutable audited originals."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re
import zipfile

SNAPSHOT = 'skill-bundle-snapshots/source-integration-rework2-v1.1-review'
SOURCE_MANIFEST_SHA256 = '583f7cb49ae1725afca280808a9f28c278a03c5d14e64b0521378827a08518af'
ARCHIVE_ROOT = 'Investment-master-public-source-projection-v1'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def safe_path(root, relative):
    path = Path(relative)
    require(not path.is_absolute() and '..' not in path.parts and relative == path.as_posix(), 'unsafe inventory path')
    require(not any((root / Path(*path.parts[:i])).is_symlink() for i in range(1, len(path.parts) + 1)), 'symlink prohibited')
    return root / path


def strings(obj):
    if isinstance(obj, dict):
        for value in obj.values():
            yield from strings(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from strings(value)
    elif isinstance(obj, str):
        yield obj


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
    obj[int(key) if isinstance(obj, list) else key] = value


def differing_pointers(a, b, prefix=''):
    if type(a) is not type(b):
        return [prefix]
    if isinstance(a, dict):
        if set(a) != set(b):
            return [prefix]
        answer = []
        for key in a:
            segment = str(key).replace('~', '~0').replace('/', '~1')
            answer.extend(differing_pointers(a[key], b[key], prefix + '/' + segment))
        return answer
    if isinstance(a, list):
        if len(a) != len(b):
            return [prefix]
        answer = []
        for index in range(len(a)):
            answer.extend(differing_pointers(a[index], b[index], prefix + '/' + str(index)))
        return answer
    return [] if a == b else [prefix]


def privacy_scan(files, root):
    checks = {
        'private_absolute_machine_path': re.compile(r'/(?:Users|home|root|workspace|tmp)/[A-Za-z0-9._-]+'),
        'private_collaboration_url': re.compile(r'https?://[^\s"<>]*(?:fei' + r'shu|lar' + r'ksuite)\.[^\s"<>]+', re.I),
        'fmp_data_endpoint': re.compile(r'https?://(?:[^\s/]+\.)?financial' + r'modelingprep\.com/(?:api|stable)/[^\s"<>]+', re.I),
        'credential_literal': re.compile(r'(?:s' + r'k-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}|A' + r'KIA[0-9A-Z]{16}|gh' + r'p_[A-Za-z0-9]{30,}|github_' + r'pat_[A-Za-z0-9_]{30,})'),
        'literal_bearer_token': re.compile(r'Bearer\s+[A-Za-z0-9._-]{30,}'),
        'literal_secret_assignment': re.compile(r'(?:api[_-]?key|access[_-]?token|password|client[_-]?secret)\s*[=:]\s*[\"\'][A-Za-z0-9_./+-]{16,}[\"\']', re.I),
        'personal_tax_identifier_value': re.compile(r'[\"\'](?:ssn|social_security_number|personal_tax_id|taxpayer_identification_number)[\"\']\s*:\s*[\"\']\d[\d-]{7,}[\"\']', re.I),
        'raw_market_bar_payload': re.compile(r'[\"\']historical[\"\']\s*:\s*\[\s*\{\s*[\"\']date[\"\']\s*:\s*[\"\']\d{4}-\d{2}-\d{2}[\"\'].*?[\"\'](?:adjClose|volume)[\"\']\s*:', re.S),
    }
    findings = []
    for relative in files:
        path = root / relative
        require(path.suffix in ('.json', '.md', '.py') or path.name.endswith('LICENSE'), 'unallowlisted format: ' + relative)
        data = path.read_text(encoding='utf-8')
        for name, pattern in checks.items():
            if pattern.search(data):
                findings.append({'path': relative, 'check': name})
    require(not findings, 'publication-excluded content pattern found: ' + json.dumps(findings))
    return {'patterns_checked': list(checks), 'findings': [],
            'limitation': 'Bounded pattern checks and exact allowlist provenance, not a guarantee of every possible secret encoding or broad legal clearance.'}


def verify(root, source_base=None, archive=None):
    root = root.resolve()
    manifest_path = root / 'PUBLIC-MANIFEST.json'
    manifest = load(manifest_path)
    metadata = load(root / 'PUBLIC-PROJECTION.json')
    mappings = load(root / 'provenance/source-to-public-hashes.json')['files']
    transforms = load(root / 'provenance/locator-transforms.json')['transforms']
    quote = load(root / 'provenance/quote-budget-summary.json')
    expected = {entry['path']: entry for entry in manifest['files']}
    require(len(expected) == len(manifest['files']), 'duplicate public inventory path')
    require('PUBLIC-MANIFEST.json' not in expected, 'manifest self-indexing is invalid')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    require(actual == set(expected) | {'PUBLIC-MANIFEST.json'}, 'public file membership differs from manifest')
    require(manifest['file_count_including_manifest'] == len(actual), 'wrong manifest file count')
    json_docs = {}
    for relative, entry in expected.items():
        path = safe_path(root, relative)
        require(path.is_file(), 'missing inventory file')
        data = path.read_bytes()
        require(len(data) == entry['bytes'] and sha(data) == entry['sha256'], 'inventory hash mismatch: ' + relative)
        if path.suffix == '.json':
            json_docs[relative] = json.loads(data)
    require(len(mappings) == 181 and len({r['source_path'] for r in mappings}) == 181, 'wrong source mapping membership')
    require(len({r['projected_path'] for r in mappings}) == 181, 'duplicate projected source mapping')
    require(len(transforms) == 13 and len({r['source_path'] for r in transforms}) == 6, 'wrong locator transform counts')
    require(len({r['transform_id'] for r in transforms}) == 13, 'duplicate transform id')
    require(all(t['json_pointer'].endswith('/locator') for t in transforms), 'non-locator change proposed')
    require(all(not t['projected_path'].startswith('historical-methods/') for t in transforms), 'historical methods transformation prohibited')
    require(metadata['immutable_source_manifest_sha256'] == SOURCE_MANIFEST_SHA256, 'accepted source identity changed')
    require(metadata['source_files_changed'] == 6 and metadata['locator_replacements'] == 13, 'wrong projection counts')
    require(metadata['accepted_research_files_mutated'] is False and metadata['research_rework_counters_changed'] is False, 'source preservation claim missing')
    require(metadata['native_baseline_code_included'] is False and metadata['no_financial_outcome_dataset_or_result_included'] is True, 'source-only scope missing')
    by_source = {r['source_path']: r for r in mappings}
    changed = set()
    preserved = 0
    historical_count = 0
    licenses = []
    root_counts = Counter()
    for record in mappings:
        source_path = record['source_path']
        projected = record['projected_path']
        path = safe_path(root, projected)
        require(projected in expected, 'mapped file not inventoried')
        data = path.read_bytes()
        require(sha(data) == record['projected_sha256'] and len(data) == record['projected_bytes'], 'mapping projected hash mismatch')
        actually_changed = record['source_sha256'] != record['projected_sha256']
        require(actually_changed == record['content_changed'], 'wrong changed flag')
        if actually_changed:
            changed.add(source_path)
        else:
            preserved += 1
        if projected.startswith('historical-methods/'):
            historical_count += 1
            require(not actually_changed, 'historical methods bytes changed')
        if projected.endswith('LICENSE'):
            licenses.append(projected)
            require(not actually_changed, 'upstream license changed')
        matched_roots = [r for r in metadata['source_root_counts'] if source_path.startswith(r + '/')]
        require(len(matched_roots) == 1, 'source outside audited roots')
        root_counts[matched_roots[0]] += 1
    require(dict(root_counts) == metadata['source_root_counts'], 'source root membership counts changed')
    require(changed == {t['source_path'] for t in transforms}, 'changed files do not exactly match locator transforms')
    require(preserved == 175 and len(changed) == 6, 'source content count mismatch')
    require(historical_count == 14, 'historical methods membership mismatch')
    require(len(licenses) == 20, 'license notice count mismatch')
    require('bundle-manifest.json' not in expected, 'old bundle manifest must not be a root public inventory')
    archived = root / metadata['archived_original_manifest']
    require(sha(archived.read_bytes()) == SOURCE_MANIFEST_SHA256, 'archived original manifest bytes changed')
    old_manifest = load(archived)
    require(len(old_manifest['files']) == 159, 'old source manifest entry count mismatch')
    for record in old_manifest['files']:
        original = by_source[SNAPSHOT + '/' + record['path']]
        require((original['source_sha256'], original['source_bytes']) == (record['sha256'], record['bytes']), 'source hash mapping no longer agrees with frozen original manifest')
    old_locator_hashes = {t['original_value_sha256'] for t in transforms}
    for relative, document in json_docs.items():
        for value in strings(document):
            require(sha(value.encode('utf-8')) not in old_locator_hashes, 'unnecessary original locator expression retained: ' + relative)
    for transform in transforms:
        require(pointer_get(json_docs[transform['projected_path']], transform['json_pointer']) == transform['replacement'], 'projected locator mismatch')
        require(sha(transform['replacement'].encode('utf-8')) == transform['replacement_sha256'], 'replacement digest mismatch')
        require(transform['transform_id'] in by_source[transform['source_path']]['transform_ids'], 'transform missing from hash map')
    require(all(s['projected_direct_prose_words'] <= s['operational_cap_words'] for s in quote['source_totals']), 'audited quotation budget exceeded')
    require({sid: s['projected_direct_prose_words'] for s in quote['source_totals'] for sid in s['source_ids']}['DRU-03'] == 0, 'DRU-03 quotation projection missing')
    require({sid: s['projected_direct_prose_words'] for s in quote['source_totals'] for sid in s['source_ids']}['DAL-10'] == 0, 'DAL-10 quotation projection missing')
    privacy = privacy_scan(sorted(actual), root)
    source_result = {'status': 'not_run_without_source_base', 'limits': 'Portable hash verification alone cannot independently prove original source immutability or semantic equality.'}
    if source_base is not None:
        source_base = source_base.resolve()
        audit_root = source_base / 'rights-publication-audit'
        for name, expected_sha in metadata['audit_inputs_sha256'].items():
            require(sha(safe_path(audit_root, name).read_bytes()) == expected_sha, 'audit metadata changed')
        allow = load(audit_root / 'minimal-allowlist.json')
        require({r['path']: (r['sha256'], r['bytes']) for r in allow['files']} == {
            r['source_path']: (r['source_sha256'], r['source_bytes']) for r in mappings}, 'public map exceeds or differs from exact audit allowlist')
        proposal = load(audit_root / 'proposed-redaction-manifest.json')
        require(len(proposal['transforms']) == len(transforms), 'audit transform count differs')
        for old, public in zip(proposal['transforms'], transforms):
            require((old['path'], old['json_pointer'], old['original_value_sha256'], old['replacement']) ==
                    (public['source_path'], public['json_pointer'], public['original_value_sha256'], public['replacement']), 'public transform differs from audited proposal')
        semantic_changes = []
        original_values = []
        by_file = {}
        for transform in transforms:
            by_file.setdefault(transform['source_path'], []).append(transform)
        original_data = {}
        for record in mappings:
            data = safe_path(source_base, record['source_path']).read_bytes()
            original_data[record['source_path']] = data
            require(sha(data) == record['source_sha256'] and len(data) == record['source_bytes'], 'immutable original changed: ' + record['source_path'])
            if record['source_path'] not in changed:
                require(data == (root / record['projected_path']).read_bytes(), 'unchanged source bytes differ')
                continue
            before = json.loads(data)
            after = json_docs[record['projected_path']]
            actual_changes = differing_pointers(before, after)
            expected_changes = [t['json_pointer'] for t in by_file[record['source_path']]]
            require(set(actual_changes) == set(expected_changes) and len(actual_changes) == len(expected_changes), 'change outside audited locator pointers')
            expected_document = copy.deepcopy(before)
            for transform in by_file[record['source_path']]:
                value = pointer_get(before, transform['json_pointer'])
                original_values.append(value)
                require(sha(value.encode('utf-8')) == transform['original_value_sha256'], 'locator preimage digest mismatch')
                pointer_set(expected_document, transform['json_pointer'], transform['replacement'])
                semantic_changes.append({'path': record['projected_path'], 'json_pointer': transform['json_pointer'], 'only_locator_changed': True})
            expected_bytes = (json.dumps(expected_document, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
            require(expected_bytes == (root / record['projected_path']).read_bytes(), 'projected serialization is not reproducible')
        # The full original locators and identified exact phrase fragments must not recur.
        removed_fragment_patterns = (
            r'Why\s+did\s+you\s+feel\s+it\s+was\s+really\s+big\?',
            r'What\s+are\s+some\s+things\s*\.\.\.\s*you\s+have\s+unlearned\?',
            r'In\s+terms\s+of\s+our\s+portfolio',
            r'We\s+are\s+studying',
        )
        # The regex strings spell no contiguous original paragraph/question in this source file.
        for relative in actual:
            text = (root / relative).read_text(encoding='utf-8')
            require(not any(value in text for value in original_values), 'original locator prose recurred')
            require(not any(re.search(pattern, text) for pattern in removed_fragment_patterns), 'identified unnecessary quotation fragment recurred')
        for record in load(root / 'provenance/source-acceptance-summary.json')['receipts']:
            require(sha(safe_path(source_base, record['source_receipt']).read_bytes()) == record['sha256'], 'source acceptance receipt changed')
        # Recheck originals at the end of the read-only verification pass.
        require(all(safe_path(source_base, path).read_bytes() == data for path, data in original_data.items()), 'original changed during verification')
        source_result = {'status': 'passed', 'audited_original_files_verified': 181,
                         'immutable_source_manifest_entries_verified': 159,
                         'unchanged_source_files_byte_equal': 175,
                         'semantic_locator_changes': semantic_changes,
                         'source_acceptance_receipts_hash_verified': 4,
                         'originals_unchanged_during_verification': True}
    archive_result = {'status': 'not_run_without_zip'}
    if archive is not None:
        with zipfile.ZipFile(archive) as zf:
            names = zf.namelist()
            zip_expected = {ARCHIVE_ROOT + '/' + p for p in actual}
            require(len(names) == len(set(names)) and set(names) == zip_expected, 'archive membership differs')
            require(names == sorted(names), 'archive entries not sorted')
            for name in names:
                relative = name[len(ARCHIVE_ROOT) + 1:]
                require(zf.read(name) == (root / relative).read_bytes(), 'archive bytes differ from projection')
                info = zf.getinfo(name)
                require(info.date_time == (2026, 10, 13, 0, 0, 0), 'archive timestamp not deterministic')
                require((info.external_attr >> 16) == 0o100644, 'archive mode not deterministic')
                require(info.compress_type == zipfile.ZIP_DEFLATED, 'archive compression differs')
            require(zf.testzip() is None, 'archive CRC error')
        archive_result = {'status': 'passed', 'file_count': len(names), 'sha256': sha(archive.read_bytes()), 'bytes': archive.stat().st_size}
    return {'schema_version': 'public-source-projection-verification.v1', 'status': 'PASS',
            'projection_file_count': len(actual), 'public_manifest_sha256': sha(manifest_path.read_bytes()),
            'audited_source_file_count': len(mappings), 'locator_replacements': len(transforms),
            'changed_source_file_count': len(changed), 'unchanged_source_file_count': preserved,
            'historical_methods_files_preserved': historical_count, 'upstream_license_files_preserved': len(licenses),
            'old_manifest_retained_as_provenance_only': True,
            'FMP_raw_or_derived_results_excluded_by_exact_audited_source_scope': True,
            'privacy_scan': privacy, 'source_verification': source_result, 'archive_verification': archive_result,
            'limits': ['No remote publication or writes performed.', 'This is source packaging acceptance evidence, not runtime, routes, investment outcomes or comprehensive legal clearance.', 'A hash inventory is an integrity check, not independent authentication without a trusted external receipt.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--projection', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--source-base', type=Path)
    parser.add_argument('--zip', type=Path)
    parser.add_argument('--json-output', type=Path)
    args = parser.parse_args()
    try:
        result = verify(args.projection, args.source_base, args.zip)
    except (ValueError, AssertionError, KeyError, OSError, json.JSONDecodeError, zipfile.BadZipFile) as error:
        result = {'schema_version': 'public-source-projection-verification.v1', 'status': 'FAIL', 'error': str(error)}
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
