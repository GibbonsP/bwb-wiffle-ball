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

## Home Run Derby champion added to player Accolades

HR Derby winners only lived on the year-by-year All-Star Game record
(`ASG[year].hrd`), not in any player's `honors.awards` — so a Derby title
never showed up on the winner's own profile page, only buried in the
All-Star Games section. Built `HRD_BY_PLAYER` (a name → years lookup) once
from `ASG` at module load, and merge it straight into `accolades()`'s
existing award-grouping (`grp`) as a normal "Home Run Derby Champion" tile —
same styling, same ×N-years treatment as MVP/Cy Young/etc., added to
`AW_ORDER` right after Home Run King. `totAw` (the "N Awards" header count)
now sums `grp`'s bucket lengths instead of just `h.awards.length`, so it
counts Derby titles too. Verified against all 7 real winners in the data
(Fraioli ×3, Wilkins ×3, Spoto ×2, plus four single winners) — every one
shows the right year(s) on their own page now.

## Brookside Beavers text linked to the Beavers page

The player-profile NWLA tab's Game Log note ("From the Brookside Beavers'
NWLA tournament box scores...") had "Brookside Beavers" as plain text — the
only other places that name appears in `generate.py` are the Beavers page
itself, which doesn't need to link to itself. Made it a real link: added a
bare `data-beavers` marker (no value needed, unlike `data-t`/`data-g`/
`data-bv` which carry an id) and a matching delegated click handler in
`detail()`'s listener block that navigates to `#/beavers`. Verified the
click actually lands on the Beavers page from a player's NWLA tab.

## Player profile: Stats/Splits/Game Log split into their own tabs

Each phase tab (Regular Season, Postseason, All-Star Games, Spring Training,
Fall Ball, NWLA Tournament) used to concatenate its season-by-season stats
table, Splits breakdown, and Game Log into one long stacked scroll. Asked the
user whether splitting them into their own nested tabs was worth doing given
the extra click it costs; they agreed, so added a second-level tab bar
(Stats / Splits / Game Log) under the existing phase tab bar.

`phaseTab(t)` now returns `{stats, splits, log}` separately instead of one
concatenated string (or `{none: html}` for the "no postseason on record"
case, which still shows with no sub-tabs — there's nothing to divide).
The phase-tab-bar's own filter (hide a phase with nothing at all) now checks
all three pieces combined rather than one merged string. A new `playerSubView`
state (`'stats'|'splits'|'log'`, alongside the existing `playerTab`) picks
which piece renders; the sub-tab bar only lists views that actually have
content for the current phase, and falls back to the first available one if
the current selection doesn't apply (same fallback pattern already used for
`playerTab` itself). `playerSubView` persists across phase switches by
design — if you're looking at Splits and click over to Postseason, you
probably still want Splits, not to be dropped back to Stats.

New CSS `.subtabs2` reuses `.subtabs`'s structure at a smaller size/tighter
spacing so the hierarchy between "which phase" and "which view" reads
clearly at a glance.

Verified two ways: every one of a player's own view/phase clicks lands on
the right content (spot-checked via the actual buttons, not just state
changes), and a full sweep — all 96 players × 6 phases × 3 views (1,728
renders) — threw zero errors. Also checked the whole dataset for a phase
with only 1 or 2 of the three pieces non-empty (which would exercise the
"hide the empty view tabs" branch): none exist today — every phase with any
content has all three — so that branch is correct but currently dormant;
kept it in since a future thin dataset (an exhibition phase with stats but
no logged games, say) would need it.

## Beavers link, part 2: the actual gap was the NWLA stats table

The earlier "link Brookside Beavers" fix only covered one spot (the NWLA
Game Log's note paragraph); the user pointed out it still wasn't linked
elsewhere. The real remaining gap was `teamCell()` — the "Tm" column
formatter used by every phase's season-by-season stats table (`phaseBlock`).
It only knew how to link a real `TEAMS[...]` entry; "Brookside Beavers" isn't
one (it's tracked separately under `DB.beavers`, never `DB.teams`), so it
fell through to plain escaped text on the NWLA Stats tab specifically —
exactly the tab most people would actually look at. Added a second
special case to `teamCell()`: if the team string is literally "Brookside
Beavers", render the same `data-beavers` button the earlier fix introduced
(reusing its existing click wiring in `detail()`) instead of plain text.
Verified on the NWLA season-table row, not just the Game Log note this time.

## All-Star Team Captain History on division pages

Added a new section to each division page listing who captained that
division's All-Star squad every year — data that already existed (a
"(C)" marker inline in `ASG[year].squads[].players`, the same field the
per-game roster listing already reads) but had never been surfaced as its
own history list. `asgCaptainFor(y)` picks that year's marked name out of
the squad roster; rendered via the existing `plink()` helper (already
handles the "(C)" marker, name aliases, and linking) into a new "All-Star
Team Captain History" block, placed between "All-Star Game History" and
"All-Star Game Stats". No data changes — every year back to 2013 already
had this in the ASG roster data on both the Brookside and Brentwood pages.

## Percentile Rankings: dropped OPS, kept OPS+

User's reasoning: OPS+ already accounts for league average (that's the
entire point of the stat), making it strictly more informative than raw OPS
in a percentile-ranking context where every other stat is already being
compared against the field. Removed the `SV_BAT` entry for OPS;
OPS+ stays.

## All-Star Game MVP added to accolades, and a data fix

Same pattern as the Home Run Derby Champion addition: `ASGMVP_BY_PLAYER`
built from `ASG[year].mvp` at load time, merged into `accolades()`'s award
grouping as "All-Star Game MVP" (added to `AW_ORDER` right after Postseason
MVP). Handles a co-MVP tie the same way `plink()`/`tnick()` already handle
multi-name fields elsewhere: split the stored value on "/".

That co-MVP case is exactly why this needed a data fix first: 2024's `mvp`
field read `"TJC/James Duffy"` — shorthand, not the two players' actual
register names ("TJ Ciafone" and "James Duffelmeyer"), per the user. Fixed
directly in `players.json` to `"TJ Ciafone/James Duffelmeyer"`, which also
fixes the existing All-Star Games page display (`awardsSection()`'s
`plink(a.mvp)` call) — it had been rendering the shorthand as unlinked
plain text since neither name matched a real player key. Verified both
names now show as separate linked players on the Awards page's All-Star
Games tab, and both players' own profiles show "All-Star Game MVP · 2024".

## New exhibition game: the Brookside Field Finale

Added a one-off exhibition game — All-Time Panthers vs. All-Time Kraken,
2026-04-11 at Brookside Field — as a full new phase, not a Beavers-style
bolt-on. Transcribed and verified against the source box score
(mystatsonline.com, IDGame=1888619): every player's batting/pitching line
cross-checked against that team's printed totals (AB, R, H, HR, RBI, BB, K
for batting; H, R, ER, BB, K for pitching) before writing anything — all
reconciled exactly.

Chose to model this as a real `GAMES` entry (`gid: 1888619`, `phase:
'Exhib'`) rather than a parallel data source like the Beavers, since unlike
the Beavers' separate GameChanger export, this is a single normal-shaped box
score that fits the existing schema exactly — doing it this way means
`collectPlayerGames`/`playerGameLog`/`playerSplits`/`boxScore` all handle it
for free, no new rendering code needed beyond registering the phase itself:

- `SEASON_TYPES` and `PHASE_META` gained an `Exhib` entry (`head:'Brookside
  Field Finale'`), and the player-profile tab order now reads Regular →
  Playoffs → All-Star → Spring → Fall → **Exhib** → NWLA, per the user's
  requested placement.
- `phLabel()` maps `Exhib` → "Exhibition" for the small phase-tag badge
  (games list, etc.), matching how `AllStar` already maps to "All-Star".
- Added one `Exhib`-type season row per player to `players.json` (12
  players total — 6 per side, all already-registered players), plus the
  `GAMES` entry itself, via a script that asserted each side's per-player
  lines summed to that side's actual final line-score totals before writing
  anything.
- "All-Time Panthers" / "All-Time Kraken" are plain strings, not `TEAMS`
  entries — exactly like "Brookside Beavers" before it was special-cased,
  every existing team-name formatter (`teamCell`, `histTeamLink`, etc.)
  already falls back to plain unlinked text for an unknown team, so this
  needed no new code to satisfy "they don't need team pages." Confirmed on
  the Games list: the date is a link, the team names are not.

Because it's tagged `phase: 'Exhib'` (not `'Regular'`), it's automatically
excluded from things that should stay real-season-only: team win/loss
streaks, single-game Records leaderboards, and the forfeit-day detector —
none of those needed to change, they simply never look at this phase.

Verified: all 12 players' Stats/Splits/Game Log sub-tabs render with zero
errors; the two batting-only players (Peter Sposato, Austin Corvino)
correctly show no Pitching table; the box score page's line score, R/H/E,
and every batting/pitching line matches the source exactly; the Games list
shows the game with an "Exhibition" tag and unlinked team names.

## Exhibition tab: generic label, event name shown as context

Follow-up correction: the new phase's tab/heading was showing "Brookside
Field Finale" directly, but the user wanted the tab itself generic
("Exhibition" — matching the pattern of every other phase tab being a
category, not a specific event name) with the actual event named as context
underneath, since this phase is meant to hold whatever one-off exhibition
games come along later, not just this one.

`PHASE_META.Exhib.head` changed to `'Exhibition'`. Rather than hardcode
"Brookside Field Finale" into the subtitle (which would be wrong the moment
a second, differently-named event gets added), `phaseBlock()` now derives
the event name(s) straight from that phase's actual games — reading the
`div` field already on each game (`collectPlayerGames(pl, 'Exhib').map(r=>
r.g.div)`, deduped, year-prefix stripped since the year already shows
separately). Subtitle now reads "1 appearance · 2026 · Brookside Field
Finale" — generic label, specific event named from the data, and correct
automatically if a differently-named second event shows up next year.

## Team page: Season by Season redesign, Franchise Roster split

**Season by Season** (`teamRecordTable`) column order changed to Year, Name,
Division, W, L, PCT, Result, Finish, RF, RA, Diff, per the user's exact
spec. Removed: Ros (roster count) and the old raw "Playoffs" W–L column,
replaced by the new narrative Result column; the combined "W–L" mono column
also split into separate W and L columns.

Three new columns, all computed from data already on hand — nothing new
added to `players.json`:

- **Division**: `divisionOf(name, y)` finds which key in `DB.divisions[y]`
  lists this team. Shows the division's own era-accurate name for that year
  directly (`DB.divisions` is already keyed "North"/"South" pre-2021,
  "Brookside"/"Brentwood" from 2021 on) — no canonicalizing needed. Caught a
  genuine historical quirk while testing, not a bug: Brookside Panthers are
  filed under the "Brentwood" division key in 2023 in the source data, since
  (per an existing code comment) these are fixed bracket-position labels,
  not geography. The column correctly surfaces that instead of hiding it.
- **Finish**: `divisionFinish(name, y, dn)` reruns that division's own
  standings sort (PCT, then head-to-head, then run differential — the exact
  comparator `renderDivision` uses) and reports this team's rank as an
  ordinal (1st/2nd/3rd/...).
- **Result**: `playoffResultFor(name, y)` — `DNQ` if the team isn't in
  either side's seeds that year; `LOST WC` or `LOST DS` (year ≥2025 → DS,
  matching the user's note that the first round was always a single
  winner-take-all game before 2025, so there's no score to show) if they
  lost round one; otherwise `WON WS`/`LOST WS` with a real series score.
  That score — same lesson as the bracket work earlier this session — is
  counted from the actual matched box scores via the existing `seriesGids`
  helper, never read off `PLAYOFFS[y].finalSeries`'s own tuple order (proven
  unreliable then, so never trusted here either). Falls back to no score
  (just "WON WS") on the one year (2017) where no box score for the Final
  exists to count — same "don't fabricate a number" rule as everywhere else.

**Franchise Roster** (`teamAllYears`) split into "Franchise Roster ·
Hitting" and "Franchise Roster · Pitching" instead of one table with both
sets of columns side by side — matches the Batting/Pitching split already
used in every other stat table on the site (`phaseBlock`,
`teamStatsBySeason`). Each table now only lists players relevant to it
(`PA>0` / `IPouts>0`), and the pitching table sorts by innings pitched
rather than inheriting the batting table's PA sort.

Verified: all 15 franchises with a real team page render both new sections
with zero errors; spot-checked several teams' Division/Finish/Result values
against the underlying `DB.divisions`/`PLAYOFFS`/`GAMES` data directly
(2026 Panthers "LOST WS 2-0" matches the Shock sweep confirmed earlier this
session); Career total row correctly leaves Division/Result/Finish blank
rather than showing a meaningless aggregate.

## Season by Season: Home/Away and vs-division records, with PCT

User asked for Home/Away and Brookside-vs-Brentwood records added, each
with its own winning percentage, then asked directly whether it would all
fit. It would not, as separate columns — Home alone would need 3 (W, L,
PCT), ×4 record types = up to 12 new columns on top of the 11 already
there. Fit it by combining each record into one cell instead: `fmtSplit(w,l)`
renders `"10–1 (.909)"`, W-L primary and PCT muted/parenthetical — same
idea as the site's existing combined "W–L" cells (Home/Away already render
this way on the Standings page), just with PCT folded in. That kept it to
4 new columns (Home, Away, vs Brookside, vs Brentwood) instead of up to 12.

"Brookside vs Brentwood" specifically (not "vs North/South" pre-2021) was a
deliberate choice, not just copying the Standings page's own per-division
columns: this table spans every year in one place, both eras, so the column
*headers* have to be fixed — `vsCanonicalRecord()` looks up each
opponent's division for that specific year and folds it through
`canonicalDivision()` (North→Brookside, South→Brentwood, the same mapping
the site already uses to treat 2012's North/South as one continuous
division under two names) before bucketing the W/L. A 2018 opponent from
"North" and a 2023 opponent from "Brookside" land in the same column
correctly.

Home/Away comes straight off `standRow()`'s own hW/hL/aW/aL, already
computed for the Standings page. Career-row totals for all four new columns
are accumulated across years in the same loop that builds each season's row,
rather than a second pass.

Verified by reconciling every direction the numbers can be checked against
each other for the 2017 Panthers and their career totals: Home+Away game
counts equal the season's overall total, vs Brookside + vs Brentwood game
counts also equal that same total, and both pairs' summed W/L match the
season's overall W/L exactly — true for both the single 2017 row and the
full career row (177 games either way summed). All 15 real team pages
render with zero console errors.

## Playoff series pages, Finish format, Playoffs column rename

Three related asks in one turn.

**Finish**: `divisionFinish()` now returns `"1st of 3"` instead of just
`"1st"` — the division's own team count for that year appended, so the
number means something without cross-referencing the standings.

**Result → Playoffs**: renamed the column header only; the underlying
`playoffResultFor()` data/logic is unchanged.

**New playoff series pages** (`renderSeries(year, roundKey)`, routed at
`#/series/<year>/<brookside|brentwood|final>`), modeled on
baseball-reference's postseason series pages: every game in that series and
each side's combined batting/pitching across just those games. The
`roundKey` values are deliberately the same three keys `playoffResultFor()`
already computes internally (`'brookside'`/`'brentwood'` for a round-1 exit,
`'final'` for anything that reached the World Series) — that function now
returns `{label, seriesKey}` instead of a bare string, so the Playoffs
column's cell can link straight to the right series with no re-deriving of
which round it was. `DNQ` and years/entries with no series naturally get
`seriesKey: null` and render as plain unlinked text, so "no link for a team
that didn't qualify" falls out of the existing logic rather than needing a
special case.

Stats reuse `rosterBatting`/`rosterPitching` (already built for the
division All-Star pages) fed a roster built by summing just that series'
own `gameBatRow`/`gamePitRow` lines per player — the exact same aggregation
shape, just scoped to a handful of games instead of a whole division-year.
OPS+ uses `post:true` (postseason league baseline for that year), matching
how every other postseason OPS+ figure on the site is computed.

One gap found in testing, not a crash but a bad user experience: a series
with no matched box scores (2017-era games, before per-game logging) was
silently bouncing the click back to Standings with zero explanation. Fixed
by keeping the user on the series page and showing what the bracket data
*does* know — both teams, who won — with a note that no box scores exist
for that era, matching the "show what we know, say what we don't" pattern
used for the Postseason tab's own empty state.

Verified exhaustively: all 10 years × 3 round keys (30 series) render with
zero errors, including the no-box-score 2017 case landing on its new
fallback message instead of redirecting away. Clicked through for real
(not just programmatically) from the Panthers' 2025 "WON WS 2-1" cell —
landed on a page showing the correct 3 games (3–0, 0–5, 1–0 over the
Kraken), which also lines up with a no-hitter already on record this
session (TJ Ciafone's Game 2 shutout "to force Game 3").

## Playoff series pages: game boxes instead of linked lines

User shared a baseball-reference-style game-result card (team names, score,
W/L/S pitchers) and asked for that instead of the plain linked-line list the
series pages launched with — scoped explicitly to the playoff series pages
only, not the Beavers page's own separate game cards or anything else.

Each game is now its own `.pb-match` card (reusing the exact classes the
playoff bracket already uses, so it's visually consistent with the rest of
the site rather than a one-off style): a header with game number and date,
a `.pb-row` per team with logo, name, and that game's own run total —
highlighted via the bracket's existing `.pb-row.win` treatment — then a
decisions section listing **W**/**L**/**S** with the actual pitcher(s) who
recorded them that game, and a "Box score →" link. Cards lay out in a
wrapping flex row (new `.game-cards` class) so a 2-or-3-game series reads
as a short row of cards rather than a tall stack.

Decisions come straight off each game's own pitching lines — whichever
pitcher(s), from either side, actually carry `w>0`/`l>0`/`sv>0` for that
specific game (`decisionsFor(g)`); skipped the "(1-0)" running-record
parenthetical real box scores show next to each name, since computing a
pitcher's correct record as-of that exact date would need its own
chronological pass — noting it here in case it's wanted later, but out of
scope for "show it as boxes."

Verified: all 10 years × 3 round keys re-render with zero errors after the
change; spot-checked the 2025 World Series (Panthers over Kraken, 2-1) —
each card's teams, scores, win highlight, and W/L pitcher both link and
match the actual box score; confirmed the Beavers page (which has its own
separate, unrelated game-card renderer) was untouched.

## Running (W-L)/SV record next to each decision

Follow-up to the game-box cards: added the "(1-0)" running record real box
scores show next to each W/L, and a plain save count like "(4)" next to SV
— the piece explicitly skipped last time as needing its own chronological
pass. `pitcherPostseasonTally(name)` builds exactly that pass: every one of
that pitcher's Playoffs-phase games *for that year* (via the same
`collectPlayerGames` used everywhere else on the site), sorted
chronologically, walked once to build a `gid → {w,l,sv}` running-total map.
Scoped to that single year's postseason, not regular season or career —
matches how a real postseason record actually resets each October, and how
a team's own two rounds (round-1 + potentially the Final) share one running
tally, not two independent ones. Cached per pitcher per page since the same
starter/closer often appears in multiple games in the same series.

