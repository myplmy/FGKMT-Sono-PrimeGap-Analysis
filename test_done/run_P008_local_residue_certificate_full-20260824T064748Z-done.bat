@echo off
setlocal EnableExtensions DisableDelayedExpansion

if /I not "%~1"=="--confirm-p008" goto :usage
if not "%~2"=="" goto :usage

echo [INFO] This reads the READY file produced in WSL by prepare_P008_local_primecounts.sh.
echo [INFO] It uses Windows FGKMT Python and does not call WSL itself.
echo [INFO] Representative blocks are not an exhaustive coverage ledger.
echo [INFO] Unresolved right-boundary gaps can never be marked CERTIFIED_ZERO.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_local_residue_certificate.ps1" -Mode Full -Approved
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" (
    echo [FAIL] P008 full phase-A analysis stopped with exit code %RUN_EXIT%.
    exit /b %RUN_EXIT%
)

echo [PASS] P008 full phase-A analysis completed.
exit /b 0

:usage
echo Usage: %~nx0 --confirm-p008
echo First run in WSL: bash ./prepare_P008_local_primecounts.sh --confirm-p008
exit /b 1
