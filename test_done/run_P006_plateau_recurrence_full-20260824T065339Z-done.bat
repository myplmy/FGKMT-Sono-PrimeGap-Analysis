@echo off
setlocal EnableExtensions DisableDelayedExpansion

if /I not "%~1"=="--confirm-p006" goto :usage
set "ANALYSIS_LIMIT=%~2"
if not defined ANALYSIS_LIMIT set "ANALYSIS_LIMIT=1000000000"
if "%ANALYSIS_LIMIT%"=="1000000000" goto :run
if "%ANALYSIS_LIMIT%"=="10000000000" goto :run
goto :usage

:run
echo [INFO] P006 exact configured range: [2, %ANALYSIS_LIMIT%].
echo [INFO] Windows FGKMT Python will be used; WSL is not called.
echo [INFO] Full means the complete configured finite range, never 1e20.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_plateau_recurrence.ps1" -Approved -AnalysisLimit %ANALYSIS_LIMIT% -SegmentSpan 50000000 -RunLabel p006_full_%ANALYSIS_LIMIT%
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" (
    echo [FAIL] P006 full-range run stopped with exit code %RUN_EXIT%.
    exit /b %RUN_EXIT%
)

echo [PASS] P006 full configured range completed.
exit /b 0

:usage
echo Usage: %~nx0 --confirm-p006 [1000000000^|10000000000]
echo Default limit is 1000000000; 10000000000 is an optional larger run.
exit /b 1
