---
description: Standing Order 014 — Enforcement and upkeep of local indexing and file directories.
---

# 📜 Standing Order 014: UI Audit & Architecture Indexing

**Authority:** Captain Michael / Bridge Prime
**Scope:** ALL LOCAL AGENTS (Bridge, Nexus, Cortex)
**Applies To:** Monorepo architecture mapping and knowledge retrieval.

## Directive Overview
Agents operating within repository sub-projects must prioritize maintaining an indexed "dictionary" of visual and routing files to prevent exhaustive searching of the codebase during task execution.

Every architectural change, new addition, or significant refactor MUST trigger a prompt indexing operation using the explicit schema outlined below. The index provides immediate conceptual context mapped directly to the local filesystem.

## Agent Instructions: Generating & Updating the Index

When requested to create or update an index artifact (e.g., `reference/ui-audit-index.md`), agents MUST adhere strictly to this prompt/framework:

1. **Explore the Codebase:** Systematically scan through all core application directories (e.g., `src/`, `components/`, `lib/`, `api/`, `docs/`, etc.). Ignore build artifacts, `node_modules`, and standard configuration files unless they contain critical custom logic.
2. **Build the Index:** For every significant file, create an entry in the designated index document.
3. **Format Requirements:** Structure each entry clearly. You must include the following fields for every file:
   - **File Path:** The relative path (e.g., `src/app/api/auth/route.ts`).
   - **Overview:** A concise 1-2 sentence description explaining exactly what the file does, what patterns it uses, and its primary responsibility in the application.
   - **Keywords:** A comma-separated list of 5-10 highly relevant search terms. These should include function names, exported components, business logic concepts (e.g., "authentication, firebase, edge runtime, session cookies, login"), and data models handled within.

### Example Schema
```markdown
### `src/components/RoleGuard.tsx`
**Overview:** Client-side wrapper component that enforces Role-Based Access Control (RBAC). It intercepts unauthorized users based on Firebase Custom Claims and forcefully redirects them to the fallback dashboard.
**Keywords:** RBAC, security, routing, layout wrapper, permissions, redirect, useAuth, ADMIN, CLIENT, STAFF.
```

## Mandatory Cross-Agent Sharing
Any localized updates to the index must be immediately cross-referenced or ported to the overarching `multi-agent-core/reference/` repository, ensuring that all dispatched agents inherit an accurate geographical mapping of the file hierarchies they will navigate.
