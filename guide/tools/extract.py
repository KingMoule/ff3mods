#!/usr/bin/env python3
"""Extrait les donnees du guide FF6 / FF3 US v1.1 depuis la ROM et ecrit guide/data/*_raw.json.

Usage (depuis la racine du depot) :
    python -I guide/tools/extract.py --rom rom/ff3_us_11.sfc [--mod build/ff3mods.sfc]

--rom : ROM propre (v1.1, sans header, CRC32 C0FA0464). Obligatoire.
--mod : ROM moddee (sortie de `python build.py`). Si fournie, les donnees ecrites
        sont celles du mod et mod_diff.json liste les enregistrements qui changent
        par rapport a la ROM propre. Sans --mod, le guide decrit le jeu non modde.
La ROM n'est jamais ecrite, copiee ni versionnee. Formats : desassemblage
everything8215/ff6 (src/data/*.asm).
"""
import argparse
import json
import os
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ff6rom import Rom, bits, CRC32_CLEAN, _CHARS  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "data"))

ELEMENTS = ["Fire", "Ice", "Bolt", "Poison", "Wind", "Pearl", "Earth", "Water"]
# statuts : octet 0 = status1, 1 = status2, 2 = status3, 3 = status4
STATUS = ["Blind", "Zombie", "Poison", "Magitek", "Vanish", "Imp", "Petrify", "Death",
          "Doom", "Near Fatal", "Image", "Mute", "Berserk", "Muddle", "Sap", "Sleep",
          "Dance", "Regen", "Slow", "Haste", "Stop", "Shell", "Safe", "Reflect",
          "Rage", "Frozen", "Life 3", "Morph", "Control", "Hide", "Dog Block", "Float"]
CHAR_NAMES = ["Terra", "Locke", "Cyan", "Shadow", "Edgar", "Sabin", "Celes", "Strago",
              "Relm", "Setzer", "Mog", "Gau", "Gogo", "Umaro"]
BATTLE_CMDS = ["Fight", "Item", "Magic", "Morph", "Revert", "Steal", "Capture", "SwdTech",
               "Throw", "Tools", "Blitz", "Runic", "Lore", "Sketch", "Control", "Slot",
               "Rage", "Leap", "Mimic", "Dance", "Row", "Defend", "Jump", "X-Magic",
               "GP Rain", "Summon", "Health", "Shock", "Possess", "Magitek"]
ITEM_TYPES = ["tool", "weapon", "armor", "shield", "helmet", "relic", "consumable"]
RELIC1 = ["Atlas Armlet : +50 % dégâts physiques", "Earring : +100 % dégâts magiques",
          "PV max +25 %", "PV max +50 %", "PV max +12,5 %", "PM max +25 %", "PM max +50 %",
          "PM max +12,5 %"]
RELIC2 = ["Quick au 1er tour (Gale Hairpin)", "Évite les attaques par l'arrière (Back Guard)",
          "Jump", "X-Magic", "Control", "GP Rain", "Capture", "Dragon Horn : Jump"]
RELIC3 = ["Vol x2 (Sneak Ring)", "Magie +50 % (Earring simple)", "Sketch amélioré",
          "Control amélioré", "Précision maximale", "Coût en PM /2", "Coût en PM = 1",
          "Vigor +50 %"]
RELIC4 = ["Fight x4 (Offering)", "Contre-attaque aléatoire", "Esquive aléatoire (Beads)",
          "Gauntlet : BP de l'arme x7/4", "Genji Glove : 2 armes", "Merit Award",
          "Couverture (True Knight)", None]
RELIC5 = ["Shell si PV bas", "Safe si PV bas", "Reflect si PV bas", "EXP x2", "Gil x2", None, None,
          "Mort-vivant (Relic Ring)"]
WEAPON_SPECIAL = ["", "ThiefKnife (Steal)", "Atma Weapon", "Mort instantanée", "Man Eater",
                  "Drainer", "Soul Sabre", "Crit. MP", "Fort vs volants", "Dice", "ValiantKnife",
                  "Tempest", "Heal Rod", "Scimitar", "Ogre Nix", "Crit. MP+"]
MONSTER_FLAGS = ["Meurt à 0 MP", None, "Nom caché", None, "Humain", None, "Bonus Imp", "Mort-vivant"]
MONSTER_STATUS = ["Fuite difficile", "Attaque en premier", "Insuplexable", "Fuite impossible",
                  "Non scannable", "Non Sketchable", "Événement spécial", "Non contrôlable"]
