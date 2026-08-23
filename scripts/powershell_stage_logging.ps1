Set-StrictMode -Version Latest

$script:RunnerLogPath = $null
$script:RunnerCaptureDirectory = $null
$script:RunnerCapturePrefix = $null
$script:RunnerCurrentStage = 'initialization'
$script:RunnerUtf8NoBom = [System.Text.UTF8Encoding]::new($false)

function Initialize-RunnerLogging {
    param(
        [Parameter(Mandatory = $true)][string]$LogPath,
        [Parameter(Mandatory = $true)][string]$CaptureDirectory,
        [Parameter(Mandatory = $true)][string]$CapturePrefix
    )
    if (Test-Path -LiteralPath $LogPath) {
        throw "Refusing to overwrite runner log: $LogPath"
    }
    New-Item -ItemType Directory -Path $CaptureDirectory -Force | Out-Null
    $script:RunnerLogPath = $LogPath
    $script:RunnerCaptureDirectory = $CaptureDirectory
    $script:RunnerCapturePrefix = $CapturePrefix
    [System.IO.File]::WriteAllText($LogPath, '', $script:RunnerUtf8NoBom)
}

function Write-RunLine {
    param(
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$Message
    )
    if ([string]::IsNullOrEmpty($script:RunnerLogPath)) {
        throw 'Runner logging has not been initialized.'
    }
    Write-Host $Message
    [System.IO.File]::AppendAllText(
        $script:RunnerLogPath,
        $Message + [Environment]::NewLine,
        $script:RunnerUtf8NoBom
    )
}

function Write-RunBlock {
    param(
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$Prefix,
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$Text
    )
    foreach ($Line in ($Text -split "`r?`n")) {
        Write-RunLine "$Prefix$Line"
    }
}

function Copy-CapturedOutput {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][ValidateSet('stdout', 'stderr')][string]$Stream
    )
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return
    }
    $Lines = [System.IO.File]::ReadAllLines($Path, $script:RunnerUtf8NoBom)
    if ($Lines.Count -eq 0) {
        return
    }
    Write-RunLine "[CAPTURE] stream=$Stream begin"
    foreach ($Line in $Lines) {
        Write-RunLine $Line
    }
    Write-RunLine "[CAPTURE] stream=$Stream end"
}

function Invoke-LoggedNativeStage {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )
    $script:RunnerCurrentStage = $Name
    Write-RunLine "[STAGE] $Name"
    $SafeName = $Name -replace '[^A-Za-z0-9_-]', '_'
    $StdoutPath = Join-Path $script:RunnerCaptureDirectory (
        "$($script:RunnerCapturePrefix).$SafeName.stdout.tmp"
    )
    $StderrPath = Join-Path $script:RunnerCaptureDirectory (
        "$($script:RunnerCapturePrefix).$SafeName.stderr.tmp"
    )
    if ((Test-Path -LiteralPath $StdoutPath) -or (Test-Path -LiteralPath $StderrPath)) {
        throw "Refusing to overwrite stage capture for '$Name'."
    }

    $StageExit = $null
    try {
        $Process = Start-Process -FilePath $FilePath -ArgumentList $Arguments `
            -Wait -PassThru -NoNewWindow `
            -RedirectStandardOutput $StdoutPath `
            -RedirectStandardError $StderrPath
        $StageExit = $Process.ExitCode
    }
    finally {
        try {
            Copy-CapturedOutput -Path $StdoutPath -Stream stdout
            Copy-CapturedOutput -Path $StderrPath -Stream stderr
        }
        finally {
            if (Test-Path -LiteralPath $StdoutPath) {
                Remove-Item -LiteralPath $StdoutPath -Force
            }
            if (Test-Path -LiteralPath $StderrPath) {
                Remove-Item -LiteralPath $StderrPath -Force
            }
        }
    }
    if ($StageExit -ne 0) {
        throw "Stage '$Name' failed with exit code $StageExit."
    }
    Write-RunLine "[PASS] $Name"
}

function Write-RunnerFailure {
    param(
        [Parameter(Mandatory = $true)]
        [System.Management.Automation.ErrorRecord]$ErrorRecord
    )
    $ExceptionType = $ErrorRecord.Exception.GetType().FullName
    Write-RunLine "[FAIL] runner_stage=$($script:RunnerCurrentStage)"
    Write-RunLine "[FAIL] exception_type=$ExceptionType"
    Write-RunLine "[FAIL] message=$($ErrorRecord.Exception.Message)"
    Write-RunLine "[FAIL] fully_qualified_error_id=$($ErrorRecord.FullyQualifiedErrorId)"
    Write-RunLine "[FAIL] category=$($ErrorRecord.CategoryInfo)"
    if ($null -ne $ErrorRecord.InvocationInfo) {
        Write-RunBlock -Prefix '[FAIL] invocation: ' -Text (
            [string]$ErrorRecord.InvocationInfo.PositionMessage
        )
    }
    if (-not [string]::IsNullOrEmpty($ErrorRecord.ScriptStackTrace)) {
        Write-RunBlock -Prefix '[FAIL] stack: ' -Text $ErrorRecord.ScriptStackTrace
    }
    Write-RunLine '[FAIL] error_record_begin'
    $Details = $ErrorRecord | Format-List * -Force | Out-String -Width 4096
    Write-RunBlock -Prefix '' -Text ([string]$Details)
    Write-RunLine '[FAIL] error_record_end'
}

