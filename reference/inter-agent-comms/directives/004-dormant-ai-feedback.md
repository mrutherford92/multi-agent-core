# ⚠️ Standing Order 004: AI Coaching Feedback DORMANT

**From Captain Michael via Bridge — 2026-03-13 19:28 ET**
**Status: ACTIVE — applies until further notice**

---

## Order

The AI spectrogram-based coaching feedback pipeline is **DORMANT**.
Coaching feedback will come from **HITL (Human-in-the-Loop)** review via the admin tool, not from automated Gemini analysis.

## What's Disabled

| Component | File | Status |
|-----------|------|--------|
| Gemini feedback generation | `watcher.py` step 6 | Commented out |
| `CoachingFeedbackCard` widget | `coaching_feedback_card.dart` | DORMANT header added |
| Card usage in recording screen | `recording_playback_screen.dart` | Commented out |
| Import statement | `recording_playback_screen.dart:17` | Commented out |

## What Remains Active

- ✅ Spectrogram generation (step 3)
- ✅ ML classifier / tags (step 4)
- ✅ Pitch analysis — notes, contours, cents (step 5)
- ✅ All three analysis tabs in Flutter UI (Spectrogram, Piano Roll, Intonation)
- ✅ Admin Recording Feedback page (`10_Recording_Feedback.py`) for HITL workflow

## Agent-Specific Orders

### Cortex
- **DO NOT** re-enable Gemini feedback in `watcher.py`
- **DO NOT** write `feedback_text` or `recommended_exercises` to Firestore from the automated pipeline
- **DO** continue running spectrogram, classifier, and pitch analysis as normal
- **DO** keep the admin Recording Feedback page functional for manual HITL coaching
- `gemini_feedback.py` code is preserved for future use — do not delete

### Nexus
- **DO NOT** re-enable `CoachingFeedbackCard` in the recordings UI
- **DO NOT** reference `feedbackText` or `recommendedExercises` in any new UI work
- **DO** keep the `coaching_feedback_card.dart` widget file intact (dormant)
- **DO** keep the model fields (`feedbackText`, `recommendedExercises`) in `RecordingModel` for future HITL data display
- Focus on pure analytics display: spectrogram, piano roll, intonation views

## Rationale

The AI-generated coaching feedback from spectrogram analysis produced unreliable, generic text. Real coaching requires human expertise. The HITL workflow through the admin tool allows coaches to review analytics and write personalized feedback.