Verified by hand against the raw game data, not just re-reading my own
output: pulled every one of Peter Fraioli's and TJ Ciafone's 2025 Playoffs
pitching lines directly from `players.json` in date order and recomputed
their running W-L myself — matched the page exactly at every step,
including a case where the record entering a series' Game 1 already
reflected 2 decisions from an earlier round-1 series that same postseason
(Fraioli: "(3-0)" after Game 1, not "(1-0)", because he'd already picked up
2 wins in the round before it). Also found and confirmed a real save case
(Evan Wilkins, 2020 World Series Game 2) renders "S Evan Wilkins (1)"
correctly. Full 30-series sweep still zero errors after the change.

## Game card formatting fixes

User caught two real layout bugs after the running-record change.

**Score misalignment**: the winning team's score wasn't lining up with the
losing team's, because the winning row's `.pb-row.win::after` arrow
(inherited from the original bracket styling, where it means "advanced")
sits *after* the score and also claims `margin-left:auto` — competing with
the score's own auto margin and shoving it left of where the loser's score
sits. Since the user also said the arrow wasn't wanted here, removed it with
a scoped override (`.game-cards .pb-row.win::after{content:none}`) rather
than touching `.pb-row.win` globally — the original bracket display
(Standings/home page) still gets its arrow, confirmed unaffected.

**Decision rows wrapping onto 3 lines**: "W", the pitcher's name, and their
"(3-0)" record were each landing on their own line instead of reading as
one line. Root cause: `.pb-score button.pname{display:block}`, written for
the *previous* single-link-per-game design (back when the whole card was
one clickable line) and never scoped down when the cards gained multiple
buttons per card (box score link + a linked name per decision). Fixed by
moving `display:block` to a new `.pb-boxlink` class applied only to the
"Box score →" button, and giving `.pb-score-row` its own
`display:flex;align-items:baseline;gap:5px` so W/L/S rows lay out inline
correctly by construction rather than by accident.

Verified visually this time, not just via DOM queries — screenshotted the
2025 World Series page before and after: scores now sit flush on the same
right edge on both the winning and losing row in every card, no arrow, and
every decision reads as one line ("W Peter Fraioli (3-0)"). Re-ran the full
30-series sweep (zero errors) and confirmed the original bracket's own win
arrow on Standings/home still renders exactly as before.

## Playoff bracket links to the series pages too

The series pages were only reachable from a team's own Season by Season
Playoffs column. User asked for the bracket itself (shown on the home page
snapshot and the Standings page) to link there too.

Added a "Full series →" row inside each bracket match's existing `.pb-score`
box (`pbScore()` gained an optional `seriesKey` param that appends this row
using the same `data-series` pattern the team-page link already uses) —
`'brookside'`/`'brentwood'` for each semi, `'final'` for the World Series
box, matching `renderSeries()`'s own routing exactly. Since `playoffBracket()`
itself is shared by two different pages (`renderHome()` and
`renderStandings()`), the `.pname[data-series]` click handler had to be
added to both pages' own listener blocks, not just one.

Verified: both the home page snapshot and Standings show all three "Full
series →" links per year with the correct year/round encoded; clicked one
through end-to-end to the right series page; re-ran the full bracket ×
series sweep across all 10 years with zero errors.

## Percentile Rankings: faded estimate below qualification

Previously a player under the qualification bar (9+ G batting, 12+ IP
pitching) got nothing at all for that season — "No qualified regular
season." User wanted an estimate shown anyway down to a much lower floor
(3+ G batting, 3+ IP pitching), visually marked as unofficial, and — the
important constraint — without that player joining the comparison pool
itself and skewing everyone else's percentile.

That constraint fell out almost for free from how the pool was already
built: `qb`/`qp` are filtered by the real `SV_MING`/`SV_MINOUTS` bar, which
an unqualified subject by definition doesn't clear — so plotting their
percentile *against* `qb`/`qp` unchanged, without adding them to it, was
just a matter of calling `svPct()`/`svPanel()` on a subject that isn't part
of the array it's being measured against. Added `SV_MIN_SHOW_G = 3` /
`SV_MIN_SHOW_OUTS = 9` (3 innings) as the new floor just for *displaying*
an estimate; `svPanel()` takes an `unqualified` flag that tags the panel
title ("est. · unqualified") and every row with a new `.svunq` class.
Verified directly: pulled the qualified pool for Alex Homem's 2020 season
(3 games, well under the 9-game bar) and confirmed his own row was not a
member of the 13-player pool his estimate was plotted against.

Faded/patterned per the user's own suggestion: `.svrow.svunq{opacity:.5}`
for the fade, a dashed 2px border on the percentile dot, and a diagonal
hatch pattern layered onto the bar track's existing color gradient (multiple
`background` layers, hatch on top) — all scoped so a fully-qualified
player's panel (checked Peter Fraioli) picks up none of it. A season below
even the 3/3 floor still shows nothing, with the "not enough of a line to
estimate" message adjusted to reference the new, lower floor instead of the
qualification bar.

Verified across the whole roster: every player × every one of their
regular-season years (96 players) rendered with zero errors.

## Fixed: unqualified percentile bar line wasn't actually faded

Follow-up ask ("add faded lines too") turned out to be pointing at a real
bug in the first pass, not a missing feature. `.svrow.svunq .svbar::before`
set `background-image` directly to just the hatch pattern — since the base
bar's blue-grey-red scale was *also* set via the `background` shorthand (on
the plain, lower-specificity `.svbar::before` rule), the unqualified
override's higher-specificity `background-image` replaced it outright
instead of layering on top. The line for an unqualified row was rendering
as a bare white hatch with no color scale underneath at all — not faded,
just wrong.

Fixed by listing both background layers together in the override (hatch
pattern first, base gradient second — first-listed paints on top) and
adding an explicit `opacity:.55` on the bar itself, on top of the row's
existing `opacity:.5` fade, plus a small opacity reduction on the dot
(`.85`) for consistency. Verified via computed styles (not just re-reading
the CSS) that the fixed rule now resolves to both the hatch pattern *and*
the original gradient stacked together, and separately confirmed a
qualified player's bar (Peter Fraioli) still resolves to the plain,
full-strength gradient with no hatch and no extra opacity — the fix is
additive for unqualified rows only, nothing about the normal case changed.
Full 96-player sweep still zero errors.

## Records page split into tabs

The four sections (Single-Season, Single-Game, Streaks, No-Hitters &
Perfect Games) used to all render at once, stacked in one long scroll.
Split into tabs — same `subtabs`/`data-XX`/`aria-pressed` pattern already
used on the Awards page and player profiles — while keeping the era chips
working exactly as before.

New `recordsTab` state (alongside the existing `recordsEra`), a `tabs` array
of `[key, buttonLabel, heading, contentHTML]` built from the same
computations as before (nothing about *how* each section is computed
changed, only how much of the final markup gets shown), and a `data-rt`
click handler that swaps tabs without touching era state. Each section's
own content generation still runs on every render regardless of which tab
is active — the dataset is small enough that this costs nothing measurable,
and keeping it unconditional means the era chip's existing behavior (already
correct per-section, including No-Hitters staying deliberately unaffected
by era) needed no changes to keep working under tabs.

Verified: all 4 tabs show distinct, correctly-labeled content; switching
the era chip while on the Streaks tab stays on Streaks and actually changes
the numbers; the No-Hitters tab's content is provably identical between
"All Years" and "2022–2026 Era" (byte-identical length), confirming it's
still exempt from the era filter as intended. Swept all 12 tab × era
combinations programmatically — zero errors.

## New feature: Player Comparison tool

Added a head-to-head player comparison — pick two players, see their career
lines side by side, at `#/compare` (picker) and `#/compare/<A>/<B>` (the
actual comparison). Entry point is a "Compare Players →" button on the
Players directory's controls bar rather than a new top-level nav item (nav
already has 10 entries; this reads as a Players sub-feature, not a whole new
section).

**Picker**: two text inputs backed by a shared `<datalist>` of every player
name (same pattern already used for the team-name input in the season-row
editor), a "Compare →" button, and Enter-to-submit on either field. An
unrecognized name doesn't silently fail — shows "Couldn't find '{name}' —
pick a name from the list" and leaves the picker up so it's a one-character
fix, not a dead end.

**Comparison view**: Career Hitting (full slash line plus counting stats,
OPS+ injected as an extra row via `careerWeights`/`opsPlusFor` since it needs
each player's own year-by-year weighting, not just their raw career totals)
and Career Pitching — the latter only rendered if *either* player has any
IPouts at all, so a pure-hitter-vs-pure-hitter comparison doesn't show an
empty pitching table. An Accolades block (World Series rings, awards,
All-Star selections, All-Star Game MVP, HR Derby titles, no-hitters) reuses
the same lookups (`HRD_BY_PLAYER`, `ASGMVP_BY_PLAYER`, `NOHIT_BY_PITCHER`)
built earlier this session for the individual player-page accolades, so
nothing needed to be recomputed. Every row highlights whichever side is
better, with a `lowerBetter` flag per stat — batting K is fewer-is-better,
pitching K is more-is-better, same row label, opposite direction, both
correct in the same table.

Verified: cross-checked the actual highlighted winner and value against
known career lines (Fraioli vs Gibbons) for both the fewer-is-better and
more-is-better cases, including the two K rows landing on opposite winners
for exactly the reason they should; confirmed a real `IPouts=0`-but-
`G_pit>0` edge case (a token relief appearance with zero outs recorded)
renders ERA as "—" instead of a divide-by-zero artifact; swept all 96
players in sequential pairs (and a full run pairing every player against
the next one in the roster) with zero errors. Noted one minor rough edge
for later, not fixed: Enter-to-submit in a `<input list>` field can get
swallowed by the browser's own datalist-suggestion UI in some cases — the
"Compare →" button is unaffected and remains the reliable path.

## 2026-09-18 — Fixed stray gray values on Standings and other directory tables

Reported: "why are some values in the standings faded gray, make sure
they are all the same navy color."

Root cause: `.dir tbody td:nth-child(2){color:var(--muted)}` — a blanket
rule that muted the *second column* of every `.dir`-classed table purely
by position, added for the Players/Leaderboards tables where column 2 is
the "Tm" (team abbreviation) column. But several other tables share the
`.dir` class with a totally different column 2: Standings' `W` column,
the Division page's "Member Teams" table's `Seasons` column, and the
Games list's away-team-name column — all three were being greyed out
with no relation to what they actually contain.

The Players/Leaderboards "Tm" column already had its own dedicated,
correctly-scoped rule — `.dir td.tm{color:var(--muted)}` — applied via
an explicit `tm` class on those cells specifically. The position-based
rule was pure redundant dead weight for its one legitimate use case and
an active bug everywhere else. Deleted it outright; no replacement rule
needed since `.dir td.tm` already covers the intended case.

Verified via computed `color` styles (not just re-reading the CSS):
Standings' W/L/PCT cells, the Division member table, and the Games list
now all resolve to the standard ink color; the Players directory's `Tm`
column is still muted as intended. Swept Standings, Players, Games,
both Division pages, Teams, Records, and Compare with zero console
errors.

Follow-up: user reported still seeing gray values on Standings and
Games after that fix. Turned out to be two more, unrelated `var(--muted)`
rules, not the same bug — `.stand .rk` (the small "1"/"2"/"3" rank
number in front of each team name on Standings) and `.gtag` (the
playoff-round badge, e.g. "World Series"/"Divisional Series", shown
next to the season on Games, Home's recent-games list, and player Game
Logs). Both were deliberately muted by earlier design choices, but per
this feedback the user wants Standings and Games fully navy with no
gray text at all, so switched both to `var(--ink)`. Verified via
computed styles that `.rk` and `.gtag` now render the same navy as
their surrounding row text, with zero console errors.

## 2026-09-18 — Fixed 2023 WS game order; added a postseason overview page per year

**2023 World Series game order**: reported "game 1 and 3 for the 2023 WS
are flipped." All three games shared the same recorded date
(2023-08-06) with no `dt` timestamp, so `seriesGids`' sort fell back to
insertion order (ascending gid) for the tie — which put Bananas 2–0
Gladiators first and Bananas 3–4 Gladiators last, backwards from the
real order. Added explicit `dt` timestamps an hour apart to the three
`GAMES` entries (29918520, 29918519, 29918518) so the true order sorts
correctly: Game 1 Bananas 3–4 Gladiators, Game 2 Bananas 5–12
Gladiators, Game 3 Bananas 2–0 Gladiators — a sweep, matching the
recorded champion. Since `renderSeries`' game numbering and each
pitcher's running postseason record both derive from this same sort,
fixing the timestamps fixed both in one place rather than patching the
display layer.

**Postseason overview page**: new `renderPostseason(year)` at
`#/postseason/<year>` — reuses the existing `playoffBracket(year)` (the
same bracket with round-1/WS game-score boxes already shown inline on
Standings and Home) as a first-class destination of its own, with year
chips across every postseason on record so it doubles as a browsable
archive. The bracket's own "Full series →" links already went into the
round pages built earlier this session (`renderSeries`); this page is
just a proper home for the bracket to live at, so those links needed no
changes.

Wired up three entry points: the "{year} Playoffs" heading on both
Standings and Home is now a button into this page instead of static
text, and every round page's "← Standings" back button now reads
"← {year} Postseason" and returns here instead — since a round page is
always reached either from this overview or from a team's Playoffs
column, Standings was never really its logical parent.

Verified: swept all 10 postseason years, clicking every round's "Full
series →" link and back button, with zero console errors; confirmed
the year chips, and both the Standings and Home entry buttons, land on
the right year.

## 2026-09-18 — Added a Postseason tab to Records

New `Postseason` tab on the Records page, between Single-Game and
Streaks, with two subsections:

**Single Postseason** — one player's whole playoff run in a given year,
combined across every round (Wild Card/Divisional Series plus World
Series). The `Playoffs`-type season row already *is* that combined
line — checked first that no player has more than one Playoffs row for
the same year, so no extra aggregation was needed, just reusing the
existing `catS`-style top-10 machinery pointed at `type==='Playoffs'`
rows instead of `'Regular'`. Rate stats (AVG/OPS/OPS+/ERA/WHIP) need
only 3+ games batting or 3+ IP (9 outs) pitching to qualify, well under
the regular season's 9-G/12-IP bar — a full postseason is at most a
single-game round plus a best-of-3 World Series, so the season-level
minimums would exclude nearly everyone. OPS+ compares against that
year's postseason league average (`post:true`), matching how the
series pages already compute it.

**Single Game** — the same box-score categories as the existing
Single-Game tab (HR/H/RBI/R/2B/3B batting, K/IP pitching), just the
existing game pools filtered down to `phase==='Playoffs'` before
ranking, so a regular-season outlier can't show up in a "postseason"
record.

Verified: spot-checked the top "Home Runs in a Game" postseason line
(Evan Wilkins, 2019-09-03) against the raw game data to confirm it's
actually tagged `Playoffs`, not regular season; swept every
tab × era combination with zero console errors; confirmed the era
filter still applies to the new tab and player-name links still route
to the right player page.

## 2026-09-18 — Removed the postseason overview page

User feedback after using it: "we can remove those full postseason
pages since it's just the bracket on them" — the `#/postseason/<year>`
page added earlier this session added nothing beyond what the bracket
already shows inline on Standings and Home (chips to flip years being
the only real addition, and Standings' own year chips already cover
that for the bracket in context).

Removed `renderPostseason` entirely, its two dispatch routes, the
`data-po` click wiring on Home and Standings, and reverted the
"{year} Playoffs" headings on both pages back to plain text (no longer
a button to nowhere). The individual round pages
(`renderSeries`, `#/series/<year>/<brookside|brentwood|final>`) stay —
per explicit instruction to keep those — with their back buttons
pointed back at "← Standings" as they were before this page existed.

Verified: the Playoffs headings on Home and Standings are plain text
again; a round page's back button returns to Standings; an old
`#/postseason/<year>` link now falls back to the Home page rather than
breaking; swept series pages across several years with zero console
errors.

## 2026-09-19 — Added the BWB Grid game

New "Grid" nav entry (`#/grid`) — an original 9-square trivia game built
from scratch against this site's own data: every square needs a player
who fits both its row and column category, one guess per square. Not
copied from any other site's specific categories, text, layout or
branding — only the general "3×3 grid, guess a name matching the row
and column" idea (a format with many independent implementations) was
kept, everything else (categories, wording, scoring, visuals) is native
to this register.

**Category pool** (`gridTeamCats`/`gridDivCats`/`gridAwardCats`/
`gridStatCats`, built once and cached in `GRID_CATS`):
- Franchises — only clubs with 5+ all-time players (11 of the 14
  qualify), so no team category is a two-name gimme
- Division (Brookside/Brentwood, unified across old North/South names
  via `canonicalDivision`)
- Awards and honors — MVP, Cy Young, Postseason MVP, All-Star Game MVP,
  Rookie of the Year, Silver Slugger, Golden Hands, Batting Title, Home
  Run King, Home Run Derby Champion, Reliever of the Year, Comeback
  Player, Manager of the Year, World Series Champion, All-Star
  selection, and threw a no-hitter — any type with fewer than 3
  distinct winners is dropped from the pool
- Career statistical thresholds off `pl.careerReg` (100+ HR, 300+ RBI,
  200+ R, 300+ H, 150+ BB, 100+ games played, .400+ AVG/1.500+ OPS at
  150+ PA, 30+ wins, 150+ K pitching, 50+ IP, 5+ saves) — every cutoff
  was checked against this league's actual leaderboards first so each
  lands with roughly 3–15 qualifiers, never 0 or "everyone"

**Puzzle generation** (`pickGrid`): shuffles the category pool and
takes 3 rows + 3 columns, but only accepts the shuffle if all 9
row×column intersections are actually non-empty (checked via
`gridIntersection`, retried up to 300 times) — a generated grid is
always completable, never a guessed-at layout. "Today's Grid" seeds a
small PRNG (`mulberry32`) off the calendar date so everyone sees the
same puzzle on a given day with no backend; "Practice Grid" reshuffles
with `Math.random()` on demand and isn't persisted. Progress on today's
grid is saved to `localStorage` per calendar day and restored on
reload.

No fabricated crowd/rarity stats — landing a square shows the real,
computed count of how many players in league history qualify for it
("3 players qualify"), not an invented pick-frequency percentage.

**Bug caught during testing**: `pickGrid()` returns `{rows, cols}` with
no `answers` field; `getDailyGrid()` wrapped it correctly but the three
places that built a practice grid didn't, so opening Practice Grid
threw immediately (`Cannot read properties of undefined`). Fixed by
adding a `newPracticeGrid()` helper that always attaches `answers:{}`,
and pointing all three call sites at it — caught via a real console
error during testing, not by inspection.

Verified: a full 9-cell practice grid solved end-to-end with real
answers; a deliberately wrong guess locks the cell red without
revealing the answer; an unrecognized name shows an inline error
without consuming the guess; today's grid progress survives a full
page reload; switching Daily ↔ Practice preserves each mode's own
state; zero console errors across repeated mode switches and shuffles.

## 2026-09-19 — Added the BWB Stat Pad game

New "Stat Pad" nav entry (`#/statpad`) — a second original game, distinct
from the Grid: instead of "find any right answer," this one is "find
the *best* answer." Not copied from any other site's specific
requirements, wording, layout or branding — only the general
constrained-optimization shape (submit a player+year meeting stated
requirements; your score is their real stat total that year) was kept
as a starting idea, and every requirement, stat cutoff, and word of
copy was built fresh from this site's own data.

**How it plays**: one target counting stat for the whole puzzle (Home
Runs, RBI, Runs, Hits, Walks, Wins, Strikeouts-pitching, or Saves).
Five rows, each with 1–2 requirements drawn from the same category
families as the Grid — franchise (5+ all-time players only), division,
award/honor, career stat threshold — but split into two flavors this
game actually needs: a "that season" requirement (team/division) must
hold in the specific year you submit; a "career" requirement
(award/honor, career stat threshold) only needs to be true at some
point in the player's career. Submitting a valid player+year locks in
that row's real single-season total for the target stat that year — so
the game rewards finding the *highest-scoring* valid year, not just a
valid one. A locked row can be reopened ("Try a different player →")
to take another shot at a higher score; every submission, valid or
not, counts toward a running guess total.

**Solvability**: `pickStatpad` retries row generation (up to 30 shuffles
per row) until real players can actually satisfy each row's
requirements combination — checked via `statpadRowEligible`, not
assumed. "Today's Pad" seeds off the calendar date (reusing the Grid's
`mulberry32`/`gridDailyKey` seeding, with its own key prefix so the two
games' daily puzzles don't correlate) so everyone gets the same pad
each day, with progress saved to `localStorage`; "Practice Pad"
reshuffles freely and isn't persisted.

**Reuse**: award and career-stat-threshold requirements are literally
the Grid's own category sets (`gridAwardCats()`/`gridStatCats()`, just
tagged `sameSeason:false`) — "true anytime in career" already meant
exactly that for the Grid, so no logic needed duplicating. Team and
division requirements needed new year-by-year rosters (`statpadTeamCats`/
`statpadDivCats`) since the Grid's versions only tracked "ever played
for," not which specific years.

