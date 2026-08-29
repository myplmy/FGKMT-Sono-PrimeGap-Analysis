[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('A_FULL', 'B_MID')]
    [string]$Mode,
    [switch]$ConfirmAfterP013B
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmAfterP013B) {
    throw 'P017 requires -ConfirmAfterP013B after the original P013-B process has ended.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$CalibrationSource = Join-Path $ProjectRoot 'source\recurrence_parallel_calibration.py'
$CalibrationCli = Join-Path $ProjectRoot 'source\recurrence_parallel_calibration_cli.py'
$ParallelSource = Join-Path $ProjectRoot 'source\parallel_segment_statistics.py'
$Records = Join-Path $ProjectRoot (
    'datas\validated\prime-gap-list-project\' +
    '1a112a1387052d9ad360686313f501c01fe46b68\maximal_gap_records.csv'
)
$P012Contract = Join-Path $ProjectRoot 'test_plan\P012_statistical_contract_v1.json'
$P013Contract = Join-Path $ProjectRoot 'test_plan\P013_recurrence_extension_contract_v1.json'
$P017Contract = Join-Path $ProjectRoot 'test_plan\P017_p013_parallel_calibration_contract_v1.json'
$P012BRoot = Join-Path $ProjectRoot 'test_result\run_20260827T121734Z_p012b_stratified_null_holdout'
$P012BManifest = Join-Path $P012BRoot 'manifest.json'
$P012BSavedReport = Join-Path $P012BRoot 'saved_verification_report.json'
$OracleRoot = Join-Path $ProjectRoot 'test_result\run_20260828T071601Z_p013a_recurrence_extension_1e11_r2'

if ($Mode -eq 'A_FULL') {
    $RunLabel = 'p017a_p013a_parallel_full_calibration'
    $TerminalLabel = 'P017-A P013-A parallel full calibration'
    $RangeText = '[10^10,10^11)'
    $SegmentCount = '32'
}
else {
    $RunLabel = 'p017b_p013b_parallel_midrange_calibration'
    $TerminalLabel = 'P017-B P013-B parallel midrange calibration'
    $RangeText = '[10^11,316227766017)'
    $SegmentCount = '64'
}

$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + "_$RunLabel"
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"
$ProgressPath = Join-Path $RunRoot 'progress.jsonl'
foreach ($Required in @(
    $Python, $Helper, $CalibrationSource, $CalibrationCli, $ParallelSource,
    $Records, $P012Contract, $P013Contract, $P017Contract,
    $P012BManifest, $P012BSavedReport,
    (Join-Path $OracleRoot 'sufficient_statistics_checkpoint.json'),
    (Join-Path $OracleRoot 'analysis.json')
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

$CommonArguments = @(
    '--mode', $Mode,
    '--records', $Records,
    '--p012-contract', $P012Contract,
    '--p013-contract', $P013Contract,
    '--p012b-manifest', $P012BManifest,
    '--p012b-saved-report', $P012BSavedReport,
    '--calibration-contract', $P017Contract,
    '--oracle-root', $OracleRoot,
    '--physical-cores', '4',
    '--logical-processors', '8'
)
$PreflightArguments = @(
    '-B', '-m', 'source.recurrence_parallel_calibration_cli', 'preflight'
) + $CommonArguments
$RunArguments = @(
    '-u', '-B', '-m', 'source.recurrence_parallel_calibration_cli', 'run',
    '--approved-by-user', '--output-directory', $RunRoot
) + $CommonArguments

try {
    Set-Location -LiteralPath $ProjectRoot
    Write-RunLine '[RUN] experiment=P017_P013_PARALLEL_ACTUAL_CALIBRATION'
    Write-RunLine "[RUN] mode=$Mode range=$RangeText"
    Write-RunLine '[RUN] execute_only_after_original_p013b_ended=true'
    Write-RunLine '[RUN] current_p013b_artifacts_read=false current_p013b_process_modified=false'
    Write-RunLine '[RUN] cpu_budget=4_physical_cores_8_logical_processes affinity=topology_enforced'
    Write-RunLine "[RUN] workers=8 segments=$SegmentCount worker_native_threads=1"
    Write-RunLine '[RUN] precision_reduced=false work_items_omitted=false'
    Write-RunLine "[RUN] live_progress_file=$ProgressPath"
    Write-RunLine '[INFO] During the long stage, inspect live progress with:'
    Write-RunLine "[INFO] while (-not (Test-Path -LiteralPath '$ProgressPath')) { Start-Sleep -Seconds 1 }; Get-Content -LiteralPath '$ProgressPath' -Wait"
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Write-RunLine "[RUN] log=$LogPath"
    Write-RunLine "[RUN] runner_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $MyInvocation.MyCommand.Path).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] calibration_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $CalibrationSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] parallel_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $ParallelSource).Hash.ToLowerInvariant())"
    Invoke-LoggedNativeStage -Name 'p017-input-preflight' -FilePath $Python `
        -Arguments $PreflightArguments
    Invoke-LoggedNativeStage -Name 'p017-targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest',
        'tests.test_parallel_segment_statistics',
        'tests.test_recurrence_parallel_calibration', '-v'
    )
    Invoke-LoggedNativeStage -Name 'p017-exact-calibration' -FilePath $Python `
        -Arguments $RunArguments
    Invoke-LoggedNativeStage -Name 'p017-saved-artifact-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.recurrence_parallel_calibration_cli', 'verify',
        '--result-directory', $RunRoot,
        '--report', (Join-Path $RunRoot 'saved_verification_report.json')
    )
    Write-RunLine "[PASS] $TerminalLabel completed."
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
