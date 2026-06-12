#!/bin/zsh
# Sequoia-X 全表同步脚本
# 用法: ./scripts/sync_all.sh [YYYYMMDD]

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATE="${1:-$(date +%Y%m%d)}"
LOG_FILE="$PROJECT_DIR/logs/sync-all-$DATE.log"
mkdir -p "$PROJECT_DIR/logs"
cd "$PROJECT_DIR"

# 生成表名列表到临时文件
TMPFILE=$(mktemp)
.venv/bin/python -c "
import os; os.environ['RICH_NO_COLOR'] = '1'
import logging; logging.disable(logging.CRITICAL)
from sequoia_x.data.engine import DataEngine
from sequoia_x.core.config import get_settings
for t in sorted(DataEngine(get_settings())._TABLE_API_MAP.keys()): print(t)
" 2>/dev/null > "$TMPFILE"

total=$(wc -l < "$TMPFILE" | tr -d ' ')
echo "==========================================" | tee -a "$LOG_FILE"
echo "  Sequoia-X 全表同步  日期: $DATE  共 $total 张表" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

i=0; ok=0; fail=0
while IFS= read -r table; do
    ((i++))
    start=$(date +%s)
    echo -n "[$i/$total] $table ... "
    echo "[$i/$total] $table ... " >> "$LOG_FILE"

    output=$(.venv/bin/python main.py --sync-table "$table" --date "$DATE" 2>&1)
    rc=$?
    elapsed=$(($(date +%s) - start))

    # 提取结果摘要
    summary="$(echo "$output" | sed -n 's/.*写入 \([0-9]*\) 条.*/写入 \1/p')"
    [ -z "$summary" ] && summary="$(echo "$output" | sed -n 's/.*无数据.*/无数据/p')"
    [ -z "$summary" ] && summary="写入 0"

    if [ $rc -eq 0 ]; then
        echo "$summary (${elapsed}s)"
        echo "$summary (${elapsed}s)" >> "$LOG_FILE"
        ((ok++))
    else
        echo "异常退出 (${elapsed}s)"
        echo "异常退出 (${elapsed}s)" >> "$LOG_FILE"
        ((fail++))
    fi
    sleep 0.3
done < "$TMPFILE"
rm -f "$TMPFILE"

echo "" | tee -a "$LOG_FILE"
echo "完成: 成功 $ok / 失败 $fail / 总计 $total" | tee -a "$LOG_FILE"
