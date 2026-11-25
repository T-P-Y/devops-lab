# Linux & DevOps Infrastructure Lab

![CI Status](https://github.com)

Практический стенд и набор инфраструктурных конфигураций для администрирования Linux-серверов, контейнеризации, мониторинга и автоматизации.

## Структура репозитория

* **`scripts/backup_and_check.sh`** — Bash-скрипт для резервного копирования рабочих директорий (`tar`), снятия дампов PostgreSQL (`pg_dump`) и мониторинга состояния Nginx, свободного места на диске и доступной ОЗУ.
* **`nginx/`** — конфигурации веб-сервера Nginx: настройка обратного прокси (`Reverse Proxy`), принудительный редирект `HTTP -> HTTPS` (301) и работа с SSL-сертификатами на 443 порту.
* **`docker/`** — многоконтейнерная связка `Nginx + Redis` в Docker Compose с пробросом локальных томов в режиме `read-only`.
* **`monitoring/`** — стек визуального мониторинга метрик сервера на базе `Prometheus + Node Exporter + Grafana`.
* **`.github/workflows/ci-checks.yml`** — автоматический CI-пайплайн в GitHub Actions для проверки синтаксиса Bash-скриптов (`ShellCheck`), YAML-манифестов Docker Compose и конфигов Nginx.

## Стек технологий
* **OS & Shell:** Ubuntu Linux (WSL2), Zsh, Bash, Cron
* **Web & Security:** Nginx, OpenSSL, SSH (ed25519), UFW
* **Containers & DB:** Docker, Docker Compose, PostgreSQL, Redis
* **Monitoring & CI/CD:** Prometheus, Node Exporter, Grafana, Git, GitHub Actions