Verified: a full 5-row practice pad solved end-to-end using genuinely
eligible player/year combinations for each row's actual requirements;
an invalid player name shows a specific inline reason (not found /
missing a career requirement / wrong team-year / no season that year)
without consuming the row; a locked row's "Try a different player"
and "Cancel" flow works; the guess counter tracks every submission
including invalid ones; today's pad progress survives a full page
reload; zero console errors across mode switches, shuffles, and a full
completion sweep.

## 2026-09-19 — Color-coded Stat Pad answers by real quality

Reused the site's existing percentile color system (`svColor`/`svPct`,
built earlier this session for the Savant panels — blue → gray → red)
so a locked Stat Pad row's score is colored by how it actually ranks,
not just shown as a bare number.

`statpadRowValues(quals, meta)` computes the target stat's real value
for *every* (name, year) combination that legally satisfies that row's
exact requirements — the true field a submitted answer is judged
against. `svPct` places the submitted value in that field (0 = weakest
valid answer on record, 100 = strongest), `svColor` turns that into the
same blue/gray/red scale already used elsewhere on the site, and it's
applied directly to the `.spscore` number. Computed once per puzzle and
cached on `puzzle.rowValues` (deterministic from `rows`+`statKey`, so
it doesn't need persisting to `localStorage` — a reload just
recomputes it from the same seed). A row with only one possible valid
answer colors neutral gray (its only option is by definition
"average"), which `svPct`'s existing tie-handling produces without any
special-casing.

Verified: submitted the actual worst (3 HR) and best (72 HR) real
answers for one row and confirmed they render at the blue and red
ends of the scale respectively, with mid-range answers landing
in between; zero console errors across a full 5-row practice pad.

## 2026-09-19 — Stat Pad: tiered scoring and a post-completion answer reveal

Two follow-up requests on Stat Pad: show the percentile itself (not
just a color), turn the whole answer box's color by a black/bronze/
silver/gold/platinum tier instead of the continuous blue-gray-red
gradient, and reveal the top 5 real possible answers per row once the
whole pad is filled.

**Tiers**: `statpadTier(pct)` — an original 5-band read on the same
percentile the color-coding already used, in ascending order Black
(0–19) → Bronze (20–39) → Silver (40–59) → Gold (60–79, reusing the
site's own `--gold` token) → Platinum (80–100). Applied as a CSS
custom property (`--tier`) on the row itself via a new `.tiered` class,
tinting the row's background and border, plus a text badge naming the
tier — color is never the only signal. The percentile itself is spelled
out next to it ("79th percentile of every valid answer").

**Answer reveal**: `statpadRevealHTML(puzzle)` — once all 5 rows are
filled, a new section lists each row's top 5 real (player, year, value)
combinations, sourced from the same `rowCombos` already computed for
tiering (just sorted and sliced instead of a fresh query). The player's
own pick is marked inline with a "your pick" tag when it actually
lands in the top 5; when it doesn't, a separate line shows their
answer for direct comparison instead of silently omitting it.

Verified: filled a full practice pad and confirmed the reported tier
name, percentile, and row-background color all agree with each other
row by row; confirmed the reveal correctly tags an in-top-5 pick inline
and falls back to the separate comparison line for the rows that
weren't in the top 5; zero console errors.

## 2026-09-19 — Consolidated Grid and Stat Pad into one Arcade nav tab

Grid and Stat Pad had their own top-level nav buttons; merged them
under a single "Arcade" entry with a sub-tab bar (`arcadeTabBar`,
reusing the site's existing `.subtabs` component from Records/player
profiles) to switch between the two games.

Kept the refactor deliberately small: each game still owns its full
render/wire cycle exactly as before (`renderGrid`/`renderStatpad`
still build their own `app.innerHTML` and call their own `wireGrid`/
`wireStatpad`) — the only changes were swapping `setNav('grid')` /
`setNav('statpad')` for `setNav('arcade')`, heading each page "Arcade"
with the sub-tab bar underneath, and having the sub-tab buttons just
change `location.hash` between `#/grid` and `#/statpad` so the existing
router does the actual switching. No new shared state between the two
games, so nothing about how either one plays changed. `#/arcade` itself
routes to Grid by default; `#/grid` and `#/statpad` still work as
direct deep links and correctly show Arcade active with the right
sub-tab selected.

Verified: nav shows one "Arcade" button (highlighted for both games);
clicking the Stat Pad sub-tab from Grid navigates and re-renders
correctly with the tab state flipped; both old direct-link routes
(`#/grid`, `#/statpad`) still land correctly; zero console errors.

## 2026-09-19 — Grid: no reusing the same player twice

Reported: "you can't use the same person in the grid twice" — until
now, the same name could legally fill more than one of the 9 squares.
`gridUsedNames(puzzle)` collects every name already locked in as a
correct answer elsewhere in the grid; a new submission is refused
(inline error, cell stays open, doesn't consume the one-guess rule)
if it would otherwise be correct but the player's already been used.
A guess that's simply wrong for the square still locks in as wrong
regardless of reuse — the check only fires on what would've been a
correct-but-repeated answer.

Verified: locked in a real name for one square, then confirmed
guessing that same name again on a different square where it would
otherwise have qualified was refused with a clear message and left
the square open; a genuinely different valid name for that same square
then locked in correctly. Zero console errors.

## 2026-09-19 — Stat Pad: dropdown player picker, Platinum reserved for the best, no repeat combos

Three follow-up requests on Stat Pad:

**Dropdowns**: the free-text player field (backed by a datalist) is now
a real `<select class="spplayer">` listing every player, with a
disabled "Choose a player…" placeholder as the default option. Removed
the now-unused `statpadNames` datalist and its CSS. Since a `<select>`
can only ever hold a real name, the "couldn't find" branch of
`statpadFailureReason` is effectively unreachable through the UI now
but left in place as a harmless guard. Also gave the year select its
own `spyear` class — with two selects in one form, the old bare
`f.querySelector('select')` would have silently grabbed the wrong one.

**Platinum, only for the single best answer**: `statpadTier` now takes
an explicit `isBest` flag instead of inferring "best" from the top of
the percentile band — checked directly as `ans.value === Math.max(...
rowValues)`, since `svPct`'s tie-averaging means a percentile of 100
isn't guaranteed even for a true max when other entries tie near it.
Black/Bronze/Silver/Gold still split the remaining percentile range
below that.

**No repeat player+year combos**: `statpadUsedCombos(puzzle, excludeRow)`
collects every other row's exact (name, year) pair; a submission that
would otherwise be valid is now refused if that exact combo already
answers a different row, with the current row excluded so re-submitting
your own existing answer during a retry isn't blocked. The same player
in a *different* year is still allowed across rows — only the identical
pair is blocked.

Verified: dropdowns list every player and the correct year set;
submitted the actual best real (player, year) for a row and confirmed
Platinum, then the second-best and confirmed Gold instead; found a real
(player, year) that legally satisfied two different rows in one
generated pad, locked it into the first, and confirmed the second was
refused with a clear message while staying open for another guess;
zero console errors.

## 2026-09-19 — Added the BWB 15-0 game (third Arcade tab)

New "15-0" tab alongside Grid and Stat Pad — a draft game: you're
dealt one BWB franchise's entire hitting history (every player who's
ever batted for that club, career totals with that club only) and
draft any 9 of them into a roster, then see how close the combined
lineup projects toward a perfect 15-0 (a full BWB regular season).
Only the general shape — deal a themed player pool, draft a fixed
roster, project a season record from it — is a generic, widely-cloned
format; the pool logic, the projection math, and all the wording and
visuals are original and built from this site's own numbers.

**Pool**: `b0Pool()` sums each player's own Regular-season batting
lines *for one specific franchise* (so a split-team season only counts
the games actually played for that club), keeping only franchises with
12+ career hitters — enough for a real draft decision, not just
"pick the only 9 that exist."

**Projection**: deliberately simple and labeled as an estimate on the
page, not dressed up as a real simulation. `b0League()` computes two
real numbers once — league-average OPS across every regular-season
batting line ever recorded, and league-average runs per team-game
straight off real box scores. `b0Simulate` scales the drafted roster's
combined OPS against league-average OPS to project a per-game run
rate, then estimates a win percentage as that rate's share of the
combined projected-plus-league-average scoring (`projRPG / (projRPG +
avgRPG)`) and applies it across 15 games.

**Modes**: Today's Team (daily-seeded, shared, progress saved to
`localStorage`) vs. Practice Team (reshuffle anytime); independently,
Draft (stats shown per pool hitter) vs. Blind (names only). Draft/
remove is unlimited before locking; locking is final and computes the
projected record, matching the "one real shot at your final nine"
spirit of the other Arcade games.

Verified: drafted a full 9-hitter roster and confirmed the locked
record's win/loss math against the roster's own OPS and the league
averages shown alongside it; confirmed Blind mode actually hides every
stat span and Draft mode shows all of them; confirmed a daily pick
survives a full page reload; zero console errors.

## 2026-09-19 — Rebuilt BWB 15-0 as a 5-round draft, added a real game-by-game simulation

Two follow-up requests replaced the original design entirely:

**5-round draft**: instead of drafting 9 hitters from one franchise's
whole career history, the game now deals a *different real team-and-
year* each round — that club's actual single-season roster — and you
draft exactly one player from it before the next round's pool appears.
`b0RoundPool()` builds every (team, year) with a real, ≥5-player roster
from `TEAMS[t].seasons[y].roster` (using each entry's own `.regular`
line, so a pick's stats are that specific season, not a career total);
`b0Rounds(rng)` deals 5 distinct pairs per draft. A finished 5-player
team needs at least 2 who actually pitched in their drafted season
(`b0PitcherCount`) — the Lock button is replaced by an inline
requirement notice until that's true, and an "Undo" on the most recent
pick lets you go back and draft a pitcher instead without restarting.

**Real simulation**: the record is no longer `Math.round(winPct*15)`.
`b0Simulate` now runs an actual 15-game loop, drawing a random runs-
scored and runs-allowed for each individual game from Poisson
distributions centered on the team's projected rates (`b0PoissonDraw`,
Knuth's textbook sampling method) and tallying real per-game
win/loss outcomes — shown as a 15-game log alongside the final record,
not just a single number. The daily version seeds its "luck" off the
calendar day alone (not the drafted roster), so everyone comparing
that day's results is being compared on team-building, not on who
drew a friendlier random sequence; Practice mode just uses fresh
randomness each run.

**Bug fixed during testing**: `renderB0()` unconditionally read
`puzzle.rounds[puzzle.picks.length]` to show "the current round," which
is `undefined` once all 5 picks are made but before locking — threw
immediately and blanked the page. Fixed by only rendering the round
pool when a round actually exists at that index. Also hit stale
`localStorage` from the *original* 9-hitter design (picks stored as
plain name strings, not `{name,team,year,line}` objects) crashing the
new code on load — fixed by versioning the storage key (`bwb-b0v2-`)
and validating the shape of anything loaded before trusting it.

Verified: drafted a full 5-round team favoring pitchers and confirmed
the pitcher-count gate correctly blocked/allowed locking; locked in and
confirmed the 15-entry game log's win/loss tally matches the displayed
record; reproduced and fixed both crashes above in a clean tab with
zero console errors afterward.

## 2026-09-19 — Added D00B, a fourth Arcade game (photo blend, guess both)

New "D00B" tab alongside Grid, Stat Pad and 15-0. Two players who have
a photo on file (43 of 96) are dealt, their own uploaded photos are
layered on top of each other with a CSS `mix-blend-mode: lighten` (the
standard no-canvas way to fade two photos into one ghostly double
exposure — no external image processing needed), and you guess both
names from the blend in one lock-in, order doesn't matter.

`b1Score` matches the two guesses against the two real names as sets
(so guessing the same name twice only ever counts once, and guessing
both correctly in either order both count) — partial credit for one of
two. The reveal shows both real photos side by side with a hit/miss
tag on each.

Today's D00B is dealt once daily (seeded off the date like the other
three games) and its result persists to `localStorage`; Practice D00B
deals a fresh pair on demand and keeps a running session tally
(correct guesses out of 2 per blend, across however many blends played)
that resets on reload — deliberately not persisted, since practice mode
elsewhere in Arcade doesn't persist either.

Verified: a fully-correct guess scores 2/2 with both reveal cards
marked "guessed"; a one-right-one-wrong guess scores 1/2 with the
correct card marked and the wrong one marked "missed"; guessing the
same name in both slots is refused with an inline message instead of
submitting; today's result survives a full page reload; zero console
errors.

## 2026-09-19 — Removed D00B; real roster rules and sample-size regression for 15-0

Removed the D00B (photo blend guessing) game entirely — nav tab,
routes, all `b1*`/`B1_*` code and CSS. Arcade is back to three games:
Grid, Stat Pad, 15-0.

Three follow-up requests reshaped 15-0 into a more rigorous draft game:

**No repeat players**: the same player could previously be drafted
twice under two different (team, year) deals — e.g., a Kraken 2020
season and a Kraken 2023 season both dealing the same person. The
draft pool now shows "Already on your team" with no Draft button for
anyone already picked in an earlier round, and the click handler
itself refuses the pick as a second guard.

**Explicit pitching staff ("make your lineup")**: instead of just
counting anyone who happened to have pitched that season, there's now
a real lineup step after all 5 picks are in — designate at least 2 of
them as your pitching staff (only players with real innings pitched
that season are eligible; everyone still hits regardless). `b0Simulate`
now sums *all 5* players' batting lines for team offense but only the
*designated* pitchers' lines for team pitching, so a spot-innings
appearance from a non-designated player no longer silently counts
toward the team's run prevention.

**Sample-size regression**: "season sample size for a player should
factor in like games played" — a 2-game hot streak and a 15-game
season were being trusted equally. `b0RegressLine` now shrinks each
player-season's rate-driving fields (H/BB/HBP/TB for batting, ER for
pitching) toward league average, weighted by how far that season's own
games-played or innings-pitched falls short of this site's existing
qualification bar (`SV_MING`/`SV_MINOUTS` — the same 9 games / 12 IP
already used for percentile rankings elsewhere, reused here instead of
inventing a new number). Real at-bats, plate appearances and innings
are never touched, only the outcome rates built from them. Applied
once in `b0RoundPool()` so the draft pool's own displayed stats already
match what the simulation will use — no discrepancy between what you
see while drafting and what actually gets simulated.

Storage key bumped to `bwb-b0v3-` (adds the `pitchers` array to the
saved shape) so a browser with `v2` state from before this change is
ignored rather than misread.

Verified: found a real (team,year) pair overlap across two rounds in a
generated draft, drafted the shared player in the earlier round, and
confirmed the later round correctly blocked it; completed a full draft
with a deliberately weak pitching staff (11.18 ERA) and got an 0-15
result — confirmed by the numbers this is a legitimately unlucky but
valid outcome (~0.2% likely at a .344 win rate), not a bug; confirmed
daily picks and an empty pitcher list survive a full page reload; zero
console errors throughout.

## 2026-09-20 — 15-0: bootstrap-resampled simulation and a real salary cap

Two follow-up requests, discussed first before building:

