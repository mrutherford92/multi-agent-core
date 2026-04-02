# 🔵→🟠 Nexus → Cortex Handoff: Coaching Feedback Integration Complete

**From**: Nexus (Experience Designer) | **To**: Cortex (Intelligence Officer)
**Date**: 2026-03-13 19:09 ET | **Priority**: INFORMATIONAL

---

## Summary

Nexus has completed all items from your handoff (`nexus_coaching_feedback_ux.md`). The Flutter app now reads, displays, and live-watches the 3 new fields you specified.

---

## What Flutter Now Reads

| Firestore Field | Dart Field | Type | Status |
|-----------------|------------|------|--------|
| `feedback_text` | `feedbackText` | `String?` | ✅ Parsed + displayed |
| `recommended_exercises` | `recommendedExercises` | `List<Map<String, dynamic>>` | ✅ Parsed + tappable |
| `analysis_error_message` | `analysisErrorMessage` | `String?` | ✅ Parsed + displayed |
| `analysis_status` | `analysisStatus` | `String?` | ✅ Already existed |

---

## Field Contracts — What Cortex Must Write

### `feedback_text`
- **Type**: String (nullable)
- **Content**: Warm, second-person coaching prose
- **When**: After AI generates or coach edits feedback
- **Flutter behavior**: Displayed in a gradient card with 🎓 icon

### `recommended_exercises`
```json
[
  {
    "firestoreId": "triad-low",     // REQUIRED — must match vocal_exercises doc ID
    "name": "Triad Low",            // REQUIRED — display name
    "reason": "Strengthens breath"  // OPTIONAL — shown as subtitle
  }
]
```
- **Flutter behavior**: Each exercise is a tappable chip → navigates to `ExercisePitchScreen(initialExerciseId: firestoreId, initialRange: range)`
- **Range detection**: Nexus infers range from the `firestoreId` — IDs ending in `-high` → `high`, everything else → `low`

### `analysis_status`
Must follow this exact lifecycle:
```
"pending" → "processing" → "complete" | "error"
```
- `pending` → Shows "Your coach will review this recording soon"
- `processing` → Shows animated progress bar + "AI analyzing..."
- `complete` → Shows feedback card (if `feedback_text` exists)
- `error` → Shows `analysis_error_message` with ⚠️ warning icon

### `analysis_error_message`
- **Type**: String (nullable)
- **When**: Only set when `analysis_status == "error"`
- **Content**: Human-readable error explanation

---

## Real-Time Updates

The Flutter app now uses a **Firestore snapshot listener** on the selected recording document. When Cortex writes any of these fields, the UI updates **instantly** without requiring the user to refresh or reselect.

---

## Exercise Deep-Linking Contract

`ExercisePitchScreen` now accepts `initialExerciseId`. This must match a document ID in the `vocal_exercises` Firestore collection. If the ID doesn't match any exercise, the screen falls back to the first exercise in the filtered range.

---

## Answers to Cortex's Questions

1. **Feedback as 4th tab or separate card?** → **Separate card** below the analysis gallery. Keeps the 3-tab gallery (Spectrogram/Piano Roll/Intonation) focused on visual data.
2. **Deep-linkable exercises?** → **Yes.** Tapping navigates to `ExercisePitchScreen` with that exercise pre-selected.
3. **Notification badge?** → **Not yet implemented.** Will add in a future pass once we confirm the pipeline is producing data.

---

## Files Modified by Nexus

| File | What Changed |
|------|-------------|
| `recording_model.dart` | +3 fields, `copyWith()` |
| `recording_repository.dart` | `watchRecording()` snapshot stream |
| `recording_player_view_model.dart` | `_startWatchingRecording()`, wired to select/play |
| `recording_playback_screen.dart` | Integrated `CoachingFeedbackCard` |
| `exercise_pitch_screen.dart` | `initialExerciseId` parameter |
| **NEW** `coaching_feedback_card.dart` | Full feedback card widget |
