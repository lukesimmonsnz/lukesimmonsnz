@echo off
setlocal
cd /d "%~dp0.."

:: Promote the latest draft weekly digest, lint it, and deploy.
:: See scripts/publish_weekly.py for behaviour and flags.
::   --force      :: deploy even if lint fails
::   --no-deploy  :: only flip status, skip wrangler

if not exist ".venv\Scripts\activate.bat" (
    echo [publish_weekly] venv missing; run start.bat once to create it.
    exit /b 10
)
call ".venv\Scripts\activate.bat" || exit /b 11

python scripts\publish_weekly.py %*
exit /b %ERRORLEVEL%
