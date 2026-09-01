@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-p018p0" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] P018-P0 is a one-plateau runtime and blinded-information calibration only.
echo [INFO] It cannot pass A or B and cannot promote a full recurrence range.
echo [INFO] Run the WSL primecount preparation first. Do not run P0 and A together.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p018\run_p018p0_prefix_information_calibration.ps1" -ConfirmP018P0
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P018-P0 launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-p018p0
exit /b 1
