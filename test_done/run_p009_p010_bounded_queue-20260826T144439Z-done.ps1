[CmdletBinding()]
param(
    [switch]$ConfirmBoundedQueue,
    [string]$P010AReplayManifest = 'Z:\FGKMT-Sono-PrimeGap-Analysis\test_result\run_20260826T100715Z_p010a_mod2310_replay\manifest.json'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmBoundedQueue) {
    throw 'The bounded P009/P010 queue requires -ConfirmBoundedQueue.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$ReplayManifest = [System.IO.Path]::GetFullPath($P010AReplayManifest)
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p009_p010_bounded_queue'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"

foreach ($Required in @($Python, $Helper, $ReplayManifest)) {
    if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) {
        throw "Required file was not found: $Required"
    }
}
New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null
. $Helper
Initialize-RunnerLogging -LogPath $LogPath -CaptureDirectory $LogDirectory -CapturePrefix $RunId
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

try {
    Set-Location -LiteralPath $ProjectRoot
    Write-RunLine '[RUN] queue=P009_P010_BOUNDED_RESEARCH_QUEUE'
    Write-RunLine '[RUN] max_wall_seconds=55800 (15h30m)'
    Write-RunLine '[RUN] max_disk_gb=50 (50000000000 bytes)'
    Write-RunLine '[RUN] cpu_only=true gpu_used=false'
    Write-RunLine '[RUN] queue_is_orchestration_only=true'
    Write-RunLine "[RUN] p010a_replay_manifest=$ReplayManifest"
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'bounded-research-queue' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.bounded_research_queue_cli',
        '--approved-by-user', '--project-root', $ProjectRoot,
        '--replay-manifest', $ReplayManifest, '--output-directory', $RunRoot,
        '--max-wall-seconds', '55800', '--max-disk-gb', '50'
    )
    Write-RunLine '[PASS] P009/P010 bounded research queue completed.'
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
