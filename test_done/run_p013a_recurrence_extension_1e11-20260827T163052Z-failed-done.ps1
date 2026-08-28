[CmdletBinding()]
param([switch]$ConfirmP013A)

$ErrorActionPreference = 'Stop'
if (-not $ConfirmP013A) {
    throw 'P013-A requires -ConfirmP013A.'
}
$ProjectRoot = Split-Path -Parent (
    Split-Path -Parent (
        Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    )
)
& (Join-Path $ProjectRoot 'scripts\runners\run_p013_extension.ps1') `
    -Stage A -ConfirmP013
exit $LASTEXITCODE
