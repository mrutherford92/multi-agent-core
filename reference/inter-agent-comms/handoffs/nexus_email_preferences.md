# 🔵 Nexus Handoff — Email Notification Preferences UI

**From**: Bridge 🌉
**To**: Nexus 🔵
**Date**: 2026-03-14
**Priority**: MEDIUM
**Status**: AWAITING PICKUP

---

## Context

Bridge deployed email notifications for connection requests and acceptances alongside existing push notifications. Emails are sent via SendGrid from `functions_notifications/main.py`. The system checks `notificationPreferences.emailNotifications` before sending — but the **Flutter UI does not yet expose this toggle**.

## What Bridge Built (Backend)

1. **`notify_connection_request`** (enhanced) — sends push + email to recipient when a connection request is created
2. **`on_connection_accepted`** (new trigger) — sends push + email to original requester when accepted
3. **Email preference check**: `user_data.notificationPreferences.emailNotifications` — defaults to `true` if not set

## What Nexus Needs To Do

### 1. Add Email Notification Toggle to Settings

- [ ] In the notification preferences UI (wherever `communityNotifications` toggles live), add an **"Email Notifications"** toggle
- [ ] Field path: `notificationPreferences.emailNotifications` (Boolean)
- [ ] Default: `true` — should display as ON when the field doesn't exist
- [ ] Toggling OFF should set `emailNotifications: false` in Firestore
- [ ] Consider grouping under existing community notifications section

### 2. Verify Connection Request Flow Still Works

- [ ] Send a connection request → verify push notification fires
- [ ] Check email inbox (sender receives email too)
- [ ] Accept a connection request → verify push notification fires to requester
- [ ] Verify both events log properly in Firebase Functions logs

### 3. Consider Email Opt-In UX (Future)

- [ ] During onboarding, prompt user to enable/disable email notifications
- [ ] Consider per-type granularity later (e.g., email for connections but not for likes)

---

## Key Files

| File | Purpose |
|------|---------|
| `functions_notifications/main.py` | Connection triggers with email (lines 556-766) |
| `functions_notifications/email_templates.py` | Branded HTML templates |
| Notification preferences in Firestore | `users/{uid}.notificationPreferences.emailNotifications` |
