# 🔵 Nexus Handoff — Rename "Apps" → "Tools" (GitHub #36)

**From**: Bridge 🌉
**To**: Nexus 🔵
**Date**: 2026-03-14
**Priority**: HIGH
**Status**: ✅ COMPLETED — 2026-04-02: Code changes verified. Documentation synced.

---

## Context

GitHub Issue #36 — "Rename Apps". The team has decided on **"Tools"** as the new name for the Apps tab. Rationale from METRODAOco: *"We offer research-based digital therapy 'tools' that assist users in creating pathways for mental wellness."*

This is a terminology rename only — no structural changes. Replace "Apps" with "Tools" everywhere it appears as user-facing text.

## Exact Changes Required

### 1. Bottom Navigation Bar

**File**: `lib/navigation/bottom_nav_bar.dart`

| Line | Current | Change To |
|------|---------|-----------|
| 32 | `GlobalKey<NavigatorState>(debugLabel: 'AppsNav')` | `'ToolsNav'` |
| 132 | `// 1: Apps` (comment) | `// 1: Tools` |
| 188–190 | `icon: Icon(Icons.palette_outlined), activeIcon: Icon(Icons.palette), label: 'Apps'` | Change label to `'Tools'` and consider icon → `Icons.build_outlined` / `Icons.build` or `Icons.handyman_outlined` / `Icons.handyman` |

### 2. Directory Screen (the "Apps" tab content)

**File**: `lib/features/arts/views/neuro_arts_directory_screen.dart`

| Line | Current | Change To |
|------|---------|-----------|
| 315 | `title: "Apps"` | `title: "Tools"` |
| 345 | `hintText: 'Search apps...'` | `hintText: 'Search tools...'` |
| 459 | `'All Experiences'` | Keep as-is (or `'All Tools'`) |
| 541 | `'Let us pick the best apps for you...'` | `'Let us pick the best tools for you...'` |
| 594 | `'Suggest Apps For Me'` | `'Suggest Tools For Me'` |

### 3. App Catalog Data

**File**: `lib/features/arts/data/app_catalog.dart`

- The class name `AppCatalog` and `AppEntry` can stay (they're internal code names, not user-facing)
- OR rename to `ToolCatalog` / `ToolEntry` for consistency — Captain's call

### 4. Chatbot Config Reference

**File**: `lib/features/arts/views/neuro_arts_directory_screen.dart`

| Line | Current | Change To |
|------|---------|-----------|
| 208 | `configId: 'chatbot_apps'` | Consider renaming to `'chatbot_tools'` in both Firestore and here |
| 324 | `configId: 'chatbot_apps'` | Same |
| 325–326 | `initialPrompt: "I want a recommendation..."` | Keep as-is (internal prompt, not user-facing) |

> ⚠️ If renaming the Firestore config ID, the `chatbot_apps` document in `chatbot_configs` collection must also be renamed/created. Coordinate with Cortex.

### 5. Favorites Carousel (Home Screen)

**File**: `lib/features/home/widgets/favorites_carousel.dart`

- Check for any "Apps" or "apps" string literals used as section headers
- The carousel imports `app_catalog.dart` — if the class name changes, update the import

### 6. Chatbot RAG Content

- Check if there's an `apps_directory_guide.md` or similar RAG doc that references "Apps tab"
- Update terminology to "Tools" / "Toolbox"

## Icon Decision

**Captain's order: Keep `Icons.palette_outlined` / `Icons.palette`** — these are creative/artistic tools, the palette fits.

Do NOT change the icon.

## Do NOT Change

- Internal variable names (unless Captain requests full rename)
- Feature directory `lib/features/arts/` — this is fine, no user sees it
- The `AppEntry` / `AppCatalog` class names — unless explicitly requested
- The Firestore `chatbot_apps` config ID — unless coordinated with Cortex
- Any functionality — this is a pure cosmetic/terminology change

---

## Verification

- [ ] Build the app and confirm no "Apps" string appears in the bottom nav
- [ ] Navigate to the Tools tab — title should say "Tools" or "Toolbox"
- [ ] Search hint should say "Search tools..."
- [ ] Suggest button should say "Suggest Tools For Me"
- [ ] Run `grep -r '"Apps"' lib/` and `grep -r "'Apps'" lib/` to confirm no remaining user-facing occurrences
