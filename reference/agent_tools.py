#!/usr/bin/env python3
"""
agent_tools.py — NeuroArts Multi-Agent System CLI

Manage the agent communication system from the command line.
Uses `gh` CLI for GitHub Issues and reads local reference files.

Usage:
    python reference/agent_tools.py status    # View agent statuses
    python reference/agent_tools.py tasks     # List open agent tasks
    python reference/agent_tools.py assign nexus "Fix notification badges"
    python reference/agent_tools.py handoff bridge nexus "Audio pipeline data"
    python reference/agent_tools.py health    # System health check
    python reference/agent_tools.py logs      # Recent starfleet log entries
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = "mrutherford92/neuro-arts-flutter"
SCRIPT_DIR = Path(__file__).resolve().parent
COMMS_DIR = SCRIPT_DIR / "inter-agent-comms"

AGENTS = {
    "bridge": {"label": "agent:bridge", "color": "Gray", "role": "Architect & Coordinator"},
    "nexus": {"label": "agent:nexus", "color": "Blue", "role": "Mobile Experience Designer"},
    "cortex": {"label": "agent:cortex", "color": "Amber", "role": "Intelligence Officer (ML/Data)"},
    "prism": {"label": "agent:prism", "color": "Purple", "role": "Web Experience Designer"},
    "beacon": {"label": "agent:beacon", "color": "Green", "role": "Marketing & Growth"},
}

REQUIRED_LABELS = [
    "agent:bridge", "agent:nexus", "agent:cortex", "agent:prism", "agent:beacon",
    "agent-task", "handoff", "directive", "blocked",
]


def run_gh(args: list[str], check: bool = True) -> str:
    """Run a gh CLI command and return stdout."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True, text=True, check=check
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print("ERROR: `gh` CLI not found. Install: https://cli.github.com/")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: gh command failed: {e.stderr.strip()}")
        return ""


def cmd_status(args):
    """Show agent status from local JSON files and GitHub Issues."""
    print("=" * 60)
    print("🛸 NEUROARTS CREW STATUS")
    print("=" * 60)

    status_dir = COMMS_DIR / "status"
    if not status_dir.exists():
        print("\n⚠️  No status directory found at:", status_dir)
        return

    for agent_name, info in AGENTS.items():
        status_file = status_dir / f"{agent_name}.json"
        print(f"\n{'─' * 40}")
        print(f"{'🔵' if agent_name == 'nexus' else '🟠' if agent_name == 'cortex' else '🟣' if agent_name == 'prism' else '🟢' if agent_name == 'beacon' else '⬜'} {agent_name.upper()} — {info['role']}")

        if status_file.exists():
            try:
                data = json.loads(status_file.read_text())
                status = data.get("status", "unknown")
                last_task = data.get("lastTask") or data.get("currentMission") or "N/A"
                blockers = data.get("blockers")
                timestamp = data.get("timestamp") or data.get("lastActive") or "N/A"

                status_icon = "✅" if status == "completed" else "🔴" if status == "blocked" else "🔄" if status == "in-progress" else "❓"
                print(f"  Status: {status_icon} {status}")
                print(f"  Last task: {last_task[:80]}{'...' if len(last_task) > 80 else ''}")
                if blockers:
                    print(f"  ⚠️  Blocker: {blockers}")
                print(f"  Updated: {timestamp}")
            except json.JSONDecodeError:
                print("  ⚠️  Invalid JSON in status file")
        else:
            print("  ⚠️  No status file")

        # Count open GitHub issues for this agent
        output = run_gh(["issue", "list", "--label", info["label"],
                        "--state", "open", "--repo", REPO, "--json", "number"], check=False)
        if output:
            try:
                issues = json.loads(output)
                count = len(issues)
                if count > 0:
                    print(f"  📋 {count} open GitHub issue(s)")
            except json.JSONDecodeError:
                pass

    print(f"\n{'=' * 60}")


def cmd_tasks(args):
    """List all open agent tasks from GitHub."""
    print("📋 OPEN AGENT TASKS")
    print("=" * 60)

    output = run_gh([
        "issue", "list", "--label", "agent-task", "--state", "open",
        "--repo", REPO, "--json", "number,title,labels,updatedAt",
    ])

    if not output:
        print("\nNo open agent tasks.")
        return

    try:
        issues = json.loads(output)
    except json.JSONDecodeError:
        print("ERROR: Could not parse GitHub response")
        return

    if not issues:
        print("\nNo open agent tasks.")
        return

    for issue in issues:
        labels = ", ".join(l["name"] for l in issue.get("labels", []))
        print(f"\n  #{issue['number']}: {issue['title']}")
        print(f"    Labels: {labels}")
        print(f"    Updated: {issue['updatedAt'][:10]}")

    # Also show directives
    print(f"\n{'─' * 40}")
    print("📡 ACTIVE DIRECTIVES")

    dir_output = run_gh([
        "issue", "list", "--label", "directive", "--state", "open",
        "--repo", REPO, "--json", "number,title",
    ])

    if dir_output:
        try:
            directives = json.loads(dir_output)
            for d in directives:
                print(f"  #{d['number']}: {d['title']}")
        except json.JSONDecodeError:
            pass

    print(f"\n{'=' * 60}")


