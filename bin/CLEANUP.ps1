# bin/CLEANUP.ps1 - one-shot repo hygiene pass.
#
# Run from PowerShell at the repo root:
#     powershell -ExecutionPolicy Bypass -File bin\CLEANUP.ps1
#
# Idempotent. Each section is wrapped in try/catch. Full transcript at
# logs\cleanup.log. Window pauses at end.

$ErrorActionPreference = 'Continue'

try {
    $scriptDir = $PSScriptRoot
    if ([string]::IsNullOrEmpty($scriptDir)) { $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path }
    $root = Split-Path -Parent $scriptDir
    Set-Location -LiteralPath $root
} catch {
    Write-Host "FATAL: cannot resolve repo root. $_" -ForegroundColor Red
    Read-Host "Press Enter to close"
    exit 1
}

$logsDir = Join-Path $root 'logs'
if (-not (Test-Path $logsDir)) { New-Item -ItemType Directory -Force -Path $logsDir | Out-Null }
$logFile = Join-Path $logsDir 'cleanup.log'
try { Stop-Transcript | Out-Null } catch {}
try { Start-Transcript -Path $logFile -Force | Out-Null } catch {}

Write-Host "[cleanup] root: $root" -ForegroundColor Cyan
Write-Host "[cleanup] log:  $logFile" -ForegroundColor Cyan
Write-Host ""

$summary = [ordered]@{}

function Step($name, [scriptblock]$body) {
    Write-Host "==== $name ====" -ForegroundColor Yellow
    try { & $body } catch {
        Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
        $summary["$name (errored)"] = $true
    }
    Write-Host ""
}

Step '1. stop server / daemon' {
    foreach ($s in @('stop.bat','stop-ml.bat')) {
        $p1 = Join-Path $scriptDir $s
        $p2 = Join-Path $root $s
        if (Test-Path -LiteralPath $p1) { & $p1 2>&1 | Out-Null; Write-Host "  ran bin\$s" }
        elseif (Test-Path -LiteralPath $p2) { & $p2 2>&1 | Out-Null; Write-Host "  ran $s" }
        else { Write-Host "  $s missing - skip" -ForegroundColor DarkYellow }
    }
}

Step '2. remove polluted root files' {
    $polluted = @(Get-ChildItem -LiteralPath $root -File -Force -ErrorAction SilentlyContinue | Where-Object { $_.Name -like 'D:\*' -or $_.Name -like '*\*' })
    Write-Host "  $($polluted.Count) polluted files"
    $n = 0
    foreach ($f in $polluted) {
        try { Remove-Item -LiteralPath $f.FullName -Force -ErrorAction Stop; $n++ }
        catch { Write-Host "    fail: $($f.Name)" -ForegroundColor Red }
    }
    $summary['polluted_files_deleted'] = $n
    $pdirs = @(Get-ChildItem -LiteralPath $root -Directory -Force -ErrorAction SilentlyContinue | Where-Object { $_.Name -like 'D:\*' -or $_.Name -like '*\*' })
    Write-Host "  $($pdirs.Count) polluted dirs"
    $m = 0
    foreach ($d in $pdirs) {
        try { Remove-Item -LiteralPath $d.FullName -Recurse -Force -ErrorAction Stop; $m++ }
        catch { Write-Host "    fail: $($d.Name)" -ForegroundColor Red }
    }
    $summary['polluted_dirs_deleted'] = $m
}

Step '3. remove superseded root .bat files' {
    $bats = @('start.bat','stop.bat','start-ml.bat','stop-ml.bat')
    $n = 0
    foreach ($b in $bats) {
        $p = Join-Path $root $b
        if (Test-Path -LiteralPath $p) {
            if (Test-Path -LiteralPath (Join-Path $scriptDir $b)) {
                try { Remove-Item -LiteralPath $p -Force -ErrorAction Stop; $n++ }
                catch { Write-Host "    fail: $b" -ForegroundColor Red }
            } else { Write-Host "    skip $b - no bin\ replacement" -ForegroundColor DarkYellow }
        }
    }
    $summary['root_bats_deleted'] = $n
}

