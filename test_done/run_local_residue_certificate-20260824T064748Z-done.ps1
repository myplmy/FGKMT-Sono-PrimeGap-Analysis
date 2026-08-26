param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('Pilot', 'Full')]
    [string]$Mode,

    [switch]$Approved,

    [string]$ReadyFile
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if (-not $Approved) {
    throw 'P008 actual feasibility experiment requires the explicit -Approved switch.'
}

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$CertificatePath = Join-Path $ProjectRoot 'ai_dev_tool\temp_prime_gap_count_algorithm\source\C2310_certificate.txt'
$RunStamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$ModeLabel = $Mode.ToLowerInvariant()
$RunId = "${RunStamp}_p008_${ModeLabel}"
$ResultDirectory = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"
$LoggingHelper = Join-Path $ProjectRoot 'scripts\powershell_stage_logging.ps1'
$CountsPath = $null
$CountMetadataPath = $null

function Resolve-ProjectRelativePath {
    param([Parameter(Mandatory = $true)][string]$RelativePath)
    if ([System.IO.Path]::IsPathRooted($RelativePath)) {
        throw "READY path must be project-relative: $RelativePath"
    }
    $ResolvedRoot = [System.IO.Path]::GetFullPath($ProjectRoot).TrimEnd('\') + '\'
    $Candidate = [System.IO.Path]::GetFullPath(
        (Join-Path $ProjectRoot ($RelativePath -replace '/', '\'))
    )
    if (-not $Candidate.StartsWith($ResolvedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "READY path escapes the project root: $Candidate"
    }
    return $Candidate
}

if ($Mode -eq 'Full') {
    if ([string]::IsNullOrWhiteSpace($ReadyFile)) {
        $ReadyFile = Join-Path $ProjectRoot 'tmp\p008-primecounts\READY.txt'
    }
    if (-not (Test-Path -LiteralPath $ReadyFile -PathType Leaf)) {
        throw "P008 prime-count READY file was not found: $ReadyFile"
    }
    $ReadyValues = @{}
    foreach ($Line in [System.IO.File]::ReadAllLines($ReadyFile)) {
        if ([string]::IsNullOrWhiteSpace($Line) -or $Line.StartsWith('#')) { continue }
        $Parts = $Line.Split('=', 2)
        if ($Parts.Count -ne 2) { throw "Malformed READY line: $Line" }
        $ReadyValues[$Parts[0]] = $Parts[1]
    }
    foreach ($RequiredKey in @('counts_relative', 'metadata_relative')) {
        if (-not $ReadyValues.ContainsKey($RequiredKey)) {
            throw "READY file lacks $RequiredKey"
        }
    }
    $CountsPath = Resolve-ProjectRelativePath $ReadyValues['counts_relative']
    $CountMetadataPath = Resolve-ProjectRelativePath $ReadyValues['metadata_relative']
}

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
    Write-RunLine '[RUN] scope=P008_LOCAL_RESIDUE_STATE_CERTIFICATE'
    Write-RunLine "[RUN] id=$RunId"
    Write-RunLine "[RUN] mode=$ModeLabel"
    Write-RunLine '[RUN] threshold_gap=1856'
    Write-RunLine '[RUN] boundary=start_[A,B)_with_explicit_right_crossing'
    Write-RunLine "[RUN] python=$Python"
    Write-RunLine '[RUN] gpu_used=false'
    Write-RunLine '[RUN] actual_prime_search=false'
    Write-RunLine '[RUN] representative_sweep_is_coverage_ledger=false'
    Write-RunLine '[RUN] direct_search_acceleration_claimed=false'
    if ($Mode -eq 'Full') {
        Write-RunLine "[RUN] ready_file=$ReadyFile"
        Write-RunLine "[RUN] counts_path=$CountsPath"
        Write-RunLine "[RUN] count_metadata_path=$CountMetadataPath"
    }

    if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
        throw "Fixed FGKMT Python was not found: $Python"
    }
    if (-not (Test-Path -LiteralPath $CertificatePath -PathType Leaf)) {
        throw "Reviewed certificate was not found: $CertificatePath"
    }
    if ($Mode -eq 'Full') {
        if (-not (Test-Path -LiteralPath $CountsPath -PathType Leaf)) {
            throw "Prime-count CSV was not found: $CountsPath"
        }
        if (-not (Test-Path -LiteralPath $CountMetadataPath -PathType Leaf)) {
            throw "Prime-count metadata was not found: $CountMetadataPath"
        }
    }
    if (Test-Path -LiteralPath $ResultDirectory) {
        throw "Refusing to overwrite result directory: $ResultDirectory"
    }
    Set-Location -LiteralPath $ProjectRoot

    $PreflightArguments = @(
        '-B', '-m', 'source.local_residue_certificate_cli', 'preflight',
        '--mode', $ModeLabel,
        '--certificate-path', $CertificatePath
    )
    if ($Mode -eq 'Full') {
        $PreflightArguments += @(
            '--counts-path', $CountsPath,
            '--count-metadata-path', $CountMetadataPath
        )
    }
    Invoke-LoggedNativeStage -Name 'preflight' -FilePath $Python -Arguments $PreflightArguments

    Invoke-LoggedNativeStage -Name 'unit-tests' -FilePath $Python -Arguments @(
        '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'
    )

    $RunArguments = @(
        '-B', '-m', 'source.local_residue_certificate_cli', 'run',
        '--mode', $ModeLabel,
        '--certificate-path', $CertificatePath,
        '--output-directory', $ResultDirectory,
        '--approved-by-user'
    )
    if ($Mode -eq 'Full') {
        $RunArguments += @(
            '--counts-path', $CountsPath,
            '--count-metadata-path', $CountMetadataPath
        )
    }
    Invoke-LoggedNativeStage -Name 'approved-local-bound-analysis' -FilePath $Python -Arguments $RunArguments

    Invoke-LoggedNativeStage -Name 'saved-artifact-verification' -FilePath $Python -Arguments @(
        '-B', '-m', 'source.local_residue_certificate_cli', 'verify',
        '--result-directory', $ResultDirectory
    )

    Write-RunLine '[PASS] P008 local-certificate feasibility run completed.'
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
