# FF6 Guide (offline PWA)

Game guide for **Final Fantasy III US v1.1 (SNES FF6) with the ff3mods mod changes**.
Static site (HTML/CSS/JS, no framework and no mandatory build step), installable on iPhone,
100% offline after the first visit. English only; item, monster and spell names are the SNES US ROM names.

## Contents

- **Walk**: World of Balance then World of Ruin chapters, location by location, with checkboxes (progress per
  location, per chapter and overall; "Unchecked", "Missable only" and "Lost for good" filters; search), the monsters
  of each location linked to the bestiary. Trackers for the 27 Espers, 14 characters and 24 Lores.
- **Bestiary**: every named monster (stats, weaknesses, statuses, steal/drop, attacks read from the AI scripts,
  Rage, Sketch, Control, Metamorph, locations), search and filters.
- **Party**: starting stats, commands, techniques (natural magic, modded SwdTech and Blitz, dances, tools...),
  best equipment per category (with the source of each item).
- **Formulas** (modded version) + small calculators.
- **More**: Espers, items (sources: chests, shops, steals, drops, Colosseum, Metamorph), shops, Colosseum, Lores,
  world encounter map (8×8 sectors), HP/MP/EXP tables, list of mod differences, quests, settings (theme,
  export/import/clear progress).

## Navigation

- Bottom tabs: **Walkthrough**, **Bestiary**, **Characters**, **Items** (`#/more/items`) and **Espers**
  (`#/more/espers`), plus **More**: a two-column grid of the remaining sections (Formulas at `#/formulas`, shops,
  Colosseum, Lores, techniques, encounter map, tables, mod changes, quests, quest items, settings).
- Walkthrough home: a "Continue" button to the last opened chapter (`ff6g.lastChap`), then the chapters as a
  two-column grid with progress and lost-forever counts.
- Chapter page: a sticky strip of chapter numbers (1–21, R1–R11, Espers/Chars/Lores; ✓ = fully checked) to jump
  in one tap, previous/All/next links at the bottom, and location headers that collapse when tapped.
- Bestiary and items: the search box and filter chips stay sticky; chips scroll horizontally.

## Data reliability

| Data | Source |
| --- | --- |
| Monsters, items, spells, Espers, characters, shops, Colosseum, Metamorph, tables, SwdTech/Blitz | read from the modded ROM (`extract.py`) |
| Chests (position, contents), random encounters per map and per world sector | read from the ROM |
| A monster's attacks | decoded from the ROM AI scripts ("attack" command) |
| Who casts which Lore | same (AI scripts) |
| Chapter order, maps reachable at each step, events, rewards, "lost for good" | hand-written, **cross-checked with the Caves of Narshe walkthrough** ("guide" tag); anything confirmed by no source stays marked "≈" |
| Location names, grouping of maps into locations, events (characters, Espers, bosses, hidden items, missables), equipment advice | **hand-written**, inferred from ROM dialogue/contents and game knowledge: **unverified** (marked "≈" in the app) |
| "ROM" (green tag) | the item/Esper does appear in a ROM event script (rough byte-search cross-check) |
| Esper locations | hints: the map whose trigger starts just before the "give Esper" byte (may be wrong) |

Every ROM chest is attached to the **first chapter whose entry lists its map** (`maps=[...]` in
`walkthrough_src.py`; without `maps`, every map of the location). Chests with variable contents (same event bit
on several maps) are merged. **Lost for good**: `lost="reason"` on a chapter entry (all its chests) or on an
event; shown in red only for equipment, relics and rare items; the other chests of the same entry show
"last chance" (amber).

Known limits: the full analysis of event scripts is not done (event rewards are therefore hand-written);
the area names of untitled maps are guesses; several chests exist in variants (same chest, contents depending
on progress): they are merged into a single box tagged "variable"; terrain-based dance learning is not detailed.
The reference walkthrough is the GBA version (some names and extras differ from the SNES game).

## Regenerating the data

Requirements: Python 3.11+; the clean ROM `rom/ff3_us_11.sfc` (CRC32 `C0FA0464`, never committed);
to describe the modded game, the ROM produced by `python build.py` (`build/ff3mods.sfc`). From the repository root:

```bash
python -I guide/tools/extract.py --rom rom/ff3_us_11.sfc --mod build/ff3mods.sfc
python -I guide/tools/build_data.py
```

- `extract.py` writes `guide/data/raw/*.json` (not versioned), `attacks.json`, `espers.json`, `misc.json`,
  `mod_diff.json`. Without `--mod`, the guide describes the unmodified game.
- `build_data.py` merges that data with `tools/walkthrough_src.py` (chapters and events) and
  `tools/content.py` (formulas, mod list, tips), writes the final JSON files and **regenerates `sw.js`**
  (version = file fingerprint → the offline cache updates itself).
- Icons: `python -I guide/tools/make_icons.py` (needs Pillow; the PNGs are already provided).

The JSON files in `guide/data/` (except `raw/`) are versioned so the site works without a ROM.
No `.sfc` file nor the ROM is ever written or committed.

## Testing locally

```bash
python -m http.server 8791 --bind 127.0.0.1 --directory guide
```

then open <http://127.0.0.1:8791/>. At phone size (375×812): all sections display, checked boxes persist
(localStorage), checklist → bestiary links work.

## Installing on iPhone

Safari only installs a PWA and keeps the offline cache from an **HTTPS** host (or `localhost`).
The simplest free option is **GitHub Pages** (the `pages.yml` workflow publishes `guide/` on every push to `main`).

1. Open `https://<user>.github.io/<repo>/` **in Safari** on the iPhone and let the page load fully
   (first online load = caching).
2. Share button › **Add to Home Screen**. Launch the "Guide FF6" icon: fullscreen, offline.
3. To update: relaunch the app with network (the service worker fetches the new version; close and reopen
   the app once).

## Structure

```
guide/
  index.html, manifest.webmanifest, sw.js (generated), icons/, css/app.css
  js/   app.js (router) · walk.js · bestiary.js · chars.js · formulas.js · more.js · state.js · util.js
  data/ generated *.json (raw/ ignored)
  tools/ ff6rom.py · extract.py · build_data.py · walkthrough_src.py · content.py · make_icons.py · sw.template.js
```

ROM formats: everything8215/ff6 disassembly (monsters CF/0000, names CF/C050, spells C4/6AC0,
items D8/5000, Espers D8/6E00, characters ED/7CA0, chests ED/8634, encounter groups CF/4800-CF/5600...).
