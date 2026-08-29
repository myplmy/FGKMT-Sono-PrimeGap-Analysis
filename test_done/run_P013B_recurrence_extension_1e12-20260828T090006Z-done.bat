@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-p013b" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] P013-B prospectively analyzes gap starts in [10^11,10^12).
echo [INFO] It uses the frozen P012 rules and performs a second full recomputation.
echo [INFO] CPU budget: 4 physical cores / 8 logical processors; the sieve stream itself is single-threaded.
echo [INFO] CPU only; this is an empirical diagnostic, not a theorem.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p013\run_p013b_recurrence_extension_1e12.ps1" -ConfirmP013B
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P013-B launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-p013b
exit /b 1
