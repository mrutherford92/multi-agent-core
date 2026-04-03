#!/usr/bin/env python3
"""
agent_tools.py — Syndicate Multi-Agent System CLI (Firestore Edition)

Manage the agent communication system from the command line.
Uses Firebase Firestore for global task management (No GH Token Needed).
"""
import argparse
import json
import subprocess
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print("ERROR: firebase-admin not installed. Run 'pip install firebase-admin'")
    sys.exit(1)

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

def get_db():
    try:
        app = firebase_admin.get_app()
    except ValueError:
        # Check local path for development vs ambient GCP auth (Cloud Run)
        cred_path = os.path.expanduser("~/vocalbrain-adminsdk.json")
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {"projectId": "vocalbrain-web"})
        else:
            firebase_admin.initialize_app({"projectId": "vocalbrain-web"})
    return firestore.client()


def cmd_status(args):
    db = get_db()
    print("=" * 60)
    print("🛸 NEUROARTS CREW STATUS")
    print("=" * 60)

    status_dir = COMMS_DIR / "status"
    for agent_name, info in AGENTS.items():
        status_file = status_dir / f"{agent_name}.json"
        print(f"\n{'─' * 40}")
        print(f"{agent_name.upper()} — {info['role']}")

        if status_file.exists():
            try:
                data = json.loads(status_file.read_text())
                status = data.get("status", "unknown")
                last_task = data.get("lastTask", "N/A")
                print(f"  Status: {status}")
                print(f"  Last task: {last_task[:80]}")
            except Exception:
                print("  ⚠️  Invalid status JSON")
        
        # Poll Firestore for agent tasks
        tasks = db.collection('agent_tasks').where('labels', 'array_contains', info['label']).where('state', '==', 'open').get()
        if len(tasks) > 0:
            print(f"  📋 {len(tasks)} open Firestore task(s)")

    print(f"\n{'=' * 60}")


def cmd_tasks(args):
    db = get_db()
    print("📋 OPEN AGENT TASKS (FIRESTORE)")
    print("=" * 60)

    tasks_ref = db.collection('agent_tasks').where('state', '==', 'open').get()
    
    if not tasks_ref:
        print("\nNo open agent tasks in Firestore.")
        return

    for doc in tasks_ref:
        task = doc.to_dict()
        labels = ", ".join(task.get('labels', []))
        print(f"\n  #{doc.id[:6]}: {task.get('title', 'Unknown')}")
        print(f"    Labels: {labels}")
        print(f"    Updated: {task.get('updatedAt', 'Unknown')[:10]}")
    print(f"\n{'=' * 60}")


def cmd_assign(args):
    db = get_db()
    agent = args.agent.lower()
    if agent not in AGENTS:
        print(f"ERROR: Unknown agent '{agent}'.")
        sys.exit(1)

    now = datetime.now(timezone.utc).isoformat()
    db.collection('agent_tasks').add({
        "title": f"[{agent.upper()}] {args.title}",
        "body": f"Created via Firestore Link.\n\nOrders: {args.title}",
        "state": "open",
        "labels": ["agent-task", AGENTS[agent]['label']],
        "createdAt": now,
        "updatedAt": now
    })
    print(f"✅ Mission injected into Firestore for {agent.upper()}")


def cmd_handoff(args):
    db = get_db()
    from_agent, to_agent = args.from_agent.lower(), args.to_agent.lower()
    
    now = datetime.now(timezone.utc).isoformat()
    db.collection('agent_tasks').add({
        "title": f"[{from_agent.upper()}→{to_agent.upper()}] {args.title}",
        "body": f"Handoff from {from_agent.upper()} to {to_agent.upper()}.\n\n{args.title}",
        "state": "open",
        "labels": ["agent-task", "handoff", AGENTS[to_agent]['label']],
        "createdAt": now,
        "updatedAt": now
    })
    print(f"✅ Handoff injected into Firestore: {from_agent.upper()} → {to_agent.upper()}")


def cmd_health(args):
    print("🩺 FIRESTORE SYSTEM HEALTH CHECK")
    print("=" * 60)
    try:
        db = get_db()
        # Test connection
        db.collection('agent_tasks').limit(1).get()
        print("   ✅ Firestore connection authenticated!")
    except Exception as e:
        print(f"   ❌ Firestore Error: {e}")
    print(f"\n{'=' * 60}")


# Add stubs for logs, search, email, write so integrations don't break
def cmd_logs(args):
    print("Log viewing available in IDE.")

def cmd_search(args):
    subprocess.run(["git", "grep", "-inI", args.query], cwd=SCRIPT_DIR.parent)

def cmd_write(args):
    Path(args.path).write_text(args.content)

def cmd_email(args):
    print("Command deprecated.")


def main():
    parser = argparse.ArgumentParser(description="🛸 Syndicate Firestore CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show agent statuses")
    subparsers.add_parser("tasks", help="List open tasks")
    
    assign_parser = subparsers.add_parser("assign", help="Create an agent task")
    assign_parser.add_argument("agent")
    assign_parser.add_argument("title")

    handoff_parser = subparsers.add_parser("handoff", help="Create handoff")
    handoff_parser.add_argument("from_agent")
    handoff_parser.add_argument("to_agent")
    handoff_parser.add_argument("title")

    subparsers.add_parser("health", help="System health check")
    
    # stubs
    logs = subparsers.add_parser("logs", help="logs")
    logs.add_argument("-n", "--count", type=int, default=3)
    
    search = subparsers.add_parser("search")
    search.add_argument("query")
    
    write = subparsers.add_parser("write")
    write.add_argument("path")
    write.add_argument("content")
    
    email = subparsers.add_parser("email")
    email.add_argument("--to")
    email.add_argument("--subject")
    email.add_argument("--body")

    args = parser.parse_args()

    commands = {
        "status": cmd_status,
        "tasks": cmd_tasks,
        "assign": cmd_assign,
        "handoff": cmd_handoff,
        "health": cmd_health,
        "logs": cmd_logs,
        "search": cmd_search,
        "write": cmd_write,
        "email": cmd_email,
    }
    commands[args.command](args)

if __name__ == "__main__":
    main()
