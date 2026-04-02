# Handoff: Beta Tester Onboarding Infrastructure

**From**: Bridge
**Date**: 2026-03-18
**Priority**: 🟡 Awareness + Future Enhancement

---

## What Was Built

Bridge created a tester onboarding pipeline in your project:

### New Files
- **`scripts/add_testers_to_group.py`** — Bulk-imports beta testers from HubSpot CSV into:
  1. Google Group (`closed-testers@neuroarts.ai`) → Play Store closed testing access
  2. Firestore `beta_testers` collection → source of truth for all tester data

- **`data/hubspot-beta-signups.csv`** — Latest HubSpot export (gitignored, contains PII)

### Infrastructure Set Up
- **Python venv** created at `.venv/` with `google-api-python-client`, `google-auth`, `firebase-admin`
- **Admin SDK API** enabled on `vocalbrain-web`
- **Domain-wide delegation** configured for service account (scope: `admin.directory.group.member`)

### Current State
- **13 beta testers** imported from HubSpot → Google Group (15 total members) + Firestore
- **1 iOS tester** flagged: Marshall Green (`marshall.green04@icloud.com`)
- Workflow documented at `/.agents/workflows/onboard-testers.md`

## Firestore Schema: `beta_testers/{email_hash}`

```
email: string
firstName: string | null
lastName: string | null
phone: string | null
preferredDevice: "iOS" | "Android" | null
interest: string | null
referralSource: string | null
signupDate: string | null
source: "hubspot"
platforms:
  googleGroup: boolean
  googleGroupAddedAt: Timestamp | null
  testFlight: boolean
  testFlightAddedAt: Timestamp | null
createdAt: Timestamp
updatedAt: Timestamp
```

## Your Action Items

### Optional Enhancements (When Time Permits)
1. **Add a "Beta Testers" page to Streamlit** — read from Firestore `beta_testers`, show table with platform status, device preference, signup date. Allow manual toggle of `testFlight` flag.
2. **Analytics** — signup trend chart, referral source breakdown, device preference distribution
3. **Email integration** — when a tester is added, trigger a welcome email via SendGrid

### No Immediate Action Required
The pipeline is operational. Captain will re-export from HubSpot and re-run the script as new signups come in.
