# SO-012: Input Validation & Guardrails
**Effective Date**: 2026-04-02
**Applies To**: All Agents

## Directive Objective
All text inputs across the platform must have designated guardrails (sensible max lengths).

## Rules
1. **Enforcement**: Inputs must define `maxLength` or `inputFormatters` to prevent overflow and UI breaks.
2. **Standard Fallback**: All unrecognized or newly created TextFields default to `maxLength: 1000`.