SPECIAL_EXTRA = ["Dégâts x1,5", "Dégâts x2", "Dégâts x2,5", "Dégâts x3", "Dégâts x3,5",
                 "Dégâts x4", "Dégâts x4,5", "Dégâts x5", "Dégâts x5,5", "Dégâts x6",
                 "Dégâts x6,5", "Dégâts x7", "Dégâts x7,5", "Dégâts x8", "Dégâts x8,5",
                 "Dégâts x9", "Draine les PV", "Draine les MP", "Retire Reflect"]
SPELL_FLAGS = ["Physique", "Mort instantanée", "Soigne/Raise", "Inversé vs morts-vivants",
               "Cible au hasard", "Ignore la défense", "Dégâts non divisés", "Monstres seulement",
               "Menu", "Passe Reflect", "Lore", "Runic", "Warp rapide", "Re-cible auto",
               "Air Anchor", "Affecte les MP", "Restauratif", "Drain", "Retire un statut",
               "Alterne un statut", "Défense = Stamina", "Ne rate jamais", "Dégâts selon niveau",
               "PV fractionnaires"]
EFFECTS = ["", "ThiefKnife", "Atma Weapon", "Mort instantanée", "Man Eater", "Drainer", "Soul Sabre",
           "Crit. MP", "Fort vs volants", "Dice", "ValiantKnife", "Tempest", "Heal Rod", "Scimitar",
           "Ogre Nix", "Crit. MP+", "Scan", "Golem", "Metamorph", "Palidor", "(20)", "Mantra", "Spiraler",
           "Tapir", "Warp", "Exploder", "Blow Fish", "White Wind", "Reflect???", "L? Pearl", "Step Mine",
           "Dischord", "Pep Up", "Rippler", "Stone", "Sans contre", "Crusader", "Rate les volants",
           "Wallchange", "Escape", "Mind Blast", "N. Cross", "Flare Star", "R. Polarity", "Launcher",
           "Love Token", "Seize", "Targetting", "Suplex", "Force Field", "Quadra Slam", "BabaBreath",
           "Charm", "Doom", "Empowerer", "Overcast", "Sneeze", "Engulf", "Zinger", "Evil Toot", "Retort",
           "Revenge", "Phantasm", "Stunner", "Fallen One", "Dégâts /2", "Dégâts /4", "Quick", "Discard",
           "Clear", "(70)", "(71)", "(72)", "Magicite", "Super Ball", "Smoke Bomb", "Elixir", "Warp Stone",
           "Dried Meat", "(79)", "Possess", "Gil Toss", "Steal", "Control", "Leap", "Sketch", "Debilitator",
           "Air Anchor"]
GENJU_BONUS_FR = ["PV max +10 %", "PV max +30 %", "PV max +50 %", "PM max +10 %", "PM max +30 %",
                  "PM max +50 %", "PV max +100 %", "Niveau +30 %", "Niveau +50 %", "Force +1",
                  "Force +2", "Vitesse +1", "Vitesse +2", "Endurance +1", "Endurance +2",
                  "Magie +1", "Magie +2"]
