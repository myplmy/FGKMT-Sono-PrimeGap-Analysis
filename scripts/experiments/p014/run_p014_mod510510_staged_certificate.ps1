[CmdletBinding()]
param([switch]$ConfirmP014)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP014) {
    throw 'P014 modulus-510510 staged experiment requires -ConfirmP014.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$AnalysisSource = Join-Path $ProjectRoot 'source\finite_gap_mod510510.py'
$CliSource = Join-Path $ProjectRoot 'source\finite_gap_mod510510_cli.py'
$ProgressSource = Join-Path $ProjectRoot 'source\live_progress.py'
$G4Root = Join-Path $ProjectRoot 'test_result\run_20260826T155918Z_p010a_mod30030_cutting_plane_11h'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p014_mod510510_staged_certificate'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"
$AnalysisProgressPath = Join-Path $LogDirectory "$RunId.p014-analysis.progress.jsonl"
$VerificationProgressPath = Join-Path $LogDirectory "$RunId.p014-verification.progress.jsonl"
foreach ($Required in @(
    $Python, $Helper, $AnalysisSource, $CliSource, $ProgressSource,
    (Join-Path $G4Root 'manifest.json'),
    (Join-Path $G4Root 'saved_verification_report.json'),
    (Join-Path $G4Root 'best_certificate_mod30030.txt')
)) {
    if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) {
        throw "Required file was not found: $Required"
    }
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
    Write-RunLine '[RUN] experiment=P014_MOD510510_STAGED_CERTIFICATE'
    Write-RunLine '[RUN] objective=count_upper_bound_only direct_prime_search=false'
    Write-RunLine '[RUN] modulus=510510 states=92160 constraints=8524288932 threshold=1856'
    Write-RunLine '[RUN] stage_a=exact_lift_full_scan gate_seconds=14400'
    Write-RunLine '[RUN] stage_b=conditional_working_set max_iterations=12 max_working=100000'
    Write-RunLine '[RUN] max_wall_seconds=54000 per_solve_seconds=1800'
    Write-RunLine '[RUN] max_disk_bytes=10000000000 full_matrix_materialized=false'
    Write-RunLine '[RUN] cpu_only=true gpu_used=false search_acceleration_proved=false'
    Write-RunLine '[RUN] cpu_budget=4_physical_cores_8_logical_processors affinity=topology_enforced'
    Write-RunLine '[RUN] p014_scan_parallelism=single_python_stream highs_thread_pool_ceiling=8'
    Write-RunLine '[RUN] python_live_heartbeat_seconds=300 durable_fsync=true'
    Write-RunLine "[RUN] analysis_progress_log=$AnalysisProgressPath"
    Write-RunLine "[RUN] verification_progress_log=$VerificationProgressPath"
    Write-RunLine "[RUN] runner_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $MyInvocation.MyCommand.Path).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] analysis_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $AnalysisSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] cli_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $CliSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] progress_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $ProgressSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'p014-prerequisite-resource-preflight' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_mod510510_cli', 'preflight',
        '--g4-result-directory', $G4Root,
        '--chunk-rows', '64',
        '--physical-cores', '4',
        '--logical-processors', '8',
        '--progress-log', $AnalysisProgressPath,
        '--heartbeat-seconds', '300',
        '--live-console'
    )
    Invoke-LoggedNativeStage -Name 'p014-targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest',
        'tests.test_finite_gap_mod510510',
        'tests.test_finite_gap_cutting_plane',
        'tests.test_finite_gap_separation',
        'tests.test_finite_gap_replay', '-v'
    )
    Invoke-LoggedNativeStage -Name 'p014-staged-analysis' -FilePath $Python -Arguments @(
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
        '--physical-cores', '4',
        '--logical-processors', '8',
        '--progress-log', $VerificationProgressPath,
        '--heartbeat-seconds', '300',
        '--live-console'
    )
    Invoke-LoggedNativeStage -Name 'p014-saved-full-exact-recomputation' -FilePath $Python -Arguments @(
        '-u', '-B', '-m', 'source.finite_gap_mod510510_cli', 'verify',
        '--result-directory', $RunRoot,
        '--report', (Join-Path $RunRoot 'saved_verification_report.json'),
        '--chunk-rows', '64',
        '--physical-cores', '4',
        '--logical-processors', '8'
    )
    Write-RunLine '[PASS] P014 modulus-510510 staged certificate experiment completed.'
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
