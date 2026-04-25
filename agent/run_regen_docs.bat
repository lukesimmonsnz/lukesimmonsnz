@echo off
setlocal
cd /d "%~dp0.."

:: Refresh SITEMAP.md and the auto:* blocks in README.md and docs/ARCHITECTURE.md.
:: Designed to be called by Windows Task Scheduler on a short interval (e.g. every 15 minutes)
:: so the sitemap stays current when pages or routes change outside an agent run.
:: Exit codes: 0 ok / 10 no venv / 11 activate failed

if not exist ".venv\Scripts\activate.bat" (
    echo [run_regen_docs] No virtualenv found. Run start.bat first.
    exit /b 10
)
call ".venv\Scripts\activate.bat" || exit /b 11

python -m agent.regen_docs
set REGEN_RC=%ERRORLEVEL%

:: Render Auckland chart specs (idempotent — skips unchanged outputs)
python "content\auckland\tools\render_charts.py"
set CHARTS_RC=%ERRORLEVEL%

:: Render Auckland map specs (idempotent — fetched GeoJSON is cached)
python "content\auckland\tools\render_maps.py"
set MAPS_RC=%ERRORLEVEL%

if not "%REGEN_RC%"=="0" exit /b %REGEN_RC%
if not "%CHARTS_RC%"=="0" exit /b %CHARTS_RC%
exit /b %MAPS_RC%
