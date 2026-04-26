# VALORANT dump → external / internal reference (IDA MCP extraction)

> **Copy in this repo:** Paths like `research/ida-mcp/` refer to the maintainer’s vdumper workspace, not to folders on GitHub. For links that work **here**, use [`SDK_DIRECTORY_INDEX.md`](SDK_DIRECTORY_INDEX.md) and the `docs/` artifacts beside this file.

This document merges **automated IDA Pro MCP** pulls from `VALORANT-Win64-Shipping_Dump_fresh.exe` with **sig dump** data and **live ESP** notes. Use it to maximize what you can take from the **offline PE** without running the game.

**Regenerate MCP JSON:** run `research\ida-mcp\run_all.bat` (IDA MCP must listen on `http://127.0.0.1:13337/mcp` with the dump IDB open). Raw responses: `research/ida-mcp/out_*.json`.

---

## 1. Binary identity (survey_binary + health)

| Field | Value |
|--------|--------|
| **Image base** | `0x7ff686010000` |
| **Size of image** | `0xCF82000` |
| **MD5** | `f28c3d3d6c5361c7c9ac3d74a85670bc` |
| **SHA256** | `e038bf5a6e84d35454f5cdecfa87fdbb844fb644b2e6663dc23b6659271754af` |
| **IDB** | `VALORANT-DUMPER/output/dumps/VALORANT-Win64-Shipping_Dump_fresh.exe.i64` |
| **Strings (indexed)** | ~306733 |
| **Named functions** (snapshot) | ~611 (auto-analysis still indexing more) |
| **`.text`** | `0x7ff686011000` – `0x7ff68f360000` (rx) |
| **`.rdata`** | `0x7ff68f361000` – `0x7ff691e9f000` (r) — **reflection / FName / property names** |
| **`.data` / `.pdata`** | standard PE layout |

**`auto_analysis_ready`:** often **false** while IDA chews a 200MB+ game — string search still works; **xrefs** get richer when analysis finishes.

---

## 2. Image-relative RVAs (sig scan — same numeric as runtime `module_base + RVA`)

Copied from `VALORANT-DUMPER/output/sdk-offsets/valorant-offsets-2026-04-26.txt` for this build:

| RVA | Purpose |
|-----|---------|
| `0xC1AD2A0` | `GWorld` |
| `0xC34B800` | `FNamePool` |
| `0x40EBC10` | `BoneMatrix` |
| `0x1B74230` | `ProcessEvent` (UObject dispatch — **internal** hook target; **not** a plain string in dump) |
| `0x1BA05C0` | `StaticFindObject` |
| `0x1BA40F0` | `StaticLoadObject` |
| `0x1747C10` | `FMemoryMalloc` |
| `0x177F496` | `TriggerVeh` |
| `0x407F040` | `SetOutlineMode` |
| `0x6F04280` | `GetSpreadValues` |
| `0x62DEAA0` | `GetSpreadAngles` |
| `0x6AA7A30` | `GetFiringLocationAndDirection` |
| `0x1847290` | `ToVectorAndNormalize` |
| `0x1841A90` | `ToAngleAndNormalize` |
| `0x62424D0` | `PlayFinisher` |

**Code:** see `src/sdk/offsets.hpp` → `off::SigRva` (mirrors this table for C++).

---

## 3. `.rdata` string anchors (VA = `0x7ff686010000` + file offset into mapped image)

Use these in IDA: **Jump to address** → **Xrefs** → decompile. VAs below are **absolute** for this dump session.

### World / net / viewport

| String | VA |
|--------|-----|
| `UWorld::InitializeActorsForPlay` | `0x7ff690d66118` |
| `PersistentLevel` | `0x7ff69069eb80` |
| `OwningGameInstance` | `0x7ff690b55948` |
| `GameNetDriver` | `0x7ff69069ede8` |
| `PendingNetDriver` | `0x7ff69069edd0` |
| `BeaconNetDriver` | `0x7ff69069edc0` |
| `ActiveNetDrivers` | `0x7ff690b55930` |
| `GameViewport` | `0x7ff690b55960` |
| `GetGameViewport` | `0x7ff690fa5cf0` |
| `GameViewportClient.cpp` path | `0x7ff690c68ff0` |

