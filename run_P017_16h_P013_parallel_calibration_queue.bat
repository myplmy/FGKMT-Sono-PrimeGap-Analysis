@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-after-p013b" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] Run only after the original P013-B process has completely ended.
echo [INFO] Queue order: P013-A full parallel calibration, then P013-B midrange serial/parallel calibration.
echo [INFO] Child timeout sum: 15 hours. Global hard wall: 16 hours. Disk cap: decimal 5 GB.
echo [INFO] Do not also run the two individual P017 launchers.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p017\run_p017_16h_parallel_calibration_queue.ps1" -ConfirmAfterP013B
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P017 16-hour calibration queue launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-after-p013b
exit /b 1
