@echo off
setlocal EnableExtensions DisableDelayedExpansion

if /I not "%~1"=="--confirm-p008" goto :usage
if not "%~2"=="" goto :usage

echo [INFO] P008 pilot uses exact toy prime streams and the supplied modulus-2310 certificate.
echo [INFO] It tests local-bound arithmetic, right-boundary handling, and saved-artifact verification.
echo [INFO] It does not search 10^20 to 10^21 and does not prove a speedup.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_local_residue_certificate.ps1" -Mode Pilot -Approved
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" (
    echo [FAIL] P008 pilot stopped with exit code %RUN_EXIT%.
    exit /b %RUN_EXIT%
)

echo [PASS] P008 pilot completed.
exit /b 0

:usage
echo Usage: %~nx0 --confirm-p008
echo This authorizes only the toy/local-certificate pilot, not prime-gap search.
exit /b 1
