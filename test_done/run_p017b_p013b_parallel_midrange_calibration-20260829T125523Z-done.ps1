[CmdletBinding()]
param([switch]$ConfirmAfterP013B)

$ErrorActionPreference = 'Stop'
if (-not $ConfirmAfterP013B) {
    throw 'P017-B requires -ConfirmAfterP013B.'
}
$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
& (Join-Path $ProjectRoot 'scripts\runners\run_p013_parallel_calibration.ps1') `
    -Mode B_MID -ConfirmAfterP013B
exit $LASTEXITCODE
