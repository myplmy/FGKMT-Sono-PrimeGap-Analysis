@echo off
setlocal EnableExtensions DisableDelayedExpansion
if /I not "%~1"=="--confirm-p014r2" goto :usage
if not "%~2"=="" goto :usage
echo [INFO] P014-R2 scans exact modulus-510510 constraints with 8 worker processes.
echo [INFO] Arithmetic, coverage, and reduction remain exact; no constraint is sampled or omitted.
echo [INFO] The saved result is recomputed independently by the original serial exact scanner.
echo [INFO] CPU budget: 4 physical cores / 8 logical processors; CPU only; decimal 10 GB child cap.
echo [INFO] Analysis and serial-verification progress files are fsync-written every five minutes.
echo [INFO] Do not run this while P017 or another CPU-heavy experiment is active.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\experiments\p014\run_p014r2_mod510510_parallel_staged_certificate.ps1" -ConfirmP014R2
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" exit /b %RUN_EXIT%
echo [PASS] P014-R2 launcher completed.
exit /b 0
:usage
echo Usage: %~nx0 --confirm-p014r2
exit /b 1
