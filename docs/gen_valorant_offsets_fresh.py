"""
Merge vdumper .text scan output + reference-offsets.json into valorant-offsets-fresh.txt.
Run from repo root or this directory:
  python output/sdk-offsets/gen_valorant_offsets_fresh.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# vdumper: script in output/sdk-offsets/ beside scan + JSON.
# valorant-dumps: script in docs/; dated scan in ../offsets/; JSON in docs/.
if (HERE / "valorant-offsets-2026-04-26.txt").is_file():
    SCAN_FILE = HERE / "valorant-offsets-2026-04-26.txt"
    REF_FILE = HERE / "reference-offsets.json"
    OUT_FILE = HERE / "valorant-offsets-fresh.txt"
else:
    SCAN_FILE = HERE.parent / "offsets" / "valorant-offsets-2026-04-26.txt"
    REF_FILE = HERE / "reference-offsets.json"
    OUT_FILE = HERE / "valorant-offsets-fresh.txt"

PAIR_RE = re.compile(r"^([^:]+):\s*(0x[0-9A-Fa-f]+)\s*$", re.I)


def norm_hex(hexstr: str) -> str:
    return "0x" + format(int(hexstr, 16), "X")


def load_scan_pairs(path: Path) -> tuple[list[tuple[str, str]], list[str]]:
    pairs: list[tuple[str, str]] = []
    missing: list[str] = []
    if not path.is_file():
        return pairs, missing
    in_missing = False
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("// -"):
            missing.append(s[4:].strip())
            continue
        if "Missing" in s and "signature" in s.lower():
            in_missing = True
            continue
        if not s or s.startswith("//"):
            continue
        m = PAIR_RE.match(s)
        if m:
            pairs.append((m.group(1).strip(), norm_hex(m.group(2).strip())))
    return pairs, missing


def main() -> int:
    scan_pairs, missing = load_scan_pairs(SCAN_FILE)
    seen = {k for k, _ in scan_pairs}

    lines: list[str] = [
        "// VALORANT offsets — merged fresh export",
        "// Section A: kernel PE + offline pattern scanner (.text) — vdumper",
        "// Section B: reference-offsets.json — struct / layout (re-validate each patch; not all are module RVAs)",
        "// See SIG_RESEARCH_MATRIX.md for A vs D semantics.",
        "",
        "// --- Section A (pattern scan) ---",
    ]
    for k, v in sorted(scan_pairs, key=lambda x: x[0].lower()):
        lines.append(f"{k}: {v}")

    if not REF_FILE.is_file():
        lines.append("")
        lines.append("// ERROR: reference-offsets.json not found")
        OUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return 1

    data = json.loads(REF_FILE.read_text(encoding="utf-8-sig"))
    entries = data.get("entries") or []
    by_cat: dict[str, list[tuple[str, str]]] = {}
    for e in entries:
        cat = e.get("category") or "Uncategorized"
        key = e.get("key")
        val = e.get("value_hex")
        if not key or not val:
            continue
        val = norm_hex(str(val).strip())
        by_cat.setdefault(cat, []).append((str(key), val))

    lines.append("")
    lines.append("// --- Section B (reference sheet by category) ---")
    for cat in sorted(by_cat.keys()):
        lines.append(f"// [{cat}]")
        for k, v in sorted(by_cat[cat], key=lambda x: x[0].lower()):
            if k in seen:
                continue
            lines.append(f"{k}: {v}")
        lines.append("")

    lines.append("// --- Scanner Tier2 not resolved (still missing on this build) ---")
    for m in missing:
        lines.append(f"// - {m}")

    OUT_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print("Wrote", OUT_FILE, "lines", len(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
