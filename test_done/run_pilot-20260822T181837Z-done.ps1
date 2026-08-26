[CmdletBinding()]
param(
    [switch]$Approved,
    [ValidateRange(1, 1000)]
    [int]$IntervalCount = 5,
    [string]$Commit = "",
    [string]$RunId = ""
)

$ErrorActionPreference = "Stop"
$FgkmtPython = "W:\miniforge3\envs\FGKMT\python.exe"

if (-not $Approved) {
    throw "Actual pilot execution requires explicit user approval. Re-run with -Approved only after that approval."
}

if (-not (Test-Path -LiteralPath $FgkmtPython -PathType Leaf)) {
    throw "Required FGKMT Python was not found: $FgkmtPython"
}

$Timestamp = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ")
$EffectiveRunId = if ($RunId) { $RunId } else { $Timestamp + "_pilot" + $IntervalCount }
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
    "pilot",
    "--approved-by-user",
    "--interval-count",
    $IntervalCount,
    "--run-id",
    $EffectiveRunId
)

if ($Commit) {
    $CliArguments += @("--commit", $Commit)
}

$StartedAt = [DateTime]::UtcNow
$script:ExperimentExitCode = 1
& {
    Write-Output ("[RUN] scope=LIMITED_PILOT")
    Write-Output ("[RUN] id=" + $EffectiveRunId)
    Write-Output ("[RUN] python=" + $FgkmtPython)
    Write-Output ("[RUN] interval_count=" + $IntervalCount)
    Write-Output ("[RUN] started_at_utc=" + $StartedAt.ToString("o"))
    & $FgkmtPython @CliArguments
    $script:ExperimentExitCode = $LASTEXITCODE
    $FinishedAt = [DateTime]::UtcNow
    $Elapsed = $FinishedAt - $StartedAt
    Write-Output ("[RUN] finished_at_utc=" + $FinishedAt.ToString("o"))
    Write-Output ("[RUN] elapsed_seconds=" + [Math]::Round($Elapsed.TotalSeconds, 3))
    Write-Output ("[RUN] exit_code=" + $script:ExperimentExitCode)
} *>&1 | Tee-Object -FilePath $LogPath

if ($script:ExperimentExitCode -ne 0) {
    throw "FGKMT-Sono pilot failed with exit code $script:ExperimentExitCode; log: $LogPath"
}

