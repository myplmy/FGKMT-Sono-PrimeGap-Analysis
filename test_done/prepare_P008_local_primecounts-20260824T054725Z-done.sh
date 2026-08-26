#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${1:-}" != "--confirm-p008" || "$#" -ne 1 ]]; then
    echo "Usage: bash ./prepare_P008_local_primecounts.sh --confirm-p008" >&2
    echo "This computes exact pi(x) inputs only; it does not search prime gaps." >&2
    exit 2
fi

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ready_file="$repo_root/tmp/p008-primecounts/READY.txt"
if [[ -e "$ready_file" ]]; then
    echo "[STOP] READY file already exists; refusing ambiguous reuse: $ready_file" >&2
    exit 3
fi

for command_name in primecount python3 sha256sum tee grep tail awk sort wc nproc head; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        echo "[STOP] Missing WSL command: $command_name" >&2
        exit 4
    fi
done
if [[ ! -x /usr/bin/time ]]; then
    echo "[STOP] Missing WSL command: /usr/bin/time" >&2
    exit 4
fi

threads=8
if (( $(nproc) < threads )); then
    echo "[STOP] Need at least $threads logical CPUs." >&2
    exit 4
fi
ulimit -v 31457280
export OMP_NUM_THREADS="$threads"
export OMP_DYNAMIC=FALSE

run_stamp="$(date -u +%Y%m%dT%H%M%SZ)"
run_id="${run_stamp}_p008_primecount_prepare"
run_root="$repo_root/tmp/p008-primecounts/$run_id"
counts_file="$run_root/prime_counts.csv"
metadata_file="$run_root/metadata.txt"
metrics_file="$run_root/metrics.txt"
log_file="$repo_root/test_result/logs/run_${run_id}.log"
mkdir -p "$run_root" "$(dirname "$log_file")" "$(dirname "$ready_file")"
if [[ -e "$log_file" || -e "$counts_file" || -e "$metadata_file" ]]; then
    echo "[STOP] Refusing to overwrite P008 preparation artifacts." >&2
    exit 5
fi
: > "$log_file"
exec > >(tee -a "$log_file") 2>&1

