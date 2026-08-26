[CmdletBinding()]
param(
    [switch]$ConfirmP010B,
    [Parameter(Mandatory = $true)]
    [string]$P010AReplayManifest
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP010B) {
    throw 'P010B modulus-30030 one-candidate scan requires -ConfirmP010B.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$Certificate = Join-Path $ProjectRoot 'test_result\run_20260824T090010Z_p007_full\certificate_mod2310.txt'
$ReplayManifest = [System.IO.Path]::GetFullPath($P010AReplayManifest)
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p010b_mod30030_candidate_scan'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"

foreach ($Required in @($Python, $Helper, $Certificate, $ReplayManifest)) {
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
    Write-RunLine '[RUN] experiment=P010B_MOD30030_ONE_CANDIDATE_SCAN'
    Write-RunLine '[RUN] scope=search-acceleration prerequisite cost scan'
    Write-RunLine '[RUN] lp_solve=false'
    Write-RunLine '[RUN] direct_prime_search=false'
    Write-RunLine "[RUN] p010a_replay_manifest=$ReplayManifest"
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'certificate-preflight' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_replay_cli', 'preflight',
        '--certificate', $Certificate
    )
    Invoke-LoggedNativeStage -Name 'targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_finite_gap_separation',
        'tests.test_finite_gap_replay', '-v'
    )
    Invoke-LoggedNativeStage -Name 'mod30030-one-candidate-scan' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_replay_cli', 'scan-30030',
        '--approved-by-user', '--certificate', $Certificate,
        '--replay-manifest', $ReplayManifest, '--output-directory', $RunRoot,
        '--chunk-rows', '64', '--top-k', '1000'
    )
    Invoke-LoggedNativeStage -Name 'saved-artifact-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_replay_cli', 'verify-scan',
        '--result-directory', $RunRoot
    )
    Write-RunLine '[PASS] P010B modulus-30030 one-candidate scan completed.'
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
