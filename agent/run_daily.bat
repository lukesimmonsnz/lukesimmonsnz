@echo off
setlocal
cd /d "%~dp0.."

:: Activate the project venv and run the daily agent.
:: Designed to be called by Windows Task Scheduler (hidden) or manually.
:: Exit codes: 0 ok / 1 no sources / 2 ollama unreachable / 3 ollama http / 4 bad json / 5 missing fields

if not exist ".venv\Scripts\activate.bat" (
    echo [run_daily] No virtualenv found. Run start.bat first.
    exit /b 10
)
call ".venv\Scripts\activate.bat" || exit /b 11

python -m agent.daily_post %*
set DAILY_RC=%ERRORLEVEL%

:: Refresh docs regardless of the agent's outcome — the sitemap should reflect
:: the current state of routes and content even if the blog run failed.
python -m agent.regen_docs
set REGEN_RC=%ERRORLEVEL%

:: Exit with the blog agent's code if it failed; otherwise surface any regen error.
if not "%DAILY_RC%"=="0" exit /b %DAILY_RC%
exit /b %REGEN_RC%
