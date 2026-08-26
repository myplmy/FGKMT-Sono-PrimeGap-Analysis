param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Pilot', 'Full')]
    [string]$Mode,

    [switch]$Approved
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if (-not $Approved) {
    throw 'P007 actual certificate experiment requires the explicit -Approved switch.'
}

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$CertificatePath = Join-Path $ProjectRoot 'ai_dev_tool\temp_prime_gap_count_algorithm\source\C2310_certificate.txt'
$RunStamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$ModeLabel = $Mode.ToLowerInvariant()
$RunId = "${RunStamp}_p007_${ModeLabel}"
$ResultDirectory = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"
$LoggingHelper = Join-Path $ProjectRoot 'scripts\powershell_stage_logging.ps1'

if (-not (Test-Path -LiteralPath $LoggingHelper -PathType Leaf)) {
    throw "Shared runner logging helper was not found: $LoggingHelper"
}
New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null
. $LoggingHelper
Initialize-RunnerLogging -LogPath $LogPath -CaptureDirectory $LogDirectory `
    -CapturePrefix $RunId
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

try {
    $script:RunnerCurrentStage = 'preconditions'
    Write-RunLine '[RUN] scope=P007_FINITE_RANGE_RESIDUE_STATE_CERTIFICATE'
    Write-RunLine "[RUN] id=$RunId"
    Write-RunLine "[RUN] mode=$ModeLabel"
    Write-RunLine '[RUN] range_start_bounded=[10^20,10^21)'
    Write-RunLine '[RUN] threshold_gap=1856'
    Write-RunLine "[RUN] python=$Python"
    Write-RunLine '[RUN] gpu_used=false'
    Write-RunLine '[RUN] actual_prime_search=false'
    Write-RunLine '[RUN] direct_search_acceleration_claimed=false'

    if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
        throw "Fixed FGKMT Python was not found: $Python"
    }
    if (-not (Test-Path -LiteralPath $CertificatePath -PathType Leaf)) {
        throw "Reviewed certificate was not found: $CertificatePath"
    }
    if (Test-Path -LiteralPath $ResultDirectory) {
        throw "Refusing to overwrite result directory: $ResultDirectory"
    }
    Set-Location -LiteralPath $ProjectRoot

Invoke-LoggedNativeStage -Name 'preflight' -FilePath $Python -Arguments @(
    '-B', '-m', 'source.finite_gap_certificate_cli', 'preflight',
    '--certificate-path', $CertificatePath,
    '--mode', $ModeLabel
)

Invoke-LoggedNativeStage -Name 'unit-tests' -FilePath $Python -Arguments @(
    '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'
)

if ($Mode -eq 'Pilot') {
    Invoke-LoggedNativeStage -Name 'approved-supplied-certificate-audit' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_certificate_cli', 'audit',
        '--certificate-path', $CertificatePath,
        '--output-directory', $ResultDirectory,
        '--approved-by-user'
    )
}
else {
    Invoke-LoggedNativeStage -Name 'approved-small-modulus-comparison' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.finite_gap_certificate_cli', 'compare',
        '--moduli', '30,210,2310',
        '--output-directory', $ResultDirectory,
        '--solve-constraint-cap', '1000000',
        '--approved-by-user'
    )
}

Invoke-LoggedNativeStage -Name 'saved-artifact-verification' -FilePath $Python -Arguments @(
    '-B', '-m', 'source.finite_gap_certificate_cli', 'verify',
    '--result-directory', $ResultDirectory
)

Write-RunLine '[PASS] P007 certificate experiment and saved-artifact verification completed.'
Write-RunLine "[RUN] result_directory=$ResultDirectory"
Write-RunLine "[RUN] log=$LogPath"

}
catch {
    try {
        Write-RunnerFailure -ErrorRecord $_
        Write-RunLine "[RUN] result_directory=$ResultDirectory"
        Write-RunLine "[RUN] log=$LogPath"
    }
    catch {
        Write-Error "Runner failure logging also failed: $($_ | Out-String)"
    }
    exit 1
}

exit 0
