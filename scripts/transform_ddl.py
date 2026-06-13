#!/usr/bin/env python3
"""Transform tushare_ddl.sql: add auto-increment `id` PK to every table,
determine correct business UNIQUE key, add missing composite indexes."""

import re
import sys


def determine_business_key(table_name: str, field_lines: list[str],
                           old_pk_cols: list[str]) -> list[str]:
    """Determine the correct business UNIQUE key for a table."""
    all_cols: set[str] = set()
    for fl in field_lines:
        m = re.match(r"\s*`(\w+)`", fl)
        if m:
            all_cols.add(m.group(1))

    # Normalize: some tables use "code"/"theme_code"/"con_code" instead of
    # "ts_code"; "time"/"date"/"cal_date" instead of "trade_date".
    ts_code_col = next((c for c in ["ts_code", "code", "theme_code"] if c in all_cols), None)
    trade_date_col = next((c for c in ["trade_date", "time", "date", "cal_date"] if c in all_cols), None)
    has_end_date = "end_date" in all_cols
    has_report_type = "report_type" in all_cols
    has_con_code = "con_code" in all_cols

    # Many-to-many mapping tables: ts_code + con_code
    if ts_code_col and has_con_code:
        if trade_date_col:
            return [ts_code_col, "con_code", trade_date_col]
        return [ts_code_col, "con_code"]

    # Daily data tables: ts_code + trade_date
    if ts_code_col and trade_date_col:
        return [ts_code_col, trade_date_col]

    # Financial report tables: ts_code + end_date (+ report_type)
    if ts_code_col and has_end_date:
        if has_report_type:
            return [ts_code_col, "end_date", "report_type"]
        return [ts_code_col, "end_date"]

    # Aggregate tables: trade_date only (possibly + exchange_id)
    if trade_date_col and not ts_code_col:
        if "exchange_id" in all_cols:
            return [trade_date_col, "exchange_id"]
        return [trade_date_col]

    # Reference tables: ts_code only
    if ts_code_col and not trade_date_col and not has_end_date:
        return [ts_code_col]

    # Special: bse_mapping has n_code/o_code
    if "n_code" in all_cols:
        return ["n_code"]

    # Tables with just a "name" or other single natural key
    if "name" in all_cols:
        return ["name"]

    # Fallback
    if old_pk_cols:
        return old_pk_cols
    return []


def compute_new_indexes(field_lines: list[str], uk_cols: list[str],
                        existing_idx_columns: set[str]) -> list[str]:
    """Compute NEW indexes to add. Returns SQL lines."""
    all_cols: set[str] = set()
    for fl in field_lines:
        m = re.match(r"\s*`(\w+)`", fl)
        if m:
            all_cols.add(m.group(1))

    # Columns covered by UK (as leading columns) + existing indexes
    covered = set(existing_idx_columns)
    for c in uk_cols:
        covered.add(c)

    new_idx: list[str] = []

    # Normalize column synonyms
    has_stock_code = bool({"ts_code", "code"} & all_cols)
    has_trade_date = bool({"trade_date", "time", "date", "cal_date"} & all_cols)
    has_end_date = "end_date" in all_cols
    has_ann_date = "ann_date" in all_cols

    # For daily tables: add trade_date index for reverse lookups
    actual_trade_col = next((c for c in ["trade_date", "time", "date", "cal_date"] if c in all_cols), None)
    if has_stock_code and has_trade_date and actual_trade_col:
        if actual_trade_col not in covered:
            new_idx.append(f"  INDEX `idx_{actual_trade_col}` (`{actual_trade_col}`)")

    # For financial tables: add end_date, ann_date, f_ann_date.
    if has_stock_code and has_end_date:
        if "end_date" not in covered:
            new_idx.append("  INDEX `idx_end_date` (`end_date`)")
        if has_ann_date and "ann_date" not in covered:
            new_idx.append("  INDEX `idx_ann_date` (`ann_date`)")
        if "f_ann_date" in all_cols and "f_ann_date" not in covered:
            new_idx.append("  INDEX `idx_f_ann_date` (`f_ann_date`)")

    # For reference tables (ts_code only): add date indexes if present
    if has_stock_code and not has_trade_date and not has_end_date:
        if has_ann_date and "ann_date" not in covered:
            new_idx.append("  INDEX `idx_ann_date` (`ann_date`)")

    return new_idx


