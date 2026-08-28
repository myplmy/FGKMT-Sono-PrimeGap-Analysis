@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-p013a" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] P013-A r2 corrects the NumPy large-hypergeometric implementation limit.
echo [INFO] It prospectively analyzes gap starts in [10^10,10^11) with the frozen P012 rules.
echo [INFO] CPU budget: 4 physical cores / 8 logical processors; the sieve stream itself is single-threaded.
echo [INFO] A sufficient-statistics checkpoint is saved before Monte Carlo inference.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p013\run_p013a_recurrence_extension_1e11_r2.ps1" -ConfirmP013A
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P013-A r2 launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-p013a
exit /b 1
