[CmdletBinding()]
param(
    [switch]$Approved,
    [string]$Commit = "",
    [string]$RunId = "",
    [string]$AnalysisLimit = "100000000000000000000"
)

$ErrorActionPreference = "Stop"
$FgkmtPython = "W:\miniforge3\envs\FGKMT\python.exe"

if (-not $Approved) {
    throw "Actual experiment execution requires explicit user approval. Re-run with -Approved only after that approval."
}

if (-not (Test-Path -LiteralPath $FgkmtPython -PathType Leaf)) {
    throw "Required FGKMT Python was not found: $FgkmtPython"
}

$Timestamp = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ")
$EffectiveRunId = if ($RunId) { $RunId } else { $Timestamp + "_autohead" }
$LogDirectory = Join-Path $PSScriptRoot "test_result\logs"
$LogPath = Join-Path $LogDirectory ("run_" + $EffectiveRunId + ".log")
if (Test-Path -LiteralPath $LogPath) {
    throw "Refusing to overwrite an existing log: $LogPath"
}
New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null

$CliArguments = @(
    "-B",
    "-m",
    "source.cli",
    "run",
    "--approved-by-user",
    "--analysis-limit",
    $AnalysisLimit,
    "--run-id",
    $EffectiveRunId
)

if ($Commit) {
    $CliArguments += @("--commit", $Commit)
}

Write-Host "[RUN] id=$EffectiveRunId"
Write-Host "[RUN] python=$FgkmtPython"
Write-Host "[RUN] log=$LogPath"
& $FgkmtPython @CliArguments *>&1 | Tee-Object -FilePath $LogPath
$ExperimentExitCode = $LASTEXITCODE
if ($ExperimentExitCode -ne 0) {
    throw "FGKMT-Sono experiment failed with exit code $ExperimentExitCode; log: $LogPath"
}
