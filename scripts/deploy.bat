@echo off
setlocal
cd /d "%~dp0.."

:: Freeze the Flask app to _site/ and deploy to Cloudflare Pages.
:: See docs/CLOUDFLARE-DEPLOY.md for one-time setup (domain, Turnstile,
:: Resend, env vars, wrangler login).

:: ---- Edit these two before first use ----------------------------------
:: Public Turnstile site key (not secret — baked into rendered HTML).
if "%TURNSTILE_SITE_KEY%"=="" set TURNSTILE_SITE_KEY=0x4AAAAAADCRtescIooaJl01
:: Pages project name as created in the Cloudflare dashboard.
set PAGES_PROJECT=lukesimmonsnz
:: -----------------------------------------------------------------------

set SITE_URL=https://lukesimmonsnz.kiwi
set CONTACT_SUBMIT_URL=/api/contact

if not exist ".venv\Scripts\activate.bat" (
    echo [deploy] venv missing; run start.bat once to create it.
    exit /b 10
)
call ".venv\Scripts\activate.bat" || exit /b 11

echo [deploy] freezing Flask app to _site/ ...
python scripts\freeze.py || exit /b 20

echo [deploy] pushing _site/ to Cloudflare Pages project "%PAGES_PROJECT%" ...
wrangler pages deploy _site --project-name %PAGES_PROJECT%
exit /b %ERRORLEVEL%
