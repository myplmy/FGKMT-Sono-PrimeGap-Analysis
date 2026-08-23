[CmdletBinding()]
param(
    [switch]$Approved,
    [string]$RecordsPath = "datas\validated\prime-gap-list-project\1a112a1387052d9ad360686313f501c01fe46b68\maximal_gap_records.csv",
    [string]$AnalysisLimit = "100000000000000000000",
    [string]$RunId = ""
)

$ErrorActionPreference = "Stop"
$FgkmtPython = "W:\miniforge3\envs\FGKMT\python.exe"

if (-not $Approved) {
    throw "Actual full experiment execution requires explicit user approval. Re-run with -Approved only after that approval."
}

if (-not (Test-Path -LiteralPath $FgkmtPython -PathType Leaf)) {
    throw "Required FGKMT Python was not found: $FgkmtPython"
}

$ResolvedRecordsPath = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot $RecordsPath)).Path
$Timestamp = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ")
$EffectiveRunId = if ($RunId) { $RunId } else { $Timestamp + "_full1e20" }
$ResultDirectory = Join-Path $PSScriptRoot ("test_result\run_" + $EffectiveRunId)
$LogDirectory = Join-Path $PSScriptRoot "test_result\logs"
$LogPath = Join-Path $LogDirectory ("run_" + $EffectiveRunId + ".log")
$IndependentRawDirectory = Join-Path $PSScriptRoot ("datas\raw\independent\oeis\" + $EffectiveRunId)
$OliveiraRawDirectory = Join-Path $PSScriptRoot ("datas\raw\independent\oliveira\" + $EffectiveRunId)

foreach ($PathToProtect in @($ResultDirectory, $LogPath, $IndependentRawDirectory, $OliveiraRawDirectory)) {
    if (Test-Path -LiteralPath $PathToProtect) {
        throw "Refusing to overwrite an existing full-run artifact: $PathToProtect"
    }
}
New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null

$AnalyzeArguments = @(
    "-B",
    "-m",
    "source.cli",
    "analyze",
    "--approved-by-user",
    "--records-path",
    $ResolvedRecordsPath,
    "--analysis-limit",
    $AnalysisLimit,
    "--run-id",
    $EffectiveRunId
)
$CrossArguments = @(
    "-B",
    "-m",
    "source.cli",
    "cross-validate-oeis",
    "--approved-by-user",
    "--records-path",
    $ResolvedRecordsPath,
    "--result-directory",
    $ResultDirectory,
    "--source-run-id",
    $EffectiveRunId
)
$OliveiraCrossArguments = @(
    "-B",
    "-m",
    "source.cli",
    "cross-validate-oliveira",
    "--approved-by-user",
    "--records-path",
    $ResolvedRecordsPath,
    "--result-directory",
    $ResultDirectory,
    "--source-run-id",
    $EffectiveRunId
)
$VerifyArguments = @(
    "-B",
    "-m",
    "source.cli",
    "verify-results",
    "--approved-by-user",
    "--records-path",
    $ResolvedRecordsPath,
    "--result-directory",
    $ResultDirectory
)

$StartedAt = [DateTime]::UtcNow
$script:ExperimentExitCode = 1
& {
    Write-Output "[RUN] scope=FULL_1E20"
    Write-Output ("[RUN] id=" + $EffectiveRunId)
    Write-Output ("[RUN] python=" + $FgkmtPython)
    Write-Output ("[RUN] records=" + $ResolvedRecordsPath)
    Write-Output ("[RUN] analysis_limit=" + $AnalysisLimit)
    Write-Output ("[RUN] started_at_utc=" + $StartedAt.ToString("o"))

    Write-Output "[STAGE] analyze"
    & $FgkmtPython @AnalyzeArguments
    $script:ExperimentExitCode = $LASTEXITCODE

    if ($script:ExperimentExitCode -eq 0) {
        Write-Output "[STAGE] cross-validate-oeis"
        & $FgkmtPython @CrossArguments
        $script:ExperimentExitCode = $LASTEXITCODE
    }

    if ($script:ExperimentExitCode -eq 0) {
        Write-Output "[STAGE] cross-validate-oliveira"
        & $FgkmtPython @OliveiraCrossArguments
        $script:ExperimentExitCode = $LASTEXITCODE
    }

    if ($script:ExperimentExitCode -eq 0) {
        Write-Output "[STAGE] verify-results"
        & $FgkmtPython @VerifyArguments
        $script:ExperimentExitCode = $LASTEXITCODE
    }

    $FinishedAt = [DateTime]::UtcNow
    $Elapsed = $FinishedAt - $StartedAt
    Write-Output ("[RUN] finished_at_utc=" + $FinishedAt.ToString("o"))
    Write-Output ("[RUN] elapsed_seconds=" + [Math]::Round($Elapsed.TotalSeconds, 3))
    Write-Output ("[RUN] exit_code=" + $script:ExperimentExitCode)
} *>&1 | Tee-Object -FilePath $LogPath

if ($script:ExperimentExitCode -ne 0) {
    throw "FGKMT-Sono full experiment failed with exit code $script:ExperimentExitCode; log: $LogPath"
}
