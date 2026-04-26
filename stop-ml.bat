@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: ============================================================
:: stop-ml.bat — stop the ML daemon on port 5001
:: Mirrors the PID-file pattern of stop.bat.
:: ============================================================

set STOPPED=0

:: Prefer the recorded PID.
if exist ".ml-daemon.pid" (
    set /p ML_PID=<".ml-daemon.pid"
    taskkill /F /PID !ML_PID! >nul 2>&1
    if not errorlevel 1 set STOPPED=1
    del ".ml-daemon.pid" >nul 2>&1
)

:: Fallback: kill whatever is listening on port 5001.
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /R /C:":5001 .*LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    if not errorlevel 1 set STOPPED=1
)

if !STOPPED!==1 (
    echo [ml-daemon] Stopped.
) else (
    echo [ml-daemon] No running daemon found.
)

%WINDIR%\System32\timeout.exe /t 2 /nobreak >nul
exit /b 0