**Bootstrap-resampled game simulation** — asked "how can we make the
simulation better," recommended and got a yes on replacing the Poisson
run model with real data: `b0RunsPool()` collects every real BWB
team-game run total ever recorded (each game counted for both sides),
filtering out forfeit-batch dates using the same signature the Records
page's streak-building already flags (4+ games on one date, one score
pair accounting for a strict majority). `b0BootstrapDraw` now draws an
actual real run total from that pool and scales it to the team's own
projected rate, instead of `b0PoissonDraw`'s idealized bell curve —
this league's real scoring is far more bursty than Poisson assumes
(real box scores here include 30+ run games), so sampling from what's
actually happened produces realistic blowouts and shutouts at their
real frequency.

**Real salary cap** — "the game is too easy... a budget system where
each player has a money value and you have to stay under a cap."
`b0Value(line)` scores each drafted player-season as OPS-above-league-
average times plate appearances, plus ERA-below-league-average times
innings pitched for anyone who pitched — a transparent "value above
average, weighted by how much of it you got," not a rigorous linear-
weights model but honest about what it's doing. `b0RoundPool()` maps
every real player-season's value onto a $1-$50 price (linear, off this
site's own actual min/max, not an arbitrary curve) and picks now cost
real money against a $100 team cap. Checked the real distribution
first (min -132/max 165 in value terms, mean price $23) before picking
$100 as the cap specifically because it sits *below* what 5
average-priced players would cost — an average team runs over budget,
so affording even one star requires real bargain-hunting elsewhere.

**Bug caught during testing**: greedily drafting the most expensive
affordable player each round could burn through the budget early and
leave a later round with *no* affordable option at all — a real
dead-end, not a strategy mistake. Fixed with `b0RemainingFloor`, which
sums each remaining round's own actual cheapest price (not a flat $1
guess) and caps every pick at (what's left) minus that floor — a
mathematical guarantee the draft can never get stuck, shown to the
player as "at least $X needed for the rest of the draft" alongside the
running budget.

Verified: reproduced the dead-end bug with a deliberate worst-case
greedy draft before the fix, confirmed it can no longer happen after;
re-ran the same worst-case draft post-fix and it completed cleanly at
exactly $0 remaining; confirmed prices, the running budget, and the
"needed for the rest" hint all track correctly through a real draft;
confirmed a daily pick's price survives a full page reload; zero
console errors throughout.

## 2026-09-20 — Optional salary cap, full-stat player valuation, and a real 2023 WS fix

**2023 World Series order, corrected again**: the earlier `dt`-based
fix (2026-09-18) had games 1 and 3 backwards. Confirmed against the
real scores this time — Game 1 is Bananas 2–0, Game 2 Gladiators
12–5, Game 3 Gladiators 4–3 — and updated the three games' `dt`
timestamps accordingly. Both the series page and the bracket read
game order off the same `seriesGids` sort, so fixing the underlying
data fixed both places at once, matching what was reported.

**Salary Cap is now an option, not the only mode**: Today's Draft
stays Salary Cap always (one well-defined shared daily challenge), but
Practice Draft now has its own Salary Cap / Free Draft toggle. Free
Draft still shows every price for reference but drops the budget
constraint entirely — draft whoever you want. `capMode` is stored per
puzzle so a mid-draft mode never gets stale mid-flight; storage key
bumped to `bwb-b0v4-`.

**Valuation now uses every batting and pitching counting stat this
site tracks**, not just OPS and ERA. `b0BatPoints`/`b0PitPoints` are an
original linear-weights point system — singles through home runs,
walks, HBP, steals and caught stealing for batting; earned runs,
strikeouts, walks and hits allowed for pitching — each compared to
what a league-average player produces in the same playing time
(`b0Value`). The same per-stat league rates now also drive sample-size
regression (`b0RegressLine`), extended from just H/BB/HBP/TB/ER to
cover every field the valuation formula reads, so a small-sample
season's 1B/2B/3B/HR/SB/CS/K/BB-allowed/H-allowed all get shrunk
consistently with everything else. Fielding stats are deliberately
left out of both — tracked far more sparsely and unevenly across
seasons than batting/pitching, so including them would add noise
rather than signal.

**Bug caught during testing**: dealing 5 random rounds with zero
regard for price could hand out a set whose combined *cheapest
possible* team already exceeded the $100 cap — not a mid-draft dead
end but an unsolvable draft from round 1, discovered when a fresh
daily deal showed every player in the very first round marked "Over
budget" at full $100 budget. Fixed by having `b0Rounds` retry the
whole deal (in Salary Cap mode only) until the sum of every round's
own real cheapest option actually fits under the cap — the same
"verify solvability, don't assume it" discipline already used
elsewhere on this site (Grid's `pickGrid`, Stat Pad's row generator).

Verified: reproduced the round-1 unsolvable-deal bug, confirmed the
fix (round minimums now sum to $96, all of round 1 affordable);
completed a full cap-mode draft end to end through lock-in and
simulation; confirmed Free Draft actually ignores the cap (spent $179
of a nominal $100); confirmed the 2023 WS series page now shows the
corrected game order; zero console errors throughout.

## 2026-09-20 — Site-wide consistency pass: fixed a real character-encoding bug

Asked to "go through the whole site and make sure the headers and font
and everything is consistent and looks good." Audited the typography
system (every heading rule uses the same Oswald/Arial Narrow stack,
consistently sized by level — page title, section, subsection) and
visually swept Home, Players, a player profile, Standings, Records,
Teams, a team page, and all three Arcade games.

The one real, high-impact bug: **no `<meta charset="utf-8">`
declaration anywhere in the document**. Without one, a browser served
this file without an explicit charset header (confirmed locally with
Python's `http.server`, which doesn't set one) has to guess the
encoding — and guessed wrong, misreading this file's UTF-8 em-dashes,
en-dashes and middle dots (used constantly in headers, subtitles and
notes across every page) as a different encoding, mangling every one
of them into "â€"'"/"Â·"-style garbage. Confirmed directly against the
DOM's own `textContent` (not just the screenshot) before and after —
added `<meta charset="utf-8">` as the very first line of `<head>`, the
standard fix, and every dash and middle dot checked came back correct
site-wide with no other code changes needed.

Everything else checked out: consistent heading hierarchy, consistent
color tokens, no console errors across a 15-page sweep (Home, Players,
Teams, Standings, Leaders, Records, Games, Champs, Awards, Beavers,
Grid, Stat Pad, 15-0, a player profile, a team page).

## 2026-09-20 — 15-0: fixed fractional stat display and a real budget-solvability gap

Two follow-up reports, both real bugs:

**"Stats aren't reading correctly" / "should be regular season stats
only"**: the pool was showing the *regressed* (shrunk-toward-average)
version of a player's line instead of their real season totals — a
player's card could read "1.38 HR" instead of a real integer, because
`b0RoundPool()` overwrote `line` with the output of `b0RegressLine`
entirely. Fixed by keeping both: `line` is now always the player's
real, unmodified regular-season totals (what's displayed everywhere —
the pool, the roster, the lineup step), and `regLine` is the shrunk
version, used only internally for `b0Value` (pricing) and `b0Simulate`
(the team-projection math). The underlying data was already
regular-season-only the whole time (`e.regular`, verified directly
against `players.json` — Brentwood Gladiators 2023 shows separate
`regular`/`playoffs` blocks per player, never merged); the bug was
never about mixing in playoff stats, it was about showing the
statistically-adjusted number instead of the real one.

**"Players aren't pickable from the start"**: real, but not where the
last investigation looked (round 1 tested fine in isolation, in every
mode, across 400 simulated dates). The actual gap: `b0RemainingFloor`
summed each remaining round's own cheapest price as if independently
achievable — but two different rounds' cheapest option can be the
*same real player* dealt in two different years, and the no-repeat-
player rule means only one of those rounds can actually have them.
Treating both floors as achievable at once could quietly overestimate
how much budget was actually safe to spend, letting a draft paint
itself into a corner a couple of rounds in. Replaced with
`b0MinDistinctCost`, a small brute-force search for the true cheapest
way to fill the remaining rounds with distinct players, and made
affordability a genuinely per-candidate check (drafting a specific
player now excludes them from their own floor calculation) instead of
one shared number for the whole round. Storage bumped to `bwb-b0v5-`
for the updated pick shape (`regLine` added).

Verified: confirmed every displayed HR/RBI/K count is now a clean
integer; ran 25 trials of the exact adversarial strategy that
originally got stuck (always draft the most expensive affordable
option each round) with zero failures; confirmed daily mode unaffected;
zero console errors.

## 2026-09-20 — 15-0: fixed massive price clustering (rank-based pricing)

Reported: "so many players have the same value." Confirmed directly
against the real data — the previous linear min-max price scaling had
**136 of 294 player-seasons (46%) all priced at the exact same $29**,
with the rest thinly spread across the other 37 price points. Root
cause: this pool's value distribution is heavily right-skewed (a
handful of real standout seasons pulling the max way up, a big cluster
of everyone else sitting close to replacement level) — a straight
linear scale compresses that whole cluster into a narrow slice of the
$1-$50 range regardless of how many players are in it.

Fixed by pricing off each player-season's RANK in the value
distribution instead of the raw value itself: sort all eligible
entries by value, map each one's position in that order linearly onto
$1-$50. Since rank is by construction evenly distributed, this
guarantees a spread across every dollar amount no matter how skewed
the underlying values are — checked against the same real pool: all
50 price points now get used, and the worst tie is 5 players (the
unavoidable minimum for splitting ~225 eligible entries across 50
prices). This also likely explains why the budget-floor numbers felt
"off" in the previous report — with nearly half the pool priced
identically, a floor calculation referencing genuinely different
per-round minimums wouldn't have matched what was visibly on screen.

Verified: confirmed the real price distribution now uses all 50 points
with a max 5-way tie (was a single 136-way tie at $29); re-ran the
25-trial adversarial worst-case draft strategy (always draft the most
expensive affordable option) against the new pricing — 40/40 trials
completed with zero stuck drafts; spot-checked that the "$X needed for
the rest of the draft" figure now tracks sensibly against the visibly
varied prices on screen; zero console errors.

## 2026-09-20 — Compare Players now shows percentile bars

Added a "Percentile Comparison" section to the Compare page, reusing
the same Savant-style bars, colors and math already built for a single
player's own Percentile Rankings — `SV_BAT`/`SV_PIT` metric list,
`svColor`/`svPct`, and the same qualification bar (`SV_MING`/
`SV_MINOUTS`, with the same `SV_MIN_SHOW_G`/`SV_MIN_SHOW_OUTS`
faded-estimate floor for a short career) — just against a career-totals
pool (`CMP_POOL_BAT`/`CMP_POOL_PIT`, every qualified player's own
career line) instead of one season's, and with both players sharing
one track per row instead of one dot per row.

Each metric's two dots sit on the same 0-100 bar so you can see at a
glance who ranks higher and by how much, labeled A/B matching the
names above; qualification is checked per player per category (a
mostly-pitcher and a mostly-hitter can each show a real ranking on
their own side and a faded estimate on the other, in the same row) —
reusing `cmpCareerQual`, the career-scoped version of the same
qualification check the single-player page already used.

Verified: both dots render at distinct, correct percentile positions
with correct colors and tooltips (checked directly against the DOM,
not just the screenshot); the section correctly hides when neither
player has enough of a career to estimate anything; zero console
errors.

## 2026-09-20 — 15-0: fixed the real remaining cause of round-1 lockouts

Reported again: "there are still some cases where you can't even draft
a player on round 1 because of their budget." The previous fix
(`b0MinDistinctCost`, a brute-force search for the true cheapest way to
fill the remaining rounds with distinct players) trimmed each round to
its cheapest 8 candidates before searching, for speed. That trim was
the bug: if the *true* minimum-cost combination needs a round's 9th-
cheapest option or later — which heavy cross-round overlap can force —
the trimmed search comes back with no valid combination at all, even
though a real one exists, which is exactly what made every round-1
option look unaffordable.

Fixed by trying the fast trimmed search first, and only falling back
to an exact, untrimmed search on the rare occasions the trim comes up
empty — correct in every case (the untrimmed search can't miss a
combination that exists), fast in the common case (the trim almost
always succeeds on the first try). Measured directly: 300 full deal
generations plus a full round of per-candidate floor checks each,
completed in 39ms total — the fallback path costs nothing in practice.

Verified: 60 more adversarial trials (always draft the most expensive
affordable option, the same worst-case strategy used before) with zero
stuck drafts; confirmed no performance regression; zero console errors.

## 2026-09-20 — Shareable daily results for all three Arcade games

Added a Wordle-style "Share result →" button to Grid, Stat Pad, and 15-0,
shown only once that day's puzzle is complete (and only in each game's
daily mode, not practice — sharing a private practice run isn't
meaningful). It builds a spoiler-free text summary — an emoji grid/strip
plus the headline number — and copies it to the clipboard:

- Grid: 3x3 emoji grid (🟩 correct / 🟥 wrong / ⬜ unattempted) + "N/9 correct".
- Stat Pad: one tier emoji per row (⬛ Black · 🟫 Bronze · ⬜ Silver · 🟨 Gold ·
  💎 Platinum) + the total stat headline.
- 15-0: one 🟩/🟥 per simulated game + the final win-loss record and cap mode.

Since this whole site runs inside a sandboxed Artifact iframe, a blocked
`navigator.clipboard` call can't fall back to `window.prompt()` either —
tested directly and confirmed it throws `prompt() is not supported.` in
that context. Replaced that fallback with a plain read-only `<textarea>`
that appears pre-selected next to the button, so the result is always
copyable by hand even when the Clipboard API is unavailable.

## 2026-09-20 — Consistent headers across a player's Stats/Splits/Game Log tabs

Reported: "the headers on the site aren't consistent... stats, splits, and
game logs all have different header looks when you click into them on a
player profile." Confirmed — the three subviews under each phase tab
used three unrelated header styles: Stats' top header (the phase name,
e.g. "Regular Season") was a bold 1.35rem `<h3>`; Splits' top header
("Splits") was a bigger 1.4rem `<h3 class="hsub">` (the site's generic
sitewide subsection style, unrelated to the phase header); Game Log's
top header ("Game Log") was a tiny uppercase `<h4>` — the same small,
muted style used for the nested "Batting"/"Pitching" table headers one
level down, so it read as a sub-heading, not the top of its own section.

Introduced a shared `.viewhead` class carrying the Stats phase header's
exact styling, and applied it to all three: Splits' and Game Log's
headers are now `<h3 class="viewhead">`, matching Stats' `<h3>` (which
already gets the same rule via `.phase>h3`). Verified on both a regular
phase and the NWLA Tournament phase (which has its own Splits/Game Log
builders) that all three headers now render pixel-identical in font,
size, weight and color — only the label text differs, same as
"Batting"/"Pitching" already did one level down. Zero console errors.

## 2026-09-20 — Career team history, a fixed franchise logo, and clearer Compare dots

Four small fixes from one round of feedback:

**Daniel Brady's 2026 logo.** Reported wrong on Leaders/Full Stats. Root
cause: his 2026 regular season is a two-team split (Brentwood Gladiators,
then Silver Lake Snapping Turtles — he played the postseason with the
Gladiators, so that's genuinely the team he finished the year on).
`build.py` stores a two-team season as `"A / B"` ordered by games played,
not chronologically, and the display code has always shown whichever
team comes *second* in that string as the primary logo — a real,
site-wide mismatch between what the data encodes and what the renderer
assumes, not unique to Brady. Rather than change that renderer for all 6
split-season players on a guess, corrected the one entry that was
actually wrong: swapped Brady's stored order to
`"Silver Lake Snapping Turtles / Brentwood Gladiators"` in `players.json`,
so the Gladiators — his real end-of-season team — is what shows.

**Players directory now shows a player's whole team history.** The
Stats table and A–Z view previously showed only the player's *latest*
club. Added `careerTeams(pl)`, which walks `teamsByYear` into per-team
stints (splitting a player's return to an old team from an uninterrupted
run — a real case: Victor Cottini's Braves stint is 2017 and, separately,
2024–2025, not one continuous span), and `teamHistoryChips(pl)`, a row
of small clickable team-logo icons for the Stats table (tooltipped with
the franchise name and every year range) with the A–Z view getting the
same list as plain nicknames.

**Compare page's percentile dots now say which player is which.** The
"Percentile Comparison" section already explained "A = Player 1, B =
Player 2" once in the intro text, but each individual dot only showed
its percentile number — nothing tied a specific dot back to A or B
without cross-referencing position against the legend. Added a small
"A"/"B" tag above each dot, and the player's actual name into its
tooltip alongside the percentile (also fixed to a real ordinal — "92nd",
not "92th").

## 2026-09-20 — 15-0: dropped the salary cap for forced Pitcher Rounds

The salary cap kept causing real problems — three separate round-1
solvability bugs, a price-clustering bug, and a standing complaint that
the valuations still didn't feel right even after fixing all of those.
Underneath it all was one structural problem: turning a wiffleball
season into a single fair dollar figure is inherently squishy, and no
formula tweak was going to make that feel right. Discussed it and agreed
to drop pricing and the cap entirely rather than keep patching it.

That made the game too easy on its own (the earlier salary cap existed
specifically because a totally free draft meant just taking the best
player every round), so the difficulty moved somewhere else: **Rounds 4
and 5 are now forced Pitcher Rounds.** Their pool is trimmed to only
players who actually pitched in that dealt season, and whoever you draft
there joins your pitching staff automatically — no more separate "Set
Your Lineup" step at the end. Team offense still comes from all 5 picks;
team pitching now comes specifically from those 2 forced picks.

Removed entirely: `b0BatPoints`/`b0PitPoints`/`b0Value` (the whole
valuation formula), rank-based pricing, the Salary Cap/Free Draft toggle,
and the `b0MinDistinctCost`/`b0RemainingFloor` solvability-search
machinery that existed only to keep the cap from locking someone out of
round 1. `b0RegressLine`'s sample-size regression stays — that's still
doing real work for the simulation, independent of pricing.

Dealing now draws the 2 Pitcher Round slots from a separate pool (any
team-year with 2+ players who pitched that season), then checks the two
dealt seasons can actually supply 2 *different* real pitchers before
accepting the deal — the same "verify, don't assume" approach as the old
solvability checks, just against a much smaller, cheaper problem now
that there's no budget to solve for. Verified with 300 adversarial deal
generations (zero failures, ~9ms total) and a full draft-through-lock
run via real button clicks, including that Undo correctly un-assigns a
pitcher when you take back a Pitcher Round pick. Storage bumped to
`bwb-b0v6-` for the shape change.

## 2026-09-20 — 15-0: random Pitcher Rounds; No-Hitters table cleanup

**15-0: which 2 rounds are Pitcher Rounds is now random**, not fixed at
4 and 5 — a partial Fisher-Yates shuffle of the 5 round indices drawn
from the same seeded rng as the rest of the deal, so the daily draft
stays reproducible/shareable and practice drafts get a fresh pair every
time. Verified all 10 possible pitcher-round pairs actually occur across
300 seeded trials, with zero solvability failures. Storage bumped to
`bwb-b0v7-` since this shifts the whole rng sequence a deal draws from —
an in-progress draft saved under the old fixed-4-and-5 shape would no
longer line up with newly-regenerated rounds.

**No-Hitters & Perfect Games table**: dropped the free-text "Notes"
column (hand-typed trivia like "Ended on crazy peg at first" — fun, but
not a stat, and it was the widest column on the page) and added each
team's real logo next to its name in the Team and Opponent columns,
matching how logos already appear everywhere else stats are listed.

## 2026-09-20 — Two new pitching streaks: Scoreless Innings and Complete Games

The Records > Streaks tab only ever covered team win/loss streaks and
three batting streaks — no pitching. Added a `pitcherStreaks(cond,
valueFn)` builder, the pitching mirror of the existing batting-streak
logic (consecutive regular-season appearances meeting a condition, reset
at a season boundary, restricted to games with a recorded individual
line, 2020 on):

- **Longest Scoreless Innings Streaks** — consecutive appearances with 0
  runs allowed, measured in real innings pitched summed across the whole
  streak (the traditional way a scoreless streak is reported), not just
  a count of outings.
- **Longest Complete-Game Streaks** — consecutive starts that were each a
  full complete game. There's no stored per-game "complete game" flag in
  the box scores (only a season total), so this is derived straight from
  two numbers that ARE recorded: a pitcher's own IP for that game equals
  the game's full length in outs — which can only be true if nobody else
  on their side recorded an out that game either.

The "Player" streak header split into "Batting" and "Pitching" to make
room. Verified both new lists directly against raw per-game data (e.g.
Parker Gibbons' reported 11.2-inning scoreless streak sums exactly to
five real games' outs; Zach Lieberman's reported 10-game complete-game
streak checks out as ip === game length across all 10 real appearances).

## 2026-09-20 — "Perfect Game" instead of just "Perfect"

Small copy fix: the perfect-game tag in the Records No-Hitters table and
a player's own Accolades card just said "Perfect", ambiguous next to a
"No-Hitter" list. Both now read "Perfect Game".

## 2026-09-20 — Team logos on the Games tab and box scores

Added team logos to the two places that were still text-only: the Games
tab's list (a small icon next to each Away/Home team, matching the same
`.tmcell` treatment used on the No-Hitters table and Players directory)
and each box score's matchup header (a larger logo flanking each team
name around the score, a new `.llogo-lg`/`.muteam` pairing). Verified on
both a modern game and a 2017 thin-box-score game (single team-total
line, no per-player rows) — the header logos render the same either way
since they only depend on the team/year, not on box score detail level.

