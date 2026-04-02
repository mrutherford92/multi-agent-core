# 🟠 Cortex Handoff — Content Upload & Management

**From**: Bridge 🌉
**To**: Cortex 🟠
**Date**: 2026-03-13
**Priority**: MEDIUM
**Status**: STANDING INSTRUCTIONS

---

## Overview

All audio content assets have been consolidated under `content/` at the monorepo root. You now have two tools for managing content uploads to Firebase Storage:

1. **CLI Script**: `projects/admin-tool/scripts/upload_content.py`
2. **Admin UI**: Streamlit → Page 11 (Upload)

## Content Directory Structure

```
content/
├── exercises/          Pitch trainer (DO NOT MODIFY — use upload_exercises.sh)
├── music/              Audio library tracks
├── meditations/        Guided meditations
├── podcasts/           Podcast episodes
└── courses/            Program content (markdown, not audio)
```

Each audio subdirectory contains one track:
```
content/music/rain/
├── rain.mp3
└── rain.jpg          (optional cover art)
```

## Firebase Storage Path Convention

**Bucket**: `gs://vocalbrain-web.appspot.com`

Files are uploaded with paths mirroring the local structure:

| Local | Storage |
|-------|---------|
| `content/music/rain/rain.mp3` | `content/music/rain.mp3` |
| `content/meditations/aliveness/aliveness.mp3` | `content/meditations/aliveness.mp3` |
| `content/podcasts/cadence_s01_e01/cadence-s01-e01.mp3` | `content/podcasts/cadence-s01-e01.mp3` |

**Firestore Collection**: `anp_songs` — each track gets a document with `audioUrl` pointing to the Storage URL.

> ⚠️ **Legacy content** still lives under `songs/anp_songs/` in Storage. The `audioUrl` in existing Firestore docs still points there. New uploads go to `content/<category>/` paths.

## CLI Usage

```bash
cd projects/admin-tool

# Preview what would upload (no changes)
python scripts/upload_content.py --dry-run

# Upload all music
python scripts/upload_content.py --category music

# Replace a specific track
python scripts/upload_content.py --replace rain

# Upload to Storage only (no Firestore changes)
python scripts/upload_content.py --skip-firestore
```

## Adding New Content

1. Create a subdirectory under the appropriate category in `content/`:
   ```
   content/music/new_track_name/
   ```
2. Place the MP3 (and optional cover art) inside
3. Upload via CLI or admin UI
4. Verify in Firestore that the `anp_songs` document was created

## Standing Rules

- **Never upload placeholder files** — SO-003
- **Always log errors with context** — SO-003
- Track IDs use `snake_case` matching the directory name
- Cover art should be `.jpg` or `.png`, same name as the directory

## Dependencies

- `google-cloud-storage` (added to `pyproject.toml`)
- `firebase-admin` (already present)
- Credentials: `~/vocalbrain-adminsdk.json` or `GOOGLE_APPLICATION_CREDENTIALS`
