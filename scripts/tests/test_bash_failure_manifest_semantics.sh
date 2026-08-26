#!/usr/bin/env bash
set -Eeuo pipefail

task_tmp="$(mktemp -d -t fgkmt-errexit-toy-XXXXXX)"
cleanup() {
    case "$task_tmp" in
        /tmp/fgkmt-errexit-toy-*) rm -rf -- "$task_tmp" ;;
        *) return 97 ;;
    esac
}
trap cleanup EXIT

manifest="$task_tmp/manifest.failed.txt"
continued="$task_tmp/continued.txt"
failure_written=0
write_failed_manifest() {
    local exit_code="$1"
    if (( failure_written != 0 )); then return 0; fi
    failure_written=1
    (
        set +e
        trap - ERR
        printf 'status=FAILED\nexit_code=%s\n' "$exit_code" > "$manifest"
    )
}
on_error() {
    local exit_code="$1"
    write_failed_manifest "$exit_code"
}

set +e
(
    set -Eeuo pipefail
    trap 'on_error "$?"' ERR
    false
    : > "$continued"
)
child_exit="$?"
set -e

if [[ "$child_exit" -eq 0 ]]; then
    echo 'BASH_ERREXIT_TOY_FAIL child unexpectedly passed' >&2
    exit 3
fi
if [[ ! -f "$manifest" ]]; then
    echo 'BASH_ERREXIT_TOY_FAIL failure manifest missing' >&2
    exit 4
fi
if [[ -e "$continued" ]]; then
    echo 'BASH_ERREXIT_TOY_FAIL command after failure executed' >&2
    exit 5
fi
grep -q '^status=FAILED$' "$manifest"
echo 'BASH_ERREXIT_MANIFEST_TOY_PASS'
