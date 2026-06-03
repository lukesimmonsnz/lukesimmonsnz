# Section Review Session Prompts

Generated 2026-04-27. Nine sessions covering the remaining 11 regions.
Run parallel sessions only within the same tier group (M1+M2 can run together;
L sessions can run in parallel with each other since they touch separate directories).

---

## Protocol (applies to every session)

```
1. lint          python content/<region>/tools/lint.py              — must be 0 errors baseline
2. claim sweep   read all claim YAMLs; flag suspicious quantitative figures
3. fix           BASH HEREDOC ONLY — see CRITICAL rule below
4. integrity     run post-write check on every file immediately after writing
5. re-lint       must return 0 errors 0 warnings after all fixes
6. render        python content/<region>/tools/render.py --all
7. smoke         check 44/44 leaf routes HTTP 200 via Flask test client
8. CLAUDE.md     append row to §6 layer table with findings
```

---

## CRITICAL: File Writing Rule

**NEVER use the Write tool for YAML files. It truncates files at unpredictable lengths.**

Always use bash heredoc:
```bash
cat > "/sessions/wizardly-funny-allen/mnt/Current website/content/<region>/data/claim/<file>.yaml" << 'ENDOFFILE'
id: claim.<region_id>.<theme>.<slug>
statement: >-
  Full statement text here.
value: 42
unit: description of unit
time_period: '2023'
confidence: medium
verification_status: cited_only
last_verified: null
source_ids:
- source.some_source_id
scoped_to:
- <region-slug>
national_assertion: false
region_mentions:
- <region-slug>
methodology_tag: methodology.admin_count_v1
notes: null
ENDOFFILE
```

---

## CRITICAL: Post-Write Integrity Check

Run this immediately after EVERY heredoc write. If it fails, the file is corrupt — rewrite it.

```bash
python3 -c "
import yaml, sys
f = '/sessions/wizardly-funny-allen/mnt/Current website/content/<region>/data/claim/<file>.yaml'
try:
    d = yaml.safe_load(open(f).read())
    required = ['id','statement','value','unit','time_period','confidence',
                'verification_status','last_verified','source_ids','scoped_to',
                'national_assertion','region_mentions','methodology_tag','notes']
    missing = [k for k in required if k not in d]
    bad_list = [k for k in ['source_ids','scoped_to','region_mentions']
                if not isinstance(d.get(k), list)]
    if missing: print('MISSING FIELDS:', missing); sys.exit(1)
    if bad_list: print('NOT A LIST:', bad_list); sys.exit(1)
    print('OK:', d['id'])
except Exception as e:
    print('PARSE ERROR:', e); sys.exit(1)
"
```

After fixing all files, run a bulk integrity check across the entire claim directory:
```bash
python3 -c "
import yaml, sys
from pathlib import Path
errors = []
for f in sorted(Path('/sessions/wizardly-funny-allen/mnt/Current website/content/<region>/data/claim').glob('*.yaml')):
    try:
        d = yaml.safe_load(f.read_text())
        for k in ['source_ids','scoped_to','region_mentions']:
            if not isinstance(d.get(k), list):
                errors.append(f'{f.name}: {k} is not a list (got {d.get(k)!r})')
        import re
        mt = d.get('methodology_tag')
        if mt and not re.match(r'^methodology\.[a-z][a-z0-9_]*_v[0-9]+\$', str(mt)):
            errors.append(f'{f.name}: bad methodology_tag: {mt!r}')
    except Exception as e:
        errors.append(f'{f.name}: PARSE ERROR: {e}')
if errors:
    for e in errors: print(e)
    sys.exit(1)
else:
    print(f'All files OK')
"
```

---

## Bash paths

- Site root: `/sessions/wizardly-funny-allen/mnt/Current website/`
- Python: `PATH="/sessions/wizardly-funny-allen/.local/bin:$PATH" python3`
- Deps if needed: `pip install flask python-frontmatter markdown pyyaml --break-system-packages -q`

---

## Known error patterns (from Auckland/Wellington/small-region/Hawke's Bay reviews)

