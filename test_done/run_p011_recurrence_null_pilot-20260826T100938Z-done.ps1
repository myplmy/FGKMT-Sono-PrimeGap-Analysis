[CmdletBinding()]
param([switch]$ConfirmP011)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP011) {
    throw 'P011 recurrence null-model pilot requires -ConfirmP011.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$P006Root = Join-Path $ProjectRoot 'test_result\run_20260824T065339Z_p006_full_1000000000'
$Complete = Join-Path $P006Root 'tables\complete_plateaus.csv'
$Histogram = Join-Path $P006Root 'tables\gap_histogram.csv'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p011_recurrence_null_pilot'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"

foreach ($Required in @($Python, $Helper, $Complete, $Histogram)) {
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
    Write-RunLine '[RUN] experiment=P011_P006_RECURRENCE_NULL_MODEL'
    Write-RunLine '[RUN] source=P006 full [2,10^9] saved tables'
    Write-RunLine '[RUN] model=leave-plateau-out diagnostic binomial'
    Write-RunLine '[RUN] monte_carlo_replications=20000 seed=20260826'
    Write-RunLine '[RUN] theorem_claimed=false'
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'input-preflight' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.recurrence_null_model_cli', 'preflight',
        '--complete-plateaus', $Complete, '--gap-histogram', $Histogram
    )
    Invoke-LoggedNativeStage -Name 'targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_recurrence_null_model', '-v'
    )
    Invoke-LoggedNativeStage -Name 'null-model-analysis' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.recurrence_null_model_cli', 'analyze',
        '--approved-by-user', '--complete-plateaus', $Complete,
        '--gap-histogram', $Histogram, '--output-directory', $RunRoot,
        '--replications', '20000', '--seed', '20260826'
    )
    Invoke-LoggedNativeStage -Name 'saved-artifact-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.recurrence_null_model_cli', 'verify',
        '--result-directory', $RunRoot
    )
    Write-RunLine '[PASS] P011 recurrence null-model pilot completed.'
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Write-RunLine "[RUN] log=$LogPath"
}
catch {
    try {
        Write-RunnerFailure -ErrorRecord $_
        Write-RunLine "[RUN] log=$LogPath"
    }
    catch { Write-Error "Runner failure logging also failed: $($_ | Out-String)" }
    exit 1
}
exit 0
