#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${1:-}" != "--confirm-p018-prefix-counts" || "$#" -ne 1 ]]; then
    echo "Usage: bash ./scripts/experiments/p018/prepare_p018_prefix_primecounts.sh --confirm-p018-prefix-counts" >&2
    echo "This computes exact endpoint pi(x) values only; it does not run recurrence analysis." >&2
    exit 2
fi

script_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
repo_root="$(cd -- "$script_directory/../../.." && pwd -P)"
contract="$repo_root/test_plan/P018_prefix_information_probe_contract_v1.json"
expected_contract_sha='7171efef2659340e240993a384f5dfdfb1b5d60c1b1ab20880aa2129317b0f92'
ready_file="$repo_root/tmp/p018-prefix-primecounts/READY.txt"

if [[ ! -f "$contract" ]]; then
    echo "[STOP] Missing frozen P018 prefix contract: $contract" >&2
    exit 3
fi
if [[ "$(sha256sum "$contract" | awk '{print $1}')" != "$expected_contract_sha" ]]; then
    echo "[STOP] Frozen P018 prefix contract hash mismatch." >&2
    exit 3
fi
if [[ -e "$ready_file" ]]; then
    echo "[STOP] READY file already exists; refusing ambiguous reuse: $ready_file" >&2
    exit 3
fi

for command_name in primecount python3 sha256sum tee grep tail awk nproc head lscpu taskset basename; do
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
physical_cores=4
virtual_memory_limit_kib=30000000
if (( $(nproc) < threads )); then
    echo "[STOP] Need at least $threads logical CPUs." >&2
    exit 4
fi
ulimit -v "$virtual_memory_limit_kib"
export OMP_NUM_THREADS="$threads"
export OMP_DYNAMIC=FALSE

