[CmdletBinding()]
param(
    [switch]$ConfirmP009Actual,
    [Parameter(Mandatory = $true)]
    [string]$P010AReplayManifest
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP009Actual) {
    throw 'P009 single-block actual run requires -ConfirmP009Actual.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$Bounds = Join-Path $ProjectRoot 'test_result\run_20260824T064748Z_p008_full\local_block_bounds.csv'
$AdapterManifest = Join-Path $ProjectRoot 'test_result\run_20260826T090950Z_p009_pari_adapter_validation\manifest.json'
$ReplayManifest = [System.IO.Path]::GetFullPath($P010AReplayManifest)
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p009_single_block_actual'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"

foreach ($Required in @($Python, $Helper, $Bounds, $AdapterManifest, $ReplayManifest)) {
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
    Write-RunLine '[RUN] experiment=P009_SINGLE_BLOCK_BOUNDARY_ACTUAL'
    Write-RunLine '[RUN] block=[100000000000000000000,100000000000000001000)'
    Write-RunLine '[RUN] threshold=1856 (equality included as large)'
    Write-RunLine '[RUN] direct_full_range_search=false'
    Write-RunLine "[RUN] p010a_replay_manifest=$ReplayManifest"
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'prerequisite-preflight' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.boundary_witness_pari_cli', 'preflight',
        '--local-bounds', $Bounds, '--adapter-manifest', $AdapterManifest,
        '--replay-manifest', $ReplayManifest
    )
    Invoke-LoggedNativeStage -Name 'targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_boundary_witness',
        'tests.test_pari_certificate', 'tests.test_boundary_witness_pari', '-v'
    )
    Invoke-LoggedNativeStage -Name 'single-block-pari-certificate' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.boundary_witness_pari_cli', 'run',
        '--approved-by-user', '--local-bounds', $Bounds,
        '--adapter-manifest', $AdapterManifest, '--replay-manifest', $ReplayManifest,
        '--output-directory', $RunRoot, '--timeout-seconds', '900'
    )
    Write-RunLine '[PASS] P009 single-block actual feasibility completed.'
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
