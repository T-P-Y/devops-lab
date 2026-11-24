#!/bin/bash

DATE=$(date +%Y-%m-%d_%H-%M)
BACKUP_DIR="$HOME/backups"
SOURCE_DIR="$HOME/devops_lab"
LOG_FILE="$BACKUP_DIR/status.log"

# 1. Создаем сжатый архив рабочей папки
tar -czf "$BACKUP_DIR/lab_backup_$DATE.tar.gz" "$SOURCE_DIR" 2>/dev/null

# 2. Проверяем, работает ли Nginx
if systemctl is-active --quiet nginx; then
    STATUS="OK: Nginx работает"
else
    STATUS="ALERT: Nginx остановлен!"
fi

# 3. Собираем метрики диска и памяти
FREE_DISK=$(df -h / | awk 'NR==2 {print $4}')
FREE_RAM=$(free -h | awk 'NR==2 {print $7}')

# 4. Записываем полный отчет в лог
echo "[$DATE] Бэкап создан | $STATUS | Диск свободно: $FREE_DISK | ОЗУ доступно: $FREE_RAM" >> "$LOG_FILE"