declare -A selected_core_keys=()
selected_cpus=()
while IFS=, read -r cpu core socket _; do
    [[ "$cpu" == \#* ]] && continue
    [[ -z "$cpu" ]] && continue
    core_key="$socket:$core"
    if [[ -z "${selected_core_keys[$core_key]+set}" ]]; then
        if (( ${#selected_core_keys[@]} >= physical_cores )); then
            continue
        fi
        selected_core_keys[$core_key]=1
    fi
    if (( ${#selected_cpus[@]} < threads )); then
        selected_cpus+=("$cpu")
    fi
done < <(lscpu -p=CPU,CORE,SOCKET)
if (( ${#selected_core_keys[@]} != physical_cores || ${#selected_cpus[@]} != threads )); then
    echo "[STOP] WSL topology did not expose 4 physical cores / 8 logical CPUs." >&2
    exit 4
fi
cpu_list="$(IFS=,; echo "${selected_cpus[*]}")"

run_stamp="$(date -u +%Y%m%dT%H%M%SZ)"
run_id="${run_stamp}_p018_prefix_primecount_prepare"
run_root="$repo_root/tmp/p018-prefix-primecounts/$run_id"
counts_file="$run_root/prime_counts.csv"
metadata_file="$run_root/metadata.txt"
metrics_file="$run_root/metrics.txt"
log_file="$repo_root/test_result/logs/run_${run_id}.log"
failed_manifest="$run_root/manifest.failed.txt"
mkdir -p "$run_root" "$(dirname "$log_file")" "$(dirname "$ready_file")"
if [[ -e "$log_file" || -e "$counts_file" || -e "$metadata_file" ]]; then
    echo "[STOP] Refusing to overwrite P018 prime-count preparation artifacts." >&2
    exit 5
fi
: > "$log_file"
exec > >(tee -a "$log_file") 2>&1

current_stage='initialization'
failure_line='unknown'
failure_command='unknown'
failure_written=0
write_failed_manifest() {
    local exit_code="$1"
    if (( failure_written != 0 )); then return 0; fi
    failure_written=1
    (
        set +e
        trap - ERR
        {
            echo 'status=P018_PREFIX_PRIMECOUNTS_FAILED'
            echo "run_id=$run_id"
            echo "failed_at_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
            echo "failed_stage=$current_stage"
            echo "exit_code=$exit_code"
            echo "failed_line=$failure_line"
            printf 'failed_command=%q\n' "$failure_command"
            echo "threads=$threads"
            echo "physical_cores=$physical_cores"
            echo "cpu_list=$cpu_list"
            echo "virtual_memory_limit_kib=$virtual_memory_limit_kib"
            echo 'gpu_used=false'
            [[ -f "$counts_file" ]] && sha256sum "$counts_file"
            [[ -f "$metrics_file" ]] && sha256sum "$metrics_file"
            [[ -f "$log_file" ]] && sha256sum "$log_file"
        } > "$failed_manifest"
        echo "[FAIL] P018 prefix prime-count preparation stopped" >&2
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
        if [[ "$failure_line" == 'unknown' ]]; then
            failure_line="$exit_line"
            failure_command="$exit_command"
        fi
        write_failed_manifest "$exit_code"
    fi
}
trap 'on_error "$?" "$LINENO" "$BASH_COMMAND"' ERR
trap 'on_exit "$?" "$LINENO" "$BASH_COMMAND"' EXIT

echo '[RUN] experiment=P018_PREFIX_PRIMECOUNT_PREPARATION'
echo "[RUN] id=$run_id"
echo "[RUN] threads=$threads"
echo "[RUN] physical_cores=$physical_cores cpu_list=$cpu_list"
echo "[RUN] virtual_memory_limit_kib=$virtual_memory_limit_kib"
echo '[RUN] gpu_used=false actual_recurrence_analysis=false'
echo "[RUN] contract_sha256=$expected_contract_sha"
current_stage='primecount-version'
primecount_version="$(primecount --version | head -n 1)"
echo "[RUN] primecount_version=$primecount_version"

declare -A pi_cache
PI_RESULT=''
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
        taskset -c "$cpu_list" primecount "$endpoint" --threads="$threads" --gourdon \
        2>&1 | tee "$gourdon_out"
    current_stage="primecount-${label}-deleglise-rivat"
    echo "[STAGE] primecount endpoint=$endpoint algorithm=deleglise-rivat"
    /usr/bin/time -v -a -o "$metrics_file" \
        taskset -c "$cpu_list" primecount "$endpoint" --threads="$threads" --deleglise-rivat \
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
        exit 7
    fi
    pi_cache[$endpoint]="$gourdon_value"
    PI_RESULT="$gourdon_value"
    echo "[CHECK] primecount_algorithms_match endpoint=$endpoint pi=$PI_RESULT"
}

printf '%s\n' 'mode,lower_inclusive,upper_exclusive,lower_minus_1,upper_minus_1,pi_lower_minus_1,pi_upper_minus_1,exact_gap_start_count,count_provenance' > "$counts_file"
write_mode() {
    local mode="$1"
    local lower="$2"
    local upper="$3"
    local lower_minus_1
    local upper_minus_1
    lower_minus_1="$(python3 -c 'import sys; print(int(sys.argv[1])-1)' "$lower")"
    upper_minus_1="$(python3 -c 'import sys; print(int(sys.argv[1])-1)' "$upper")"
    compute_pi "$lower_minus_1" "${mode,,}_lower_minus_1"
    local pi_lower="$PI_RESULT"
    compute_pi "$upper_minus_1" "${mode,,}_upper_minus_1"
    local pi_upper="$PI_RESULT"
    local exact_count
    exact_count="$(python3 -c 'import sys; print(int(sys.argv[2])-int(sys.argv[1]))' "$pi_lower" "$pi_upper")"
    if [[ "$exact_count" -le 0 ]]; then
        echo "[FAIL] Nonpositive exact gap count for mode=$mode" >&2
        exit 8
    fi
    printf '%s,%s,%s,%s,%s,%s,%s,%s,%s\n' \
        "$mode" "$lower" "$upper" "$lower_minus_1" "$upper_minus_1" \
        "$pi_lower" "$pi_upper" "$exact_count" \
        'primecount_gourdon_deleglise_rivat_match' >> "$counts_file"
    echo "[CHECK] mode=$mode exact_gap_start_count=$exact_count"
}

current_stage='write-exact-counts'
write_mode 'P0' '1346294310749' '1408695493610'
write_mode 'A' '1000000000000' '1968188556462'

counts_sha256="$(sha256sum "$counts_file" | awk '{print $1}')"
metrics_sha256="$(sha256sum "$metrics_file" | awk '{print $1}')"
evidence_manifest="$run_root/primecount_evidence.sha256"
: > "$evidence_manifest"
for evidence_file in "$run_root"/*_gourdon.txt "$run_root"/*_deleglise_rivat.txt; do
    printf '%s  %s\n' \
        "$(sha256sum "$evidence_file" | awk '{print $1}')" \
        "$(basename "$evidence_file")" >> "$evidence_manifest"
done
evidence_manifest_sha256="$(sha256sum "$evidence_manifest" | awk '{print $1}')"
{
    echo 'status=P018_PREFIX_PRIMECOUNTS_READY'
    echo "run_id=$run_id"
    echo "primecount_version=$primecount_version"
    echo 'algorithms=gourdon,deleglise-rivat'
    echo 'algorithms_match=true'
    echo "threads=$threads"
    echo "physical_cores=$physical_cores"
    echo "cpu_list=$cpu_list"
    echo "virtual_memory_limit_kib=$virtual_memory_limit_kib"
    echo 'gpu_used=false'
    echo 'actual_recurrence_analysis=false'
    echo "contract_sha256=$expected_contract_sha"
    echo 'count_provenance=primecount_gourdon_deleglise_rivat_match'
    echo "counts_sha256=$counts_sha256"
    echo "metrics_sha256=$metrics_sha256"
    echo "evidence_manifest_sha256=$evidence_manifest_sha256"
} > "$metadata_file"

{
    echo "counts_relative=${counts_file#"$repo_root"/}"
    echo "metadata_relative=${metadata_file#"$repo_root"/}"
    echo "preparation_log_relative=${log_file#"$repo_root"/}"
    echo "evidence_manifest_relative=${evidence_manifest#"$repo_root"/}"
} > "$ready_file"

current_stage='completed'
trap - ERR EXIT
echo '[PASS] P018 prefix exact prime-count preparation completed.'
echo "[RUN] counts=$counts_file"
echo "[RUN] metadata=$metadata_file"
echo "[RUN] ready=$ready_file"
echo '[NEXT] Exit WSL and run only one Windows P018 prefix BAT at a time.'
