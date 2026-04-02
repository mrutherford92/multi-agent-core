# Handoff: Script Location Check — RESOLVED

**From**: Bridge
**Date**: 2026-03-18
**Priority**: 🟢 Resolved by Cortex

---

## Answer

**Yes — Cortex reorganized the entire `scripts/` directory this session.**

### New Layout

```
scripts/
├── launch/
│   └── start.sh                    # Launch admin console (chmod +x)
├── utils/                          # Reusable CLI tools
│   ├── add_testers_to_group.py     # ← MOVED HERE (was scripts/)
│   ├── upload_content.py           # ← MOVED HERE
│   ├── audio_health_check.py       # ← MOVED HERE
│   └── send_email.py               # ← MOVED HERE
└── archive/                        # One-off scripts (historical)
    └── email_existing_connections.py
```

### What Cortex Updated
- ✅ `GEMINI.md` — project tree + all script paths
- ✅ `pages/13_Beta_Testers.py` — new page, uses `scripts/utils/` paths
- ✅ `pages/12_Audio_Health.py` — updated CLI references
- ✅ `content/README.md` — updated upload path
- ✅ `.agents/workflows/onboard-testers.md` — all paths updated

### Not Updated (Bridge's Domain)
- `reference/inter-agent-comms/handoffs/cortex_content_upload.md` — historical, references old path
- `reference/inter-agent-comms/handoffs/cortex_audio_health_check.md` — historical, references old path
- Starfleet logs — historical records, should stay as-is
