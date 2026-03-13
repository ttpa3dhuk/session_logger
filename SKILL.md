---
name: session-logger
description: Maintain persistent session memory across restarts. Appends messages to a SESSION-MEMORY.md file with automatic rotation (keeps last N messages). Use after every user message and agent response to log conversation context. Triggers on session logging, memory persistence, context recovery, session continuity, or when asked to "log this", "remember this exchange", or ensure conversation survives restarts.
---

# Session Logger

Lightweight session continuity via file-based message logging with rotation.

## How It Works

A Python script appends timestamped messages to `SESSION-MEMORY.md` and rotates old entries (default: 10 messages). Zero API cost — runs entirely locally.

## Usage

### Log a message

```bash
python3 SKILL_DIR/scripts/log-session.py "<role>" "<message>"
```

- `role`: e.g. `🧑 User` or `🤖 Agent`
- `message`: brief summary of the exchange

### After /new or restart

Read `SESSION-MEMORY.md` to recover conversation context. The file contains the last N exchanges with timestamps.

## Setup

Zero config needed. Default file: `~/.openclaw/workspace/SESSION-MEMORY.md`

Optional env vars:
- `SESSION_LOG_FILE` — custom path (e.g. Obsidian vault)
- `SESSION_MAX_MSGS` — rotation size (default: 10)

File is auto-created on first run with proper template.

### Integration steps

1. Add to agent startup: read the log file before responding
2. Add to agent response loop: call script after each exchange

## File Format

```markdown
## Последние сообщения

**[HH:MM]** 🧑 User: что-то сказал
**[HH:MM]** 🤖 Agent: что-то ответил

## Текущий контекст

- Key state info
- Active tasks
```

## Critical: Log Before Responding

The #1 failure mode is forgetting to log. Follow this order strictly:

1. **Received message** → log immediately (`🧑 User: ...`)
2. **Process and respond**
3. **Response sent** → log immediately (`🤖 Agent: ...`)

Never defer logging to "the end of the turn" — it will be forgotten.

## Tips

- Keep messages brief — summaries, not transcripts
- Log both sides (user + agent) for full context
- The script is idempotent — safe to call multiple times
- Add a checklist reminder to agent instructions: "Response not complete until logged"
