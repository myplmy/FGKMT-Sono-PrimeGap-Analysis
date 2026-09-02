[CmdletBinding()]
param([switch]$ConfirmP018A)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP018A) {
    throw 'P018-A prefix probe requires -ConfirmP018A.'
}
$Runner = Join-Path (
    Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
) 'runners\run_p018_prefix_information.ps1'
& $Runner -Mode A -ConfirmP018Prefix
exit $LASTEXITCODE
