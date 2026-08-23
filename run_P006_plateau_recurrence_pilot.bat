@echo off
setlocal EnableExtensions DisableDelayedExpansion

if /I not "%~1"=="--confirm-p006" goto :usage
if not "%~2"=="" goto :usage

echo [INFO] P006 exact pilot range: [2, 100000000].
echo [INFO] Windows FGKMT Python will be used; WSL is not called.
echo [INFO] This reconstructs every consecutive gap in the configured range.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_plateau_recurrence.ps1" -Approved -AnalysisLimit 100000000 -SegmentSpan 10000000 -RunLabel p006_pilot1e8
set "RUN_EXIT=%ERRORLEVEL%"
if not "%RUN_EXIT%"=="0" (
    echo [FAIL] P006 pilot stopped with exit code %RUN_EXIT%.
    exit /b %RUN_EXIT%
)

echo [PASS] P006 pilot completed.
exit /b 0

:usage
echo Usage: %~nx0 --confirm-p006
echo This explicitly authorizes the exact [2, 1e8] pilot.
exit /b 1
