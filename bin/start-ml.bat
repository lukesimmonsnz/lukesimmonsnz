@echo off
setlocal enabledelayedexpansion
:: Move to repo root (this script lives at <root>\bin\).
cd /d "%~dp0\.."

:: ============================================================
:: start-ml.bat — Layer 0.5b ML daemon (localhost:5001)
:: Mirrors the PID-file pattern of start.bat.
:: ============================================================

:: Ensure runtime dirs exist.
if not exist "instance" mkdir "instance"
if not exist "logs"     mkdir "logs"

:: If already running, bail out.
if exist "instance\.ml-daemon.pid" (
    set /p EXISTING_PID=<"instance\.ml-daemon.pid"
    tasklist /FI "PID eq !EXISTING_PID!" 2>nul | findstr /C:"!EXISTING_PID!" >nul
    if not errorlevel 1 (
        echo [ml-daemon] Already running ^(PID !EXISTING_PID!^). Run bin\stop-ml.bat first.
        exit /b 0
    )
    del "instance\.ml-daemon.pid" >nul 2>&1
)

:: Sanity check: .venv-ml must exist.
if not exist ".venv-ml\Scripts\python.exe" (
    echo [ml-daemon] ERROR: .venv-ml not found. Run:
    echo   python -m venv .venv-ml
    echo   .venv-ml\Scripts\activate
    echo   pip install torch --index-url https://download.pytorch.org/whl/cu121
    echo   pip install -r requirements-ml.txt
    pause
    exit /b 1
)

:: Verify torch is present in .venv-ml before handing off to uvicorn.
".venv-ml\Scripts\python.exe" -c "import torch" 2>nul
if errorlevel 1 (
    echo [ml-daemon] ERROR: torch not found in .venv-ml. Run:
    echo   .venv-ml\Scripts\activate
    echo   pip install torch --index-url https://download.pytorch.org/whl/cu121
    echo   pip install -r requirements-ml.txt
    pause
    exit /b 1
)

echo [ml-daemon] Starting on http://127.0.0.1:5001
echo [ml-daemon] First-start model downloads may take 30-60 s.
echo [ml-daemon] Logs: logs\ml-daemon.log / logs\ml-daemon.err

:: Single-line PowerShell call — no ^ continuations.
powershell -NoProfile -Command "$d = (Get-Location).Path; $p = Start-Process -FilePath ($d + '\.venv-ml\Scripts\uvicorn.exe') -ArgumentList 'tools.ml_daemon:app','--host','127.0.0.1','--port','5001','--workers','1','--log-level','info' -WindowStyle Hidden -PassThru -WorkingDirectory $d -RedirectStandardOutput ($d + '\logs\ml-daemon.log') -RedirectStandardError ($d + '\logs\ml-daemon.err'); $p.Id | Out-File -Encoding ascii -NoNewline -FilePath ($d + '\instance\.ml-daemon.pid')"

if errorlevel 1 (
    echo.
    echo [ml-daemon] Something went wrong launching the daemon.
    echo [ml-daemon] Inspect logs\ml-daemon.err for details. Press any key to close.
    pause > nul
    exit /b 1
)

echo [ml-daemon] Started. PID stored in instance\.ml-daemon.pid
exit /b 0
