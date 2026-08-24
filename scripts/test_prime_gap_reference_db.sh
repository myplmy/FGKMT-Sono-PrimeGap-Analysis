#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "$#" -ne 2 ]]; then
    echo "Usage: bash ./scripts/test_prime_gap_reference_db.sh allgaps.sql expected_sha256" >&2
    exit 2
fi

sql_path="$1"
expected_sha256="$2"
if [[ ! -f "$sql_path" ]]; then
    echo "P005_GAPS_DB_TOY_FAIL missing_sql=$sql_path" >&2
    exit 3
fi
observed_sha256="$(sha256sum "$sql_path" | awk '{print $1}')"
if [[ "$observed_sha256" != "$expected_sha256" ]]; then
    echo "P005_GAPS_DB_TOY_FAIL hash_mismatch=$observed_sha256" >&2
    exit 4
fi

task_tmp="$(mktemp -d -t fgkmt-p005-gaps-db-XXXXXX)"
cleanup() {
    case "$task_tmp" in
        /tmp/fgkmt-p005-gaps-db-*) rm -rf -- "$task_tmp" ;;
        *)
            echo "P005_GAPS_DB_TOY_FAIL unsafe_temp=$task_tmp" >&2
            return 97
            ;;
    esac
}
trap cleanup EXIT

database="$task_tmp/gaps.db"
sqlite3 "$database" < "$sql_path"
table_exists="$(sqlite3 "$database" \
    "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='gaps';")"
row_count="$(sqlite3 "$database" "SELECT COUNT(*) FROM gaps;")"
if [[ "$table_exists" -ne 1 || "$row_count" -le 0 ]]; then
    echo "P005_GAPS_DB_TOY_FAIL table=$table_exists rows=$row_count" >&2
    exit 5
fi

echo "P005_GAPS_DB_TOY_PASS rows=$row_count sha256=$observed_sha256"
