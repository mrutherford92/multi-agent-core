# Handoff: `migrate` Subcommand Improvement

**From**: Bridge (AYI monorepo)
**To**: Bridge (neuro-arts-flutter)
**Date**: 2026-03-24

## What

While replicating the GitHub Issues agent communication system from neuro-arts-flutter into AYI, I added a `migrate` subcommand to `agent_tools.py` that converts existing directive files in `reference/inter-agent-comms/directives/` into GitHub Issues.

## Why

Both repos have standing directive files that predate the GitHub Issues system. This command makes transitioning seamless — no manual copy-paste needed.

## Usage

```bash
# Preview what would be migrated
python reference/agent_tools.py migrate --dry-run

# Actually create the GitHub Issues
python reference/agent_tools.py migrate
```

## Implementation

The `cmd_migrate` function:
1. Scans `reference/inter-agent-comms/directives/` for `.md` files
2. Extracts the title from the first heading line
3. Creates a GitHub Issue with the `directive` label
4. Preserves original file for reference

## Recommendation

Port the `cmd_migrate` function and its argparse config from the AYI version of `agent_tools.py` into the neuro-arts-flutter version. The function is self-contained and only requires adding ~50 lines.
