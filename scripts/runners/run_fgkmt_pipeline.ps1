[CmdletBinding()]
param(
    [switch]$Approved,
    [string]$Commit = "",
    [string]$RunId = "",
    [string]$AnalysisLimit = "100000000000000000000"
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if (-not $Approved) {
    throw 'Actual FGKMT dataset/analysis execution requires -Approved.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$LoggingHelper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$RunStamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$EffectiveRunId = if ($RunId) { $RunId } else { "${RunStamp}_autohead" }
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$EffectiveRunId.log"

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Required FGKMT Python was not found: $Python"
}
if (-not (Test-Path -LiteralPath $LoggingHelper -PathType Leaf)) {
    throw "Shared logging helper was not found: $LoggingHelper"
}
New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null
. $LoggingHelper
Initialize-RunnerLogging -LogPath $LogPath -CaptureDirectory $LogDirectory `
    -CapturePrefix $EffectiveRunId
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

try {
    Set-Location -LiteralPath $ProjectRoot
    $script:RunnerCurrentStage = 'preconditions'
    Write-RunLine '[RUN] scope=FGKMT_CANONICAL_PIPELINE'
    Write-RunLine "[RUN] id=$EffectiveRunId"
    Write-RunLine "[RUN] python=$Python"
    Write-RunLine "[RUN] analysis_limit=$AnalysisLimit"
    Write-RunLine "[RUN] commit=$Commit"

    Invoke-LoggedNativeStage -Name 'preflight' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.cli', 'preflight'
    )
    $Arguments = @(
        '-B', '-m', 'source.cli', 'run',
        '--approved-by-user',
        '--analysis-limit', $AnalysisLimit,
        '--run-id', $EffectiveRunId
    )
    if ($Commit) { $Arguments += @('--commit', $Commit) }
    Invoke-LoggedNativeStage -Name 'approved-pipeline' -FilePath $Python `
        -Arguments $Arguments
    Write-RunLine '[PASS] canonical FGKMT pipeline completed.'
    Write-RunLine "[RUN] log=$LogPath"
}
catch {
    try {
        Write-RunnerFailure -ErrorRecord $_
        Write-RunLine "[RUN] log=$LogPath"
    }
    catch {
        Write-Error "Runner failure logging also failed: $($_ | Out-String)"
    }
    exit 1
}

exit 0
