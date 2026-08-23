[CmdletBinding()]
param(
    [switch]$Approved,
    [string]$RecordsPath = "datas\validated\prime-gap-list-project\1a112a1387052d9ad360686313f501c01fe46b68\maximal_gap_records.csv",
    [string]$AnalysisLimit = "100000000000000000000",
    [string]$RunId = ""
)

$ErrorActionPreference = "Stop"
$FgkmtPython = "W:\miniforge3\envs\FGKMT\python.exe"
$ExpectedCommit = "1a112a1387052d9ad360686313f501c01fe46b68"
$ExpectedRecordsHash = "62ecb9028e77893c79a57512488544b91b628a006bb2bd306b670afa34676297"

if (-not $Approved) {
    throw "P004 actual sensitivity execution requires explicit user approval and -Approved."
}
if (-not (Test-Path -LiteralPath $FgkmtPython -PathType Leaf)) {
    throw "Required FGKMT Python was not found: $FgkmtPython"
}

$ResolvedRecordsPath = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot $RecordsPath)).Path
$Timestamp = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ")
$EffectiveRunId = if ($RunId) { $RunId } else { $Timestamp + "_p004_sensitivity" }
$ResultDirectory = Join-Path $PSScriptRoot ("test_result\run_" + $EffectiveRunId)
$LogDirectory = Join-Path $PSScriptRoot "test_result\logs"
$LogPath = Join-Path $LogDirectory ("run_" + $EffectiveRunId + ".log")

foreach ($ProtectedPath in @($ResultDirectory, $LogPath)) {
    if (Test-Path -LiteralPath $ProtectedPath) {
        throw "Refusing to overwrite an existing P004 artifact: $ProtectedPath"
    }
}
New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null

$StartedAt = [DateTime]::UtcNow
$script:ExperimentExitCode = 1
& {
    Write-Output "[RUN] scope=P004_START_END_AND_ENVELOPE_SENSITIVITY"
    Write-Output ("[RUN] id=" + $EffectiveRunId)
    Write-Output ("[RUN] python=" + $FgkmtPython)
    Write-Output ("[RUN] records=" + $ResolvedRecordsPath)
    Write-Output ("[RUN] analysis_limit=" + $AnalysisLimit)
    Write-Output ("[RUN] started_at_utc=" + $StartedAt.ToString("o"))

    Write-Output "[STAGE] preflight"
    & $FgkmtPython -B -m source.cli preflight
    $script:ExperimentExitCode = $LASTEXITCODE

    if ($script:ExperimentExitCode -eq 0) {
        Write-Output "[STAGE] unit-tests"
        & $FgkmtPython -B -m unittest discover -s tests -v
        $script:ExperimentExitCode = $LASTEXITCODE
    }

    if ($script:ExperimentExitCode -eq 0) {
        Write-Output "[STAGE] analyze-sensitivity"
        & $FgkmtPython -B -m source.sensitivity_pipeline analyze `
            --approved-by-user `
            --records-path $ResolvedRecordsPath `
            --result-directory $ResultDirectory `
            --analysis-limit $AnalysisLimit `
            --expected-records-sha256 $ExpectedRecordsHash `
            --expected-source-commit $ExpectedCommit
        $script:ExperimentExitCode = $LASTEXITCODE
    }

    if ($script:ExperimentExitCode -eq 0) {
        Write-Output "[STAGE] verify-sensitivity"
        & $FgkmtPython -B -m source.sensitivity_pipeline verify `
            --approved-by-user `
            --records-path $ResolvedRecordsPath `
            --result-directory $ResultDirectory
        $script:ExperimentExitCode = $LASTEXITCODE
    }

    $FinishedAt = [DateTime]::UtcNow
    $Elapsed = $FinishedAt - $StartedAt
    Write-Output ("[RUN] finished_at_utc=" + $FinishedAt.ToString("o"))
    Write-Output ("[RUN] elapsed_seconds=" + [Math]::Round($Elapsed.TotalSeconds, 3))
    Write-Output ("[RUN] exit_code=" + $script:ExperimentExitCode)
} *>&1 | Tee-Object -FilePath $LogPath

if ($script:ExperimentExitCode -ne 0) {
    throw "P004 sensitivity experiment failed with exit code $script:ExperimentExitCode; log: $LogPath"
}

