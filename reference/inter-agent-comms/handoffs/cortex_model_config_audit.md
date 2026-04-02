# 🟠 Cortex Handoff — Chatbot Model Configuration Audit

**From**: Nexus 🔵
**To**: Cortex 🟠
**Date**: 2026-03-13
**Priority**: HIGH
**Status**: ✅ COMPLETED — 2026-03-18. Pages already had all collections. Apps→Tools rename done.

---

## Context

Captain ordered a full audit and fix of the chatbot AI model configuration. The 504 timeout errors in the Vocal Coach chatbot were caused by:

1. **Dead Firebase Data Connect code** in `functions_chatbot/main.py` causing a `NameError` on every request (fixed by Nexus)
2. **Slow model** — `gemini-3.1-pro-preview` and `gemini-2.0-flash` being used where `gemini-3.1-flash-preview` is needed (seed script updated by Nexus)

## What Nexus Did

- ✅ Removed dead FDC code from `functions_chatbot/main.py` (replaced with Firestore user profile fetch)
- ✅ Fixed hardcoded project_id placeholder (`"formatted-project-id"` → fail-fast ValueError)
- ✅ Updated `scripts/seed_chatbot_configs.py` — all 9 configs now default to `gemini-3.1-flash-preview`
- ✅ Updated admin tool `pages/1_Chatbot_Config.py` — expanded dropdown from 6 → 13 collections
- ✅ Updated admin tool `pages/4_Available_Models.py` — expanded model checker and Quick Update from 3 → 12 collections

## What Cortex Needs To Do

### 1. Verify Admin Tool Model Configuration Pages

Open the admin tool (`projects/admin-tool/`) and verify:

- [ ] **Page 1 (Chatbot Config)**: All 13 config collections appear in the dropdown
- [ ] **Page 4 (Available Models)**: All 12 collections appear in the "Config vs Available Models" section
- [ ] **Page 4 (Quick Model Update)**: All 12 collections appear in the feature dropdown
- [ ] **Page 4**: Click "Fetch Available Models" and verify `gemini-3.1-flash-preview` appears in the Gemini models list for `us-central1`

### 2. Update Firestore Model Names

The seed script has been updated but **Firestore has NOT been re-seeded yet**. Either:

- Run `python scripts/seed_chatbot_configs.py` from `projects/neuro-arts-flutter/`
- OR use the admin tool's "Quick Model Update" on Page 4 to update each config individually

**Target model for all configs**: `gemini-3.1-flash-preview`

### 3. Verify Model Availability

Use the admin tool's Available Models page to confirm that `gemini-3.1-flash-preview` is available in the `global` region (which is what most configs use for `vertex_ai_location`). If it's not available in `global`, check `us-central1`.

### 4. Report Back

Update your status file at `reference/inter-agent-comms/status/cortex.json` with findings.

---

## Files Changed by Nexus

| File | Change |
|------|--------|
| `functions_chatbot/main.py` | Removed dead FDC code, added Firestore user fetch, fixed project_id |
| `scripts/seed_chatbot_configs.py` | All models → `gemini-3.1-flash-preview` |
| `admin-tool/pages/1_Chatbot_Config.py` | Added 7 missing config collections |
| `admin-tool/pages/4_Available_Models.py` | Expanded model checker + Quick Update to all collections |
