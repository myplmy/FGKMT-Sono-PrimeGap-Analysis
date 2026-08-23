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

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Fixed FGKMT Python was not found: $Python"
}
if (-not (Test-Path -LiteralPath $CertificatePath -PathType Leaf)) {
    throw "Reviewed certificate was not found: $CertificatePath"
}
if (Test-Path -LiteralPath $ResultDirectory) {
    throw "Refusing to overwrite result directory: $ResultDirectory"
}
if (Test-Path -LiteralPath $LogPath) {
    throw "Refusing to overwrite log: $LogPath"
}

Set-Location -LiteralPath $ProjectRoot
New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null

function Write-RunLine {
    param([Parameter(Mandatory = $true)][string]$Message)
    Write-Host $Message
    Add-Content -LiteralPath $LogPath -Value $Message -Encoding UTF8
}

function Copy-CapturedOutput {
    param([Parameter(Mandatory = $true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return
    }
    foreach ($Line in Get-Content -LiteralPath $Path) {
        Write-RunLine $Line
    }
}

function Invoke-PythonStage {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )
    Write-RunLine "[STAGE] $Name"
    $SafeName = $Name -replace '[^A-Za-z0-9_-]', '_'
    $StdoutPath = Join-Path $LogDirectory "$RunId.$SafeName.stdout.tmp"
    $StderrPath = Join-Path $LogDirectory "$RunId.$SafeName.stderr.tmp"
    if ((Test-Path -LiteralPath $StdoutPath) -or (Test-Path -LiteralPath $StderrPath)) {
        throw "Refusing to overwrite stage capture for '$Name'."
    }
    try {
        # Start-Process keeps normal native stderr (including unittest -v output)
        # out of PowerShell's error stream.  This avoids the Windows PowerShell
        # 5.1 NativeCommandError failure that stopped the first P006 pilot.
        $Process = Start-Process -FilePath $Python -ArgumentList $Arguments `
            -Wait -PassThru -NoNewWindow `
            -RedirectStandardOutput $StdoutPath `
            -RedirectStandardError $StderrPath
        $StageExit = $Process.ExitCode
        Copy-CapturedOutput -Path $StdoutPath
        Copy-CapturedOutput -Path $StderrPath
    }
    finally {
        if (Test-Path -LiteralPath $StdoutPath) {
            Remove-Item -LiteralPath $StdoutPath -Force
        }
        if (Test-Path -LiteralPath $StderrPath) {
            Remove-Item -LiteralPath $StderrPath -Force
        }
    }
    if ($StageExit -ne 0) {
        throw "Stage '$Name' failed with exit code $StageExit."
    }
    Write-RunLine "[PASS] $Name"
}

Write-RunLine '[RUN] scope=P007_FINITE_RANGE_RESIDUE_STATE_CERTIFICATE'
Write-RunLine "[RUN] id=$RunId"
Write-RunLine "[RUN] mode=$ModeLabel"
Write-RunLine '[RUN] range_start_bounded=[10^20,10^21)'
Write-RunLine '[RUN] threshold_gap=1856'
Write-RunLine "[RUN] python=$Python"
Write-RunLine '[RUN] gpu_used=false'
Write-RunLine '[RUN] actual_prime_search=false'
Write-RunLine '[RUN] direct_search_acceleration_claimed=false'

Invoke-PythonStage -Name 'preflight' -Arguments @(
    '-B', '-m', 'source.finite_gap_certificate_cli', 'preflight',
    '--certificate-path', $CertificatePath,
    '--mode', $ModeLabel
)

Invoke-PythonStage -Name 'unit-tests' -Arguments @(
    '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'
)

if ($Mode -eq 'Pilot') {
    Invoke-PythonStage -Name 'approved-supplied-certificate-audit' -Arguments @(
        '-B', '-m', 'source.finite_gap_certificate_cli', 'audit',
        '--certificate-path', $CertificatePath,
        '--output-directory', $ResultDirectory,
        '--approved-by-user'
    )
}
else {
    Invoke-PythonStage -Name 'approved-small-modulus-comparison' -Arguments @(
        '-B', '-m', 'source.finite_gap_certificate_cli', 'compare',
        '--moduli', '30,210,2310',
        '--output-directory', $ResultDirectory,
        '--solve-constraint-cap', '1000000',
        '--approved-by-user'
    )
}

Invoke-PythonStage -Name 'saved-artifact-verification' -Arguments @(
    '-B', '-m', 'source.finite_gap_certificate_cli', 'verify',
    '--result-directory', $ResultDirectory
)

Write-RunLine '[PASS] P007 certificate experiment and saved-artifact verification completed.'
Write-RunLine "[RUN] result_directory=$ResultDirectory"
Write-RunLine "[RUN] log=$LogPath"