### Camera / view

| String | VA |
|--------|-----|
| `MinimalViewInfo` | `0x7ff690b52b30` |
| `CameraCachePrivate` | `0x7ff690b958a0` |
| `LastFrameCameraCachePrivate` | `0x7ff690b95880` |
| `GetCameraCachePOV` | `0x7ff690e8d7f0` |
| `GetLastFrameCameraCachePOV` | `0x7ff690e8d780` |
| `GetPlayerCameraManager` | `0x7ff690c5a300` |
| `PlayerCameraManager` | `0x7ff690cfb148` |
| `ViewTarget` | `0x7ff690b95870` |
| `ControlRotation` | `0x7ff690c35a98` |

### Pawn / Shooter / component transform

| String | VA |
|--------|-----|
| `AcknowledgedPawn` | `0x7ff690cfb168` |
| `ShooterCharacter` | `0x7ff690f186c8` |
| `GetShooterCharacter` | `0x7ff690f66f00` |
| `OwningShooterCharacter` | `0x7ff690f0a328` |
| `K2_GetComponentToWorld` | `0x7ff690ba9c30` |
| `bComponentToWorldUpdated` | `0x7ff690ba9f40` |

### Damage / Ares gameplay

| String | VA |
|--------|-----|
| `DamageableComponent.cpp` path | `0x7ff6912604f0` |
| `OwnerDamageableComponent` | `0x7ff69100fef8` |
| `bDamageableComponentAlive` | `0x7ff690f68058` |

### Local player / actors (subset — full tables in older research note)

| String | VA |
|--------|-----|
| `LocalPlayers` | `0x7ff690c58af8` |
| `ActorArray` | `0x7ff690da3040` |
| `SkeletalMeshComponent` | `0x7ff690be8638` |

---

## 4. What IDA **cannot** guarantee from strings alone

| Gap | Mitigation |
|-----|------------|
| **`UWorld::PersistentLevel` member offset** | Live read + pointer sanity (your `0x100` session) or xref from engine init |
| **`ProcessEvent` name stripped** | Use sig RVA `0x1B74230` + pattern re-scan on patch |
| **`FNamePool` / GObjects** | `FNamePool` RVA known; full `GObjects` was **missing** in sig run — use `StaticFindObject` / world walk |
| **Internal stability** | Vanguard blocks in-process execution — treat internal offsets as **research** unless you have a separate bypass story |

---

## 5. External ESP (`vesp`) — how this dump backs the code

| System | Dump backing |
|--------|----------------|
| Module base + `GWorld` | Sig RVA + IDA confirms UE strings exist |
| `PersistentLevel` / `Actors` / `GameInstance` | Live offsets + `PersistentLevel` / `OwningGameInstance` / `ActorArray` strings |
| Camera | `GetCameraCachePOV` / `CameraCachePrivate` strings + community `0x520` / `0x20A0` + **runtime POV decode** in `dllmain.cpp` |
| Position | `K2_GetComponentToWorld` + `ShooterCharacter` strings + live `+0x308` bot FVector |
| Bones | `BoneMatrix` RVA + `SkeletalMeshComponent` string (mesh layout still needs live or SDK) |

---

## 6. Internal (future) — minimal hook graph from dump

1. **`GWorld`** → `PersistentLevel` → `Actors` → filter by **`ShooterCharacter`** / vtable (string `ShooterCharacter` for reflection, not RTTI).  
2. **`ProcessEvent`** at `image + 0x1B74230` — only if your loader can run without VAN.  
3. **`StaticFindObject`** / **`StaticLoadObject`** — resolve `UClass` / `UFunction` without full `GObjects`.  
4. **`FNamePool`** — names for debug / class filter (`FName::ToString` sig was **missing** in dumper run — re-scan on patch).

---

## 7. Related files in this repo

