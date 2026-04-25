@echo off
setlocal
cd /d "%~dp0"

:: If a PID file exists and that PID is still running, don't start a second copy.
if exist ".server.pid" (
    set /p EXISTING_PID=<.server.pid
    tasklist /FI "PID eq %EXISTING_PID%" 2>nul | findstr /C:"%EXISTING_PID%" >nul
    if not errorlevel 1 (
        powershell -NoProfile -Command "[System.Windows.Forms.MessageBox]::Show('Server already running (PID %EXISTING_PID%). Run stop.bat first.', 'Luke Simmons site', 'OK', 'Information') | Out-Null" >nul 2>&1
        exit /b 0
    )
    del ".server.pid" >nul 2>&1
)

:: Create venv and install dependencies on first run (visible, so you can see progress).
if not exist ".venv\Scripts\activate.bat" (
    echo [setup] First-run setup: creating virtualenv and installing dependencies...
    python -m venv .venv || goto :error
    call ".venv\Scripts\activate.bat" || goto :error
    pip install -r requirements.txt || goto :error
) else (
    call ".venv\Scripts\activate.bat" || goto :error
)

:: Launch Flask hidden, without the auto-reloader (single PID, clean to stop).
:: Stdout/stderr are captured to server.log / server.err for debugging.
powershell -NoProfile -Command ^
    "$p = Start-Process -FilePath '.venv\Scripts\flask.exe' -ArgumentList 'run','--no-reload' -WindowStyle Hidden -PassThru -RedirectStandardOutput 'server.log' -RedirectStandardError 'server.err'; $p.Id | Out-File -Encoding ascii -NoNewline -FilePath '.server.pid'" || goto :error

:: Done. The cmd window closes automatically now that the batch has finished.
exit /b 0

:error
echo.
echo [start] Something went wrong. Press any key to close.
pause > nul
exit /b 1
