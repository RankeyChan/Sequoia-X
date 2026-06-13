#!/bin/zsh
# Sequoia-X MySQL 同步脚本
# 用法:
#   ./scripts/sync_all.sh                       # 同步所有表
#   ./scripts/sync_all.sh daily                 # 同步单表 (ts_daily)
#   ./scripts/sync_all.sh daily moneyflow       # 同步多表
#   ./scripts/sync_all.sh --date 20260612 daily # 指定日期同步

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# ── 参数解析 ──
DATE=""
TABLES=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --date) DATE="$2"; shift 2 ;;
        -h|--help)
            echo "用法:"
            echo "  $0                         同步所有表"
            echo "  $0 <table> [table...]      同步指定表 (如 daily moneyflow)"
            echo "  $0 --date YYYYMMDD [table] 指定日期同步"
            exit 0
            ;;
        *) TABLES+=("$1"); shift ;;
    esac
done
DATE="${DATE:-$(date +%Y%m%d)}"

LOG_FILE="$PROJECT_DIR/logs/sync-$DATE.log"
mkdir -p "$PROJECT_DIR/logs"
cd "$PROJECT_DIR"

# ── 获取表列表 ──
if [[ ${#TABLES} -eq 0 ]]; then
    # 无参数：从 MySQL 获取所有 ts_ 表
    TMPFILE=$(mktemp)
    mysql -u root -h 127.0.0.1 tushare -N \
        -e "SELECT TABLE_NAME FROM information_schema.tables WHERE table_schema='tushare' AND TABLE_NAME LIKE 'ts_%' ORDER BY TABLE_NAME;" \
        2>/dev/null > "$TMPFILE"
    while IFS= read -r t; do
        TABLES+=("$t")
    done < "$TMPFILE"
    rm -f "$TMPFILE"
else
    # 自动补 ts_ 前缀：daily → ts_daily
    NORMALIZED=()
    for t in "${TABLES[@]}"; do
        [[ "$t" != ts_* ]] && t="ts_$t"
        NORMALIZED+=("$t")
    done
    TABLES=("${NORMALIZED[@]}")
fi

total=${#TABLES}

echo "==========================================" | tee -a "$LOG_FILE"
echo "  Sequoia-X MySQL 同步  日期: $DATE  共 $total 张表" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

((total == 0)) && { echo "  无表需同步"; exit 0; }

i=0; ok=0; fail=0
for table in "${TABLES[@]}"; do
    ((i++))
    start=$(date +%s)
    echo -n "[$i/$total] $table ... "
    echo "[$i/$total] $table ... " >> "$LOG_FILE"

    output=$(.venv/bin/python main.py --sync-table "$table" --date "$DATE" 2>&1)
    rc=$?
    elapsed=$(($(date +%s) - start))

    # 提取写入行数或"无数据"
    summary="$(echo "$output" | sed -n 's/.*写入 \([0-9]*\) 条.*/写入 \1/p')"
    [ -z "$summary" ] && summary="$(echo "$output" | sed -n 's/.*无数据.*/无数据/p')"
    [ -z "$summary" ] && summary="写入 0"

    if [[ $rc -eq 0 ]]; then
        echo "$summary (${elapsed}s)"
        echo "$summary (${elapsed}s)" >> "$LOG_FILE"
        ((ok++))
    else
        echo "异常退出 (${elapsed}s)"
        echo "异常退出 (${elapsed}s)" >> "$LOG_FILE"
        echo "$output" | tail -3 >> "$LOG_FILE"
        ((fail++))
    fi
    sleep 0.3
done

echo "" | tee -a "$LOG_FILE"
echo "完成: 成功 $ok / 失败 $fail / 总计 $total" | tee -a "$LOG_FILE"