| File | Role |
|------|------|
| `IDA_EXTERNAL_BACKING.md` | Narrative + workflow |
| `src/sdk/offsets.hpp` | **C++ constants**: world chain + `SigRva` block |
| `src/dllmain.cpp` | External implementation |
| `VALORANT-DUMPER/output/research/ida-mcp-research-2026-04-26.md` | Earlier exhaustive string tables |
| `VALORANT-DUMPER/output/sdk-offsets/SIG_RESEARCH_MATRIX.md` | **Sigs vs struct offsets vs IDA** — what is safe for external vs internal |
| `VALORANT-DUMPER/output/sdk-offsets/SDK_DIRECTORY_INDEX.md` | **Master TOC** for sdk-offsets + links to MCP / dumper / example `offsets.hpp` |
| `research/ida-mcp/ida-mcp-synthesized.md` | All `find_regex` hits (auto table) |
| `research/ida-mcp/run_round3.bat` | Round-3 MCP batch only (fast refresh) |
| `research/ida-mcp/NOTE_WHILE_ANALYZING.md` | String pulls vs xref timing |

---

## 8. MCP queries that returned **no** plain ASCII hit (patch / strip)

- `ProcessEvent` (literal)  
- `FNamePool` (literal)  
- `BoneArray` (literal)  
- `StaticFindObject` (literal)  
- `_PC_C` glob (too specific for regex engine)

Use **sig RVAs** or **wider** patterns / **xref from known** `Engine.*` cpp paths instead.

---

## 9. Research round 2 — expanded `find_regex` batch (2026-04-26)

**Full tables (all patterns, all hits per query):** [`research/ida-mcp/ida-mcp-synthesized.md`](research/ida-mcp/ida-mcp-synthesized.md) — regenerated by `python research/ida-mcp/summarize_out.py research/ida-mcp/ida-mcp-synthesized.md` after `run_all.bat`.

**New query files** (same folder as other `q_find_*.json`): `uobject`, `uclass`, `uengine`, `replicated`, `bonename`, `drawhud`, `canvas`, `hitresult`, `char_move`, `capsule`, `equippable`, `gameplay_ability`, `attribute_set`, `outline`, `level_stream`, `primitive`, `pawn`, `controller`, `bounds`, `transform`, `linetrace`, `spawn_actor`, `widget`, `playerstate`, `teamid`, `net_dormant`, `static_mesh`, `instanced`, `batched`, `game_viewport`.

### 9.1 Curated anchors (xref starting points)

| Topic | String | VA |
|--------|--------|-----|
| **CoreUObject** | `C:\fbroot\Engine\Source\Runtime\CoreUObject\Private\UObject\Class.cpp` | `0x7ff6906bfed0` |
| **Async load** | `AsyncLoading2.cpp` | `0x7ff6906bbba0` |
| **GAS attributes** | `AttributeSet.cpp` (plugin path) | `0x7ff690daacd0` |
| **GAS specs** | `GameplayAbilitySpec` | `0x7ff690d9c220` |
| **Character move** | `CharacterMovementComponent.cpp` | `0x7ff690c13770` |
| **Shooter move** | `ShooterCharacterMovement.cpp` | `0x7ff69130bf70` |
| **Shooter move API** | `GetShooterCharacterMovement` | `0x7ff6911a3778` |
| **Weapons** | `GetEquippable` | `0x7ff690f098a0` |
| **Weapons** | `Equippable` | `0x7ff690f179f0` |
| **Trace** | `LineTraceSingle` | `0x7ff690c87bd0` |
| **Trace** | `K2_LineTraceComponent` | `0x7ff690b97358` |
| **HUD hook (internal)** | `ReceiveDrawHUD` | `0x7ff690c738f0` |
| **Bones** | `GetBoneName` | `0x7ff690babff8` |
| **Replication** | (see `q_find_replicated` in synthesized file — many property names) | — |
| **Outline / UI** | `OutlineMaterial` | `0x7ff690701db0` |
| **Draw batching** | `BatchedElements.cpp` | `0x7ff690bf8020` |
| **Sig alignment** | `SetOutlineMode` is **code** at RVA `0x407F040` (§2); string hits here are mostly **font/Slate** outline — do not conflate. |

### 9.2 Empty or sparse patterns (try alternate spellings next round)

