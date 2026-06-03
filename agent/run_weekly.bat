@echo off
setlocal
cd /d "%~dp0.."

:: Activate the project venv and run the weekly agent.
:: Designed to be called by Windows Task Scheduler on Sundays, after the day's
:: daily run has finished so the latest daily draft is included in the weekly.
:: Exit codes: 0 ok / 1 no sources / 2 ollama unreachable / 3 ollama http / 4 bad json / 5 missing fields

if not exist ".venv\Scripts\activate.bat" (
    echo [run_weekly] No virtualenv found. Run start.bat first.
    exit /b 10
)
call ".venv\Scripts\activate.bat" || exit /b 11

python -m agent.weekly_post %*
set WEEKLY_RC=%ERRORLEVEL%

:: Refresh the research corpus: lint sweep, regen consolidated section
:: essays for all 16 regions, run the watchlist (drafts only — live
:: corpus is never touched). See agent/weekly_research.py for details.
:: Non-fatal: if it fails, we still want the blog post and docs regen
:: above/below to land. RC is logged separately.
python -m agent.weekly_research
set RESEARCH_RC=%ERRORLEVEL%

:: Refresh docs so counts and the live sitemap reflect the new post.
python -m agent.regen_docs
set REGEN_RC=%ERRORLEVEL%

if not "%WEEKLY_RC%"=="0" exit /b %WEEKLY_RC%
if not "%RESEARCH_RC%"=="0" exit /b %RESEARCH_RC%
exit /b %REGEN_RC%
