param(
    [string]$Python = 'W:\miniforge3\envs\FGKMT\python.exe'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Helper = Join-Path $ProjectRoot 'scripts\powershell_stage_logging.ps1'
$TempBase = [System.IO.Path]::GetTempPath()
$TempLeaf = 'fgkmt-runner-logging-' + [Guid]::NewGuid().ToString('N')
$TempRoot = Join-Path $TempBase $TempLeaf

try {
    if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
        throw "Fixed Python was not found: $Python"
    }
    New-Item -ItemType Directory -Path $TempRoot | Out-Null
    . $Helper

    $LogPath = Join-Path $TempRoot 'selftest.log'
    Initialize-RunnerLogging -LogPath $LogPath -CaptureDirectory $TempRoot `
        -CapturePrefix 'selftest'

    $SuccessScript = Join-Path $TempRoot 'success.py'
    [System.IO.File]::WriteAllText(
        $SuccessScript,
        "import sys`nprint('stdout-before')`nprint()`nprint('stdout-after')`nsys.stderr.write('stderr-before\n\nstderr-after\n')`n",
        [System.Text.UTF8Encoding]::new($false)
    )
    Invoke-LoggedNativeStage -Name 'blank-line-success' -FilePath $Python `
        -Arguments @('-B', $SuccessScript)

    $FailureScript = Join-Path $TempRoot 'failure.py'
    [System.IO.File]::WriteAllText(
        $FailureScript,
        "import sys`nsys.stderr.write('synthetic stderr failure\n')`nraise SystemExit(7)`n",
        [System.Text.UTF8Encoding]::new($false)
    )
    $Caught = $false
    try {
        Invoke-LoggedNativeStage -Name 'synthetic-failure' -FilePath $Python `
            -Arguments @('-B', $FailureScript)
    }
    catch {
        $Caught = $true
        Write-RunnerFailure -ErrorRecord $_
    }
    if (-not $Caught) {
        throw 'Synthetic nonzero exit was not converted to a logged failure.'
    }

    $Log = [System.IO.File]::ReadAllText(
        $LogPath,
        [System.Text.UTF8Encoding]::new($false)
    )
    foreach ($Required in @(
        'stdout-before',
        'stdout-after',
        'stderr-before',
        'stderr-after',
        'synthetic stderr failure',
        "Stage 'synthetic-failure' failed with exit code 7.",
        '[FAIL] error_record_begin',
        '[FAIL] error_record_end'
    )) {
        if (-not $Log.Contains($Required)) {
            throw "Runner self-test log is missing: $Required"
        }
    }
    if ($Log -notmatch 'stdout-before\r?\n\r?\nstdout-after') {
        throw 'Blank stdout line was not preserved.'
    }
    if ($Log -notmatch 'stderr-before\r?\n\r?\nstderr-after') {
        throw 'Blank stderr line was not preserved.'
    }
}
finally {
    if (Test-Path -LiteralPath $TempRoot) {
        $ResolvedBase = [System.IO.Path]::GetFullPath($TempBase)
        $ResolvedRoot = [System.IO.Path]::GetFullPath($TempRoot)
        if (-not $ResolvedRoot.StartsWith($ResolvedBase) -or
            -not ([System.IO.Path]::GetFileName($ResolvedRoot)).StartsWith(
                'fgkmt-runner-logging-'
            )) {
            throw "Refusing unsafe self-test cleanup: $ResolvedRoot"
        }
        Remove-Item -LiteralPath $ResolvedRoot -Recurse -Force
    }
}

Write-Output 'POWERSHELL_STAGE_LOGGING_SELFTEST_PASS'
