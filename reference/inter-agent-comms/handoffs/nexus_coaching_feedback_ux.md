# 🧠→🔵 Cortex → Nexus Handoff: Coaching Feedback UX

**From**: Cortex (Intelligence Officer) | **To**: Nexus (Experience Designer)
**Date**: 2026-03-13 | **Priority**: HIGH

---

## Situation

Cortex has built the **admin-side analysis pipeline** — coaches can now review student recordings, trigger AI analysis (spectrogram → classifier → Gemini feedback), edit tags, and write coaching notes. All results are written to Firestore.

**The problem**: The Flutter app can *display* spectrograms, piano rolls, and intonation charts, but **cannot display the coaching feedback or exercise recommendations** that Cortex generates. These fields (`feedback_text`, `recommended_exercises`) are **not yet consumed** by the mobile app.

---

## What Cortex Writes to Firestore

Every recording document in the `recordings` collection gets these fields populated by the analysis pipeline:

| Field | Type | Source | Flutter Status |
|-------|------|--------|----------------|
| `analysis_status` | `String` | Pipeline | ✅ Read by `RecordingModel` |
| `analysisImageUrls.spectrogram_png.public_url` | `String` | Spectrogram gen | ✅ Read by `AnalysisGalleryWidget` |
| `spectrogramStoragePath` | `String` | Spectrogram gen | ✅ Read by `RecordingModel` |
| `tags` | `List<String>` | Classifier + coach | ✅ Read & displayed as chips |
| `feedback_text` | `String` | Gemini AI + coach edit | ❌ **NOT in RecordingModel** |
| `recommended_exercises` | `List<Map>` | Gemini AI | ❌ **NOT in RecordingModel** |
| `analysis_error_message` | `String?` | Pipeline errors | ❌ **NOT in RecordingModel** |

### `recommended_exercises` shape
```json
[
  {
    "firestoreId": "triad-low",
    "name": "Triad Low",
    "reason": "Strengthens your breath support in the lower register"
  }
]
```

---

## What Nexus Needs to Build

### 1. Add Missing Fields to `RecordingModel`

File: `lib/features/recording_playback/models/recording_model.dart`

Add these fields:
```dart
final String? feedbackText;           // ← "feedback_text"
final List<Map<String, dynamic>> recommendedExercises;  // ← "recommended_exercises"
final String? analysisErrorMessage;   // ← "analysis_error_message"
```

And read them in `fromSnapshot`:
```dart
feedbackText: data['feedback_text'] as String?,
recommendedExercises: List<Map<String, dynamic>>.from(data['recommended_exercises'] ?? []),
analysisErrorMessage: data['analysis_error_message'] as String?,
```

---

### 2. Build Coaching Feedback Card

Below the `AnalysisGalleryWidget` (spectrogram/piano roll/intonation), add a **Coaching Feedback Card** that shows:

- **🎯 Feedback text** — warm, second-person coaching prose from Gemini (or manually written by coach)
- **📚 Recommended Exercises** — tappable list that navigates to each exercise
- **⏳ Status indicator** — "Waiting for coach review" if `analysis_status == 'pending'`

**IMPORTANT**: `feedback_text` may be `null` even when `analysis_status == 'complete'` — the spectrogram and tags can exist without feedback. Show "Awaiting coach feedback" in this case — **do NOT show placeholder text** (SO-003).

#### Suggested widget location in `recording_playback_screen.dart`:
After the track info section (line ~340), before the seek bar, or as an expandable card below the list.

---

### 3. Make Recommended Exercises Tappable

Each recommended exercise has a `firestoreId` mapping to the `vocal_exercises` collection. Tapping should navigate to: `ExercisePitchScreen` with that exercise loaded.

---

### 4. Real-Time Status Updates

The app currently fetches recordings once. For the coaching loop to feel alive:
- Listen for Firestore snapshot updates on the selected recording doc
- When `analysis_status` transitions from `pending` → `processing` → `complete`, the UI should auto-update (no manual refresh)
- When `feedback_text` appears, show a subtle "New feedback!" indicator

---

### 5. Polish Suggestions

- **Feedback card design**: Match the warm coaching tone — use a gradient card with an avatar/icon, not raw text
- **Tag display on list items**: Already working ✅ but consider color-coding pedagogical tags (e.g., green for `Clear`, `Resonant`; amber for `Pitchy`, `Shaky`)
- **Empty state**: If a recording has `analysis_status: 'pending'`, show an animated "Analyzing..." state with a calming message

---

## Existing Code Reference

These Flutter files are already solid and ready to extend:

| File | What's There | What Nexus Adds |
|------|-------------|-----------------|
| `recording_model.dart` | 14 fields parsed | +3 fields (feedback, recs, error) |
| `analysis_gallery_widget.dart` | 3-tab gallery (Spectrogram, Piano Roll, Intonation) | — (complete as-is) |
| `tagging_dialog.dart` | 14 pedagogical tags with FilterChip | — (complete as-is) |
| `recording_repository.dart` | CRUD + tag update | Consider snapshot listener |
| `recording_playback_screen.dart` | Full playback + gallery + list | +Coaching feedback card |

---

## Cortex's Commitments

I will ensure these fields are always populated correctly:

1. **`feedback_text`** — Gemini-generated or coach-edited, warm second-person prose, ≤200 words
2. **`recommended_exercises`** — 2-3 exercises with valid `firestoreId` matching `vocal_exercises` collection
3. **`tags`** — ML classifier labels + coach manual tags, from the standard 14-tag vocabulary
4. **`analysis_status`** — Always transitions: `pending` → `processing` → `complete` | `error`
5. **`analysis_error_message`** — Only set when `analysis_status == 'error'`, human-readable

---

## Questions for Nexus

1. Should the coaching feedback appear as a **4th tab** in `AnalysisGalleryWidget`, or as a **separate card** below the gallery?
2. Should recommended exercises be **deep-linkable** (tap → navigate to exercise screen)?
3. Do you want a **notification badge** on the Recordings list when new feedback arrives?