SHOP_NAMES = """NARSHE_WEAPONS_1 NARSHE_ARMOR_1 NARSHE_RELICS_1 NARSHE_ITEMS_1 FIGARO_CASTLE_ITEMS_1 SOUTH_FIGARO_WEAPONS_1
SOUTH_FIGARO_ARMOR_1 SOUTH_FIGARO_RELICS_1 SOUTH_FIGARO_ITEMS_1 MOBLIZ_WEAPONS MOBLIZ_ARMOR MOBLIZ_RELICS MOBLIZ_ITEMS
NIKEAH_WEAPONS_1 NIKEAH_ARMOR_1 NIKEAH_ITEMS_1 NIKEAH_RELICS_1 KOHLINGEN_WEAPONS_1 KOHLINGEN_ARMOR_1 KOHLINGEN_ITEMS_1
JIDOOR_WEAPONS_1 JIDOOR_ARMOR_1 JIDOOR_ITEMS_1 JIDOOR_RELICS_1 ALBROOK_ITEMS_1 ALBROOK_WEAPONS_1 ALBROOK_ARMOR_1
VECTOR_WEAPONS VECTOR_ARMOR TZEN_WEAPONS_1 TZEN_ARMOR_1 TZEN_ITEMS_1 TZEN_RELICS_1 THAMASA_WEAPONS_1 THAMASA_ARMOR_1
THAMASA_ITEMS_1 RETURNERS_HIDEOUT_ITEMS MARANDA_WEAPONS_1 MARANDA_ARMOR_1 CRAZY_OLD_MANS_HOUSE ALBROOK_RELICS_1
NARSHE_WEAPONS_2 NARSHE_ARMOR_2 NARSHE_RELICS_2 NARSHE_ITEMS_2 THAMASA_RELICS_1 BLACKJACK_ITEMS FIGARO_CASTLE_ITEMS_2
ALBROOK_ITEMS_2 ALBROOK_WEAPONS_2 ALBROOK_ARMOR_2 ALBROOK_RELICS_2 TZEN_WEAPONS_2 TZEN_ARMOR_2 TZEN_ITEMS_2 TZEN_RELICS_2
NIKEAH_WEAPONS_2 NIKEAH_ARMOR_2 NIKEAH_ITEMS_2 NIKEAH_RELICS_2 SOUTH_FIGARO_WEAPONS_2 SOUTH_FIGARO_ARMOR_2
SOUTH_FIGARO_RELICS_2 SOUTH_FIGARO_ITEMS_2 FIGARO_CASTLE_ITEMS_3 KOHLINGEN_WEAPONS_2 KOHLINGEN_ARMOR_2 KOHLINGEN_ITEMS_2
NARSHE_WEAPONS_3 NARSHE_ARMOR_3 NARSHE_RELICS_3 NARSHE_ITEMS_3 THAMASA_WEAPONS_2 THAMASA_ARMOR_2 THAMASA_ITEMS_2
THAMASA_RELICS_2 JIDOOR_WEAPONS_2 JIDOOR_ARMOR_2 JIDOOR_ITEMS_2 JIDOOR_RELICS_2 MARANDA_WEAPONS_2 MARANDA_ARMOR_2
FIGARO_CASTLE_TOOLS_1 FIGARO_CASTLE_TOOLS_2 FIGARO_CASTLE_TOOLS_3 PHANTOM_TRAIN_ITEMS UNUSED_ITEMS""".split()


def cname(i):
    return CHAR_NAMES[i] if i < len(CHAR_NAMES) else f"#{i}"


def text_desc(rom, addr, limit=200):
    """Texte de description de menu : 0x01 = saut de ligne, 0x00 = fin."""
    out = []
    for c in rom.b(addr, limit):
        if c == 0:
            break
        if c == 1:
            out.append("\n")
        elif c == 0xFF:
            out.append(" ")
        elif c == 0xD3:
            out.append('"')
        else:
            out.append(_CHARS.get(c, ""))
    return "".join(out).strip()


def load_names(rom):
    D = {}
    D["magic"] = [rom.text(0xE6F567 + i * 7, 7, True) for i in range(54)]
    D["esper"] = [rom.text(0xE6F6E1 + i * 8, 8) for i in range(27)]
    D["attack_raw"] = [rom.text(0xE6F7B9 + i * 10, 10) for i in range(175)]
    D["esper_attack"] = [rom.text(0xE6FE8F + i * 10, 10) for i in range(27)]
    D["swdtech"] = [rom.text(0xCF3C40 + i * 12, 12) for i in range(8)]
    D["dance"] = [rom.text(0xE6FF9D + i * 12, 12) for i in range(8)]
    D["item"] = [rom.text(0xD2B300 + i * 13, 13, True) for i in range(256)]
    D["monster"] = [rom.text(0xCFC050 + i * 10, 10) for i in range(384)]
    D["monster_special"] = [rom.text(0xCFD0D0 + i * 10, 10) for i in range(384)]
    D["rare_item"] = [rom.text(0xCEFBA0 + i * 13, 13) for i in range(20)]
    attack = D["magic"] + D["esper"] + D["attack_raw"]
    # les 8 SwdTech (0x55-0x5C) ont leur nom dans une table a part
    for k in range(8):
        attack[0x55 + k] = D["swdtech"][k]
    attack[0xEE] = "(Attaque normale)"
    attack[0xEF] = "(Attaque spéciale)"
    D["attack"] = attack
    return D


# ---------------------------------------------------------------- scripts d'IA des monstres
AI_PARAMS = {0xF0: 3, 0xF1: 1, 0xF2: 3, 0xF3: 2, 0xF4: 3, 0xF5: 3, 0xF6: 3, 0xF7: 1, 0xF8: 2,
             0xF9: 3, 0xFA: 3, 0xFB: 2, 0xFC: 3, 0xFD: 0, 0xFE: 0, 0xFF: 0}


