# Public source projection v1

This directory is a source-only packaging candidate, separate from its immutable accepted research snapshot. No remote write, release, runtime activation, stock opinion or financial outcome has been produced by this build.

## Inventory and provenance

- PUBLIC-MANIFEST.json indexes every delivered file except itself with freshly computed SHA-256 and byte lengths.
- PUBLIC-PROJECTION.json records the immutable accepted source manifest, audit input hashes, scope and rights gates.
- provenance/source-to-public-hashes.json maps all 181 audited input files to their public locations and hashes. Exactly six source files have changed content, solely at the 13 recorded locator pointers.
- provenance/accepted-source-bundle-manifest.json is an unchanged archived original manifest. Its hashes apply only to the accepted original snapshot, never the projected files. It is not a second release inventory.
- The technology extension and conceptual baseline ledger remain separate source scopes. Their old candidate labels are immutable historical build metadata; the hashed external source-acceptance receipts are identified in provenance/source-acceptance-summary.json. No source-acceptance receipt grants publication or runtime authorization.

All historical-methods files, investment rules outside the locator fields, licenses and attributions remain unchanged. FMP data and numeric results remain excluded pending applicable rights verification. The numeric observations, metadata, heuristic thresholds and synthetic examples already in the exact audited source allowlist retain their existing meaning; they are not a newly generated real-world financial result.

## Verify

Use Python 3.10 or later. No third-party packages, network connection or authentication are needed.

    python tools/verify_public_projection.py --projection .
    python tools/test_public_projection.py --projection .

To verify original-source immutability and the exact semantic differences, supply the directory holding the original relative input trees and rights-publication-audit as --source-base. It is a local command-line argument; no machine path is embedded in this package. Add --zip to verify archive contents. Verification writes nothing unless an explicit --json-output path is supplied.

## Reproduce

The builder reads only the exact audited allowlist files, the audit metadata and four source-acceptance receipts. It creates a new output directory and refuses an existing output or archive. It does not mutate any original input. Use the same generated-at value recorded in PUBLIC-PROJECTION.json for byte-for-byte metadata reproduction.

    python tools/build_public_projection.py --source-base INPUT_BASE --output NEW_DIRECTORY --generated-at RECORDED_UTC --zip NEW_ARCHIVE.zip

ZIP entries are sorted, use fixed timestamps and ordinary read-only data-file modes, and contain one stable top-level directory. The archive itself is excluded from the projection inventory. A transport receipt must hash the final ZIP after creation. Independently review and re-scan the exact staging tree before any later authorized publication.
