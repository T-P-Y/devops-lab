#!/bin/bash

DATE=$(date +%Y-%m-%d_%H-%M)
BACKUP_DIR="$HOME/backups"
SOURCE_DIR="$HOME/devops_lab"
LOG_FILE="$BACKUP_DIR/status.log"

# 1. Бэкап рабочих файлов
tar -czf "$BACKUP_DIR/lab_backup_$DATE.tar.gz" "$SOURCE_DIR" 2>/dev/null

# 2. Бэкап базы данных PostgreSQL (если контейнер запущен)
if docker ps --format '{{.Names}}' | grep -q "^my_postgres$"; then
    docker exec my_postgres pg_dump -U admin app_db | gzip > "$BACKUP_DIR/db_backup_$DATE.sql.gz"
    DB_STATUS="DB: OK"
else
    DB_STATUS="DB: SKIP"
fi

# 3. Проверка Nginx и ресурсов
if systemctl is-active --quiet nginx; then
    NG_STATUS="Nginx: OK"
else
    NG_STATUS="Nginx: ALERT"
fi

FREE_DISK=$(df -h / | awk 'NR==2 {print $4}')
FREE_RAM=$(free -h | awk 'NR==2 {print $7}')

echo "[$DATE] Бэкап готов | $NG_STATUS | $DB_STATUS | Диск: $FREE_DISK | ОЗУ: $FREE_RAM" >> "$LOG_FILE"
