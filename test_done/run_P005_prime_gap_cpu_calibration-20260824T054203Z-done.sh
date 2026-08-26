#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${1:-}" != "--confirm-cpu" || "$#" -ne 1 ]]; then
    echo "Usage: bash ./run_P005_prime_gap_cpu_calibration.sh --confirm-cpu" >&2
    echo "This authorizes only the bounded CPU calibration, not Rank 85-to-86 exhaustive coverage." >&2
    exit 2
fi

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
helper="$script_dir/scripts/run_prime_gap_cpu_calibration.sh"
if [[ ! -f "$helper" ]]; then
    echo "[FAIL] Missing helper: $helper" >&2
    exit 3
fi
if [[ ! -f "$script_dir/AGENTS.md" ]]; then
    echo "[FAIL] This script must be run from a complete project checkout." >&2
    exit 4
fi

run_stamp="$(date -u +%Y%m%dT%H%M%SZ)"
log_file="$script_dir/test_result/logs/run_${run_stamp}_p005_prime_gap_cpu_calibration.log"
if [[ -e "$log_file" ]]; then
    echo "[FAIL] Refusing to overwrite existing log: $log_file" >&2
    exit 5
fi
mkdir -p "$(dirname "$log_file")"
: > "$log_file"
exec > >(tee -a "$log_file") 2>&1


echo "[INFO] WSL-native execution; no Windows path translation is used."
echo "[INFO] CPU-only, 8-thread ceiling, 30 GiB hard virtual-memory limit."
echo "[INFO] This is a correctness/performance calibration in m*P#/d coordinates."
echo "[INFO] It is not arbitrary x-range exhaustive coverage."
echo "[INFO] Log: $log_file"

exec bash "$helper" --approved "$script_dir" "$log_file" --log-already-open