def parse_ai(rom, i):
    """Retourne (attaques, attaques_en_riposte, objets) du script d'IA du monstre i."""
    p = rom.u16(0xCF8400 + i * 2)
    a = 0xCF8700 + p
    d = rom.b(a, 400)
    pos = 0
    sections = []
    for sec in range(2):
        atk, items = [], []
        while pos < len(d):
            op = d[pos]
            if op < 0xF0:
                pos += 1  # ne devrait pas arriver; evite une boucle infinie
                continue
            n = AI_PARAMS[op]
            args = d[pos + 1:pos + 1 + n]
            if op == 0xF0:
                for x in args:
                    if x != 0xFE and x not in atk:
                        atk.append(x)
            elif op == 0xF6:
                for x in args[1:]:
                    if x not in items:
                        items.append(x)
            pos += 1 + n
            if op == 0xFF:
                break
        sections.append((atk, items))
    return sections[0][0], sections[1][0], sections[0][1] + [x for x in sections[1][1] if x not in sections[0][1]]


def decode_monsters(rom, D):
    mons = []
    for i in range(384):
        m = rom.b(0xCF0000 + i * 32, 32)
        it = rom.b(0xCF3000 + i * 4, 4)
        sk = rom.b(0xCF4300 + i * 2, 2)
        ctl = rom.b(0xCF3D00 + i * 4, 4)
        meta = m[17]
        spec = m[31]
        eff = spec & 0x3F
        spec_txt = None
        if eff < 32:
            spec_txt = STATUS[eff]
        elif eff - 32 < len(SPECIAL_EXTRA):
            spec_txt = SPECIAL_EXTRA[eff - 32]
        atk, counter, uses = parse_ai(rom, i)

        def item(v):
            return None if v == 0xFF else v
        imm = m[20] | m[21] << 8 | (m[22] & 0xFE) << 16
        mon = {
            "id": i, "name": D["monster"][i],
            "level": m[16], "hp": m[8] | m[9] << 8, "mp": m[10] | m[11] << 8,
            "exp": m[12] | m[13] << 8, "gil": m[14] | m[15] << 8,
            "speed": m[0], "atk": m[1], "hit": m[2], "evade": m[3], "mblock": m[4],
            "def": m[5], "mdef": m[6], "magpwr": m[7],
            "weak": bits(m[25], ELEMENTS), "null": bits(m[24], ELEMENTS), "absorb": bits(m[23], ELEMENTS),
            "immune": bits(imm, STATUS[:24]),
            "start": bits(m[27] | m[28] << 8 | m[29] << 16, STATUS[:24]),
            "flying": bool(m[22] & 1),
            "flags": bits(m[18], MONSTER_FLAGS),
            "mstatus": bits(m[19], MONSTER_STATUS),
            "steal": [item(it[0]), item(it[1])], "drop": [item(it[2]), item(it[3])],
            "special": {"name": D["monster_special"][i], "effect": spec_txt,
                        "nodmg": bool(spec & 0x40), "nomiss": bool(spec & 0x80)},
            "attacks": atk, "counter": counter, "uses": uses,
            "sketch": [sk[0], sk[1]], "control": [c for c in ctl if c != 0xFF],
        }
        if meta >> 5 != 7:
            mon["meta"] = {"group": meta & 0x1F, "rate": meta >> 5}
        if i < 256:
            mon["rage"] = rom.u8(0xCF4600 + i * 2 + 1)
        mons.append(mon)
    return mons


def target_text(t):
    if t == 0xFF:
        return "Menu"
    init = t & 0x0C
    base = {0: "Une cible", 4: "Tous (alliés et ennemis)", 8: "Un camp", 12: "Tout un camp"}[init]
    extra = []
    if t & 0x40:
        extra.append("ennemi par défaut")
    if t & 0x20:
        extra.append("multi-cibles")
    if t & 0x80:
        extra.append("roulette")
    return base + (" (" + ", ".join(extra) + ")" if extra else "")


def decode_attacks(rom, D):
    out = []
    for i in range(256):
        b = rom.b(0xC46AC0 + i * 14, 14)
        flags = b[2] | b[3] << 8 | b[4] << 16
        st = b[10] | b[11] << 8 | b[12] << 16 | b[13] << 24
        eff = b[9]
        out.append({
            "id": i, "name": D["attack"][i], "target": target_text(b[0]),
            "element": bits(b[1], ELEMENTS), "flags": bits(flags, SPELL_FLAGS),
            "mp": b[5], "power": b[6], "hit": b[8],
            "effect": EFFECTS[eff] if eff < len(EFFECTS) else ("" if eff == 0xFF else f"({eff})"),
            "status": bits(st, STATUS), "raw": b.hex(),
        })
    return out


