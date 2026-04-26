# IDA string anchors — curated (VALORANT-Win64-Shipping dump)

Absolute VAs use image base **`0x7ff686010000`** for the 2026-04-26 kernel PE dump session. Use **Jump → address** in IDA, then **xrefs** once auto-analysis completes. Full machine tables: [`ida-mcp-synthesized.md`](ida-mcp-synthesized.md).

## World / viewport / camera

| String | VA |
|--------|-----|
| `PersistentLevel` | `0x7ff69069eb80` |
| `OwningGameInstance` | `0x7ff690b55948` |
| `GetGameViewport` | `0x7ff690fa5cf0` |
| `GetCameraCachePOV` | `0x7ff690e8d7f0` |
| `CameraCachePrivate` | `0x7ff690b958a0` |

## Shooter / GAS / match

| String | VA |
|--------|-----|
| `ShooterGameState` | `0x7ff690f21150` |
| `GetShooterGameState` | `0x7ff691198600` |
| `AresAbilitySystemComponent` | `0x7ff6910971a8` |
| `AbilitySystemComponent.cpp` | `0x7ff690da84e0` |
| `MatchState` | `0x7ff690c58198` |
| `HandleSpikePlanted` | `0x7ff69115cd58` |

## Input / Slate

| String | VA |
|--------|-----|
| `EnhancedInputLibrary.cpp` | `0x7ff690de7c20` |
| `SlateApplication.cpp` | `0x7ff69071b1b0` |

## Net / replication helpers

| String | VA |
|--------|-----|
| `FastArraySerializer` | `0x7ff6907643e0` |
| `DemoNetDriver.cpp` | `0x7ff690c46160` |

## Zero-hit greps (try alternate strings next patch)

Examples: literal `ConstructObject`, `ReplicationGraph`, `KismetMathLibrary`, `FArchive` — see `ida-mcp-synthesized.md` empty sections and Round 4 notes in maintainer `DUMP_FROM_IDA.md` (private tree).
