# Standing Order 006: Code Reviews

**From:** Captain Michael
**Applies to:** Bridge (primary reviewer and fixer)
**Status:** ACTIVE

## Protocol

Bridge is responsible for code reviews AND the resulting fixes. Other agents stay focused on their current work.

1. **Bridge reviews** significant code changes
2. Bridge creates a GitHub Issue titled `[BRIDGE] Code Review: <file> — Status: PENDING`
3. **Bridge fixes the issues directly** — do NOT assign fixes to the original author
4. After fixing, Bridge updates the issue to `Status: APPROVED` and closes it

## Status Lifecycle
- 🟡 **PENDING** — Review created, fixes identified
- 🔧 **IN PROGRESS** — Bridge is applying fixes
- 🟢 **APPROVED** — All issues resolved, code is cleared
- 🔴 **BLOCKED** — Critical design issue that requires Captain decision

## What Gets Reviewed
- New files over 100 lines
- Changes to data models or Firestore writes
- Security-sensitive code (auth, roles, privacy)
- Migration scripts
- Anything touching Standing Order 003 compliance

## Key Rule
**Do NOT assign review fixes to busy agents.** Bridge owns the review process end-to-end. If a fix requires deep domain knowledge Bridge doesn't have, escalate to the Captain — not the agent.