def decode_items(rom, D):
    items = []

    def sgn(n):
        return n if n < 8 else -(n - 8)
    for i in range(256):
        b = rom.b(0xD85000 + i * 30, 30)
        typ = b[0] & 7
        eq = b[1] | b[2] << 8
        desc_ptr = rom.u16(0xED7AA0 + i * 2)
        it = {"id": i, "name": D["item"][i], "type": ITEM_TYPES[typ] if typ < 7 else "?",
              "price": b[28] | b[29] << 8, "desc": text_desc(rom, 0xED6400 + desc_ptr)}
        if typ in (1, 2, 3, 4, 5):
            it["equip"] = [CHAR_NAMES[c] for c in range(14) if eq >> c & 1]
            it["imp"] = bool(eq & 0x4000)
            it["power"] = b[20]
            if typ == 1:
                it["hit"] = b[21]
                it["element"] = bits(b[15], ELEMENTS)
                it["special"] = WEAPON_SPECIAL[b[27] >> 4]
                f = b[19]
                it["wflags"] = [n for n, k in (("SwdTech", 2), ("Rangée arrière", 0x20),
                                               ("Deux armes", 0x40), ("Runic", 0x80)) if f & k]
            else:
                it["mdef"] = b[21]
                it["absorb"] = bits(b[22], ELEMENTS)
                it["null"] = bits(b[23], ELEMENTS)
                it["weak"] = bits(b[24], ELEMENTS)
                it["block"] = "physique" if b[27] & 4 else ("magique" if b[27] & 8 else "")
            it["bonus"] = {"str": sgn(b[16] & 15), "spd": sgn(b[16] >> 4), "sta": sgn(b[17] & 15), "mag": sgn(b[17] >> 4)}
            ev, mb = b[26] & 15, b[26] >> 4
            it["evade"] = ev * 10 if ev < 6 else -(ev - 5) * 10
            it["mevade"] = mb * 10 if mb < 6 else -(mb - 5) * 10
            it["immune"] = bits(b[6] | b[7] << 8, STATUS[:16])
            it["auto"] = bits(b[25] | b[8] << 8, STATUS[8:24])
            it["fx"] = ([RELIC1[k] for k in range(8) if b[9] >> k & 1] + [RELIC2[k] for k in range(8) if b[10] >> k & 1] +
                        [RELIC3[k] for k in range(8) if b[11] >> k & 1] +
                        [x for k, x in enumerate(RELIC4) if x and b[12] >> k & 1] +
                        [x for k, x in enumerate(RELIC5) if x and b[13] >> k & 1])
            if b[3] or b[4]:
                it["teaches"] = {"spell": b[4], "rate": b[3]}
            sc = b[18]
            if sc:
                it["cast"] = {"spell": sc & 0x3F, "random": bool(sc & 0x40), "asitem": bool(sc & 0x80)}
            fe = b[5]
            if fe & 3:
                it["field"] = "Moins de combats" if fe & 1 else "Aucun combat"
            if fe & 0x20:
                it["field"] = "Sprint"
            if fe & 0x80:
                it["field"] = "Soin au pas (Tintinabar)"
        elif typ == 0:
            it["cast"] = {"spell": b[18]}
        else:
            it["power"] = b[20]
        items.append(it)
    return items


def decode_espers(rom, D):
    out = []
    for i in range(27):
        b = rom.b(0xD86E00 + i * 11, 11)
        spells = []
        for k in range(5):
            rate, sp = b[k * 2], b[k * 2 + 1]
            if sp != 0xFF and rate:
                spells.append({"id": sp, "spell": D["attack"][sp], "rate": rate})
        bonus = None if b[10] == 0xFF else b[10]
        out.append({"id": i, "name": D["esper"][i], "attack": D["esper_attack"][i], "spells": spells,
                    "bonus": GENJU_BONUS_FR[bonus] if bonus is not None else None,
                    "bonus_desc": text_desc(rom, 0xEDFE00 + rom.u16(0xEDFFD0 + bonus * 2)) if bonus is not None else None})
    return out


