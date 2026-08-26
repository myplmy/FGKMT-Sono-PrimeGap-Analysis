[CmdletBinding()]
param(
    [switch]$ConfirmP010AExactLift,
    [Parameter(Mandatory = $true)][string]$P010AReplayManifest,
    [Parameter(Mandatory = $true)][string]$P010BScanManifest
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP010AExactLift) {
    throw 'P010A modulus-30030 exact lift requires -ConfirmP010AExactLift.'
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
$ScanManifest = [System.IO.Path]::GetFullPath($P010BScanManifest)
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p010a_mod30030_exact_lift'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"

foreach ($Required in @($Python, $Helper, $Certificate, $ReplayManifest, $ScanManifest)) {
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
    Write-RunLine '[RUN] experiment=P010A_MOD30030_EXACT_LIFT'
    Write-RunLine '[RUN] scope=unchanged-bound exact certificate feasibility baseline'
    Write-RunLine '[RUN] lp_solve=false'
    Write-RunLine '[RUN] direct_prime_search=false'
    Write-RunLine '[RUN] disk_cap_bytes=50000000000'
    Write-RunLine '[RUN] full_constraint_matrix_materialized=false'
    Write-RunLine "[RUN] p010a_replay_manifest=$ReplayManifest"
    Write-RunLine "[RUN] p010b_scan_manifest=$ScanManifest"
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_finite_gap_certificate',
        'tests.test_finite_gap_separation', 'tests.test_finite_gap_replay', '-v'
    )
    Invoke-LoggedNativeStage -Name 'mod30030-exact-lift' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_replay_cli', 'lift-30030-exact',
        '--approved-by-user', '--certificate', $Certificate,
        '--replay-manifest', $ReplayManifest, '--scan-manifest', $ScanManifest,
        '--output-directory', $RunRoot, '--chunk-rows', '64'
    )
    Invoke-LoggedNativeStage -Name 'saved-artifact-exact-reverification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_replay_cli', 'verify-lift',
        '--result-directory', $RunRoot, '--report',
        (Join-Path $RunRoot 'saved_verification_report.json')
    )
    Write-RunLine '[PASS] P010A modulus-30030 exact lift completed.'
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
