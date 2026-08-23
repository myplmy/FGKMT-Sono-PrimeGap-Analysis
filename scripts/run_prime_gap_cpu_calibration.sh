#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${1:-}" != "--approved" ]]; then
    echo "ERROR: explicit --approved flag is required" >&2
    exit 2
fi

repo_root="${2:-}"
log_file="${3:-}"
if [[ -z "$repo_root" || -z "$log_file" ]]; then
    echo "ERROR: repository root and log path are required" >&2
    exit 2
fi
repo_root="${repo_root%/}"
log_already_open="${4:-}"

if [[ -n "$log_already_open" && "$log_already_open" != "--log-already-open" ]]; then
    echo "ERROR: unknown logging mode: $log_already_open" >&2
    exit 2
fi
if [[ "$log_already_open" == "--log-already-open" ]]; then
    if [[ ! -f "$log_file" ]]; then
        echo "ERROR: wrapper-declared log does not exist: $log_file" >&2
        exit 3
    fi
else
    if [[ -e "$log_file" ]]; then
        echo "ERROR: refusing to overwrite existing log: $log_file" >&2
        exit 3
    fi
    mkdir -p "$(dirname "$log_file")"
    exec > >(tee "$log_file") 2>&1
fi

pin="8f3e81b9ddadf1fd59552ee7e86fc1d6a5bb918d"
threads=8
max_mem_gib=28
virtual_mem_kib=31457280
started_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
run_id="$(date -u +%Y%m%dT%H%M%SZ)_p005_prime_gap_cpu_calibration"
run_root="$repo_root/tmp/prime-gap-p005/$run_id"
source_dir="$run_root/source"
metrics_file="$run_root/metrics.txt"

echo "[RUN] scope=P005_PRIME_GAP_CPU_CALIBRATION"
echo "[RUN] id=$run_id"
echo "[RUN] started_at_utc=$started_at"
echo "[RUN] upstream_commit=$pin"
echo "[RUN] threads=$threads"
echo "[RUN] upstream_max_mem_gib=$max_mem_gib"
echo "[RUN] virtual_memory_limit_kib=$virtual_mem_kib"
echo "[RUN] gpu_disabled=true"
echo "[RUN] target_exhaustive_search=false"
if [[ -e "$run_root" ]]; then
    echo "[STOP] Refusing to overwrite run directory: $run_root"
    exit 5
fi
mkdir -p "$run_root"

current_stage="initialization"
failure_line="unknown"
failure_command="unknown"
failure_written=0
failed_manifest="$run_root/manifest.failed.txt"
search_db=""

write_failed_manifest() {
    local exit_code="$1"
    set +e
    trap - ERR
    if (( failure_written != 0 )); then
        return
    fi
    failure_written=1
    echo "[FAIL] P005 calibration stopped" >&2
    echo "[FAIL] stage=$current_stage exit_code=$exit_code line=$failure_line" >&2
    echo "[FAIL] command=$failure_command" >&2
    if [[ ! -e "$failed_manifest" ]]; then
        {
            echo "status=CALIBRATION_FAILED"
            echo "run_id=$run_id"
            echo "started_at_utc=$started_at"
            echo "failed_at_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
            echo "failed_stage=$current_stage"
            echo "exit_code=$exit_code"
            echo "failed_line=$failure_line"
            printf 'failed_command=%q\n' "$failure_command"
            echo "upstream_commit_expected=$pin"
            echo "threads=$threads"
            echo "max_mem_gib=$max_mem_gib"
            echo "virtual_mem_kib=$virtual_mem_kib"
            echo "gpu_disabled=true"
            echo "target_exhaustive_search=false"
            if [[ -f "$metrics_file" ]]; then
                sha256sum "$metrics_file"
            else
                echo "metrics_status=not_created"
            fi
            if [[ -n "$search_db" && -f "$search_db" ]]; then
                sha256sum "$search_db"
            else
                echo "search_db_status=not_created"
            fi
            if [[ -d "$run_root/source/unknowns" ]]; then
                find "$run_root/source/unknowns" -maxdepth 1 -type f -print0 \
                    | sort -z | xargs -0 -r sha256sum
            else
                echo "unknowns_status=not_created"
            fi
        } > "$failed_manifest"
        echo "[FAIL] manifest=$failed_manifest" >&2
    else
        echo "[FAIL] existing_manifest_preserved=$failed_manifest" >&2
    fi
}

on_error() {
    local exit_code="$1"
    failure_line="$2"
    failure_command="$3"
    write_failed_manifest "$exit_code"
}

on_exit() {
    local exit_code="$1"
    local exit_line="$2"
    local exit_command="$3"
    if (( exit_code != 0 )); then
        if [[ "$failure_line" == "unknown" ]]; then
            failure_line="$exit_line"
            failure_command="$exit_command"
        fi
        write_failed_manifest "$exit_code"
    fi
}

