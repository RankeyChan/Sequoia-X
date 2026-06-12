#!/bin/zsh
# Sequoia-X 日常运行脚本（由 launchd 定时触发）
# 日志输出到 logs/ 目录，按日期命名

set -e

PROJECT_DIR="/Library/Repository/github/Sequoia-X"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"
LOG_DIR="$PROJECT_DIR/logs"
TODAY=$(date +%Y-%m-%d)

cd "$PROJECT_DIR"

echo "========================================"
echo "  Sequoia-X 定时任务启动"
echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# 当日日志
LOG_FILE="$LOG_DIR/daily-$TODAY.log"

$VENV_PYTHON main.py >> "$LOG_FILE" 2>&1

EXIT_CODE=$?
echo "退出码: $EXIT_CODE" >> "$LOG_FILE"

# 保留最近 60 天日志
find "$LOG_DIR" -name "daily-*.log" -mtime +60 -delete 2>/dev/null
