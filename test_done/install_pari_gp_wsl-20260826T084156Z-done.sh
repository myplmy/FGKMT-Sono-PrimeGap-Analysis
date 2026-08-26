#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${1:-}" != "--confirm-install" || "$#" -ne 1 ]]; then
    echo "Usage: bash ./scripts/setup/install_pari_gp_wsl.sh --confirm-install" >&2
    echo "This installs the Ubuntu pari-gp package; it does not run P009." >&2
    exit 2
fi

if [[ ! -r /proc/version ]] || ! grep -qi microsoft /proc/version; then
    echo "[STOP] This helper is intended for Ubuntu under WSL." >&2
    exit 3
fi
for command_name in sudo apt-get tee date grep; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        echo "[STOP] Missing required command: $command_name" >&2
        exit 4
    fi
done

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
repo_root="$(cd -- "$script_dir/../.." && pwd -P)"
run_stamp="$(date -u +%Y%m%dT%H%M%SZ)"
log_dir="$repo_root/tmp/setup"
log_file="$log_dir/install_pari_gp_${run_stamp}.log"
mkdir -p "$log_dir"
if [[ -e "$log_file" ]]; then
    echo "[STOP] Refusing to overwrite log: $log_file" >&2
    exit 5
fi
: > "$log_file"
exec > >(tee -a "$log_file") 2>&1

echo '[RUN] scope=PARI_GP_WSL_INSTALL'
echo '[RUN] package=pari-gp'
echo '[RUN] P009_experiment_executed=false'
sudo apt-get update
sudo apt-get install -y pari-gp
if ! command -v gp >/dev/null 2>&1; then
    echo '[FAIL] gp executable not found after package installation.' >&2
    exit 6
fi
gp --version
smoke_output="$(printf 'c=primecert(101); print(primecertisvalid(c)); quit\n' | gp -q)"
if ! grep -qx '1' <<<"$smoke_output"; then
    echo "[FAIL] PARI certificate smoke test failed: $smoke_output" >&2
    exit 7
fi
echo '[PASS] PARI/GP installed and primecert verification smoke test passed.'
echo "[RUN] log=$log_file"