trap 'on_error "$?" "$LINENO" "$BASH_COMMAND"' ERR
trap 'on_exit "$?" "$LINENO" "$BASH_COMMAND"' EXIT

current_stage="dependency-preflight"

missing=0
for command_name in git g++ make sqlite3 md5sum sha256sum grep tee awk sort wc nproc find xargs; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        echo "[DEPENDENCY] MISSING command=$command_name"
        missing=1
    fi
done
if [[ ! -x /usr/bin/time ]]; then
    echo "[DEPENDENCY] MISSING command=/usr/bin/time"
    missing=1
fi
for package_name in libgmp-dev libsqlite3-dev libprimesieve-dev time; do
    if ! dpkg-query -W -f='${Status}' "$package_name" 2>/dev/null | grep -q 'install ok installed'; then
        echo "[DEPENDENCY] MISSING package=$package_name"
        missing=1
    fi
done
if (( missing != 0 )); then
    echo "[STOP] Required WSL packages are missing; nothing was installed."
    echo "[REQUEST] sudo apt update"
    echo "[REQUEST] sudo apt install -y build-essential git make sqlite3 libgmp-dev libsqlite3-dev libprimesieve-dev time"
    exit 4
fi
available_threads="$(nproc)"
if (( available_threads < threads )); then
    echo "[STOP] Need at least $threads logical CPUs; WSL reports $available_threads."
    exit 4
fi
echo "[RUN] available_logical_cpus=$available_threads"


# Apply a hard process-tree address-space ceiling below the user's 32 GiB cap.
ulimit -v "$virtual_mem_kib"
export OMP_NUM_THREADS="$threads"
export OMP_DYNAMIC=FALSE

current_stage="clone-pinned-source"
echo "[STAGE] clone-pinned-source"
git clone --quiet https://github.com/sethtroisi/prime-gap.git "$source_dir"
git -C "$source_dir" checkout --quiet --detach "$pin"
actual_pin="$(git -C "$source_dir" rev-parse HEAD)"
if [[ "$actual_pin" != "$pin" ]]; then
    echo "[STOP] Upstream pin mismatch: $actual_pin"
    exit 6
fi
if [[ -n "$(git -C "$source_dir" status --short)" ]]; then
    echo "[STOP] Pinned source is unexpectedly dirty before build"
    exit 7
fi

cd "$source_dir"
mkdir -p unknowns

current_stage="build-cpu-only"
echo "[STAGE] build-cpu-only"
echo "===== build-cpu-only =====" >> "$metrics_file"
/usr/bin/time -v -a -o "$metrics_file" \
    make -j"$threads" combined_sieve gap_stats gap_test_simple VALIDATE_FACTORS=1
current_stage="initialize-sqlite-ledger"
echo "[STAGE] initialize-sqlite-ledger"
search_db="$source_dir/prime-gap-search.db"
if [[ -e "$search_db" ]]; then
    echo "[STOP] Refusing to reuse SQLite ledger: $search_db"
    exit 7
fi
sqlite3 "$search_db" < "$source_dir/schema.sql"
schema_tables="$(sqlite3 "$search_db" \
    "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('range','range_stats','m_stats','result') ORDER BY name;")"
expected_schema_tables=$'m_stats\nrange\nrange_stats\nresult'
if [[ "$schema_tables" != "$expected_schema_tables" ]]; then
    echo "[STOP] SQLite ledger schema mismatch"
    printf '[STOP] observed_tables=%q\n' "$schema_tables"
    exit 7
fi
echo "[CHECK] sqlite_ledger_initialized=true"
echo "[CHECK] sqlite_tables=m_stats,range,range_stats,result"

params=(-p 907 -d 2190 --mstart 1 --max-prime 100 --sieve-length 11000)
reference_fn="907_2190_1_200_s11000_l100M.txt"
reference_m1_fn="907_2190_1_200_s11000_l100M.m1.txt"

current_stage="upstream-reference-method1"
echo "[STAGE] upstream-reference-method1"
echo "===== upstream-reference-method1 =====" >> "$metrics_file"
/usr/bin/time -v -a -o "$metrics_file" \
    ./combined_sieve --method1 -qqq --save-unknowns "${params[@]}" --minc 200 -t 1 --max-mem "$max_mem_gib" \
        --search-db "$search_db"

current_stage="upstream-reference-method2"
echo "[STAGE] upstream-reference-method2"
echo "===== upstream-reference-method2 =====" >> "$metrics_file"
/usr/bin/time -v -a -o "$metrics_file" \
    ./combined_sieve -qqq --save-unknowns "${params[@]}" --minc 200 -t "$threads" --max-mem "$max_mem_gib" \
        --search-db "$search_db"

echo "15a5cbff7301262caf047028c05f0525  unknowns/$reference_fn" | md5sum -c -
echo "15a5cbff7301262caf047028c05f0525  unknowns/$reference_m1_fn" | md5sum -c -

