[CmdletBinding()]
param([switch]$ConfirmP010A)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP010A) {
    throw 'P010A modulus-2310 replay requires -ConfirmP010A.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$Certificate = Join-Path $ProjectRoot 'test_result\run_20260824T090010Z_p007_full\certificate_mod2310.txt'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p010a_mod2310_replay'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"

foreach ($Required in @($Python, $Helper, $Certificate)) {
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
    Write-RunLine '[RUN] experiment=P010A_MOD2310_REPLAY'
    Write-RunLine '[RUN] scope=count-upper-bound certificate replay'
    Write-RunLine '[RUN] direct_prime_search=false'
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'preflight' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_replay_cli', 'preflight',
        '--certificate', $Certificate
    )
    Invoke-LoggedNativeStage -Name 'targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_finite_gap_certificate',
        'tests.test_finite_gap_separation', 'tests.test_finite_gap_replay', '-v'
    )
    Invoke-LoggedNativeStage -Name 'mod2310-exact-replay' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_replay_cli', 'replay-2310',
        '--approved-by-user', '--certificate', $Certificate,
        '--output-directory', $RunRoot, '--chunk-rows', '64', '--top-k', '100'
    )
    Invoke-LoggedNativeStage -Name 'saved-artifact-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_replay_cli', 'verify-replay',
        '--result-directory', $RunRoot, '--report',
        (Join-Path $RunRoot 'saved_verification_report.json')
    )
    Write-RunLine '[PASS] P010A modulus-2310 replay completed.'
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
