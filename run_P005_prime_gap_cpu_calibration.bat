@echo off
setlocal EnableExtensions DisableDelayedExpansion

if /I not "%~1"=="--confirm-cpu" goto :usage

where wsl.exe >nul 2>&1
if errorlevel 1 (
    echo [FAIL] wsl.exe was not found.
    exit /b 2
)

set "PROJECT_ROOT=%~dp0"
for /f "usebackq delims=" %%I in (`wsl.exe -d Ubuntu -- wslpath -a "%PROJECT_ROOT%"`) do set "WSL_PROJECT_ROOT=%%I"
if not defined WSL_PROJECT_ROOT (
    echo [FAIL] Could not translate the project path for WSL Ubuntu.
    exit /b 3
)

for /f "usebackq delims=" %%I in (`powershell.exe -NoProfile -Command "[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')"`) do set "RUN_STAMP=%%I"
set "LOG_DIRECTORY=%PROJECT_ROOT%test_result\logs"
if not exist "%LOG_DIRECTORY%" mkdir "%LOG_DIRECTORY%"
set "LOG_PATH=%LOG_DIRECTORY%\run_%RUN_STAMP%_p005_prime_gap_cpu_calibration.log"
if exist "%LOG_PATH%" (
    echo [FAIL] Refusing to overwrite existing log: %LOG_PATH%
    exit /b 4
)

for /f "usebackq delims=" %%I in (`wsl.exe -d Ubuntu -- wslpath -a "%LOG_PATH%"`) do set "WSL_LOG_PATH=%%I"
if not defined WSL_LOG_PATH (
    echo [FAIL] Could not translate the log path for WSL Ubuntu.
    exit /b 5
)

echo [INFO] CPU-only prime-gap calibration will use 8 threads.
echo [INFO] Memory is capped at 30 GiB with upstream --max-mem 28.
echo [INFO] This is a bounded calibration search, not Rank 85-to-86 exhaustive coverage.
echo [INFO] Log: %LOG_PATH%

wsl.exe -d Ubuntu -- bash "%WSL_PROJECT_ROOT%/scripts/run_prime_gap_cpu_calibration.sh" --approved "%WSL_PROJECT_ROOT%" "%WSL_LOG_PATH%"
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" (
    echo [FAIL] P005 CPU calibration stopped with exit code %RUN_EXIT%.
    echo [INFO] Review: %LOG_PATH%
    exit /b %RUN_EXIT%
)

echo [PASS] P005 CPU calibration completed.
echo [INFO] Review: %LOG_PATH%
exit /b 0

:usage
echo Usage: %~nx0 --confirm-cpu
echo This explicitly authorizes a bounded CPU-only calibration search.
exit /b 1
