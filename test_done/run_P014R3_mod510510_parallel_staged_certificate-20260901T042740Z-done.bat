@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-p014r3" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] P014-R3 retries the exact modulus-510510 staged certificate after the PowerShell 5.1 argv fix.
echo [INFO] Arithmetic, coverage, reduction, resource limits, and the serial saved oracle are unchanged from R2.
echo [INFO] CPU budget: 4 physical cores / 8 logical processors; CPU only; decimal 10 GB child cap.
echo [INFO] Analysis and serial-verification progress files are fsync-written every five minutes.
echo [INFO] Child stdout and stderr are shown live in this window by the Python tee broker.
echo [INFO] Do not run this while another CPU-heavy experiment is active.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p014\run_p014r3_mod510510_parallel_staged_certificate.ps1" -ConfirmP014R3
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P014-R3 launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-p014r3
exit /b 1
