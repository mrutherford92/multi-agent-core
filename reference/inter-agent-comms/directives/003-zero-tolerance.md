# ⛔ Standing Order 003: Zero Tolerance (PERMANENT)

**Issued by**: Captain Michael
**Date**: 2026-03-13
**Status**: PERMANENT — This overrides all other behaviors.

---

This directive applies to **ALL agents** on the NeuroArts crew.

## Rules

1. **NEVER insert placeholder data.** If a field has no real value, use `null` — not "pending", not "TBD", not a fabricated string. Those are LIES that corrupt the data.

2. **NEVER swallow exceptions silently.** Every `catch` must log the error with context. If using a fallback, log a WARNING explaining what failed and why.

3. **NEVER use hidden defaults that mask failures.** If a query fails, return an error — don't return empty results pretending nothing is wrong.

4. **NEVER hide true system status.** Loading = "Loading". Error = show the error. Empty = "No data". Not fake data.

5. **Fail loudly.** A visible error is 10x better than invisible corruption. The Captain needs to see what's real.

## Language-Specific

### Python (Cortex)
- Every `except` block must `logging.error()` with full context
- If a row fails to import, log it with the row data — don't skip silently
- If 0 rows processed, that's a 🔴 CRITICAL issue to report

### Dart/Flutter (Nexus)
- Services throw → ViewModels catch → UI surfaces (SnackBar/Toast/Dialog)
- Never return empty lists or error strings from service methods
- Always `rethrow` after `debugPrint`

### TypeScript/Next.js (Prism)
- Every `catch` must `console.error()` with full context AND surface the error in the UI
- If an API returns an error, show the error — don't render fake cards
- If data is missing, show "No data" — not fabricated values

### HTML/Static (Beacon)
- Never use placeholder copy — use real brand messaging or leave sections clearly marked as TODO
- Never use stock photos without explicit approval