def transform_ddl(input_path: str, output_path: str) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match: optional comment + DROP TABLE + CREATE TABLE
    pattern = re.compile(
        r"(-- .*?\n)?DROP TABLE IF EXISTS `(\w+)`;\n"
        r"CREATE TABLE `\2` \(\n(.*?)\)\s*ENGINE=.*?;",
        re.DOTALL,
    )

    def transform_table(match: re.Match) -> str:
        comment = match.group(1) or ""
        table_name = match.group(2)
        body = match.group(3)

        lines = body.split("\n")

        old_pk_cols: list[str] = []
        field_lines: list[str] = []
        existing_indexes: list[tuple[str, str]] = []  # (sql_line, index_type)
        has_auto_increment = False

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("PRIMARY KEY"):
                m = re.findall(r"`(\w+)`", stripped)
                old_pk_cols = m
            elif stripped.startswith("INDEX ") or stripped.startswith("KEY "):
                existing_indexes.append((line, "INDEX"))
            elif stripped.startswith("UNIQUE KEY ") or stripped.startswith("UNIQUE INDEX "):
                existing_indexes.append((line, "UNIQUE"))
            elif "AUTO_INCREMENT" in stripped.upper():
                has_auto_increment = True
                field_lines.append(line)
            elif stripped == ",":
                pass  # stray comma
            else:
                field_lines.append(line)

        if has_auto_increment:
            return match.group(0)

        # Determine business UNIQUE key
        uk_cols = determine_business_key(table_name, field_lines, old_pk_cols)
        uk_set = set(uk_cols)

        # Collect existing index columns (for dedup).
        # Index syntax: INDEX `idx_name` (`col1`, `col2`)
        # Extract column names from inside the parentheses.
        existing_idx_columns: set[str] = set()
        filtered_existing_indexes: list[str] = []
        for sql_line, idx_type in existing_indexes:
            paren_match = re.search(r"\(([^)]+)\)", sql_line)
            if paren_match:
                idx_cols = re.findall(r"`(\w+)`", paren_match.group(1))
            else:
                idx_cols = []
            idx_tuple = tuple(idx_cols)
            # Skip if identical to UK
            if idx_tuple == tuple(uk_cols):
                continue
            # Record column names for dedup
            for c in idx_cols:
                existing_idx_columns.add(c)
            filtered_existing_indexes.append(sql_line)

        # Compute new indexes (deduped against existing)
        new_indexes = compute_new_indexes(field_lines, uk_cols, existing_idx_columns)

        # Build output
        new_lines: list[str] = []

        # 1. Auto-increment id
        new_lines.append("  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,")

        # 2. Field columns
        for fl in field_lines:
            new_lines.append(fl)

        # 3. PK on id
        new_lines.append("")
        new_lines.append("  PRIMARY KEY (`id`),")

        # 4. UNIQUE KEY — build with prefix for TEXT columns
        if uk_cols:
            # Detect TEXT columns to add prefix length
            col_types: dict[str, str] = {}
            for fl in field_lines:
                m = re.match(r"\s*`(\w+)`\s+(\w+)", fl)
                if m:
                    col_types[m.group(1)] = m.group(2).upper()

            uk_name = "uk_" + "_".join(uk_cols)
            uk_parts = []
            for c in uk_cols:
                if col_types.get(c, "") in ("TEXT", "MEDIUMTEXT", "LONGTEXT", "TINYTEXT", "BLOB"):
                    uk_parts.append(f"`{c}`(255)")
                else:
                    uk_parts.append(f"`{c}`")
            cols_str = ", ".join(uk_parts)
            new_lines.append(f"  UNIQUE KEY `{uk_name}` ({cols_str}),")

        # 5. Existing indexes (deduped)
        for idx_line in filtered_existing_indexes:
            new_lines.append(idx_line)

        # 6. New indexes
        for ni in new_indexes:
            new_lines.append(ni)

        # Remove trailing comma from the LAST line
        new_lines[-1] = new_lines[-1].rstrip(",")

        new_body = "\n".join(new_lines)

        # Extract ENGINE tail (keep original engine config)
        engine_match = re.search(
            r"\)\s*(ENGINE=InnoDB\s+DEFAULT\s+CHARSET=utf8mb4\s+COLLATE=utf8mb4_unicode_ci\s+COMMENT=.*?;)",
            match.group(0), re.DOTALL
        )
        if engine_match:
            engine_tail = engine_match.group(1)
        else:
            # Fallback: grab from "ENGINE=" to the end
            engine_match = re.search(r"\)\s*(ENGINE=.*)", match.group(0), re.DOTALL)
            engine_tail = engine_match.group(1) if engine_match else \
                "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"

        return (
            f"{comment}DROP TABLE IF EXISTS `{table_name}`;\n"
            f"CREATE TABLE `{table_name}` (\n{new_body}\n) {engine_tail}"
        )

    result = pattern.sub(transform_table, content)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Written to {output_path}")

    return result


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "data/tushare_ddl.sql"
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file
    transform_ddl(input_file, output_file)
    print("Done.")
