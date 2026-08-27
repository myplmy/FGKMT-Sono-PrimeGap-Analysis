[CmdletBinding()]
param(
    [switch]$ConfirmP012A
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP012A) {
    throw 'P012-A actual development-range analysis requires -ConfirmP012A.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$P006Root = Join-Path $ProjectRoot 'test_result\run_20260824T065339Z_p006_full_1000000000'
$P011Root = Join-Path $ProjectRoot 'test_result\run_20260826T100938Z_p011_recurrence_null_pilot'
$CompletePlateaus = Join-Path $P006Root 'tables\complete_plateaus.csv'
$P011Statistics = Join-Path $P011Root 'plateau_null_statistics.csv'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p012a_stratified_null_development'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"

foreach ($Required in @($Python, $Helper, $CompletePlateaus, $P011Statistics)) {
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
    Write-RunLine '[RUN] experiment=P012_P011_LOGX_STRATIFIED_CONDITIONAL_NULL'
    Write-RunLine '[RUN] phase=P012-A development range [2,10^9]'
    Write-RunLine '[RUN] holdout_range=[10^9,10^10] touched=false'
    Write-RunLine '[RUN] primary_bins=width0.5_shift0 sensitivity=shift0.25,width1_shift0.5'
    Write-RunLine '[RUN] primary_statistic=family_max_absolute_z secondary=enrichment_BH'
    Write-RunLine '[RUN] replications=100000 seed=20260827'
    Write-RunLine '[RUN] cpu_only=true gpu_used=false'
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'p012-input-preflight' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.recurrence_stratified_null_cli', 'preflight',
        '--complete-plateaus', $CompletePlateaus,
        '--p011-statistics', $P011Statistics,
        '--analysis-limit', '1000000000',
        '--segment-span', '50000000'
    )
    Invoke-LoggedNativeStage -Name 'p012-targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_recurrence_stratified_null',
        'tests.test_recurrence_null_model', 'tests.test_plateau_recurrence', '-v'
    )
    Invoke-LoggedNativeStage -Name 'p012-development-analysis' -FilePath $Python -Arguments @(
        '-u', '-B', '-m', 'source.recurrence_stratified_null_cli', 'analyze',
        '--approved-by-user',
        '--complete-plateaus', $CompletePlateaus,
        '--p011-statistics', $P011Statistics,
        '--output-directory', $RunRoot,
        '--analysis-limit', '1000000000',
        '--segment-span', '50000000',
        '--replications', '100000',
        '--seed', '20260827'
    )
    Invoke-LoggedNativeStage -Name 'p012-saved-full-recomputation' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.recurrence_stratified_null_cli', 'verify',
        '--result-directory', $RunRoot,
        '--report', (Join-Path $RunRoot 'saved_verification_report.json')
    )
    Write-RunLine '[PASS] P012-A stratified conditional null development run completed.'
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
