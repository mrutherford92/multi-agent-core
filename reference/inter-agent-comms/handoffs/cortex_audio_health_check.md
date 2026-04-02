# 🟠 Cortex Handoff — Audio Format Health Check Integration

**From**: Bridge 🌉
**To**: Cortex 🟠
**Date**: 2026-03-14
**Priority**: HIGH
**Status**: AWAITING PICKUP

---

## Context

We discovered a critical audio playback bug: the iOS `record` plugin saves **WAV (PCM) data** with an **`.m4a` extension**. When `just_audio` hands this to iOS AVFoundation, it reads the extension, expects AAC, finds WAV data → **error -11829 "Cannot Open"**.

### Root Cause Evidence

```bash
$ file test_recording.m4a
RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 44100 Hz
```

Every single recording in the system had this same mismatch.

### Client-Side Fix (Bridge/Nexus)

`recording_player_view_model.dart` now detects RIFF magic bytes in downloaded data and saves cached files with `.wav` extension instead of `.m4a`.

## What Bridge Built

### 1. CLI Script: `scripts/audio_health_check.py`

```bash
cd projects/admin-tool
uv run python scripts/audio_health_check.py              # Scan all recordings
uv run python scripts/audio_health_check.py --fix        # Scan AND auto-fix
uv run python scripts/audio_health_check.py --user UID   # Scan specific user
uv run python scripts/audio_health_check.py --verbose    # Show healthy too
```

What it does:
- Queries all recordings from Firestore
- Downloads first 16 bytes of each file from Storage (magic bytes)
- Detects actual audio format vs filename extension
- Reports mismatches, missing files, empty files
- `--fix` mode: re-uploads with correct extension and updates Firestore

### 2. Streamlit Page: `pages/12_Audio_Health.py`

Dashboard UI for the same scan. Shows:
- Summary metrics (healthy, mismatched, missing, empty)
- Problem table with recording ID, exercise, user, issue type
- Filters by user ID and scan limit

## What Cortex Needs To Do

### 1. Review and Test the CLI

- [ ] Run `uv run python scripts/audio_health_check.py` from `projects/admin-tool/`
- [ ] Verify it detects the WAV-as-.m4a mismatches
- [ ] Run with `--fix` to correct existing recordings in Storage
- [ ] Verify fixed files play correctly

### 2. Consider Recording Pipeline Fix

The root cause is in the **recording upload pipeline**. When the app records and uploads:
- The `record` plugin on iOS records as WAV
- The upload path uses `.m4a` extension

Cortex should investigate:
- [ ] Can the recording config be changed to actually record AAC (true .m4a)?
- [ ] Or should the upload pipeline detect format and use correct extension?
- [ ] Consider adding format validation to the Cloud Function that processes uploads

### 3. Add to CI/Health Monitoring

- [ ] Consider scheduling the health check as a periodic Cloud Function or GitHub Action
- [ ] Add format validation to any content upload pipeline (content songs too)

### 4. Test the Streamlit Page

- [ ] Run the admin tool: `cd projects/admin-tool && uv run streamlit run app.py`
- [ ] Navigate to "Audio Health" page
- [ ] Verify the scan works and results are correct

---

## Files Created by Bridge

| File | Purpose |
|------|---------|
| `admin-tool/scripts/audio_health_check.py` | CLI health check scanner |
| `admin-tool/pages/12_Audio_Health.py` | Streamlit dashboard page |
| `recording_player_view_model.dart` | Client-side magic bytes fix (lines 602-622) |