| Query | Result |
|--------|--------|
| `q_find_canvas` | **0** hits (`FCanvas` not stored as that substring — use `BatchedElements.cpp` @ `0x7ff690bf8020` or search `Canvas` without `F` prefix) |
| `q_find_game_viewport` | **0** for `UGameViewportClient` — strings use `GameViewport` / path `GameViewportClient.cpp` (see §3) |
| `q_find_capsule` | **1** hit (`CapsuleComponent` only — widen with `CapsuleHalfHeight`, `ShapeColor`) |
| `q_find_mesh` (round 1) | **0** for `BoneArray` — keep using **`BoneMatrix` RVA** + bone name strings above |

### 9.3 Workflow

1. Run `research\ida-mcp\run_all.bat` whenever the IDB is updated (or `run_round3.bat` for the latest batch only).  
2. Run `summarize_out.py` to refresh `ida-mcp-synthesized.md`.  
3. Pick strings **in `.rdata`**, jump to VA, **xrefs → decompile** once `auto_analysis_ready` is true (see `out_q_health.json`).

**While IDA is still analyzing:** string MCP pulls remain valid — see `research/ida-mcp/NOTE_WHILE_ANALYZING.md`.

---

## 10. Research round 3 (IDA still analyzing — string-only pull)

Captured with `auto_analysis_ready: false`; all VAs below are **`.rdata` / reflection strings** (good for xref later, not code sigs).

### 10.1 GAS / Ares gameplay

| String | VA |
|--------|-----|
| `AresAbilitySystemComponent` | `0x7ff6910971a8` |
| `AbilitySystemComponent.cpp` (plugin path) | `0x7ff690da84e0` |
| `GetAbilitySystemComponent` | `0x7ff690da2f40` |
| `K2_ApplyGameplayEffectSpecToTarget` | `0x7ff690d9c490` |

### 10.2 Animation / mesh

| String | VA |
|--------|-----|
| `AnimInstance.cpp` | `0x7ff690bd1de0` |
| `SkinnedMeshComponent.cpp` | `0x7ff690c25390` |
| `GetAnimInstance` | `0x7ff690ae2478` |

### 10.3 Replication / net / Iris

| String | VA |
|--------|-----|
| `FastArraySerializer` | `0x7ff6907643e0` |
| `IrisFastArraySerializer` | `0x7ff6908e1c30` |
| `ActorChannelPool` | `0x7ff690cc8fa8` |
| `DemoNetDriver.cpp` | `0x7ff690c46160` |
| `GetDemoNetDriver` | `0x7ff69115ce08` |

### 10.4 Modes / spike / replay

| String | VA |
|--------|-----|
| `HandleSpikePlanted` | `0x7ff69115cd58` |
| `HandleSpikeDefused` | `0x7ff69115cd28` |
| `HandleSpikeExploded` | `0x7ff69115cd70` |
| `HasSpike` | `0x7ff691075490` |
| `EShooterGameMode::SpikeMode5v5` | `0x7ff691075760` |
| `ReplaySubsystem.cpp` | `0x7ff690d187c0` |

### 10.5 World / navigation / online

| String | VA |
|--------|-----|
| `WorldPartition` | `0x7ff690bbba00` |
| `NavigationSystemBase.h` | `0x7ff690bcb230` |
| `OnlineSubsystem.cpp` | `0x7ff690dc6480` |
| `GetGameInstanceSubsystem` | `0x7ff690d465a8` |

### 10.6 Actor lifecycle / rendering helpers

| String | VA |
|--------|-----|
| `ReceiveBeginPlay` | `0x7ff690bc7368` |
| `ReceiveTick` | `0x7ff690bc7338` |
| `GetGlobalPostProcessVolume` | `0x7ff690f43918` |
| `MaterialInstanceDynamic` | `0x7ff690c1b4f0` |
| `NiagaraSystem` | `0x7ff690db5538` |
| `TimerManager.cpp` | `0x7ff690d506c0` |

### 10.7 Round 3 queries with **no** ASCII hit (try later / alt spellings)

