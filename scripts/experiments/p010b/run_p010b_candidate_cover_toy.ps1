[CmdletBinding()]
param(
    [switch]$ConfirmToy
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmToy) {
    throw 'P010B synthetic candidate-cover verifier requires -ConfirmToy.'
}

$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$Helper = Join-Path $ProjectRoot 'scripts\common\powershell_stage_logging.ps1'
$AnalysisSource = Join-Path $ProjectRoot 'source\candidate_cover.py'
$CliSource = Join-Path $ProjectRoot 'source\candidate_cover_cli.py'
$RunId = ([DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')) + '_p010b_candidate_cover_toy'
$ArtifactRoot = Join-Path $ProjectRoot 'tmp\p010b-candidate-cover'
$RunRoot = Join-Path $ArtifactRoot $RunId
$LogPath = Join-Path $ArtifactRoot "run_$RunId.log"

foreach ($Required in @($Python, $Helper, $AnalysisSource, $CliSource)) {
    if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) {
        throw "Required file was not found: $Required"
    }
}
New-Item -ItemType Directory -Path $ArtifactRoot -Force | Out-Null
. $Helper
Initialize-RunnerLogging -LogPath $LogPath -CaptureDirectory $ArtifactRoot `
    -CapturePrefix $RunId
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

try {
    Set-Location -LiteralPath $ProjectRoot
    Write-RunLine '[RUN] experiment=P010B_EXACT_CANDIDATE_COVER_GATE'
    Write-RunLine '[RUN] mode=synthetic_toy_no_actual_prime_search'
    Write-RunLine '[RUN] range=[1000,10000) threshold=20'
    Write-RunLine '[RUN] generator=exhaustive_toy_oracle acceleration_eligible=false'
    Write-RunLine '[RUN] gpu_used=false'
    Write-RunLine "[RUN] runner_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $MyInvocation.MyCommand.Path).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] analysis_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $AnalysisSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] cli_source_sha256=$((Get-FileHash -Algorithm SHA256 -LiteralPath $CliSource).Hash.ToLowerInvariant())"
    Write-RunLine "[RUN] result_directory=$RunRoot"
    Invoke-LoggedNativeStage -Name 'p010b-candidate-cover-unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'tests.test_candidate_cover', '-v'
    )
    Invoke-LoggedNativeStage -Name 'p010b-candidate-cover-toy' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.candidate_cover_cli', 'toy',
        '--output-directory', $RunRoot,
        '--a', '1000',
        '--b', '10000',
        '--threshold', '20'
    )
    Invoke-LoggedNativeStage -Name 'p010b-candidate-cover-saved-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.candidate_cover_cli', 'verify',
        '--result-directory', $RunRoot,
        '--report', (Join-Path $RunRoot 'saved_verification_report.json')
    )
    Write-RunLine '[PASS] P010B candidate-cover toy verifier completed.'
    Write-RunLine '[RUN] acceleration_proved=false'
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
