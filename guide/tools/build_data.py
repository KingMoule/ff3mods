#!/usr/bin/env python3
"""Assemble les données finales du guide à partir des JSON bruts (extract.py) et des sources
écrites à la main (walkthrough_src.py, content.py). Écrit guide/data/*.json et guide/sw.js.

Usage : python -I guide/tools/build_data.py     (après extract.py)
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import walkthrough_src as W  # noqa: E402
import content as C  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
GUIDE = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(GUIDE, "data")


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def dump(name, obj):
    path = os.path.join(DATA, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    print("ecrit", name, os.path.getsize(path), "octets")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def main():
    mons = load("raw/monsters_raw.json")
    items = load("raw/items_raw.json")
    attacks = load("attacks.json")
    espers = load("espers.json")
    chars = load("raw/chars_raw.json")
    misc = load("misc.json")
    maps = load("raw/maps_raw.json")
    scan = load("raw/event_scan.json")
    modd = load("mod_diff.json")

    by_name = {}
    for m in mons:
        if m["name"]:
            by_name.setdefault(norm(m["name"]), []).append(m["id"])

    def mon_id(ref):
        if "#" in ref:
            return int(ref.split("#")[1])
        ids = by_name.get(norm(ref))
        if not ids:
            raise SystemExit(f"monstre inconnu : {ref}")
        return ids[0]

    # ------------------------------------------------------------ lieux : map -> lieu
    loc_of_map = {}
    for lid, (name, mlist) in W.LOC.items():
        for mp in mlist:
            loc_of_map.setdefault(mp, []).append(lid)
    locs_out = {lid: {"name": name, "maps": mlist} for lid, (name, mlist) in W.LOC.items()}

    # ------------------------------------------------------------ coffres groupés par bit d'événement
    groups = {}
    for ch in maps["chests"]:
        groups.setdefault(ch["bit"], []).append(ch)
    chapter_order = {}
    first_for_group = {}
    def entry_maps(le):
        return le["maps"] if "maps" in le else W.LOC[le["loc"]][1]

    for ci, chap in enumerate(W.CHAPTERS):
        for li, le in enumerate(chap["locs"]):
            if le.get("nochest"):
                continue
            for pi, mp in enumerate(entry_maps(le)):
                chapter_order.setdefault(mp, (ci, li, pi))
    unassigned = []
    group_home = {}
    for bit, lst in groups.items():
        homes = [(chapter_order[c["map"]], c["map"]) for c in lst if c["map"] in chapter_order]
        if not homes:
            unassigned.append(bit)
            continue
        group_home[bit] = min(homes)[0][:2]
    if unassigned:
        miss = sorted({(c["map"], c["kind"]) for b in unassigned for c in groups[b]})
        print("ATTENTION coffres sans lieu :", miss)

    item_names = {i["id"]: i["name"] for i in items}
    mon_names = {m["id"]: m["name"] for m in mons}

    item_type = {i["id"]: i["type"] for i in items}
    KEEP = {237, 238, 239, 249}   # X-Ether, Elixir, Megalixir, Magicite

    def important(v):
        if v["kind"] == "item":
            return item_type.get(v["item"]) in ("weapon", "armor", "helmet", "shield", "relic", "tool") or v["item"] in KEEP
        if v["kind"] == "gil":
            return v["gil"] >= 5000
        return False

    def chest_variant(c):
        v = {"map": c["map"], "x": c["x"], "y": c["y"], "kind": c["kind"]}
        lids = loc_of_map.get(c["map"], [])
        if lids:
            v["loc"] = lids[0]
        if c["kind"] == "item":
            v["item"] = c["item"]
        elif c["kind"] == "gil":
            v["gil"] = c["gil"]
        elif c["kind"] == "monster":
            v["mon"] = c["monsters"]
        return v

    # ------------------------------------------------------------ événements : vérif ROM (script)
    give_item = {int(k) for k in scan["give_item"]}
    give_esper = {int(k) for k in scan["give_esper"]}
    esper_idx = {e["name"].lower(): e["id"] for e in espers}
    item_idx = {i["name"].lower(): i["id"] for i in items if i["name"]}

    # ------------------------------------------------------------ rencontres par lieu
    def monsters_of_maps(mlist):
        found = []
        for mp in mlist:
            e = maps["maps"].get(str(mp), {})
            for bl in e.get("battles", []):
                for f in bl:
                    for mid in maps["formations"][str(f)]:
                        if mid not in found and mon_names.get(mid):
                            found.append(mid)
        return found

    wchap = []
    shown_chests = set()
    place_map = {}   # monstre -> liste de lieux

    def add_place(mid, p):
        lst = place_map.setdefault(mid, [])
        if p not in lst:
            lst.append(p)

    n_checks = 0
    for ci, chap in enumerate(W.CHAPTERS):
        c_out = {"id": chap["id"], "world": chap["world"], "title": chap["title"], "intro": chap["intro"], "locs": []}
        for li, le in enumerate(chap["locs"]):
            lid = le["loc"]
            lname = W.LOC[lid][0]
            mlist = entry_maps(le)
            entry = {"loc": lid, "name": le.get("title") or lname, "items": [], "mon": [], "boss": []}
            # coffres
            chests = []
            for bit, hm in group_home.items():
                if hm == (ci, li):
                    chests.append(bit)
            rows = []
            for bit in chests:
                lst = groups[bit]
                lst_sorted = sorted(lst, key=lambda c: chapter_order.get(c["map"], (99, 0, 0)))
                primary = lst_sorted[0]
                vs = [chest_variant(c) for c in lst_sorted]
                contents = {json.dumps({k: v for k, v in x.items() if k not in ("map", "loc")}, sort_keys=True) for x in vs}
                variable = len({(v.get("item"), v.get("gil"), tuple(v.get("mon", [])), v["kind"]) for v in vs}) > 1
                row = {"id": f"c{bit}", "k": "chest", "x": primary["x"], "y": primary["y"], "v": vs}
                if variable:
                    row["m"] = True
                    row["var"] = True
                for v in vs:
                    h = getattr(W, "CHEST_HINT", {}).get((v["map"], v["x"], v["y"]))
                    if h:
                        row["hint"] = h
                        break
                if le.get("lost"):
                    row["m"] = True
                    # rouge « perdu à jamais » seulement pour ce qui compte ; le reste = « dernière chance »
                    if any(important(v) for v in vs):
                        row["lost"] = le["lost"]
                    else:
                        row["last"] = le["lost"]
                rows.append(row)
            rows.sort(key=lambda r: (r["v"][0].get("map", 0), r["y"], r["x"]))
            for r in rows:
                entry["items"].append(r)
                for v in r["v"]:
                    if v["kind"] == "item":
                        pass
            # événements
            for ei, ev in enumerate(le.get("events", [])):
                eid = hashlib.sha1((chap["id"] + "|" + ev["t"]).encode("utf-8")).hexdigest()[:8]
                row = {"id": "e" + eid, "k": ev["k"], "t": ev["t"]}
                for f in ("m", "g", "c", "lost", "item", "esper"):
                    if ev.get(f):
                        row[f] = ev[f]
                if ev.get("mon"):
                    row["mon"] = [mon_id(x) for x in ev["mon"]]
                # recoupement ROM
                if ev.get("item") and ev["item"].lower() in item_idx:
                    cnt = scan["give_item"].get(str(item_idx[ev["item"].lower()]), 0)
                    row["rom"] = 0 < cnt <= 2
                if ev.get("esper") and ev["esper"].lower() in esper_idx:
                    row["rom"] = esper_idx[ev["esper"].lower()] in give_esper
                entry["items"].append(row)
            # monstres
            entry["mon"] = monsters_of_maps(mlist)
            entry["boss"] = [mon_id(b) for b in le.get("boss", [])]
            in_ev = {m for ev in entry["items"] if ev["k"] != "chest" for m in ev.get("mon", [])}
            entry["boss_chips"] = [b for b in entry["boss"] if b not in in_ev]
            for mid in entry["mon"]:
                add_place(mid, {"t": "loc", "id": lid, "c": chap["id"]})
            for mid in entry["boss"]:
                add_place(mid, {"t": "boss", "id": lid, "c": chap["id"]})
            for ev in entry["items"]:
                for mid in ev.get("mon", []) if ev["k"] != "chest" else []:
                    add_place(mid, {"t": "boss", "id": lid, "c": chap["id"]})
            n_checks += len(entry["items"])
            c_out["locs"].append(entry)
        wchap.append(c_out)

    # ------------------------------------------------------------ suivis (espers, personnages, lores)
    def tracker(cid, title, intro, rows):
        loc = {"loc": cid, "name": title, "items": rows, "mon": [], "boss": [], "boss_chips": []}
        wchap.append({"id": cid, "world": "T", "title": title, "intro": intro, "locs": [loc]})
        locs_out[cid] = {"name": title, "maps": []}
    esp_rows = []
    for e in espers:
        ms = scan.get("esper_maps", {}).get(str(e["id"]), [])
        hint = []
        for mp in ms:
            for lid in loc_of_map.get(mp, [])[:1]:
                if W.LOC[lid][0] not in hint:
                    hint.append(W.LOC[lid][0])
        txt = e["name"] + " — " + (e["bonus"] or "no bonus") + (" · ROM hint: " + ", ".join(hint) if hint else "")
        row = {"id": f"esp{e['id']}", "k": "esper", "t": txt, "g": True}
        if e["name"] == "Ifrit":
            row["m"] = True
        esp_rows.append(row)
    tracker("t_esper", "Esper tracker (27)", "Tick the Espers you have obtained. Locations are hints inferred from the ROM scripts (unverified).", esp_rows)
    char_rows = [{"id": f"chr{c['id']}", "k": "char", "t": c["name"] + " — " + ", ".join(c["cmds"])} for c in chars if c["id"] < 14]
    tracker("t_char", "Character tracker (14)", "Tick each recruited character.", char_rows)
    lore_rows = [{"id": f"lore{l['id']}", "k": "learn", "t": l["name"] + (" (known at the start)" if l["idx"] in misc["lore_start"] else "")} for l in misc["lores"]]
    tracker("t_lore", "Lore tracker (24)", "Tick the Lores Strago has learned (see More > Lores to see who casts them).", lore_rows)

    # coffres monstres
    for ch in maps["chests"]:
        if ch["kind"] == "monster":
            lids = loc_of_map.get(ch["map"], [])
            for mid in ch["monsters"]:
                if mon_names.get(mid) and lids:
                    add_place(mid, {"t": "chest", "id": lids[0]})

    # ------------------------------------------------------------ carte du monde
    # repères : entrées de la carte du monde -> lieu
    landmarks = {0: [], 1: []}
    for src, x, y, dest in maps["entrances"]:
        if src in (0, 1) and dest in loc_of_map and dest > 2:
            landmarks[src].append((x, y, loc_of_map[dest][0]))
    world_out = {}
    for w in (0, 1):
        cells = {}
        for e in maps["world"]:
            if e["w"] != w:
                continue
            s = e["sector"]
            cell = cells.setdefault(s, {"terr": []})
            ms = []
            for bl in e["battles"]:
                for f in bl:
                    for mid in maps["formations"][str(f)]:
                        if mon_names.get(mid) and mid not in ms:
                            ms.append(mid)
            cell["terr"].append(ms)
        for s, cell in cells.items():
            cx, cy = (s % 8) * 32 + 16, (s // 8) * 32 + 16
            best = None
            for x, y, lid in landmarks[w]:
                d = (x - cx) ** 2 + (y - cy) ** 2
                if best is None or d < best[0]:
                    best = (d, lid)
            cell["near"] = best[1] if best else None
            allm = []
            for ms in cell["terr"]:
                for mid in ms:
                    if mid not in allm:
                        allm.append(mid)
            cell["all"] = allm
            for mid in allm:
                add_place(mid, {"t": "w", "w": w, "s": s})
        world_out[str(w)] = {str(s): c for s, c in cells.items()}

    # ------------------------------------------------------------ bestiaire final
    out_m = []
    for m in mons:
        if not m["name"]:
            continue
        m = dict(m)
        m["places"] = place_map.get(m["id"], [])
        out_m.append(m)

    # ------------------------------------------------------------ sources des objets
    src = {i["id"]: {"chest": [], "shop": [], "steal": [], "drop": [], "colo": [], "meta": []} for i in items}
    for bit, lst in groups.items():
        for c in lst:
            if c["kind"] == "item":
                lids = loc_of_map.get(c["map"], [])
                src[c["item"]]["chest"].append({"loc": lids[0] if lids else None, "map": c["map"], "x": c["x"], "y": c["y"]})
    for sh in misc["shops"]:
        for it in sh["items"]:
            src[it]["shop"].append(sh["name"])
    for m in out_m:
        for k, kk in ((0, "steal"), (1, "steal")):
            v = m["steal"][k]
            if v is not None:
                src[v][kk].append({"m": m["id"], "rare": k == 0})
        for k in (0, 1):
            v = m["drop"][k]
            if v is not None:
                src[v]["drop"].append({"m": m["id"], "rare": k == 0})
    for c in misc["colosseum"]:
        if c["prize"] != 0xFF and c["monster"] != 0xFF:
            src[c["prize"]]["colo"].append({"bet": c["bet"], "m": c["monster"]})
    for g, lst in enumerate(misc["metamorph"]):
        for it in set(lst):
            src[it]["meta"].append(g)
    meta_mons = {}
    for m in out_m:
        if "meta" in m:
            meta_mons.setdefault(m["meta"]["group"], []).append(m["id"])
    for it in items:
        s = src[it["id"]]
        s["metamon"] = [mid for g in s["meta"] for mid in meta_mons.get(g, [])]
        del s["meta"]
        it["src"] = {k: v for k, v in s.items() if v}

    # ------------------------------------------------------------ espers : indices de lieu (ROM)
    for e in espers:
        ms = scan.get("esper_maps", {}).get(str(e["id"]), [])
        hint = []
        for mp in ms:
            for lid in loc_of_map.get(mp, [])[:1]:
                if W.LOC[lid][0] not in hint:
                    hint.append(W.LOC[lid][0])
        e["hint"] = hint

    # ------------------------------------------------------------ personnages
    for c in chars:
        extra = C.CHARS.get(c["name"], {})
        c.update(extra)

    # ------------------------------------------------------------ lores : qui les lance
    lore_src = {}
    for l in misc["lores"]:
        lore_src[l["id"]] = [m["id"] for m in out_m if l["id"] in m["attacks"] and m["name"] != "Dark Force"]
    misc["lore_sources"] = {str(k): v for k, v in lore_src.items()}

    # ------------------------------------------------------------ sortie
    dump("monsters.json", out_m)
    dump("items.json", items)
    dump("chars.json", chars)
    dump("misc.json", misc)
    dump("walkthrough.json", {"chapters": wchap, "locs": locs_out})
    dump("world.json", world_out)
    dump("content.json", C.CONTENT)
    dump("espers.json", espers)
    # mod_diff reste en place
    print("cases à cocher :", n_checks)

    # ------------------------------------------------------------ service worker versionné
    h = hashlib.sha256()
    files = []
    for root, _dirs, fnames in os.walk(GUIDE):
        rel_root = os.path.relpath(root, GUIDE).replace("\\", "/")
        if rel_root.startswith(("tools", "__pycache__", "data/raw")):
            continue
        for fn in sorted(fnames):
            rel = (rel_root + "/" + fn) if rel_root != "." else fn
            if fn in ("sw.js", "README.md") or fn.startswith(("_", ".")) or fn.endswith(".pyc"):
                continue
            files.append(rel)
    files.sort()
    for rel in files:
        h.update(rel.encode())
        with open(os.path.join(GUIDE, rel), "rb") as f:
            h.update(f.read())
    version = h.hexdigest()[:10]
    with open(os.path.join(HERE, "sw.template.js"), encoding="utf-8") as f:
        sw = f.read()
    sw = sw.replace("__VERSION__", version).replace("__ASSETS__", json.dumps(["./"] + files, indent=1))
    with open(os.path.join(GUIDE, "sw.js"), "w", encoding="utf-8") as f:
        f.write(sw)
    print("sw.js version", version, len(files), "fichiers")


if __name__ == "__main__":
    main()
