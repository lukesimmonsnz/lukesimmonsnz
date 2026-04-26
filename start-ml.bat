@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: ============================================================
:: start-ml.bat — Layer 0.5b ML daemon (localhost:5001)
:: Mirrors the PID-file pattern of start.bat.
:: ============================================================

:: If already running, bail out.
if exist ".ml-daemon.pid" (
    set /p EXISTING_PID=<".ml-daemon.pid"
    tasklist /FI "PID eq !EXISTING_PID!" 2>nul | findstr /C:"!EXISTING_PID!" >nul
    if not errorlevel 1 (
        echo [ml-daemon] Already running ^(PID !EXISTING_PID!^). Run stop-ml.bat first.
        exit /b 0
    )
    del ".ml-daemon.pid" >nul 2>&1
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
echo [ml-daemon] Logs: ml-daemon.log / ml-daemon.err

:: Single-line PowerShell call — no ^ continuations.
:: PowerShell single-quoted strings are literal, so no \" escapes needed
:: inside the outer CMD double-quoted argument.
powershell -NoProfile -Command "$d = (Get-Location).Path; $p = Start-Process -FilePath ($d + '\.venv-ml\Scripts\uvicorn.exe') -ArgumentList 'tools.ml_daemon:app','--host','127.0.0.1','--port','5001','--workers','1','--log-level','info' -WindowStyle Hidden -PassThru -WorkingDirectory $d -RedirectStandardOutput ($d + '\ml-daemon.log') -RedirectStandardError ($d + '\ml-daemon.err'); $p.Id | Out-File -Encoding ascii -NoNewline -FilePath ($d + '\.ml-daemon.pid')"

if errorlevel 1 (
    echo.
    echo [ml-daemon] Something went wrong launching the daemon.
    echo [ml-daemon] Inspect ml-daemon.err for details. Press any key to close.
    pause > nul
    exit /b 1
)

echo [ml-daemon] Started. PID stored in .ml-daemon.pid
exit /b 0
