@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-p014" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] P014 exact-checks the lifted modulus-510510 certificate first.
echo [INFO] The optimizer runs only if the four-hour stage-A gate is met.
echo [INFO] CPU budget: 4 physical cores / 8 logical processors; exact scans remain single-stream.
echo [INFO] Python writes a durable progress heartbeat to test_result\logs every five minutes.
echo [INFO] CPU only, 10 GB child cap; no direct prime search or proven speedup.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p014\run_p014_mod510510_staged_certificate.ps1" -ConfirmP014
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P014 launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-p014
exit /b 1
