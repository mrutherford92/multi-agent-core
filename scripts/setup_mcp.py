#!/usr/bin/env python3
"""
setup_mcp.py — Automates the injection of the Uhura MCP server
into the global Antigravity MCP configuration.

Run this script once to hook this repository into your IDE instances.
"""
import json
import os
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent.parent
MCP_CONFIG = Path(os.path.expanduser("~/.gemini/antigravity/mcp_config.json"))

VENV_PYTHON = str(CORE_DIR / "reference" / "venv" / "bin" / "python")
MCP_SCRIPT = str(CORE_DIR / "reference" / "uhura_mcp.py")

UHURA_COMMS_CONFIG = {
  "command": VENV_PYTHON,
  "args": [MCP_SCRIPT],
  "env": {}
}

def setup_mcp():
    print(f"📡 Attemping to inject Uhura MCP Server into:\n   {MCP_CONFIG}")

    if not MCP_CONFIG.exists():
        print("❌ Error: IDE MCP Configuration file not found. Have you launched Antigravity?")
        return

    try:
        data = json.loads(MCP_CONFIG.read_text())
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format in the MCP configuration file.")
        return

    if "mcpServers" not in data:
        data["mcpServers"] = {}

    # Inject the server
    data["mcpServers"]["uhura_comms"] = UHURA_COMMS_CONFIG

    # Write safely with indentations
    MCP_CONFIG.write_text(json.dumps(data, indent=2))
    print("✅ Successfully linked the Uhura-Comms MCP server.")
    print("🔄 Antigravity will now automatically boot the server and handle the lifecycle in the background!")

if __name__ == "__main__":
    setup_mcp()
