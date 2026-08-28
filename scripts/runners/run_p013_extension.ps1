[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][ValidateSet('A', 'B')][string]$Stage,
    [switch]$ConfirmP013
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP013) {
    throw 'P013 prospective recurrence extension requires -ConfirmP013.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$AnalysisSource = Join-Path $ProjectRoot 'source\recurrence_sequential_extension.py'
$CliSource = Join-Path $ProjectRoot 'source\recurrence_sequential_extension_cli.py'
$Records = Join-Path $ProjectRoot (
    'datas\validated\prime-gap-list-project\' +
    '1a112a1387052d9ad360686313f501c01fe46b68\maximal_gap_records.csv'
)
$P012Contract = Join-Path $ProjectRoot 'test_plan\P012_statistical_contract_v1.json'
$P013Contract = Join-Path $ProjectRoot 'test_plan\P013_recurrence_extension_contract_v1.json'
$P012BRoot = Join-Path $ProjectRoot 'test_result\run_20260827T121734Z_p012b_stratified_null_holdout'
$P012BManifest = Join-Path $P012BRoot 'manifest.json'
$P012BSavedReport = Join-Path $P012BRoot 'saved_verification_report.json'

if ($Stage -eq 'A') {
    $RunLabel = 'p013a_recurrence_extension_1e11_r2'
    $RangeText = '[10^10,10^11)'
    $ExpectedGapStarts = '3663002302'
    $Seed = '20260828'
    $TerminalLabel = 'P013-A prospective recurrence extension r2'
}
else {
    $RunLabel = 'p013b_recurrence_extension_1e12'
    $RangeText = '[10^11,10^12)'
    $ExpectedGapStarts = '33489857205'
    $Seed = '20260829'
    $TerminalLabel = 'P013-B prospective recurrence extension'
}

$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + "_$RunLabel"
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"
foreach ($Required in @(
    $Python, $Helper, $AnalysisSource, $CliSource, $Records,
    $P012Contract, $P013Contract, $P012BManifest, $P012BSavedReport
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
$CheckpointDirectory = Join-Path $ProjectRoot 'tmp\p013-checkpoints'
$CheckpointPath = Join-Path $CheckpointDirectory (
    "p013$($Stage.ToLowerInvariant())_sufficient_statistics_v2.json"
)

try {
    Set-Location -LiteralPath $ProjectRoot
    Write-RunLine '[RUN] experiment=P013_PROSPECTIVE_STRATIFIED_RECURRENCE_EXTENSION'
    Write-RunLine "[RUN] stage=$Stage range=$RangeText"
    Write-RunLine "[RUN] expected_gap_starts=$ExpectedGapStarts"
    Write-RunLine "[RUN] replications=100000 seed=$Seed bonferroni_alpha=0.025"
    Write-RunLine '[RUN] p012_rules_frozen=true post_result_pooling=false'
    Write-RunLine '[RUN] saved_verification=second_full_range_recomputation'
    Write-RunLine '[RUN] cpu_only=true gpu_used=false'
    Write-RunLine '[RUN] cpu_budget=4_physical_cores_8_logical_processors affinity=topology_enforced'
    Write-RunLine '[RUN] p013_compute_parallelism=single_python_stream thread_pool_ceiling=8'
    Write-RunLine "[RUN] sufficient_statistics_checkpoint=$CheckpointPath"
    Write-RunLine "[RUN] checkpoint_preexisting=$((Test-Path -LiteralPath $CheckpointPath -PathType Leaf).ToString().ToLowerInvariant())"
    Write-RunLine "[RUN] runner_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $MyInvocation.MyCommand.Path).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] analysis_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $AnalysisSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] cli_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $CliSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name "p013$($Stage.ToLowerInvariant())-input-preflight" -FilePath $Python -Arguments @(
        '-B', '-m', 'source.recurrence_sequential_extension_cli', 'preflight',
        '--stage', $Stage,
        '--records', $Records,
        '--p012-contract', $P012Contract,
        '--p013-contract', $P013Contract,
        '--p012b-manifest', $P012BManifest,
        '--p012b-saved-report', $P012BSavedReport,
        '--segment-span', '50000000',
        '--physical-cores', '4',
        '--logical-processors', '8'
    )
    Invoke-LoggedNativeStage -Name 'p013-targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest',
        'tests.test_recurrence_sequential_extension',
        'tests.test_recurrence_stratified_holdout',
        'tests.test_recurrence_stratified_null', '-v'
    )
    Invoke-LoggedNativeStage -Name "p013$($Stage.ToLowerInvariant())-analysis" -FilePath $Python -Arguments @(
        '-u', '-B', '-m', 'source.recurrence_sequential_extension_cli', 'analyze',
        '--approved-by-user',
        '--stage', $Stage,
        '--records', $Records,
        '--p012-contract', $P012Contract,
        '--p013-contract', $P013Contract,
        '--p012b-manifest', $P012BManifest,
        '--p012b-saved-report', $P012BSavedReport,
        '--output-directory', $RunRoot,
        '--checkpoint-path', $CheckpointPath,
        '--segment-span', '50000000',
        '--physical-cores', '4',
        '--logical-processors', '8'
    )
    Invoke-LoggedNativeStage -Name "p013$($Stage.ToLowerInvariant())-saved-full-recomputation" -FilePath $Python -Arguments @(
        '-u', '-B', '-m', 'source.recurrence_sequential_extension_cli', 'verify',
        '--result-directory', $RunRoot,
        '--report', (Join-Path $RunRoot 'saved_verification_report.json'),
        '--physical-cores', '4',
        '--logical-processors', '8'
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