- Copy-paste driver/problem narratives in claim `statement` that don't match `value`/`unit`
- Wrong region geography in fire/flood/event claims (Port Hills = Christchurch 2017; Pigeon Valley = Nelson 2022)
- Straight-line vs road distances as isolation metrics
- Tunnel/infrastructure age or type misattributed
- `methodology.admin_count_v1` applied to non-count figures — flag but retain with note
- Claim statements generic enough to belong to any region (no region-specific content)
- Inter-region inconsistencies for shared events (Cyclone Gabrielle: national $9B; Hawke's Bay $3-5B; Gisborne $500M-$1B)
- Entity IDs changed by agent without updating problem references (P1 violations)
- `region_mentions: null`, `scoped_to: null`, `national_assertion: null` (Write tool truncation artifacts)
- `time_period` as integer instead of quoted string
- `source_ids` with truncated values (e.g. 'source.stats_nz_census_2' instead of 'source.stats_nz_census_2023')

---

## Smoke test snippet

```python
import sys; sys.path.insert(0, '.')
from app import create_app
from pathlib import Path
app = create_app()
client = app.test_client()
for region in ['<slug>']:
    pages_dir = Path(f'content/{region}/pages')
    results = [(client.get(f'/research/{region}/{md.parent.name}/{md.stem}/').status_code,
                f'/research/{region}/{md.parent.name}/{md.stem}/') for md in sorted(pages_dir.rglob('*.md'))]
    ok = sum(1 for s,_ in results if s==200)
    fail = [(s,u) for s,u in results if s!=200]
    print(f'{region}: {ok}/{len(results)} OK')
    for s,u in fail: print(f'  FAIL {s}  {u}')
```

---

## M1 — Northland + Waikato (medium, ~202 + 164 entities)

NOTE: M1 and M2 already completed 2026-04-27. M1 found systemic copy-paste (no changes made,
escalated to PI). M2 completed with repairs. Prompts retained for reference only.

---

## M2 — Hawke's Bay + Taranaki (medium, ~163 + 137 entities)

NOTE: Completed 2026-04-27. See CLAUDE.md for findings.

---

## L1 — Bay of Plenty (large, ~247 entities)

**NEVER use the Write tool for YAML. Use bash heredoc + integrity check after every write.**

```
You are performing a structured fact-check review of the Bay of Plenty regional research
corpus. Part of the Aotearoa migration project at D:\ai-website-manager\Current website
(Flask site, lukesimmonsnz.kiwi).

Region slug: bay-of-plenty

STEP 1 — Baseline lint (must pass before any changes):
  cd "/sessions/wizardly-funny-allen/mnt/Current website"
  PATH="/sessions/wizardly-funny-allen/.local/bin:$PATH" python3 content/bay-of-plenty/tools/lint.py

STEP 2 — Read ALL claim YAMLs and identify errors:
  cat /sessions/wizardly-funny-allen/mnt/Current\ website/content/bay-of-plenty/data/claim/*.yaml

  Bay of Plenty context for fact-checking:
  - Tauranga: NZ's fastest-growing city; Port of Tauranga (NZ's largest export port by
    volume, handles ~23-28% of NZ exports); Tauranga Moana; Mauao (Mt Maunganui).
  - Eastern Bay: Whakatane, Opotiki, Kawerau (geothermal/forestry/pulp); high Maori
    population in eastern sub-region; Tuhoe (Te Urewera); Ngati Awa; Whakatohea.
  - Geothermal: Rotorua (shared with Waikato boundary); Wairakei.
  - Primary sector: kiwifruit (Zespri headquartered in Te Puke; NZ exports ~30% of world
    kiwifruit); avocados; forestry; Port of Tauranga container volumes.
  - Tauranga City Council governance (2022-2024): government-appointed commissioners
    replaced elected council due to performance failures; commissioners lifted 2024.
  - Whakaari/White Island eruption: 9 December 2019 — 22 deaths, 25 serious injuries.
    Do NOT conflate with Kaikoura earthquake (2016) or any other event.

  Flag: wrong region events; figures misattributed from Waikato or Gisborne; Port of
  Tauranga volume claims (internally consistent?); Whakaari death toll if cited.

STEP 3 — Fix confirmed errors. CRITICAL RULE: NEVER use the Write tool.
  Use ONLY bash heredoc:
    cat > "/sessions/wizardly-funny-allen/mnt/Current website/content/bay-of-plenty/data/claim/<file>.yaml" << 'ENDOFFILE'
    <complete YAML — all fields must be present>
    ENDOFFILE

  After EVERY heredoc write, run the integrity check:
    python3 -c "
    import yaml, sys
    f = '/sessions/wizardly-funny-allen/mnt/Current website/content/bay-of-plenty/data/claim/<file>.yaml'
    try:
        d = yaml.safe_load(open(f).read())
        bad = [k for k in ['source_ids','scoped_to','region_mentions'] if not isinstance(d.get(k),list)]
        if bad: print('NOT A LIST:', bad); sys.exit(1)
        print('OK:', d['id'])
    except Exception as e: print('PARSE ERROR:', e); sys.exit(1)
    "

STEP 4 — Bulk integrity check across all claim files:
  python3 -c "
  import yaml, sys, re
  from pathlib import Path
  errors = []
  for f in sorted(Path('/sessions/wizardly-funny-allen/mnt/Current website/content/bay-of-plenty/data/claim').glob('*.yaml')):
      try:
          d = yaml.safe_load(f.read_text())
          for k in ['source_ids','scoped_to','region_mentions']:
              if not isinstance(d.get(k), list): errors.append(f'{f.name}: {k} not a list')
          mt = d.get('methodology_tag')
          if mt and not re.match(r'^methodology\.[a-z][a-z0-9_]*_v[0-9]+$', str(mt)):
              errors.append(f'{f.name}: bad methodology_tag: {mt!r}')
      except Exception as e: errors.append(f'{f.name}: PARSE ERROR: {e}')
  if errors:
      for e in errors: print(e)
      sys.exit(1)
  print('All files OK')
  "

STEP 5 — Re-lint (must be 0 errors 0 warnings):
  PATH="/sessions/wizardly-funny-allen/.local/bin:$PATH" python3 content/bay-of-plenty/tools/lint.py

STEP 6 — Render pages:
  PATH="/sessions/wizardly-funny-allen/.local/bin:$PATH" python3 content/bay-of-plenty/tools/render.py --all 2>&1 | tail -5

STEP 7 — Smoke test 44/44 leaf routes:
  python3 -c "
  import sys; sys.path.insert(0, '.')
  from app import create_app
  from pathlib import Path
  app = create_app()
  client = app.test_client()
  pages_dir = Path('content/bay-of-plenty/pages')
  results = [(client.get(f'/research/bay-of-plenty/{md.parent.name}/{md.stem}/').status_code,
              f'/research/bay-of-plenty/{md.parent.name}/{md.stem}/') for md in sorted(pages_dir.rglob('*.md'))]
  ok = sum(1 for s,_ in results if s==200)
  fail = [(s,u) for s,u in results if s!=200]
  print(f'bay-of-plenty: {ok}/{len(results)} OK')
  for s,u in fail: print(f'  FAIL {s}  {u}')
  "

DO NOT update CLAUDE.md — parent session consolidates all findings.

Return: entity count, lint status, smoke result, every file changed + what was wrong + what was fixed.
```

---

## L2 — Gisborne (large, ~247 entities)

**NEVER use the Write tool for YAML. Use bash heredoc + integrity check after every write.**

```
You are performing a structured fact-check review of the Gisborne (Tairawhiti) regional
research corpus. Part of the Aotearoa migration project at D:\ai-website-manager\Current website.

Region slug: gisborne

STEP 1 — Baseline lint:
  cd "/sessions/wizardly-funny-allen/mnt/Current website"
  PATH="/sessions/wizardly-funny-allen/.local/bin:$PATH" python3 content/gisborne/tools/lint.py

STEP 2 — Read ALL claim YAMLs:
  cat /sessions/wizardly-funny-allen/mnt/Current\ website/content/gisborne/data/claim/*.yaml

  Gisborne / Tairawhiti context:
  - Easternmost city in NZ; one of the first to see the new day.
  - Highest Maori population proportion of any NZ region (~50%); Ngati Porou (East Cape),
    Rongowhakaata, Ngai Tamanuhiri, Te Aitanga-a-Mahaki are key iwi.
  - Primary sector: forestry (East Cape plantation forestry — massive erosion and slash
    problems post-Cyclone Gabrielle); wine (Gisborne Chardonnay); horticulture.
  - Cyclone Gabrielle (February 2023): devastated Gisborne — Tolaga Bay wharf area
    destroyed, massive forestry slash damage, SH2 closed for months, major infrastructure
    loss. CRITICAL: Do NOT conflate Gisborne damage figures with Hawke's Bay or national
    totals. Gisborne regional damage roughly $500M-$1B; national total ~$9B.
  - Consistently records highest deprivation of any NZ region; high youth unemployment;
    lowest tertiary participation nationally.
  - Infrastructure: no rail; SH2 (south to Hawke's Bay) and SH35 (East Cape coastal loop,
    ~330 km Gisborne to Opotiki) are primary routes.

  Flag: Cyclone Gabrielle damage conflated with national/HB figures; wrong deprivation
  rankings; forestry slash incorrectly attributed to another region.

STEP 3 — Fix confirmed errors using bash heredoc ONLY (never Write tool).
  After every write, run integrity check:
    python3 -c "
    import yaml, sys
    f = '/sessions/wizardly-funny-allen/mnt/Current website/content/gisborne/data/claim/<file>.yaml'
    try:
        d = yaml.safe_load(open(f).read())
        bad = [k for k in ['source_ids','scoped_to','region_mentions'] if not isinstance(d.get(k),list)]
        if bad: print('NOT A LIST:', bad); sys.exit(1)
        print('OK:', d['id'])
    except Exception as e: print('PARSE ERROR:', e); sys.exit(1)
    "

STEP 4 — Bulk integrity check:
  python3 -c "
  import yaml, sys, re
  from pathlib import Path
  errors = []
  for f in sorted(Path('/sessions/wizardly-funny-allen/mnt/Current website/content/gisborne/data/claim').glob('*.yaml')):
      try:
          d = yaml.safe_load(f.read_text())
          for k in ['source_ids','scoped_to','region_mentions']:
              if not isinstance(d.get(k), list): errors.append(f'{f.name}: {k} not a list')
          mt = d.get('methodology_tag')
          if mt and not re.match(r'^methodology\.[a-z][a-z0-9_]*_v[0-9]+$', str(mt)):
              errors.append(f'{f.name}: bad methodology_tag: {mt!r}')
      except Exception as e: errors.append(f'{f.name}: PARSE ERROR: {e}')
  if errors:
      for e in errors: print(e)
      sys.exit(1)
  print('All files OK')
  "

STEP 5 — Re-lint: must be 0 errors 0 warnings.
STEP 6 — Render: python3 content/gisborne/tools/render.py --all 2>&1 | tail -5
STEP 7 — Smoke: 44/44 leaf routes via Flask test client (replace slug as needed).

DO NOT update CLAUDE.md. Return: entity count, lint, smoke, files changed + fixes.
```

---

## L3 — Manawatu-Whanganui (large, ~295 entities)

**NEVER use the Write tool for YAML. Use bash heredoc + integrity check after every write.**

```
You are performing a structured fact-check review of the Manawatu-Whanganui regional
research corpus. Part of the Aotearoa migration project at D:\ai-website-manager\Current website.

Region slug: manawatu-whanganui

STEP 1 — Baseline lint:
  cd "/sessions/wizardly-funny-allen/mnt/Current website"
  PATH="/sessions/wizardly-funny-allen/.local/bin:$PATH" python3 content/manawatu-whanganui/tools/lint.py

STEP 2 — Read ALL claim YAMLs:
  cat /sessions/wizardly-funny-allen/mnt/Current\ website/content/manawatu-whanganui/data/claim/*.yaml

  Manawatu-Whanganui context:
  - Palmerston North (Manawatu): largest city; Massey University (AgriFood, vet school,
    distance education); NZDF bases (Linton Army, Ohakea RNZAF); food processing hub.
  - Whanganui city: Whanganui River (Te Awa Tupua — granted legal personhood under Te Awa
    Tupua Act 2017; first river in world with legal personhood); Sarjeant Gallery;
    ageing population; pockets of high deprivation.
  - Sub-regions: Rangitikei, Ruapehu, Horowhenua, Tararua districts.
  - Ruapehu: Mt Ruapehu (active volcano, lahar hazard; Ngati Tuwharetoa mana whenua);
    Whakapapa and Turoa ski fields; Tongariro National Park (World Heritage dual listing).
  - SH1 (spine route); Palmerston North Airport (main domestic hub for lower North Island);
    Palmerston North–Gisborne rail (freight only).
  - Whanganui River legal personhood: Te Awa Tupua (Whanganui River Claims Settlement)
    Act 2017 — do not describe as proposed or pending; it is enacted law.
  - Highest-risk claims: Whanganui River facts, Ruapehu volcanic/lahar hazard statistics,
    Massey University research/enrolment figures, NZDF employment numbers.

STEP 3 — Fix confirmed errors using bash heredoc ONLY. After every write, integrity check:
    python3 -c "
    import yaml, sys
    f = '/sessions/wizardly-funny-allen/mnt/Current website/content/manawatu-whanganui/data/claim/<file>.yaml'
    try:
        d = yaml.safe_load(open(f).read())
        bad = [k for k in ['source_ids','scoped_to','region_mentions'] if not isinstance(d.get(k),list)]
        if bad: print('NOT A LIST:', bad); sys.exit(1)
        print('OK:', d['id'])
    except Exception as e: print('PARSE ERROR:', e); sys.exit(1)
    "

STEP 4 — Bulk integrity check:
  python3 -c "
  import yaml, sys, re
  from pathlib import Path
  errors = []
  for f in sorted(Path('/sessions/wizardly-funny-allen/mnt/Current website/content/manawatu-whanganui/data/claim').glob('*.yaml')):
      try:
          d = yaml.safe_load(f.read_text())
          for k in ['source_ids','scoped_to','region_mentions']:
              if not isinstance(d.get(k), list): errors.append(f'{f.name}: {k} not a list')
          mt = d.get('methodology_tag')
          if mt and not re.match(r'^methodology\.[a-z][a-z0-9_]*_v[0-9]+$', str(mt)):
              errors.append(f'{f.name}: bad methodology_tag: {mt!r}')
      except Exception as e: errors.append(f'{f.name}: PARSE ERROR: {e}')
  if errors:
      for e in errors: print(e)
      sys.exit(1)
  print('All files OK')
  "

STEP 5 — Re-lint: 0 errors 0 warnings.
STEP 6 — Render: python3 content/manawatu-whanganui/tools/render.py --all 2>&1 | tail -5
STEP 7 — Smoke: 44/44 leaf routes.

DO NOT update CLAUDE.md. Return: entity count, lint, smoke, files changed + fixes.
```

---

## L4 — Marlborough (large, ~256 entities)

**NEVER use the Write tool for YAML. Use bash heredoc + integrity check after every write.**

```
You are performing a structured fact-check review of the Marlborough regional research
corpus. Part of the Aotearoa migration project at D:\ai-website-manager\Current website.

Region slug: marlborough

STEP 1 — Baseline lint:
  cd "/sessions/wizardly-funny-allen/mnt/Current website"
  PATH="/sessions/wizardly-funny-allen/.local/bin:$PATH" python3 content/marlborough/tools/lint.py

STEP 2 — Read ALL claim YAMLs:
  cat /sessions/wizardly-funny-allen/mnt/Current\ website/content/marlborough/data/claim/*.yaml

  Marlborough context:
  - Blenheim: sunniest city in NZ (2,400+ sunshine hours/year).
  - Marlborough Sounds: drowned river valleys; mussel and salmon aquaculture (Marlborough
    is NZ's largest mussel-producing region by volume); Queen Charlotte Track tourism.
  - Wine: Marlborough produces ~75-80% of NZ's wine by volume; Sauvignon Blanc dominant;
    ~28,000 ha under vine.
  - Kaikoura earthquake (14 November 2016, Mw 7.8): epicentre inland from Kaikoura town;
    massive landslides closed SH1 coastal route for ~1 year; damaged CentrePort Wellington;
    Coastal Pacific train (Picton-Christchurch) suspended for years. Marlborough was
    significantly affected by the SH1 closure and coastal rail disruption.
    NOTE: Kaikoura earthquake was 2016 — do not confuse with 2011 Christchurch quakes.
  - Cook Strait ferries: Interislander and Bluebridge operate Picton-Wellington.
    New Interislander ferry procurement has had significant delays and cost overruns
    as of 2025 — do not describe as completed or operational.
  - Highest-risk claims: wine hectares/volume (75-80% NZ production), aquaculture tonnage,
    Kaikoura damage figures (Marlborough portion vs national), Cook Strait ferry statistics.

STEP 3 — Fix confirmed errors using bash heredoc ONLY. After every write, integrity check:
    python3 -c "
    import yaml, sys
    f = '/sessions/wizardly-funny-allen/mnt/Current website/content/marlborough/data/claim/<file>.yaml'
    try:
        d = yaml.safe_load(open(f).read())
        bad = [k for k in ['source_ids','scoped_to','region_mentions'] if not isinstance(d.get(k),list)]
        if bad: print('NOT A LIST:', bad); sys.exit(1)
        print('OK:', d['id'])
    except Exception as e: print('PARSE ERROR:', e); sys.exit(1)
    "

STEP 4 — Bulk integrity check:
  python3 -c "
  import yaml, sys, re
  from pathlib import Path
  errors = []
  for f in sorted(Path('/sessions/wizardly-funny-allen/mnt/Current website/content/marlborough/data/claim').glob('*.yaml')):
      try:
          d = yaml.safe_load(f.read_text())
          for k in ['source_ids','scoped_to','region_mentions']:
              if not isinstance(d.get(k), list): errors.append(f'{f.name}: {k} not a list')
          mt = d.get('methodology_tag')
          if mt and not re.match(r'^methodology\.[a-z][a-z0-9_]*_v[0-9]+$', str(mt)):
              errors.append(f'{f.name}: bad methodology_tag: {mt!r}')
      except Exception as e: errors.append(f'{f.name}: PARSE ERROR: {e}')
  if errors:
      for e in errors: print(e)
      sys.exit(1)
  print('All files OK')
  "

STEP 5 — Re-lint: 0 errors 0 warnings.
STEP 6 — Render: python3 content/marlborough/tools/render.py --all 2>&1 | tail -5
STEP 7 — Smoke: 44/44 leaf routes.

DO NOT update CLAUDE.md. Return: entity count, lint, smoke, files changed + fixes.
```

---

## L5 — Otago (large, ~262 entities)

**NEVER use the Write tool for YAML. Use bash heredoc + integrity check after every write.**

```
You are performing a structured fact-check review of the Otago regional research corpus.
Part of the Aotearoa migration project at D:\ai-website-manager\Current website.

Region slug: otago

STEP 1 — Baseline lint:
  cd "/sessions/wizardly-funny-allen/mnt/Current website"
  PATH="/sessions/wizardly-funny-allen/.local/bin:$PATH" python3 content/otago/tools/lint.py

STEP 2 — Read ALL claim YAMLs:
  cat /sessions/wizardly-funny-allen/mnt/Current\ website/content/otago/data/claim/*.yaml

  Otago context:
  - Dunedin: largest city; University of Otago (oldest NZ university, founded 1869;
    ~20,000 students); Otago Polytechnic; Forsyth Barr Stadium (opened 2011, replaced
    Carisbrook); aging infrastructure; significant student economy.
  - Queenstown-Lakes: tourism capital of NZ; Queenstown (adventure tourism, Remarkables,
    Coronet Peak); Wanaka; housing unaffordability among highest in NZ (median multiple
    possibly >15x at recent peaks); significant short-term rental displacement of long-term
    housing stock; worker housing crisis severe.
  - Central Otago: gold rush history; stone fruit orcharding (cherries, apricots, peaches);
    wine (Central Otago Pinot Noir — southernmost wine region in the world).
  - Coastal Otago: Oamaru (blue penguin colony; steampunk); Waitaki district.
  - Kai Tahu / Ngai Tahu mana whenua across Otago (and most of South Island).
  - Dunedin Hospital rebuild: major capital project underway; one of NZ's largest
    infrastructure projects; significant cost escalations reported 2023-2024.
  - Highest-risk claims: Queenstown housing figures (do not confuse with national averages;
    they are extreme outliers), tourism visitor numbers (pre-COVID vs post-COVID distinction
    critical), Dunedin Hospital cost escalations, university enrolment numbers.

STEP 3 — Fix confirmed errors using bash heredoc ONLY. After every write, integrity check:
    python3 -c "
    import yaml, sys
    f = '/sessions/wizardly-funny-allen/mnt/Current website/content/otago/data/claim/<file>.yaml'
    try:
        d = yaml.safe_load(open(f).read())
        bad = [k for k in ['source_ids','scoped_to','region_mentions'] if not isinstance(d.get(k),list)]
        if bad: print('NOT A LIST:', bad); sys.exit(1)
        print('OK:', d['id'])
    except Exception as e: print('PARSE ERROR:', e); sys.exit(1)
    "

STEP 4 — Bulk integrity check:
  python3 -c "
  import yaml, sys, re
  from pathlib import Path
  errors = []
  for f in sorted(Path('/sessions/wizardly-funny-allen/mnt/Current website/content/otago/data/claim').glob('*.yaml')):
      try:
          d = yaml.safe_load(f.read_text())
          for k in ['source_ids','scoped_to','region_mentions']:
              if not isinstance(d.get(k), list): errors.append(f'{f.name}: {k} not a list')
          mt = d.get('methodology_tag')
          if mt and not re.match(r'^methodology\.[a-z][a-z0-9_]*_v[0-9]+$', str(mt)):
              errors.append(f'{f.name}: bad methodology_tag: {mt!r}')
      except Exception as e: errors.append(f'{f.name}: PARSE ERROR: {e}')
  if errors:
      for e in errors: print(e)
      sys.exit(1)
  print('All files OK')
  "

STEP 5 — Re-lint: 0 errors 0 warnings.
STEP 6 — Render: python3 content/otago/tools/render.py --all 2>&1 | tail -5
STEP 7 — Smoke: 44/44 leaf routes.

DO NOT update CLAUDE.md. Return: entity count, lint, smoke, files changed + fixes.
```

---

## L6 — Southland (large, ~259 entities)

**NEVER use the Write tool for YAML. Use bash heredoc + integrity check after every write.**

```
You are performing a structured fact-check review of the Southland regional research
corpus. Part of the Aotearoa migration project at D:\ai-website-manager\Current website.

Region slug: southland

STEP 1 — Baseline lint:
  cd "/sessions/wizardly-funny-allen/mnt/Current website"
  PATH="/sessions/wizardly-funny-allen/.local/bin:$PATH" python3 content/southland/tools/lint.py

STEP 2 — Read ALL claim YAMLs:
  cat /sessions/wizardly-funny-allen/mnt/Current\ website/content/southland/data/claim/*.yaml

  Southland context:
  - Invercargill: southernmost city in NZ; Ngai Tahu mana whenua throughout; significant
    Maori, Pacific, and migrant population; Al Hatch succeeded Sir Tim Shadbolt as mayor
    in 2022 after Shadbolt's very long tenure.
  - Gore: eastern Southland; country music capital of NZ; Hokonui Hills.
  - Fiordland: Milford Sound (Piopiotahi); Doubtful Sound; Fiordland National Park
    (largest NP in NZ at 1.26M ha). Milford Road (SH94) is avalanche-prone; Homer Tunnel
    is single-lane with traffic lights. Milford Sound received ~700,000+ visitors pre-COVID;
    substantially reduced during COVID; recovery ongoing but not yet at pre-COVID levels.
  - Tiwai Point aluminium smelter (Bluff): operated by New Zealand Aluminium Smelters
    (NZAS, Rio Tinto majority); ~1,000 direct jobs; consumes ~13% of NZ's electricity
    (supplied by Meridian Energy from Manapouri hydro); has faced repeated closure threats;
    contract extended to 2024, then further — verify current status carefully, do not
    state closure as completed if the smelter is still operating.
  - Fonterra Edendale: one of the world's largest dairy processing factories by milk intake.
  - Bluff oysters: Foveaux Strait dredge oyster fishery; iconic NZ product; quota-managed.
  - Stewart Island / Rakiura: small community (~400 permanent residents); Rakiura NP.
  - Highest-risk claims: Tiwai Point employment/power/closure status, Milford Sound
    visitor numbers (pre vs post COVID), Fonterra Edendale processing volume, Bluff
    oyster quota figures, Fiordland tourism revenue.

STEP 3 — Fix confirmed errors using bash heredoc ONLY. After every write, integrity check:
    python3 -c "
    import yaml, sys
    f = '/sessions/wizardly-funny-allen/mnt/Current website/content/southland/data/claim/<file>.yaml'
    try:
        d = yaml.safe_load(open(f).read())
        bad = [k for k in ['source_ids','scoped_to','region_mentions'] if not isinstance(d.get(k),list)]
        if bad: print('NOT A LIST:', bad); sys.exit(1)
        print('OK:', d['id'])
    except Exception as e: print('PARSE ERROR:', e); sys.exit(1)
    "

STEP 4 — Bulk integrity check:
  python3 -c "
  import yaml, sys, re
  from pathlib import Path
  errors = []
  for f in sorted(Path('/sessions/wizardly-funny-allen/mnt/Current website/content/southland/data/claim').glob('*.yaml')):
      try:
          d = yaml.safe_load(f.read_text())
          for k in ['source_ids','scoped_to','region_mentions']:
              if not isinstance(d.get(k), list): errors.append(f'{f.name}: {k} not a list')
          mt = d.get('methodology_tag')
          if mt and not re.match(r'^methodology\.[a-z][a-z0-9_]*_v[0-9]+$', str(mt)):
              errors.append(f'{f.name}: bad methodology_tag: {mt!r}')
      except Exception as e: errors.append(f'{f.name}: PARSE ERROR: {e}')
  if errors:
      for e in errors: print(e)
      sys.exit(1)
  print('All files OK')
  "

STEP 5 — Re-lint: 0 errors 0 warnings.
STEP 6 — Render: python3 content/southland/tools/render.py --all 2>&1 | tail -5
STEP 7 — Smoke: 44/44 leaf routes.

DO NOT update CLAUDE.md. Return: entity count, lint, smoke, files changed + fixes.
```

---

## L7 — Canterbury (large, ~289 entities)

**NEVER use the Write tool for YAML. Use bash heredoc + integrity check after every write.**

```
You are performing a structured fact-check review of the Canterbury regional research
corpus. Part of the Aotearoa migration project at D:\ai-website-manager\Current website.

Region slug: canterbury

STEP 1 — Baseline lint:
  cd "/sessions/wizardly-funny-allen/mnt/Current website"
  PATH="/sessions/wizardly-funny-allen/.local/bin:$PATH" python3 content/canterbury/tools/lint.py

STEP 2 — Read ALL claim YAMLs:
  cat /sessions/wizardly-funny-allen/mnt/Current\ website/content/canterbury/data/claim/*.yaml

  Canterbury context:
  - Christchurch: largest South Island city. Canterbury earthquake sequence:
      * Mw 7.1 — 4 September 2010 (Darfield); no deaths directly from quake.
      * Mw 6.3 — 22 February 2011 (Christchurch CBD); 185 deaths — deadliest NZ
        earthquake in 80 years. CTV building collapse: 115 of the 185 deaths.
      * Mw 6.0 — 13 June 2011 aftershock.
    DO NOT conflate the 2010 and 2011 events or their death tolls.
    Rebuild cost: ~$40B total (government + insurance combined); city centre substantially
    rebuilt; Christchurch Convention Centre opened 2022.
  - Canterbury Plains: most productive agricultural land in NZ; intensive dairy and arable
    farming; significant groundwater nitrate contamination (monitored by ECan /
    Environment Canterbury).
  - Port Hills fire: February 2017 — do NOT say 2022 (that was Nelson/Tasman).
    Lyttelton Harbour: Port of Lyttelton (major South Island import/export); Lyttelton
    Road Tunnel.
  - Alpine: Aoraki / Mt Cook (3,724 m; highest peak in NZ and Australasia); Mackenzie Basin;
    Lake Tekapo / Lake Pukaki; Waitaki hydro scheme.
  - Kaikoura: Kaikoura District is within Canterbury Regional Council boundary. The
    Kaikoura earthquake (Mw 7.8, 14 November 2016) epicentred near Kaikoura, not
    Christchurch — do not confuse with the 2010/2011 Canterbury quakes.
  - Highest-risk claims: earthquake death tolls (2010 vs 2011 must not be conflated),
    rebuild cost ($40B total, not government-only), Port Hills fire year (2017 not 2022),
    ECan nitrate data, agricultural output figures, Christchurch Airport passenger volumes
    (pre vs post COVID).

STEP 3 — Fix confirmed errors using bash heredoc ONLY. After every write, integrity check:
    python3 -c "
    import yaml, sys
    f = '/sessions/wizardly-funny-allen/mnt/Current website/content/canterbury/data/claim/<file>.yaml'
    try:
        d = yaml.safe_load(open(f).read())
        bad = [k for k in ['source_ids','scoped_to','region_mentions'] if not isinstance(d.get(k),list)]
        if bad: print('NOT A LIST:', bad); sys.exit(1)
        print('OK:', d['id'])
    except Exception as e: print('PARSE ERROR:', e); sys.exit(1)
    "

STEP 4 — Bulk integrity check:
  python3 -c "
  import yaml, sys, re
  from pathlib import Path
  errors = []
  for f in sorted(Path('/sessions/wizardly-funny-allen/mnt/Current website/content/canterbury/data/claim').glob('*.yaml')):
      try:
          d = yaml.safe_load(f.read_text())
          for k in ['source_ids','scoped_to','region_mentions']:
              if not isinstance(d.get(k), list): errors.append(f'{f.name}: {k} not a list')
          mt = d.get('methodology_tag')
          if mt and not re.match(r'^methodology\.[a-z][a-z0-9_]*_v[0-9]+$', str(mt)):
              errors.append(f'{f.name}: bad methodology_tag: {mt!r}')
      except Exception as e: errors.append(f'{f.name}: PARSE ERROR: {e}')
  if errors:
      for e in errors: print(e)
      sys.exit(1)
  print('All files OK')
  "

STEP 5 — Re-lint: 0 errors 0 warnings.
STEP 6 — Render: python3 content/canterbury/tools/render.py --all 2>&1 | tail -5
STEP 7 — Smoke: 44/44 leaf routes.

DO NOT update CLAUDE.md. Return: entity count, lint, smoke, files changed + fixes.
```
