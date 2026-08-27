@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-48h" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] P015 runs P013-A, P013-B, and independent P014 in that order.
echo [INFO] Global wall cap is 47 hours and aggregate output cap is decimal 50 GB.
echo [INFO] Do not run the individual P013/P014 launchers as well.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p015\run_p015_48h_research_queue.ps1" -Confirm48h
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P015 launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-48h
exit /b 1
