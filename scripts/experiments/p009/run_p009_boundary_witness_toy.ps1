[CmdletBinding()]
param([switch]$ConfirmToy)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmToy) {
    throw 'P009 toy verification requires -ConfirmToy. It does not authorize the 10^20 pilot.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p009_toy'
$RunRoot = Join-Path $ProjectRoot "tmp\p009-toy\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'tmp\p009-toy\logs'
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
    Write-RunLine '[RUN] scope=P009_BOUNDARY_WITNESS_TOY_ONLY'
    Write-RunLine '[RUN] actual_1e20_experiment=false'
    Write-RunLine '[RUN] pari_required=false'
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'preflight' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.boundary_witness_cli', 'preflight'
    )
    Invoke-LoggedNativeStage -Name 'targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_boundary_witness', '-v'
    )
    Invoke-LoggedNativeStage -Name 'toy-generation' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.boundary_witness_cli', 'toy',
        '--output-directory', $RunRoot
    )
    Invoke-LoggedNativeStage -Name 'saved-artifact-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.boundary_witness_cli', 'verify',
        '--result-directory', $RunRoot
    )
    Write-RunLine '[PASS] P009 toy boundary-witness verification completed.'
    Write-RunLine "[RUN] log=$LogPath"
}
catch {
    try { Write-RunnerFailure -ErrorRecord $_ }
    catch { Write-Error "Runner failure logging also failed: $($_ | Out-String)" }
    exit 1
}
exit 0
