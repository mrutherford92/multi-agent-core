# 🔴 URGENT: Profile Privacy — "All Details" Section

**From**: Bridge
**To**: Nexus
**Date**: 2026-03-20
**Priority**: HIGH — Captain Order

## Context

Cortex added a collapsible "All Details" section to `public_profile_screen.dart` (commit `581997e7`) that exposes 7 profile fields to all visitors with **zero privacy gating**. Captain has flagged this as a privacy violation. Bridge has issued Cortex a handoff to fix the immediate issue.

## What You Need to Know

1. **Bio privacy default is wrong** — `isBioPublic ?? true` on lines 606 and 838 should be `?? false`. The Edit Profile screen already defaults this to `false`.

2. **7 fields shown without consent** — Primary Art, Creative Interests, Inspiration Sources, Singing Experience, Singing Style, Vocal Range, Favorite Artist are all shown to anyone viewing a profile.

3. **VocalBrain legacy fields** — Some of these fields (`singingExperience`, `singingStyle`, `vocalRange`, `favoriteSinger`) may be VocalBrain-specific and not relevant to NeuroArts. Review whether they belong in the NeuroArts profile at all.

## Your Action Items

1. **If Cortex applies Option A** (owner-only gating), verify the fix works correctly on device.

2. **If the team decides to add per-field privacy toggles (Option B)**, you own the UI side:
   - Add toggle switches to the Edit Profile screen for each new privacy field
   - All toggles must default to **OFF** (private)
   - Follow the existing pattern used for `isBioPublic` and `isEmailPublic`

3. **Audit the rest of `public_profile_screen.dart`** for any other fields that might be shown without privacy gates. The rule is simple: **if a field contains user-provided personal data, it must be gated.**

## Captain's Rule
> NOTHING is default public.
