# Standing Order 007: UX, Color, and Branding Standards

**From:** Captain Michael
**Applies to:** All agents (especially Nexus, Prism, Beacon)
**Status:** ACTIVE

## The Rule

**Every color in the app MUST come from `Pallete` in `lib/core/theme/app_pallete.dart`.** No exceptions. No hardcoded hex values. No `Colors.blue`. No `Color(0xFF...)` inline.

## Color Rules

### ❌ NEVER Do This
```dart
// Hardcoded hex — VIOLATION
color: Color(0xFF6366F1),

// Flutter named color — VIOLATION
color: Colors.blue,
color: Colors.red.shade400,

// Opacity on a hardcoded color — VIOLATION
color: Color(0xFF4CAF50).withOpacity(0.5),
```

### ✅ Always Do This
```dart
// Use the Palette
color: Pallete.gradient1,
color: Pallete.actionGreen,
color: Pallete.errorColor,
color: Pallete.greyColor.withOpacity(0.5),
```

### Adding New Colors
If you need a color that doesn't exist in the palette:
1. **Check first** — odds are a suitable color already exists
2. If truly needed, **add it to `app_pallete.dart`** with a descriptive name, hex comment, and put it in the correct section
3. **Never add random colors** — new colors must harmonize with the existing palette
4. Get Bridge review if adding more than one new color

## Core Brand Colors

| Name | Hex | Use |
|------|-----|-----|
| `gradient1` | `#4253FD` | Primary Blue — brand identity |
| `gradient2` | `#19857B` | Secondary Teal — brand accent |
| `gradient3` | `#8C9EFF` | Indigo A100 — light accent |
| `actionGreen` | `#00CC66` | Start/Go/Positive actions |
| `backgroundColor` | `#0F172A` | Dark mode background (Slate 900) |
| `cardColor` | `#1E293B` | Card/surface (Slate 800) |

## UX Standards

### Dark Mode
- The app is **dark-mode only**. Do not create light-mode variants.
- Background: `Pallete.backgroundColor` (Slate 900)
- Cards/surfaces: `Pallete.cardColor` (Slate 800)
- Borders: `Pallete.borderColor` (Slate 700)

### Text Hierarchy
- Primary text: `Pallete.textColor` (Slate 100)
- Secondary text: `Pallete.greyColor` (Slate 400)
- Tertiary/disabled: `Pallete.subtitleText` (Slate 500)
- Never use pure white (`Colors.white`) for body text — use `Pallete.textColor`

### Buttons & Actions
- Primary action: `Pallete.gradient1` (Blue) or gradient of `gradient1 → gradient2`
- Success/positive: `Pallete.actionGreen`
- Destructive: `Pallete.errorColor` or `Pallete.deepOrangeColor`
- Warning: `Pallete.warningColor`

### Immersive Screens
- Immersive experiences (breathing, meditation, sleep) have **their own palette sections** in `app_pallete.dart`
- These colors are ONLY for their designated screens — don't reuse `sleepIndigo` on a profile page
- Always use the named constant, never copy the hex value inline

## Branding Rules

1. **Consistency over creativity** — match existing screens, don't invent new aesthetics
2. **Gradients** — use the `tileGradients` list for card/tile backgrounds, don't create ad-hoc gradient pairs
3. **No random accent colors** — if it isn't in the palette, it doesn't belong in the app
4. **Icons** — use Material Icons (`Icons.xxx`), don't mix icon libraries without approval
5. **Typography** — use the app's theme text styles, never hardcode font sizes or weights inline
6. **Spacing** — use consistent multiples of 4px or 8px for padding/margins

## Enforcement

Bridge will flag hardcoded colors during code reviews. If you're unsure whether a color belongs, check `app_pallete.dart` first and ask Bridge.