current_stage="upstream-reference-gap-stats"
echo "[STAGE] upstream-reference-gap-stats"
echo "===== upstream-reference-gap-stats =====" >> "$metrics_file"
/usr/bin/time -v -a -o "$metrics_file" \
    ./gap_stats -u "$reference_fn" -t "$threads" --min-merit 8 --search-db "$search_db" \
    2>&1 | tee "$run_root/gap_stats_minc200.txt"
grep -q 'avg missing prob : 0.0000000' "$run_root/gap_stats_minc200.txt"

current_stage="upstream-reference-gap-test-simple"
echo "[STAGE] upstream-reference-gap-test-simple"
echo "===== upstream-reference-gap-test-simple =====" >> "$metrics_file"
/usr/bin/time -v -a -o "$metrics_file" \
    ./gap_test_simple -u "$reference_m1_fn" -t "$threads" -q --min-merit 8 --search-db "$search_db" \
    2>&1 | tee "$run_root/gap_test_simple_minc200.txt"
grep -q '^7750 ' "$run_root/gap_test_simple_minc200.txt"

scaling_hashes="$run_root/thread_scaling_sha256.txt"
: > "$scaling_hashes"
for scaling_threads in 1 2 4 8; do
    scaling_root="$run_root/thread-scaling/t${scaling_threads}"
    mkdir -p "$scaling_root/unknowns"
    scaling_db="$scaling_root/prime-gap-search.db"
    sqlite3 "$scaling_db" < "$source_dir/schema.sql"
    current_stage="thread-scaling-t${scaling_threads}"
    echo "[STAGE] thread-scaling minc=2000 threads=$scaling_threads"
    echo "===== thread-scaling-minc-2000-t$scaling_threads =====" >> "$metrics_file"
    (
        cd "$scaling_root"
        export OMP_NUM_THREADS="$scaling_threads"
        /usr/bin/time -v -a -o "$metrics_file" \
            "$source_dir/combined_sieve" -qqq --save-unknowns "${params[@]}" \
            --minc 2000 -t "$scaling_threads" --max-mem "$max_mem_gib" --search-db "$scaling_db"
    )
    scaling_output="$scaling_root/unknowns/907_2190_1_2000_s11000_l100M.txt"
    if [[ ! -f "$scaling_output" ]]; then
        echo "[STOP] Missing thread-scaling output: $scaling_output"
        exit 8
    fi
    sha256sum "$scaling_output" >> "$scaling_hashes"
done

unique_scaling_hashes="$(awk '{print $1}' "$scaling_hashes" | sort -u | wc -l)"
if [[ "$unique_scaling_hashes" -ne 1 ]]; then
    echo "[STOP] Thread-scaling outputs disagree; see $scaling_hashes"
    exit 9
fi
echo "[CHECK] thread_scaling_output_hashes_match=true"

for minc in 2000 10000; do
    fn="907_2190_1_${minc}_s11000_l100M.txt"
    current_stage="calibration-minc-${minc}"
    echo "[STAGE] calibration-search minc=$minc"
    echo "===== calibration-search-minc-$minc =====" >> "$metrics_file"
    /usr/bin/time -v -a -o "$metrics_file" \
        ./combined_sieve -qqq --save-unknowns "${params[@]}" --minc "$minc" -t "$threads" --max-mem "$max_mem_gib" \
            --search-db "$search_db"

    echo "===== calibration-stats-minc-$minc =====" >> "$metrics_file"
    /usr/bin/time -v -a -o "$metrics_file" \
        ./gap_stats -u "$fn" -t "$threads" --min-merit 8 --search-db "$search_db" \
        2>&1 | tee "$run_root/gap_stats_minc${minc}.txt"

    echo "===== calibration-gap-test-minc-$minc =====" >> "$metrics_file"
    /usr/bin/time -v -a -o "$metrics_file" \
        ./gap_test_simple -u "$fn" -t "$threads" -q --min-merit 8 --search-db "$search_db" \
        2>&1 | tee "$run_root/gap_test_simple_minc${minc}.txt"
done

current_stage="write-success-manifest"
{
    echo "status=CALIBRATION_PASS"
    echo "upstream_commit=$actual_pin"
    echo "threads=$threads"
    echo "max_mem_gib=$max_mem_gib"
    echo "virtual_mem_kib=$virtual_mem_kib"
    echo "gpu_disabled=true"
    echo "target_exhaustive_search=false"
    echo "finished_at_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "sqlite_tables=m_stats,range,range_stats,result"
    sha256sum "$search_db"
    md5sum unknowns/907_2190_1_*_s11000_l100M.txt
    echo "thread_scaling_output_hashes_match=true"
    cat "$scaling_hashes"
} > "$run_root/manifest.txt"

current_stage="completed"
trap - ERR EXIT
echo "[PASS] P005 CPU calibration completed"
echo "[RUN] artifact_root=$run_root"
echo "[RUN] manifest=$run_root/manifest.txt"
echo "[RUN] metrics=$metrics_file"

