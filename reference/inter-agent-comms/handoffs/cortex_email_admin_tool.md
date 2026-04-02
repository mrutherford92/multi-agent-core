# 🟠 Cortex Handoff — Email System & Admin Email Callable

**From**: Bridge 🌉
**To**: Cortex 🟠
**Date**: 2026-03-14
**Priority**: MEDIUM
**Status**: AWAITING PICKUP

---

## Context

Bridge deployed a full email notification system into `functions_notifications/`. Emails are sent via SendGrid alongside push notifications for connection events. A new admin-only callable `send_admin_email` is deployed and ready for integration into the admin tool.

## What Bridge Built

### 1. Cloud Functions (Deployed ✅)

| Function | Trigger | Action |
|----------|---------|--------|
| `notify_connection_request` | Firestore `onCreate` on `connection_requests/{id}` | Push + email to recipient |
| `on_connection_accepted` | Firestore `onUpdate` on `connection_requests/{id}` (status → accepted) | Push + email to requester |
| `send_admin_email` | HTTPS callable (admin-only) | Send email to one or many recipients |

### 2. Email Templates (`email_templates.py`)

- `connection_request_email(sender_name, recipient_name)` → subject + HTML
- `connection_accepted_email(acceptor_name, requester_name)` → subject + HTML
- `retroactive_connection_email(recipient_name, connection_name)` → subject + HTML
- `marketing_email(recipient_name, subject, headline, body_text, cta_text, cta_url)` → subject + HTML

All templates use the NeuroArts branded dark theme (#0A0A1A background, teal accents).

### 3. Retroactive Script (`admin-tool/scripts/email_existing_connections.py`)

Already executed — 14 emails sent to 7 accepted connections, 0 errors. Tracking collection `email_sent_connections` prevents re-sends.

## What Cortex Needs To Do

### 1. Add Email Page to Admin Tool (Streamlit)

- [ ] Create `pages/13_Email.py` (or similar) in admin-tool
- [ ] Wire to `send_admin_email` callable via Firebase Admin SDK
- [ ] UI: recipient picker (text field or user search), subject, body editor
- [ ] Support the `template: "marketing"` option for branded emails
- [ ] Display send history from a new `email_log` Firestore collection (optional)

### 2. `send_admin_email` Callable API

```python
# Call from admin tool:
from firebase_admin import functions

result = functions.httpsCallable("send_admin_email")({
    "to": "user@example.com",           # or ["a@b.com", "c@d.com"]
    "subject": "Newsletter Subject",
    "template": "marketing",            # optional — uses branded template
    "headline": "Big Announcement!",    # used with template
    "body_text": "Here's what's new...",# used with template
    "cta_text": "Open NeuroArts",       # optional
    "cta_url": "https://neuroarts.ai",  # optional
})
# Returns: {"success": true, "sentTo": 1, "failed": []}
```

Or send raw HTML:
```python
result = functions.httpsCallable("send_admin_email")({
    "to": ["user1@example.com", "user2@example.com"],
    "subject": "Custom Email",
    "html_body": "<h1>Hello</h1><p>Custom content</p>",
})
```

### 3. Security Note

- The `SENDGRID_API_KEY` is stored as a Firebase Functions secret (version 1 created)
- Admin-only check: verifies `isAdmin: true` on calling user's Firestore doc
- No need to handle the API key in the admin tool — the callable accesses it server-side

### 4. Future: Batch Email to All Users

- [ ] Consider adding a "Broadcast Email" feature that queries all users with `emailNotifications != false`
- [ ] Rate limit: SendGrid free tier = 100/day, paid = 100/second
- [ ] Could reuse the `marketing_email` template with custom headlines/body

---

## Key Files

| File | Purpose |
|------|---------|
| `functions_notifications/main.py` | All email + push logic, `send_admin_email` callable |
| `functions_notifications/email_templates.py` | 4 branded HTML templates |
| `admin-tool/scripts/email_existing_connections.py` | Retroactive email script (already run) |
