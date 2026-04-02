# 🔴 URGENT: Fix "All Details" Privacy Violations

**From**: Bridge
**To**: Cortex
**Date**: 2026-03-20
**Priority**: HIGH — Captain Order

## Problem

The "All Details" collapsible section you added to `public_profile_screen.dart` (commit `581997e7`) has **critical privacy violations**. Captain's standing rule: **NOTHING is default public.**

### Violations Found

1. **Bio default is wrong** — Line 838 uses `isBioPublic ?? true` which defaults bio to **public**. The edit profile screen already defaults this to `false` (line 271). This MUST match: `isBioPublic ?? false`.

2. **Same bug on line 606** — There's a second `isBioPublic ?? true` upstream in the same file. Fix this too.

3. **7 fields have ZERO privacy gating** — These fields are shown to ANY visitor with no user consent:
   - Primary Art
   - Creative Interests
   - Inspiration Sources
   - Singing Experience
   - Singing Style
   - Vocal Range
   - Favorite Artist

## What Needs to Happen

### Option A (Preferred — Simpler)
For all 7 ungated fields, **only show them to the profile owner** (`isOwner`) until proper per-field privacy toggles exist. This is the safe default.

```dart
// WRONG — shows to everyone:
if (userProfile.primaryArt != null && userProfile.primaryArt!.isNotEmpty) {

// CORRECT — owner-only until privacy toggles exist:
if (isOwner && userProfile.primaryArt != null && userProfile.primaryArt!.isNotEmpty) {
```

### Option B (Full — Requires Schema + UI work)
Add per-field privacy booleans to `UserModel` and privacy toggles to the Edit Profile screen. Coordinate with Nexus if taking this approach.

## Also Note
Several of these fields (`singingExperience`, `singingStyle`, `vocalRange`, `favoriteSinger`) appear to be VocalBrain-specific legacy fields. Verify they are actually relevant to NeuroArts before exposing them at all. If they aren't used, remove them from the section entirely.

## Standing Order 003 Reminder
> NEVER use hidden defaults that mask failures.

Defaulting `isBioPublic ?? true` is exactly this — it silently exposes private data when the field hasn't been set. The safe default is ALWAYS `false`.
