# 🛸 Inter-Agent Communications Hub

This directory serves as the **shared communication layer** between AI agents (Gemini, Antigravity, others), human operators, and the NeuroArts platform itself. It is the single source of truth for cross-agent coordination, handoffs, and progress tracking.

---

## 📂 Directory Structure

```
reference/inter-agent-comms/
├── README.md              ← You are here. The protocol.
├── crew-manifest.md       ← Full crew roster and roles
├── starfleet-logs/        ← Progress logs & cross-agent comms history
│   └── YYYY-MM-DD.md      ← Daily log entries
├── handoffs/              ← Agent-to-agent task handoff briefs
├── directives/            ← Standing orders & priorities from the captain
├── status/                ← Agent status files (JSON)
└── context/               ← Shared context snapshots for new agents joining
```

---

## 🔄 Communication Protocol

### Who Uses This

| Party | Role |
|-------|------|
| **Michael (Captain)** | Sets directives, reviews logs, issues orders |
| **Bridge** | Cross-project architect (Antigravity / VS Code) |
| **Cortex** | ML & data agent (admin-tool, includes ml/ classifier module) |
| **Nexus** | Mobile experience agent (neuro-arts-flutter) |
| **Prism** | Web experience agent (neuroarts-nextjs) |
| **Beacon** | Marketing & growth agent (public-web) |

### How It Works

1. **Before starting work**, an agent checks:
   - `directives/` — for any standing orders or priorities
   - `starfleet-logs/` — for the latest entry to understand recent progress
   - `status/` — for other agents' current state
   - `handoffs/` — for any pending tasks handed off by another agent

2. **During work**, agents update:
   - Their own log entry in `starfleet-logs/` with what they accomplished
   - Any `handoffs/` if they need another agent to pick up a task

3. **After completing work**, an agent writes:
   - A summary in `starfleet-logs/` with key decisions, blockers, and next steps
   - A `handoffs/` file if follow-up work is needed by a different agent or system
   - Updates their `status/` JSON file

4. **Michael** can:
   - Drop a new file in `directives/` to set priorities or issue orders
   - Review `starfleet-logs/` to see the full timeline of progress
   - Add notes to any log entry for agents to pick up

---

## 📒 Starfleet Logs

The `starfleet-logs/` directory is the **running record** of all progress, communications, and decisions across the NeuroArts project. Think of it as the ship's log.

### Log Entry Format

```markdown
# Starfleet Log — YYYY-MM-DD

## Agent: [Agent Name]
**Stardate**: [timestamp]
**Mission**: [brief description of what was worked on]

### Accomplishments
- What was completed

### Decisions Made
- Key design decisions and rationale

### Blockers & Issues
- What's stuck and why

### Handoffs
- Tasks that need another agent or Michael's attention

### Next Steps
- What should happen next
```

### Rules
- **One file per day**, multiple agents append to the same file
- **Newest entries at the top** within each file
- **Be specific** — link to files, mention function names, quote error messages
- **No assumptions** — if you're unsure, say so and flag for Michael

---

## 📋 Handoffs

When one agent needs another to pick up work:

```markdown
# Handoff: [Brief Title]

**From**: [Agent Name]
**To**: [Target Agent or "Any"]
**Date**: YYYY-MM-DD
**Priority**: 🔴 High | 🟡 Medium | 🟢 Low

## Context
[What was being worked on and why]

## Task
[Exactly what needs to be done]

## Key Files
- [links to relevant files]

## Gotchas
- [anything the receiving agent should watch out for]
```

---

## 📡 Directives

Standing orders from Michael. Agents should check this directory at the start of every session.

Format is freeform — Michael writes what he needs, agents follow.

---

## 🧠 Context Snapshots

When a new agent joins a session or needs to get up to speed quickly, a context snapshot provides:
- Current project state
- Active priorities
- Recent decisions
- Key files and their purposes

These are written by agents who have deep context, for the benefit of agents who don't yet.

---

## 📎 Related Resources
- `agent_instructions/` — Task-specific handoff documents (e.g., vocal analysis pipeline)
- `docs/multi-agent-system.md` — Full system documentation for humans and agents
