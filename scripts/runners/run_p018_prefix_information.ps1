[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][ValidateSet('P0', 'A')][string]$Mode,
    [switch]$ConfirmP018Prefix
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP018Prefix) {
    throw 'P018 prefix information probe requires -ConfirmP018Prefix.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$LiveTee = Join-Path $ProjectRoot 'scripts\common\live_native_tee.py'
$AnalysisSource = Join-Path $ProjectRoot 'source\recurrence_prefix_information.py'
$CliSource = Join-Path $ProjectRoot 'source\recurrence_prefix_information_cli.py'
$DualSource = Join-Path $ProjectRoot 'source\parallel_dual_partition.py'
$ParallelSource = Join-Path $ProjectRoot 'source\parallel_segment_statistics.py'
$HoldoutSource = Join-Path $ProjectRoot 'source\recurrence_stratified_holdout.py'
$NullSource = Join-Path $ProjectRoot 'source\recurrence_stratified_null.py'
$PowerSource = Join-Path $ProjectRoot 'source\recurrence_information_preflight.py'
$RecordSource = Join-Path $ProjectRoot 'source\plateau_recurrence.py'
$ResourceSource = Join-Path $ProjectRoot 'source\runtime_resources.py'
$ProgressSource = Join-Path $ProjectRoot 'source\live_progress.py'
$Records = Join-Path $ProjectRoot (
    'datas\validated\prime-gap-list-project\' +
    '1a112a1387052d9ad360686313f501c01fe46b68\maximal_gap_records.csv'
)
$Contract = Join-Path $ProjectRoot 'test_plan\P018_prefix_information_probe_contract_v1.json'
$Ready = Join-Path $ProjectRoot 'tmp\p018-prefix-primecounts\READY.txt'
if ($Mode -eq 'P0') {
    $RunLabel = 'p018p0_prefix_information_calibration'
    $RangeText = '[1346294310749,1408695493610)'
    $CompleteRecords = '51'
    $Segments = '16/17'
    $HardWallSeconds = '7200'
    $TerminalLabel = 'P018-P0 prefix information calibration'
}
else {
    $RunLabel = 'p018a_prefix_information_probe'
    $RangeText = '[1000000000000,1968188556462)'
    $CompleteRecords = '51,52'
    $Segments = '64/65'
    $HardWallSeconds = '43200'
    $TerminalLabel = 'P018-A blinded prefix information probe'
}
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + "_$RunLabel"
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"
$ProgressPath = Join-Path $LogDirectory "$RunId.progress.jsonl"
$Mutex = $null
$MutexAcquired = $false
$RunnerExit = 0

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
    $Mutex = [System.Threading.Mutex]::new(
        $false, 'Local\FGKMT_Sono_P018_Prefix_Information'
    )
    try {
        $MutexAcquired = $Mutex.WaitOne(0, $false)
    }
    catch [System.Threading.AbandonedMutexException] {
        $MutexAcquired = $true
    }
    if (-not $MutexAcquired) {
        throw 'Another P018 P0/A prefix run is already active.'
    }
    foreach ($Required in @(
        $Python, $LiveTee, $AnalysisSource, $CliSource, $DualSource,
        $ParallelSource, $HoldoutSource, $NullSource, $PowerSource,
        $RecordSource, $ResourceSource, $ProgressSource, $Records, $Contract, $Ready
    )) {
        if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) {
            throw "Required file was not found: $Required"
        }
    }
    Write-RunLine '[RUN] experiment=P018_PREFIX_INFORMATION_PROBE'
    Write-RunLine "[RUN] mode=$Mode range=$RangeText complete_records=$CompleteRecords"
    Write-RunLine "[RUN] dual_partition_segments=$Segments full_parallel_passes=2 serial_oracle=false"
    Write-RunLine "[RUN] hard_wall_seconds=$HardWallSeconds max_disk_bytes=5000000000"
    Write-RunLine '[RUN] gate_reads=population,gap_counts,exposure_counts observed_recurrence_read=false'
    Write-RunLine '[RUN] hypothesis_test=false figures=false automatic_full_range_promotion=false'
    Write-RunLine '[RUN] cpu_budget=4_physical_cores_8_logical_processors worker_processes=8'
    Write-RunLine '[RUN] windows_job_memory_limit_bytes=31500000000 disk_free_preflight_bytes=5000000000'
    Write-RunLine '[RUN] mutual_exclusion=Local\FGKMT_Sono_P018_Prefix_Information'
    Write-RunLine '[RUN] cpu_only=true gpu_used=false worker_native_thread_ceiling=1'
    Write-RunLine '[RUN] independent_gap_count=primecount_gourdon_deleglise_rivat_match'
    Write-RunLine '[RUN] live_transport=utf8_json_base64 heartbeat_seconds=300'
    Write-RunLine "[RUN] progress_log=$ProgressPath"
    Write-RunLine "[RUN] runner_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $MyInvocation.MyCommand.Path).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] powershell_helper_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $Helper).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] live_tee_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $LiveTee).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] analysis_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $AnalysisSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] cli_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $CliSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] dual_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $DualSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] parallel_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $ParallelSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] holdout_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $HoldoutSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] null_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $NullSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] power_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $PowerSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] record_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $RecordSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] resource_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $ResourceSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] progress_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $ProgressSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] contract_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $Contract).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] result_directory=$RunRoot"

    Invoke-LiveLoggedNativeStage -Name "p018-$($Mode.ToLowerInvariant())-input-preflight" -FilePath $Python -BrokerPythonPath $Python -Arguments @(
        '-B', '-m', 'source.recurrence_prefix_information_cli', 'preflight',
        '--mode', $Mode,
        '--records', $Records,
        '--contract', $Contract,
        '--ready-file', $Ready,
        '--project-root', $ProjectRoot,
        '--physical-cores', '4',
        '--logical-processors', '8'
    )
    Invoke-LiveLoggedNativeStage -Name 'p018-prefix-targeted-unit-tests' -FilePath $Python -BrokerPythonPath $Python -Arguments @(
        '-B', '-m', 'unittest',
        'tests.test_recurrence_prefix_information',
        'tests.test_parallel_dual_partition',
        'tests.test_parallel_segment_statistics',
        'tests.test_runtime_resources',
        'tests.test_live_native_tee', '-v'
    )
    Invoke-LiveLoggedNativeStage -Name "p018-$($Mode.ToLowerInvariant())-dual-partition-analysis" -FilePath $Python -BrokerPythonPath $Python -Arguments @(
        '-u', '-B', '-m', 'source.recurrence_prefix_information_cli', 'run',
        '--approved-by-user',
        '--mode', $Mode,
        '--records', $Records,
        '--contract', $Contract,
        '--ready-file', $Ready,
        '--project-root', $ProjectRoot,
        '--output-directory', $RunRoot,
        '--progress-log', $ProgressPath,
        '--heartbeat-seconds', '300',
        '--live-console',
        '--physical-cores', '4',
        '--logical-processors', '8'
    )
    Invoke-LiveLoggedNativeStage -Name "p018-$($Mode.ToLowerInvariant())-saved-blinded-recomputation" -FilePath $Python -BrokerPythonPath $Python -Arguments @(
        '-B', '-m', 'source.recurrence_prefix_information_cli', 'verify',
        '--result-directory', $RunRoot,
        '--report', (Join-Path $RunRoot 'saved_verification_report.json')
    )
    Write-RunLine "[PASS] $TerminalLabel completed."
    Write-RunLine '[RUN] observed_recurrence_saved=false hypothesis_test_performed=false'
    Write-RunLine '[RUN] automatic_full_range_promotion=false'
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
    $RunnerExit = 1
}
finally {
    if ($MutexAcquired -and $null -ne $Mutex) {
        $Mutex.ReleaseMutex()
    }
    if ($null -ne $Mutex) {
        $Mutex.Dispose()
    }
}
exit $RunnerExit