def cmd_assign(args):
    """Create a task issue for a specific agent."""
    agent = args.agent.lower()
    if agent not in AGENTS:
        print(f"ERROR: Unknown agent '{agent}'. Choose from: {', '.join(AGENTS.keys())}")
        sys.exit(1)

    title = f"[{agent.upper()}] {args.title}"
    labels = f"agent-task,{AGENTS[agent]['label']}"

    body = f"""## Orders
{args.title}

## Context
Created via `agent_tools.py assign` by Captain Michael.

## Acceptance Criteria
- [ ] Task completed as described
- [ ] No Standing Order 003 violations

## Notes
Created: {datetime.now(timezone.utc).isoformat()}
"""

    output = run_gh([
        "issue", "create", "--repo", REPO,
        "--title", title,
        "--label", labels,
        "--body", body,
    ])

    print(f"✅ Task created for {agent.upper()}: {output}")


def cmd_handoff(args):
    """Create a handoff issue between agents."""
    from_agent = args.from_agent.lower()
    to_agent = args.to_agent.lower()

    for name in [from_agent, to_agent]:
        if name not in AGENTS:
            print(f"ERROR: Unknown agent '{name}'. Choose from: {', '.join(AGENTS.keys())}")
            sys.exit(1)

    title = f"[{from_agent.upper()}→{to_agent.upper()}] {args.title}"
    labels = f"agent-task,handoff,{AGENTS[to_agent]['label']}"

    body = f"""## Context
Handoff from {from_agent.upper()} to {to_agent.upper()}.

## Task
{args.title}

## Key Files
<!-- Add relevant file paths -->

## Gotchas
<!-- Add any warnings -->

## Notes
Created: {datetime.now(timezone.utc).isoformat()}
"""

    output = run_gh([
        "issue", "create", "--repo", REPO,
        "--title", title,
        "--label", labels,
        "--body", body,
    ])

    print(f"✅ Handoff created ({from_agent.upper()} → {to_agent.upper()}): {output}")


def cmd_health(args):
    """Run system health checks."""
    print("🩺 SYSTEM HEALTH CHECK")
    print("=" * 60)
    issues_found = 0

    # 1. Check gh auth
    print("\n1. GitHub CLI authentication...")
    auth = run_gh(["auth", "status"], check=False)
    if "Logged in" in auth or "✓" in auth:
        print("   ✅ Authenticated")
    else:
        print("   ❌ Not authenticated — run `gh auth login`")
        issues_found += 1

    # 2. Check labels
    print("\n2. GitHub labels...")
    label_output = run_gh(["label", "list", "--repo", REPO, "--json", "name"])
    if label_output:
        try:
            existing = {l["name"] for l in json.loads(label_output)}
            for label in REQUIRED_LABELS:
                if label in existing:
                    print(f"   ✅ {label}")
                else:
                    print(f"   ❌ Missing: {label}")
                    issues_found += 1
        except json.JSONDecodeError:
            print("   ⚠️  Could not parse label list")

    # 3. Check issue templates
    print("\n3. Issue templates...")
    template_dir = SCRIPT_DIR.parent / ".github" / "ISSUE_TEMPLATE"
    expected_templates = ["agent-task.md", "agent-handoff.md", "directive.md"]
    for tmpl in expected_templates:
        path = template_dir / tmpl
        if path.exists():
            print(f"   ✅ {tmpl}")
        else:
            print(f"   ❌ Missing: {tmpl}")
            issues_found += 1

    # 4. Check status files
    print("\n4. Agent status files...")
    status_dir = COMMS_DIR / "status"
    for agent_name in AGENTS:
        sf = status_dir / f"{agent_name}.json"
        if sf.exists():
            try:
                data = json.loads(sf.read_text())
                ts = data.get("timestamp", data.get("lastActive", ""))
                if ts:
                    print(f"   ✅ {agent_name}.json (updated: {ts[:10]})")
                else:
                    print(f"   ⚠️  {agent_name}.json (no timestamp)")
            except json.JSONDecodeError:
                print(f"   ❌ {agent_name}.json — invalid JSON")
                issues_found += 1
        else:
            print(f"   ❌ {agent_name}.json — missing")
            issues_found += 1

    # 5. Check stale issues (open > 7 days with no update)
    print("\n5. Stale issues (open > 7 days)...")
    stale_output = run_gh([
        "issue", "list", "--label", "agent-task", "--state", "open",
        "--repo", REPO, "--json", "number,title,updatedAt",
    ])
    if stale_output:
        try:
            stale_issues = json.loads(stale_output)
            now = datetime.now(timezone.utc)
            for issue in stale_issues:
                updated = datetime.fromisoformat(issue["updatedAt"].replace("Z", "+00:00"))
                age = (now - updated).days
                if age > 7:
                    print(f"   ⚠️  #{issue['number']} ({age}d old): {issue['title'][:50]}")
                    issues_found += 1
            if not any((now - datetime.fromisoformat(i["updatedAt"].replace("Z", "+00:00"))).days > 7 for i in stale_issues):
                print("   ✅ No stale issues")
        except (json.JSONDecodeError, ValueError):
            pass
    else:
        print("   ✅ No open agent tasks")

    # 6. Check directives
    print("\n6. Active directives...")
    dir_path = COMMS_DIR / "directives"
    if dir_path.exists():
        directives = [f for f in dir_path.iterdir() if f.suffix == ".md" and f.name != "README.md"]
        for d in sorted(directives):
            print(f"   📡 {d.name}")
    else:
        print("   ⚠️  No directives directory")

    # Summary
    print(f"\n{'=' * 60}")
    if issues_found == 0:
        print("✅ ALL SYSTEMS NOMINAL")
    else:
        print(f"⚠️  {issues_found} issue(s) found — review above")
    print(f"{'=' * 60}")


