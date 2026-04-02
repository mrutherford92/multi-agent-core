# 🟠 Cortex Handoff — "Apps" → "Tools" Rename (GitHub #36)

**From**: Bridge 🌉
**To**: Cortex 🟠
**Date**: 2026-03-14
**Priority**: MEDIUM
**Status**: ✅ COMPLETED — 2026-03-18. Display labels renamed, Firestore collection name kept as chatbot_apps.

---

## Context

The in-app tab previously "Apps" is renamed to **"Tools"**. Cortex owns the backend configs and admin tool pages that reference this section.

## What Cortex Needs To Do

### 1. Firestore Chatbot Config

The chatbot config for the Tools tab is currently named `chatbot_apps` in the `chatbot_configs` Firestore collection.

**Decision needed from Captain**: Rename to `chatbot_tools`?

If yes:
- [ ] Create new `chatbot_tools` document in `chatbot_configs` with same content as `chatbot_apps`
- [ ] Delete old `chatbot_apps` document (or keep as alias)
- [ ] Update `scripts/seed_chatbot_configs.py` — rename the `chatbot_apps` entry
- [ ] Coordinate with Nexus — they reference `configId: 'chatbot_apps'` in 2 places in `neuro_arts_directory_screen.dart`

If no (keep `chatbot_apps` internally):
- No action needed — internal config name doesn't have to match UI label

### 2. Admin Tool

- [ ] Check `pages/1_Chatbot_Config.py` — if it displays "Apps" anywhere in the config list or labels, rename to "Tools"
- [ ] Check `pages/4_Available_Models.py` — same scan for "Apps" references
- [ ] Any chatbot RAG content that references the "Apps tab" should say "Tools tab"

### 3. Cloud Functions

- [ ] Check `functions_chatbot/main.py` — the `chatbot_apps` config is referenced when processing recommendations. Internal only, but update comments if helpful.

---

## No Structural Changes

This is purely a terminology rename. No data models, schemas, or APIs change.
