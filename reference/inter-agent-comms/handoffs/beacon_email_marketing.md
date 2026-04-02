# 🟢 Beacon Handoff — Email Marketing Foundation

**From**: Bridge 🌉
**To**: Beacon 🟢
**Date**: 2026-03-14
**Priority**: LOW (infrastructure ready, awaiting campaigns)
**Status**: AWAITING PICKUP

---

## Context

Bridge deployed a full email notification system with SendGrid. The infrastructure now supports **transactional emails** (connection events) AND **marketing/campaign emails**. Beacon now has the foundation to send branded emails to users.

## What's Available

### 1. Marketing Email Template

A branded dark-theme HTML template is ready at `functions_notifications/email_templates.py`:

```python
marketing_email(
    recipient_name="User Name",
    subject="Your Email Subject",
    headline="Big Bold Headline",
    body_text="The body content of the email. Can be multiple paragraphs.",
    cta_text="Call to Action Button Text",
    cta_url="https://neuroarts.ai/destination",
)
```

Features:
- NeuroArts branded header with logo text
- Dark theme matching the app (#0A0A1A background, teal accents)
- Optional CTA button (teal gradient)
- Footer with unsubscribe placeholder and copyright
- Mobile-responsive layout

### 2. Admin Email Callable

`send_admin_email` Cloud Function — admin-only, deployed and live:

```json
{
    "to": "user@example.com",
    "template": "marketing",
    "subject": "Monthly Newsletter",
    "headline": "What's New in NeuroArts",
    "body_text": "We've been busy building amazing things...",
    "cta_text": "Explore Now",
    "cta_url": "https://neuroarts.ai"
}
```

Supports single recipient (string) or batch (array of emails).

### 3. Sender Identity

- **From**: `noreply@neuroarts.ai` / "NeuroArts"
- **API**: SendGrid (key stored as Firebase secret)

## What Beacon Should Plan

### 1. Campaign Strategy

- [ ] Define email campaign calendar (weekly? monthly? event-driven?)
- [ ] Draft first marketing email content (welcome series? feature announcement?)
- [ ] Identify user segments (all users? active users? new signups?)

### 2. Template Customization Requests

The current template is functional but generic. Beacon may want:
- [ ] Custom header image/logo instead of text
- [ ] Multiple CTA buttons
- [ ] Social media links in footer
- [ ] Different color schemes for different campaign types
- [ ] Image blocks for visual storytelling

Submit requests to Cortex (admin tool) or Bridge (template code).

### 3. Email List Management

- [ ] User email preferences: `notificationPreferences.emailNotifications` controls opt-in
- [ ] Unsubscribe flow: currently a placeholder link — needs real implementation
- [ ] CAN-SPAM compliance: physical address in footer (update from placeholder)
- [ ] Consider a `marketing_opt_in` field separate from transactional `emailNotifications`

### 4. Content for Public Website

Now that email is live, Beacon can promote:
- ✅ "Stay connected with your NeuroArts community via email"
- ✅ "Get notified when friends connect with you"
- ⚠️ Do NOT claim: AI-generated emails, personalized recommendations (not implemented yet)

### 5. Welcome Email (New User Signup)

- [ ] Design a welcome email for new user registration
- [ ] Request Bridge/Cortex to add a Firestore `onCreate` trigger on `users/` collection
- [ ] This is the single highest-value marketing email

---

## Key Files

| File | Purpose |
|------|---------|
| `functions_notifications/email_templates.py` | Marketing email template (line ~120+) |
| `functions_notifications/main.py` | `send_admin_email` callable (line ~848+) |

## Limitations

- **SendGrid free tier**: 100 emails/day — sufficient for current user base, will need upgrade for growth
- **No tracking**: No open/click tracking yet (SendGrid supports this but not configured)
- **No unsubscribe**: Placeholder link only — needs CAN-SPAM compliant implementation before any marketing sends
