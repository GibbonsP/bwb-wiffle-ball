# BWB Wiffleball Career Register — build kit

Interactive single-file HTML site for the Brookside Wiffleball League (every player + franchise, 2017–2026).

Live Artifact: https://claude.ai/code/artifact/38e0593f-f6fc-4444-a77b-b426ed2e5853

## Pipeline

    python3 build.py      # reads source data -> players.json  (needs pandas, numpy, openpyxl)
    python3 generate.py   # reads players.json -> index.html   (this is the Artifact; stdlib only)

`build.py` needs `pandas`/`numpy`/`openpyxl`; a fresh machine/session may need
`pip3 install --user pandas numpy openpyxl` first. `generate.py` has no
dependencies beyond the standard library.

## Files

- `build.py`      — data pipeline. Reads the xlsx + CSVs + `pw_*.json` + `data_2016.py` + `beavers_2026.py`.
- `generate.py`   — HTML/JS generator (all CSS + the SPA). Writes `index.html`.
  Franchise colours live in `FRANCHISE_COLORS` (from the club wordmark sheet:
  primary `p` / secondary `s`); `teamAccent()` derives a theme-neutral accent and
  `setTeamVars()` puts `--tp/--ts/--tc` on `#app` for team hero bands, player-page
  name/card accents, standings chips and the ticker. `sparkline()` draws the
  season-trajectory SVGs (player OPS/ERA, team win %). Leader lists carry a
  ranking bar via `--w` on each `<li>`. The home page shows a reigning-champion
  band tinted with that club's colours.
  Player pages carry a compact Baseball-Savant-style "Percentile Rankings" card
  (`savantCard`) with a season toggle — ranks a player's chosen regular season vs
  that season's qualified pool (9+ G batting, 12+ IP pitching), client-side.
  K%/BB%/ERA/WHIP/BB3/OPP-AVG are ranked low-is-better. The picked year is sticky
  across player pages (`svYear`).
  The Players index sorts and groups by surname (`nameLast`/`nameParts`, suffix-aware)
  and shows "Last, First" (`nameLF`). Roster / leaderboard-style tables (`class="detail sortable"`)
  get click-to-sort via `makeSortable()`; naturally-ordered tables (by season, box
  scores, game logs) do not. The `CHAMPS` score field is the champion's combined
  regular-season + postseason record that year (2026 Shelton Shock = 14-5); the
  champs-page column is labeled "Overall".
  All-Time Head-to-Head moved back above the year chips (always visible, not
  gated behind "All years") per user feedback.
  New **Records** page (nav "Records", `renderRecords()`): Single-Season Records
  (top 10 per category from individual player-seasons, regular season only,
  multi-team seasons combined) and Single-Game Records (top 10 per category from
  recorded box scores, regular season + playoffs), both batting and pitching,
  reusing the `llist`/leader-card styling from the Leaders page. Also a
  **No-Hitters & Perfect Games** table.

  No-hitters/perfect games were first computed heuristically from box scores,
  but the user supplied the league's own hand-kept log (more complete and goes
  back to 2013, well before per-game data exists) — that heuristic was ripped
  out and replaced. Source: `source/Career_All-Time Franchise & League
  Individual Stats - No Hitters_Perfect Games.csv` (also read live from
  `~/Downloads/`). build.py's `# NO-HITTERS / PERFECT GAMES` section (near the
  end, before `out = {...}`) parses it — columns Player/Team/Opponent/Field/
  Date/IP/BB/K/Score/Result/Notes — stopping at the first blank row (the CSV's
  own hand-tallied summary table below that is stale, missing 2026 entries, and
  is ignored). Team/opponent nicknames run through the existing `NICK_FIX` +
  `canon_team(year, name)` (the same historical-rename machinery used
  everywhere else), which resolves them correctly with zero new mapping tables.
  Dates: `M/D/YY`, a trailing `*` = postseason, or the one `"Month YYYY"` entry
  (April 2013, no day given). Player names resolve via the existing `pkey()`.
  Each row also gets a best-effort `gid` match against the built `games` dict
  (same date + same two canonical teams) so the date can link to a box score —
  works for 2017+ (36 of 38 rows), not for the 2013–2016 entries (no per-game
  data that far back) or two 2023/2025 rows whose exact date has no matching
  game record. Emitted as `out['noHitters']`; generate.py reads `DB.noHitters`
  directly (`const NOHIT = ...`) — no client-side detection anymore. 38 entries,
  3 perfect games, as of the 2013–2026 log. Feeds both the Records page table
  (with Score/Notes columns — the notes are the fun part, e.g. "World Series
  clinching win!") and a "No-Hitters" block in each pitcher's Accolades section.
  Team page layout was cleaned up: the "All years / <year>" chips used to sit
  below four always-shown all-time sections (season record, batting-by-season,
  pitching-by-season, head-to-head) that ignored the chip entirely. Now only the
  compact `teamRecordTable()` overview sits above the chips; batting-by-season,
  pitching-by-season, head-to-head and the all-time roster (`teamStatsBySeason()`
  + `teamH2H()` + `teamAllYears()`) render together under the "All years" chip,
  so a specific year shows just that year's record cards/roster/game log with
  nothing left over from the all-time view. (`teamSeasonTables()` was split into
  `teamRecordTable()` + `teamStatsBySeason()`.)
  Each team page has an "All-Time Head-to-Head" table (`teamH2H()`) — franchise
  series record vs every opponent it's ever played, regular season + playoffs
  combined (exhibition/All-Star excluded), sortable, with clickable opponent
  links; footer row totals reconcile to the franchise's regular+playoff game count.
  Roster entries are dropped in build.py when the player logged 0 games in every
  phase for that club/year (rostered but never appeared); `rosterBatting` also
  hides rows with no PA so Fall/exhibition-only entries don't render as blanks.
  Playoff brackets: `PLAYOFFS_RAW` in build.py (per year: Brookside seeds,
  Brentwood seeds, the two finalists, champion — nicknames as used that year,
  resolved to canonical franchises via `canon_team`). Each semifinal's winner is
  whichever seed reached the final. `playoffBracket()` in generate.py renders it
  on the Standings page for the selected season, franchise-coloured, with full
  team names (`histName`, the name used that year) and each series' game scores
  (`_pk_series` pulls the playoff-phase games between the two seeds from the team
  game logs; blank where a game wasn't recorded, e.g. some early finals).
  The Teams page shows a static `FRANCHISE_SUMMARY` table (full league history
  2012–present: W/L, years, WS titles/appearances, division titles, playoff
  appearances, winning seasons, All-Star count, all-time playoff record) above
  separate All-Time Team Batting and Team Pitching tables (stat-database era only,
  so their win totals won't match the summary). All three are click-sortable.
- `data_2016.py`  — 2016 cumulative-stat supplement. Currently GATED OFF (`INCLUDE_2016 = False` in build.py).
- `beavers_2026.py` — Brookside Beavers, 2026 NWLA National Tournament (GameChanger),
  transcribed from box-score screenshots. Two-sided box scores (`bat`/`pit` +
  `opp_bat`/`opp_pit`), phase per game (Pool Play / Death Bracket / Bracket Play).
  Feeds the standalone `beavers` block + the "Beavers" page, and an "NWLA Tournament"
  phase block on each player's profile (type `NWLA` season rows, kept separate from
  league regular/postseason totals). Beavers lines reconcile to the printed team
  totals; opponent batting is best-effort (per-game `opp_note` flags the few cells
  — G1/G2/G3 R-or-RBI, G7 ~2 R / 1 SO — that couldn't be pinned).
- `players.json`  — last build output.
- `index.html`    — last generated site (matches the published Artifact).
- `pw_*.json`     — prowiffleball.com API dumps for 2026 (league id 5 = Brookside Wiffleball League).
- `source/`       — raw inputs (xlsx + CSVs).

## Path note

`build.py` currently reads its inputs from `~/Downloads/` (`DL` variable near the top,
plus a hardcoded xlsx path around line 88, and the awards CSV around line 760).
The same source files are copied into `source/` here. To rebuild from this folder,
point `DL` (and the xlsx path) at `source/`, or keep the originals in `~/Downloads/`.

## Data sources

- `source/BWB League Lineup Export.xlsx` — sheet `Player_Stats_with_Game_Info` (header row 2), one row per player-game. 2017–2025.
- `source/games.csv`, `source/team_player_lookup.csv` — team affiliation (PlayerID -> TeamID -> name).
- `source/BWB League Lineup Export - Games.csv` — clean line scores for box scores.
- `source/2026 BWB Season 2.0 - Franchise Name Timeline.csv` — franchise-name canonicalization.
- `source/2026 BWB Season 2.0 - ASG History.csv` — All-Star Game history.
- `source/Career_All-Time ... All-Time Awards By Year 2012-.csv` — annual awards.
- `pw_*.json` — 2026, from prowiffleball.com public JSON API. 2026 **season
  totals** (batting + pitching, regular + playoffs) are taken straight from
  `pw_{batting,pitching}-stats.json` and the `-po` variants so they match the
  site's player profiles and stat leaders exactly; earned runs aren't published,
  so ER is derived from ERA (`ER = round(ERA * IP / 3)`, ERA being per 3 IP).
  Play-by-play (`pw_boxes.json`) still feeds the per-game box scores. The
  lineup feed's per-game IP/H/BB/K are reliable, but its runs figure and game
  ERA don't tie out to the official season line, so `build.py` spreads each
  2026 pitcher's profile R and ER across his games (proportional to the
  lineup's per-game runs) — every box-score pitching column now sums to the
  player's profile. To refresh:
  re-curl `/api/leagues/5/{batting-stats,pitching-stats}?showAll=true&playoffs={false,true}`,
  `/api/leagues/5/games?pageSize=300`, `/api/leagues/5/teams`, and per-game
  `/api/scores/{id}/{box-score,lineups,plays}` into `pw_boxes.json`.

## Live editing (owner-only)

The site now declares the `artifact` capability and can save edits from
inside the page itself — **no db capability used**: that would have made the
whole artifact organization-internal (can't be shared by link anymore), which
defeats the point of a page the league browses. `artifact.publish()` keeps
public link-sharing intact and enforces "owner only" at the platform level
(a non-owner's `publish()` call rejects `not_writer`/`not_granted` — that's
the real access control, not just hiding buttons).

How it works (`generate.py`, "LIVE EDITING" section): an edit mutates the
in-memory `DB` object (same object every render function already reads —
nothing else had to change), recomputes any derived fields that depend on
what changed, then `saveDB()` fetches this artifact's own current HTML
(`fetch(location.href)` — never serializes the live DOM, which carries
routed-page state), splices the updated `JSON.stringify(DB)` into the
`<script id="data">` block, and calls `artifact.publish(html)` with the
result. A successful publish reloads the page with the new data. A failed
one (`not_writer`, `conflict`, or anything else) rolls the in-memory edit
back and re-renders the form so nothing is left in a half-saved state.
**Gotcha hit once, worth remembering**: a literal `</script>` inside a JS
string anywhere in the inline script silently truncates it at the HTML
parser level (it doesn't know JS from a string literal) — write it as
`'<'+'/script>'` instead, as `saveDB()` does when it searches for the data
block's closing tag.

Shipped so far: **player season-row editing** — the "✎ Edit seasons" button
on each player page (visible once `claude.use('artifact')` resolves) opens a
form per season row (all batting/pitching/fielding fields; H, TB, PA and
IP-outs are derived automatically, matching build.py's `agg()`), with
add-row and delete-row. Saving recomputes that player's `career`/`careerReg`/
`careerPO`/`years`/`teamsByYear` from the edited `seasons` array
(`recomputePlayer()` — mirrors build.py's aggregation) — this is exactly the
kind of fix the Victor Cottini duplicate needed, now doable from the page
instead of editing CSVs and rerunning the pipeline.

**Not yet built** (explicitly scoped out of this pass — user asked for
"everything," but shipping one tested piece beats a rushed pass across five
data shapes at once): editing/adding a game's full box score, and editing
the curated lists (Awards, No-Hitters, Champions, ASG rosters). Same
`saveDB()`/modal plumbing would carry over directly; box-score edits would
also need to recompute the two affected teams' season/career records
(`teams[*].seasons[y].record` / `.games` / `.record`), and curated-list edits
would need to recompute affected players' `honors` (rings/awards/asg) the
way build.py currently derives them via `pkey()`/`plink()` name-matching.

**Caveat**: capabilities only resolve inside a Claude-served view (chat
panel, artifacts gallery) — opening the raw public link as a standalone page
resolves every `claude.use()` call to `null` "for now" per the platform
contract, so editing only works for the owner while viewing through Claude,
not from the bare shared URL. Everyone else's read-only experience is
unaffected either way.

## Editable visuals (logos, photos, banner) + a reusable bar chart

Same tradeoff as the live-editing decision: the capability for real uploaded
file storage (`assets`) *also* makes the artifact organization-internal — no
public link-sharing — so images are embedded as base64 data URIs in `DB`
instead (same "edit in memory, republish the whole page" pipeline as stats).
`resizeImageFile()` (canvas-based, client-side) downscales + recompresses to
JPEG before anything is saved, since every viewer's browser downloads the
*whole* page — all stats, every image — and that has to fit under the
artifact's 16MB cap. Team logos cap at 200px, player photos 240px, the home
banner 900px, all at ~0.75 JPEG quality.

Shipped: **team logos** (`TEAMS[name].logo`, "✎ Edit logo" on team pages, shown
in the hero), **player photos** (`P[name].photo`, "✎ Edit photo" on player
pages), **home banner** (`DB.banner`, "✎ Edit banner" on the home page) — all
via one generic `openImageEditor(title, currentUrl, maxDim, onSave)` modal
(pick → resize → preview → Save/Remove), reusing the exact same `saveDB()` /
rollback-on-failure plumbing the season editor uses.

Also added `barChart()` — a generic horizontal-bar SVG helper (reused the
`sparkline()` theme-color conventions) with auto-sizing label width so long
team names don't clip. Tried it on the Standings page (win% by team) per the
original "more charts" ask; **user said no bar graphs on Standings**, so that
call site was removed — the `barChart()` function itself is still there,
unused, ready if a chart is wanted somewhere else later.

## Social links (Instagram / YouTube)

`@bwbwiffleball` on both. Two spots, both plain outbound links (inline SVG
icons, `currentColor` so they follow the theme) — no live embed: Instagram
has no widget script on the CDN allowlist, and a YouTube *channel* can't be
iframe-embedded (only a specific video, via `/embed/<id>`), so both stayed as
link-out cards rather than half-working embeds. `<footer class="sitefoot">`
(icon pair, site-wide, right after `#app`) and a "Follow BWB Wiffleball"
section on the home page (`.followgrid`, bigger cards with platform name +
handle). If a specific YouTube video ever comes up (highlight reel, channel
trailer), that one's a real iframe embed away — just needs the video's id/url.

## Head-to-head year-by-year drilldown

Each row in the All-Time Head-to-Head table now has a ▸ toggle that expands
a nested Year/W–L/PCT/RF/RA/Diff table for that one opponent, built from a
`byYear` map added alongside the existing aggregate accumulator in
`teamH2H()` (same per-game loop, just also bucketed by year). Rewrote the
table by hand (not `statTable()`, which has no concept of a per-row detail
row) so each opponent renders as a `<tr class="h2hrow">` immediately followed
by a `<tr class="h2hdetail" hidden>` holding the nested table in a
`colspan`'d cell; `.h2htoggle` click flips `hidden` and the ▸/▾ glyph.
**Dropped `sortable`** from this table — column-sort works by physically
reordering `<tr>` elements in the tbody, which would separate a `h2hrow`
from its own `h2hdetail` sibling the first time someone sorted; the default
order (most games played against that opponent, descending) is still the
right "most significant rivalries first" view. Verified expand, collapse,
and that the opponent name link still navigates instead of just toggling.

## Full franchise names on Teams page + a real home page

**Teams page bug**: the "Franchise Summary" table (top of `#/teams`) showed
bare nicknames ("Panthers", "Sox", "Squirrels") while every other table on
the site — including the "All-Time Team Batting/Pitching" tables right below
it on the same page — shows the full "Location Nickname" form. Root cause:
`FRANCHISE_SUMMARY`'s row objects only had a `t` (nickname) and `f` (link
target, `null` for the 6 defunct-before-2017 franchises with no live team
page: Sox, Royals, Aces, Squirrels, Angels, Diablos) — the display text used
`d.t` unconditionally. Fixed by adding an explicit `full:` field with the
correct historical location for those 6 (Davenport Sox, Brookside Royals,
Brentwood Aces, Brookside Squirrels, Downtown Angels, Gleason Diablos — all
already known from `PREFIX` in build.py, just not previously threaded through
to this one hardcoded JS table) and rendering `d.f || d.full || d.t`. Search
filter (`match()`) updated to also match against `d.full`.

**Home page**: replaced the `.homenav` grid of 8 buttons (Players/Teams/
Standings/Leaders/Games/Champs/Awards/Beavers) with a **Standings Snapshot**
— those buttons were pure navigation, entirely redundant with the top nav
tabs sitting right above them, and added no information of their own. The
snapshot shows each division's top 3 teams (logo, name, W–L) for the most
recent year with division data (`ALL_YEARS.filter(y=>DB.divisions[y])`,
reusing `standRow()` — already a top-level function, no duplicate logic
needed) plus a "Full standings, any season →" link. Old dead CSS (`.homenav`/
`.hcard`) removed; the old `data-go` nav-button wiring generalized to any
`[data-go]` element so the new "Full standings" link (and anything similar
later) works the same way.

## Bigger logos + a real duplicate-player fix (Tom/Tommy Giandomenico)

Bumped `.champlogo` 36→60px and `.stlogo` 26→44px — both still sourced from
320px originals, so no quality loss.

User also caught a genuine data bug: **Tom Giandomenico** and **Tommy
Giandomenico** were two separate player entries for the same person (2026
stat rows used "Tom", 2025 used "Tommy" — a spelling inconsistency in the
source Excel, same pattern as the Dan/Daniel Brady and A.J./AJ Cefaloni
merges already in `ALIAS`). Merged into **Tom Giandomenico** (kept — it
already had the headshot) in `players.json`: combined `seasons` (now 2
years), recomputed `career`/`careerReg`/`careerPO`/`years`/`teamsByYear`,
merged `gids`/`honors`, renamed every `"Tommy Giandomenico"` in `games`
box scores *and* in `TEAMS[*].seasons[*].roster` (missed this second spot
on the first pass — a name merge has to touch both places any per-game or
per-team-roster data denormalizes the player name into its own record, not
just the top-level `players` dict). Added `'Tommy Giandomenico':'Tom
Giandomenico'` to build.py's `ALIAS` map so a from-scratch rebuild merges
them automatically too, matching the existing Dan Brady / AJ Cefaloni /
Evan Wilkins entries there. Worth a periodic check: search `players.json`
for other close-spelling name pairs the same way this one was found.

## Champs/standings follow-up: photo fit, captain-for-all-years, logos everywhere

- **Photo not fitting at full screen**: `.champphoto` was `width:100%;object-fit:cover` —
  on a wide viewport that stretches a ~700px source past its native size and
  `cover` crops whatever doesn't fit the box. Switched to `max-width:100%;
  height:auto;max-height:520px;object-fit:contain`, centered — shows the
  whole photo at its natural aspect ratio, never upscaled past source
  resolution, on any screen width.
- **Captain applies to every title year for that franchise**, not just the
  years with a photo: Peter Fraioli now captains all 5 Panthers titles
  (2014/16/17/21/25), Parker Gibbons all 3 Kraken titles (2013/15/24), plus
  Shock 2026 → **TJ Ciafone** (the missing one from last time).
- **Roster lists the captain first** — `champsSection()` moves `c.captain`
  to the front of the roster array before rendering, instead of leaving them
  wherever they fell in the roster order with just a badge.
- **Team logos added in two more places**: each champion card's `<h4>` now
  shows `TEAMS[c.tm].logo` (`.champlogo`, 36px) next to the year/team name;
  the Standings table's team column shows the same logo (`.stlogo`, 26px) in
  place of the plain `.clubdot` color swatch — teams without a logo on file
  still fall back to the color dot, so nothing goes blank.

## Championship photos + full rosters + captains

`~/Desktop/Champioship Photos/` (9 photos, 2018–2026, one per title team) →
resized to 700px wide, JPEG q78 (~680KB combined) → merged as a `photo` field
onto the matching year's entry in `players.json`'s `champs` array. Matched
each photo's year to that year's champion via the existing `CHAMPS` table in
build.py (e.g. 2026→Shelton Shock, 2024→Brookside Kraken) — visually spot-
checked 2026 against the photo to confirm (Shock jerseys, 2026 trophy).

User also gave franchise→captain mappings ("Panthers is Peter", "Kraken is
Parker", etc.) — applied as a `captain` field on each matching year's champs
entry (Panthers→Peter Fraioli for both its 2021 and 2025 titles, Gladiators→
Austin Corvino for 2022 and 2023, etc.) using each team's *canonical* full
player name. **Shelton Shock (2026) has no captain set** — "Shock" wasn't
among the names given (the list included "Sox is Kento" instead, which
doesn't match any of these 9 photo years since Davenport Sox last won in
2012) — ask the user for 2026's captain and set `captain` on that one champs
entry when they answer. Applied "Sox is Kento" (Kento Kamezaki) to the 2012
entry anyway, even without a photo, since it's still valid info they gave.

`champsSection()` in generate.py was rewritten from a single flat table to
one card per year (`.champyear`): photo (where set) + a two-column roster
list. Roster comes from `TEAMS[<franchise>].seasons[<year>].roster` (the
same real per-club-per-year stat roster every team page already uses) when
that year is in the stat database (2017+); years before that (2012–2016)
fall back to the hand-curated notable-players list (`champs[*].pl`) that
was always there, since there's no per-team roster data that far back.
Captain marking reuses the *existing* `plink()` "(C)" convention (already
used for ASG captains) rather than inventing a new one — pass `"Name (C)"`
and it renders the same `.cap` badge automatically. Source photos archived
to `source/champ_photos/`.

## Team / division / league logos

`~/Downloads/Team Logos/` (10 PNGs, all RGBA/transparent, 1080–2000px) →
resized+PNG-optimized with Pillow (kept PNG, not JPEG, to preserve
transparency — unlike headshots/banner which are opaque photos and fine as
JPEG) and merged into `players.json`:

- **6 current-team logos** (200px) → `TEAMS[<franchise>].logo`: Kingslogo→Harris
  Kings, snappingturtles→Silver Lake Snapping Turtles, kraken26→Brookside
  Kraken, glads26→Brentwood Gladiators, PanthersLogoNewestnoback→Brookside
  Panthers, Shock2026logo→Shelton Shock. Same field the live "Edit logo"
  button writes to, so these are just pre-filled versions of that.
- **2 division crests** (160px) → new `DB.divisionLogos = {Brookside, Brentwood}`,
  shown next to each division's `.divh` header on the Standings page (only
  when a logo exists for that division name — old North/South years show
  no icon, which is correct, they never had one).
- **League crest** `bwbLogo24.png` (260px) → new `DB.leagueLogo`, shown in
  the site header next to the "BWB Wiffleball" wordmark (`#brandLogo`, set
  once via JS right after `DB` loads — it's a static header element outside
  the router, so it doesn't belong inside any `render*()` function).
- **15th Anniversary badge** `15thAnniversaryBWBLogo.png` (2012–2026, 220px)
  → new `DB.anniversaryLogo`, shown on the home page next to the intro
  paragraph (`.leadrow`/`.annivbadge`).

Re-processed at higher resolution after user feedback that they read too
small (320px for team/anniversary, 260px division, 380px league — up from
200/160/220/260) and doubled the display sizes to match: `.tlogo` 56→92px,
`#brandLogo img` 42→64px, `.divlogo` 28→48px, `.annivbadge` 84→130px. ~430KB
combined now → page at 2.62MB, still far under the cap. Source PNGs archived
to `source/logos/`. None of these four new fields
(`divisionLogos`, `leagueLogo`, `anniversaryLogo`, plus the 6 team `.logo`s)
have an edit-UI control yet — they were set directly in `players.json` like
the headshots, not through the site. Same build.py warning applies: don't
re-run it without merging these back in.

## Historical (era) logos + postseason/World Series crests

User handed over a second batch, `~/Downloads/Team Logos 2/` (38 PNGs, named
`<Nickname> Logo <years>.png`). 4 were byte-identical (checked by MD5) to
files already loaded above — `bwbLogo24.png`, `15thAnniversaryBWBLogo.png`,
`BrooksideDivision.png`, `BrentwoodDivision.png` — and skipped. 6 more were
byte-identical to the 6 current-team `.logo`s already embedded (e.g. "Kraken
Logo 2026-Present.png" = `kraken26 (3).png`); rather than re-encode those,
their bytes were reused as-is when extending that team's history. The
remaining 28 (22 team-era + 6 postseason/World Series) were genuinely new,
resized the same way as before (320px longest side, PNG, Pillow) and merged
into `players.json`, archived to `source/logos2/`.

**Per-era team logos** — each live `TEAMS[<franchise>]` gained a
`logoHistory: [{from, to, logo}]` array (`to:null` = current/open-ended),
sorted ascending; `.logo` is kept in sync as the most recent entry (same
field the "Edit logo" button writes, so old behavior is unaffected). A new
`teamLogoForYear(full, y)` in generate.py (next to `histName`, same
from/to-range scan) is now what every year-scoped view calls instead of
reading `.logo` directly: the Standings page (`stMark`), the Champions page
(`champsSection`), and the Home page standings snapshot. The Team page hero
still shows `.logo` (current), since that page isn't year-scoped. Two
franchises needed their *historical* nickname-era logo attributed to the
*current* franchise name, reusing the existing `AWARD_TEAM_ALIAS` mapping as
the source of truth: "Dashers Logo 2016-2017.png" → Brentwood Braves (2016
was the Braves' "Dashers" era) and "Special K's Logo 2018-2021.png" → Harris
Kings. "Devils Logo 2013-2014.png" has no matching franchise nickname
anywhere in the data — its years exactly match the Diablos entry in
`FRANCHISE_SUMMARY` (2013–2014), so it's stored as that franchise's crest;
the graphic itself apparently reads "Devils" even though the franchise is
recorded as "Diablos" everywhere else.

**Defunct-franchise crests** — six franchises with no live `TEAMS` entry
(Sox, Royals, Aces, Squirrels, Angels, Diablos — the same six that got a
`full:` fallback name on `FRANCHISE_SUMMARY` earlier) got one crest each in
a new top-level `DB.franchiseLogos = {<nickname>: <dataURI>}`, keyed by the
`t` field of their `FRANCHISE_SUMMARY` row. Shown next to their row on the
Teams directory (`.fdotlogo`, 26px) alongside the six live franchises' own
`.logo` — every row in the Franchise Summary table now has an icon.
`champsSection()` also falls back to this map for the pre-stat-era
champions who have no `c.tm` (e.g. 2012 Davenport Sox): it looks up the
matching `FRANCHISE_SUMMARY` row by `d.full===c.full`.

**Postseason & World Series crests** (2024–2026 only — the only years the
user had them for) — two new top-level maps, `DB.postseasonLogos` and
`DB.worldSeriesLogos`, both keyed by year string. Rendered together as a
`.champbadges` row (52px each) on the relevant year's Champions card,
between the header and the champion photo — postseason crest first, then
the World Series matchup crest. Nothing shown for other years, which is
correct (no assets exist for them).

~570KB of new image data → page now 6.58MB, still well under the 16MB cap.
Same standing warning: these fields aren't in build.py's pipeline; don't
re-run it without merging them back in first.

Follow-up: added a "Logo History" section to the Team page itself
(`teamLogoHistory()`, called from `teamDetail()` right under the hero),
showing every crest in `t.logoHistory` most-recent-first with its year
range. Only renders when a franchise has 2+ eras on record (`hist.length<2`
→ skip) — a team with just one logo already shows it in the hero, a second
copy in a "history" strip would be noise.

## Bulk player headshots

User handed over `~/Downloads/Pictures/` — 44 PNGs named `<Player Name>.png`.
Matched 43 of them straight to `players.json` keys (one rename needed:
`Danny ElJamal.png` → `Danny Eljamal`, case fix; one skipped as a dup:
`JohnLuke Viti.png`, since `John-Luke Viti.png` already covers that player).
Resized to 240px on the long side + recompressed to JPEG q75 with Pillow
(same numbers the client-side `resizeImageFile()` uses for player photos —
kept them consistent since both paths write to the same `players[*].photo`
field), then merged directly into `players.json`. ~591KB total for all 43,
page landed at 2.05MB — nowhere near the 16MB cap. Source PNGs archived to
`source/headshots/` for the kit. `pip3 install --user pillow` if a fresh
machine doesn't have it (same as pandas/numpy/openpyxl for build.py).

**Important**: this went straight into `players.json`, bypassing build.py
entirely (photos aren't part of its pipeline, and never should be — it reads
from the Excel/CSV exports, which don't know about photos at all). **Re-running
build.py from scratch would silently wipe every photo, logo, and banner**
that's been added this way, along with any live edits made through the
site itself (like Parker Gibbons' own photo upload, merged in a few messages
back). If build.py ever needs to run again for a real data refresh, merge its
fresh output's `players`/`teams`/`games`/etc. into the current `players.json`
— don't just overwrite it — the same way the live-edit merge was done above.

## ProWiffleball link + a live-edit merge

Added a third link (footer icon + home "Follow" card, `https://prowiffleball.com/leagues/5`)
alongside Instagram/YouTube — same plain-link pattern, described as "Live
stats & box scores" since it's a data source, not a social account. Icon is
a hand-recreated inline-SVG "PRO" badge (blue rounded square, white bold
italic text) matching ProWiffleball's own mark — the user pasted the real
logo image in chat, but there was no way to pull its actual file bytes into
this pipeline, so it's a vector recreation of the badge portion rather than
the source file. Fixed brand color (`#1e4fa8`), not theme-linked, same as
the Instagram gradient / YouTube red already do.

While doing this, an `artifact-changed` notification showed the live artifact
had moved ahead of this session's last publish — the user had tried the new
photo-upload feature for real and set Parker Gibbons' own player photo. Before
publishing the ProWiffleball change, read the live artifact back, extracted
its embedded data blob, diffed it against local `players.json` (a systemic
`0.0`→`0` float-formatting difference showed up everywhere — cosmetic, from
the round-trip through `JSON.parse`/`JSON.stringify` in the browser, not a
real change), found the one real diff (Parker Gibbons' `photo` field), and
merged just that into `players.json` before regenerating — so the live photo
edit didn't get clobbered by this session's next publish. Worth remembering:
**always re-read + diff the live artifact before publishing after an
`artifact-changed` notification**, since edits can now happen from the page
itself, not only from this pipeline.

## Data integrity check (added after a real duplicate was found)

User caught Victor Cottini's 2022 combined line showing .450 AVG / 27 H instead
of the correct .420 / 21 H. Root cause: the source Excel had his 6/17/2022
Panthers@Dragons game logged **twice** under two different PlayerIDs (14451771,
his usual Shelton Shock registration, and 14500771, a one-off) — both rows hit
the same GameID with identical stats. Since PlayerID→team is a season-long
lookup (not per-game), the row under his normal Shock PlayerID got bucketed
into "Shelton Shock" even though that specific game was Panthers vs. Dragons —
double-counting one 10-AB/6-H game into his season total.

Fixed in build.py: right after `df['TeamName']` is assigned, a new check builds
`_gid_teams` (GameID -> the two canonical teams that actually played that game,
from games.csv) and drops any row whose looked-up TeamName isn't one of them —
a `PlayerID`-to-team mismatch means a stray/duplicate registration, not a real
appearance for that club. Scanned the full 2017–2026 Regular+Playoffs dataset:
**exactly one** such row existed (this one); build.py now prints what it drops
so a future data refresh surfaces any new ones instead of silently baking them in.

## Design refresh — "less vibe-coded"

User feedback: the site read as a generic AI-generated dashboard. Root
causes and fixes, all CSS/markup-only in `generate.py` (no data or logic
changes):

- **Palette** was a stock dark-navy-SaaS blue (`--accent:#1f3a93`/`#88a6f2`).
  Repainted `:root` (light) and both dark blocks (`@media` + `[data-theme]`)
  to a scheme grounded in the actual sport: `--accent` is now a deep field
  green (`#2b6b4a` light / `#7fbf8a` dark — the color of the diamond, and it
  already lines up with the existing pos/neg convention on run differential),
  `--clay` a muted brick/infield red (was a brighter stock red), `--gold`
  dialed back toward antique bronze (trophies, not UI chrome). Light paper
  shifted off pure dashboard-white to a warm stone tone; dark paper shifted
  from navy to a warm near-black ("under the lights" rather than "SaaS dark
  mode").
- **Wordmark** was two competing accent colors (clay "BWB" + accent-blue
  "Wiffleball") — classic AI two-tone-everything default. "Wiffleball" now
  just takes `--ink`; one accent pop (the clay red) reads more confident
  than two.
- **Rainbow gradient bar under the header** (`.perf`) — a 3-stop
  clay→gold→accent gradient, the generic "AI dashboard progress strip."
  Replaced with a single solid rule. It still recolors itself to the
  reigning champion's team color via `--pa` (unchanged JS at the bottom of
  the file) — kept the meaningful behavior, dropped the decorative gradient.
- **Every repeated block was an identically rounded, identically shadowed
  card** — stat tiles, `.split`, `.rec`, `.snapdiv`, `.sparkcard`, `.llist`,
  `.champyear`, `.asgyear`, `.followcard`, `.logohist-item` all shared
  `border-radius:12px` + `box-shadow:var(--shadow)`. Stripped the shadow and
  tightened the radius to 8px on all of these so they read as flat ledger
  entries instead of floating UI cards. Shadow+radius is now reserved for
  genuinely elevated moments only: the team hero banner, the reigning-champs
  bar, the playoff bracket trophy card, and the edit modal — spending the
  effect by role instead of stamping it on everything.
- **Section headers** (`.hsub`) had the "title ---------" pattern (flex-box
  heading with a `::after` line stretching to the fill width) — one of the
  most recognizable generated-template tells. Replaced with a plain 2px
  ink underline sized to the text, echoing the header's own rule instead of
  imitating a landing-page section divider.
- **🏆 emoji** (3 spots: reigning-champs bar, player career rings, playoff
  bracket trophy card) replaced with one inline SVG trophy glyph (`TROPHY`
  constant near `esc()`), sized `1em` so it scales with its context
  (14px in a ring pill, larger in the champbar) and colored via `--gold`
  through `currentColor` — "emoji as section markers" was flagged
  specifically as an AI-design tell; a drawn icon reads as designed rather
  than sprinkled on.

Verified in both themes and at mobile width (375px) before publishing;
no console errors, no functional changes — every edit was to a CSS rule,
a hex value, or a template-string icon swap.

### Follow-up: MLB.com-style pass

User asked for a look closer to MLB.com specifically, one design turn after
the "less vibe-coded" pass above — a different, more specific reference than
"not generic," so the scorebook/ledger direction above got overridden in
favor of MLB's actual brand system: navy, red, white, bold condensed
headlines. Still CSS/markup-only in `generate.py`:

- **Typography**: swapped the slab-serif display face (Zilla Slab) for
  **Oswald** everywhere a heading used it (16 selectors — player names, team
  names, page titles, card headers) — a bold condensed grotesk is the
  actual MLB.com headline treatment; a serif never was.
- **Palette**: `--accent` is now MLB navy (`#041e42` light / a lighter
  `#5b8fd9` in dark so it stays legible on a dark card), `--clay` is MLB red
  (`#d50032` light / `#ff5470` dark), paper shifted to a neutral light gray
  page background (white cards on gray, not gray-on-gray).
- **Masthead**: `header.mast` is now a **fixed navy bar** via new
  `--brandbar`/`--brandbar-ink` tokens that do NOT change with the light/
  dark toggle — real MLB.com's header never changes color, so the site's
  brand chrome now stays constant while the content area below still
  themes. Required one markup change: wrapped the header's contents in a
  new `.mast-inner` div so the navy background can bleed full-width while
  the content stays centered at 1180px. `.tog` (theme button) restyled as
  a white-outlined pill to sit on navy.
- **Nav row**: active tab underline changed from navy to red (`--clay`) —
  matches MLB's red active-tab convention — plus Oswald for the nav labels.
- **Table headers**: every `thead th` site-wide is now a solid navy bar
  with white text and a red bottom border (was a transparent header with
  muted-gray text) — this is the single biggest visual change since the
  site is almost entirely stat tables. Sort-state indicators changed from
  a color swap (`--accent` text, invisible against its own navy background
  now) to an opacity change (dim → full-white on hover/sorted-column).
- **Cards partially un-flattened**: the previous pass had stripped shadows
  from `.split`/`.rec`/`.snapdiv`/`.sparkcard`/`.champyear`/`.asgyear`/
  `.followcard`/`.logohist-item` to fix "everything is a floating card."
  MLB.com actually *does* use elevated white cards on a gray page — so
  `box-shadow:var(--shadow)` came back on all of them, with `border-radius`
  tightened from 8px to 6px (MLB's modules read crisper/less bubbly than a
  12px radius). Same 12–14px → 8px tightening applied to `.tscroll`,
  `.thero`, `.champbar`, `.pb-trophy`, and `.modal`. `.tile` (the dense
  home-page stat chips) deliberately stayed flat — too many small repeated
  atoms in a row for individual elevation to read as anything but noise.
- **`.hsub` section headers** changed again from the plain underline (prior
  pass) to a **left red tab accent** (`border-left:5px solid var(--clay)`)
  with bold condensed navy-colored text — a more recognizably "sports
  media module header" than a plain rule.

Verified both themes + mobile (375px) again before publishing; no
functional changes.

### Champion photo resolution fix

User reported the championship team photos looked blurry. Cause: they'd
been encoded at 700px wide (the original headshot-era convention), and
`.champphoto`'s CSS (`max-height:520px`, no explicit width) displays them
at up to ~780×520 — on any 2x/3x HiDPI screen (basically all current
laptops and phones) that's a 700px source stretched to fill roughly double
its own pixel count, which reads as soft/blurry regardless of JPEG quality.
Re-opened the full-resolution originals in `source/champ_photos/`
(1334×750 up to 5184×3456 — plenty of headroom) and re-encoded all 9 at
**1600px** on the long side, JPEG q82 (up from 700px/q78), replacing
`champs[*].photo` in `players.json` directly. `ImageOps.exif_transpose()`
applied first so any camera-rotated originals (phone photos carry EXIF
orientation flags) come out right-side-up rather than reading the raw
sensor orientation. ~530KB → ~2.9MB total for the 9 photos; page grew from
6.6MB to 9.9MB, still comfortably under the 16MB Artifact cap. No CSS
changes needed — `.champphoto` already scales down via `max-height`, it
just needed source pixels to scale down *from*.

## Playoff round labels (Wild Card / Divisional Series / World Series)

Every postseason game used to carry one generic `"Playoffs"` tag — the
per-game `phase` field in `players.json` has never distinguished rounds,
and never will (that's out of `build.py`'s scope; adding a round column to
the source data isn't worth it when the bracket data already implies it).
User wants the two rounds labeled the way the league actually names them:
the division round was called **Wild Card** every year through 2024, then
renamed **Divisional Series** starting 2025; the final is the **World
Series**, every year.

Rather than hand-label ~50 individual games, `generate.py` derives the
round at render time from data that already exists — `DB.playoffs[year]`
(the same bracket data `playoffBracket()` uses to draw the Brookside/
Brentwood mini-brackets). New `playoffRound(year, teamA, teamB)`: build a
`{teamA, teamB}` set, check whether it exactly matches either division's
two-seed set (`p.brookside.seeds`/`p.brentwood.seeds`, by full franchise
name) — if so it's the division round (`year>=2025 ? 'Divisional Series' :
'Wild Card'`); otherwise it's the two division winners meeting, i.e. the
`'World Series'`. Verified this classifies all 45 recorded playoff games
(2017–2026) correctly with zero fallback misses before wiring it in.

New `gameTag(g)` wraps this and replaces every `phLabel(g.phase)` call
(ticker, home page recent-scores list, Games directory, and the per-team
per-year Game Log): non-Playoffs phases pass through unchanged (still
`phLabel` under the hood for the "AllStar"→"All-Star" rename), Playoffs
games get the derived round name instead. One wrinkle: the per-team Game
Log (`gameLog()`, used on team pages) works from a flattened per-player-
game row that only has `.opp`/`.ha`, not the raw `{away,home}` team
objects `playoffRound` needs — `gameTag` falls back to `GAMES[g.gid]` (the
raw game record) when the row carries a `gid`, which every playoff game
does. Left the ultra-compact single-letter tag in the per-player career
box-score accordion (`g.phase[0]`, i.e. still just "P") alone — "Wild
Card" and "World Series" both start with W, so a single letter can't
disambiguate them anyway, and it's a dense table with no room for the
full word.

**Follow-up**: the Standings page's visual bracket (`playoffBracket()`)
still had its old static labels — "Brookside"/"Brentwood" (division names)
on the two round-1 match cards and "Final" on the championship card — with
no round name anywhere on it, inconsistent with the tags everywhere else
now. Rather than repeat the round name on every match card (redundant: both
round-1 cards are the same round), added one shared heading per round
instead: wrapped each match (or match pair) in a new `.pb-group` — a small
`.pbround` label (`Wild Card`/`Divisional Series`/`World Series`, same
`year>=2025` rule as `playoffRound()`) sits above the Brookside+Brentwood
pair, and another sits above the championship card, whose own `<h5>` title
was dropped (passed `''` to `pbMatch`) since "World Series" directly above
it made "Final" redundant. Division names (Brookside/Brentwood) stayed on
the individual match cards — that's genuinely different information from
the round name, not a duplicate of it. Checked 2026 (Divisional Series),
2020 (Wild Card, and confirms the era-correct "Harris Special K's" name
still renders as champion), and mobile width — bracket still scrolls
horizontally without the new headings cramping it.

## Player page: persistent overview + per-phase tabs

User feedback: the player page was one long scroll (splits → sparks →
accolades → percentile rankings → every phase's stat tables → a single
combined game log at the end). Restructured `detail()`:

- **Always visible, no longer a tab**: the Regular/Postseason split cards,
  OPS/ERA-by-season sparklines, Accolades, and the Percentile Rankings
  card. This is the "who is this player" context — it shouldn't be one
  click away.
- **One tab per phase** below that — Regular Season, Postseason, All-Star
  Games, Spring Training, Fall Ball, NWLA Tournament — using
  `PHASE_META[type].head` for the label so tab names, phase headings, and
  the rest of the site's phase vocabulary stay in sync automatically.
  Regular Season and Postseason always show (Postseason falls back to the
  existing "No postseason games on record" message); the four exhibition
  tabs only appear when `phaseBlock()` actually returns rows for that
  player — a bench player with no All-Star nod just doesn't get that tab.
  New `.subtabs` CSS reuses the main site nav's exact visual language
  (underline + horizontal scroll) so it reads as "the same kind of control"
  without literally being the global nav.
- **Game logs moved into their own phase's tab**, right under that phase's
  stat tables, instead of one combined log mixing every phase together at
  the bottom. `playerGameLog(pl, type)` now takes a phase and filters
  `GAMES` by it; the Postseason log also tags each game with its round
  (Wild Card/Divisional Series/World Series) via the existing `gameTag()`
  helper, which wasn't shown per-game before.
- **NWLA game logs, added as a follow-up**: `playerGameLog` can't cover
  NWLA at all — those games were never in the main `GAMES` dict, only in
  `BV.games` (`DB.beavers`, the separate box-score set `renderBeavers()`
  already uses, keyed by tournament game number with its own `bat`/`pit`
  arrays). New `playerNWLALog(pl)` filters `BV.games` by name match instead
  of `gids`, rendering the same-shaped log table with each game's
  tournament round ("Pool Play"/"Bracket Play") as its tag, plus a link to
  the Beavers page for the full two-sided box score (these games have no
  `#/g/<id>` route since they live outside `GAMES`).

Verified against a player with all 6 tabs (AJ Cefaloni — including 3 real
NWLA games with logs) and one with a narrower set (no Spring/Fall), both
themes, both desktop and mobile widths.

### Follow-ups: year tabs, box-score links, Beavers page overhaul

Three more asks landed on top of the phase-tab work above, same session:

- **Game log years became tabs instead of a `<details>` accordion.** Every
  phase's game log used to stack a collapsed `<details>` per year; both
  `playerGameLog(pl, type, selYear)` and `playerNWLALog(pl, selYear)` now
  take the currently-selected year and render one table plus a `.chips`
  row of year buttons (reusing the same pill component the Leaders/Records
  pages already use) — no new component. New `logYear` state (alongside
  `playerTab`) drives it, reset to `null` whenever the phase tab changes so
  each phase opens on its own latest year rather than carrying over a year
  that might not exist for the new phase. This applies to **every** phase
  tab, not just NWLA — Regular Season, Postseason, All-Star, Spring, Fall
  all converted the same way since they share `playerGameLog`.
- **NWLA dates are now clickable into the actual box score.** These games
  were never clickable at all before (plain text), since `BV.games` isn't
  in the main `GAMES` dict and has no `#/g/<id>` route. Added
  `#/beavers/<gid>` as a real route (`dispatch()` regex + `renderBeavers`
  takes an optional `focusGid`) — each game's `<details id="bvg-<gid>">`
  now has a stable id, and `renderBeavers(focusGid)` opens and scrolls to
  the matching one after render. The player page's NWLA log date is a
  `.pname[data-bv]` button wired to that route, same pattern as the
  existing `[data-g]`/`[data-t]` link wiring.
- **Beavers page redesigned as an overview, like a team page.** Was a bare
  `<div class="phead">` with a text-only meta line. Added a `.thero`
  gradient hero (same component team pages use) with the real Brookside
  Beavers crest and a fixed gold/black color pair (`--tp:#c99a2e`) since
  this team isn't in `FRANCHISE_COLORS` — plus a 3-card `.recgrid` overview
  (Record, Team Batting, Team Pitching) mirroring `teamOneYear()`'s own
  record cards, built from the same `bTot`/`pTot` aggregates the page
  already computed for the season stat tables. Two crests were provided —
  `BeaversLogo.png` (the circular mascot mark, used as `BV.logo` in the
  hero) and `BeaversLogo2.png` (a script "B" wordmark, stored as
  `BV.logo2` but not placed anywhere yet — no natural second spot on this
  page). Both resized to 340px PNG, archived to `source/beavers/`.

Verified: clicking a Regular Season date still opens `#/g/<id>` as before;
clicking an NWLA date opens `#/beavers/<gid>` with exactly that game's box
score expanded and scrolled into view; plain `#/beavers` still opens with
nothing pre-expanded; every phase tab (Regular/Postseason/All-Star/NWLA)
shows its own correct year chips.

## Scroll-to-top fixed for in-page toggles

Bug: clicking almost any in-page control — a player's phase tab, a year
chip on Standings/Leaders/Team/Records, a phase toggle — jumped the page
back to the top. Root cause: 9 render functions (`detail`, `teamDetail`,
`renderStandings`, `renderLeaders`, `renderRecords`, `renderHome`,
`boxScore`, `renderChampsPage`, `renderAwards`) each ended with their own
unconditional `scrollTo(0,0)`. That's correct for real navigation (arriving
at a new page should start at the top) but every one of these functions is
*also* called directly by its own in-page toggles (e.g. `playerTab='...';
detail(name)`) — which don't touch `location.hash` at all, so the
resulting scroll-to-top had nothing to do with navigating anywhere.

Fix: deleted all 9 individual `scrollTo(0,0)` calls and moved a single one
into `route()` — the function that runs *only* on an actual `hashchange`
event. In-page toggles call their render function directly and never fire
`hashchange`, so they no longer reach it; clicking a player link, a team
link, or a nav tab still does (it sets `location.hash`), so real
navigation still opens at the top, now consistently across every page
(a few pages — Teams, Games, Players directory, Beavers — never had a
scroll reset before this and now do too, for free). One guard added:
skip the scroll when the hash still carries an in-page `#h-anchor` suffix
(the Awards page's own subnav), so a direct deep-link to `#/awards#h-awards`
doesn't fight the browser's native anchor scroll — though in practice
that subnav already prevents the hash from changing at all (its click
handler calls `preventDefault()` and does its own `scrollIntoView`), so
this guard only matters for someone typing such a URL in by hand.

Verified: clicking a phase tab, a year chip (Team/Standings/Leaders), and
a segmented toggle all now hold scroll position; navigating to a different
player/team/page still resets to the top.

## Franchise Name History timeline (Teams page)

User provided a full 2012–2026 nickname-by-year spreadsheet for all 20
franchises (a proper "team timeline" — every name a franchise has ever
played under, not just what's in the stat database) plus a Location/Team
list pairing each franchise with its home-town prefix. Neither on its own
was enough: the spreadsheet only had bare nicknames per year (no location),
the Location list only had one representative nickname per franchise (not
the year-by-year history), and — critically — **`TEAMS[*].nameByYear`
already in `players.json` only covers 2017 on** (the stat-database era),
so the pre-2017 nickname history the user wanted shown didn't exist
anywhere on the site yet.

Built a new, self-contained dataset instead of trying to merge into
`nameByYear` (which other features already depend on and I didn't want to
risk breaking): `FRANCHISE_TIMELINE` in `generate.py`, one entry per
franchise with `eras: [{from, to, name}]` — full location+nickname
strings, hand-transcribed from the spreadsheet, collapsing consecutive
years under one name into a single era (e.g. Kraken: 2012 Capitals →
2013–2016 Eagles → 2017 Bluefish → 2018–2026 Kraken). New
`franchiseTimeline()` renders it as a bordered list at the very top of the
Teams page, one row per franchise (sorted oldest-founded first): crest
icon + current full name (linked for live franchises, plain text for
defunct ones, same pattern as the Franchise Summary table below it) on the
left, the era sequence on the right with a `→` between consecutive eras
and a red `⋯` where the franchise went inactive for a stretch (Kings
2022–2025, Shock 2025, Braves 2018–2023) rather than implying continuity
that isn't there.

Two location conflicts surfaced between the user's fresh data and the
already-hardcoded `FRANCHISE_SUMMARY` table: **Angels** was listed as
"Downtown" there but "Parsons" in the new data — fixed `FRANCHISE_SUMMARY`
to match (`Downtown Angels` → `Parsons Angels`) since nothing else on the
site depends on that string. **Braves/Dashers** was trickier: the new data
says the 2016–2017 "Dashers" era was based in *Avondale*, not *Brentwood*
— but "Brentwood Braves" is the live, current TEAMS key referenced
everywhere (roster pages, box scores, standings). Rather than relocate the
whole franchise, stored that one era as a literal override string
(`'Avondale Dashers'`) instead of building it from the franchise's current
`Brentwood` prefix — the same pattern the codebase already uses for
`AWARD_TEAM_ALIAS`'s `'Avondale Dashers'` entry. **Diablos** shows as
"Gleason Devils" in the timeline specifically (matching the fresh data and
the actual logo art, which reads "Devils") while keeping `Gleason Diablos`
as the canonical key everywhere else — the same intentional dual-naming
already established earlier this session for that franchise.

Verified: all 20 rows render with correct eras and gap markers; franchise
links navigate to the right team page; defunct franchises show their
`franchiseLogos` icon where the summary table also does; both themes and
mobile (rows stack name-above-eras under 600px) checked.

### Follow-up: rebuilt as an actual Gantt-style grid

The row-of-chips version above wasn't what "an actual timeline like the
excel" meant — the user wanted the spreadsheet's own shape: franchises as
rows, years as aligned columns, name-eras as colored bars spanning their
real year range, so you can see at a glance which franchises overlapped
and which years a franchise didn't exist. Rebuilt `franchiseTimeline()` as
a genuine CSS Grid (`.tlg-grid`, 180px name column + 15 year columns,
`grid-auto-rows`), every cell explicitly placed with `grid-row`/
`grid-column` — year Y maps to column `(Y-2012)+2`, an era spanning
`from`–`to` gets `grid-column: colOf(from) / colOf(to)+1`. `FRANCHISE_TIMELINE`
entries changed from a single `name` string per era to `{loc, nick}` so
the bar can show the short nickname (fits a ~60px column) while the
`title` tooltip and hover give the full `loc + nick`. Bars are colored via
the existing `teamAccent()` helper (same club-color system team pages
already use) so a franchise's color stays visually consistent across its
different name eras — added `Parsons Angels` to `FRANCHISE_COLORS` (was
keyed as `Downtown Angels`, now stale after the location fix above) so it
still resolves. Years with no bar are simply blank in that franchise's
row — a clearer, more honest "inactive" signal than the arrow/gap-glyph
version had. The name column uses `position:sticky;left:0` so it stays
readable while scrolling the year columns horizontally, which is also how
the whole thing degrades on mobile (native horizontal scroll on a
`min-width:900px` grid rather than any layout collapse).

Verified: bars land in the correct year columns for spot-checked
franchises (Kraken, Kings, Braves, Shock all show accurate eras and gaps);
sticky name column holds in place while horizontally scrolling at both a
mid-width and true mobile viewport; franchise links still navigate; both
themes checked.

## Postseason toggle for Standings team stats

Team Batting/Team Pitching on the Standings page were regular-season only,
hardcoded to `roster.filter(e=>e.regular)`. Added a `standPhase` state
(new module-level var, `'reg'`|`'post'`, mirrors the same idea as the team
page's `teamPhase` but kept separate so toggling one doesn't affect the
other) and a `.segs.post` Regular/Playoffs toggle above the two tables —
same reusable component the team page's `phaseToggleHTML()` already uses,
just wired to its own `data-sp` attribute and state instead of sharing
`teamPhase`. The aggregation swapped `e.regular` for `e[phKey]`
(`phKey = standPhase==='post' ? 'playoffs' : 'regular'`), same pattern
`teamOneYear()` already uses for the team page's own toggle. Table titles
now read "Team Batting · 2026 · Postseason" so it's unambiguous which
phase is showing.

Follow-up: the first version left non-playoff teams in the Postseason
view as zeroed-out rows. Changed `agg`'s `.map()` to also tag each row
`made:ph.length>0`, then `.filter(a=> standPhase==='reg' || a.made)` so
the Playoffs table only lists teams that actually made the postseason
that year (Regular view is untouched — every team still shows). The
League total row recomputes from the filtered set, so it now reflects
just the playoff field instead of the whole league.

Verified: toggling Playoffs on 2026 drops the table from 6 teams to the
4 that made the playoffs (Brookside Kraken, Shelton Shock, Brookside
Panthers, Brentwood Gladiators), with real playoff-only totals and
correct titles; Regular still lists all 6; mobile and desktop checked.

## Postseason toggle for League Leaders

League Leaders was regular-season only (`P[n].seasons.find(x=>...&&
x.type==='Regular')` for a single year, `P[n].careerReg` for career).
Added a `leadPhase` state (`'reg'`|`'post'`) and the same `.segs.post`
toggle component, wired to `data-lp`. The season lookup now filters on
`x.type===(isPost?'Playoffs':'Regular')`, and career mode swaps in
`P[n].careerPO` (already computed per-player, same field `savantCard`
uses) instead of `careerReg`.

Postseason sample sizes are much smaller than a full regular season —
league max single-season playoff games is 6, career playoff PA tops
out around 140 — so the regular season's qualifying minimums (9 games,
150 AB/PA, 36/180 outs pitched) would leave every postseason list
empty or nearly so. First pass added separate, lower thresholds for
`isPost` (3 games / 25 AB/PA / 9–21 outs); user follow-up asked for no
qualification at all on postseason, so `minAB`/`minPA`/`minG`/`minO`
are now just `0` when `isPost` — every player with any postseason
plate appearance or out recorded is eligible (the existing `x.v!==0`
filter in `cat()` still drops entries with a literal zero in that
stat, e.g. 0 HR). Regular season's minimums are untouched. Footnote
swaps to "No minimum AB/PA/IP — small postseason samples all qualify."
when `isPost`, instead of stating a threshold.

Verified: Playoffs toggle on a single year and on Career both swap in
real, distinct postseason leaders (e.g. career Playoffs batting-average
leader vs. career Regular leader are different players with different
averages); every batting/most pitching categories now fill a full top
10 with no minimum; Regular season note/thresholds unchanged; toggling
doesn't jump scroll position; no console errors.

## Player splits (Home/Away, By Field, vs Each Team)

Added a Splits section to each phase tab on the player page, sitting
between `phaseBlock()`'s season-by-season tables and the (year-scoped)
game log — same position for every phase (Regular, Playoffs, All-Star,
Spring, Fall, NWLA), built fresh each time from that phase's raw
per-game bat/pit lines rather than the season roster totals, since
those totals don't carry home/away, field or opponent information.

New shared plumbing:
- `collectPlayerGames(pl, type)` — factored out of `playerGameLog()`
  (which used to inline this loop over `pl.gids`/`GAMES`) so both the
  game log and the new splits read from one place. `playerGameLog()`
  now just groups this list by year instead of building it itself;
  behavior is unchanged.
- `gameBatRow()`/`gamePitRow()` — reshape one raw box-score line
  (`{ab,h,hr,2b,3b,...}`, `{ip,h,er,...}`) into the ZERO_KEYS field
  names (`AB`,`H`,`HR`,`TB`,`IPouts`,`ER`,...) that `sumRows()`/
  `avg()`/`era()`/etc. already expect everywhere else in the file, so
  the split tables reuse the exact same stat-line helpers as every
  other table on the site instead of a one-off formula.
- `splitGroup(games, keyFn, labelFn)` — buckets a game list by an
  arbitrary key (side, field, opponent) and sums each bucket to one
  stat line; `splitDim(title, rows)` renders one dimension as a
  Batting `statTable` plus a Pitching one (only if the total has any
  innings pitched, same `career.IPouts>0` gate `phaseBlock` uses) under
  a `<h4 class="divh">` heading — reusing the same heading style as the
  Standings division headers rather than inventing a new one.
- `playerSplits(pl, type)` covers the three dimensions for every
  GAMES-backed phase; `playerNWLASplits(pl)` covers just Home/Away and
  vs Each Team for the Beavers' NWLA tab, since `BV.games` (a
  differently-shaped dataset — see the NWLA/Beavers section above)
  tracks `ha`/`opp` but never a field/venue.
- Team names in "vs Each Team" go through the existing `teamLink()`
  helper, so they render as working links to the team page — same as
  every other opponent reference on the site — and non-franchise
  opponents (division names in All-Star games, NWLA tournament teams)
  fall back to plain text automatically since `teamLink()` already
  handles a name that isn't a `TEAMS` key.

One real gotcha: per-game lines only exist from 2020 on (same
limitation the game log already notes), so a career total built from
splits can come in lower than the career total shown in the overview
card above it, which pools every year including the pre-2020,
season-only ones. Added a `pmeta` line under the Splits heading calling
this out explicitly rather than let the numbers look inconsistent with
no explanation.

Verified: on Parker Gibbons (a two-way player), Home vs Away, By Field
and vs Each Team all render on Regular and Playoffs with matching
Total-row footers across the Batting and Pitching tables; a batting-only
player (Dustin Lee) correctly gets no Pitching sub-table in any
dimension; NWLA renders only two dimensions (no By Field); "vs Each
Team" team-name links work; mobile width renders cleanly with each
table scrolling in its own container; no console errors across several
players and every phase tab.

## Year toggle for player splits

Follow-up to the splits section above: it always pooled every year for
a phase, with no way to isolate one season. Added a `splitYear` state
(`'all'` by default, or a specific year string) plus a second,
independent year-chip row (`splitYearChips()`, reusing the same
`.chips.logchips` look the game log's own year picker already uses) —
independent because the two serve different purposes: the game log
always pins to one year with no "All" option, while splits default to
every year pooled (bigger samples, especially for "vs Each Team") and
can be narrowed down on request. `playerSplits()`/`playerNWLASplits()`
now take a `selYear` param, compute the full year list first, then
filter `collectPlayerGames()`'s output to that year before bucketing —
same shape as before, just fed a smaller game list. Switching phase
tabs resets `splitYear` back to `'all'` (same spot `logYear` already
gets reset to `null`), since a year that's valid on the Regular tab
won't line up with Playoffs/NWLA's own years. The chip row hides
itself when a phase only has one year on record, matching the game
log's own chip row exactly.

Verified on Parker Gibbons: the "All" chip matches the previous
career-pooled numbers exactly; picking 2026 drops Home/Away down to
that year's much smaller per-game counts; switching to the Playoffs
tab resets the chip row back to "All" independently of the game log's
own (unrelated) year selection below it; no console errors.

## Sortable splits tables

The splits tables (Home/Away, By Field, vs Each Team) had rows in
whatever order `splitGroup()` bucketed and sorted them by usage —
fine as a default, but every other multi-row leaderboard-style table
on the site (team rosters, the all-time team tables) lets you click a
header to re-sort via the existing `makeSortable()`. Added the same to
splits: `splitDim()`'s two `statTable()` calls now pass `sortable=true`
so each gets `class="detail sortable"`.

One wrinkle `makeSortable` doesn't hit anywhere else: split tables can
re-render from a direct function call (a phase-tab click, a split-year
chip click) that never goes through `route()` — and `route()` is the
only place that currently re-runs `document.querySelectorAll('table.
sortable').forEach(makeSortable)` after a render. Without it, a table
built by a second, direct call to `detail()` would carry the
`sortable` class but no click handler. `renderTeams()` already hits
this same issue for its own reason (a search-input re-render) and
already re-calls `makeSortable` at its own end — followed the same
fix here: `detail()` now also calls
`app.querySelectorAll('table.sortable').forEach(makeSortable)` as its
last line, so every path that can render the player page (initial
navigation via `route()`, or a direct `detail(name)` call from a tab/
year click) leaves sortable tables properly wired. `makeSortable`'s
existing `sortWired` guard makes the occasional double-call (`route()`
then `detail()`'s own line, on initial navigation) harmless.

Verified: clicking HR on a "vs Each Team" batting table sorts
descending then ascending correctly; switching phase tabs and clicking
a header on the freshly-rendered table sorts immediately (no dead
click from a missing handler); picking a split-year chip and sorting
afterward also works; the season-by-season tables above (from
`phaseBlock()`) are intentionally untouched and remain non-sortable,
matching their pre-existing behavior; no console errors.

## Duplicate-player merge: Bob/Brandon Gibbons, Trevor "Garfield"/Trevor Meyler

Same class of bug as the earlier Tom/Tommy Giandomenico merge: two
`players.json` entries for one real person, split by a name variant in
the source data across different years. User identified two pairs:

- **Bob Gibbons** (2017-19, Beaver Brook Lavahogs) and **Brandon
  Gibbons** (2020-26, mostly Brentwood Gladiators) — non-overlapping
  years, i.e. a name that changed over time. Kept **Brandon Gibbons**
  (has the headshot, and his `honors` already carried awards back to
  2012-2019 under that name, confirming the two were always meant to
  be one continuous record).
- **Trevor "Garfield" Meyler** (one 2021 Spring Training season,
  Brookside Panthers) and **Trevor Meyler** (2019-2026, everything
  else) — the nickname stood in for the surname on a single season's
  import. Kept **Trevor Meyler**.

Wrote a one-off merge script (not checked in — scratchpad only) rather
than hand-editing the JSON, since a name merge touches several places
that all have to move together:
- `players[old]` deleted; its `seasons` concatenated into `players[new]`
  (checked first that neither pair had a year+type collision — they
  didn't); `years`/`gids` unioned; `career`/`careerReg`/`careerPO`
  summed key-by-key; `teamsByYear` merged (both pairs' overlapping
  years, where any, already agreed on the same team, so no real
  conflict); `firstDate`/`lastDate` took the min/max; `photo` kept
  whichever side had one.
- `honors` merged **with dedup** — this was the one real gotcha.
  Trevor's two records both carried a 2021 Brookside Panthers rings
  entry (the ring is presumably keyed to the team/year in the source
  data regardless of which name variant that season used), so a naive
  concatenation would have shown two 2021 championships instead of
  one. Deduped rings by `(year, team)`, awards by `(year, award)`, asg
  appearances by `year`.
- Renamed every `games[*][home|away][bat|pit][].n` box-score line
  (104 for Gibbons, 5 for Meyler) and every `beavers.games[].{bat,pit}`
  NWLA line (0 for both — neither played NWLA under the old name).
- `TEAMS[*].seasons[*].roster` needed two different fixes depending on
  whether the old and new name already had *separate* roster rows for
  the same team+year: Gibbons' 3 old-name rows (2017-19, no year
  overlap with Brandon) just got renamed in place. Meyler's case did
  collide — Brookside Panthers' 2021 roster already had both a
  "Trevor Meyler" row (real regular/playoffs stats, from his other
  2021 game types) and a "Trevor 'Garfield' Meyler" row (empty — Spring
  Training isn't tracked in the roster's regular/playoffs sub-fields,
  so that row carried no stats at all). Renaming both in place would
  have left two "Trevor Meyler" rows on that one team-season table, so
  that pair's old row was merged into the new one (summed any
  `regular`/`playoffs` sub-fields, since both existed for the empty row
  it was a no-op) and dropped instead of renamed.
- Added `'Bob Gibbons':'Brandon Gibbons'` and `'Trevor "Garfield"
  Meyler':'Trevor Meyler'` to build.py's `ALIAS` map (also repointed
  the existing `'BOB'`/`'BOB Gibbons'` typo-aliases straight at
  Brandon), so a from-scratch rebuild merges the `players` dict and
  `TEAMS` roster automatically too — matching the existing Dan Brady/
  AJ Cefaloni/Tom Giandomenico entries there. Note this still won't
  auto-fix `games` box-score names on a rebuild: `box_bat()`/`box_pit()`
  read `PlayerName` from a separate raw CSV parse that never passes
  through `ALIAS` (a pre-existing gap — none of the other aliases fix
  box scores on rebuild either), so that half of a future merge like
  this one would still need the same manual/scripted treatment.

Verified: `Bob Gibbons`/`Trevor "Garfield" Meyler` no longer exist as
player keys (`#/p/Bob%20Gibbons` redirects home, matching `detail()`'s
existing not-found handling); Brandon Gibbons' page shows 9 seasons
spanning 2017-2026 with combined career/postseason lines and both
Regular-tab year ranges; Trevor Meyler shows exactly one 2021 ring (no
double-count) and picked up a Spring Training tab; the Beaver Brook
Lavahogs/Brookside Panthers team pages and a Bob-Gibbons-era box score
all render the merged name with no leftover references anywhere
(players list, records, leaders, awards); no console errors.

## Team logos on League Leaders

Each leader-list row already showed the team name/nickname under the
player's name (`teamOf(x)` in `renderLeaders()`); added the era-accurate
logo next to it, reusing `teamLogoForYear()` — the same helper the
Standings and Team Timeline logos already use, so the crest matches
whichever name/era that season actually used.

`teamOf()` used to return a plain display string; changed it to return
`{label, logo}` so the same function that resolves the display text
also resolves the matching logo in one place, instead of a second
lookup at render time. Three cases:
- Single-team season/career: `TEAMS[team] ? histName(team, yr) :
  team` for the label (unchanged), `teamLogoForYear(team, yr)` for the
  logo.
- Split season (player played for two clubs that year): label already
  abbreviated to `"NickA/NickB"` to fit the narrow card; logo just
  shows the *first* club's mark — two logos won't fit next to a name
  in a ~230px-wide list card, and the abbreviated team text next to it
  still spells out both.
- No team on file: `{label:'', logo:null}` — `llist()` already
  skips rendering the `.lt` team-text span when empty, and now
  likewise skips the `<img>` when `logo` is falsy.

`llist()` renders the `<img class="llogo">` first, ahead of the name/
team `<span class="ln">`, sized 20×20px (`.llogo` — small enough for
the compact card, matching the general sizing of the site's other
inline logo treatments like `.stlogo`).

Verified across Regular/Playoffs, every year and Career, batting and
pitching categories: every row gets the right era-accurate crest;
split-season rows (checked 2018, 2019, 2022, 2025) show the first
team's logo without errors; mobile width renders cleanly with full
names now readable in the single-column layout; no console errors.

## Bigger leader-list logos, no name truncation, logos + box-score links on Records

Follow-up to the Leaders logos: user asked to make them bigger, stop
cutting off names, and extend logos to the Records page too — plus a
mid-turn ask for dates/box-score links on Single-Game Records, and a
second mid-turn ask to show *both* team logos for a leader who split a
season between two clubs.

- **Bigger + no truncation**: `.llogo` 20px → 30px. `.llist button.
  pname` and `.llist .lt` both dropped `white-space:nowrap;overflow:
  hidden;text-overflow:ellipsis` in favor of `white-space:normal;
  word-break:break-word` — names now wrap instead of getting clipped.
  `.llgrid`'s card minimum width also went 230px → 260px, so most
  names still fit on one line at typical widths and only wrap when
  they'd genuinely overflow a card.
- **Two logos for a split season**: `teamOf()` in `renderLeaders()`
  returns `logo2` alongside `logo` now — the second club's era-accurate
  mark for a player who played for two teams in the same year (the
  `"NickA/NickB"` label already showed both abbreviated names; now both
  crests show too). `llist()` renders `it.logo2` right after `it.logo`
  when present.
- **Records page logos**: same `teamLogoForYear()` reuse as Leaders.
  `catS()` (single-season records) resolves the season's own team +
  year via a new `sLogo(x)` helper — a multi-team combined ("2TM") row
  correctly shows no logo, same as it shows no single team name today.
  `catG()` (single-game records) needed the player's own team threaded
  through: `batPool`/`pitPool` push calls now also carry `team:s.team`
  (previously only the *opponent* was tracked, for the "vs Opponent"
  text), and a new `gLogo(x)` resolves it.
- **Dates + box-score links on Single-Game Records**: `gSub(x)` used
  to show just `"2018 · vs Kings"` — swapped the bare year for the
  actual `GAMES[gid].date`, wrapped in the same `.pname[data-g]` box
  score link every other date-as-link uses elsewhere on the site (the
  click wiring in `renderRecords()` already existed, since dates
  already linked in the no-hitter table). Since the `.llist button.
  pname` rule forces `display:block` (so a *player-name* button gets
  its own line above the team text), a date button re-using the same
  `.pname` class inside `.lt` needed its own override —
  `.llist .lt button.pname{display:inline}` — so it flows inline with
  " · vs Team" instead of forcing a line break.
- **Underlying refactor**: `llist()` used to `esc()` the `tm` field
  itself, which only worked because every caller passed plain text.
  Embedding a `<button>` for the date meant `tm` had to become
  caller-escaped HTML instead — `llist()` no longer escapes it, and
  all three producers (`renderLeaders()`'s `teamOf`, and Records'
  `ySub`/`gSub`) now `esc()` their own dynamic text before handing it
  over. Worth remembering if a fourth `llist()` caller gets added later:
  its `tm` must come pre-escaped.

Verified: Leaders logos visibly bigger, zero overflowing name buttons
at 2026/regular season (checked via `scrollWidth>clientWidth`); a 2018
split-season row (AJ Cefaloni, Mustangs/Kraken) shows both logos on
desktop and mobile; Records' single-season and single-game lists both
show correct era logos, with the "2TM" combined row correctly logo-less;
clicking a Single-Game Records date navigates to the right box score;
the date link renders inline, not on its own line; no console errors
across Leaders/Records/Players/Standings/Teams.

## Second team logo on Records' single-season "2TM" rows

Follow-up to the Leaders two-logo fix: Records' single-season list
(`catS()`) combines a multi-team season into one "2TM" row with
`team:null` (build.py's own combined-total row), so there was no
single team to look up a logo for. Added `splitTeamsOf(x)`, which
recovers the two clubs from that player's own *other* season rows for
the same year/type — the individual `split:true` rows build.py already
writes alongside the "tot" row, each with its own single `team`.
`sLogo(x)` now returns `{logo, logo2}`: a normal single-team row uses
`x.s.team` as before with `logo2:null`; a "2TM" row looks up both
split rows' teams instead. Order matches whatever order `build.py`'s
`sorted(clubs)` produced (alphabetical) — good enough since nothing
else in Records depends on a specific left/right order for this case,
unlike Leaders' "NickA/NickB" label which is sourced from a different
field (`teamsByYear`, ordered by game count).

Verified: the AJ Cefaloni 2018 "2TM" batting-average row shows both
the Mustangs and Kraken logos.

## Era-accurate team names on box scores, game logs, and Records

User asked for box scores to use the year-specific team name instead
of the current one, "kept consistent across pages... e.g. records" —
this was visibly wrong in several places at once: the home ticker and
`boxScore()` both showed `TEAMS[tm].nick`/`g.away.team` (today's name)
for a 2017 game that a division-realignment/rename had since renamed,
while `playoffBracket()` on Standings already did this correctly via
`histName()` (added in an earlier session). Generalized that existing
pattern instead of inventing a new one:

- Added `histNick(full, y)` next to the existing `histName(full, y)` —
  same idea (look up `TEAMS[full].nameByYear[y]`, fall back to the
  current name) but returns the bare nickname with no location prefix,
  for narrow contexts that already showed just a nickname.
- Added `histTeamLink(full, y)` / `histNickLink(full, y)` — the
  clickable-button version of each: display text is era-accurate, but
  `data-t` stays the *current* franchise key, so the link still opens
  the live team page. Same split `teamLink()`/`histName()` combo
  Standings' `nk()` helper and the Team Timeline already used ad hoc;
  now it's a named, reusable pair.
- Swapped in across every place that ties a team name to one specific
  year: `boxScore()`'s header (now also clickable, since the existing
  `.pname[data-t]` wiring on that page wasn't limited to the line
  score), `lineScore()`, `boxSide()`'s table titles (needed `yr`
  threaded through as a new param), `renderGames()`'s Away/Home
  columns, the home-page ticker (`buildTicker()`), Records'
  single-season and single-game team text (`ySub`/`gSub`), the
  no-hitters table (team + opponent), a player's Game Log opponent
  column, and a player's World Series ring nicknames in `accolades()`
  (removed the local `tnk()` helper there — folded into the two new
  no-hitter and ring call sites via the shared helpers instead).
- Underlying refactor: `llist()`'s `it.tm` field had already become
  caller-escaped raw HTML (from the Single-Game Records date-link
  work); Records' `ySub`/`gSub` needed adjusting again here since they
  now build era-accurate text with their own `esc()` calls per piece
  rather than escaping the whole template at once.

One limitation carried over rather than fixed: `TEAMS[*].nameByYear`
only has entries from 2017 on (an existing, pre-2017-per-game-data gap
noted elsewhere in this file), so a name shown for 2012–2016 still
falls back to the current name — same behavior `playoffBracket()`
already had, not a regression.

Verified: the Games list filtered to 2017 shows "Brookside Bluefish"
(that franchise's actual 2017 name) instead of "Brookside Kraken";
opening that game's box score shows the same era name in the header
(now clickable), line score, and box-score table titles, all still
linking to the live Brookside Kraken team page; Records' single-season
list shows "2017 · Bluefish" instead of "2017 · Kraken"; a player's
Game Log opponent column for a 2017 game against that franchise shows
"Brookside Bluefish"; no console errors across Home/Players/Teams/
Standings/Leaders/Records/Games/Champs/Awards/Beavers.

## Playoff bracket on the home page, stat tiles removed

Replaced the "Seasons/Players/Franchises/Games/Home runs/Runs scored"
tile row on the home page with the most recent year's playoff bracket
— reuses `playoffBracket(year)` verbatim (the same function Standings
already uses under its own "20XX Playoffs" heading), just called from
`renderHome()` with the latest year found in `ALL_YEARS.filter(y=>
PLAYOFFS[String(y)])`, mirroring the existing `snapYears`/`snapY`
pattern already used right below it for the standings snapshot. Placed
between the champion banner and the standings snapshot — champion →
how they got there → current-season standings reads as a natural
sequence down the page.

Deleted the now-unused `tiles` array and the `HR`/`R` career-total
accumulation that only fed it, plus the dead `.tiles`/`.tile`/`.tk`/
`.tv` CSS rules (nothing else referenced them). `playoffBracket()`'s
own team links (`.pname[data-t]`) work with no extra wiring — they're
covered by the same generic `.pname[data-t]` listener `renderHome()`
already attached at the end of the function for the champion banner
and standings-snapshot links.

Verified: home page now shows "2026 Playoffs" (Divisional Series →
World Series → Champion, logos included) right above "2026 Standings";
clicking a bracket team link navigates to that team's page; mobile
width renders cleanly (the bracket's own horizontal-scroll wrapper
handles the narrow viewport, same as it already does on Standings); no
console errors.

## Team Accolades on team pages

Added a "Team Accolades" section to `teamDetail()` — right after the
hero header, before Logo History — with three counts, each derived
fresh from existing league data rather than a new hand-kept field:

- **World Series**: years where `PLAYOFFS[y].championFull` equals this
  team's live key.
- **Division Titles**: years this team's entry in `DB.divisions[y]`
  carries the `'^'` marker — the same raw marker Standings already
  reads to render the superscript "z" division-winner badge (learned
  the hard way: first pass checked for `'z'` itself, since that's what
  Standings *displays*, not what the data actually stores — `'^'` is
  the real marker, `'z'`/`'x'` are just the on-screen labels for
  `'^'`/`'*'`).
- **Division Pennants**: years this team won its side's bracket
  (Brookside or Brentwood) and reached the World Series, whether or
  not they went on to win it — checked via `PLAYOFFS[y][side].seeds`
  (matched by the seed's `full` key, not its nickname, so an era name
  change doesn't miss a year) against `PLAYOFFS[y][side].winner`.

All three match by the *live* franchise key, so a franchise's history
stays unified across a name change (e.g. a division title as "Brookside
Bluefish" in 2017 still counts toward Brookside Kraken's total) — same
principle as every other franchise-unification feature already in the
file. A team with none of the three shows no section at all (checked
against `Brentwood Mustangs`, `Downtown Titans`, `Purchase Dragons`,
`Purchase PawSox`, `Silver Lake Snapping Turtles`, `Shraken`).

Verified: Brookside Panthers shows 5× World Series (2014/16/17/21/25),
7× Division Titles, 8× Division Pennants, with the World Series years
correctly a subset of the Division Pennant years for every team
checked (winning the title requires winning the pennant first — a
built-in sanity check); Harris Kings shows 2 World Series wins with 0
Division Titles, a legitimate case (won their side's bracket without
having led their division that regular season) rather than a bug;
mobile width renders cleanly; no console errors across every team in
`TEAMNAMES`.

## Visual trophy case for Team Accolades

Follow-up to Team Accolades: replaced the plain year lists with actual
graphics — gold trophy medallions for World Series, downward-pointing
pennant flags (in the team's own color) for Division Titles and
Division Pennants, all in a fixed 3-column grid per category.

- `.acc-trophy`: a 50px circle, radial gold gradient (mixing the
  theme's existing `--gold` token, not a new hardcoded color, so it
  still adapts between light/dark) plus an inset highlight and drop
  shadow for a medallion look, the 🏆 emoji centered inside, year below
  in mono type.
- `.acc-pennant`: a solid shape via `clip-path: polygon(0 0,100% 0,
  100% 55%,50% 100%,0 55%)` — a rectangle that tapers to a single
  point at the bottom, i.e. a pennant hanging down rather than flying
  sideways. Colored with `var(--tc, var(--accent))` — the same
  team-accent CSS variable `setTeamVars()` already sets for every other
  team-colored element on the page — so it automatically matches
  whichever team page it's on with no per-team logic needed. Division
  Titles and Division Pennants use the identical pennant shape/color;
  they're already distinguished by their separate `<h4>` headers.
- `.acc-grid3`: `grid-template-columns:repeat(3,78px)` — a fixed
  3-column layout (not auto-fill) so a team with, say, 8 pennants wraps
  3/3/2 rather than spreading thin across the full page width.
- `teamAccolades()`'s year-list logic (`wsYears`/`pennantYears`/
  `divYears`) is unchanged from the previous pass — only the rendering
  changed, from a plain `<p class="acc-years">` string to a
  `trophies()`/`pennants()` template per category.

Verified: Brookside Panthers' 5 World Series trophies and 8 red
pennants render correctly; Brookside Kraken's pennants render in that
team's magenta/pink accent instead, confirming the color follows
`--tc` per team automatically; 3-column wrapping looks right at both
5 and 8 items; mobile width unaffected (fixed-width grid cells don't
need to reflow); no console errors.

## Team Accolades follow-up: real trophy shape, distinguishable pennants, wider grid, reorder

Four fixes to the trophy-case redesign, the last two only surfacing
once real screenshots were compared against the reference the user
attached:

- **Section order**: `teamLogoHistory(t)` now renders before
  `teamAccolades(name)` instead of after — the team's logo-era history
  sits right under the hero header, accolades below that.
- **A real three-column trophy**: the user attached a photo of an
  actual trophy — star on top, a tapering neck, a disc resting on
  three gold columns around a center medallion, a base with a
  nameplate — and pointed out that's what "three-column trophy" meant
  last time, not a 3-column CSS grid (my misreading). Replaced the
  gold-medallion-with-🏆-emoji with a purpose-built inline SVG
  (`TROPHY3`, local to `teamAccolades()`) tracing that exact shape:
  a star polygon, a triangular neck, an ellipse rim, three gold
  `<rect>` columns, a stroked circle medallion, a base rect and a
   nameplate rect — gold pieces use `var(--gold)` (the existing themed
  token, not a new hardcoded color) so it still adapts with the
  light/dark theme; the dark tiers/base use a fixed bronze-black
  (`#2a1c0c`) since those are meant to read as a physical material
  regardless of theme, matching how the reference photo's trophy looks
  the same in any room. Left the plain-cup `TROPHY` SVG (used inline in
  running text elsewhere — champbar, player rings, playoff bracket)
  untouched; this is a separate, decorative-only icon.
- **Division Titles vs. Division Pennants now read apart at a glance**:
  both were identical pennants in the same flat team-accent color.
  Titles kept that flat single-tone fill; Pennants switched to a
  two-tone gradient using the franchise's own `--tp`/`--ts` colors
  (the same pair `setTeamVars()` already sets for the hero/champbar
  treatment elsewhere — falls back to the flat accent if a team has no
  `FRANCHISE_COLORS` entry) plus a small gold ★ above the year. The
  reasoning: Pennants (reached the World Series) are the bigger
  accomplishment, so they get the richer two-tone treatment already
  reserved elsewhere on the site for championship-adjacent moments.
- **Grid was too narrow on desktop**: `.acc-grid3`'s fixed
  `repeat(3,78px)` — a leftover from originally misreading "three
  column trophy" as a layout instruction — left a wide page mostly
  empty for a team with only 5-8 accolades. Renamed to `.acc-grid` and
  changed to `repeat(auto-fill,76px)`: same fixed 76px tile size, but
  now as many columns as the container width allows (10 on a full
  desktop width, still wrapping sensibly to fewer on mobile) instead
  of being artificially capped at 3.

Verified: Brookside Panthers' World Series row now shows five
recognizable star-topped, three-column trophies instead of gold
circles; its Division Titles pennants are solid red while Division
Pennants are black-to-red two-tone with a gold star, clearly distinct
side by side; the grid fills 10 columns at desktop width and wraps
cleanly on mobile (5/7/7+1); Logo History renders above Team Accolades
on the page; no console errors.

## Wiffleball finial on trophies, division logos on pennants

Two more additions to the trophy case:

- **Wiffleball finial**: added a small perforated ball (a cream circle
  plus five small dot "holes" suggesting the real ball's pattern) above
  the star on `TROPHY3`. Rather than compressing the existing shape,
  shifted every other element (star, neck, rim, columns, medallion,
  base, nameplate) down by 16 SVG units and used the freed space at the
  top for the ball — the total drawing still fits the original `0 0 64
  100` viewBox with room to spare, so no other sizing changed.
- **Division logos on the pennants**: Division Titles and Division
  Pennants now show that year's division logo (`DB.divisionLogos`)
  inside the flag instead of (for Pennants) or in addition to (for
  Titles) plain text. Needed a year's *actual* division name, which
  PLAYOFFS itself can't give — its `brookside`/`brentwood` keys are
  fixed bracket-position labels, not real division names, so a 2018
  pennant would misreport as "Brookside" even though 2018's divisions
  were called North/South. Added `divisionNameOf(year, team)`, which
  looks up the real name from `DB.divisions[year]` instead — the same
  source Standings already reads for the year's actual division
  labels. Division Titles already iterated `DB.divisions` directly, so
  getting the division name there was free; Division Pennants now call
  `divisionNameOf()` per entry.
- **North/South explicitly unhandled, on request**: the user has North/
  South division logos to upload later but hasn't yet, and asked to
  leave 2017–2020 alone in the meantime. Since `DB.divisionLogos` only
  has `Brookside`/`Brentwood` entries, a lookup for "North" or "South"
  naturally returns `undefined` — each pennant/title item falls back
  to the pre-logo look (plain flag for Titles, the gold ★ for
  Pennants) automatically, no special-casing needed. Adding North/South
  logos later to `DB.divisionLogos` will make them appear with no code
  change.

Verified: Brookside Panthers' World Series trophies show the ball
above the star; their 2017/2018/2020 Division Titles (North/South
years) stay plain while 2021/2024/2025/2026 (Brookside years) show the
Brookside division logo; their 2013–2017 Division Pennants keep the
star fallback while 2021/2025/2026 show the logo instead; Brookside
Kraken's own titles correctly show the *Brentwood* division logo (they
play in the other division) — confirming the lookup is per-team, not
hardcoded; mobile renders cleanly; no console errors.

## More accurate wiffleball icon, then a side-view correction

User attached a photo of an actual wiffleball to correct the finial:
real ball has 8 elongated slots, not the small round dots the first
pass used. First fix replaced the five `<ellipse>` dots with 8 radial
`<line>`s evenly spaced in a full 360° ring — but that's a face-on
view (like looking straight down the ball's pole), when the reference
photo — and the trophy's own side-on framing — shows the ball from the
side, where only the holes on the near hemisphere are visible, most
foreshortened toward the edges.

Replaced the even 8-point ring with 7 slots confined to an arc across
just the top: three full-length slots at -24°/0°/24° (the "three holes
on top" the user asked for), then progressively shorter, thinner pairs
at ±47° and ±70° to suggest the remaining holes curving out of view
around the ball's sides — mimicking how a sphere's far-side and
underside holes foreshorten and disappear in a real side-view photo.

Verified by rendering the raw SVG standalone at 5x scale (a temporary
file served locally, not committed) since the icon is too small on the
actual page to inspect by eye: the arc reads clearly as a ball viewed
from the side with holes clustered on top, tapering down each side —
matching the reference photo's framing. No console errors on the live
page.

User's next look at it on the actual page: the hole detail just read
as noise at this size ("it looks bad"). Dropped the perforation
attempt entirely — the finial is now a single plain white `<circle>`,
no strokes or lines. A tiny icon doesn't have to resolve every detail
of the reference to do its job; a plain white ball above the star
already reads as "wiffleball" in context, and stops looking cluttered.

## Era toggle for Records

Added a three-way era filter to the Records page: "2017–2021 Era",
"2022–<current year> Era", "All Years" (default) — reusing the same
`.chips` component every other year/phase selector on the site already
uses, wired to a new `recordsEra` module-level state var (mirrors
`gYear`/`standYear`/etc.). A single `inEra(y)` predicate gates both
filtered sections:

- **Single-Season Records**: `seasonPool` now only pushes a
  player-season row when `inEra(s.year)` is true.
- **Single-Game Records**: the `GIDS.forEach` loop that builds
  `batPool`/`pitPool` skips a game entirely when its year fails
  `inEra`.

Both sections' description text now names the active era (`eraLabel`)
instead of always stating the site's full range, so the numbers shown
are self-explanatory without checking which chip is pressed.

**No-Hitters & Perfect Games explicitly excluded** — first pass filtered
it too, but the user asked mid-turn to leave it alone: that table is a
single continuous historical log (going back to 2013, before this
site's per-game data even starts) rather than a set of statistical
leaderboards, so slicing it by the same two eras didn't fit its
purpose the way it does for the other two sections. Reverted that part
and added a closing note under the table saying it's intentionally
unaffected by the toggle, so it doesn't read as a bug when the chip
selection doesn't change that table's contents.

The end year for the "2022–Pres" label pulls from `DB.seasonRange[1]`
rather than a hardcoded "2026", so it keeps reading correctly as the
league adds seasons in future rebuilds.

Verified: Batting Average leader changes from Peter Fraioli (.636, an
early-era season) under "All Years"/"2017–2021" to Tommy Peck (.571)
under "2022–2026"; both filtered sections' description lines update
to show the active era; the No-Hitters table and its footnote stay
identical across all three chip states; mobile renders cleanly; no
console errors.

## Career Records: added, then removed (already covered by Leaders)

Briefly added a "Career Records" section to the era toggle — each
player's seasons summed within the selected era, own qualifying
thresholds, team-of-record logic borrowed from Leaders' career mode.
User pointed out League Leaders' own Career mode already covers this
ground, so it was redundant on this page. Removed `careerPool`,
`careerTeamOf()`, `catC()`, `careerBat`/`careerPit`, and the "Career
Records" block from the template — Records' era toggle now applies to
just Single-Season and Single-Game Records, as originally shipped.

## Era chip order + a literal 0.00 ERA/WHIP being excluded from every leaderboard

Two small fixes from the same round of feedback:

- **Chip order**: "All Years" (the default) moved to the leftmost
  position in the era toggle, ahead of "2017–2021 Era" and "2022–<year>
  Era" — matches the existing convention on the Leaders page, where
  "Career" (its own default/aggregate option) is likewise first, ahead
  of the individual year chips.
- **Zero-value ERA/WHIP bug**: `catS()` (Single-Season Records) and
  `cat()` (League Leaders) filtered qualifying rows with `x.v!==0` —
  meant to drop a real zero (0 HR isn't a leaderboard-worthy stat), but
  it also silently dropped a pitcher whose ERA or WHIP legitimately
  computed to exactly `0.00` — the *best* possible value for either
  stat, not an absence of one. `cat()` already had the escape hatch
  half-built (`isFinite(x.v) && (o.zero||x.v!==0)`) but nothing ever
  passed `o.zero:true`; `catS()` was missing that half of the condition
  entirely. Added `zero:true` to both pages' ERA and WHIP category
  calls, and the missing `(o.zero||...)` branch to `catS()`.
- **Fallout from that fix — the "missing bars" report**: once a real
  0.00 could reach a low-is-better leaderboard, `svBarW()`'s highlight-
  bar width calculation broke for the whole list: `base` (the best/
  lowest value) became `0`, and the function's own `!base` guard — meant
  to catch a missing/undefined base — treats numeric `0` as falsy too,
  so the guard fired and returned `0` width for every row, not just the
  zero one. Rewrote the guard to check `isFinite(base)` instead of
  truthiness, and special-cased `base===0` for a low-is-better list: the
  row that *is* zero gets the full 100% bar, every other row gets the
  usual 8% floor (infinitely worse than a perfect zero, but still a
  visible bar).

Verified: era chips now read All Years → 2017–2021 → 2022–2026;
Single-Season Records' ERA list leads with a real 0.00 season, full
bar on that row, floor-width bars on the rest (previously invisible
bars on the entire list); HR/Wins/other non-rate categories still
correctly exclude true zeros; no console errors on Records, Leaders,
or mobile.

## Division pages (not linked from Teams, on request)

Added a new page per division — `#/div/Brookside` and `#/div/Brentwood`
— reached only from a division header on Standings or a division-logo
pennant in a team's Team Accolades, deliberately not added to the
Teams directory (explicit ask).

**North/South unified with Brookside/Brentwood**: the league realigned
divisions in 2021 (North → Brookside, South → Brentwood) — user
confirmed these are the same two divisions under old names, so treated
it exactly like a franchise surviving a name change elsewhere on this
site. Added `DIVISION_ALIAS` + `canonicalDivision()` (old name → live
key) and `divisionEraName()` (live key + year → whichever name
`DB.divisions` actually used that year) near `PLAYOFFS`, so both
Standings and the new division page can share the same mapping. A
division page's own URL and internal state (`divYear`) always use the
canonical (current) name; only the *display* name and the `DB.
divisions`/`DB.divisionLogos` lookups switch to the historical name for
years before 2021.

**Page content**, modeled after a team page's depth:
- Hero: current division logo + name, with "known as the North/South
  Division through 2020" when applicable.
- Year chips + a division-only standings table — reuses `standRow()`
  and the same row/column layout Standings already has, minus the
  cross-division "vs X" columns (meaningless with only one division on
  the page).
- **Division Champions**: every year's `'^'`-marked (division winner)
  team, newest first — deliberately NOT restricted to years the
  currently-viewed franchise won; this is the division's own history,
  so a champion list naturally includes different franchises across
  years (verified on Brookside: Brentwood Bananas 2023, Shelton Shock
  2022 both show up as *Brookside* division winners those years, since
  division membership is reassigned on realignment, not tied to a
  franchise's identity).
- **Member Teams**: every franchise that's ever had a season in this
  division, sorted by most seasons first, with each one's year span —
  a quick answer to "who's played in this division, ever."

**Wiring**: added a `#/div/(.+)` route in `dispatch()`. Standings'
division header (`<h4 class="divh">`) and Team Accolades' Division
Titles/Pennants pennants both got `data-div` buttons pointing at
`canonicalDivision(...)` of whatever name they're displaying — so a
2017 "North Division" header or a pre-2021 pennant (no logo yet, per
the earlier North/South note) still correctly links to the *Brookside*
division page. The pennant needed a couple of button-reset rules
(`border:0;font:inherit;cursor:pointer` on `.acc-pennant`, scoped
further with `button.acc-pennant` for the hover/cursor) since it went
from a plain `<div>` to a clickable `<button>`.

Verified: Standings' "Brookside Division" header and a Team Accolades
division pennant both navigate to `#/div/Brookside`; the division
page's 2026 standings match the Home page's own division snapshot
exactly (Panthers/Gladiators tied 8–7, Snapping Turtles 2–13); the year
chips walk back to 2017 and correctly show that year's actual team
names (era-accurate via `histName()`, e.g. "Brookside Bluefish");
Member Teams lists 12 different franchises for Brookside across its
history; the Teams directory page has zero mention of divisions
anywhere; no console errors.

## All-Star history and stats on division pages

Added two more sections to `renderDivision()`, between Division
Champions and Member Teams: All-Star Game History and All-Star
Selections.

All-Star squads are always exactly the two divisions facing each
other (North vs South, later Brookside vs Brentwood — never any other
pairing), so every ASG year applies to a division page; the interesting
part was matching squads by *division*, not by name, since `DB.asg`'s
own squad names lag `DB.divisions`' realignment by a year (divisions
switched to Brookside/Brentwood in 2021; ASG squads didn't switch
until 2022) and 2012 uses squad names ('Sluggers'/'Crushers') that
predate divisions entirely:

- `asgSquadFor(y)` finds whichever of `ASG[y].squads` canonicalizes
  (via the same `canonicalDivision()` from the earlier division-page
  work) to this page's division — naturally excludes 2012, where
  neither squad name has an alias.
- Box scores for the actual ASG games (`GAMES`, `phase==='AllStar'`)
  store the team as `"North Division"`/`"Brookside Division"` etc., so
  `boxForASG()` strips the `" Division"` suffix before running it
  through the same `canonicalDivision()` check — one matching function
  used for three different naming schemes (squad names, box-score team
  strings, and division-header labels) rather than three near-duplicate
  ones.
- Record and per-year result (W/L) come from `ASG[y].winner`, a
  loosely-formatted string (`"South 10-9"`, `"North"`, or empty for a
  no-decision year like 2021/2026) — parsed by taking its first word as
  the winning squad's name and comparing to this division's squad name
  that year.
- All-Star Selections is a plain appearance-count leaderboard across
  every squad roster this division has ever fielded, reusing the same
  name-normalization `plink()` already applies (strip a captain mark,
  drop periods, apply the two existing name aliases) so a count merges
  onto the same `P[]` key `plink()`'s own links resolve to — otherwise
  a roster entry spelled slightly differently one year wouldn't merge
  with itself in the tally.

Verified: Brookside's All-Star history runs the full 2013–2026 (no
2012, correctly excluded), showing "vs South" for years before the
2022 squad renaming and "vs Brentwood" after, with box-score links
appearing only for 2017+ (when per-game data exists) — matches the
site's existing per-game data floor everywhere else; Brookside's 5–7
all-time record and Brentwood's 7–5 are exact inverses of each other,
confirming the W/L parsing is internally consistent; a box-score link
opens the correct recorded ASG game; a Selections leaderboard name
links to the correct player page; no console errors; no horizontal
overflow at mobile width.

## Player stats on division pages — corrected to mean All-Star Game stats

First pass added a "Player Stats" section combining that year's
regular-season roster lines from every team in the division, with a
Regular/Playoffs toggle — modeled directly on a team page's own roster
tables. User clarified that wasn't what they meant: they wanted
**All-Star Game** stats specifically, not the teams' regular-season
numbers restated at the division level. Removed the regular-season
version entirely (the `divPhase` state var, its toggle, and the
`TEAMS[tm].seasons[divYear].roster` concatenation) and replaced it with
real batting/pitching lines pulled from the All-Star Game box scores
themselves.

All-Star Game Stats sits between All-Star Game History and All-Star
Selections: it walks every `GAMES` entry with `phase==='AllStar'`,
keeps the side whose team (after stripping the `" Division"` suffix
and running it through the same `canonicalDivision()` used everywhere
else on this page) matches the division being viewed, and folds each
player's bat/pit line through `gameBatRow()`/`gamePitRow()` — the same
per-game-to-ZERO_KEYS converters the player-splits feature already
uses — before summing with `sumRows()`. The resulting rows go straight
into the existing `rosterBatting()`/`rosterPitching()` (passing `'asg'`
as the phase key, since those functions only ever do `e[ph]` and don't
care what the key is called) rather than a new table-rendering path.
Since ASG games never touch a `TEAMS` roster at all, this is a
genuinely different data source from the (now-removed) regular-season
version, not just a relabeling.

Verified: Brookside's All-Star Stats batting table lists real per-game
lines (e.g. Peter Fraioli 6 G, .575 AVG, 2.146 OPS across his ASG
appearances) with a Team total row; column sorting still works; the
old "Player Stats" section and its toggle are gone with no leftover
`[data-dp]` elements; Brentwood's own totals differ correctly from
Brookside's; no console errors on desktop or mobile.

## Data fix: Daniel Brady's 2026 stats were entirely under the wrong team for his first 3 games

User: Brady started 2026 on Silver Lake Snapping Turtles, played 3
games there, then was traded to Brentwood Gladiators and finished the
season there. `players.json` had his entire 2026 Regular season (12
games) filed as one plain row under Brentwood Gladiators — the
Snapping Turtles stint was missing from his player page, his team
seasons, and the Turtles' own roster entirely.

The raw per-game box scores (`games`) were already correct — his three
May 28 game appearances (gids 1583/1584/1585) already show `Silver
Lake Snapping Turtles` as his side; the bug was purely in the derived
season aggregate and the `TEAMS` roster mirror of it, which had never
been split. Recomputed his two stints directly from those per-game bat/
pit lines (a one-off scratchpad script, not committed) and verified
the two splits sum to *exactly* the existing combined total before
writing anything — batting matched immediately; the one wrinkle was
pitcher W/L, where the box scores' own per-line `w`/`l` fields were all
`0` despite the season total showing 2 decisions. Resolved it by
checking, for each of his 4 pitching appearances, whether he was the
sole pitcher on his side and whether that side won or lost — his
Turtles start (5/28, sole pitcher, team won 11–7) accounts for the win
there; his three Gladiators appearances (sole pitcher in two losses,
one shared start in a win) accounted for the Gladiators' 1–2 — the
1+1 wins and 0+2 losses reconcile to the existing 2–2 exactly, so no
data was invented, just correctly attributed.

Changes, following the same "split season" convention already used
site-wide for a mid-year trade (e.g. AJ Cefaloni 2018):
- `players.json → players['Daniel Brady'].seasons`: the old single
  2026 Regular row became the `tot`/combined row (`team: null,
  tot: true, nTeams: 2`, stats unchanged since they already equaled
  the true total); added two new `split: true` rows, one per team,
  with the recomputed stint stats.
- `teamsByYear['2026']` updated to `"Brentwood Gladiators / Silver Lake
  Snapping Turtles"` (order matches build.py's own convention — more
  games first).
- `teams['Brentwood Gladiators'].seasons['2026'].roster`: his existing
  entry's `regular` line corrected down from all 12 games to just his
  9 Gladiators games (`playoffs`, entirely after the trade, was already
  correct and untouched).
- `teams['Silver Lake Snapping Turtles'].seasons['2026'].roster`: added
  a new entry for his 3-game stint (no `playoffs` key — he wasn't on
  the Turtles for the postseason).

`career`/`careerReg`/`careerPO` needed no change — those are full-
career sums and the total stats didn't change, only which team they're
attributed to within one season.

Verified: his player page now shows three 2026 Regular rows (Brentwood
Gladiators, Silver Lake Snapping Turtles, and a 2TM total) instead of
one; the Snapping Turtles team page now lists him with his 3-game
line; the Gladiators team page shows only his 9-game line; the new
Brookside Division Player Stats table (above) shows both stints
separately; no console errors.

## "Full Stats" sortable table on League Leaders

Added a second view to League Leaders, toggled via a new "Top 10" /
"Full Stats" `.segs` control: a complete, click-to-sort table of every
player who batted or pitched in the current scope, instead of just the
top 10 per category. Deliberately modeled on the Players page's own
stats table (`renderDir()`/`BAT_COLS`/`PIT_COLS`/`cell()`) since that's
the closest existing thing on the site — same column sets (minus the
`yrs` column, meaningless for a single year/career scope that's already
picked above), same click-a-header-to-sort behavor with its own
`leadSortKey`/`leadSortDir`/`leadMode` state (independent from
Players' `sortKey`/`sortDir`/`mode`, so switching modes on one page
never affects the other), same Batting/Pitching toggle that resets to
a sensible default sort column when switching.

Two differences from the Players table, both intentional:
- **Team logos** — the one thing the user explicitly asked to add
  that the Players page doesn't have. Reuses `teamOf(x)`, the helper
  the Top 10 lists already call for era-accurate team name + logo (and
  a second logo for a split season), so a traded player shows both
  clubs' marks here too.
- **Scoped to the Leaders page's own Career/year and Regular/Playoffs
  selection**, not always full career — `fullStatsHTML()` reads from
  the same `pool` array the Top 10 categories already use, so picking
  "2026" and "Playoffs" up top shows the Full Stats table for exactly
  that slice, not a fixed all-time view. No AB/PA/IP qualifying floor
  either — showing everyone who appeared, unfiltered, is the point of
  a "full" table as distinct from the qualified Top 10 lists next to
  it.

First pass also added `.pname[data-t]` wiring for a team link inside
the new table, but `teamOf()` only returns a display label (plain
text) — never a raw team key — the same as the Top 10 lists' own team
text, which isn't clickable either. Removed the dead wiring rather
than half-build team links against data that doesn't carry a key.

Verified: switching to Full Stats shows a sortable table with logos;
clicking HR re-sorts and switching to Pitching mode swaps to the
pitching column set with its own default sort (W); the view survives
switching Career/year and Regular/Playoffs (row count changes
correctly — 96 career batters vs. 40 with a Postseason at-bat); the
wide table scrolls in its own container with no page-level horizontal
overflow at mobile width; no console errors.

## Split-team rows show only the second team's logo

Every split-team leader row (Leaders' Top 10 and Full Stats, Records'
"2TM" single-season rows) was showing *both* team logos side by side
next to the "NickA/NickB" text. User asked to keep both names but drop
down to one logo — the second team.

Two render sites build these `<img>` tags from the same `{logo,
logo2}` shape `teamOf()`/`sLogo()` already produce, so the fix is the
same one-line change in both places: prefer `logo2` and only fall back
to `logo` when there's no second team, instead of concatenating both.
`llist()`'s shared `logos()` helper covers Leaders' Top 10 lists *and*
Records' single-season list (both eventually render through `llist()`
regardless of which page built the items); the Full Stats table's own
`fullCell()` needed the identical change since it builds its team cell
independently of `llist()`.

Verified: AJ Cefaloni's 2018 "Mustangs/Kraken" split-season row now
shows exactly one logo in the Leaders Top 10 list, the Leaders Full
Stats table, and Records' "2TM" row — all three previously showed two;
text still reads "Mustangs/Kraken" in every case; no console errors.

## Recent-scores ticker restyled as stacked boxes

The homepage "Recent scores" ticker (`buildTicker()`, the horizontal
scroller populating `#ticker`) rendered each game as one inline-flex
line: date, away logo/name, a shared "R–R" score, home logo/name, then
the playoff-round tag at the very end. User asked for it to look more
like a box: away team on top of home team, the playoff label moved
above the teams, and a date label.

Each `.tk-item` is now a column instead of a single row. A new
`.tk-head` strip sits on top holding the date (`.tk-d`) and, for any
postseason game, the round's `.gtag` — so the label reads before the
matchup instead of trailing after it. Below that, a new `tkRow()`
helper renders one row per team (logo, nickname, that team's own run
total via `.tk-row`/`.tk-nm`/`.tk-r`), away first then home, with the
winner bolded (`.tk-w`). `.tk-item` gained a `min-width` so the
boxes line up evenly while scrolling.

Follow-up: the winning row was also tinted to its franchise's accent
color via an inline `style="color:..."` from a `tint()` helper. User
asked to drop that — team names in the ticker are plain text now,
bold-only for the winner; `tint()` was removed from `buildTicker()`.

Verified locally: the ticker shows four-column-wide boxes, each with
the date and round label (e.g. "World Series", "Divisional Series") on
top and the two teams stacked below with per-team scores, winner in
bold with no color; clicking a box still opens that game's full box
score; no console errors.

## Site-wide spacing/formatting sweep

User asked to go through the whole site looking for spacing and
formatting issues. Reviewed every major page (Home, Players directory
and A-Z, a player page, Teams directory and franchise timeline, a team
page, Standings incl. Team Stats toggle, Leaders Top 10 and Full
Stats, Records, Games and a box score, Champs, Awards incl. Annual
Awards, a Division page, Beavers) at desktop and mobile widths, plus a
pass in both light and dark theme.

Found one real bug: `playoffBracket()`'s postseason-round badge icons
(`.pbicon`, the "POSTSEASON" and "WORLD SERIES" wordmark graphics) and
their round labels didn't line up with each other. The old markup
wrapped each icon+label+match-column together in one `.pb-group` flex
item, and `.pbracket` vertically centered each group as a whole — so
the round-1 group (two stacked semifinal matches, tall) and the World
Series group (one match, short) centered independently, landing their
icons at different heights. `.pbracket` is now a 5-column CSS grid
(`auto 34px auto 34px auto` for round1 / connector / World Series /
connector / champion); a new `.pb-lanehead` class holds each lane's
icon+label in row 1 (so both icons share the same top line), while the
match columns (`.pb-col`) and connectors sit in row 2, still centered
within that row's own track height — so the World Series box and the
champion card still land vertically centered between the two
semifinal boxes exactly as before. `playoffBracket()` is shared by the
homepage snapshot and the Standings page's per-year bracket, so both
picked up the fix from the one change.

Everything else checked out clean — no overlap, misalignment, or
broken wrapping found on any of the other pages/viewports/themes
reviewed. (Several things that looked like mojibake — "Â·", "â€"", the
sort-arrow glyph — while testing against a plain `python3 -m
http.server` locally turned out to be a local-only artifact: the raw
`index.html` fragment has no `<meta charset>` since the Artifact
publish pipeline adds one at wrap time. Confirmed clean on the live
published artifact, so left alone.)

Verified: bracket icons/labels align on the homepage's "2026 Playoffs"
snapshot and on the Standings page's per-year bracket; match-column
centering (World Series box and champion card between the two
semifinal boxes) unchanged; no console errors anywhere in the sweep.

## Team logos on the homepage leaders lists

The "2026 Season Leaders" and "Career leaders · regular season" grids
on the home page (`renderHome()`'s `ll()` lists) only ever showed a
player's name and value — no team context at all, unlike the identical-
looking `.llist` component on the real Leaders page, which pairs each
name with a logo and team-name subtitle via `renderLeaders()`'s own
`teamOf()`. User asked to add the logos here too.

Rather than duplicate that team-resolution logic, pulled it out of
`renderLeaders()` into a shared top-level `teamOfPlayer(x, year,
isCareer)` (right after `histNickLink`) — same behavior: era-accurate
team name/logo for a given year, "A/B" nickname text with the second
team's logo for a split season, and (for career mode) whichever team a
player was on most recently. `renderLeaders()` now just calls it
through a one-line `const teamOf = x => teamOfPlayer(x, leadYear,
isCareer);` wrapper, unchanged behavior. `renderHome()`'s `ll()` gained
the same logo markup `llist()` uses (prefer `logo2`, fall back to
`logo`) plus the `.lt` team-name subtitle, and a new `withTeam()`
helper decorates each ranked leader with `{tm, logo, logo2}` — the
season grid resolves against `LY` (the latest year), the career grid
against `isCareer:true` so it lands on each player's latest team.

Verified: both homepage grids show a logo + team name under every
player name, matching the Leaders page's look; clicking a name still
opens that player's page; checked at mobile width and both themes; no
console errors. No split-team player happened to land in the current
top-7 cutoffs to check that case directly, but it runs through the
exact same `teamOfPlayer()` already verified elsewhere (Leaders,
Records).

## Leaders polish: name wrapping, Full Stats spacing, split-team logo check

Three follow-ups after adding logos to the leaders lists:

**Names wrapping to two lines.** `.llist button.pname` allowed
`white-space:normal;word-break:break-word`, a holdover from before
logos/team subtitles existed in these rows. With a logo and a value
now also competing for space in a narrow `.llist` card (e.g. the
3-per-row grids on Leaders/Home), a longer name like "James
Duffelmeyer" would wrap to a second line and throw off row height.
Changed `.llist button.pname` and `.llist .lt` (the team-name
subtitle) to `white-space:nowrap` with `text-overflow:ellipsis` so a
name always stays on one line. To make sure that's a true fix and not
just a truncation band-aid, also tightened `.llogo` (30px→26px),
`.llist li`'s flex `gap` (10px→8px), and `.llist`'s side padding
(15px→13px) — measured via `scrollWidth`/`clientWidth` in the browser
that every name in every `.llist` card (Leaders Top 10, Home page,
Records) now fits with zero truncation, not just fewer characters
clipped.

**Full Stats team-cell spacing.** In the Leaders Full Stats table,
`fullCell()`'s `team` column dropped the `<img class="llogo">` and the
team name directly next to each other with no wrapper — an `<img>`
and a text node as bare siblings default to baseline alignment with
zero gap, so the logo and name were touching and the logo sat
noticeably higher than the text's visual center. Wrapped both in a new
`<span class="tmcell">` (`display:inline-flex;align-items:center;
gap:6px`), matching how `.llist` already center-aligns its own
logo/name pair via flex. Verified in the browser: logo and text are
now vertically centered on each other with a clean 6px gap, in both
Batting and Pitching mode.

**Split-team logo, re-checked on 2026 Daniel Brady specifically** (the
hand-entered Turtles→Gladiators split from earlier this session, since
that's a real multi-team case rather than a hypothetical one). His row
shows exactly one logo everywhere — Leaders Top 10 lists, Full Stats
(both Batting and Pitching), confirmed pixel-for-pixel identical to
the Silver Lake Snapping Turtles logo used elsewhere on the same page.
Team order in a split season's combined string follows build.py's
"most games played first" convention, not calendar order — for Brady
that puts Brentwood Gladiators (9 G) before Silver Lake Snapping
Turtles (3 G) in the "Gladiators/Snapping Turtles" text, so the "second
team" logo shown is the Snapping Turtles mark. That's consistent with
how every other split-team row on the site already resolves `logo`
vs `logo2`; no code change was needed here, just verification.

## Player page overview redesign

User asked to rework the top of the player page (`detail()`): show the
player's *current* team (not whoever they last played for, ever), add
a Baseball-Reference-style row of team-history number circles, replace
the Regular Season/Postseason split cards with two career-regular-
season cards (hitting, pitching), and drop the OPS-by-season /
ERA-by-season sparkline cards. Keep Accolades (rings, awards, All-Star,
no-hitters/perfect games — all already one function, `accolades()`)
and Percentile Rankings (`savantCard()`) as-is.

**Current team.** Added a top-level `LATEST_YEAR = Math.max(...ALL_YEARS)`
next to `ALL_YEARS`. The header meta line used to append whichever team
`latestTeam(pl)` returned — that player's most recent team *ever*,
regardless of how long ago. Now it only appends a team when
`pl.teamsByYear[LATEST_YEAR]` exists, i.e. the player actually has a
roster entry in the league's current season; otherwise the suffix is
just omitted. `latestTeam(pl)` itself is untouched and still drives
`setTeamVars()` (the page's accent-color theming), which intentionally
stays keyed to a player's most recent team ever, not just the current
year — a retired player's page should still carry their team's colors.

**Team history circles.** New `teamHistoryCircles(pl)` (next to
`barChart()`): one `.numring` circle per regular-season team stint
(each split row on its own, the combined "tot" row skipped), sorted by
year, ringed in the team's franchise accent color (`teamAccent()`,
same helper used for standings dots) with the jersey number in the
middle and a hover tooltip (native `title` plus a small styled
`.numring-tip`) showing team name and year. It reads the number from a
new (currently unpopulated) `s.num` field on each season row, and
**returns an empty string when no stint has one** — so it stays
invisible rather than showing a row of blank circles until real jersey
numbers exist in the data. See the blocker note below.

**Two new overview cards.** Replaced the `card()` helper's Regular
Season/Postseason pair with `hitCard` ("Regular Season Hitting":
AVG/OBP/SLG big line, HR/RBI sub-line) and `pitCard` ("Regular Season
Pitching": W–L + ERA big line, K/WHIP/IP sub-line), both off
`pl.careerReg` only — postseason totals are no longer shown in the
overview at all (they're still one tab away). Both fall back to a
"No appearances" line the same way the old cards did, for a pure
pitcher or pure position player.

**Sparklines removed.** The `playerSparks(pl)` call is gone from
`overviewHTML`; the function itself is left defined but unused (same
pattern as leaving `sparkline()` itself in place — cheap to keep,
matches how the codebase hasn't been deleting now-orphaned helpers
this session unless asked).

**Jersey-number data blocker.** There is no jersey number anywhere in
`players.json` or the team rosters — this is a brand new data field.
User supplied `team_player_lookup.csv` (TeamID, PlayerID, First, Last,
ShirtNumber from what looks like a league-management export), but the
TeamID has no team-name or year attached. Tried matching every TeamID
to one of our (team, year) rosters by player-name overlap
(`/private/tmp/.../scratchpad/match_teamid*.py`, not saved to the
repo) — high-overlap matches exist for maybe a third of the ~100
distinct TeamIDs, but many entries needed at high confidence show a
*different* TeamID confidently claiming the *same* team-year (e.g. four
separate TeamIDs all best-matching "Brookside Kraken 2025"), which
means the underlying assumption (one TeamID = one team-season) doesn't
hold cleanly, or a name-overlap heuristic alone can't resolve it given
how much players move between teams over 9 seasons. Did not write any
inferred numbers into `players.json` — wrong historical data is worse
than missing data. `teamHistoryCircles()` and the `s.num` field are
ready to go the moment real numbers land; needs either a cleaner
TeamID→team/year key from wherever that CSV was exported, or hand
entry.

## Jersey numbers: resolved via the league's Games export

User pointed at a second file, `BWB League Lineup Export.xlsx`
(`source/` in this repo), specifically its `Games` sheet —
`VisitingTeamID`/`VisitingTeamName`/`HomeTeamID`/`HomeTeamName`/`Date`
per game, 2017–2025. That's the key the roster CSV was missing: a
TeamID's `TeamName` (e.g. "Bluefish", "Panthers") plus the game's year
pins it to one of our franchises, because every team's `seasons[year].name`
field already stores that exact era-accurate nickname (this is how the
site knows Brookside Kraken were called "Bluefish" in 2017, etc.) — so
matching (nickname, year) against every franchise's own season names
resolves the TeamID with real evidence, not a name-overlap guess.

Wrote three one-off scripts (kept in the scratchpad, not the repo):
1. Built a `(nickname, year) → franchise` table from every team's own
   `seasons[year].name`, then resolved each of the 116 TeamIDs seen in
   the Games sheet against it. 100 resolved cleanly; the other 16 all
   turned out to be "North/South/Brookside/Brentwood Division" —
   division All-Star Game entries, not real club rosters, so correctly
   not part of anyone's *team* history.
2. For each resolved TeamID, matched `team_player_lookup.csv`'s
   (FirstName, LastName, ShirtNumber) rows against that specific
   team-year's actual roster (from `TEAMS[full].seasons[year].roster`
   — small, so exact-name-or-unique-last-name matching is reliable
   here in a way it wasn't across the whole league). A manual alias
   table covers 3 known nickname mismatches (Dan/Daniel Brady, Trevor
   Fraioli→Meyler, Bob/Brandon Gibbons). 226 rows resolved to a unique
   number; 10 (player, team, year) triples got *two different* numbers
   across the season's roster entries (e.g. Evan Wilkins shows both 21
   and 8 for Glenwood Process 2019) — left those out rather than guess
   which is right. ~66 CSV rows never matched anyone on that team's
   *recorded* roster — expected, since our roster lists only include
   players who accrued at least one tracked stat, while the league's
   registration list includes bench players who never did.
3. Applied the resulting 219 numbers to the matching `Regular`-season
   row in each player's `pl.seasons` (never the combined "tot" row for
   a split season) and re-saved `players.json`.

Two real gaps, not fixable from what's on hand: the Games sheet only
covers 2017–2025, so **no 2026 numbers exist yet** — every player's
current-team stint is missing from Team History until a 2026 games
export appears. And a handful of rows only exist under a `Fall` or
`Spring` season type with no matching `Regular` row that year (Austin
Corvino/AJ Cefaloni/Matt Crane on the 2020 Gladiators' Fall-only
season, JB Breig's 2021 Spring-only Kraken stint, Parker
Gibbons/TJ Ciafone's 2023 "Shraken" Spring team) — `teamHistoryCircles()`
only looks at `Regular` rows by design, so those numbers have nowhere
to attach; they're sitting unused in the assignment set if that filter
ever gets extended.

Verified: AJ Cefaloni's page shows 9 team-history circles across his
career (mostly "3", one "2" for a 2020 Lavahogs stint, tooltip on
hover reading "Lavahogs · 2020"); Evan Wilkins — who has several of
the 10 conflicting years — correctly shows only 3 circles, one per
clean year, with the ambiguous ones simply absent; checked in both
themes and at mobile width (circles wrap); no console errors.

## Team History: merged year ranges, two-tone rings, 2026 numbers

Three follow-ups from the user after seeing the circles live.

**Merge consecutive same-team-same-number years into one circle.**
`teamHistoryCircles()` used to emit one ring per `pl.seasons` row, so a
player who wore the same number for the same team for a decade showed
a decade of identical rings. It now walks the sorted rows and collapses
a run into a single `{team, num, from, to}` stint whenever the team,
the number (compared as strings, since `num` can come in as either),
*and* the year are all a direct continuation of the previous row —
any gap (a year with no number on record, a different team, or a
number change) starts a new stint. The tooltip shows the merged range
("Panthers · 2018–2026") instead of a single year when `from !== to`.

**Two-tone rings from the franchise's actual colors.** Previously the
ring used `teamAccent()` — a single derived color, the same one used
for standings dots, chosen specifically to be visible against both
light and dark themes. That's the wrong tool here: user asked for two
concentric rings, one in the team's primary color and one in its
secondary, "like the logos" — so switched to `FRANCHISE_COLORS[team].p`
and `.s` directly (the same pair `.thero`/`.pb-trophy`/team hero
banners already use for `--tp`/`--ts`), full-strength, no attempt to
lighten/darken for theme contrast. CSS: `--rc-p` drives the ring's
`border` (outer), `--rc-s` drives an `inset 0 0 0 3px` box-shadow
layered with the existing drop shadow (inner ring) — two color bands
around one circle, no extra markup needed.

**2026 numbers.** The league-export files only went through 2025 (see
above), so every player's current-team stint had no ring at all. User
pasted a roster dump instead — number, name, and team nickname for
2026, six clubs. Matched each row against our canonical player names
(three aliases needed: A.J.→AJ Cefaloni, T.J.→TJ Ciafone, Dan→Daniel
Brady) and each nickname to this year's franchise the same way the
Games-sheet nicknames resolved earlier (Panthers→Brookside Panthers,
Kraken→Brookside Kraken, Gladiators→Brentwood Gladiators,
Kings→Harris Kings, Snapping Turtles→Silver Lake Snapping Turtles,
Shock→Shelton Shock), then set `num` on each player's 2026 `Regular`
row. 47 of 55 pasted rows applied. The other 8: 4 are players brand
new to the league this year with no `players.json` entry yet at all
(Connor Moss, Joe Pugliano, Victor Arcara, Alden Dayton — nothing to
attach a number to until they record a stat line), and 4 are existing
players (Griffin Krueger, Dean Corvino, David Pizzutello, Nick Lucas)
who are on the 2026 roster but haven't recorded a single stat yet
this season, so they have no 2026 season row at all yet either — same
reason, not an error. Total jersey numbers on record: 266.

Verified: Peter Fraioli's 9 straight years on the Panthers wearing 17
now render as one ring, tooltip "Panthers · 2018–2026"; Victor Cottini
shows a merged "Shock · 2022–2023" ring plus a separate standalone
"Shock · 2026" ring (2024–2025 have no number on record, correctly not
bridging the gap); James Duffelmeyer's five different teams all wearing
9 stay five separate, distinctly two-toned rings, now including 2026;
checked in both themes; no console errors.

## Full team names on circles; career row on team season tables

Two small follow-ups.

**Full names on the Team History rings.** The ring tooltip was using
`TEAMS[team].nick` (e.g. "Panthers") — user wants the full name
("Brookside Panthers"), and for a merged multi-year stint that happens
to span a franchise rename, the *latter* name. Switched to the
existing `histName(team, year)` helper (same one game pages and box
scores use so they never claim a modern name existed in the past), but
called with `st.to` — the stint's last year — instead of `st.from`, so
a run that crossed a rename shows the name it ended under. No franchise
in the current jersey-number data actually spans a rename yet (the
resolved years don't reach back to a team's earliest name), so this
couldn't be verified against a real example, but the logic mirrors
`histName`'s existing, well-exercised behavior elsewhere on the site.

**Career row on the team page's Season by Season table.**
`teamRecordTable()` now sums W/L/T, RF, RA and roster-row count across
every season and appends one `Career` row in a `<tfoot>` (same styling
every other totals row on the site uses). PCT and the playoff record
are recomputed from the *summed* W/L rather than averaging each year's
own rate, so they stay internally consistent with the row's own
W–L — e.g. Brookside Panthers' new Career row reads 106–71 / .599 /
+184 diff / 10–10 playoffs / 54 roster-slots, each hand-checked against
a manual sum of the ten season rows above it.

## Team History tooltip clipping off the page edge

The `.numring-tip` hover tooltip was always centered under its ring
(`left:50%;transform:translateX(-50%)`). Team History sits flush at
the page's own left margin, so the first ring's tooltip — often a
full franchise name plus a year range, wider than the 46px ring itself
— had nowhere to go on its left half and ran off the edge of the page.
Added `.numring:first-child .numring-tip{left:0;transform:none}` to
anchor that one to the ring's left edge instead of its center (so it
only ever grows rightward, into the row), and a mirrored
`:last-child` rule (`left:auto;right:0`) so a full-width row's final
ring doesn't run off the *right* edge either. Ordered the `:last-child`
rule first in the stylesheet so a single-ring row (matching both
selectors) resolves to the `:first-child` behavior — grow right, not
left — since that's the one guaranteed safe direction for a ring
sitting at the page's left margin.

Verified: AJ Cefaloni's now-4-ring history (post-merge) — hovering the
first ring ("Brentwood Mustangs · 2018") stays fully on-page instead of
clipping left; checked the last ring's computed style directly
(`right:0`, tooltip's right edge flush with the ring's right edge)
since that row wasn't wide enough on its own to visually prove the
right-edge case. No console errors.

## Fixed: single-ring players still clipping (Peter Fraioli, Trevor Meyler)

The `:first-child`/`:last-child` fix above missed a case: a player with
exactly **one** Team History ring (Peter Fraioli's whole career
collapsed into one "Panthers 2018–2026" ring by the earlier merge
work) matches *both* selectors at once. CSS cascades per-property, not
per-rule — the `:last-child` rule set `right:0` and the `:first-child`
rule only overrode `left` (to `0`) without touching `right`, so the
lone ring ended up with `left:0` **and** `right:0` simultaneously.
For an absolutely-positioned box with `width:auto`, having both left
and right set stretches the box to fill exactly that span — here, the
46px ring itself — squashing the tooltip down to a ~40px box regardless
of its actual text. Confirmed via computed style before the fix:
`width: 40px` for a tooltip that should have been ~207px; after adding
`right:auto` to the `:first-child` rule (so it fully overrides every
positioning property the `:last-child` rule might have left behind,
not just `left`), the same ring now computes `width: 207.375px` — its
natural, unstretched size — anchored correctly at the ring's left edge.

This is why it looked fine for players with 2+ rings (Trevor Meyler
included) — only a lone ring hits both selectors at once, so it's a
narrower bug than "the whole fix is broken," but a real one.

Verified: Peter Fraioli's single ring now shows the full "Brookside
Panthers · 2018–2026" tooltip at its natural width, positioned on-page;
re-checked AJ Cefaloni's 4-ring row (first/middle/last) still computes
correctly with no stretching on any of them; no console errors.

## 2017 numbers backfilled from 2018

2017 had zero jersey numbers (the roster export's 2017 rows all had
`ShirtNumber: 0`, i.e. no data — see the earlier "Jersey numbers"
section). User's call: for any player who also played in 2018, copy
their 2018 number back onto their 2017 row, on the reasoning that a
rec-league player's number is normally sticky year to year regardless
of which team they were on. Applied literally as asked — by player,
not by matching team, so e.g. Jake Quigley's 2017 Brookside Panthers
row now carries the `27` he wore for Harris Kings in 2018, even though
that's a different club.

14 players had both a 2017 and a 2018 row; 13 got a number this way.
The 14th, Alex Homem, has no 2018 number on record either (his 2018
row exists but was never matched to a shirt number), so there was
nothing to copy — he's still a gap. Also found and separately reported
to the user: 6 players who appear in 2017 but never again — Jaden
Helmer (Brookside Kraken), Joey Cardascia (Brentwood Braves), Mathew
Wilkins (Glenwood Process), Sam Estroff (Brookside Panthers), Sean
Walther (Brentwood Mustangs), Tristan An (Brookside Panthers) — user is
supplying their numbers directly since there's no later year to infer
from.

Verified: Peter Fraioli's ring now merges all the way back to
"Brookside Panthers · 2017–2026" (wore 17 the whole time); Vinny Spoto
— who changed teams between 2017 and 2018 — correctly keeps 2017 as
its own standalone "Brentwood Dashers · 2017" ring (era-accurate name)
rather than merging into the 2018+ Panthers ring, since the team
differs; no console errors.

## 2017-only players and a Dan Brady correction

User supplied numbers for the 6 players flagged as appearing in 2017
only (no later year to backfill from): Jaden Helmer (Kraken, #1), Joey
Cardascia (Braves, #8), Mathew Wilkins (Process, #2), Sam Estroff
(Panthers, #1), Sean Walther (Mustangs, #8), Tristan An (Panthers,
#33) — applied directly to each one's 2017 `Regular` row. Separately,
Alex Homem's missing 2018 number turned out to be `#2`; applied to
both his 2017 Glenwood Process row (per the "use 2018's number" rule)
and his 2018 Harris Kings row.

Then a correction: Daniel Brady's numbers had drifted across three
different sources this session — `13` from the historical CSV match
(2022, 2023, 2025), `21` for 2024 (same CSV, evidently wrong), and
`11` for 2026 Gladiators (from the user's own pasted 2026 roster,
also apparently wrong) — with his 2026 Snapping Turtles stint missing
a number entirely. User confirmed directly: all of Dan Brady's numbers
are `13`. Overwrote every one of his `Regular` rows (2022 Gladiators,
2023 Gladiators, 2024 Gladiators, 2025 Gladiators, 2026 Gladiators,
2026 Snapping Turtles) to `13` — his Team History now shows two rings,
a merged "Brentwood Gladiators · 2022–2026" and "Silver Lake Snapping
Turtles · 2026", both `13`.

## Merged a duplicate player: Nick Sabino / Nikolas Sabino

User caught that `players.json` had two separate records for the same
person — "Nick Sabino" (2024, Shelton Shock, 10 games) and "Nikolas
Sabino" (2025, Downtown Titans, 12 games) — evidently split because
some 2024 box scores logged him as "Nick" while everything from 2025
on used "Nikolas." No year or team overlap between the two records, so
the merge was a straightforward union rather than a reconciliation:
combined `seasons`, `years`, `gids`, `teamsByYear`, and summed
`career`/`careerReg`/`careerPO` field-by-field (safe since the two
records never shared a game), concatenated `honors` (carrying over his
2024 Rookie of the Year), kept the merged record under "Nikolas
Sabino," and deleted the "Nick Sabino" entry.

Being a name that only lives as a string in a few places, not a
foreign key, the merge also had to sweep: 14 box-score bat/pit line
`n` fields across his 10 "Nick Sabino" games (`games[gid].away/home
.bat/pit[].n`), his one team-roster entry (`teams[...].seasons[...]
.roster[]`, renamed rather than merged since no "Nikolas Sabino" entry
existed on that team-year to merge into), and — caught only by a
generic recursive string-scan over the remaining top-level DB
sections — the `winner` field on his own 2024 Rookie of the Year award
record, which still said "Nick Sabino" after the player-record merge.

Verified: Nikolas Sabino's page now shows 2 seasons (2024–2025, 21 reg.
games), both team-history rings (6 for Shock 2024, 20 for Titans
2025), the Rookie of the Year accolade, and combined career hitting/
pitching lines; the 2024-05-26 box score vs. Brookside Panthers (one of
his renamed games) now prints "Nikolas Sabino" in the Shock batting
table; no leftover "Nick Sabino" anywhere in the generated output; no
console errors.

## Awards page: tabs instead of scroll-links, plus team logos

Two changes to `renderAwards()`. First, the page used to render both
All-Star history and Annual Awards on one long page with a `.subnav`
of anchor links that just scrolled you to one section or the other —
both sections always rendered, always in the DOM. User asked for real
tabs. Added `let awardsTab = 'awards'` module state and a `.subtabs`
toggle (same component the player page uses for its Regular/Playoffs/
All-Star/etc. sections) with "Awards" and "All-Star Games" buttons;
`renderAwards()` now renders only the active section's function
(`awardsSection()` or `asgSection()`), defaulting to Awards. Each tab
gets its own `<p class="note">` tail text instead of one note trying
to cover both.

Second, `tnick()` (resolves an award's team-nickname string to a
linked franchise button) gained an optional `year` parameter: when
given a year, it now renders `histNick(full, year)` instead of the
franchise's current nickname, and prepends a small `<img
class="tlogo-mini">` from `teamLogoForYear(full, year)` — so a 2018
award correctly shows that era's name and logo instead of retroactively
applying today's branding. `awardsSection()` passes each row's actual
award year through. `tnick()` had exactly one call site, so this
couldn't regress anything else.

Verified: Awards tab shows first by default; clicking All-Star Games
swaps the section and back; 2026 MVP row shows the Shock logo inline
next to the team name; no console errors.

## Removed 10 zero-game "phantom" season rows

User's rule: a player shouldn't be shown as rostered for a team-season
where they recorded zero games; an exhibition-only (Spring/Fall)
appearance is fine to show on those tabs, just not folded into the
Regular season roster.

Before touching anything, searched every player's `seasons` for a row
with a `team` set and `G_bat === G_pit === G_fld === 0`. Found 10 —
9 `Regular`, 1 `Playoffs` (Nima Khodakhah, 2022 Brentwood Gladiators).
Every one of them turned out to be linked to a real game ID from that
year, which matches a documented site limitation: "2017–19 games were
usually logged as a single line per team," so a player can be in a
game's lineup with no individual stat line recorded. Surfaced the full
list to the user before changing anything, since 3 of the 10 were a
player's *only* season on record — removing them meant deleting the
player entirely, one of which (Sean Walther) had just been given a
jersey number the same session, and carried a real 2014 Comeback
Player of the Year award. User's call: remove all 10 as originally
asked.

For the 7 that leave the player otherwise intact: deleted the zero row
from `pl.seasons`, recomputed `years` from what's left, and for the
affected year either dropped it from `teamsByYear` (nothing left that
year) or repointed it at whichever row remains — Reed Hakim's 2020
`teamsByYear` now points at Brookside Kraken (his real Fall stint)
instead of the deleted zero-game Panthers row. Nima Khodakhah's zero
Playoffs row also had a matching `teams[...].seasons.roster[]` entry
(the only one of the 10 that did) — removed its `playoffs` stat block
there too, keeping the entry for his real Regular season.

For the 3 that emptied out entirely (Sean Walther, Trevor Fraioli,
Brendan McGurk): deleted each player record outright. Checked all
three for any other reference across `awards`/`asg`/`champs`/
`noHitters` first — only Sean Walther's award turned up
(`awards.2014[17].winner`), left as plain text since `plink()` already
falls back to unlinked text for a name with no `P[]` entry, so the
historical award fact itself still displays correctly, just without a
player-page link. Trevor Fraioli and Brendan McGurk had no other
references anywhere.

Verified: Reed Hakim's page now shows his real 2020 Fall Ball stint
(Brookside Kraken, 3 games) with the bogus Panthers Regular row gone
from both the season table and his Team History rings; Sean Walther's
2014 award still renders with the Harris Kings logo, name now plain
text instead of a link; `P['Sean Walther']`, `P['Trevor Fraioli']`,
`P['Brendan McGurk']` all resolve to `undefined`; Nima Khodakhah's page
and his Brentwood Gladiators 2022 team page both render cleanly; no
console errors anywhere.

## Player overview cards renamed to Career Hitting/Pitching

Label-only change: the two overview cards at the top of a player page
(`hitCard`/`pitCard` in `detail()`) were titled "Regular Season
Hitting"/"Regular Season Pitching." User asked for "Career Hitting"/
"Career Pitching" instead. Retitled both `<h4>`s; the underlying data
is unchanged — still `pl.careerReg` (regular-season career totals
only, postseason excluded, same as before), just described as
"career" rather than "regular season" since that's the more natural
read for a career-totals card. Verified the two titles render as
"Career Hitting" / "Career Pitching" with no console errors.

## Added OPS+ (FIP skipped — data doesn't support it)

User asked for OPS+ and FIP on the career cards. Checked the codebase
first (via a research subagent) for any existing league-average
infrastructure to build on — there is none; no file anywhere sums
stats across all players into a league-total bucket. Also surfaced a
hard blocker for FIP: the box-score pitching line is `{IP, H, R, ER,
BB, K, W, L, SV}` — no home-runs-allowed field for pitchers (only
batters carry a HR stat), and since games commonly use more than one
pitcher, there's no way to attribute a specific home run to a specific
pitcher after the fact even if the raw box scores were re-parsed.
Textbook FIP needs HR-allowed as its core term. Asked the user how to
handle it (an HR-less component formula, skip it, or something else);
they chose to skip FIP entirely for now and just add OPS+.

**OPS+.** Added a new top-level league baseline right after `sumRows`
(needs it): `LEAGUE_CAREER = sumRows(NAMES.map(n=>P[n].careerReg))`,
then `LG_OBP`/`LG_SLG` off that, and `opsPlus(d) = 100*(obp(d)/LG_OBP +
slg(d)/LG_SLG - 1)`, rounded. This is an **all-time** baseline (every
player's entire regular-season career summed together), not a
per-season one — simpler, and matches the "Career" framing the
hitting/pitching cards just got renamed to, at the cost of not
adjusting for any scoring-era drift the way a real single-season OPS+
would. Wired into the Career Hitting card's sub-line: `HR · RBI ·
OPS+`, with a hover title ("100 = league average, all-time") since
it's not a self-explanatory number like HR or RBI. Guarded with
`isFinite()`/`d.AB` checks so a player with no at-bats just omits the
figure instead of showing `NaN`.

Verified: James Duffelmeyer's career .563 OBP/1.271 SLG against the
league's .597/.941 baseline computes to 129 OPS+, matching a
hand-worked check of the formula; low-output players correctly show
negative OPS+ (mathematically valid — it isn't floor-bound at 0, same
as real-world OPS+) without any display glitch; checked Home and a
couple of player pages for console errors post-change — none.

## OPS+ everywhere OPS already appears

Follow-up: user wanted OPS+ next to OPS site-wide, calling out Leaders
and Records specifically. Used a research subagent to grep every
`'OPS'` occurrence and map each to its page/function before touching
anything, since this stat shows up in four structurally different
patterns across the file:

- **Pattern A** — a `[key,label,type]` column-tuple array read by a
  generic `cell()` formatter, with a separate row-builder computing
  the actual values (`BAT_COLS`/`rowVals` — Players directory *and*
  Leaders' Full Stats view, which reuses `BAT_COLS`; `T_BAT_COLS`/
  `teamRowVals` — Team directory summary). Gave `OPS+` type `'n'`
  (plain integer) rather than `'r'`, so it falls through `cell()`'s
  existing untyped-number branch (`isFinite(v)?String(v):'—'`) instead
  of hitting `rate()`'s decimal formatting — meant zero changes to
  `cell()` itself, in either location.
- **Pattern B** — a `{l, m, f}` self-contained-formatter array fed
  straight to `statTable()`, one `f` per column. Seven of these:
  player-page season-by-season batting (`phaseBlock`), Standings'
  per-year Team Batting table (`renderStandings`, `League` row
  included), a team's per-season roster batting (`rosterBatting` —
  also what division pages reuse for All-Star Game stats, so those
  picked it up for free), a franchise's batting-by-season table
  (`teamStatsBySeason`), the franchise's all-time roster table
  (`teamAllYears`, which only had AVG/OPS with no OBP/SLG columns —
  added OPS+ after OPS there too), player-page Splits tables
  (`SPLIT_BAT_COLS`), and the Beavers page batting table. Each got
  `{l:'OPS+',m:1,f:d=>{const v=opsPlus(d);return isFinite(v)?String(v)
  :'—';}}` inserted right after its `OPS` entry.
- **Pattern C** — `cat('OPS', ...)` / `catS('OPS', ...)` calls building
  a Top-10-style leaderboard card via the shared `llist()` — Leaders'
  batting Top 10 and Records' single-season batting Top 10, the two
  the user named explicitly. Added a new `cat('OPS+', s=>opsPlus(s), …)`
  / `catS('OPS+', …)` call right after each, giving both pages a
  standalone "OPS+" leaderboard card. Records' version applies the
  same all-time league baseline to a *single season's* rate stats —
  consistent with how the site already treats OPS+ everywhere else,
  though a real single-season OPS+ would normalize against that
  season's own league average rather than the all-time one.
- **4th pattern** — `SV_BAT`'s `[label, fn, fmt, lowerBetter]` tuples
  driving the Percentile Rankings panel's percentile bars. Added
  `['OPS+', c=>opsPlus(c), v=>isFinite(v)?String(v):'—', false]` after
  `OPS` there too, so a player's OPS+ now gets its own percentile-rank
  bar alongside AVG/OBP/SLG/OPS.

Also had to extend the two `batKeys` sort-reset whitelists (one in
`renderDir`, one in `renderLeaders`) to include `'OPS+'` — without it,
sorting a table by the new column and then switching to Pitching mode
would leave `sortKey`/`leadSortKey` pointing at a column that no longer
exists in the pitching table instead of resetting to a pitching
default.

**Left alone, deliberately:** the Home page's two leader-snapshot grids
(`cGrid`/`yGrid` in `renderHome()`) have an "OPS · 150+ PA" / "OPS · 9+
G" card each, but those grids are a fixed, curated set of highlights
rather than an exhaustive stat index like Leaders/Records — didn't
expand them, since the user's explicit examples were the two
comprehensive stat-browsing pages. Easy to add if wanted.

Verified across every surface: Leaders Full Stats column sorts
correctly by OPS+ and resets cleanly on switching to Pitching mode;
Leaders and Records each show a new standalone "OPS+" Top-10 card;
Players directory, Team directory, a team's roster/season-by-season/
franchise-all-time tables, a division page's All-Star stats, player
Splits tables, the Beavers page, and Standings' Team Batting table (League
row included) all show the new column; the Percentile Rankings panel
shows an OPS+ bar; no console errors on any page checked.

## OPS+ correction: season-specific, not all-time

User caught a real modeling error: OPS+ is always relative to *that
season's* league average, never an all-time or blended one. The
version just shipped compared every player-season to one fixed
all-time league OBP/SLG — wrong for exactly the reason a real OPS+
exists: it's supposed to correct for scoring-era differences, and an
all-time baseline throws that away. Rebuilt the whole thing.

**Single-season OPS+** is now straightforward: `LEAGUE_BY_YEAR[year]`
(and a separate `LEAGUE_BY_YEAR_POST[year]` for postseason) is that
year's combined batting line across every player who recorded one that
year — built the same "sum every non-tot row" way a team's own
per-year total already is, so a split season counts once. A season's
OPS+ is `100 × (OBP/thatYear'sLgOBP + SLG/thatYear'sLgSLG − 1)`.

**Career (or any other multi-year) OPS+** needed the approach the user
specified directly, not what I'd started building (PA-weighting each
season's own *OPS+ result*, which isn't the same thing): weight the
*league baseline itself* by the player's own PA in each year they
played, then apply the standard formula once to their actual career
totals against that blended baseline. So a year a player barely
played barely moves their baseline, same as a real career OPS+'s
weighted league average. Implemented as `opsPlusFor(d, weights)` —
`d` is the stat bucket to evaluate, `weights` is `[{year, pa, post}]`;
for a single season that's a one-entry array (the weight value doesn't
matter with only one contributor); for a career it's one entry per
year with plate appearances, weighted by how many.

Every site touched in the earlier OPS+ pass needed rewiring to supply
the right `weights` for its own context, since each one previously
called the flat old `opsPlus(d)`:
- **Player-career contexts** (Players directory, Team directory, a
  player's Career Hitting card, Leaders' Career scope) use a new
  `careerWeights(pl, post)` — every one of a player's own
  `{year, pa}` pairs, straight from `pl.seasons`.
- **Team-career contexts** (Team directory's franchise-wide row,
  the franchise's all-time roster table) needed the *team's* own
  year-by-year PA instead of any one player's — added `TAGG_WEIGHTS`
  alongside the existing all-time `TAGG` aggregate, and a per-player
  `_weights` array (that player's own PA *while on this specific
  franchise*, which can be a subset of their whole career) on each row
  of the franchise roster table.
- **Single-year contexts** (Records, Standings' Team Batting +
  League row, the Percentile Rankings panel, a team's one-season
  roster table, one row of a season-by-season table) just pass a
  one-entry weight for that specific year — for these, `s.year` was
  usually already sitting right on the stat-bucket object being
  formatted, no extra plumbing needed.
- **Leaders' Full Stats table and Top-10 cards** had to keep working
  in *both* modes (Career chip vs. a specific year chip) — used
  `isCareer` to pick between `careerWeights(P[x.n], isPost)` and a
  single-year weight. `cat()`'s formatter only ever receives the raw
  stat bucket, never the player name it belongs to, so for the Top-10
  card specifically, precomputed a `Map` from each pool item's bucket
  *object reference* to its weights before building the list — the
  cleanest way to smuggle the extra context through without changing
  `cat()`'s signature (which a dozen other stat categories also call).
- **Player Splits tables** were the hardest case: a split bucket can
  pool games from every year at once (the "All" chip, the default) or
  from one selected year. `SPLIT_BAT_COLS` became a function
  (`splitBatCols(weights)`) so each call can supply the right weights;
  `playerSplits` computes them once — a single-year weight when one
  year's picked, or (for "All") each year's actual share of the
  player's own PA across the exact games behind that split, by
  re-deriving PA per game year from the same `gameBatRow()` used to
  build the splits themselves.
- **Two contexts have no sound baseline at all and now honestly show
  "—" instead of a fabricated number**: a division page's All-Star
  Game combined stats (spans years with no per-appearance year kept
  by that point in the pipeline) and NWLA tournament splits (not part
  of the BWB league). The Beavers page's main batting table lost its
  OPS+ column outright rather than a column of nothing but dashes —
  the Beavers' NWLA opponents aren't part of the BWB league either, so
  there's no league to compare against there at all.

Also fixed a real bug the rewrite introduced and caught before
publishing: the new `buildLeagueByYear()` referenced `ALL_YEARS`,
which isn't declared until much later in the file — since it's a
top-level `const` that runs immediately (not deferred inside a
function body), this crashed every page load with "Cannot access
'ALL_YEARS' before initialization." Fixed by deriving the set of years
directly from the season data being summed, removing the dependency
entirely.

Drive-by fix noticed while testing: the franchise's all-time roster
table's "Yrs" column printed the literal word "undefined" in its
totals row (pre-existing, unrelated to OPS+ — the column's formatter
reads a field that only individual rows have, never the summed total).
Added `noTot:1` so the total row leaves that cell blank instead,
matching how every other non-summable column already behaves.

Verified extensively: League's own OPS+ on the Standings page comes
out to exactly 100 for every year (the correct sanity check — a
league's combined line compared to its own average must equal
exactly the average); James Duffelmeyer's career OPS+ (193) matches a
full hand-worked recomputation of the PA-weighted formula; his 2026
single-season OPS+ (253) matches a hand check against 2026's own
league baseline; Records/Leaders/Full Stats/franchise-roster all agree
with each other on the same player's same-scope number; switching a
Splits table between "All" and a specific year changes the number as
expected; Division ASG and Beavers correctly show no fabricated
figure; no console errors on any page (one stale cached error from an
earlier broken build briefly confused verification — confirmed via a
fresh tab that it wasn't reproducing on the fixed code).

## Data fix: 2021-08-15 Kraken/Process tripleheader location

All three games between the Kraken and Process on 2021-08-15 (gids 28249259,
28249260, 28249261) had `loc: "TBA"`. Set to `"Brookside Field"` per the user.
Direct `players.json` edit, no generate.py change needed for the data itself.

## Field column on the Games tab

The master Games list (`renderGames()`) showed Date/Away/R/Home/Season but not
where the game was played, even though every game row already carries a `loc`
field (used elsewhere — box-score headers, the player Splits "By Field"
breakdown). Added a Field column between Home and Season, falling back to
"TBA" for the ~60 games with no recorded location (same fallback the Splits
code already used).

## Beavers page: games grouped by tournament

The Brookside Beavers page (`renderBeavers()`) is the club's national-team
page (NWLA tournament box scores, separate from BWB league play). It was
built around a single tournament (`beavers` was one object in players.json:
`{team, meta, games, batting, pitching, inRegister, logo}`), with the user
noting more tournaments will be added over time and asking for games to sit
under a tournament-specific heading (e.g. "2026 NWLA National Tournament")
rather than a flat "Games" list.

**Pipeline change (`build.py`)**: `beavers` is now a **list**, one entry per
tournament. `_BV_TOURNAMENTS = [_BV_2026]` holds the source modules (each a
`beavers_YYYY.py` file, same format as the existing `beavers_2026.py`) —
adding a tournament in the future means writing a new module and appending it
to this list, no other pipeline change required. The per-tournament
aggregation logic (box-score parsing, batting/pitching totals, the
player-profile "NWLA" season-row injection) is unchanged, just wrapped in a
loop over tournaments; the injected player season row's `year` now comes from
that tournament's own `meta.date` instead of a hardcoded `2026`.

`players.json` was updated directly to match (`d['beavers'] = [d['beavers']]`)
rather than rerunning the full `build.py` CSV pipeline, which would have
overwritten every hand-patch made to `players.json` this session (Sabino
merge, jersey numbers, zero-game-row removal, etc.) that has no CSV source.

**Rendering (`generate.py`)**:
- `BV` (single object) → `BV_LIST` (array). `BV_ALL_GAMES` (flattened games,
  used by the player-profile NWLA game log/splits, which don't care which
  tournament a game belongs to) and `BV_INREG` (a `Set` union of every
  tournament's `inRegister`, used by `bvName`) are derived once.
- `renderBeavers()`: the hero and the Record/Team Batting/Team Pitching
  overview grid are now **all-time across every tournament** (summed
  records; `mergeBvRows()` sums a player's batting/pitching lines by name
  across tournaments, so a player who appears in multiple tournaments gets
  one combined row instead of a duplicate per tournament — this only matters
  once a second tournament exists, but the merge is correct now rather than
  needing a fix later). Below the overview, each tournament gets its own
  `<h3>` section (`"${year} ${event}"`, e.g. "2026 NWLA National Tournament")
  with that tournament's own record line and phase-grouped game cards —
  this is the section the user asked for. The Batting/Pitching stat tables
  stay as one combined career leaderboard below all tournament sections.
- `playerNWLALog`/`playerNWLASplits` (player-profile "NWLA Tournament" tab):
  switched from `BV.games` to `BV_ALL_GAMES` — no other logic change, since
  they already worked in terms of individual games regardless of which
  tournament produced them.

Verified: 2026 page unchanged in substance (same 7 games, same batting/
pitching totals — `mergeBvRows` over one tournament is the identity), now
under a "2026 NWLA National Tournament" heading; player NWLA tab (e.g. Parker
Gibbons) still shows the game log and splits correctly; no console errors.

## Team captains and co-captains

Added a "Leadership" section (Captain + Co-Captains, with the years each
co-captain held the role) to every franchise page, from a list the user
provided by hand — this isn't derivable from any existing data (box scores
don't record team leadership).

Data lives in a new top-level `leadership` object in `players.json`, keyed by
full franchise name (matching `TEAMS` keys), e.g.:
```
"Brookside Panthers": {"captain": "Peter Fraioli",
  "coCaptains": [{"name": "Victor Cottini", "years": "2015"}, ...]}
```
`generate.py`: `LEADERSHIP = DB.leadership`; `leaderName(n)` links to the
player page if `n` exists in `P` (the register), otherwise renders plain text
— several co-captains predate the 2017 stat database and were never tracked
as players (e.g. Kento Kamezaki, Aidan Cocuella, Kodai Tachimoto, Ike
Onwuasoanya, AJ Trolio, Jonathan Alsina), and one (Sean Walther) was removed
from the register entirely earlier this session as a zero-game player — all
correctly fall back to plain text rather than a dead link. `teamLeadershipHtml(full)`
renders the block; wired into `teamDetail()` right after the hero.

**Six franchises with no existing page.** The user's list covered 20 teams,
but only 14 have a `TEAMS` entry — Sox, Royals, Aces, Squirrels, Angels, and
Diablos all folded before 2012–2016, before the stat database begins (2017),
so they only existed as historical rows in `FRANCHISE_SUMMARY`/
`FRANCHISE_TIMELINE` (win-loss record and name-history only, no rosters or
box scores, `f: null`). Asked the user whether to skip these or add bare
pages for them; they chose bare pages. Added `renderHistoricalTeam(d)`: a
stripped-down page (hero using `FRANCHISE_COLORS/franchiseLogos` — both
already existed for all 6 — the franchise's win-loss record, its name-history
eras from `FRANCHISE_TIMELINE`, the new Leadership section, and a note
explaining why there's no roster/box-score detail). `teamDetail(name)` now
falls through to this path when `TEAMS[name]` doesn't exist but a historical
`FRANCHISE_SUMMARY` row does; `renderTeams()`'s Franchise Summary table and
`franchiseTimeline()` both link to these 6 the same way they already linked
to live franchises (previously plain, unlinked text since there was nowhere
to send them).

One data question resolved by the user directly: "the Diablos are the
Devils" — confirmed against `FRANCHISE_TIMELINE`, whose only recorded era for
Gleason Diablos is `{from:2013,to:2014,nick:'Devils'}`, so the Diablos
leadership entry is keyed to `Gleason Diablos` and renders "Played as Gleason
Devils (2013–2014)" on the bare page.

Verified: all 20 franchise pages render a Leadership block with correctly
linked/plain-text names; Franchise Summary and Franchise Name History both
link through to all 6 historical pages; no console errors on any page
checked.

## Streaks on the Records page

Added a "Streaks" section to Records: team winning/losing streaks, and player
hitting streaks, alongside the existing Single-Season/Single-Game/No-Hitters
sections. Like No-Hitters, this section ignores the era toggle (a streak
spanning an era boundary would be understated if filtered).

**Team win/loss streaks** — built from each franchise's own game log
(`TEAMS[..].seasons[y].games`, unified across name changes already), which
carries the league's official W/L result independent of individual box
scores, so unlike hitting streaks this needed no per-game-logging-quality
caveat. Top 10 winning and top 10 losing streaks, regular season.

**Player hitting streaks** — consecutive regular-season games with a hit,
using `collectPlayerGames()` (the same source as a player's own Game Log
tab), restricted to games with an individual batting line recorded, 2020 on
— the same "per-game lines where recorded (2020 on)" reliability boundary
already documented elsewhere on the site. A game the player didn't bat in is
skipped rather than treated as breaking the streak (pitched-only appearance,
etc.), matching standard hitting-streak convention.

**Bug caught during testing, fixed before publishing**: the first version let
both streak types run straight across season boundaries with no reset. Since
this is a summer league with a long off-season — and some franchises go
dormant for years at a stretch (Harris Kings fielded no team 2022–2025) —
this produced badly misleading entries: a "24-game losing streak" for the
Kings spanning 2020 to 2026 (almost entirely a 4-year gap where the team
didn't exist), and a defunct franchise's last-ever recorded game (Brentwood
Mustangs, folded 2018) tagged "ongoing" simply because no later game existed
to break it. Fixed by resetting the streak walk at every season (year)
boundary for both team and player streaks, and by gating the "ongoing" tag on
the streak's final game actually falling in `LATEST_YEAR` (the site's current
season) rather than just being the last game in that entity's own history.
Re-verified after the fix: no cross-year spans in the top 10 of either list,
and "ongoing" no longer appears on any stale/defunct-team entry.

## Home run and on-base streaks

Extended the player streak logic to two more per-game conditions, alongside
hitting streaks. Refactored the hit-streak computation into `playerStreaks(hit)`,
which takes a predicate over a game's bat line — `Hitting` uses `b.h>0`,
`Home Run` uses `b.hr>0`, `On-Base` uses `b.h>0 || b.bb>0 || b.hbp>0` — and a
shared `streakList(title, streaks)` builds each `llist()` block from the
result. Same season-boundary reset, 2020-on per-game-data restriction, and
`LATEST_YEAR`-gated "ongoing" tag as hitting streaks, since all three share
every other rule.

Verified: On-Base streaks top out at 15 (a full season) for several players —
expected, not a bug, since reaching base is a low bar in this league and a
15-game regular season is common; no console errors, links to both players
and games resolve correctly.

## Streaks: era toggle, and excluding forfeit-batch games

Two follow-ups from the user after reviewing the Streaks section.

**Era toggle now applies to Streaks.** Originally built to ignore the era
chip (like No-Hitters, on the theory that a boundary mid-streak would
understate it) — the user asked for it to be filtered like the rest of the
page instead. Team streaks now filter each season by `inEra(+y)` before
building the game list; player streaks add `inEra(...)` to the existing
`>=2020` filter on `collectPlayerGames`.

**Forfeit games no longer count toward team win/loss streaks.** The user
noticed some streaks looked like data artifacts: "if a win streak or losing
streak happened all on one day and/or happened by the same scores, it was
forfeits." Investigating confirmed it exactly — e.g. Harris Kings were
credited with sixteen 0–6 losses on a single day in 2019-08-12, every one
with an empty box score (`bat: []`, `pit: []` on both sides) and a zeroed
line score despite a nonzero run total. A normal day tops out at 3 games for
a team (216 of 320 team-days); the forfeit-processing days ran as high as 21.

Checked whether "no individual box score" alone could identify these —
it can't: 2017–19 "thin" games (a known, documented site limitation) use the
exact same empty-bat/zeroed-line shape for perfectly real games, so that
signal alone flagged 108 games, far more than the actual forfeit batches.
Landed on: a `(team, date)` is a forfeit batch when it has 4+ games **and**
one score accounts for a strict majority of them. Verified against every
4+-games-in-a-day case in the data (`per_day` counts, `Counter` on `(rf,ra)`)
— this cleanly separated 15 confirmed forfeit dates (50–100% score dominance)
from 7 genuine high-volume days where every score differs (Brookside Kraken's
real 6-game 2023-07-24, for instance, tops out at 33%).

Also mattered: filtering at the **game** level, not the whole streak. Beaver
Brook Lavahogs had 6 forfeit games against Harris Kings on 2019-08-12
followed immediately by 1 real win on 2019-08-13 — all logged as one
"7-game" streak. Rejecting a streak only when *every* game in it looked
like a forfeit (my first pass) missed this case, since the mix of scores
across the 7 games meant it didn't uniformly qualify. `dropForfeitDays()`
removes the flagged dates' games from a team's game list *before* the streak
walk runs, so the real 08-13 game is correctly left standing on its own
(too short to rank in the top 10) instead of inheriting a fake 7-game credit.

Re-verified: every previously-inflated entry (Purchase PawSox 24-loss,
Brentwood Mustangs 19-loss, Harris Kings' forfeit-day appearances, the
Lavahogs 7-win) is gone from both lists; legitimate streaks (Brookside
Kraken's real runs, etc.) moved up to fill the top 10; the era toggle
correctly narrows the Streaks section now; no console errors.

## Data fix: Mathew Wilkins is actually Matthew Rosmarin

Renamed a single player record (`players.json`, direct edit, no generate.py
change) — this was a plain rename, not a merge like the Sabino case earlier
(confirmed no existing "Matthew Rosmarin" record to conflict with first).
Renamed the `players` dict key, the 2 box-score `bat`/`pit` line `n` fields
in `games`, and the 1 `TEAMS['Glenwood Process'].seasons['2017'].roster`
entry; a recursive scan of `champs`/`awards`/`asg`/`noHitters`/`divisions`/
`beavers`/`playoffs`/`leadership` found no other stray references.

Caught one thing the recursive scan's key list didn't cover: the player
record itself carries its own `name` field (`players[key].name`), separate
from the dict key — missed on the first pass, caught by grepping the whole
file for the old name afterward and finding one leftover hit. Fixed
separately. Worth remembering for the next player rename/merge: grep the
whole file for the old name at the end, don't just trust the scan of the
sibling top-level structures.

## Playoff bracket scores link to their box scores

The playoff bracket (`playoffBracket()`, shown on the home page snapshot and
on Standings) showed each series' game-by-game scores as plain text — `p[side].series`
and `p.finalSeries` are just `[rf,ra]` tuples in the `playoffs` data, with no
game id attached, so there was nothing to link to directly.

Added `seriesGids(year, teamA, teamB)`: filters `GIDS` for `phase==='Playoffs'`,
the matching year, and both teams in the pair, sorted chronologically — since
a series' games are always listed in the order played, this lines up 1:1 with
the `series` array by position. `pbScore(games, gids)` now renders each score
as a `data-g` button linking to that game's box score when the counts match,
falling back to the original plain text otherwise (a safety net for a
hypothetical year with thinner box-score data than its series summary —
not needed in practice, see below). Wired both call sites (`semi()` for the
two division series, and the Final) with the right team pairs.

Also had to add `.pname[data-g]` click wiring to `renderStandings()` — it
never needed it before (nothing there linked to a box score), so its handler
list was missing the one every other page that shows game links already has.

Verified: every single playoff series score across all 10 seasons on record
(2017–2026, standings + home page) resolved to a real, correctly-matched box
score — no plain-text fallback needed anywhere in practice. Spot-checked
individual scores against their box scores directly (e.g. bracket's "10–6"
Panthers-over-Process 2017 game matches gid 24174118's actual line). Styled
the linked scores to keep the bracket's existing muted look (underline,
inherit color/size) rather than switching to the site's usual bold accent-
colored link, so a compact "2–0 · 0–1 · 10–2" score line doesn't turn
visually noisy. No console errors on any year checked.

## Playoff bracket scores: labeled "Game 1", "Game 2", ...

Quick follow-up to the box-score-linking work above — `pbScore()` now
prefixes each score with its game number in the series (`Game 1: 2–0 ·
Game 2: 0–1 · Game 3: 10–2`) instead of just the bare scores, on both the
linked and plain-text-fallback paths. No layout issues: `.pb-match` already
wraps text within its fixed width rather than forcing a scrollbar, so the
longer strings just wrap onto a second line inside the bracket card.

## Playoff bracket: show each game's winner

Follow-up to the "Game 1/2/3" labeling — the user asked to show which team
actually won each game, not just the score.

First pass got this wrong and needed a second look. My first instinct was to
read the winner off the raw `[scoreA,scoreB]` tuple's own order, assuming it
consistently matched a fixed side (seeds[0]/seeds[1] for a division series,
the two round-1 winners for the Final). Cross-checking several years against
the *actual* box scores (not just trusting the summary data) found this
assumption was wrong for the Final specifically: 2018/2019/2020/2022/2023/
2024/2026 all list the "brentwood"-bracket-side score first, but 2021 lists
"brookside" first — there's no consistent rule, so a label built on that
assumption would have been confidently wrong roughly as often as right.

Fixed by never trusting the tuple's order for identity — only its two
numbers, shown as-is like before. The winner is instead read off the real,
already-matched `GAMES[gid]` entry from the earlier box-score-linking work
(`away.R` vs `home.R` tells you definitively who won that specific game).
This only works when the score was successfully linked to a game id, so the
(currently never-hit) plain-text fallback path shows no winner rather than
risk repeating the same mistake with a guess.

Verified exhaustively this time, not just spot-checked: wrote a script that
walks every playoff series across all 10 seasons (30 series, every game) and
compares the displayed winner against the authoritative `away.R`/`home.R`
in `GAMES` for that exact matched gid — zero mismatches. Lesson for next
time: when a stored summary field's internal ordering isn't explicitly
documented, verify it against several years of ground truth before building
on it, not just one clean-looking example.

## No-hitter date corrections: 2 games newly linked

The user corrected the source no-hitter/perfect-game dates and gave the full
38-row list back in chat (not a new CSV to rerun through `build.py`). Diffed
it line-by-line against the current `players.json.noHitters` array; every
row matched except two, both of which were previously *unlinked* (`gid:
null`) — makes sense in hindsight, since the wrong date is exactly why the
original gid-matching in `build.py` failed to find them:

- Justin Nardo, Brentwood Bananas @ Shelton Shock: 2023-07-18 → 2023-07-17
- Anthony Pasqua, Downtown Titans vs Silver Lake Snapping Turtles:
  2025-07-04 → 2025-07-03

Searched `games` for that exact date + team pair and found the box score for
each — confirmed beyond just date/teams by matching the stored no-hitter's
IP/BB/K against the real pitching line (Nardo: 15 outs/2 BB/11 K, 0 hits
allowed; Pasqua: 9 outs/3 BB/9 K, 0 hits allowed — both exact matches).
Updated `date`, `dateDisplay`, and `gid` directly in `players.json` for both
rows (gids 29900356 and 31199965) and re-sorted the array the same way
`build.py` does. The remaining pre-2017 entries stay unlinked, same as
before — no box-score data exists for that era regardless of date accuracy.

## Data fix: 2026 NWLA National Tournament location

Was recorded as "Harrison, NY"; corrected to "St. Louis, MO" per the user.
Fixed in all three places it's kept: the source module (`beavers_2026.py`,
both the header comment and `meta.location`), its companion notes file
(`beavers_2026.md`), and `players.json` directly (same reasoning as every
other data-only fix this session — editing the served file directly rather
than rerunning `build.py`, which would overwrite this session's other
hand-patches that have no CSV/source-module backing).

## Playoff bracket: uniform box sizes

The "Game 1/2/3 (Winner)" score labels added this session made the two semi
boxes stretch to fit their longest line on one line (up to 478px, vs. the
World Series box's 282px) instead of wrapping, because `.pb-match` only ever
had a `min-width` and nothing capping it — with the horizontally-scrollable
`.pbwrap` around it, a block with no max-width just grows to avoid wrapping
rather than actually wrapping. Every bracket box across a year now looked a
different size depending on how long that particular series' score line was.

Fixed by switching `.pb-match` from `min-width:236px` to a fixed
`width:260px` (`flex:none` so the flex column doesn't stretch it further),
which forces the score text to wrap within the box instead of growing it.
236px turned out too narrow on its own — checked every bracket box's actual
content width across all 10 seasons and found real clipping risk on longer
team names (`white-space:nowrap` on `.pb-row`, combined with the existing
`overflow:hidden`, would have silently cut them off): "Beaver Brook
Lavahogs" needed 248px against 236px's ~234px usable width, with two
"Brentwood Gladiators" rows also just over. Set the fixed width to 260px,
comfortably above that measured max, and reconfirmed zero overflow anywhere
in the same all-years sweep. Every bracket box (both semis and the Final,
every season) now renders at an identical 260px.

## Playoff bracket: game labels always stacked

Quick follow-up — the per-game "Game 1: 2–0 (Panthers)" labels were joined
with " · " and left to wrap on their own within the fixed-width box, which
meant a 2-game series read as one tidy line while a 3-game series wrapped
essentially at random depending on label length. Changed `pbScore()` to wrap
each game in its own `.pb-score-row` block (dropped the " · " separator,
now redundant) so every series — 1, 2, or 3 games — always shows one game
per line. No console errors; boxes stay the same uniform 260px width from
the sizing fix above.

## Players page: normal name order, except the A–Z tab

The Players page's Stats tab was showing names as "Last, First" (`nameLF()`)
in its name column, same as the A–Z tab. The user asked for normal "First
Last" order, keeping "Last, First" only where it belongs — the A–Z index,
which is organized by surname and reads naturally that way (like a roster).

Changed the Stats table's name cell from `nameLF(r.name)` to plain
`r.name`; left the A–Z tab's `nameLF(n)` untouched. Sorting is unaffected
either way — the Stats table's name-column sort already sorted by last name
via `nameLast()` independent of what text was displayed, and the A–Z tab was
already grouped by last-name initial.

## Outstanding work

**2016 integration** — blocked on a name+team mapping from the user for these
first-name-only players: BOB, Will, Darien, Chris, Ava, Jake, Tristan, James,
Donne, Tochi, Michael, Daniel, Dean, Landon, Mike, Vito.
When received: add lines to `MAP_2016` in `data_2016.py`, flip `INCLUDE_2016 = True`
in `build.py`, rebuild. No other code change needed. 11 confident maps are already in `data_2016.py`.

## Full context

The persistent memory note `bwb-career-register.md` (loaded automatically in any new
Claude Code session for this user) has the complete history: data quirks, the
team-inference method, 2017 first-name fixes, stat semantics (3-inning games,
ERA per 3 IP), division alignment, multi-team split rows, etc.
