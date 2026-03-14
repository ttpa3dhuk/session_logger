# session-logger

**Постоянная память для AI-агентов.**

Переживает рестарты, краши и команду `/new`. Ноль токенов. Один скрипт на Python.

---

## Проблема

AI-агенты забывают всё после рестарта. Контекст теряется. Приходится объяснять заново. И снова. И снова.

## Решение

Лёгкий скрипт, который записывает каждое сообщение в файл. При запуске агент читает лог и продолжает с того же места.

## Что вы получаете

- **Восстановление контекста** — агент помнит после любого рестарта
- **Ноль токенов** — работает локально на Python, без API-вызовов
- **Автоматическая ротация** — хранит последние N сообщений, файл не раздувается
- **Ноль настроек** — работает из коробки, файл создаётся автоматически
- **Любой канал** — Telegram, Discord, WhatsApp, Slack, Signal
- **~50 строк кода** — легко прочитать, легко доверять

## Установка

### Git clone (рекомендуется)

```bash
git clone https://github.com/ttpa3dhuk/session_logger.git
cd session_logger
chmod +x scripts/log-session.py
```

### Curl (только скрипт)

```bash
curl -O https://raw.githubusercontent.com/ttpa3dhuk/session_logger/main/scripts/log-session.py
chmod +x log-session.py
```

Зависимостей нет, только Python 3.6+.

## Использование

### Логировать сообщение

```bash
./log-session.py "User" "привет"
./log-session.py "Agent" "привет! чем помочь?"
```

### Читать лог

Файл лога — обычный markdown. Агент читает его при запуске:

```
**[12:34]** User: привет
**[12:34]** Agent: привет! чем помочь?
```

### Настроить агента

Добавь в инструкции агента:

1. **При запуске** — прочитать файл лога
2. **При каждом сообщении** — вызывать скрипт

#### Важно: логировать ДО ответа

Главная ошибка — забыть вызвать скрипт. Порядок строго такой:

1. Сообщение получено → сразу логировать
2. Думать и отвечать
3. Ответ отправлен → сразу логировать

## Дополнительно

### HANDOFF.md — передача контекста при компактификации

Создай `HANDOFF.md` рядом с логом. Настрой memoryFlush в конфиге агента:

```json
{
  "compaction": {
    "mode": "safeguard",
    "memoryFlush": {
      "enabled": true,
      "prompt": "Перед компактификацией запиши в HANDOFF.md: тему, решения, задачи, важные пути. Только факты."
    }
  }
}
```

### night-cleanup.sh — ночная архивация логов

```bash
cp scripts/night-cleanup.sh ~/.openclaw/scripts/
chmod +x ~/.openclaw/scripts/night-cleanup.sh
```

Cron (3:30 ночи):
```
30 3 * * * ~/.openclaw/scripts/night-cleanup.sh >> /tmp/cleanup.log 2>&1
```

Архивирует daily logs старше 14 дней, удаляет старше 90 дней.

## Настройки

| Переменная | По умолчанию | Описание |
|---|---|---|
| `SESSION_LOG_FILE` | `~/.openclaw/workspace/SESSION-MEMORY.md` | Путь к файлу лога |
| `SESSION_MAX_MSGS` | `10` | Сколько сообщений хранить |
| `DAILY_LOG_DIR` | `~/.openclaw/workspace/memory` | Папка для daily логов (YYYY-MM-DD.md) |

```bash
SESSION_LOG_FILE="/path/to/log.md" ./log-session.py "User" "привет"
```

## Проблемы и решения

| Проблема | Решение |
|---|---|
| `No Python 3` | Установить Python 3.6+: `brew install python3` или `apt install python3` |
| `Permission denied` | `chmod +w ~/path/` или запустить от своего пользователя |
| Нет секций в файле | Удалить файл — скрипт создаст новый автоматически |
| Путь не существует | Скрипт создаёт папки сам (mkdir -p) |
| Агент не читает лог | Добавить чтение файла в инструкции агента |

## Совместимость

Любой AI-агент с поддержкой скриптов:
- OpenClaw
- Custom GPT агенты
- Любые LLM с tool-use

## Лицензия

MIT

---

# English

**Persistent session memory for AI agents.**

Survives restarts, crashes, and `/new` commands. Zero API cost. One Python script.

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

### Git clone (recommended)

```bash
git clone https://github.com/ttpa3dhuk/session_logger.git
cd session_logger
chmod +x scripts/log-session.py
```

### Curl (script only)

```bash
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

## Extras

### HANDOFF.md — context transfer on compaction

Create `HANDOFF.md` next to your log. Configure memoryFlush in agent config:

```json
{
  "compaction": {
    "mode": "safeguard",
    "memoryFlush": {
      "enabled": true,
      "prompt": "Before compaction, write to HANDOFF.md: topic, decisions, tasks, important paths. Facts only."
    }
  }
}
```

### night-cleanup.sh — nightly log archival

```bash
cp scripts/night-cleanup.sh ~/.openclaw/scripts/
chmod +x ~/.openclaw/scripts/night-cleanup.sh
```

Cron (3:30 AM):
```
30 3 * * * ~/.openclaw/scripts/night-cleanup.sh >> /tmp/cleanup.log 2>&1
```

Archives daily logs older than 14 days, deletes older than 90 days.

## Options

| Env Variable | Default | Description |
|---|---|---|
| `SESSION_LOG_FILE` | `~/.openclaw/workspace/SESSION-MEMORY.md` | Path to log file |
| `SESSION_MAX_MSGS` | `10` | Messages to keep |
| `DAILY_LOG_DIR` | `~/.openclaw/workspace/memory` | Directory for daily logs (YYYY-MM-DD.md) |

```bash
SESSION_LOG_FILE="/path/to/log.md" ./log-session.py "User" "hello"
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `No Python 3` | Install Python 3.6+: `brew install python3` or `apt install python3` |
| `Permission denied` | Make path writable: `chmod +w ~/path/` |
| `Missing sections` | Delete the file — script creates a new one automatically |
| `Path does not exist` | Script creates folders automatically (mkdir-p) |
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
