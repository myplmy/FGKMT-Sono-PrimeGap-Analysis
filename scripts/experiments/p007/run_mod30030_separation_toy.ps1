[CmdletBinding()]
param([switch]$ConfirmToy)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmToy) {
    throw 'P007 separation toy verification requires -ConfirmToy.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p007_separation_toy'
$LogDirectory = Join-Path $ProjectRoot 'tmp\p007-separation\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Fixed FGKMT Python was not found: $Python"
}
if (-not (Test-Path -LiteralPath $Helper -PathType Leaf)) {
    throw "Shared logging helper was not found: $Helper"
}
New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null
. $Helper
Initialize-RunnerLogging -LogPath $LogPath -CaptureDirectory $LogDirectory `
    -CapturePrefix $RunId

try {
    Set-Location -LiteralPath $ProjectRoot
    Write-RunLine '[RUN] scope=P007_MOD30030_SEPARATION_DESIGN_TOY'
    Write-RunLine '[RUN] mod30030_scan=false'
    Write-RunLine '[RUN] mod30030_lp_solve=false'
    Invoke-LoggedNativeStage -Name 'preflight-estimate-only' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_separation_cli', 'preflight',
        '--chunk-rows', '64', '--top-k', '1000'
    )
    Invoke-LoggedNativeStage -Name 'targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_finite_gap_separation', '-v'
    )
    Invoke-LoggedNativeStage -Name 'mod30-toy-oracle' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_separation_cli', 'toy',
        '--modulus', '30', '--threshold', '12'
    )
    Write-RunLine '[PASS] P007 separation-oracle toy verification completed.'
    Write-RunLine "[RUN] log=$LogPath"
}
catch {
    try { Write-RunnerFailure -ErrorRecord $_ }
    catch { Write-Error "Runner failure logging also failed: $($_ | Out-String)" }
    exit 1
}
exit 0
