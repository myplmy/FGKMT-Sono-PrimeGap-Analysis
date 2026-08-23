@echo off
setlocal EnableExtensions DisableDelayedExpansion

if /I not "%~1"=="--confirm-p007" goto :usage
if not "%~2"=="" goto :usage

echo [INFO] P007 pilot verifies the supplied modulus-2310 certificate exactly.
echo [INFO] It does not enumerate primes or search the 10^20-to-10^21 interval.
echo [INFO] It does not prove that the search program is faster.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_finite_gap_certificate.ps1" -Mode Pilot -Approved
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" (
    echo [FAIL] P007 pilot stopped with exit code %RUN_EXIT%.
    exit /b %RUN_EXIT%
)

echo [PASS] P007 certificate pilot completed.
exit /b 0

:usage
echo Usage: %~nx0 --confirm-p007
echo This authorizes only exact certificate verification, not prime-gap search.
exit /b 1

