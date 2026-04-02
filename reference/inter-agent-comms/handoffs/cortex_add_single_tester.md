# Handoff: Add Single Tester via Streamlit UI

**From**: Bridge
**Date**: 2026-03-18
**Priority**: 🔴 Captain waiting — build this now
**Status**: ✅ COMPLETED — 2026-03-18

---

## Request

Add an "Add Tester" form to the Beta Testers Streamlit page (`pages/13_Beta_Testers.py`) so the Captain can manually add individual testers from the admin tool UI.

## Required Functionality

A form with these fields:
- **Email** (required)
- **First Name** (optional)
- **Last Name** (optional)
- **Preferred Device** (dropdown: Android / iOS / No Preference)

On submit, the form should:
1. **Add to Google Group** (`closed-testers@neuroarts.ai`) — using the logic from `scripts/utils/add_testers_to_group.py`
2. **Add to Firestore** (`beta_testers` collection) — same script logic
3. Show success/error status in the UI
4. Handle duplicates gracefully (skip Google Group if already member, merge-update Firestore)

## Implementation Notes

- The `add_testers_to_group.py` script already has all the functions needed: `get_directory_service()`, `add_member_to_group()`, `sync_tester_to_firestore()`, `get_firestore_client()`, `email_to_doc_id()`
- Import those functions directly rather than duplicating logic
- Service account: `~/vocalbrain-adminsdk.json` handles both Google Admin SDK and Firebase Admin
- The Google Admin SDK requires domain-wide delegation (already configured)

## Firestore Schema Reference

```
beta_testers/{email_hash_16chars}
├── email: string
├── firstName: string | null
├── lastName: string | null
├── preferredDevice: "iOS" | "Android" | null
├── source: "manual"  ← use "manual" for UI-added testers
├── platforms:
│   ├── googleGroup: true
│   ├── googleGroupAddedAt: Timestamp
│   ├── testFlight: false
│   └── testFlightAddedAt: null
├── createdAt: Timestamp
└── updatedAt: Timestamp
```

## First Test User

Captain will immediately add: `keith@keithdevens.com` (iOS user)
