param(
    [Parameter(Mandatory = $true)]
    [ValidateSet(100000000, 1000000000, 10000000000)]
    [Int64]$AnalysisLimit,

    [Parameter(Mandatory = $true)]
    [ValidateRange(1000000, 200000000)]
    [Int64]$SegmentSpan,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^p006_[a-z0-9_]+$')]
    [string]$RunLabel,

    [switch]$Approved
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if (-not $Approved) {
    throw 'P006 actual analysis requires the explicit -Approved switch.'
}

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
$SourceCommit = '1a112a1387052d9ad360686313f501c01fe46b68'
$RecordsPath = Join-Path $ProjectRoot "datas\validated\prime-gap-list-project\$SourceCommit\maximal_gap_records.csv"
$RunStamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$RunId = "${RunStamp}_${RunLabel}"
$ResultDirectory = Join-Path $ProjectRoot "test_result\run_$RunId"
$LogDirectory = Join-Path $ProjectRoot 'test_result\logs'
$LogPath = Join-Path $LogDirectory "run_$RunId.log"

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Fixed FGKMT Python was not found: $Python"
}
if (-not (Test-Path -LiteralPath $RecordsPath -PathType Leaf)) {
    throw "Pinned validated records were not found: $RecordsPath"
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
    $Message | Tee-Object -FilePath $LogPath -Append
}

function Invoke-PythonStage {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )
    Write-RunLine "[STAGE] $Name"
    & $Python @Arguments 2>&1 | Tee-Object -FilePath $LogPath -Append
    $StageExit = $LASTEXITCODE
    if ($StageExit -ne 0) {
        throw "Stage '$Name' failed with exit code $StageExit."
    }
    Write-RunLine "[PASS] $Name"
}

Write-RunLine '[RUN] scope=P006_MAXIMAL_GAP_PLATEAU_RECURRENCE'
Write-RunLine "[RUN] id=$RunId"
Write-RunLine "[RUN] analysis_limit=$AnalysisLimit"
Write-RunLine "[RUN] segment_span=$SegmentSpan"
Write-RunLine "[RUN] python=$Python"
Write-RunLine "[RUN] source_commit=$SourceCommit"
Write-RunLine '[RUN] gpu_used=false'
Write-RunLine '[RUN] generator=windows_numpy_odd_only_segmented_sieve'
Write-RunLine '[RUN] boundary=end_[e_k,e_(k+1)); exposure=start_[s_k,s_(k+1))'

Invoke-PythonStage -Name 'preflight' -Arguments @(
    '-m', 'source.plateau_recurrence_cli', 'preflight',
    '--records-path', $RecordsPath,
    '--analysis-limit', "$AnalysisLimit",
    '--segment-span', "$SegmentSpan"
)

Invoke-PythonStage -Name 'unit-tests' -Arguments @(
    '-m', 'unittest', 'discover', '-s', 'tests', '-v'
)

Invoke-PythonStage -Name 'approved-analysis' -Arguments @(
    '-m', 'source.plateau_recurrence_cli', 'analyze',
    '--records-path', $RecordsPath,
    '--output-directory', $ResultDirectory,
    '--analysis-limit', "$AnalysisLimit",
    '--segment-span', "$SegmentSpan",
    '--approved-by-user'
)

Invoke-PythonStage -Name 'saved-artifact-verification' -Arguments @(
    '-m', 'source.plateau_recurrence_cli', 'verify',
    '--result-directory', $ResultDirectory
)

Write-RunLine '[PASS] P006 analysis and saved-artifact verification completed.'
Write-RunLine "[RUN] result_directory=$ResultDirectory"
Write-RunLine "[RUN] log=$LogPath"
