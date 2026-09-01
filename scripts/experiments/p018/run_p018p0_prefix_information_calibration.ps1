[CmdletBinding()]
param([switch]$ConfirmP018P0)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if (-not $ConfirmP018P0) {
    throw 'P018-P0 calibration requires -ConfirmP018P0.'
}
$Runner = Join-Path (
    Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
) 'runners\run_p018_prefix_information.ps1'
& $Runner -Mode P0 -ConfirmP018Prefix
exit $LASTEXITCODE
