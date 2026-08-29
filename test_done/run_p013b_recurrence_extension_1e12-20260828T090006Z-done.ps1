[CmdletBinding()]
param([switch]$ConfirmP013B)

$ErrorActionPreference = 'Stop'
if (-not $ConfirmP013B) {
    throw 'P013-B requires -ConfirmP013B.'
}
$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
& (Join-Path $ProjectRoot 'scripts\runners\run_p013_extension.ps1') `
    -Stage B -ConfirmP013
exit $LASTEXITCODE
