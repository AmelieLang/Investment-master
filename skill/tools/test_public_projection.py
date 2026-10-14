#!/usr/bin/env python3
"""Portable regression and rejection tests for source-only projection integrity."""
import argparse
import contextlib
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument('--projection', type=Path, default=Path(__file__).resolve().parents[1])
PARSER.add_argument('--source-base', type=Path)
PARSER.add_argument('--zip', type=Path)
ARGS = PARSER.parse_args()
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location('projection_verifier', Path(__file__).resolve().with_name('verify_public_projection.py'))
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


@contextlib.contextmanager
def copy_projection():
    with tempfile.TemporaryDirectory(prefix='projection-test-') as name:
        output = Path(name) / 'candidate'
        shutil.copytree(ARGS.projection, output)
        yield output


def rewrite_manifest(root, relative):
    path = root / 'PUBLIC-MANIFEST.json'
    manifest = json.loads(path.read_text())
    data = (root / relative).read_bytes()
    for record in manifest['files']:
        if record['path'] == relative:
            record['sha256'] = hashlib.sha256(data).hexdigest()
            record['bytes'] = len(data)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')


class ProjectionTests(unittest.TestCase):
    def test_exact_projection_passes(self):
        result = VERIFIER.verify(ARGS.projection, ARGS.source_base, ARGS.zip)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(result['locator_replacements'], 13)
        self.assertEqual(result['changed_source_file_count'], 6)
        self.assertEqual(result['unchanged_source_file_count'], 175)

    def test_extra_file_rejected(self):
        with copy_projection() as root:
            (root / 'extra.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'membership'):
                VERIFIER.verify(root)

    def test_missing_license_rejected(self):
        with copy_projection() as root:
            (root / 'vendor/finterm/LICENSE').unlink()
            with self.assertRaisesRegex(ValueError, 'membership'):
                VERIFIER.verify(root)

    def test_file_byte_tamper_rejected(self):
        with copy_projection() as root:
            with (root / 'SKILL.md').open('ab') as file:
                file.write(b'\nChanged without a new receipt.\n')
            with self.assertRaisesRegex(ValueError, 'inventory hash mismatch'):
                VERIFIER.verify(root)

    def test_old_manifest_not_repurposed(self):
        manifest = json.loads((ARGS.projection / 'PUBLIC-MANIFEST.json').read_text())
        paths = {record['path'] for record in manifest['files']}
        self.assertNotIn('bundle-manifest.json', paths)
        self.assertIn('provenance/accepted-source-bundle-manifest.json', paths)

    def test_projected_locator_tamper_rejected_even_with_fresh_inventory(self):
        with copy_projection() as root:
            relative = 'methods/stanley-druckenmiller.json'
            document = json.loads((root / relative).read_text())
            document['rules'][4]['original_record']['evidence_anchors'][0]['locator'] = 'Unreviewed source locator'
            (root / relative).write_text(json.dumps(document, indent=2, ensure_ascii=False) + '\n')
            rewrite_manifest(root, relative)
            with self.assertRaisesRegex(ValueError, 'mapping projected hash mismatch'):
                VERIFIER.verify(root)

    def test_source_claim_boundary(self):
        document = json.loads((ARGS.projection / 'PUBLIC-PROJECTION.json').read_text())
        self.assertFalse(document['native_baseline_code_included'])
        self.assertTrue(document['no_financial_outcome_dataset_or_result_included'])
        self.assertFalse(document['research_rework_counters_changed'])
        self.assertFalse(document['accepted_research_files_mutated'])

    def test_historical_methods_unchanged(self):
        mappings = json.loads((ARGS.projection / 'provenance/source-to-public-hashes.json').read_text())['files']
        rows = [row for row in mappings if row['projected_path'].startswith('historical-methods/')]
        self.assertEqual(len(rows), 14)
        self.assertTrue(all(row['source_sha256'] == row['projected_sha256'] for row in rows))

    def test_privacy_scanner_rejects_excluded_content(self):
        with tempfile.TemporaryDirectory(prefix='projection-scan-test-') as name:
            root = Path(name)
            cases = [
                '/' + 'Users/example/private/file',
                'https://example.' + 'feishu.cn/doc/private',
                'https://financial' + 'modelingprep.com/api/v3/historical-price-full/EXAMPLE',
                's' + 'k-proj-' + 'a' * 40,
                '{"personal_' + 'tax_id": "' + '123' + '-45-' + '6789"}',
            ]
            for index, case in enumerate(cases):
                (root / 'probe.md').write_text(case)
                with self.subTest(case_index=index):
                    with self.assertRaisesRegex(ValueError, 'publication-excluded'):
                        VERIFIER.privacy_scan(['probe.md'], root)

    def test_source_immutable_and_only_locators_differ(self):
        if ARGS.source_base is None:
            self.skipTest('source-base not supplied')
        result = VERIFIER.verify(ARGS.projection, ARGS.source_base)
        evidence = result['source_verification']
        self.assertEqual(evidence['audited_original_files_verified'], 181)
        self.assertEqual(len(evidence['semantic_locator_changes']), 13)
        self.assertTrue(evidence['originals_unchanged_during_verification'])


if __name__ == '__main__':
    unittest.main(argv=['test_public_projection.py'], verbosity=2)
