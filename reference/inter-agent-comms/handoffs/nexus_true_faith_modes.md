# 🔵 Nexus Handoff — True Faith Mode Selector

**From**: Bridge 🌉
**To**: Nexus 🔵
**Date**: 2026-03-14
**Priority**: HIGH
**Status**: AWAITING PICKUP

---

## Task

Add a **mode selector** to the True Faith tool (`lib/features/music_therapy/views/true_faith_screen.dart`). The current behavior becomes "Advanced" mode. A new "Basic" mode provides a simplified, single-image experience.

## Mode Definitions

### 🟢 Basic Mode
- **One random image** is selected from `_availableCards` at session start
- Image is scanned (revealed strip-by-strip) — same visual mechanic as now
- When the image **de-scans** (erases), the session **ends immediately**
- After de-scan: show an **empty dark screen** with no image — this represents "empty mind"
- Hold the empty screen for ~5 seconds with a soft prompt like *"What remains?"* then transition to the completion screen
- **No cycling** — one image, one pass, done
- Ideal for beginners or quick sessions

### 🔴 Advanced Mode (current behavior)
- Multiple images cycle through during the session
- Timer-based duration (Fibonacci selector)
- Images cycle continuously until timer expires
- This is exactly how it works today — **no changes needed**

## UI: Mode Selector

Add a selector on the **start screen** (the pre-session config screen), above or below the duration selector.

**Suggested UI**: A segmented control / toggle with two options:

```
[ Basic ]  [ Advanced ]
```

- Style it to match the existing duration dropdown aesthetic (dark, subtle border, lavender accent)
- Default to **Basic** for new users
- Persist the selection in `SharedPreferences` (key: `true_faith_mode`) so it remembers

## Implementation Notes

### Key code locations

| What | Where |
|------|-------|
| Image loading | `_loadAssetManifest()` — line 135. Probes `card_0` to `card_21` |
| Cycling logic | `_cycleToNextCard()` — line 152. Increments `_currentCardIndex` |
| Session start | `_startSession()` — line 255. Starts timer + animation |
| Scan animation | `_scanController` — drives the strip-by-strip reveal/erase |
| Completion | `_completeSession()` — line 304. Stops everything |

### Basic Mode changes

1. In `_startSession()`, if Basic mode:
   - Pick a random card: `_currentCardIndex = Random().nextInt(_availableCards.length)`
   - Load that single image
   - Set `_scanController.duration` to a fixed duration (e.g., 2–3 minutes for one full build+hold+erase cycle)
   - When `_scanController` completes (status == `AnimationStatus.completed`), do NOT call `_cycleToNextCard()` — instead, show the empty mind screen

2. The "empty mind" screen:
   - Blank dark background (same as base gradient, no image)
   - Optional faint text: *"Empty mind..."* or *"What remains?"*
   - Hold for ~5 seconds, then call `_completeSession()`

3. Duration selector: **hide** the Fibonacci duration dropdown when Basic mode is selected (it's a single-pass experience — the duration is determined by the scan speed)

### State variable

Add: `String _selectedMode = 'basic';` (or use an enum)

## Do NOT Change

- Advanced mode behavior — leave it exactly as-is
- Image file paths or naming convention
- Audio/song selection — works the same in both modes
- The scanning visual mechanic itself — same in both modes
