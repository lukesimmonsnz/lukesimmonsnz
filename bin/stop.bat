@echo off
setlocal
:: Move to repo root (this script lives at <root>\bin\).
cd /d "%~dp0\.."

set STOPPED=0

:: Prefer the recorded PID from instance\.server.pid.
if exist "instance\.server.pid" (
    set /p SERVER_PID=<"instance\.server.pid"
    taskkill /F /PID %SERVER_PID% >nul 2>&1
    if not errorlevel 1 set STOPPED=1
    del "instance\.server.pid" >nul 2>&1
)

:: Fallback: kill whatever is listening on port 5000 (in case the PID file was lost).
for /f "tokens=5" %%a in ('netstat -aon ^| findstr /R /C:":5000 .*LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
    if not errorlevel 1 set STOPPED=1
)

if %STOPPED%==1 (
    echo [stop] Server stopped.
) else (
    echo [stop] No running server found.
)

%WINDIR%\System32\timeout.exe /t 2 /nobreak >nul
exit /b 0
