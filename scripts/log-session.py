#!/usr/bin/env python3
"""log-session.py — Append message to SESSION-MEMORY.md with rotation + daily log.

Usage:
    log-session.py "<role>" "<message>"
    log-session.py "🧑 User" "some question"
    log-session.py "🤖 Agent" "some answer"

Environment:
    SESSION_LOG_FILE  — custom path to session file (default: ~/.openclaw/workspace/SESSION-MEMORY.md)
    SESSION_MAX_MSGS  — max messages to keep (default: 10)
    DAILY_LOG_DIR     — daily log directory (default: ~/.openclaw/workspace/memory)
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path

DEFAULT_FILE = Path.home() / ".openclaw/workspace/SESSION-MEMORY.md"
SESSION_FILE = Path(os.environ.get("SESSION_LOG_FILE", str(DEFAULT_FILE)))
MAX_MESSAGES = int(os.environ.get("SESSION_MAX_MSGS", "10"))

TEMPLATE = """# SESSION-MEMORY.md — Persistent session memory

> Auto-rotated: keeps last {max} messages.
> Logged after each exchange to survive restarts.
> Read this file after /new or /reset to recover context.

---

## Последние сообщения

## Текущий контекст

- **Session:** {date}
- **Status:** active
""".format(max=MAX_MESSAGES, date=datetime.now().strftime("%Y-%m-%d"))

if len(sys.argv) < 3:
    print("Usage: log-session.py <role> <message>")
    print("  e.g: log-session.py '🧑 User' 'hello'")
    sys.exit(1)

role = sys.argv[1]
msg = " ".join(sys.argv[2:])
time_str = datetime.now().strftime("%H:%M")
entry = f"**[{time_str}]** {role}: {msg}"

# Create file with template if missing
if not SESSION_FILE.exists():
    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    SESSION_FILE.write_text(TEMPLATE)

content = SESSION_FILE.read_text()

# Insert after "## Последние сообщения\n\n"
pattern = r'(## Последние сообщения\n\n)'
match = re.search(pattern, content)
if not match:
    print("❌ No '## Последние сообщения' section found")
    sys.exit(1)

insert_pos = match.end()
before = content[:insert_pos]
after = content[insert_pos:]

# Insert new message first
new_content = before + entry + "\n" + after

# Rotate: keep only MAX_MESSAGES
context_match = re.search(r'\n(## Текущий контекст)', after)
if context_match:
    msgs_text = after[:context_match.start()]
    context_text = after[context_match.start():]

    messages = re.findall(r'\*\*\[.*?\]\*\* .*', msgs_text)
    messages = [entry] + [m for m in messages if m != entry]
    messages = messages[:MAX_MESSAGES]

    new_content = before + "\n".join(messages) + "\n" + context_text

SESSION_FILE.write_text(new_content)
print(f"✅ [{time_str}] {role}")

# --- Daily log: append to memory/YYYY-MM-DD.md (no rotation) ---
DAILY_DIR = Path(os.environ.get("DAILY_LOG_DIR", str(Path.home() / ".openclaw/workspace/Obsidian/Logs")))
daily_file = DAILY_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"
daily_entry = f"[{time_str}] {role}: {msg}\n"

DAILY_DIR.mkdir(parents=True, exist_ok=True)

if not daily_file.exists():
    daily_file.write_text(f"# 📒 {datetime.now().strftime('%Y-%m-%d')} — Daily Log\n\n")
with open(daily_file, "a") as f:
    f.write(daily_entry)
