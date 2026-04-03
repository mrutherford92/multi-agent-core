#!/usr/bin/env python3
"""
uhura_mcp.py — Uhura's Inter-Agent Communications MCP Server

This server bridges Antigravity to the fleet-wide communications network,
enabling fast handoffs, reporting, and direct assignment without needing to
manually use terminal commands.
"""

import sys
import subprocess
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize the MCP Server
mcp = FastMCP("Uhura-Comms")

SCRIPT_DIR = Path(__file__).resolve().parent
AGENT_TOOLS = SCRIPT_DIR / "agent_tools.py"

def run_agent_tools(*args: str) -> str:
    """Helper to run the agent_tools.py CLI and capture output."""
    try:
        result = subprocess.run(
            [sys.executable, str(AGENT_TOOLS), *args],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # We catch exceptions to prevent the MCP tool from crashing out fully,
        # adhering to SO-003 Zero Tolerance (Failure loud log instead of swallow).
        return f"WARNING: Command failed.\nExit code: {e.returncode}\nStderr: {e.stderr.strip()}\nStdout: {e.stdout.strip()}"

@mcp.tool()
def get_fleet_status() -> str:
    """Get the current statuses of all agents in the fleet, including missing or blocking issues."""
    return run_agent_tools("status")

@mcp.tool()
def list_open_tasks() -> str:
    """List all open agent tasks from GitHub, along with active directives."""
    return run_agent_tools("tasks")

@mcp.tool()
def assign_order(agent: str, title: str) -> str:
    """
    Create a new task assigned immediately to a specific agent.
    agent: Must be one of (nexus, cortex, prism, beacon, bridge).
    title: The title and explicit instructions of the task.
    """
    return run_agent_tools("assign", agent, title)

@mcp.tool()
def initiate_handoff(from_agent: str, to_agent: str, task_details: str) -> str:
    """
    Create a formal handoff from one agent to another and log it.
    from_agent: Name of the agent handing it over.
    to_agent: Name of the agent taking control.
    task_details: What the new agent needs to know or do.
    """
    return run_agent_tools("handoff", from_agent, to_agent, task_details)

@mcp.tool()
def read_recent_logs(count: int = 5) -> str:
    """Read recent starfleet communication logs."""
    return run_agent_tools("logs", "--count", str(count))

@mcp.tool()
def system_health_check() -> str:
    """Run a full diagnostic on label synchronizations, statuses, stales, and templates."""
    return run_agent_tools("health")

@mcp.tool()
def broadcast_directive(path: str, content: str) -> str:
    """
    Write or overwrite a directive file securely into the inter-agent-comms structure.
    path: Destination path for the markdown file (e.g., reference/inter-agent-comms/directives/SO-004.md).
    content: The markdown payload.
    """
    return run_agent_tools("write", path, content)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Uhura MCP Server")
    parser.add_argument("--serve", action="store_true", help="Launch a high-speed HTTP/SSE server for distributed syncing")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the HTTP server on")
    args = parser.parse_args()

    if args.serve:
        print(f"📡 Uhura MCP standing by on http://0.0.0.0:{args.port}/sse", file=sys.stderr)
        mcp.run(transport="sse")
    else:
        mcp.run()
