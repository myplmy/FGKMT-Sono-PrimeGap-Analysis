[CmdletBinding()]
param([switch]$ConfirmP014R3)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP014R3) {
    throw 'P014-R3 modulus-510510 parallel staged experiment requires -ConfirmP014R3.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$LiveTee = Join-Path $ProjectRoot 'scripts\common\live_native_tee.py'
$AnalysisSource = Join-Path $ProjectRoot 'source\finite_gap_mod510510.py'
$ParallelSource = Join-Path $ProjectRoot 'source\finite_gap_parallel_exact_scan.py'
$CliSource = Join-Path $ProjectRoot 'source\finite_gap_mod510510_cli.py'
$ProgressSource = Join-Path $ProjectRoot 'source\live_progress.py'
$G4Root = Join-Path $ProjectRoot 'test_result\run_20260826T155918Z_p010a_mod30030_cutting_plane_11h'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p014r3_mod510510_parallel_staged_certificate'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"
$AnalysisProgressPath = Join-Path $LogDirectory "$RunId.p014r3-analysis.progress.jsonl"
$VerificationProgressPath = Join-Path $LogDirectory "$RunId.p014r3-serial-verification.progress.jsonl"

if (-not (Test-Path -LiteralPath $Helper -PathType Leaf)) {
    throw "Runner logging helper was not found: $Helper"
}
New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null
. $Helper
Initialize-RunnerLogging -LogPath $LogPath -CaptureDirectory $LogDirectory `
    -CapturePrefix $RunId
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:OMP_NUM_THREADS = '8'
$env:OPENBLAS_NUM_THREADS = '8'
$env:MKL_NUM_THREADS = '8'
$env:NUMEXPR_NUM_THREADS = '8'
$env:VECLIB_MAXIMUM_THREADS = '8'
$env:BLIS_NUM_THREADS = '8'

try {
    Set-Location -LiteralPath $ProjectRoot
    foreach ($Required in @(
        $Python, $LiveTee, $AnalysisSource, $ParallelSource, $CliSource, $ProgressSource,
        (Join-Path $G4Root 'manifest.json'),
        (Join-Path $G4Root 'saved_verification_report.json'),
        (Join-Path $G4Root 'best_certificate_mod30030.txt')
    )) {
        if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) {
            throw "Required file was not found: $Required"
        }
    }
    Write-RunLine '[RUN] experiment=P014R3_MOD510510_PARALLEL_STAGED_CERTIFICATE'
    Write-RunLine '[RUN] revision_reason=windows_powershell_5p1_json_argv_quote_loss_fixed_by_base64_transport'
    Write-RunLine '[RUN] objective=count_upper_bound_only direct_prime_search=false'
    Write-RunLine '[RUN] modulus=510510 states=92160 constraints=8524288932 threshold=1856'
    Write-RunLine '[RUN] stage_a=parallel_exact_lift_full_scan gate_seconds=14400'
    Write-RunLine '[RUN] stage_b=conditional_working_set max_iterations=12 max_working=100000'
    Write-RunLine '[RUN] final_exact_backend=parallel saved_recomputation_backend=serial'
    Write-RunLine '[RUN] max_analysis_wall_seconds=54000 per_solve_seconds=1800'
    Write-RunLine '[RUN] max_disk_bytes=10000000000 full_matrix_materialized=false'
    Write-RunLine '[RUN] cpu_only=true gpu_used=false search_acceleration_proved=false'
    Write-RunLine '[RUN] cpu_budget=4_physical_cores_8_logical_processors affinity=topology_enforced'
    Write-RunLine '[RUN] exact_scan_workers=8 worker_native_thread_ceiling=1 row_block_rows=64'
    Write-RunLine '[RUN] python_live_heartbeat_seconds=300 durable_fsync=true'
    Write-RunLine '[RUN] live_transport=utf8_json_base64 powershell_5p1_regression_tested=true'
    Write-RunLine "[RUN] analysis_progress_log=$AnalysisProgressPath"
    Write-RunLine "[RUN] serial_verification_progress_log=$VerificationProgressPath"
    Write-RunLine "[RUN] runner_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $MyInvocation.MyCommand.Path).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] powershell_helper_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $Helper).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] live_tee_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $LiveTee).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] analysis_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $AnalysisSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] parallel_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $ParallelSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] cli_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $CliSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] progress_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $ProgressSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] result_directory=$RunRoot"

    Invoke-LiveLoggedNativeStage -Name 'p014r3-prerequisite-resource-preflight' -FilePath $Python -BrokerPythonPath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_mod510510_cli', 'preflight',
        '--g4-result-directory', $G4Root,
        '--chunk-rows', '64',
        '--exact-scan-backend', 'parallel',
        '--exact-scan-workers', '8',
        '--physical-cores', '4',
        '--logical-processors', '8'
    )
    Invoke-LiveLoggedNativeStage -Name 'p014r3-targeted-unit-tests' -FilePath $Python -BrokerPythonPath $Python -Arguments @(
        '-B', '-m', 'unittest',
        'tests.test_finite_gap_mod510510',
        'tests.test_finite_gap_parallel_exact_scan',
        'tests.test_finite_gap_cutting_plane',
        'tests.test_finite_gap_separation',
        'tests.test_finite_gap_replay',
        'tests.test_live_native_tee', '-v'
    )
    Invoke-LiveLoggedNativeStage -Name 'p014r3-parallel-staged-analysis' -FilePath $Python -BrokerPythonPath $Python -Arguments @(
        '-u', '-B', '-m', 'source.finite_gap_mod510510_cli', 'run',
        '--approved-by-user',
        '--g4-result-directory', $G4Root,
        '--output-directory', $RunRoot,
        '--max-wall-seconds', '54000',
        '--stage-a-gate-seconds', '14400',
        '--per-solve-time-limit-seconds', '1800',
        '--max-iterations', '12',
        '--seed-constraint-count', '5000',
        '--add-per-iteration', '5000',
        '--max-working-constraints', '100000',
        '--max-disk-bytes', '10000000000',
        '--chunk-rows', '64',
        '--exact-scan-backend', 'parallel',
        '--exact-scan-workers', '8',
        '--physical-cores', '4',
        '--logical-processors', '8',
        '--progress-log', $AnalysisProgressPath,
        '--heartbeat-seconds', '300',
        '--live-console'
    )
    Invoke-LiveLoggedNativeStage -Name 'p014r3-saved-full-serial-recomputation' -FilePath $Python -BrokerPythonPath $Python -Arguments @(
        '-u', '-B', '-m', 'source.finite_gap_mod510510_cli', 'verify',
        '--result-directory', $RunRoot,
        '--report', (Join-Path $RunRoot 'saved_verification_report.json'),
        '--chunk-rows', '64',
        '--physical-cores', '4',
        '--logical-processors', '8',
        '--progress-log', $VerificationProgressPath,
        '--heartbeat-seconds', '300',
        '--live-console'
    )
    Write-RunLine '[PASS] P014-R3 parallel modulus-510510 staged certificate experiment completed.'
    Write-RunLine '[RUN] independent_saved_recomputation=serial_exact_oracle'
    Write-RunLine '[RUN] search_acceleration_proved=false'
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Write-RunLine "[RUN] log=$LogPath"
}
catch {
    try {
        Write-RunnerFailure -ErrorRecord $_
        Write-RunLine "[RUN] partial_result_directory=$RunRoot"
        Write-RunLine "[RUN] log=$LogPath"
    }
    catch { Write-Error "Runner failure logging also failed: $($_ | Out-String)" }
    exit 1
}
exit 0
