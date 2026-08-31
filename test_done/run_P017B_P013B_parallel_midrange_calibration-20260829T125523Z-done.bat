@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-after-p013b" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] Run only after the original P013-B process has completely ended.
echo [INFO] P017-B compares serial and 8-worker exact results on the first P013-B half-decade only.
echo [INFO] This is not the scientific P013-B full result and does not read its live artifacts.
echo [INFO] Hard timeout when queued: 11 hours. CPU: 4 physical / 8 logical. GPU: none.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p017\run_p017b_p013b_parallel_midrange_calibration.ps1" -ConfirmAfterP013B
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P017-B launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-after-p013b
exit /b 1
