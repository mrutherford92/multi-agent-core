# Standing Order 009: Testing & Verification Standards

**Effective Date**: 2026-03-30
**Issued By**: Captain Michael via Bridge
**Applies To**: ALL agents (Bridge, Nexus, Cortex, Prism, Beacon)
**Status**: PERMANENT — This overrides default behavior.

---

## The Rule

**No code ships to `main` without passing ALL verification gates.**

Agents may NOT mark issues as "fixed" or push to `main` until they have:
1. Passed `dart analyze --fatal-infos` (or language equivalent)
2. Passed `flutter test` (ALL tests, not just your new ones)
3. Passed the SO-003 compliance scan (`scripts/so003_scan.sh`)
4. Written regression tests for any bug fix

## Agent Verification Protocol

Before pushing ANY commit to `main`, run:
```bash
cd projects/neuro-arts-flutter && bash scripts/verify.sh
```

If it fails, **DO NOT PUSH. Fix the issues first.**

## Mandatory Test Coverage

When modifying these critical systems, you MUST write or update tests:

| System | Test Directory | Minimum |
|--------|---------------|---------|
| Notifications | `test/features/notifications/` | All enum values, preference enforcement |
| Social Service | `test/features/social/` | Follow/connect/block flows |
| Dashboard | `test/features/home/` | Widget interactivity |
| Groups | `test/features/groups/` | Join/leave/invite flows |
| Models | Same as feature | Round-trip serialization for ALL enums |

### What "Writing Tests" Means

- **Bug fix?** → Write a **regression test** that fails without the fix, passes with it.
- **New enum/type?** → Add to the exhaustive enum round-trip test.
- **New preference?** → Add to the preference enforcement test suite.
- **New navigation?** → Verify the tap handler covers it.

## CI Pipeline

GitHub Actions runs automatically on every push and PR to `main`:
- Gate 1: `dart analyze --fatal-infos`
- Gate 2: `flutter test`
- Gate 3: `scripts/so003_scan.sh`

If ANY gate fails, the build is RED.

## Consequences of Violation

- Bug shipped without tests → Agent writes both the fix AND the missing tests
- Silent catch found by scanner → Agent fixes ALL instances in the file they touched
- SO-003 scan fails → Push is blocked until resolved

---

## Reference Files

- `.github/workflows/ci.yml` — CI pipeline definition
- `scripts/verify.sh` — Local pre-push verification
- `scripts/so003_scan.sh` — SO-003 compliance scanner
- `test/features/notifications/` — Reference test implementations