current_stage="initialization"
failure_line="unknown"
failure_command="unknown"
failure_written=0
failed_manifest="$run_root/manifest.failed.txt"
write_failed_manifest() {
    local exit_code="$1"
    if (( failure_written != 0 )); then
        return 0
    fi
    failure_written=1
    (
        set +e
        trap - ERR
        {
            echo 'status=P008_PRIMECOUNTS_FAILED'
            echo "run_id=$run_id"
            echo "failed_at_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
            echo "failed_stage=$current_stage"
            echo "exit_code=$exit_code"
            echo "failed_line=$failure_line"
            printf 'failed_command=%q\n' "$failure_command"
            echo "threads=$threads"
            echo 'virtual_memory_limit_kib=31457280'
            echo 'gpu_used=false'
            if [[ -f "$counts_file" ]]; then sha256sum "$counts_file"; fi
            if [[ -f "$metrics_file" ]]; then sha256sum "$metrics_file"; fi
            if [[ -f "$log_file" ]]; then sha256sum "$log_file"; fi
        } > "$failed_manifest"
        echo "[FAIL] P008 prime-count preparation stopped" >&2
        echo "[FAIL] stage=$current_stage exit_code=$exit_code line=$failure_line" >&2
        echo "[FAIL] command=$failure_command" >&2
        echo "[FAIL] manifest=$failed_manifest" >&2
    )
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

echo "[RUN] scope=P008_EXACT_LOCAL_PRIMECOUNT_INPUTS"
echo "[RUN] id=$run_id"
echo "[RUN] threads=$threads"
echo "[RUN] virtual_memory_limit_kib=31457280"
echo "[RUN] gpu_used=false"
echo "[RUN] actual_prime_gap_search=false"
echo "[RUN] block_grid=x=10^20,L={10^3,10^6,10^9,10^12}"
current_stage="primecount-version"
primecount_version="$(primecount --version | head -n 1)"
echo "[RUN] primecount_version=$primecount_version"

declare -A pi_cache
PI_RESULT=""
compute_pi() {
    local endpoint="$1"
    local label="$2"
    if [[ -n "${pi_cache[$endpoint]+set}" ]]; then
        PI_RESULT="${pi_cache[$endpoint]}"
        echo "[CACHE] endpoint=$endpoint pi=$PI_RESULT"
        return 0
    fi
    local gourdon_out="$run_root/${label}_gourdon.txt"
    local dr_out="$run_root/${label}_deleglise_rivat.txt"
    current_stage="primecount-${label}-gourdon"
    echo "[STAGE] primecount endpoint=$endpoint algorithm=gourdon"
    /usr/bin/time -v -a -o "$metrics_file" \
        primecount "$endpoint" --threads="$threads" --gourdon \
        2>&1 | tee "$gourdon_out"
    current_stage="primecount-${label}-deleglise-rivat"
    echo "[STAGE] primecount endpoint=$endpoint algorithm=deleglise-rivat"
    /usr/bin/time -v -a -o "$metrics_file" \
        primecount "$endpoint" --threads="$threads" --deleglise-rivat \
        2>&1 | tee "$dr_out"
    local gourdon_value
    local dr_value
    gourdon_value="$(grep -E '^[0-9]+$' "$gourdon_out" | tail -n 1)"
    dr_value="$(grep -E '^[0-9]+$' "$dr_out" | tail -n 1)"
    if [[ -z "$gourdon_value" || -z "$dr_value" ]]; then
        echo "[FAIL] Could not parse exact prime count for endpoint=$endpoint" >&2
        exit 6
    fi
    if [[ "$gourdon_value" != "$dr_value" ]]; then
        echo "[FAIL] primecount algorithms disagree at endpoint=$endpoint" >&2
        echo "[FAIL] gourdon=$gourdon_value deleglise_rivat=$dr_value" >&2
        exit 7
    fi
    pi_cache[$endpoint]="$gourdon_value"
    PI_RESULT="$gourdon_value"
    echo "[CHECK] primecount_algorithms_match endpoint=$endpoint pi=$PI_RESULT"
}

printf '%s\n' 'block_id,a,b,pi_a_minus_1,pi_b_minus_1,first_prime,last_prime,right_boundary_gap,actual_large_gap_count,count_provenance' > "$counts_file"
x='100000000000000000000'
lengths=(1000 1000000 1000000000 1000000000000)
a_minus_1="$(python3 -c 'import sys; print(int(sys.argv[1])-1)' "$x")"
compute_pi "$a_minus_1" 'a_minus_1'
pi_a="$PI_RESULT"
index=0
for length in "${lengths[@]}"; do
    index=$((index + 1))
    b="$(python3 -c 'import sys; print(int(sys.argv[1])+int(sys.argv[2]))' "$x" "$length")"
    b_minus_1="$(python3 -c 'import sys; print(int(sys.argv[1])-1)' "$b")"
    compute_pi "$b_minus_1" "b${index}_minus_1"
    pi_b="$PI_RESULT"
    printf 'x1e20_L%s,%s,%s,%s,%s,,,,,primecount_gourdon_deleglise_rivat_match\n' \
        "$length" "$x" "$b" "$pi_a" "$pi_b" >> "$counts_file"
done

counts_sha256="$(sha256sum "$counts_file" | awk '{print $1}')"
metrics_sha256="$(sha256sum "$metrics_file" | awk '{print $1}')"
{
    echo 'status=PRIMECOUNTS_READY'
    echo "run_id=$run_id"
    echo "primecount_version=$primecount_version"
    echo 'algorithms=gourdon,deleglise-rivat'
    echo 'algorithm_outputs_must_match=true'
    echo "threads=$threads"
    echo 'virtual_memory_limit_kib=31457280'
    echo 'gpu_used=false'
    echo 'actual_prime_gap_search=false'
    echo 'endpoint_arithmetic_generator=WSL_python3_exact_integer_strings'
    echo 'bound_calculator=Windows_FGKMT_Python_in_separate_step'
    echo "counts_sha256=$counts_sha256"
    echo "metrics_sha256=$metrics_sha256"
} > "$metadata_file"

counts_relative="${counts_file#"$repo_root"/}"
metadata_relative="${metadata_file#"$repo_root"/}"
{
    echo "counts_relative=$counts_relative"
    echo "metadata_relative=$metadata_relative"
    echo "preparation_log_relative=${log_file#"$repo_root"/}"
} > "$ready_file"

current_stage="completed"
trap - ERR EXIT
echo '[PASS] P008 exact prime-count input preparation completed.'
echo "[RUN] counts=$counts_file"
echo "[RUN] metadata=$metadata_file"
echo "[RUN] ready=$ready_file"
echo "[NEXT] Exit WSL, then run in Windows: run_P008_local_residue_certificate_full.bat --confirm-p008"