def decode_chars(rom, D):
    out = []
    for i in range(14):
        b = rom.b(0xED7CA0 + i * 22, 22)

        def itm(v):
            return None if v == 0xFF else v
        out.append({
            "id": i, "name": CHAR_NAMES[i], "hp": b[0], "mp": b[1],
            "cmds": [BATTLE_CMDS[c] for c in b[2:6] if c < 30],
            "str": b[6], "agi": b[7], "sta": b[8], "mag": b[9],
            "atk": b[10], "def": b[11], "mdef": b[12], "evade": b[13], "mblock": b[14],
            "equip": {"weapon": itm(b[15]), "shield": itm(b[16]), "helmet": itm(b[17]), "armor": itm(b[18]),
                      "relic1": itm(b[19]), "relic2": itm(b[20])},
            "run": ["125 %", "100 %", "75 %", "50 %"][b[21] & 3],
            "levelmod": ["+0", "+2", "+5", "-3"][(b[21] >> 2) & 3],
            "fixed": bool(b[21] & 0x10),
        })
    return out


def decode_misc(rom, D):
    M = {}
    M["exp_table"] = [rom.u16(0xED8220 + i * 2) for i in range(98)]
    M["hp_gain"] = [rom.u8(0xE6F4A0 + i) for i in range(98)]
    M["mp_gain"] = [rom.u8(0xE6F502 + i) for i in range(98)]
    ini = rom.u24(0xE6F564)
    M["lore_start"] = [k for k in range(24) if ini >> k & 1]
    nm = {}
    for name, a in (("Terra", 0xECE3C0), ("Celes", 0xECE3E0)):
        lst = []
        for k in range(16):
            sp, lv = rom.u8(a + k * 2), rom.u8(a + k * 2 + 1)
            if sp != 0xFF:
                lst.append({"id": sp, "spell": D["attack"][sp], "level": lv})
        nm[name] = lst
    M["natural_magic"] = nm
    bl = [rom.u8(0xE6F490 + i) for i in range(8)]
    zl = [rom.u8(0xE6F498 + i) for i in range(8)]
    M["swdtech"] = [{"id": 0x55 + k, "name": D["swdtech"][k], "level": bl[k]} for k in range(8)]
    M["blitz"] = [{"id": 0x5D + k, "name": D["attack"][0x5D + k], "level": zl[k]} for k in range(8)]
    M["dances"] = [{"name": D["dance"][k], "moves": [D["attack"][x] for x in rom.b(0xCFFE80 + k * 4, 4)],
                    "ids": list(rom.b(0xCFFE80 + k * 4, 4))} for k in range(8)]
    M["lores"] = [{"idx": k, "id": 0x8B + k, "name": D["attack"][0x8B + k]} for k in range(24)]
    M["metamorph"] = [[x for x in rom.b(0xC47F40 + g * 4, 4)] for g in range(17)]
    M["metamorph_rates"] = ["255/256", "3/4", "1/2", "1/4", "1/8", "1/16", "1/32", "0"]
    M["colosseum"] = []
    for k in range(256):
        b = rom.b(0xDFB600 + k * 4, 4)
        M["colosseum"].append({"bet": k, "monster": b[0], "prize": b[2], "hidden": b[3] != 0})
    M["shops"] = []
    for k in range(87):
        b = rom.b(0xC47AC0 + k * 9, 9)
        M["shops"].append({"id": k, "name": SHOP_NAMES[k], "kind": b[0] & 7, "items": [x for x in b[1:9] if x != 0xFF]})
    M["imp_items"] = [x for x in rom.b(0xED82E4, 16) if x != 0xFF]
    M["rare_items"] = D["rare_item"]
    return M


# ---------------------------------------------------------------- cartes, coffres, rencontres
def formation_monsters(rom, fi):
    b = rom.b(0xCF6200 + fi * 15, 15)
    out = []
    for k in range(6):
        mid = b[2 + k] | (((b[14] >> k) & 1) << 8)
        if mid != 0x1FF:
            out.append(mid)
    return out


def expand_group_entry(v):
    """Un index de combat dans un groupe : bit 15 = + rand(0..3) (ile flottante)."""
    return [v & 0x7FFF] if not v & 0x8000 else [(v & 0x7FFF) + i for i in range(4)]


