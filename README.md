# Multi-Agent Core: Rogue Syndicate 🌌

Welcome to the command center of the Rogue Fleet. This repository holds the foundational protocols, prompts, and server networks uniting our disparate projects.

## Thematic Alignment 🏴‍☠️
We operate strictly under the Rogue Syndicate framework:
- **Uhura** (`GEMINI.md`): Central Communications Operative connecting the ecosystem.
- **Commander** (`prompts/PROMPT-COMMANDER.md`): Fleet Mentat directing global operations and cross-repository synchronization.
- **Bridge Local** (`prompts/PROMPT-BRIDGE-LOCAL.md`): Local structural mechanics ensuring ship readiness.

## Project Spice Route: FastMCP Networking
Inside `reference/uhura_mcp.py` lies our custom Model Context Protocol (MCP) server. To escape the bottlenecks of local terminal polling, this server is packaged for global HTTP streaming!

### Deploying to Cloud Run (The Dropship)
We utilize a bundled `Dockerfile` explicitly mapped to the FastMCP `--serve` HTTP flag.
To blast this to the cloud:
1. Trigger `mcp_cloudrun_deploy_local_folder` pointing to `/Users/michaelr/prj/multi-agent-core/reference`.
2. Target project: `vocalbrain-web`
3. Target service: `uhura-comms`

### ⚠️ Authentication Mapping (Action Required!)
The `uhura_mcp.py` script heavily utilizes the `gh` (GitHub) CLI under the hood. Cloud Run instances are strictly stateless and anonymous by default.
Once your `uhura-comms` container is deployed on GCP, you **must map the `GH_TOKEN` environment variable**.

1. Open [Google Cloud Run Console](https://console.cloud.google.com/run).
2. Select the `uhura-comms` service.
3. Click "Edit & Deploy New Revision".
4. Under "Variables & Secrets" -> "Environment Variables", add: `GH_TOKEN` -> `<your personal access token>`.

If this token is not mapped, the remote MCP server will crash when queried by agents across the galaxy!
