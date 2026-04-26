# Research & offsets — index (valorant-dumps)

This public repo’s **canonical** artifacts remain dated **`offsets/*.txt`** and **`runs/*.md`** (RVAs + run provenance). The **`docs/`** folder adds **companion research**: how to interpret scans, reference struct seeds, and offline IDA string tables (no game binaries).

> Numeric RVAs and documentation of reverse-engineering process only. VALORANT is a trademark of Riot Games, Inc.

---

## Quick navigation

| I want… | File |
|---------|------|
| **Scan output (RVAs)** | [`../offsets/valorant-offsets-2026-04-26.txt`](../offsets/valorant-offsets-2026-04-26.txt) |
| **Run / environment / coverage** | [`../runs/dump-run-2026-04-26.md`](../runs/dump-run-2026-04-26.md) |
| **Sig vs struct vs IDA discipline** | [`SIG_RESEARCH_MATRIX.md`](SIG_RESEARCH_MATRIX.md) |
| **Promotion rules for generated headers** | [`understand-sdk-directory.md`](understand-sdk-directory.md) |
| **Categorized struct / gameplay reference (validate per patch)** | [`reference-offsets.json`](reference-offsets.json) |
| **Reference ingest report** | [`reference-offsets-validation.txt`](reference-offsets-validation.txt) |
| **Full IDA MCP `find_regex` tables** (machine-generated) | [`ida-mcp-synthesized.md`](ida-mcp-synthesized.md) |
| **Curated high-signal string VAs** | [`IDA_CURATED_ANCHORS.md`](IDA_CURATED_ANCHORS.md) |
| **Latest scan duplicate** | [`valorant-offsets-fresh.txt`](valorant-offsets-fresh.txt) |

---

## Layout

```
offsets/   valorant-offsets-YYYY-MM-DD.txt   ← pattern scanner output (RVAs)
runs/      dump-run-YYYY-MM-DD.md            ← how the capture was taken
docs/      specs + IDA string synthesis      ← this index + matrices + JSON reference
```

---

## Maintainer workflow (sync into this repo)

1. Re-run the offline dumper / pattern scanner; refresh `offsets/*.txt` and `runs/*.md`.  
2. Re-run IDA MCP `find_regex` batch + `summarize_out.py` → replace `docs/ida-mcp-synthesized.md`.  
3. Update `docs/IDA_CURATED_ANCHORS.md` with any new human-picked xref starting points.  
4. Commit with the patch date in the message.

Pattern definitions (`kTier1` / `kTier2`) live in the private vdumper tree (`src/research/valorant_automation.hpp`); they are **not** mirrored here—only **outputs** and research notes.