def cmd_logs(args):
    """Show recent starfleet log entries."""
    logs_dir = COMMS_DIR / "starfleet-logs"
    if not logs_dir.exists():
        print("⚠️  No starfleet-logs directory")
        return

    log_files = sorted(logs_dir.glob("*.md"), reverse=True)
    count = min(args.count, len(log_files))

    if not log_files:
        print("No starfleet log entries.")
        return

    print(f"📒 RECENT STARFLEET LOGS (showing {count} of {len(log_files)})")
    print("=" * 60)

    for log_file in log_files[:count]:
        content = log_file.read_text()
        print(f"\n{'─' * 40}")
        # Show first 20 lines as preview
        lines = content.strip().split("\n")
        for line in lines[:20]:
            print(f"  {line}")
        if len(lines) > 20:
            print(f"  ... ({len(lines) - 20} more lines)")

    print(f"\n{'=' * 60}")


def cmd_search(args):
    """Fast search using git grep across the repository."""
    print(f"🔍 Searching for '{args.query}'...")
    try:
        result = subprocess.run(
            ["git", "grep", "-inI", args.query],
            cwd=SCRIPT_DIR.parent,
            capture_output=True, text=True
        )
        if result.stdout:
            print(result.stdout)
        else:
            print("No results found.")
    except Exception as e:
        print(f"Search error: {e}")


def cmd_email(args):
    """Send an email using the admin-tool send_email script."""
    print(f"📧 Sending email to {args.to}...")
    email_script = SCRIPT_DIR.parent / "projects/admin-tool/scripts/utils/send_email.py"
    if not email_script.exists():
        print(f"❌ Error: {email_script} not found.")
        return

    cmd = [
        sys.executable, str(email_script),
        "--to", args.to,
        "--subject", args.subject,
        "--body", args.body
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to send email.")


def cmd_write(args):
    """Safely write content to a file, replacing it entirely."""
    file_path = Path(args.path)
    try:
        print(f"📝 Writing to {file_path}...")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(args.content)
        print(f"✅ Successfully wrote to {file_path}")
    except Exception as e:
        print(f"❌ Failed to write file: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="🛸 NeuroArts Agent System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  status     Show all agent statuses
  tasks      List open GitHub Issues for agents
  assign     Create a task for an agent
  handoff    Create a cross-agent handoff
  health     Run system health checks
  logs       View recent starfleet logs
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # status
    subparsers.add_parser("status", help="Show agent statuses")

    # tasks
    subparsers.add_parser("tasks", help="List open agent tasks")

    # assign
    assign_parser = subparsers.add_parser("assign", help="Create a task for an agent")
    assign_parser.add_argument("agent", help="Agent name (nexus, cortex, prism, beacon, bridge)")
    assign_parser.add_argument("title", help="Task description")

    # handoff
    handoff_parser = subparsers.add_parser("handoff", help="Create an agent handoff")
    handoff_parser.add_argument("from_agent", help="Source agent")
    handoff_parser.add_argument("to_agent", help="Target agent")
    handoff_parser.add_argument("title", help="Handoff description")

    # health
    subparsers.add_parser("health", help="System health check")

    # logs
    logs_parser = subparsers.add_parser("logs", help="View starfleet logs")
    logs_parser.add_argument("-n", "--count", type=int, default=3, help="Number of logs to show")

    # search
    search_parser = subparsers.add_parser("search", help="Fast repository-wide search")
    search_parser.add_argument("query", help="Text to search for")

    # email
    email_parser = subparsers.add_parser("email", help="Send an email")
    email_parser.add_argument("--to", required=True, help="Recipient email address")
    email_parser.add_argument("--subject", required=True, help="Email subject line")
    email_parser.add_argument("--body", required=True, help="HTML body content")

    # write
    write_parser = subparsers.add_parser("write", help="Safely rewrite a file")
    write_parser.add_argument("path", help="Path to file")
    write_parser.add_argument("content", help="Content to write")

    args = parser.parse_args()

    commands = {
        "status": cmd_status,
        "tasks": cmd_tasks,
        "assign": cmd_assign,
        "handoff": cmd_handoff,
        "health": cmd_health,
        "logs": cmd_logs,
        "search": cmd_search,
        "email": cmd_email,
        "write": cmd_write,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
