@echo off
setlocal

:: One-shot cleanup: delete the 7 old Cloudflare Pages deployments that
:: predate the admin-cleanup deploy. The current production deploy
:: (2f8db393) is intentionally NOT in this list.
::
:: Why deleting helps: Cloudflare's Pages-internal asset cache is still
:: serving stale /admin/* HTML from one of these older deployments
:: despite multiple "Purge Everything" runs. Removing the deployments
:: removes the underlying asset bundle the cache could refer to.
::
:: After this finishes, the cache layer should evict the stale 200s and
:: lukesimmonsnz.kiwi/admin/ will return 404.

:: Bypass the wrangler.cmd npm shim and call node on wrangler.js directly.
:: The shim has been failing with "system cannot find path specified" in
:: this environment; direct invocation is more reliable.
set NODE="C:\Program Files\nodejs\node.exe"
set WRANGLER_JS="C:\Users\Luke Simmons\AppData\Roaming\npm\node_modules\wrangler\bin\wrangler.js"

set IDS=^
332d6f24-3f84-4f94-b604-4e5a3ffbfb7f ^
a947dea8-282c-488e-9727-e3874fe26577 ^
68e65f73-6201-478e-9422-188e437d7a2a ^
70e01729-10f1-4c8c-9c76-b59ac9a7b77f ^
c29b1264-6ed3-4c91-ad59-a0c16e56d76e ^
82547c40-bb89-4f35-a2b3-be7ae76867ac ^
dd2efbd6-10fb-4f5e-a27d-bf2f8b0f7dc9

for %%I in (%IDS%) do (
    echo === Deleting %%I ===
    %NODE% %WRANGLER_JS% pages deployment delete %%I --project-name lukesimmonsnz --yes --force
    echo.
)

echo.
echo Done. Re-run the audit to confirm /admin/* paths now 404.
endlocal
