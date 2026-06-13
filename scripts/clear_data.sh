#!/bin/zsh
# Sequoia-X 清空所有 MySQL 表数据
# 用法: ./scripts/clear_data.sh
#
# 连接参数默认值同 sequoia_x/core/config.py，可通过环境变量覆盖:
#   MYSQL_HOST  MYSQL_PORT  MYSQL_USER  MYSQL_PASSWORD  MYSQL_DATABASE

# ── 连接参数 ──
HOST="${MYSQL_HOST:-127.0.0.1}"
PORT="${MYSQL_PORT:-3306}"
USER="${MYSQL_USER:-root}"
PASS="${MYSQL_PASSWORD:-}"
DB="${MYSQL_DATABASE:-tushare}"

MYSQL_OPTS=(-u "$USER" -h "$HOST" -P "$PORT" --batch --skip-column-names)
[[ -n "$PASS" ]] && MYSQL_OPTS+=("-p$PASS")

mysql_cmd() {
    mysql "${MYSQL_OPTS[@]}" "$DB" -e "$1" 2>&1
}

echo "=========================================="
echo "  Sequoia-X 清空所有 MySQL 表数据"
echo "  DB: $DB ($USER@$HOST:$PORT)"
echo "=========================================="

# ── 检查连接 ──
if ! mysql "${MYSQL_OPTS[@]}" -e "SELECT 1;" &>/dev/null; then
    echo "❌ 无法连接 MySQL，请检查连接参数"
    echo "   环境变量: MYSQL_HOST MYSQL_PORT MYSQL_USER MYSQL_PASSWORD MYSQL_DATABASE"
    exit 1
fi

# ── 获取所有 ts_ 表 ──
tables=$(mysql_cmd "SELECT TABLE_NAME FROM information_schema.tables WHERE table_schema='$DB' AND TABLE_NAME LIKE 'ts_%' ORDER BY TABLE_NAME;")

if [[ -z "$tables" ]]; then
    echo "  库中没有 ts_ 表，无需清理"
    exit 0
fi

# ── 清空所有表 ──
mysql_cmd "SET FOREIGN_KEY_CHECKS = 0;"
total=0 count=0

for table in ${(f)tables}; do
    deleted=$(mysql_cmd "SELECT COUNT(*) FROM \`$table\`;" 2>/dev/null)
    if [[ -n "$deleted" && "$deleted" -gt 0 ]]; then
        if mysql_cmd "TRUNCATE TABLE \`$table\`;" 2>/dev/null; then
            ((count++))
            ((total += deleted))
            echo "  [$count] $table: 清除 $deleted 条"
        else
            echo "  ⚠ $table: TRUNCATE 失败"
        fi
    fi
done

mysql_cmd "SET FOREIGN_KEY_CHECKS = 1;"

echo "------------------------------------------"
echo "  共清除 $count 张表, $total 条数据"
echo "  表结构已保留"
echo "=========================================="
