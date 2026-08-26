[CmdletBinding()]
param([switch]$ConfirmP009Adapter)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP009Adapter) {
    throw 'P009 PARI adapter validation requires -ConfirmP009Adapter.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p009_pari_adapter_validation'
$RunRoot = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
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
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

try {
    Set-Location -LiteralPath $ProjectRoot
    Write-RunLine '[RUN] scope=P009_PARI_ADAPTER_TOY_INTERMEDIATE_ONLY'
    Write-RunLine '[RUN] actual_1e20_experiment=false'
    Write-RunLine '[RUN] subjects=101,1000000000000000000000000000057'
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'preflight' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.pari_certificate_cli', 'preflight'
    )
    Invoke-LoggedNativeStage -Name 'targeted-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_pari_certificate',
        'tests.test_boundary_witness', '-v'
    )
    Invoke-LoggedNativeStage -Name 'adapter-generation-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.pari_certificate_cli', 'validate-adapter',
        '--approved-by-user', '--output-directory', $RunRoot,
        '--timeout-seconds', '900'
    )
    Invoke-LoggedNativeStage -Name 'saved-artifact-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.pari_certificate_cli', 'verify-adapter',
        '--result-directory', $RunRoot, '--timeout-seconds', '900'
    )
    Write-RunLine '[PASS] P009 PARI adapter validation completed.'
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
