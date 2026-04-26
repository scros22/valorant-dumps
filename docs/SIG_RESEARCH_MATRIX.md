# Signature and offset research matrix (offline dumper)

This file explains **what is “solid” for which consumer** so externals, internals, and the dumper do not mix incompatible evidence.

**Master folder index:** [`SDK_DIRECTORY_INDEX.md`](SDK_DIRECTORY_INDEX.md) (every artifact + external/internal map).

---

## 1. Four resolution classes

| Class | Source | Stability | External ESP | Internal / SDK gen |
|-------|--------|------------|----------------|---------------------|
| **A — Code sig Tier1** | `src/research/valorant_automation.hpp` → `kTier1[]` | Strong until Epic rewrites prologues | **`GWorld`** global (RIP) is the main one; optional weapon/math helpers | **`ProcessEvent`**, `StaticFindObject`, `StaticLoadObject`, `FMemoryMalloc`, spread helpers, etc. |
| **B — Code sig Tier2** | Same file → `kTier2` `AltGroup` | Weaker; order matters; some patterns are UE-generic | Rarely needed if `GWorld` resolves | **`FNamePool`**, **`GObjects`**, **`GEngine`**, `FName::ToString`, `FName::GetEntry` when Tier2 hits |
| **C — IDA string / path anchor** | MCP + `ida-mcp-synthesized.md`, `DUMP_FROM_IDA.md` | Great for **version sanity**; not RVAs by themselves | Validate you are on the right build; xref for struct layout | Same; xref → decompile for vtable / `ProcessEvent` dispatch sites |
| **D — Struct member** | `reference-offsets.json` (ingested reference sheet) | **Patch-fragile**; must be re-probed | **Primary** for pawn, camera, mesh, team, damage | Same offsets in generated headers **after** your validation gate |

Rule: **never** treat class **D** as if it were class **A**. The scanner never emits `AcknowledgedPawn` or `CameraCachePrivate`; those stay in the reference JSON until you promote them via your own checks (`understand-sdk-directory.md`).

---

## 2. Tier1 symbols (code patterns, deterministic order)

| Symbol | Role |
|--------|------|
| `ProcessEvent` | UObject script dispatch |
| `StaticFindObject` / `StaticLoadObject` | Resolve `UClass` / assets without a full object walk |
| `BoneMatrix` | Mesh / bone math |
| `SetOutlineMode` | Rendering hook (build-specific) |
| `FMemoryMalloc` | Allocator / low-level hooks |
| `PlayFinisher`, `GetSpreadValues`, `GetSpreadAngles`, `ToVectorAndNormalize`, `ToAngleAndNormalize`, `GetFiringLocationAndDirection`, `TriggerVeh` | Gameplay / weapon pipeline helpers |
| `GWorld` | **RIP-relative** global → start of world graph |

---

## 3. Tier2 groups (first matching pattern wins)

| Group | Intent | Notes |
|-------|--------|--------|
| `FNamePool` | `gnames` slot | Includes ProtonDev exact + looser FName init idioms + short `lea …; jmp` variant |
| `GObjects` | `gobjects` slot | Classic `mov rax,[rip]` + index; **plus** chunked `… 4C 8D 04 D1` path (UE5-style) |
| `GEngine` | `gengine` slot | rbx / vtbl / callsite + branch-on-null variant |
| `FName::ToString` | `fname_to_string` | Multiple prologues |
| `FName::GetEntry` | `fname_get_entry` | FName field at +4 or +8 variant |

If every pattern fails, the emitted `valorant-offsets*.txt` lists `// - GroupName` under missing — **expected** on heavily customized builds until you add a new first-winning pattern from IDA.

---

## 4. Ambiguous function pairs (always decompile)

For this build, **`GetSpreadValues`** and **`GetSpreadAngles`** were once **swapped** in `reference-offsets.json` relative to vdumper’s Tier1 pattern hits. The JSON is corrected to match scan output:

- `GetSpreadValues` → `0x6F04280`
- `GetSpreadAngles` → `0x62DEAA0`

After each patch: confirm by disassembly (return shape / callers), not by name alone.

---

## 5. External vs internal “fluent” checklist

**External (kernel read, no `.text` execution)**

- [ ] Resolve **`GWorld`** (Tier1) on the dump PE.
- [ ] Walk **`UWorld` → … → `Pawn` / mesh`** using class **D** offsets validated on **this** build (IDA strings + live probe).
- [ ] Use **C** anchors (`PersistentLevel`, `GetCameraCachePOV`, …) to detect Epic skew early.

**Internal (in-process; policy / AC constraints aside)**

- [ ] Same Tier1 table for **hooks** (`ProcessEvent`, allocators, etc.).
- [ ] Prefer **`StaticFindObject`** when **`GObjects`** Tier2 fails.
- [ ] **`FNamePool` / FName** for logging and class filters when Tier2 succeeds.

---

## 6. Related paths (this repo)

| Artifact | Purpose |
|----------|---------|
| `../offsets/valorant-offsets-2026-04-26.txt` | Latest scan RVAs |
| `../runs/dump-run-2026-04-26.md` | Capture provenance |
| `reference-offsets.json` | Struct / gameplay reference (class D) |
| `reference-offsets-validation.txt` | Ingest sanity (duplicates / conflicts) |
| `DUMP_FROM_IDA.md` | Full IDA narrative + rounds 9–11 |
| `ida-mcp-synthesized.md` | Full MCP `find_regex` tables |
| `SDK_DIRECTORY_INDEX.md` | TOC for `docs/` + `offsets/` + `runs/` |
| *(private vdumper tree)* `src/research/valorant_automation.hpp` | Authoritative Tier1/Tier2 pattern source |
