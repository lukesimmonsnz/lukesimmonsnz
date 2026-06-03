@echo off
setlocal
cd /d "%~dp0.."

:: Publish curated source tree to the GitHub mirror.
:: See scripts/publish_to_github.py for behaviour and flags.
::   --dry-run     show what would happen
::   --force       publish despite blockers/warnings
::   --message M   commit message (otherwise prompted)

if not exist ".venv\Scripts\activate.bat" (
    echo [publish_to_github] venv missing; run start.bat once to create it.
    exit /b 10
)
call ".venv\Scripts\activate.bat" || exit /b 11

python scripts\publish_to_github.py %*
exit /b %ERRORLEVEL%
