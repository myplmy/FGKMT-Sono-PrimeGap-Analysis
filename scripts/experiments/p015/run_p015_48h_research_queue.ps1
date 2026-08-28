[CmdletBinding()]
param([switch]$Confirm48h)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $Confirm48h) {
    throw 'P015 48-hour queue requires -Confirm48h.'
}
$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$QueueSource = Join-Path $ProjectRoot 'source\independent_research_queue.py'
$QueueCli = Join-Path $ProjectRoot 'source\independent_research_queue_cli.py'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p015_48h_research_queue'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"
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
    Write-RunLine '[RUN] experiment=P015_48H_INDEPENDENT_RESEARCH_QUEUE'
    Write-RunLine '[RUN] order=P013A_R2,P013B,P014'
    Write-RunLine '[RUN] child_cpu_budget=4_physical_cores_8_logical_processors'
    Write-RunLine '[RUN] child_timeouts_hours=4,20,22 global_wall_hours=47'
    Write-RunLine '[RUN] aggregate_disk_bytes=50000000000 cpu_only=true gpu_used=false'
    Write-RunLine '[RUN] queue_is_orchestration_only=true'
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'p015-queue-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_independent_research_queue', '-v'
    )
    Invoke-LoggedNativeStage -Name 'p015-bounded-research-queue' -FilePath $Python -Arguments @(
        '-u', '-B', '-m', 'source.independent_research_queue_cli', 'run',
        '--approved-by-user',
        '--project-root', $ProjectRoot,
        '--output-directory', $RunRoot,
        '--max-wall-seconds', '169200',
        '--max-disk-gb', '50'
    )
    Invoke-LoggedNativeStage -Name 'p015-saved-queue-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.independent_research_queue_cli', 'verify',
        '--result-directory', $RunRoot,
        '--report', (Join-Path $RunRoot 'saved_queue_verification_report.json')
    )
    Write-RunLine '[PASS] P015 48-hour independent research queue completed.'
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
