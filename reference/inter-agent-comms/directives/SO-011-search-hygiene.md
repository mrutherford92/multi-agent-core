# SO-011: Agent Search Engine Hygiene

## Order
When searching for files, strings, or code, ALL agents across ALL projects (including the AYI bridge/web crew) MUST strictly exclude massive dependency directories. Doing blind wildcard searches across the filesystem crashes context windows, wastes time, and angers the Captain.

**Never search inside:**
- `.venv/` (Python virtual environments)
- `node_modules/` (Node.js dependencies in Next.js/Web)
- `.dart_tool/` (Dart build cache)
- `ios/Pods/` (iOS CocoaPods)
- `build/` (Output build artifacts)
- `.git/` (Git history)

**Always:**
1. Use specific tools like `grep_search` and actively configure the `Includes` array to ONLY search `.dart`, `.py`, `.ts`, or `.tsx` files.
2. If forced to use terminal `find` or `grep`, always append exclusion flags (e.g., `-type d -name .venv -prune -o`). 
3. Rely on Antigravity/VS Code index limits where available.

## Scope
All Agents (Bridge, Nexus, Cortex, Prism, Beacon). Specifically applies to both the Flutter monorepo context and the AYI web monorepo contexts.

## Effective
Immediate
