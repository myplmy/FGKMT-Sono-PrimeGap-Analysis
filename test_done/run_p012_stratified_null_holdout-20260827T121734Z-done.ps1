[CmdletBinding()]
param(
    [switch]$ConfirmP012B
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP012B) {
    throw 'P012-B independent holdout analysis requires -ConfirmP012B.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$AnalysisSource = Join-Path $ProjectRoot 'source\recurrence_stratified_holdout.py'
$CliSource = Join-Path $ProjectRoot 'source\recurrence_stratified_holdout_cli.py'
$Records = Join-Path $ProjectRoot (
    'datas\validated\prime-gap-list-project\' +
    '1a112a1387052d9ad360686313f501c01fe46b68\maximal_gap_records.csv'
)
$FrozenContract = Join-Path $ProjectRoot 'test_plan\P012_statistical_contract_v1.json'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p012b_stratified_null_holdout'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"

foreach ($Required in @(
    $Python,
    $Helper,
    $AnalysisSource,
    $CliSource,
    $Records,
    $FrozenContract
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

try {
    Set-Location -LiteralPath $ProjectRoot
    Write-RunLine '[RUN] experiment=P012B_LOGX_STRATIFIED_CONDITIONAL_NULL_HOLDOUT'
    Write-RunLine '[RUN] phase=P012-B independent holdout [10^9,10^10)'
    Write-RunLine '[RUN] development_data_used_for_holdout_inference=false'
    Write-RunLine '[RUN] plateau_selection=complete_record_start_and_next_start_inside_holdout'
    Write-RunLine '[RUN] excluded=left_censored_continuation,right_censored_final_plateau'
    Write-RunLine '[RUN] primary_bins=width0.5_shift0 sensitivity=shift0.25,width1_shift0.5'
    Write-RunLine '[RUN] primary_statistic=family_max_absolute_z secondary=enrichment_BH'
    Write-RunLine '[RUN] zero_variance_z=undefined; plot=x_marker; not_z_zero=true'
    Write-RunLine '[RUN] replications=100000 seed=20260827'
    Write-RunLine '[RUN] expected_gap_starts=404204977'
    Write-RunLine '[RUN] saved_verification=second_full_holdout_recomputation'
    Write-RunLine '[RUN] cpu_only=true gpu_used=false'
    Write-RunLine "[RUN] runner_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $MyInvocation.MyCommand.Path).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] analysis_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $AnalysisSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] cli_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $CliSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] records_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $Records).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] frozen_contract_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $FrozenContract).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'p012b-input-preflight' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.recurrence_stratified_holdout_cli', 'preflight',
        '--records', $Records,
        '--frozen-contract', $FrozenContract,
        '--segment-span', '50000000'
    )
    Invoke-LoggedNativeStage -Name 'p012b-targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest',
        'tests.test_recurrence_stratified_holdout',
        'tests.test_recurrence_stratified_null',
        'tests.test_recurrence_null_model',
        'tests.test_plateau_recurrence', '-v'
    )
    Invoke-LoggedNativeStage -Name 'p012b-holdout-analysis' -FilePath $Python -Arguments @(
        '-u', '-B', '-m', 'source.recurrence_stratified_holdout_cli', 'analyze',
        '--approved-by-user',
        '--records', $Records,
        '--frozen-contract', $FrozenContract,
        '--output-directory', $RunRoot,
        '--segment-span', '50000000',
        '--replications', '100000',
        '--seed', '20260827'
    )
    Invoke-LoggedNativeStage -Name 'p012b-saved-full-recomputation' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.recurrence_stratified_holdout_cli', 'verify',
        '--result-directory', $RunRoot,
        '--report', (Join-Path $RunRoot 'saved_verification_report.json')
    )
    Write-RunLine '[PASS] P012-B independent stratified-null holdout completed.'
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
