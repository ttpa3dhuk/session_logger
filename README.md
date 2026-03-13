# session-logger

**Persistent session memory for AI agents.**

Survive restarts, crashes, and `/new` commands. Zero API cost. One Python script.

## The Problem

AI agents forget everything after a restart. Context is lost. You explain things again. And again.

## The Solution

A lightweight script that logs every exchange to a file. On startup, the agent reads the log and picks up right where you left off.

## What You Get

- **Context recovery** — agent remembers after any restart
- **Zero token cost** — runs locally on Python, no API calls
- **Auto-rotation** — keeps last N messages, file stays small
- **Zero config** — works out of the box, file auto-created
- **Any channel** — Telegram, Discord, WhatsApp, Slack, Signal
- **~50 lines** — easy to read, easy to trust

## Installation

### As an OpenClaw Skill

```bash
clawhub install session-logger
```

### Manual

```bash
# Download the script
curl -O https://raw.githubusercontent.com/ttpa3dhuk/session_logger/main/scripts/log-session.py
chmod +x log-session.py
```

No dependencies beyond Python 3.6+.

## Usage

### Log a message

```bash
./log-session.py "User" "hello"
./log-session.py "Agent" "hi there!"
```

### Read the log

The log file is plain markdown. Read it on agent startup to recover context:

```
**[12:34]** User: hello
**[12:34]** Agent: hi there!
```

### Configure your agent

Add to agent instructions:

1. **On startup** — read the log file
2. **On each exchange** — call the script to log messages

#### Critical: Log Before Responding

The #1 failure mode is forgetting to log. Follow this order:

1. Message arrives → log immediately
2. Process and respond
3. Response sent → log immediately

## Options

| Env Variable | Default | Description |
|---|---|---|
| `SESSION_LOG_FILE` | `~/.openclaw/workspace/SESSION-MEMORY.md` | Path to log file |
| `SESSION_MAX_MSGS` | `10` | Messages to keep |

```bash
# Example: use custom path
SESSION_LOG_FILE="/path/to/my/log.md" ./log-session.py "User" "hello"
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `No Python 3` | Install Python 3.6+: `brew install python3` or `apt install python3` |
| `Permission denied` | Make path writable: `chmod +w ~/path/` |
| `Missing sections` | Delete the file — script creates a new one automatically |
| `Path does not exist` | Script creates folders automatically (mkdir -p) |
| Agent skips the log | Add log reading to agent startup instructions |

## Works With

Any AI agent framework that supports custom scripts:
- OpenClaw
- Custom GPT agents
- Any LLM with tool-use capabilities

## License

MIT

## Links

- [OpenClaw](https://openclaw.ai)
- [ClawHub Skills](https://clawhub.com)
