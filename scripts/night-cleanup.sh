#!/bin/bash
# Night Cleanup — архивация и ротация логов
# Запускать ночью (cron 3:30), 0 токенов

set -e

LOGS_DIR="$HOME/.openclaw/workspace/Obsidian/Logs"
ARCHIVE_DIR="$LOGS_DIR/archive"
LOG_PREFIX="[cleanup $(date +%Y-%m-%d_%H:%M)]"

mkdir -p "$ARCHIVE_DIR"

echo "$LOG_PREFIX === Night Cleanup ==="

# 1. Архивация daily logs старше 14 дней
echo "$LOG_PREFIX Архивация daily logs (>14 дней)..."
find "$LOGS_DIR" -name "20*.md" -mtime +14 ! -name "SESSION*" ! -name "HANDOFF*" -exec mv {} "$ARCHIVE_DIR/" \;
ARCHIVED=$(ls "$ARCHIVE_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "$LOG_PREFIX В архиве: $ARCHIVED файлов"

# 2. Удаление архивов старше 90 дней
echo "$LOG_PREFIX Удаление архивов (>90 дней)..."
find "$ARCHIVE_DIR" -name "*.md" -mtime +90 -delete 2>/dev/null || true

# 3. Ротация backup логов
if [ -f /tmp/backup.log ]; then
    BACKUP_LOG_SIZE=$(stat -f%z /tmp/backup.log 2>/dev/null || echo 0)
    if [ "$BACKUP_LOG_SIZE" -gt 1048576 ]; then  # >1MB
        mv /tmp/backup.log /tmp/backup.log.old
        echo "$LOG_PREFIX backup.log прокручен (>1MB)"
    fi
fi

# 4. Чистка старых локальных бэкапов (>7 дней) — на всякий случай
find "$HOME/backups" -name "*.tar.gz" -mtime +7 -delete 2>/dev/null || true

# 5. Итого
REMAINING=$(ls "$LOGS_DIR"/20*.md 2>/dev/null | wc -l | tr -d ' ')
echo "$LOG_PREFIX Daily logs в папке: $REMAINING"
echo "$LOG_PREFIX === ✅ Готово ==="
