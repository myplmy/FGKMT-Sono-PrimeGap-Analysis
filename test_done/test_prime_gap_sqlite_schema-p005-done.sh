#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "$#" -ne 1 ]]; then
    echo "Usage: bash ./scripts/test_prime_gap_sqlite_schema.sh /path/to/schema.sql" >&2
    exit 2
fi

schema_path="$1"
if [[ ! -f "$schema_path" ]]; then
    echo "SCHEMA_TOY_FAIL missing_schema=$schema_path" >&2
    exit 3
fi

task_tmp="$(mktemp -d -t fgkmt-p005-sqlite-XXXXXX)"
cleanup() {
    case "$task_tmp" in
        /tmp/fgkmt-p005-sqlite-*) rm -rf -- "$task_tmp" ;;
        *)
            echo "SCHEMA_TOY_FAIL unsafe_temp=$task_tmp" >&2
            return 97
            ;;
    esac
}
trap cleanup EXIT

ledger_path="$task_tmp/prime-gap-search.db"
sqlite3 "$ledger_path" < "$schema_path"
observed_tables="$(sqlite3 "$ledger_path" \
    "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('range','range_stats','m_stats','result') ORDER BY name;")"
expected_tables=$'m_stats\nrange\nrange_stats\nresult'

if [[ "$observed_tables" != "$expected_tables" ]]; then
    printf 'SCHEMA_TOY_FAIL observed_tables=%q\n' "$observed_tables" >&2
    exit 4
fi

echo "P005_SQLITE_SCHEMA_TOY_PASS"
printf '%s\n' "$observed_tables"
