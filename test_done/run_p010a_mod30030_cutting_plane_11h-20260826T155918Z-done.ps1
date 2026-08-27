[CmdletBinding()]
param(
    [switch]$ConfirmP010AG4
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP010AG4) {
    throw 'P010A G4 actual cutting-plane requires -ConfirmP010AG4.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$ExactLiftManifest = Join-Path $ProjectRoot 'test_result\run_20260826T144450Z_p010a_mod30030_exact_lift\manifest.json'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p010a_mod30030_cutting_plane_11h'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"

foreach ($Required in @($Python, $Helper, $ExactLiftManifest)) {
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
    Write-RunLine '[RUN] experiment=P010A_MOD30030_CUTTING_PLANE'
    Write-RunLine '[RUN] objective=count_upper_bound_only'
    Write-RunLine '[RUN] direct_prime_search=false direct_search_acceleration_proved=false'
    Write-RunLine '[RUN] max_wall_seconds=39600 (11h)'
    Write-RunLine '[RUN] per_solve_time_limit_seconds=1800 (30m)'
    Write-RunLine '[RUN] max_working_constraints=250000 full_matrix_materialized=false'
    Write-RunLine '[RUN] max_disk_bytes=50000000000 cpu_only=true gpu_used=false'
    Write-RunLine "[RUN] exact_lift_manifest=$ExactLiftManifest"
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'exact-lift-preflight' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_cutting_plane_cli', 'preflight',
        '--exact-lift-manifest', $ExactLiftManifest
    )
    Invoke-LoggedNativeStage -Name 'targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_finite_gap_cutting_plane',
        'tests.test_finite_gap_separation', 'tests.test_finite_gap_replay', '-v'
    )
    Invoke-LoggedNativeStage -Name 'mod30030-cutting-plane' -FilePath $Python -Arguments @(
        '-u', '-B', '-m', 'source.finite_gap_cutting_plane_cli', 'run',
        '--approved-by-user', '--exact-lift-manifest', $ExactLiftManifest,
        '--output-directory', $RunRoot,
        '--max-wall-seconds', '39600',
        '--per-solve-time-limit-seconds', '1800',
        '--max-iterations', '100',
        '--seed-constraint-count', '20000',
        '--add-per-iteration', '10000',
        '--max-working-constraints', '250000',
        '--max-disk-bytes', '50000000000',
        '--chunk-rows', '64'
    )
    Invoke-LoggedNativeStage -Name 'saved-artifact-exact-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_cutting_plane_cli', 'verify',
        '--result-directory', $RunRoot,
        '--report', (Join-Path $RunRoot 'saved_verification_report.json')
    )
    Write-RunLine '[PASS] P010A modulus-30030 cutting-plane run completed.'
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