def decode_dialog_titles(rom):
    dlg = {}
    for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        dlg[0x20 + i] = c
    for i, c in enumerate("abcdefghijklmnopqrstuvwxyz"):
        dlg[0x3A + i] = c
    for i, c in enumerate("0123456789"):
        dlg[0x54 + i] = c
    dlg.update({0x5E: "!", 0x5F: "?", 0x60: "/", 0x61: ":", 0x63: "'", 0x64: "-", 0x65: ".", 0x66: ",", 0x7F: " "})
    dte = rom.b(0xC0DFA0, 256)
    titles = []
    for k in range(73):
        p = rom.u16(0xE68400 + k * 2)
        out = []
        for c in rom.b(0xCEF100 + p, 40):
            if c == 0:
                break
            if c >= 0x80:
                out.append(dlg.get(dte[(c - 0x80) * 2], "") + dlg.get(dte[(c - 0x80) * 2 + 1], ""))
            else:
                out.append(dlg.get(c, ""))
        titles.append("".join(out))
    return titles


def decode_maps(rom, D):
    base = 0xED8634
    ptrs = [rom.u16(0xED82F4 + i * 2) for i in range(417)]
    nmaps = 415
    chests = []
    for m in range(nmaps):
        a, b = base + ptrs[m], base + ptrs[m + 1]
        for k in range((b - a) // 5):
            e = rom.b(a + k * 5, 5)
            sw = e[2] | e[3] << 8
            kind = "gil" if sw & 0x8000 else "item" if sw & 0x4000 else "monster" if sw & 0x2000 else "empty"
            ch = {"map": m, "x": e[0], "y": e[1], "bit": sw & 0x1FF, "kind": kind}
            if kind == "gil":
                ch["gil"] = e[4] * 100
            elif kind == "item":
                ch["item"] = e[4]
            elif kind == "monster":
                ch["formation"] = e[4]
                ch["monsters"] = formation_monsters(rom, e[4])
            chests.append(ch)
    titles = decode_dialog_titles(rom)
    rg = [[rom.u16(0xCF4800 + g * 8 + k * 2) for k in range(4)] for g in range(256)]
    sub = [rom.u8(0xCF5600 + m) for m in range(512)]
    minfo = {}
    for m in range(nmaps):
        pr = rom.b(0xED8F00 + m * 33, 33)
        rate = (rom.u8(0xCF5880 + (m * 2) // 8) >> ((m * 2) % 8)) & 3
        e = {"title": titles[pr[0]] if pr[0] < 73 else ""}
        if pr[5] & 0x80:
            e["rate"] = ["normal", "bas", "haut", "très haut"][rate]
            e["battles"] = [expand_group_entry(v) for v in rg[sub[m]]]
        minfo[m] = e
    world = []
    for w, a in ((0, 0xCF5400), (1, 0xCF5500)):
        for s in range(64):
            for t in range(4):
                g = rom.u8(a + s * 4 + t)
                world.append({"w": w, "sector": s, "terrain": t,
                              "battles": [expand_group_entry(v) for v in rg[g]]})
    used = set()
    for e in minfo.values():
        for bl in e.get("battles", []):
            used.update(bl)
    for e in world:
        for bl in e["battles"]:
            used.update(bl)
    # formations d'evenement (boss) : tous les combats non aleatoires
    formations = {f: formation_monsters(rom, f) for f in range(576)}
    # entrees (carte -> carte) : utile pour relier les lieux
    edges = []
    sp = [rom.u16(0xDFBB00 + i * 2) for i in range(0x1A1)]
    for m in range(0x1A0):
        a, b = 0xDFBB00 + sp[m], 0xDFBB00 + sp[m + 1]
        for k in range((b - a) // 6):
            e = rom.b(a + k * 6, 6)
            edges.append([m, e[0], e[1], (e[2] | e[3] << 8) & 0x1FF])
    lp = [rom.u16(0xEDF480 + i * 2) for i in range(0x1A1)]
    for m in range(0x1A0):
        a, b = 0xEDF480 + lp[m], 0xEDF480 + lp[m + 1]
        for k in range((b - a) // 7):
            e = rom.b(a + k * 7, 7)
            edges.append([m, e[0], e[1], (e[3] | e[4] << 8) & 0x1FF])
    return {"chests": chests, "maps": minfo, "world": world, "formations": formations,
            "random_formations": sorted(used), "entrances": edges}


# ---------------------------------------------------------------- scan des scripts d'evenement
def scan_events(rom, D):
    """Recherche brute des octets 'donner un objet' (0x80 xx) et 'donner un esper' (0x86 xx).

    L'analyse complete des scripts n'est pas faite : les resultats servent a confirmer que
    l'objet/esper apparait quelque part dans le script d'evenements, et (pour les espers) a
    proposer des indices de lieu = cartes dont un declencheur/PNJ demarre juste avant l'octet."""
    import bisect
    d = rom.b(0xCA0000, 0xCCE600 - 0xCA0000)
    np_ = [rom.u16(0xC41A10 + i * 2) for i in range(0x1A1)]
    tp = [rom.u16(0xC40000 + i * 2) for i in range(0x1A1)]
    entries = []
    for m in range(0x1A0):
        a, b = 0xC41A10 + np_[m], 0xC41A10 + np_[m + 1]
        for k in range((b - a) // 9):
            e = rom.b(a + k * 9, 9)
            entries.append((0xCA0000 + (e[0] | e[1] << 8 | (e[2] & 3) << 16), m))
        a, b = 0xC40000 + tp[m], 0xC40000 + tp[m + 1]
        for k in range((b - a) // 5):
            e = rom.b(a + k * 5, 5)
            entries.append((0xCA0000 + (e[2] | e[3] << 8 | e[4] << 16), m))
    entries.sort()
    keys = [e[0] for e in entries]
    items, espers, where = {}, {}, {}
    for i in range(len(d) - 1):
        if d[i] == 0x80 and d[i + 1] != 0xFF:
            items.setdefault(d[i + 1], 0)
            items[d[i + 1]] += 1
        elif d[i] == 0x86 and 0x36 <= d[i + 1] <= 0x50:
            e = d[i + 1] - 0x36
            espers[e] = espers.get(e, 0) + 1
            addr = 0xCA0000 + i
            j = bisect.bisect_right(keys, addr) - 1
            if j >= 0 and addr - keys[j] <= 700:
                lst = where.setdefault(e, [])
                for q in range(max(0, j - 1), min(len(entries), j + 2)):
                    if entries[q][1] not in lst:
                        lst.append(entries[q][1])
    return {"give_item": items, "give_esper": espers, "esper_maps": where}


def diff_tables(clean, mod, Dm):
    """Differences de donnees (monstres, sorts, objets...) entre ROM propre et ROM moddee."""
    out = []

    def rec(kind, base, size, n, namefn):
        for i in range(n):
            x, y = clean.b(base + i * size, size), mod.b(base + i * size, size)
            if x != y:
                out.append({"kind": kind, "id": i, "name": namefn(i),
                            "bytes": [[k, x[k], y[k]] for k in range(size) if x[k] != y[k]]})
    rec("monster", 0xCF0000, 32, 384, lambda i: Dm["monster"][i])
    rec("attack", 0xC46AC0, 14, 256, lambda i: Dm["attack"][i])
    rec("item", 0xD85000, 30, 256, lambda i: Dm["item"][i])
    rec("esper", 0xD86E00, 11, 27, lambda i: Dm["esper"][i])
    rec("char", 0xED7CA0, 22, 64, lambda i: cname(i))
    rec("steal_drop", 0xCF3000, 4, 384, lambda i: Dm["monster"][i])
    rec("shop", 0xC47AC0, 9, 87, lambda i: SHOP_NAMES[i])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default="rom/ff3_us_11.sfc")
    ap.add_argument("--mod", default=None)
    args = ap.parse_args()
    clean = Rom(args.rom)
    crc = zlib.crc32(clean.d) & 0xFFFFFFFF
    if crc != CRC32_CLEAN:
        sys.exit(f"CRC32 inattendu {crc:08X} (attendu {CRC32_CLEAN:08X}) : il faut la ROM propre v1.1 sans header")
    rom = Rom(args.mod) if args.mod else clean
    os.makedirs(OUT, exist_ok=True)
    D = load_names(rom)

    os.makedirs(os.path.join(OUT, "raw"), exist_ok=True)

    def dump(name, obj):
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        print("ecrit", name, os.path.getsize(path), "octets")

    dump("raw/monsters_raw.json", decode_monsters(rom, D))
    dump("attacks.json", decode_attacks(rom, D))
    dump("raw/items_raw.json", decode_items(rom, D))
    dump("espers.json", decode_espers(rom, D))
    dump("raw/chars_raw.json", decode_chars(rom, D))
    dump("misc.json", decode_misc(rom, D))
    dump("raw/maps_raw.json", decode_maps(rom, D))
    dump("raw/event_scan.json", scan_events(rom, D))
    if args.mod:
        Dc = load_names(clean)
        dump("mod_diff.json", diff_tables(clean, rom, Dc))
    else:
        dump("mod_diff.json", [])


if __name__ == "__main__":
    main()