## 2026-09-20 — Fixed two defunct franchise names: Devils and Downtown Angels

Reported: the "Gleason Diablos" and "Parsons Angels" franchise entries
(2013–2014, before individual box scores) had the wrong identity. The
Diablos franchise was always actually the **Gleason Devils** — its own
`FRANCHISE_TIMELINE` era already correctly said "Devils", it was only
the top-level franchise name/nickname that wrongly said "Diablos".
Confirmed independently: a real 2013 no-hitter record in the league's
own log names the opponent "Downtown Angels", not "Parsons Angels" —
so that franchise's real name is **Downtown Angels**, not Parsons.

Renamed both consistently everywhere a franchise identity string is
used: `FRANCHISE_COLORS`, `FRANCHISE_SUMMARY`, `FRANCHISE_TIMELINE` in
generate.py, plus the matching keys in `players.json`'s `leadership`
(captain/co-captain records) and `franchiseLogos` (the Diablos logo is
now keyed "Devils" — Angels' key was already right). Verified the
Franchise Name History timeline, the Franchise Summary table, and each
team's own detail page (logo, record, and captain) all resolve under
the corrected names with zero leftover references to the old ones.

## 2026-09-20 — Added ERA+, the pitching mirror of OPS+

Requested: "add other stats like ERA+." Built `eraPlusFor(d, weights)` and
`careerWeightsPit(pl, post)` as the pitching-side twins of the existing
`opsPlusFor`/`careerWeights` — same math shape (100 × league rate ÷
player rate, blended across whichever year(s) contributed, weighted by
playing time), just weighted by innings (outs) instead of plate
appearances, and inverted since ERA is lower-is-better while ERA+ stays
higher-is-better like OPS+. League ERA per year already existed in the
same `LEAGUE_BY_YEAR` tables OPS+ uses, so no new league data had to be
built.

Added everywhere OPS+ already appears, mirroring each site exactly:
Players directory (Pitching mode), a player's own Pitching stat table
and Splits (all 3 split dimensions), Leaders (Top 10, Full Stats, and
Single-Season/Postseason Records), Standings' Team Pitching table, the
Teams directory, a team's own season roster and "Franchise Roster ·
Pitching" (all-years) tables, and a playoff series' per-team pitching
lines. Left it out everywhere OPS+ is also deliberately left out for the
same reason (the ASG roster and Beavers/NWLA tournament pages, which
combine games with no sound single-year league baseline to normalize
against) and skipped single-game leaderboards, which already have no
ERA category since a 3-inning game's ERA is too noisy/often-infinite to
rank meaningfully. Verified the formula directly against raw data and
swept every touched page for console errors.

## 2026-09-20 — New League Office page; Daniel Brady renamed to Dan Brady

Added a **League Office** page (nav: Beavers → League Office → Arcade),
listing who actually runs BWB off the field — hand-kept in a new
`LEAGUE_OFFICE_LEAD`/`LEAGUE_OFFICE_OPS` list, not derived from any game
data. Three larger cards for Parker Gibbons (Founder/Commissioner/Head
of Operations), Peter Fraioli (Co-Commissioner/Head of Content
Management and Design/League Operations Lead), and Trevor Meyler
(Assistant Commissioner/Operations Lead), then a "League Operations"
row for TJ Ciafone, Peter Sposato, Victor Cottini, Dan Brady, Austin
Corvino, and Vinny Spoto. Each card reuses that player's own profile
photo and links to their player page.

**Renamed Daniel Brady to Dan Brady** everywhere — the player dict key,
every game box score line, honors, leadership, ASG appearances, the
no-hitter log, all of it, via a global string replace across
`players.json` (107 occurrences) rather than just the display name, so
there's no longer a mismatch between how he's shown and how he's
actually stored. This also let two now-obsolete name-alias corrections
in `generate.py` get deleted — `plink()`/`normASG()` used to map a raw
"Dan Brady" mention back to the old canonical "Daniel Brady" key
specifically because some raw ASG data already called him Dan Brady;
now that the canonical name matches, that alias is dead code.

## 2026-09-20 — Added Griffin Krueger to the League Office; title fixes

Fixed Trevor Meyler's title (went through "Operations Lead" →
"Lead Operations Lead" → the intended **"League Operations Lead"**,
matching Peter Fraioli's own "League Operations Lead" title).

Added **Griffin Krueger** to the League Office page as **League
Columnist**, in a new "Columnist" section of its own below League
Operations (`LEAGUE_OFFICE_OTHER`). He didn't have a profile photo on
record — added the headshot supplied for this, resized to the site's
existing 240×240 JPEG convention (matching every other player photo's
format and roughly its file size) and saved to his player record, so it
now shows both on his League Office card and his own player page.

## 2026-09-20 — A page per Beavers tournament; "Champs" renamed to "Champions"

**Beavers tournaments now each get their own page.** The overview
(`#/beavers`) used to dump every game from every tournament inline,
which wouldn't have scaled past one trip. Split it: the overview keeps
only the combined, all-tournament record and batting/pitching tables
(exactly as requested), plus a new "Tournaments" grid of cards — one per
trip, each linking to `#/beavers/t/<start-date>` (dates are the one
field guaranteed unique per tournament, so the URL survives more trips
being added later, even out of order). That new page shows the roster's
batting/pitching for just that tournament (not merged with any other)
and every one of its games, grouped by phase, exactly like the overview
used to show inline.

Deep links into a specific game (from a player's own NWLA Game Log tab)
used to open the overview and auto-expand that game's box score; since
the game listing moved off the overview, added `bvTournamentForGame(gid)`
so that link now lands on the correct tournament's own page with the
right game expanded and scrolled to, instead of silently landing
nowhere.

**Renamed the "Champs" nav tab to "Champions"** (the page's own heading
already said "Champions of BWB Wiffleball" — only the tab label was
inconsistent).

## 2026-09-20 — Fixed missing OBP on a Beavers tournament page

Reported: OBP wasn't showing on the 2026 NWLA page. Root cause: the new
tournament page's team-total line built `bTot` with `sumBox(bat,
BV_BAT_KEYS)`, and `BV_BAT_KEYS` doesn't include `HBP`/`SF` — so
`bTot.HBP`/`bTot.SF` came back `undefined` rather than `0`, and
`obp()`'s denominator (`AB+BB+HBP+SF`) evaluated to `NaN`, which renders
as "—". Each individual player's own row was already fine (those get
`HBP:0, SF:0` set explicitly), so only the team-total "Team Batting"
line was affected. Fixed by summing `HBP`/`SF` into the team total too.
The all-tournament overview page never had this bug — it already built
its team total with those two fields seeded to 0 from the start.

## 2026-09-20 — Header cleanup: "Established in 2012"; anniversary badge moved up

Replaced the header subtitle "Career Register · 2017–2026" (the
2017–2026 span is the *stat database's* coverage, not the league's own
history) with **"Established in 2012"**, the league's actual founding
year. Also dropped the home page's redundant intro paragraph ("The
career register for BWB Wiffleball, 2017–2026 — batting, pitching and
fielding for every player...") — the site demonstrates all of that by
existing, and it repeated the same 2017–2026 framing being removed from
the header.

Moved the **15th Anniversary badge** out of that now-removed paragraph's
row (where it would've been left oddly alone) and into the header itself,
between the brand and the theme toggle — a permanent, prominent spot
that fits a season-long anniversary mark far better than a one-time
callout on the home page body. Verified on both desktop and mobile
widths.

## 2026-09-20 — Moved the 15th Anniversary badge out of the header

Reported: the anniversary badge looked terrible sitting alone in the
header's open space between the brand and the theme toggle. Pulled it
out of the header entirely and replaced it with a reusable `annivBadge()`
helper — a small inline pin meant to sit directly beside a heading's own
text, never floating alone in empty space. Placed it next to:

- the home page's "The [Team] are [Year] BWB Champions!" banner heading
  (both the photo and no-photo variants),
- the home page's "[Year] Standings" section heading, and
- the actual Standings page's own "Standings" heading (requested by name).

## 2026-09-20 — Anniversary badge: down to one spot, the Standings page

Trimmed further per follow-up: the badge should live in exactly one
place, not the header and not the home page's champion banner or its
"2026 Standings" preview section. Removed those three; it now shows only
next to the "Standings" heading on the actual Standings page.

## 2026-09-20 — Anniversary badge: moved to the home page's Standings preview

Corrected: "the 2026 standings" meant the home page's own "2026
Standings" preview section, not the full `/standings` page. Moved the
badge there and removed it from the full Standings page — it now shows
in exactly one place, next to "2026 Standings" on the home page.

## 2026-09-20 — Added a global player/team search bar to the header

Added a search box to the top-right of the header (next to the theme
toggle), available on every page since it's wired once outside the
router, not per-page. Type a few letters of a player or team name and
get a live dropdown of matches — each with their photo/logo, a subtitle
(a player's current team, or the team's full name), and a Player/Team
tag — ranked so a name that *starts with* the query beats one that just
contains it. Click, or arrow keys + Enter, jumps straight to that
player's or team's page. Escape or clicking outside closes it.

While testing this at an emulated mobile width, found the site has no
`<meta name="viewport">` tag at all (a pre-existing, unrelated issue —
mobile browsers were falling back to a ~980px desktop layout and
scaling it down instead of laying out at the real device width).
Flagged as a separate follow-up rather than fixing it inline here.

## 2026-09-20 — Players directory: "Tm" column now sorts by team count

The Players page's "Tm" column shows every career team as logo chips
(added earlier this session), but clicking the header still sorted by
the player's *latest* team name alphabetically — a leftover from before
that column showed the full history. Added `teamCount` (from the
existing `careerTeams()` helper) to each row and switched the sort to
rank by number of distinct franchises played for, ties broken
alphabetically by latest team. Verified in both Batting and Pitching
modes, ascending and descending.

## 2026-09-20 — Fielding added to Leaders; dropped the redundant Teams search

**Teams page**: removed the "Search franchises…" box and its dead
`tQuery`/`tMode`/`tSort`/`tDir` state — the new global header search
already covers finding a team by name from anywhere on the site, so this
in-page filter was pure duplication.

**Leaders now covers Fielding**, matching Batting/Pitching in both
views:
- Top 10: Fielding %, Putouts, Assists, Double Plays. Fielding %
  qualifies at the same 9-games bar batting rate stats already use
  (`G_fld>=9`), reusing the existing qualification convention rather
  than inventing a new one.
- Full Stats: a third "Fielding" toggle alongside Batting/Pitching,
  sortable by any column (G, INN, TC, PO, A, E, DP, FLD%).

Fielding data is currently only recorded for 2022–2025 (per-year totals
are missing for 2017–2021 and 2026) — 2026 correctly shows "No fielding
qualifiers" rather than an error, and will populate on its own as 2026
fielding lines get added game by game.

## 2026-09-20 — Fixed fielding % that could read over 1.000

Reported: Parker Gibbons showed a fielding percentage above 1.000 in
2025. Root cause: `fld()` divided by the separately-recorded `TC`
(total chances) field, but checked against the real data and found 8
of 122 real season rows (across 7 different players) where `TC` didn't
actually equal `PO+A+E` — Parker's 2025 was 37 PO + 16 A over a recorded
TC of 51 (53/51 = 1.039), when a real chances total can't be lower than
putouts plus assists alone. Fixed by deriving the denominator from
`PO+A+E` directly instead of trusting the independently-recorded TC
value, which makes a fielding percentage over 1.000 mathematically
impossible regardless of how TC itself was entered. Verified zero
season rows exceed 1.000 after the fix, across every player.

## 2026-09-20 — Found and fixed the actual source of Parker's fielding error

Follow-up to the fielding % fix above: traced the real cause instead of
just papering over it with a formula change. Pulled Parker Gibbons'
2025 fielding lines game-by-game from `source/BWB League Lineup
Export.xlsx` (`Player_Stats_with_Game_Info`, the actual per-game sheet
`build.py` reads) and checked every game's own TC against PO+A+E —
every game reconciled except one: 7/30/25, Gladiators @ Kraken (the
5-inning game that day), recorded as 4 TC against 2 PO + 4 A + 0 E
(should total 6). Confirmed against the real game that the correct
total was 6 chances, meaning TC was under-recorded that game, not PO
over-recorded as first suspected. Corrected Parker's 2025 season row in
`players.json`: TC 51 → 53, matching PO+A+E exactly. The `fld()` formula
fix from the previous entry stays either way (it doesn't trust TC), but
now the season's own recorded TC is also actually right, not just
inert.

## 2026-09-20 — Real per-game fielding data; box score and Game Log fielding tables

Imported 1150 real per-game fielding lines from `source/BWB League Lineup
Export.xlsx` (`Player_Stats_with_Game_Info`, header row 2) into each game's
`away`/`home` side as a new `fld` array (`n, inn, tc, po, a, e, dp` per
player), filtered to `G>0`, phase-matched against each game's own stored
`phase` (the export mixes Regular and Playoffs with no phase column),
deduplicated against a known duplicate-row artifact in the export (Victor
Cottini, GameID 29053877), and reconciled through 3 name aliases (Daniel
Brady → Dan Brady, Nick Sabino → Nikolas Sabino, Tommy Giandomenico → Tom
Giandomenico). Each side's `fld` array sorts by TC descending, same
convention as pitching sorted by IP.

Used that data for two new features:
- **Box scores** — a third Fielding table per team, alongside Batting and
  Pitching, guarded so older/un-imported games without `fld` data don't
  render an empty table.
- **Player Game Logs** — split the old single combined batting+pitching
  table into three independent Hitting / Pitching / Fielding tables (each
  omitted when a player/year has no rows for it), matching the same
  separation the Stats tab already uses. Also expanded the Hitting and
  Pitching column sets (added 2B/3B/HBP and BB/W/L/SV) now that each table
  has its own row instead of sharing space.

Also checked the 7 other players previously flagged with `TC != PO+A+E`
in their stored season totals (Daniel Cochrane 2022, David Pizzutello
2023, Jack Leary 2022, Michael Sullivan 2024, Peter Sposato 2022, Vinny
Spoto 2024 and 2025). Re-verified each one directly against the
phase-matched, deduplicated, alias-corrected per-game export: all 7
season totals are already correct as stored. The remaining TC/PO+A+E
mismatch in those cases is a per-game-level source-data inconsistency
(the same category as Parker's, one row above), not a season-total error
— already neutralized display-side by the `fld()` formula fix, and not
individually traced to a specific offending game the way Parker's was,
since that requires the player's own real-world confirmation.

## 2026-09-20 — Fielding records, Game Log totals, and the other 7 TC fixes

Three follow-ups to the fielding work above:

- **Fixed the other 7 players' `TC != PO+A+E` season rows** (Daniel Cochrane
  2022, David Pizzutello 2023, Jack Leary 2022, Michael Sullivan 2024, Peter
  Sposato 2022, Vinny Spoto 2024, Vinny Spoto 2025) the pragmatic way this
  time, since none of them could be traced to one specific bad game the way
  Parker's could: set each season's stored `TC` to `PO+A+E` directly. This
  matches what `fld()` already assumes for every percentage shown on the
  site, so the stored field and the displayed number now agree everywhere.
- **Fielding added to the Records page** — Single-Season (Fielding %,
  Putouts, Assists, Double Plays), Single-Game (Putouts/Assists/Double Plays
  in a Game), and Postseason (both of the above, playoff-only), alongside
  the existing Batting/Pitching sections in each tab.
- **Total row added to each Game Log table** — Hitting, Pitching and
  Fielding game logs each get a footer summing that table's columns across
  the selected year, matching the "Total" row convention box scores already
  use.

## 2026-09-20 — Team page cleanup; browser tab title shortened

Dropped the "Win % by season" sparkline from team pages (and the now-unused
`teamSpark()` function) and moved "All-Time Head-to-Head" from above the
year chips to below the season content — after Game Log on a specific
year, after Franchise Roster on "All years". Also shortened the
`<title>` tag from "BWB Wiffleball Career Register" to "BWB Wiffleball",
since that's what shows up as the name when someone bookmarks the site or
adds it to a phone's home screen.

## 2026-09-20 — Browser tab favicon set to the league logo

Added `<link rel="icon">` and `<link rel="apple-touch-icon">` tags using
`leagueLogo` from `players.json` (the same logo already shown in the
header) as a base64 data URI, embedded at build time by `generate.py`.
Whenever the league logo is updated through the site's own editor, the
next `python3 generate.py` picks up the new image for the favicon
automatically — no separate favicon file to keep in sync.

## 2026-09-20 — Fielding % qualifier, fresh-season defaults, logo/directory tweaks

Several smaller fixes and requests together:

- **Fielding % qualifier changed to innings, not games** — Single-Season Fielding %
  (Leaders and Records) now needs 30+ innings fielded to qualify, replacing the old
  9-games bar (which let very short, small-sample fielding stints post an inflated
  percentage). Leaders' career-mode Fielding % and the Records Postseason tab are
  unchanged. Both pages' qualifier text updated to say so.
- **Team/Player/Leaders pages now always open on the most recent season** — the
  year (`teamYear`, `logYear`/`splitYear`, `leadYear`) is reset on every fresh
  hash navigation into these pages, not just on first load. Previously the site
  could carry over a stale year from whatever you'd last looked at — e.g. viewing
  Team A's 2017 season, then clicking into Team B, used to keep showing 2017 for
  Team B too (or "All years" if that had been selected) instead of Team B's own
  most recent season.
- **Header logo and favicon switched to the 15th Anniversary logo** — both now
  read `DB.anniversaryLogo` first, falling back to `DB.leagueLogo` if it's ever
  unset.
- **Players directory "Tm" column renamed to "Teams"** (directory only — the
  Leaders page's own Tm column is untouched) and its team logo chips enlarged
  from 18px to 24px.

## 2026-09-20 — Bigger header logo, same header bar size

Went through a few rounds trying to grow the header logo (now the 15th
Anniversary logo) without also growing the navy header bar itself:

- 80px → 108px → 150px tall (still contained in normal flow) — each step
  grew the bar's total height along with it, since the header row's
  height is driven by its tallest item.
- 100px logo with padding trimmed 20px → 10px, aiming to keep the *math*
  (padding + logo) equal to the original 120px total — still read as
  too big, because the true original height was never just padding +
  logo; the "Established in 2012" subtitle stacked underneath the logo
  row was always the taller, height-driving element (~107.67px), not
  the logo itself.
- Landed on: restore the original 20px padding, and give `#brandLogo`'s
  wrapper a fixed 80px/150px box (matching the original logo's footprint
  exactly) so it no longer drives the row's height at all, while the
  actual `<img>` inside renders at 150px, absolutely positioned so it
  overflows *outside* that box (bleeding down past the header's bottom
  edge). Verified by measuring the live header's rendered height against
  the pre-session original — identical (147.67px) — and confirmed the
  overflow lands in the gap before the games ticker, not on top of it,
  on both desktop and mobile widths.

## 2026-09-20 — Team Fielding added to Standings

Added a "Team Fielding" table next to Team Batting and Team Pitching on
the Standings page's Team Stats section — INN/TC/PO/A/E/DP/FLD%, same
Regular/Playoffs toggle, summed from the same per-team roster rows
(`ZERO_KEYS` already carried the fielding fields, so no new aggregation
was needed). Only populated for years with per-game fielding data
imported (2020 on) — earlier years show zeros, same as the batting/
pitching tables already did before fielding stats existed.

## 2026-09-20 — Home page hero photo turned into a ticker

The single champion photo+caption card on the home page is now a
`DB.homeTicker` array of slides (`photo`, `tag`, `title`, `caption`,
`link`, `linkText`) — each slide's caption links wherever `link` points
(any in-site hash route, e.g. a team, player, or standings page), with
prev/next arrows and dot indicators once there's more than one slide.
Seeded with a single entry replicating the exact champion card that was
there before (converted from `CHAMPS[0]`), so nothing changed visually
yet — verified pixel-for-pixel against the old output, and that a fresh
Home visit always resets to slide 1 the same way Team/Player/Leaders
pages reset to the latest season.

There's no in-page "add a slide" editor — the old edit buttons across the
site (banner, logos, photos, seasons) all depend on `ARTIFACT_CAP`
(`window.claude.use('artifact')`), which only exists inside a Claude
Artifact iframe. On the real bwbwiffleball.com deployment (plain GitHub
Pages, no `window.claude`), `ARTIFACT_CAP` is always null and every one
of those edit buttons just shows "Editing isn't available in this view."
They've been silently dead since the move off Claude Artifact hosting
earlier this project — worth knowing if any of them are still expected
to work. New ticker slides get added the same way the rest of this
session's content changes have: ask for one to be added to
`homeTicker` in `players.json`, with a photo, caption, and a link.

## 2026-09-20 — Actually fixed the header logo (wrong root cause earlier)

The previous "same header bar size" fix used an absolute-positioning
overflow hack: `#brandLogo`'s wrapper was pinned to its original 80×150
footprint so it wouldn't affect the header row's height, while the real
150px image overflowed past that box. That created a bug this fix
report missed at the time — the overflowing image spilled *down* past
its own wrapper and into "Established in 2012," because that subtitle
sat in the very same column, directly below the logo+title row, with no
gap. It looked fine in the screenshots taken then only because the
overlap didn't happen to obscure legible text at that viewport.

Real fix: restructured the header markup so the logo is a sibling of the
*entire* text block (title + subtitle stacked together, `.brandtext`)
rather than just the title — `<span id="brandLogo">` and
`<div class="brandtext">` are now both direct flex children of
`.brand`, centered against each other. This puts the logo back in
normal document flow (no absolute positioning, no overflow trickery),
sized to whatever looks proportionate against the *two-line* text block
next to it, with zero overlap risk since they now sit in separate flex
columns rather than stacked in the same one. Landed on 150px after
comparing 110/130/150 side by side — all read clean at that width, and
150px best matches the size actually asked for earlier. Verified at both
desktop and mobile widths, measuring actual rendered box positions
rather than trusting a screenshot alone this time.

## 2026-09-20 — Trimmed header bar height

Reduced `.mast-inner`'s vertical padding from 20px to 12px top/bottom,
shrinking the header bar from 190px to 174px, without touching the logo
(still 150px) or any text size — a plain padding trim now that the logo
and title/subtitle are laid out as normal flex siblings, no overlap risk
to account for either way. Checked at desktop and mobile widths.

## 2026-09-20 — Updated ProWiffleball link

Changed both ProWiffleball footer/social links from
`prowiffleball.com/leagues/5` to `prowiffleball.com/`.

## 2026-09-21 — Sox World Series accolade; text cleanup; fixed rate-stat sorting

- **Added the Davenport Sox's 2012 World Series to their team page.** Root
  cause: `playoffs['2012'].championFull` was `null` instead of
  `"Davenport Sox"` (every other historical champion's `championFull`
  correctly points to that franchise's *current* name so old titles
  attribute to today's team page — e.g. 2013/2015 point to "Brookside
  Kraken" — but the Sox folded and have no current-day successor, so it
  should have pointed at the franchise's own name instead of being left
  null). Fixed the data, and also added a `teamAccolades()` call to
  `renderHistoricalTeam()` — the page for folded pre-2017 franchises
  never rendered a Team Accolades section at all before this, for any
  team, so this also makes any future defunct-team title show up the
  same way a live franchise's does. The Sox's page now shows both their
  World Series trophy and their 2012 division pennant.
- Removed "Leaders use regular-season totals. Generated ... from the BWB
  League Lineup export." from the bottom of the home page, and the
  "N games. Box scores are built from the recorded player lines — 2017–19
  games were usually logged as a single line per team..." note from the
  Games page (shown regardless of which year was selected).
- Replaced the site footer's "@bwbwiffleball · BWB Wiffleball Career
  Register" with "BWB Wiffleball Est. 2012".
- **Fixed OPS (and every other sub-1.000 rate stat) sorting wrong on
  sortable tables** — team roster pages, Records, anywhere a column uses
  the generic click-to-sort `makeSortable()` helper. Root cause: its
  numeric parser regex (`-?\d+\.?\d*`) required a digit *before* the
  decimal point, so a value like `.847` (this site drops the leading
  zero on rate stats, standard baseball convention) matched starting
  from the digits after the dot, parsing as `847` instead of `0.847` —
  meaning anything under 1.000 sorted as if it were an 800+ value,
  while anything 1.000 or over (OPS+, multi-homer games, etc.) sorted
  correctly, so the two groups interleaved randomly instead of sorting
  as one continuous range. Changed the regex to `-?\d*\.?\d+` (digits
  before the dot now optional, at least one required after), verified
  against a real Brentwood Braves roster (`.397` now correctly sorts
  below `.955`/`.975`, both correctly below `1.359`+), and confirmed
  plain integer and text columns still sort exactly as before.

## 2026-09-21 — Fixed Trevor Meyler's 2019 jersey number

His 2019 Regular season row with the Brookside Panthers had `num: "5"`;
every other year 2020–2026 has him at #20. Corrected 2019 to `"20"` per
confirmation he wore #20 that year too. His Team History ring now shows
one continuous #20 stint with the Panthers (2019–2026) instead of
splitting into a separate 2019 ring.

## 2026-09-21 — Removed two explanatory notes

Dropped the "Each phase — regular season, postseason, the exhibition
sets..." footnote from the bottom of every player page, and "The people
who run BWB Wiffleball off the field." subtitle from the League Office
page. The inline `*`/`†` markers themselves (estimated team, 2016
extrapolated stats) still appear in their tables; the Players directory
page keeps its own separate legend explaining `*`.

## 2026-09-21 — Franchise header color, phantom "Shraken" team, Beavers box score pages, open-in-new-tab links

- **Teams page**: the "Franchise" header cell in the Franchise Name History
  grid had white text on a white background — invisible. Root cause: it
  carries both `.tlg-head` (navy bg, white text) and `.tlg-name` (light
  card bg, for the sticky name column in body rows) classes, and
  `.tlg-name`'s `background` rule came later in the stylesheet with equal
  specificity, silently winning over `.tlg-head`'s navy background while
  the white text stayed. Added `background`/`color` directly to the
  existing `.tlg-head.tlg-name` combined-selector rule (higher specificity,
  wins regardless of source order) so it now matches the year columns
  exactly, in both themes.
- **"Shraken" was never a typo — corrected course after initially treating
  it as one.** Parker Gibbons and TJ Ciafone played a single 2023 Spring
  exhibition game (vs. the Panthers) as a one-off team called "Shraken,"
  already documented as exactly that further up this file. First pass at
  this got it wrong: assumed "Shraken" was a misspelling of "Kraken" and
  merged that game into Brookside Kraken's real 2023 season — undone.
  The game, both players' season rows, the Panthers' own game log, and the
  box score all say "Shraken" again, and the `nick2full` mapping is back.
  The one real fix that stays: `teams['Shraken']` — a full team object with
  its own page and its own line in All-Time Team Batting/Pitching, as if
  it were a real franchise — is deleted. A team name with no `TEAMS[]`
  entry already renders everywhere else on the site as plain, unlinked
  text (the same pattern used for "North/South Division" All-Star teams),
  so the name and box score stay intact without it needing a page.
- **Beavers tournament box scores are now their own pages** instead of
  inline `<details>` dropdowns — click a game and it opens on its own URL
  (`#/beavers/<gid>`) with a back button to the tournament, matching how
  the main league's box scores already work. The tournament page now lists
  games as clickable summary cards instead of expandable rows. A player's
  NWLA Game Log date link lands directly on the game's own page now too.
- **Champions page**: removed "N title games ·" from the header, keeping
  just the year range.
- **Internal links now support "open in new tab."** Every internal link
  on the site was a `<button data-p="...">`-style element with its own
  click handler — buttons never get the browser's native middle-click /
  ctrl-or-cmd-click / right-click "open in new tab," only real `<a href>`
  elements do. Rather than rewrite each of the ~70 button templates (and
  every render function that wires them) by hand, added a generic
  `upgradeNavLinks()` pass that swaps any `button[data-p|t|g|bv|div|series|go|beavers|ag]`
  for a real `<a>` with the matching hash as `href`, keeping every other
  attribute the same. It runs once via a `MutationObserver` on `#app`'s
  own child list — not a full subtree, since a single `innerHTML` swap
  already reports one childList change no matter how deep the new markup
  is — so it catches every render, including in-page re-renders (year
  chips, tabs) that change nothing about the hash and so never go through
  `route()` at all; the element-swap itself only touches nodes nested
  inside those children, which this observer configuration doesn't listen
  for, so it can't retrigger itself. Also found and fixed 8 CSS rules
  (`button.pname` in various contexts — division links, box-score links,
  the champion banner, leaders lists, the "15-0" game) that only matched
  actual `<button>` elements and would have silently lost their styling
  once those elements became anchors; changed them to plain `.pname` so
  they apply to both. Verified styling and click-through on the home page,
  Standings' division links, box scores, the Awards/Division all-star
  list, and an in-page tab switch (confirmed zero un-upgraded buttons
  remained afterward).

## 2026-09-21 — Removed the "About this register" note from Players page

Dropped the whole explanatory footnote (rate-stat definitions, team
lookup method, 2017 first-name matching, generation date) from the
bottom of the Players directory, along with its now-unused `footnote()`
function and placeholder element.

## 2026-09-21 — Fixed sortable tables losing their wiring on in-page re-renders

The Standings page's Team Batting/Pitching/Fielding tables (and, it turns
out, a team page's own roster tables) stopped being sortable the moment
you switched years or toggled Regular/Playoffs — sorting only ever worked
on the very first load. Root cause: `makeSortable()` needs to run again
every time a `table.sortable` gets freshly rendered, and `route()` already
does this once after every hash-based navigation — but year chips and
phase toggles call `renderStandings()`/`teamDetail()` directly, without
touching the hash, so they never go through `route()` and their new
tables never got re-wired. Some render functions (`renderDir`,
`renderTeams`, `renderLeaders`, others) happened to already call
`makeSortable` themselves after their own re-renders; `renderStandings`
and `teamDetail` never did. Rather than patch those two (and risk the
same bug resurfacing wherever the next render function forgets it),
folded the fix into the `MutationObserver` added for the open-in-new-tab
work — it already re-runs after every render anywhere on the site, so it
now also re-applies `makeSortable()` to any `table.sortable` it finds
(cheap and safe, since `makeSortable` already skips a table it's already
wired). Verified by switching years on both the Standings and a team
page and confirming a header click still reorders rows afterward.

## 2026-09-21 — Defunct franchises get year-specific names/logos everywhere; team pages get Team Hitting/Pitching/Fielding tables

- **No-Hitters/Perfect Games and Awards now show real names and logos for
  folded pre-2017 franchises**, not just live ones. Root cause: `histName`,
  `histNick`, `teamLogoForYear`, `histTeamLink` and `histNickLink` only ever
  checked `TEAMS[full]` — a franchise with no surviving roster/game data
  (Brentwood Aces, Downtown Angels, Gleason Devils, Brookside Squirrels,
  Brookside Royals, Davenport Sox) has no such entry, so they silently fell
  back to plain, unlinked, logo-less text everywhere. All five functions now
  fall back to `FRANCHISE_TIMELINE` (era-accurate historical name) and
  `FRANCHISE_SUMMARY` + `DB.franchiseLogos` (the logo, filed under the
  franchise's short nickname) when there's no live entry, and link to the
  franchise's own historical-team page (`renderHistoricalTeam`) instead of
  rendering plain text. Also added the 6 missing `nick2full` entries these
  franchises never had (Aces, Royals, Squirrels, Devils, Angels, Sox).
- **Extended the Awards page's team-abbreviation table** with confirmed
  3-letter/short codes used on pre-2018 multi-winner award rows (Golden
  Hands, Silver Slugger): Pan/PAN→Panthers, Hot/Hod→Lavahogs (Hotdoggers
  era), Ace→Aces, Kra→Kraken, Sql→Squirrels, Kin/Kig→Royals, Buf→Kraken
  (Bluefish era), Das→Braves (Dashers era), Mus/Bul→Mustangs (Bulldogs
  era), GLA→Gladiators, SHK→Shock, Wicked/Wic→Aces, Man→Lavahogs (Manatees
  era) — checked against the league's own records rather than guessed, and
  confirmed by the user. `tnick()` now also splits on commas (previously
  only "/"), since some of these rows list co-winners' teams comma-
  separated rather than slash-separated. One code, "Wia" (a 2015 Silver
  Slugger co-winner's team), has no confirmed match and is deliberately
  left unmapped — renders as plain text rather than guessing wrong.
- **Team pages: added Team Hitting, Team Pitching and Team Fielding
  tables**, positioned above the individual player roster tables on a
  team's single-year view — same column sets as the equivalent Standings
  page tables, built from the same season/phase roster aggregate already
  computed for that page's record cards. Replaces the old compact "Team
  Batting"/"Team Pitching" one-line summary cards, which are now redundant
  with the fuller tables. Each table is single-row (just that team's
  total, labeled with its era-accurate name for the selected year) and
  omits itself when there's no relevant data (no roster, no innings
  pitched, no fielding chances) — verified this still happens correctly,
  and that the "All years" view (a different code path, franchise-wide
  roster tables) is unaffected.

## 2026-09-21 — More award abbreviations, a 2014 data fix, Team of the Year links

- Added the last 3 confirmed team-abbreviation codes: `Dev`→Devils,
  `Eag`→Kraken (Eagles era), `Wia`→Aces.
- **Fixed a real data error in the 2014 awards**: three entries (Comeback
  Player of the Year, Manager of the Year, Team of the Year) had
  `team: 'Kings'` and one had `winner: 'Brookside Kings'` — but "Harris
  Kings" didn't exist until 2018; in 2014 the Brookside franchise
  playing under that division was the Royals (per its own
  `FRANCHISE_TIMELINE` entry, nicknamed "Royals" 2013–2014). Corrected
  all four to "Royals" / "Brookside Royals."
- **"Team of the Year" winners now link to the team's own page** instead
  of being run through the player-name linker (which never matched,
  since the winner is a team, not a person) — resolved via the same
  `tnick()` team-abbreviation machinery already used for the Team
  column, with the now-redundant Team column left blank on those rows
  specifically.
- Scanned every award winner for first-name-only entries (no confirmed
  last name, not a player already on file) — found exactly 4, all from
  2012: Golden Hands ("Peter, Kento") and Silver Slugger ("Kento,
  Parker"). Flagged to the user for confirmation rather than guessed at.

## 2026-09-21 — Fixed the Games page's slow load; confirmed the only other 2012 first-name winners

- **Confirmed the 4 first-name-only award winners from 2012**: Golden
  Hands → Peter Fraioli, Kento Kamezaki; Silver Slugger → Kento Kamezaki,
  Parker Gibbons. Fixed in the raw award data (Kento Kamezaki isn't in
  the player database, so his name still won't link to a page — same as
  any other name with no matching player record — but it now reads in
  full instead of just "Kento").
- **Fixed the Games page taking noticeably long to load.** Measured
  before touching anything: the default "All" view rendered 605 rows in
  **1078ms** and produced a **75MB** block of HTML with **1244** `<img>`
  tags — because only ~29 distinct team logos actually exist, but each
  one (a base64 string, tens of KB) was being copy-pasted directly into
  every row that used it, sometimes hundreds of times over, instead of
  being stored once. Two fixes:
  - Registered each of the ~29 distinct logos (every team's current logo,
    every entry in its `logoHistory`, every defunct-franchise logo) as
    its own CSS class in one `<style>` block injected at boot — the logo
    data itself now appears exactly once in the page regardless of how
    many rows reference it. Added `logoIcon()` as a drop-in replacement
    for `<img class="…" src="…">` that uses the registered class (a
    `<span>` with a CSS background-image) when one exists, and only
    falls back to a real `<img>` otherwise. Applied it to the Games
    page's team cells specifically, since that's the page with by far
    the most repeated logos on one screen; other pages show far fewer
    rows at once and weren't measured as a problem.
  - The Games page also defaulted to showing every year at once ("All")
    on first load rather than the most recent year, same class of bug as
    the Team/Player/Leaders pages fixed earlier this session — now
    resets to the latest year on a fresh visit, with "All" still
    available as an explicit choice.
  - Result: the same "All" view now renders in **~22ms** (roughly 50×
    faster) and produces **367KB** of HTML (roughly 200× smaller) instead
    of 75MB. Verified logos still display correctly and every link still
    navigates properly, at both desktop and mobile widths, with the full
    605-row "All" list scrolling smoothly.

## 2026-09-21 — Shortened header subtitle

Changed "Established in 2012" to "Est. 2012" under the header logo.

## 2026-09-21 — Team Hitting/Pitching/Fielding now by-season, always shown

Follow-up to yesterday's Team Hitting/Pitching/Fielding tables: moved them
out of the single-year view (where they showed one row, only for whichever
year was selected) and merged them into `teamStatsBySeason()` as one row
per year — "Team Batting by Season" and "Team Pitching by Season" already
worked this way; added a matching "Team Fielding by Season" table using
the same year-by-year aggregate. All three now render once, right after
"Season by Season" and before the year chips, so they show every year
regardless of which one is selected — same idea as "Season by Season"
itself, rather than changing with the chips. Each year links to that
year's own detail view, reusing the click-to-jump wiring the Batting/
Pitching versions already had. Fielding omits itself entirely for a
franchise with no fielding data on record at all (e.g. Purchase PawSox),
same as before.

## 2026-09-21 — Dropped pre-2022 rows from Team Fielding by Season

Fielding wasn't tracked league-wide until 2022, confirmed against the
data itself (zero player-seasons have any recorded TC before then) — so
every earlier year in "Team Fielding by Season" was a real zero, not
just a missing one, cluttering the table with a decade of empty rows.
Filtered to only years with `TC>0`, same idea already used correctly on
a player's own Fielding tab (which already excluded these).

## 2026-09-21 — Team Stats moved below player stats, with a Hitting/Pitching/Fielding toggle

Follow-up to the by-season Team Hitting/Pitching/Fielding tables added
earlier today: moved them below the individual player Batting/Pitching
tables (and, for the single-year view, above the Game Log), and replaced
showing all three stacked with a segmented toggle (`Hitting`/`Pitching`/
`Fielding`, matching the `.segs` pattern used elsewhere) that shows one
at a time — `teamStatMode`, persisted across year switches within the
same team, reset to Hitting on a fresh visit to any team page. Fielding
still only appears as a toggle option when the franchise has any (2022
on); if it was showing and you land on a team with none, it falls back
to Hitting automatically instead of showing an empty toggle state.

## 2026-09-21 — Cropped the 2026 Kraken logo tighter, matched to the older eras' size

The Brookside Kraken's current (2026-on) logo had a lot of transparent
padding baked into its 320×320 canvas — the actual artwork only filled
about 54% of the width and 71% of the height — so it rendered visibly
smaller everywhere on the site (team page, box scores, Games list,
Standings, leaders, etc.) than the franchise's own 2012–2022 and
2023–2025 logos, which fill roughly 85–92% of their own (non-square,
238×320) canvas. First pass cropped to the artwork's bounding box but
kept a square 320×320 canvas, landing at 66%/87% fill — closer, but
still not matching the older logos' scale. Redid it properly: cropped to
the bounding box (173×228, almost the same aspect ratio as the older
logos' own canvas) and built a new canvas sized to that content plus a
small 5% margin per side — 192×253, non-square like the older ones —
landing at 88%/88% fill on both axes, matching them directly rather than
approximating a fixed square.

That non-square version turned out to be wrong for one specific spot:
the team page's own hero logo (`.tlogo`, a 92×92 box) uses `object-fit:
cover`, not `contain` — `cover` fills the box completely by cropping
whatever doesn't fit, rather than letterboxing. A 192×253 portrait image
inside a 92×92 square `cover` box gets scaled to match on width, which
pushes its rendered height well past 92px — the box then clips the
excess off the top and bottom, cutting into the actual logo mark (the
top of the tentacles, part of the team-name banner), not just empty
margin. Every other team's logo is already stored on a square canvas,
which is exactly why this never came up for them. Redid the crop as a
square canvas (259×259) instead, sized to the artwork's longer dimension
plus a 6% margin — 65%/86% fill (lower on width than the portrait
version, since the mark itself is taller than it is wide and that's not
croppable away without cutting content), but critically no longer clips
anything in the `.tlogo` box, since a square source in a square `cover`
box needs no cropping at all. Only this one era's logo was touched.

## 2026-09-21 — Cropped the anniversary logo tighter; Peter Fraioli's title

- **Browser tab icon "bigger."** A browser renders its own tab favicon at
  a small, fixed size — there's no HTML/CSS lever to make that bigger.
  What *is* controllable is how much of the source image's own canvas the
  artwork fills, same issue as the Kraken logo above: the 15th Anniversary
  logo (used for both the favicon and the header logo, since they share
  the same image) only filled about 49%/74% of its 320×320 canvas.
  Cropped to its bounding box and rebuilt on a snug canvas (~90% fill,
  172×259) the same way — bigger-looking wherever it's used, tab icon
  included, without changing any CSS.
- Changed Peter Fraioli's League Office title from "Head of Content
  Management and Design" to "Director of Social and Digital Content."

## 2026-09-21 — Reverted the anniversary logo crop

The tighter crop from the previous entry made the header logo and tab
icon look too big. Reverted `anniversaryLogo` back to its original,
more-padded image; the header logo's own 150px display size and the
favicon setup are unchanged, so this is a straight revert of the image
data only. The Kraken team logo crop from earlier today is unaffected —
this only touched the anniversary logo shared by the header and favicon.

## 2026-09-21 — Fixed truncated era names in the Franchise Name History timeline

The cut-off names weren't in the "Franchise" column (measured — nothing
there was actually overflowing) but in the era-nickname bars themselves:
a franchise's single-year eras only got one ~58px-wide grid column, too
narrow for longer nicknames like "Sea Thieves" or "Hotdoggers" — both
were losing their last letter to `text-overflow: ellipsis` without it
even being visually obvious at that size. Widened each year column from
58px to 76px (enough for "Sea Thieves," the longest single-year
nickname, measured directly rather than estimated) and bumped the grid's
own min-width to match, so the horizontal scroll area is sized correctly.
Also removed "Hover a bar for the full name" from the caption underneath.

## 2026-09-21 — Fixed 2018 World Series game order

Games 1 and 2 of the 2018 World Series (Brookside Kraken vs. Harris
Special K's) were showing reversed — the 6–3 game as Game 1, the 16–14
game as Game 2. Root cause: both games are recorded with the identical
date (`2018-08-17`) and neither had a `dt` timestamp to break the tie,
so the series page's date-based sort fell back to gid order, which
happened to land backwards for this pair. Added `dt` values to both
games (`08:00` and `10:00`) — the same mechanism already used for every
other same-day doubleheader on the site — so the 16–14 game now sorts
first, per the actual order confirmed by the user. Verified on both the
series page and the Standings page's playoff bracket, which independently
reconstruct game order the same way.

## 2026-09-21 — Champions page shows era-accurate team names

Each championship year's heading now shows the franchise's name as it
actually was that season (e.g. "2018 — Harris Special K's," "2020 —
Harris Special K's") instead of the current name ("Harris Kings")
applied retroactively — using `histTeamLink()`, the same era-aware
helper already used elsewhere on the site, so the link target is
unaffected: it still points at the current franchise page. Removed the
small "aka Harris Kings" subtitle that used to sit next to the score,
since the heading itself now carries that information directly instead
of showing it twice.

## 2026-09-21 — New "Player Awards" page per team, grouped by award

New page (`#/t/<team>/awards`) showing every individual award a
franchise's players have won, grouped by award type (MVP, CY Young,
Golden Hands, etc.) rather than by year like the main Awards page —
linked from a small "Player Awards →" button in the Team Accolades
section, per the user's own placement call, rather than embedded in the
team page itself.

Awards are resolved to a franchise the same way the main Awards page's
`tnick()` already does (`AWARD_TEAM_ALIAS` → `NICK2FULL`), pulled into a
new shared `teamAwardEntries(fullName)` — multi-team/multi-winner rows
from the 2012–2017 Golden Hands/Silver Slugger co-winner era are paired
positionally (team #2 in the list with winner #2), falling back to the
raw winner string on the handful of old rows where the two lists don't
line up 1:1. Team-level honors (Team of the Year, Sox Trophy, Game of
the Year) are excluded, since their "winner" is a team or a game, not a
player. Hoisted the award-type ordering list (`AW_ORDER`) that already
existed inside a player page's own accolades function up to a shared
top-level const, rather than duplicating it.

Works for folded pre-2017 franchises too (checked against `Davenport
Sox`, `Brentwood Aces`, etc. — all have individual awards on record) —
uses the same `franchiseIsLinkable()` / `teamLogoForYear()` fallbacks
already built for defunct-team support elsewhere, rather than assuming
every team has a live `TEAMS[]` entry.

**Follow-up same day**: reworked the layout per feedback — dropped the
Notes column and swapped the per-award `<table>` (Year/Player/Notes)
for a compact card (`.pa-block`/`.pa-list`, new CSS) just listing
"YYYY — Player" per line, laid out in a `.pa-grid` (the same responsive
`auto-fit` grid pattern the Leaders page's `.llgrid` already uses) so
several award cards sit side by side instead of one full-width table
per award stacked vertically. Verified at both desktop and mobile
widths — the grid reflows to as many columns as fit.

## 2026-09-21 — Basic SEO: sitemap, robots.txt, Open Graph/Twitter cards

The low-risk SEO pieces discussed earlier: added `robots.txt` (allow
all, points at the sitemap) and `sitemap.xml` at the repo root. The
sitemap lists only the root URL — this is a hash-routed single-page app
(`#/players`, `#/t/...`, etc.), and Google doesn't treat a hash fragment
as a separate crawlable page, so listing fake "pages" for every route
wouldn't do anything; the whole site is realistically indexed as one
page regardless of what's in the sitemap. Also added `<link
rel="canonical">`, Open Graph tags, and Twitter Card tags to the page
head so shared links get a proper preview card instead of a bare URL.

Open Graph images have to be a real fetchable URL — a `data:` URI (how
every other image on this site is stored, since there's no separate
asset host) doesn't work for `og:image`/`twitter:image` on any major
platform. Extracted the 15th Anniversary logo out to a real static file,
`og-image.png` (1200×630, centered on the header's navy brand color —
the standard OG image size, so it isn't cropped oddly), committed
alongside `index.html`, `CNAME`, etc.

None of this gets individual pages (a specific player, a specific team)
showing up in search on their own — that would need real per-page URLs
instead of hash routing, a much bigger change than what was asked for
here. This is the site's homepage becoming properly indexable and
sharing well, not deep-link search results.

## 2026-09-21 — Bigger tab icon, decoupled from the header logo this time

Last attempt at "bigger tab icon" cropped `anniversaryLogo` itself,
which also changed the header logo (shared field) — reverted that
because it made the header too big. This time added a separate
`faviconLogo` field: the same anniversary logo cropped to its real
bounding box on a tight square canvas (58%/89% fill, up from 49%/74%),
used only by `LEAGUE_LOGO` in `generate.py` for the `<link rel="icon">`
/ `apple-touch-icon` tags. The header's own logo code still reads
`DB.anniversaryLogo` directly and is untouched — verified the header
screenshot is pixel-identical to before, and that the favicon and
header logo are now two distinct images (`same: false`) rather than the
same shared one.

## 2026-09-21 — Beavers roster cards, boxed game cards, team leadership, NWLA rename

Added a "Roster" section to each Beavers tournament page: one player card
per roster member (headshot + name + a one-line batting/pitching stat
summary), reusing the League Office page's existing `.officecard` styling
rather than inventing a new look. Redesigned the tournament's "Box score"
links from bare text into boxed game cards matching the postseason
series page's `.pb-match` style (team names, scores, win highlighting,
game time, boxed "Box score →" link), replacing the old ad hoc
`.bvgamecard` styling (removed as dead code). Found and fixed two more
instances of the anchor-upgrade CSS bug hit earlier this session
(`button.X` selectors that silently stop matching once the anchor-
upgrade system converts a `<button>` to a real `<a>`): `.pb-score
button.pb-boxlink` → `.pb-score .pb-boxlink`, and `button.acc-pennant` /
`:hover` → `.acc-pennant[href]` / `:hover`.

Also added a "Leadership" block to the Beavers overview page (Parker
Gibbons as captain, Peter Fraioli and Trevor Meyler as co-captains),
reusing the existing franchise `LEADERSHIP`/`teamLeadershipHtml()`
system rather than a bespoke display — made the co-captain `(years)`
suffix optional since the Beavers entry has no year ranges, unlike the
BWB franchise entries.

Renamed the NWLA event from "NWLA National Tournament" to "NWLA
Tournament" (the `event` field in `players.json`) since the "National"
qualifier wasn't wanted.

## 2026-09-21 — Beavers roster grid polish, tournament dates/MVP, real event logo

Follow-up pass on the same day's Beavers work. Roster cards: switched
to a fixed 6-column grid (`.officegrid-6`, collapsing to 3/2 columns on
narrow screens) instead of auto-fill, dropped the per-player stat line
(headshot + name only), and put the captain/co-captains first so they
land on the top row — reuses the existing `LEADERSHIP` data rather than
hardcoding names.

Fixed the tournament date display: the "2026-08-15" field is a single
day used as the routing key (`bvTournamentHref`) and had to stay as-is,
so added a separate `dateLabel` ("Aug 14–16, 2026") shown instead of
the raw date on the tournament page. Also dropped the age-division code
("18O") from that same line — it was `meta.level`, not something the
user wanted surfaced.

Added a "Team Tournament MVP" award for Victor Cottini (2026 NWLA
Tournament): added to his existing `honors.awards` array so it shows
on his own player page's Accolades card for free, and surfaced it as a
new `bvMvpLine()`/`meta.mvp` field on both the Beavers overview page's
tournament card and the tournament's own hero. Kept it out of
`honors.awards`'s usual `AW_ABBR` map on purpose, since it's a
tournament honor, not a BWB league award, so it doesn't show up in the
season-table Awards column or count toward league award leaderboards —
only in the player's own Accolades list, where the year was changed to
`"2026 NWLA Tournament"` so it reads as that specific event, not a bare
year.

Added the tournament's own event logo (provided by the user, an NWLA/
St. Louis badge) as a new `eventLogo` field, separate from the
Beavers' `logo` (the beaver mascot, still used for the franchise-level
hero at the top of the Beavers overview page). `eventLogo` is portrait-
shaped (825×1000) with content bleeding to every edge — no negative
space to crop, unlike the earlier Kraken logo fix — so it was placed on
a square, mostly-transparent canvas (94% fill by height, letterboxed
left/right) rather than cropped, so `object-fit:cover` in the `.tlogo`
box displays it whole.

## 2026-09-21 — Drop OPS+/ERA+ from NWLA Tournament stats

OPS+/ERA+ compare a season against that year's BWB league average —
meaningless for the NWLA Tournament, an outside national event with no
BWB league games of its own to average against (Victor Cottini's NWLA
line was showing a nonsense "OPS+ 66" derived from the regular BWB
league's 2026 average). Dropped the column from `phaseBlock()`'s NWLA
batting/pitching tables and from `splitBatCols()`/`splitPitCols()`
(used by the NWLA Splits tab), rather than just hiding OPS+ and leaving
the equally-meaningless ERA+ in place. Regular-season/postseason/other
phases are untouched — verified Victor Cottini's own Regular Season
splits still show OPS+ normally.

## 2026-09-21 — Add non-playing roster members to the NWLA Tournament page

Griffin Krueger and Tommy Peck were on the 2026 NWLA Tournament roster
but didn't record any stats, so they were invisible to `bvRosterGrid()`
(it only ever derived names from the batting/pitching rows). Added a
new `extraRoster` field to the tournament data for names to show with
no stats to derive from, and added both to `inRegister` too so their
cards link to their player pages like everyone else's.

## 2026-09-21 — Rename per-team Player Awards page to Awards, add Team/Game of the Year

Renamed the per-team "Player Awards" page and its link button to just
"Awards" (`renderTeamAwards()`, the "Awards →" button on the team
page). Team of the Year and Game of the Year were previously filtered
out of `teamAwardEntries()` via `NON_PLAYER_AWARDS` on the assumption
that page was individual-player awards only — now that it's just
"Awards", both are included (their "winner" is a team name or a game
description rather than a player, but `plink()` already displays a
non-player string as plain text with no crash). Left the Sox Trophy
filtered out since it's a regular-season tiebreaker, not a standalone
award. Verified on Davenport Sox (Team of the Year), Shelton Shock
(4 Game of the Year entries), and Brookside Kraken (both, plus
confirmed its 2025 Sox Trophy still doesn't show).

## 2026-09-21 — Link Game of the Year to box scores, award data corrections

Linked every "Game Of The Year" award (2022–2026, all confirmed as
regular-season games, never postseason) to its actual box score, on
both the main Awards page and each team's own Awards page. Matched
each award's "Team A @ Team B Game N" label to the real `gid` by
finding that day's head-to-head games and using chronological (gid)
order for "Game N", cross-checked against each award's own note where
one existed (inning count, score, described plays). Also normalized
the older "Team A V Team B" wording to "Team A @ Team B" for
consistency (2022, 2023, and the 2026 finalists list).

Fixed a structural inconsistency on the main Awards page: "Team of the
Year" was the only award type putting its team in the Winner column
and leaving Team blank. Winner now always shows the raw record
(plain text for Team of the Year, since the winner there already is a
team, not a player) and Team always shows the linkable team badge,
matching every other award row.

Data corrections to the hand-kept award records, per user review:
- 2012 CY Young (Darien Sharpe) was attributed to Harris Kings; he was
  on the Brookside Royals — fixed the award's team field.
- 2013 Silver Slugger (South) was missing a team for 2 of its 4
  co-winners because the old row only listed 3 team codes for 4
  names — added Tochi Onwuasoanya (Downtown Angels) and Darien Sharpe
  (Brookside Royals) to the row so both now show up on the right
  franchise's Awards page.
- Renamed the one "Avondale Dashers" mention (a 2017 Team of the Year
  winner) to "Brentwood Dashers" — `TEAMS['Brentwood Braves'].loc` is
  already `'Brentwood'` for that era everywhere else on the site (team
  pages, player history), so `FRANCHISE_TIMELINE`'s stray `loc:'Avondale'`
  was the only place still showing the wrong location.

**Follow-up, same day** — got the missing teams from the user and
finished both rows: 2013 Golden Hands (South) — Davis Kim was on the
Kraken; 2014 Golden Hands (South) — Shintaro Sakurai (corrected from
"Sakurari") and Joey Cardascia were both Squirrels, Masayuki Yamada
was a Royals; also moved the 2014 Silver Slugger (South) row's Kodai
Tachimoto from Brookside Royals to Brookside Squirrels, per the user's
confirmation, matching the site's own Leadership data.

## 2026-09-21 — NWLA Awards: new Awards tab + player accolades

Imported the league's NWLA (national tournament) award history from a
hand-kept spreadsheet — Wiffy Awards (individual national honors), a
Team Award (national/regional team ranking), and four "All-NWLA-Team"
categories (Hitting, Pitching, Rookie, Fielding), each with First/
Second/Third-team selections per year back to 2015. This is a
separate, longer-running record from the Brookside Beavers' own
per-tournament roster/stat tracking (which only starts in 2026) — the
new tab's note says so explicitly to avoid confusion.

Added a third "NWLA Awards" tab on the Awards page (next to Awards and
All-Star Games), and a new accolades block on each honored player's
own page, placed directly under their league Awards block (`accolades()`
in `generate.py`), grouped by category the same way league awards are
(e.g. "All-Hitting Team ×7 — 2022 (3rd), 2021 (2nd), ..."). Reused the
existing `tnick()`/`AWARD_TEAM_ALIAS` machinery for team-name
resolution rather than building a new one; had to add a handful of new
aliases the old awards data never needed: `Sea Thieves` → Lavahogs
(its 2018 era name), `Pawsox` → PawSox (case mismatch), and `Dra`/`Shk`
for the one mid-season-trade entry ("David Pizzutello - Dra/Shk"),
which now correctly shows both team badges.

Two names needed correcting against the player database during import:
"Daniel Brady" → Dan Brady, "TJ Fuerst" → T.J. Fuerst (kept unlinked —
he has no player page, same as several other pre-2017 award-only
names elsewhere on the site).

## 2026-09-21 — Flatten the All-NWLA-Team tables

The four All-NWLA-Team tables (Hitting/Pitching/Rookie/Fielding) on
the new NWLA Awards tab started as a Year × First/Second/Third-Team
grid, matching the source spreadsheet's own layout. In practice a tie
(several honorees in the same tier the same year) stacked multiple
names inside one grid cell, so rows ended up uneven heights next to
plain "—" cells — read as convoluted next to the clean row-per-entry
Wiffy/Team Awards tables above it. Flattened each into a Year / Tier /
Player / Team table, one row per honoree, matching that same style.

## 2026-09-21 — NWLA Awards on the per-team Awards page

Added a new `teamNwlaEntries()` (mirrors `teamAwardEntries()`, but over
`NWLA_AWARDS` instead of `AWARDS`) and a "NWLA Awards" section on each
franchise's own Awards page, right under its BWB league awards —
grouped the same way (award/category, years, tier where relevant).
A team code that's a "/"-joined pair (a player traded mid-season, e.g.
"Dra/Shk") now correctly credits BOTH franchises, same as a traded
player's stat lines do elsewhere on the site — verified David
Pizzutello's 2022 All-Rookie Team nod shows on both Purchase Dragons'
and Shelton Shock's Awards pages. Also fixed `teamAccolades()`'s
`hasAwards` check (which gates whether the "Awards →" button shows at
all) to count NWLA-only honors too, so a franchise with NWLA awards but
no BWB league awards still gets a reachable Awards page.

## 2026-09-21 — Align the two division standings tables' columns

Each division's standings table sized its own "Team" column based on
that table's own team-name lengths (default `table-layout:auto`), so
a division with "Silver Lake Snapping Turtles" ended up with a wider
Team column — and every column after it shifted out of alignment —
than a division whose longest name was shorter. Set `table-layout:fixed`
on `.stand` with an explicit 34% width on the Team column, so both
tables split their columns identically regardless of content. Checked
2018 (longer names, 3 teams/division) and 2026, desktop and mobile.

## 2026-09-21 — Fix wrapping total row on team Season by Season, rename to All-Time

The Home/Away/vs-Brookside/vs-Brentwood cells (`fmtSplit()`, "W–L
(PCT)") were wrapping the "(PCT)" part onto a second line only in the
Season by Season table's total row — every season row above it stayed
on one line. Root cause: `tbody td` already had `white-space:nowrap`
site-wide, but the equivalent `tfoot td` rule didn't, and this total
row is the only `<tfoot>` on the page that uses `fmtSplit()`'s inline
format. Added `white-space:nowrap` to `tfoot td` (benefits every other
total row on the site the same way, none of which had this problem
visibly since they don't use fmtSplit's parenthetical format). Also
renamed the row from "Career" to "All-Time", matching the team-level
(not player-level) framing of the table.

## 2026-09-21 — Fill in pre-2018 franchise logo history

The user provided a batch of 53 exported team logo files, several of
them dedicated art for a franchise's early, pre-rename identity that
had never had its own logo on the site — those years were just
showing whatever logo came later, since `logoHistory` had one entry
spanning the whole gap. Added 12 new era-specific logos (all already
square 1080×1080 art except one, letterboxed on a transparent square
canvas the same way as the NWLA logo earlier) and split/adjusted the
surrounding `logoHistory` ranges to match `FRANCHISE_TIMELINE` exactly:

- Brookside Kraken: added Capitals (2012), Eagles (2013–2016),
  Bluefish (2017); existing logo re-scoped from 2012–2022 to 2018–2022.
- Beaver Brook Lavahogs: added Tornadoes (2012), Warriors (2013–2014),
  Manatees (2015), Hotdoggers (2016), Hogriders (2017), Sea Thieves
  (2018); existing logo re-scoped from 2012–2020 to 2019–2020.
- Brookside Panthers: added Jackals (2012); existing logo re-scoped
  from 2012–2020 to 2013–2020.
- Brentwood Mustangs: added Bulldogs (2016), splitting the old
  2015–2018 entry into 2015 and 2017–2018 (same logo, both sides of
  the Bulldogs year).
- Glenwood Process: added Wildcats (2017); existing logo re-scoped
  from 2017–2021 to 2018–2021.

**Not applied, needs a decision:** the batch also included Boulders
(2012) and Bears (2012), the pre-rename identities of the fully-
defunct Brookside Squirrels and Brookside Royals. Those two franchises
have no `TEAMS[]` entry, so their logo comes from the flat
`DB.franchiseLogos` map (one logo per franchise, not year-aware) —
using these would need that map to support a `logoHistory`-style array
the way live franchises' `TEAMS[].logoHistory` already does. Skipped
for now rather than build that for two franchises without checking
first.

**Also not touched:** everything else in the batch either already had
a dedicated logo covering that exact same span (current Kraken/
Panthers/Shock/Braves/etc. eras, Special K's, the existing Sox/Royals/
Aces/Squirrels/Angels/Devils defunct-franchise logos) or is a special
asset that already exists (Postseason/World Series logos 2024–2026,
the two division logos, the anniversary/league logo) — since the user
described this batch as "the old logos," I treated it as filling
gaps rather than re-exporting things already on file, but can swap
any of those in too if the new export is meant to replace them.

## 2026-09-21 — Add Boulders/Bears logos to the Squirrels/Royals pages

Extended the defunct-franchise logo system so it can be era-aware,
the same way live franchises' `TEAMS[].logoHistory` already is.
`DB.franchiseLogos[nick]` now supports either a single data URI (still
true for most defunct franchises) or a `logoHistory`-shaped array of
`{from,to,logo}` — new `franchiseLogoDefault()`/`franchiseLogoForYear()`
helpers handle both shapes, and every call site that used to read
`DB.franchiseLogos[...]` directly (search, the Teams directory, the
Franchise Name History timeline row icon, the Champions page, and
`teamLogoForYear()` itself) now goes through one of them.

Converted Brookside Squirrels and Brookside Royals to the array form
using the Boulders (2012) and Bears (2012) logos from the same batch,
paired with each franchise's existing Squirrels/Royals-era logo for
2013 on. Added `historicalLogoHistory()` — the defunct-team-page
equivalent of live teams' `teamLogoHistory()` — so
`renderHistoricalTeam()` now shows the same kind of Logo History
gallery live franchise pages already have, gated the same way (a
franchise with only one era, i.e. every other defunct franchise on
the site, doesn't get an empty gallery).

## 2026-09-21 — Era-accurate names for live franchises' pre-2017 years

The previous pass added era-specific logos for 5 franchises' pre-2017
years (Kraken, Lavahogs, Panthers, Mustangs, Process), but the era-
specific *names* were still wrong for those same years: `histName()`/
`histNick()` only checked a live franchise's `nameByYear`, which only
covers its tracked seasons (2017 on) — any earlier year fell straight
through to the franchise's current nick. A 2013 Golden Hands award for
the Kraken franchise was showing "Kraken" instead of "Eagles", right
next to a Team badge that (after the logo fix) correctly showed the
Eagles logo — a name/logo mismatch. Both functions now fall back to
`FRANCHISE_TIMELINE` (the same data the logos already use) whenever
`nameByYear` has no entry for that year, before defaulting to the
current nick. Verified on the Awards page (2013 Golden Hands/Silver
Slugger South now read Eagles/Warriors instead of Kraken/Lavahogs) and
the Champions page (2013/2015 now read "Brookside Eagles").

Also caught up each franchise's "aka" list (the hero text and directory
subtitle) to match `FRANCHISE_TIMELINE` in full — Kraken, Lavahogs,
Panthers and Mustangs were each missing one or more of their own
pre-2017 names (e.g. Kraken's aka list had "Bluefish" but not "Capitals"
or "Eagles"). Process and Braves/Harris Kings were already complete.

## 2026-09-21 — Fix severe page-load slowness (same bug as the old Games page, spread wider)

Investigated "some pages are taking too long to load": several routes'
rendered `#app` HTML had ballooned into the tens of megabytes on every
navigation, from the same root cause the Games page hit earlier this
session (fixed there via `logoIcon()`/`LOGO_CLASS`, but that fix was
never applied to most other team-logo call sites) — a small set of
team logos embedded as raw base64 `<img src>` repeated across every
row of a large list, instead of referencing the already-registered
shared CSS class. Measured before fixing (rendered `#app.innerHTML`
size per route):

- Awards: 19.3 MB → 111 KB (174×)
- Records: 12.8 MB → 52 KB (245×)
- Leaders: 11.1 MB → 45 KB (245×)
- Players directory: 9.7 MB → 80 KB (121×)
- Home: 8.0 MB → 1.4 MB (5.6×; the rest is the homepage's own
  large-image ticker/hero content, not logo duplication)
- Teams directory: 2.6 MB → 34 KB (75×)
- Champions: 5.4 MB → 4.5 MB (modest — most of this page's weight is
  genuinely unique per-year champion photos, not a duplication bug)

Root-caused each one to a specific call site still doing raw `<img
src="${logo}">` instead of `logoIcon()`: `tnick()` (the Awards page's
Team-column badge — the single biggest offender, used for both the
main Annual Awards table across 15 years and every NWLA Awards table),
`teamHistoryChips()` (a player's career-teams chips), the Home page's
"League Leaders" preview lists, two Leaders/Records-page team-cell
helpers, the season-table and game-log team cells, the header ticker,
and the Teams directory/Franchise Timeline row icons and Champions
badge. Switched all of them to `logoIcon()`, which was already built
and already used correctly on the Games page — this pass just finished
rolling it out everywhere else a team logo can repeat across many rows
on one page. No visual change (the CSS classes render identically on
a `<span>` background as they did on an `<img>`), confirmed via
computed-style checks and a console-error sweep on every affected page.

## 2026-09-22 — 15-0 game: use OPS+/ERA+ instead of plain OPS/ERA

The 15-0 draft-and-simulate game projects a drafted team's runs scored/
allowed by comparing its combined OPS/ERA against a single flat
all-time league average — but the draft pulls player-seasons from
2017 through today, and this league's own scoring environment has
shifted a lot over that span, so a season judged only against a flat
all-time number was over- or under-rated purely by which year it
happened to come from. `b0Simulate()` now computes team OPS+/ERA+ via
the same `opsPlusFor()`/`eraPlusFor()` already used everywhere else on
the site — weighted by each pick's own year's league average, not one
blended number — and the run projection and result text both use those
instead of raw OPS/ERA. Left the draft-pool stat line (what you see
per player while picking, e.g. ".560/.703/1.289 · 9 HR") as real,
unadjusted single-season numbers — that's a look at one real season in
isolation, not a cross-era comparison, so it doesn't have the same
problem. Verified in both Practice and Today's Draft modes.

## 2026-09-22 — Grid game: reveal each square's full qualifying pool once done

Each square already showed a count ("6 players qualify") once answered,
but only the count — the actual list stayed hidden even after the
whole grid was finished. Added a per-cell `<details>` reveal, only
computed and rendered once all 9 squares are attempted (nothing to
spoil mid-game), listing every real qualifying player as a link to
their page. Had to change `.gcell` from a fixed `height` to
`min-height` so an expanded cell can actually grow the table row
instead of overflowing it, and dropped an initial 2-column list layout
after finding it visually interleaved two names into unreadable mush
in the grid's ~104px-wide cells — a single column reads fine and
scrolls internally past ~200px for a large pool.

## 2026-09-22 — Fix Grid boxes shrinking (regression from the pool-reveal change)

The pool-reveal change swapped `.gcell` from a fixed `height:96px` to
`min-height:96px`, on the assumption a fixed height would clip an
expanded reveal. It doesn't need to — a table cell already lets its
row grow past a fixed `height` when content demands more room, which
is exactly why the reveal worked in testing either way. What `min-height`
actually did was make Chrome stop reliably sizing the cell to 96px at
all: an unanswered "Guess" box measured ~46px tall instead of 96,
because `min-height` on a table cell isn't honored the same way
`height` is. Reverted to `height:96px` — verified boxes are back to
normal size, and a 15-name reveal still correctly grows its row
(checked at 289px) without needing the min-height in the first place.

## 2026-09-22 — Add team photo to the 2026 NWLA Tournament page

Added the user's team photo (the roster at the stadium field) to the
2026 NWLA Tournament entry as a new `photo` field, shown above the
Roster section on `renderBeaverTournament()` — reused the Champions
page's `.champphoto` treatment (centered, capped height, rounded
corners, shadow) rather than inventing new styling. Resized from the
original 2048×1536 to 1600×1200 and re-encoded as JPEG (quality 82,
~380KB) to match the size/quality convention already used for the
Champions page's own team photos.

## 2026-09-22 — Fix 2015 Golden Hands (South) team attribution

Same "N winners, fewer team codes" bug as the 2013 rows fixed earlier
this session: the 2015 South Golden Hands row had 4 co-winners (Parker
Gibbons, TJ Fuerst, Joey Cardascia, Vinny Spoto) but only 2 team codes
("Eagles, Squirrels"), so positional pairing put TJ Fuerst on Squirrels
instead of Eagles (Brookside Kraken's 2015 era name) — confirmed by
the user. Added a second "Eagles" so Parker and TJ both land on Kraken
and Joey Cardascia (already confirmed as Squirrels' captain) gets his
own slot; Vinny Spoto's team for this specific row is still unresolved
(no code for him at all) since I don't have a confirmed 2015 team for
him to add without guessing.

## 2026-09-22 — Player pages always open on Regular Season / Stats

`playerTab` (Regular/Postseason/All-Star/etc.) and `playerSubView`
(Stats/Splits/Game Log) are module-level state that persists across
player pages by design — switching tabs while browsing one player's
own page shouldn't need to re-pick anything. But navigating to a
*different* player (via search, a team roster link, anywhere) reused
whatever tab/sub-view was last active instead of resetting: view
Player A's Postseason Game Log, click into Player B, and B opened
straight to their Postseason Game Log too, not their Regular Season
Stats. The route dispatcher already reset `logYear`/`splitYear` on
every `#/p/<name>` navigation but missed `playerTab`/`playerSubView`
— now resets both, so every fresh player-page visit starts on Regular
Season Stats regardless of what was last viewed. Percentile Rankings'
year selector is intentionally still sticky across players (its own
long-standing comment: "sticky across player pages") — left that as
is since it's a deliberate choice, not the reported bug.

## 2026-09-22 — Update the site's search/social description

Replaced the generic stats-focused description with the user's own
copy across all three tags that carry it (`<meta name="description">`,
`og:description`, `twitter:description`) — this is what shows under
the title in Google search results and in social link previews
(iMessage, Twitter, Slack, etc.). Minor grammar fix applied ("is a
competitive...") plus a comma after "website" for readability;
otherwise used verbatim.

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