| Query | Suggested next pattern |
|--------|-------------------------|
| `ConstructObject` | `StaticConstructObject`, `NewObject` |
| `FObjectProperty` | `ObjectProperty`, `FField` |
| `SlateRenderer` | `FSlateApplication`, `DrawWindow` |
| `FRHICommand` | `FRHICommandList`, `RHICommandList` |
| `RoundBased` | `RoundState`, `MatchState`, `ShooterGameState` |
| `q_find_round` | Same row — no `RoundBased` substring in this build’s indexed strings |

Full machine tables for every round (including zeros): `research/ida-mcp/ida-mcp-synthesized.md`.

---

## 11. Research round 4 — SDK surfaces (game flow, input, objects, damage, Shooter paths)

**Batch:** `research/ida-mcp/run_round4.bat` (also folded into `run_all.bat`).

### 11.1 Game state / Shooter / Ares

| String | VA |
|--------|-----|
| `GameStateBase` | `0x7ff690f04698` |
| `ShooterGameState` | `0x7ff690f21150` |
| `ShooterGameState.cpp` | `0x7ff69128c950` |
| `GetShooterGameState` | `0x7ff691198600` |
| `OwningShooterGameState` | `0x7ff6910b9d20` |
| `AresGameInstance.cpp` | `0x7ff6912724f0` |

### 11.2 Match flow

| String | VA |
|--------|-----|
| `MatchState` | `0x7ff690c58198` |
| `GetMatchState` | `0x7ff690c580f8` |
| `AresBaseGameMatchState` | `0x7ff690fb2748` |
| `AresBombGameMatchState` | `0x7ff690fbce90` |
| `GetCurrentMatchState` | `0x7ff690ff74c8` |

### 11.3 Enhanced Input

| String | VA |
|--------|-----|
| `/Script/EnhancedInput` | `0x7ff690de61a0` |
| `EnhancedInputLibrary.cpp` | `0x7ff690de7c20` |
| `EnhancedPlayerInput.cpp` | `0x7ff690dec940` |

### 11.4 Slate application

| String | VA |
|--------|-----|
| `SlateApplication.cpp` | `0x7ff69071b1b0` |
| `FSlateApplication::Create()` | `0x7ff690d89f50` |

### 11.5 Object graph / soft refs

| String | VA |
|--------|-----|
| `NewObject` | `0x7ff69101d590` |
| `SoftObjectPath` | (see synthesized `q_find_soft_obj` — multiple engine paths) |
| `LoadStreamLevelBySoftObjectPtr` | `0x7ff690c5a558` |

### 11.6 Damage / cameras / components (subset)

| String | VA |
|--------|-----|
| `ApplyRadialDamage` | `0x7ff690c5a6f8` |
| `AresApplyRadialDamageWithFalloff` | `0x7ff691197d60` |
| `GameModeBase.cpp` | `0x7ff690c59650` |

### 11.7 ShooterGame source tree (for xref file gravity)

`q_find_shooter_game` returns many `C:\fbroot\ShooterGame\...` paths (e.g. AimTooling, DynamicVolume). Use them to **jump to string → xref** when finding Ares-specific types not present in generic UE docs.

### 11.8 Round 4 zero-hit / sparse (next patterns)

| Query | Note |
|--------|------|
| `StaticConstructObject` | 0 hits — try `StaticConstructObject_Internal`, `NewObject` callers only |
| `ReplicationGraph` | 0 — try `NetReplication`, `ReplicationDriver` |
| `IrisReplication` | 0 — try `Iris`, `DataStream` |
| `KismetMathLibrary` | 0 — try `KismetStringLibrary`, `UKismetSystemLibrary` |
| `FArchive` | 0 — try `FMemoryReader`, `FBufferArchive` |
| `TObjectPtr` | Hits are **SoftObjectPtr** helpers, not the template name — search `ObjectPtr` / `IsValid` paths separately |

### 11.9 SDK directory hub (dumper repo)

All offset artifacts + how they combine with this IDA work:  
[`VALORANT-DUMPER/output/sdk-offsets/SDK_DIRECTORY_INDEX.md`](../VALORANT-DUMPER/output/sdk-offsets/SDK_DIRECTORY_INDEX.md)
