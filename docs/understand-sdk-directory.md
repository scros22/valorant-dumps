# SDK Offsets Directory Specifications

The **`docs/`** folder in [valorant-dumps](https://github.com/scros22/valorant-dumps) stores the same **specs and reference data** that the vdumper tree keeps under `output/sdk-offsets/` (plus IDA synthesis). **Canonical RVAs** remain under `../offsets/` in this repo.

## Master index
- **`SDK_DIRECTORY_INDEX.md`** — single TOC for this folder + links to IDA MCP tables, dumper scanner source, and example consumers (`offsets.hpp`). Read this first.

## Required Artifacts
- `SIG_RESEARCH_MATRIX.md`: How **code sigs** (Tier1/2), **IDA anchors**, and **reference struct offsets** map to external vs internal use — read before merging datasets.
- `reference-offsets.json`: Parsed reference dataset with categories, line provenance, and ingest summary.
- `reference-offsets-validation.txt`: Human-readable ingest report containing duplicate/conflict checks.
- `offsets.json`: Runtime-validated offsets promoted from scanning stages.
- `offsets.hpp`: Header generated from validated offsets only.

## Quality Gates
- Do not promote values from `reference-offsets.json` directly to runtime outputs without scan confirmation.
- Reject promotion if ingest report contains `conflicting_values > 0`.
- Keep line provenance for every imported reference key.
- Preserve previous successful outputs unless an explicit clean flag is provided.

## Proof-Backed Workflow
1. Ingest reference text dataset.
2. Validate duplicate/conflict metrics.
3. Cross-check each promoted key using scanner outputs.
4. Emit canonical JSON and generated header only after validation passes.
