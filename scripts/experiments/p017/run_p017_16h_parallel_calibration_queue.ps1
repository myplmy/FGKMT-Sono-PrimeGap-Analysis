[CmdletBinding()]
param([switch]$ConfirmAfterP013B)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmAfterP013B) {
    throw 'P017 16-hour queue requires -ConfirmAfterP013B.'
}
$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$QueueSource = Join-Path $ProjectRoot 'source\p013_parallel_calibration_queue.py'
$QueueCli = Join-Path $ProjectRoot 'source\p013_parallel_calibration_queue_cli.py'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p017_16h_p013_parallel_calibration_queue'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"
$QueueLivePath = Join-Path $RunRoot 'live_console.log'
foreach ($Required in @($Python, $Helper, $QueueSource, $QueueCli)) {
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
    Write-RunLine '[RUN] experiment=P017_16H_P013_PARALLEL_CALIBRATION_QUEUE'
    Write-RunLine '[RUN] execute_only_after_original_p013b_ended=true'
    Write-RunLine '[RUN] order=P017A_A_FULL,P017B_B_MID'
    Write-RunLine '[RUN] child_timeouts_hours=4,11 child_cap_sum_hours=15 global_wall_hours=16'
    Write-RunLine '[RUN] aggregate_disk_bytes=5000000000 cpu_only=true gpu_used=false'
    Write-RunLine '[RUN] continue_after_child_failure=true queue_is_orchestration_only=true'
    Write-RunLine "[RUN] queue_live_file=$QueueLivePath"
    Write-RunLine '[INFO] During the queue, inspect live child output with:'
    Write-RunLine "[INFO] while (-not (Test-Path -LiteralPath '$QueueLivePath')) { Start-Sleep -Seconds 1 }; Get-Content -LiteralPath '$QueueLivePath' -Wait"
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Write-RunLine "[RUN] log=$LogPath"
    Invoke-LoggedNativeStage -Name 'p017-queue-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_p013_parallel_calibration_queue', '-v'
    )
    Invoke-LoggedNativeStage -Name 'p017-bounded-calibration-queue' -FilePath $Python -Arguments @(
        '-u', '-B', '-m', 'source.p013_parallel_calibration_queue_cli', 'run',
        '--approved-by-user',
        '--project-root', $ProjectRoot,
        '--output-directory', $RunRoot,
        '--max-wall-seconds', '57600',
        '--max-disk-gb', '5'
    )
    Invoke-LoggedNativeStage -Name 'p017-saved-queue-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.p013_parallel_calibration_queue_cli', 'verify',
        '--result-directory', $RunRoot,
        '--report', (Join-Path $RunRoot 'saved_queue_verification_report.json')
    )
    Write-RunLine '[PASS] P017 16-hour P013 parallel calibration queue completed.'
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
