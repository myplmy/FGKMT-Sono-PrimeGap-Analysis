@echo off
setlocal EnableExtensions DisableDelayedExpansion

if /I not "%~1"=="--confirm-p007" goto :usage
if not "%~2"=="" goto :usage

echo [INFO] P007 phase-A full run compares exact certificates for moduli 30, 210, and 2310.
echo [INFO] Modulus 30030 is resource-estimated only and is not solved.
echo [INFO] No primes are enumerated and no 10^20-to-10^21 search is performed.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_finite_gap_certificate.ps1" -Mode Full -Approved
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" (
    echo [FAIL] P007 phase-A full run stopped with exit code %RUN_EXIT%.
    exit /b %RUN_EXIT%
)

echo [PASS] P007 phase-A full certificate comparison completed.
exit /b 0

:usage
echo Usage: %~nx0 --confirm-p007
echo This authorizes small-modulus certificate discovery, not prime-gap search.
exit /b 1
