@echo off
setlocal
cd /d "%~dp0.."

:: Delete the most recent draft weekly digest. Pass --yes to skip prompt.

if not exist ".venv\Scripts\activate.bat" (
    echo [reject_weekly] venv missing; run start.bat once to create it.
    exit /b 10
)
call ".venv\Scripts\activate.bat" || exit /b 11

python scripts\reject_weekly.py %*
exit /b %ERRORLEVEL%
