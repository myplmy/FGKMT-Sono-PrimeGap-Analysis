@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-p018a-prefix" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] P018-A measures blinded information margins on the frozen two-plateau prefix.
echo [INFO] It performs two exact parallel full passes and no hypothesis test.
echo [INFO] A PASS can only request review of B; it cannot start or approve a full range.
echo [INFO] Run the WSL primecount preparation first. Do not run P0 and A together.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p018\run_p018a_prefix_information_probe.ps1" -ConfirmP018A
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P018-A prefix launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-p018a-prefix
exit /b 1
