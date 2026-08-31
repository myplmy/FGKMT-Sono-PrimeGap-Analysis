@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-after-p013b" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] Run only after the original P013-B process has completely ended.
echo [INFO] P017-A recomputes the full P013-A range with 8 exact segment workers.
echo [INFO] It compares against the completed serial checkpoint and full analysis.
echo [INFO] Hard timeout when queued: 4 hours. CPU: 4 physical / 8 logical. GPU: none.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p017\run_p017a_p013a_parallel_full_calibration.ps1" -ConfirmAfterP013B
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P017-A launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-after-p013b
exit /b 1
