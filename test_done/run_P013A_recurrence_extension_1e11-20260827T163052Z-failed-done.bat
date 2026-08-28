@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-p013a" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] P013-A prospectively analyzes gap starts in [10^10,10^11).
echo [INFO] It uses the frozen P012 rules and performs a second full recomputation.
echo [INFO] CPU only; this is an empirical diagnostic, not a theorem.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p013\run_p013a_recurrence_extension_1e11.ps1" -ConfirmP013A
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P013-A launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-p013a
exit /b 1