Step '4. archive loose .py scripts' {
    $arc = Join-Path $root 'scripts\archive\2026-Q2-corpus-build'
    if (-not (Test-Path -LiteralPath $arc)) { New-Item -ItemType Directory -Force -Path $arc | Out-Null }
    $loose = @('add_missing_drivers_camps.py','add_remaining_camps.py','add_root_camps.py','build_corpora.py','build_drivers_camps_claims.py','check_yaml.py','count_entities.py','final_fixes.py','fix_nelson.py','fix_schemas.py','gen_all_regions.py','generate_nelson.py','generate_regions.py','regenerate_claims.py','test_lint.py','validate_and_render.py','validate_edits.py','wire_entities.py')
    $n = 0
    foreach ($f in $loose) {
        $src = Join-Path $root $f
        $dst = Join-Path $arc $f
        if (Test-Path -LiteralPath $src) {
            try {
                if (Test-Path -LiteralPath $dst) { Remove-Item -LiteralPath $src -Force -ErrorAction Stop }
                else { Move-Item -LiteralPath $src -Destination $dst -ErrorAction Stop }
                $n++
            } catch { Write-Host "    fail: $f" -ForegroundColor Red }
        }
    }
    $summary['loose_scripts_archived'] = $n
}

Step '5. remove root log/pid files' {
    $rt = @('.server.pid','.ml-daemon.pid','server.log','server.err','ml-daemon.log','ml-daemon.err')
    $n = 0
    foreach ($f in $rt) {
        $p = Join-Path $root $f
        if (Test-Path -LiteralPath $p) {
            try { Remove-Item -LiteralPath $p -Force -ErrorAction Stop; $n++ }
            catch { Write-Host "    fail: $f" -ForegroundColor Red }
        }
    }
    $summary['runtime_files_deleted'] = $n
}

Step '6. remove build artefacts' {
    $art = @('_site','.wrangler')
    $n = 0
    foreach ($a in $art) {
        $p = Join-Path $root $a
        if (Test-Path -LiteralPath $p) {
            try { Remove-Item -LiteralPath $p -Recurse -Force -ErrorAction Stop; $n++ }
            catch { Write-Host "    fail: $a" -ForegroundColor Red }
        }
    }
    $summary['build_artefacts_deleted'] = $n
    $pyc = 0
    try {
        $pdirs = @(Get-ChildItem -LiteralPath $root -Recurse -Directory -Force -Filter '__pycache__' -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notlike '*\.venv\*' -and $_.FullName -notlike '*\.venv-ml\*' })
        foreach ($d in $pdirs) {
            try { Remove-Item -LiteralPath $d.FullName -Recurse -Force -ErrorAction Stop; $pyc++ } catch {}
        }
    } catch {}
    $summary['pycache_dirs_deleted'] = $pyc
}

Step '7. remove scratch reports' {
    $rep = @('REGION_BUILD_REPORT.txt','REVIEW_CHANGES.txt','REGIONAL_CHARACTERISTICS.md')
    $n = 0
    foreach ($r in $rep) {
        $p = Join-Path $root $r
        if (Test-Path -LiteralPath $p) {
            try { Remove-Item -LiteralPath $p -Force -ErrorAction Stop; $n++ }
            catch { Write-Host "    fail: $r" -ForegroundColor Red }
        }
    }
    $summary['scratch_reports_deleted'] = $n
}

Write-Host "==== summary ====" -ForegroundColor Green
$summary.GetEnumerator() | ForEach-Object {
    "{0,-32} {1,6}" -f $_.Key, $_.Value
} | Write-Host

Write-Host ""
Write-Host "Next: git status; git add -A; git commit -m 'chore: repo hygiene'" -ForegroundColor Cyan
Write-Host "Then: bin\start.bat to confirm new launch path works." -ForegroundColor Cyan
Write-Host "Transcript: $logFile" -ForegroundColor Cyan
Write-Host ""

try { Stop-Transcript | Out-Null } catch {}
Read-Host "Press Enter to close"
