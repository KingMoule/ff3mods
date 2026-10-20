"""Hand-written English text: formulas, mod differences, character tips, sidequests.

Formulas were checked against the code (everything8215/ff6 disassembly + the repository's patches/).
Passages marked "unverified" are game knowledge not cross-checked in the ROM.
"""


def P(t):
    return {"t": "p", "x": t}


def F(t):
    return {"t": "f", "x": t}


def UL(*lines):
    return {"t": "ul", "x": list(lines)}


def NOTE(t):
    return {"t": "note", "x": t}


def MOD(t):
    return {"t": "mod", "x": t}


FORMULAS = [
    dict(id="notation", title="Notation", blocks=[
        UL("Lv = attacker level; Vigor = Vigor stat (“Strength”), Vig2 = Vigor x 2 capped at 255",
           "BP = weapon Battle Power; Pwr = spell power; MagPwr = Magic Power stat (monsters: value x 1.5)",
           "Def / MDef = target Defense / Magic Defense; Evade / MBlock = Evade / Magic Block (%)",
           "All final damage is capped at 9999 per target."),
    ]),
    dict(id="phys", title="Physical damage", blocks=[
        P("Character (Fight, Capture, Blitz, SwdTech...). Base power comes from the weapon (or the Blitz power):"),
        F("base = BP + 1.5 x (Lv² x (BP + Vig2) / 256)"),
        P("Monster (monster Atk stat; a monster's Vigor is a random 56 to 63):"),
        F("base = Lv² x (4 x Atk + monster_Vigor) / 256     (no x1.5 and no +BP)"),
        P("Then, in this order:"),
        UL("Fight/Capture only (mod): Offering ÷2 (rounded up), then Genji Glove x3/4",
           "Atlas Armlet: +50%; (the mod keeps: Earring +100% / single +50% for magic)",
           "Gauntlet: the BP counts as 7/4 in the formula above",
           "Variance: x (224 to 255) / 256, i.e. about 88% to 100%",
           "Defense: x (255 − Def) / 256, then +1 (ignored by “ignores defense” attacks)",
           "Safe on the target: x 170/256 (≈ 2/3); back row or Defend: ÷2 (they stack: ÷4)",
           "Berserk, Morph (attacker), critical hit: multiplier x(1 + n/2); critical = 1 chance in 32, x2",
           "A character attacking another character (Muddle...): ÷2",
           "Elemental weakness x2; resistance ÷2; immunity 0; absorb: heals"),
        MOD("Mod (Ultimate Damage): no more overflow past 65,535 (a huge attack no longer wraps to almost 0); "
            "Offering and Genji Glove now only reduce Fight and Capture (not Pummel, SwdTech, etc.)."),
    ]),
    dict(id="magic", title="Magic damage", blocks=[
        F("base = 4 x Pwr + Lv x MagPwr x Pwr / 32"),
        UL("Earring: +100% (two Earrings) or +50% (just one); applied before variance",
           "Variance: x (224 to 255) / 256",
           "Defense: x (255 − MDef) / 256 + 1 (except spells that ignore defense)",
           "Shell on the target: x 170/256; target in Morph: magic damage ÷2 (from the code)",
           "Multiple targets: damage is usually split; some spells are not (“damage not divided”)",
           "Elements: x2 weakness, ÷2 resistance, 0 immunity, absorb = heal"),
        P("Healing: base = 4 x Pwr + Lv x MagPwr x Pwr / 32 as well (no defense); the same elements apply (inverted against the undead)."),
    ]),
    dict(id="hit", title="Hit rate and evasion", blocks=[
        P("Physical attack (mod: Evade finally works):"),
        F("hits if rand(0..99) < hit x (256 − 2 x Evade) / 256"),
        UL("hit: weapon (or monster) stat; Blind on the attacker ÷2; target with Beads (random dodge) ÷2",
           "Evade ≥ 128: minimum multiplier (1/256) → nearly impossible to hit",
           "Image: roughly one physical attack in four is absorbed (rand < 64/256) and removes Image",
           "Always hits: target in Stop, Sleep, Petrify or Frozen; target in Retort stance; “never misses” spells",
           "Magic attack: same calculations with MBlock, with no Blind or Beads."),
        MOD("Before the mod, Evade was never used (physical attacks read MBlock) and Blind/Beads did nothing. "
            "About twenty monsters with high Evade become harder to hit: Mover, Pugs, Scrapper, Punisher, Ursus, Borras, Cruller, Vindr..."),
        P("Instant death (Doom, X-Zone, X-weapons...): misses if the target is protected; otherwise a Stamina check. "
          "The mod stops Vanish from bypassing death protection."),
    ]),
    dict(id="steal", title="Stealing (Steal / Mug)", blocks=[
        F("success chance = thief_Lv + 50 − target_Lv  (%)   ; x2 with the Sneak Ring"),
        P("If the steal succeeds, the slot drawn is the rare or the common one; an empty slot makes the steal fail."),
        MOD("Mod (Locke): rare item 1 time in 4 (64/256) instead of 1 in 8 (32/256)."),
        P("End-of-battle drops: rare item 1/8, common 7/8 (a single roll per monster, unchanged by the mod)."),
    ]),
    dict(id="dice", title="Dice (Setzer)", blocks=[
        F("damage = (product of the dice) x Lv x 2     (ignores defense; bonus if the dice match)"),
        MOD("Mod (Better Dice): one die always has an even 1-to-6 spread, the others get closer to it "
            "(vanilla: 1-4 at 3/16, 5-6 at 1/8); the matching-dice bonus also applies to 2-dice Dice; "
            "Offering divides dice damage."),
    ]),
    dict(id="swd", title="SwdTech (Cyan)", blocks=[
        P("In the original game SwdTechs had their own powers. In this mod the gauge fills twice as fast "
          "(one step every 64 frames instead of 128) and every SwdTech is a physical attack based on the weapon and Vigor:"),
        F("damage = multiplier x (damage of a Fight)"),
        UL("Dispatch (Lv 1): x1.25, one target, ignores defense",
           "Retort (Lv 6): counter x1.5, ignores defense",
           "Slash (Lv 12): x1.5 + Sap; works on bosses (no more 50% HP / death check)",
           "Quadra Slam (Lv 15): 4 hits x0.75 on random targets",
           "Empowerer (Lv 24): x1 HP drain, then x0.25 MP drain",
           "Stunner (Lv 34): x1 on all enemies + Stop (140/256)",
           "Quadra Slice (Lv 44): 4 hits x1, ignores defense",
           "Cleave (Lv 70): x1.5 on all + Death (182/256)"),
        NOTE("The learn levels and powers above are read from the modded ROM (Characters page > Cyan)."),
    ]),
    dict(id="blitz", title="Blitz (Sabin)", blocks=[
        P("Blitzes are physical attacks: the Blitz power replaces the weapon BP in the physical formula "
          "(plus Vigor). Sabin learns them at levels 1, 6, 10, 15, 23, 30, 42 and 70."),
        MOD("Mod: the Blitz command opens a list (like Magitek); you pick the Blitz then the target, "
            "no more entering button combinations. Unlearned Blitzes show up empty."),
    ]),
    dict(id="sketch", title="Sketch, Control, Rage, Lore", blocks=[
        UL("Sketch (Relm): copies one of the monster's 2 “Sketch” attacks; success depends on the level ratio (Beret improves it); monsters marked “Not Sketchable” fail",
           "Control: the monster performs one of its 4 “Control” attacks; Coronet improves success",
           "Rage (Gau): Gau acts as the learned monster and uses the Rage attack on its page; “(Special attack)” = the monster's special attack",
           "Lore (Strago): magic formulas using Strago's MagPwr; learned by being hit by the attack; not learned if Strago is KO'd"),
    ]),
    dict(id="exp", title="Experience and growth", blocks=[
        P("HP, MP and stats grow per level according to the game's tables; Esper bonuses apply at the next level-up (see More > Espers). "
          "Max HP/MP can be raised by relics (+12.5%, +25%, +50%). The HP/MP/EXP tables read from the ROM are under More > Tables."),
        P("A character who joins late gets a level close to the party average (each character has its own offset: see their pages)."),
    ]),
]

# (group, title, text)
MODS = [
    ("Battle fixes", "Evade (physical)", "Physical attacks use Evade; Blind and Beads work. About twenty monsters become harder to hit."),
    ("Battle fixes", "Vanish / Doom", "Vanish no longer lets Doom or X-Zone kill targets protected against instant death (bosses included)."),
    ("Battle fixes", "Ultimate Damage", "No overflow past 65,535; Genji Glove and Offering only reduce Fight and Capture."),
    ("Battle fixes", "Dead Hare", "A monster already removed from battle (killed by the Scimitar, etc.) no longer counterattacks."),
    ("Battle fixes", "Item/Magic Counter", "Monsters that only counter one specific spell/item (SrBehemoth, FlameEater...) no longer counter everything afterwards."),
    ("Battle fixes", "Zombie/Rippler", "Rippler no longer swaps hidden statuses; a Zombie cured by Rippler recovers 1/8 of its HP."),
    ("Battle fixes", "Imp's Retort", "An Imp Cyan whose Retort fails no longer counters for the whole battle."),
    ("Battle fixes", "Self Sneeze", "The Fake Mustache link is cut when Relm uses Palidor or if a side disappears."),
    ("Battle fixes", "Dead in the Air", "Condemned during a Jump: Wound instead of staying at 0 HP; items restored after every battle; Esper +30% HP/MP bonus fixed."),
    ("Battle fixes", "Smoke and Mirrors", "A Muddled character's Smoke Bomb no longer removes the monsters (and thus the victory) in their place."),
    ("Battle fixes", "Soul Saved", "Soul Savers are immune to instant death: X-Zone can no longer end the Wrexsoul fight."),
    ("Battle fixes", "Morph Mayhem", "The Morph gauge no longer drops during Sleep/Stop/Frozen, during Quick, or after leaving battle."),
    ("Battle fixes", "Rock Bottom", "Near Fatal is reapplied when Petrify is cured below 1/8 HP."),
    ("Battle fixes", "Status Unknown", "Statuses without an outline color (Life 3, Float...) no longer show up blank."),
    ("Battle fixes", "Imp Skimp / Imp's Rage / Imp's Call", "Imp sprite tied to the status; Rage and Dance forbidden while Imp; an Esper cancelled by Imp is no longer lost."),
    ("Battle fixes", "Shadow's Status", "Lasting statuses are removed from Shadow after the Floating Continent."),
    ("Battle fixes", "Stone Faced / Stone Cold", "Petrified monsters no longer repeat their attack; Petrify no longer blocks Revivify."),
    ("Battle fixes", "Killer Life 3", "An undead monster killed by an X-weapon no longer revives with Life 3 only to die again."),
    ("Battle fixes", "Zombie/Tapir", "A Tapir that cures Zombie restores 1/8 max HP."),
    ("Battle fixes", "Double Block / Half Knife", "A Fenix Down is no longer blocked twice by a shield; Offering also halves the ValiantKnife bonus."),
    ("Battle fixes", "Bye Bye Breath / Off Death Row / Throwback", "Crashes in the 2nd Phunbaba fight fixed; Safety Bit and Memento Ring remove Condemned; Shadow throws normally at a target in Jump."),
    ("Event fixes", "Menu Malarky", "No more event skipping through the menu (Locke and the South Figaro guard, Inferno, Poltergeist)."),
    ("Event fixes", "Returner's Day Off", "Two events fixed for Gau left on the Veldt (forgotten characters, softlock after Esper World)."),
    ("Event fixes", "Shadow Gone / Shadow Copy", "No more empty party in Narshe without Shadow; Mimic no longer copies Shadow in the Dragon's Neck Colosseum."),
    ("Event fixes", "Game Over", "A defeat on the world map no longer leaves a pointer on the stack (softlock after 52 defeats)."),
    ("Event fixes", "Map Mishap / Multiple Events / Bland Entrance", "Seven map issues, ten events and the game opening fixed (see the Leet Sketcher readme)."),
    ("Event fixes", "Stepping Out / Trigger Happy / Walk This Way", "Holding Y no longer interrupts events; a timer event no longer runs past an event tile; diagonal stairs."),
    ("Event fixes", "Unequipium / Castle Party / Narshe's Door", "HP/MP refreshed when an event removes equipment; party order at Doma; Narshe's secret door."),
    ("Event fixes", "Anonymous Attack / Caravaggio / Chain of Command", "Kefka's attack at the Sealed Gate; Roulette via Sketch/Rage; Gogo's command names."),
    ("Event fixes", "Precious Jewels / Phoenix Chest / Off the Hook / Loud Music", "Gem Box without an ambush; Phoenix Cave chest; character above the hook; Opera House organ."),
    ("Event fixes", "Save Point Switch", "Switching parties in the Phoenix Cave/Kefka's Tower no longer lets you save or sleep away from a save point."),
    ("Balance", "Cyan: SwdTech", "Gauge 2x faster; all SwdTechs are physical, based on the weapon and Vigor (see Formulas)."),
    ("Balance", "Locke: steal", "Rare item stolen 1 time in 4 instead of 1 in 8."),
    ("Balance", "Better Dice", "Setzer's dice better distributed, matching-dice bonus also for 2-dice Dice, Offering halves dice."),
    ("Feature", "Blitz menu", "Sabin's Blitz command opens a list; you pick the Blitz then the target."),
]

CHARS = {
    "Terra": dict(
        role="Magic + Morph. Learns her natural magic (see table), then through Espers.",
        tips=["Morph doubles her physical and magic damage (limited time); the gauge is protected by the fixes.",
              "Natural magic: Terra and Celes learn spells at certain levels."],
        gear=[("Early", "MithrilKnife, Buckler: replace them as soon as possible with a rod/sword."),
              ("Mid-game", "Earrings + an MP relic; a robe for magic defense."),
              ("Late", "Strong Rod/Brush, Ribbon; Minerva (armor) is highly sought after.")]),
    "Locke": dict(
        role="Thief: Steal/Mug. The mod gives the rare item 1 time in 4.",
        tips=["Sneak Ring: doubles steal chance.", "Mug = Fight + steal; Thief Glove (Capture) gives Capture."],
        gear=[("Early", "Dirk then MithrilKnife/Guardian."), ("Mid", "Fast daggers (Tempest, Strato if available)."),
              ("Late", "Valiant Knife, Strato, Gauntlet/Genji Glove; Sneak Ring.")]),
    "Cyan": dict(
        role="SwdTech (mod: physical, gauge 2x faster).",
        tips=["SwdTechs depend on the weapon's BP: equip a high-BP weapon (katanas).",
              "Retort on counterattack: x1.5; Cleave at level 70."],
        gear=[("Early", "Basic katana."), ("Mid", "Kotetsu, Murasame."), ("Late", "Masamune/Aura etc., Genji Glove.")]),
    "Shadow": dict(
        role="Ninja: Throw; can leave at any time on the Floating Continent.",
        tips=["Don't let him leave without the countdown: see Walkthrough > Floating Continent."],
        gear=[("Whole game", "Shuriken/Ninja Star to throw; Tack Star; fast weapons.")]),
    "Edgar": dict(
        role="Tools (Auto Crossbow, Bio Blaster, Chain Saw, Drill...).",
        tips=["Tools don't use Vigor the same way Fight does: the Chain Saw/Drill are strong; Auto Crossbow hits everything."],
        gear=[("Early", "Tools to buy at Figaro Castle."), ("Late", "Drill, Flash, Debilitator, Air Anchor as needed.")]),
    "Sabin": dict(
        role="Blitz (mod: menu), martial arts.",
        tips=["Blitzes: Pummel, AuraBolt, Suplex, Fire Dance, Mantra, Air Blade, Spiraler, Bum Rush.",
              "He can fight without a weapon (claws/gloves)."],
        gear=[("Early", "Starting claws."), ("Late", "High-BP claws, Hyper Wrist/Sprint.")]),
    "Celes": dict(
        role="Runic (absorbs magic) + natural magic.",
        tips=["Runic absorbs offensive spells: useful against magic bosses."],
        gear=[("Early", "Knight's sword."), ("Late", "Strong swords + magic armor.")]),
    "Strago": dict(
        role="Lores (spells learned from monsters).",
        tips=["Lores are learned by being hit by the attack; see More > Lores for who casts it."],
        gear=[("Whole game", "Rods/Mithril Rod, magic robes.")]),
    "Relm": dict(
        role="Sketch (copies an attack).",
        tips=["Sketch can fail or show a random attack."],
        gear=[("Whole game", "Brushes (Magical Brsh, Rainbow Brsh), magic hats.")]),
    "Setzer": dict(
        role="Slot (+ Dice with the mod).",
        tips=["Joker Doom is very powerful but can fail; Dice are rebalanced by the mod."],
        gear=[("Early", "Cards."), ("Late", "Fixed Dice, Dice to use with Offering.")]),
    "Mog": dict(role="Dances (depending on terrain).", tips=["Learn Dance in battle on the matching terrain."],
                gear=[("Whole game", "Spears: Mithril Pike, Trident...; light weapons.")]),
    "Gau": dict(role="Rage: copies Veldt monsters.", tips=["Use Leap on the Veldt; he learns Rages in battle."],
                gear=[("Whole game", "Bare-handed weapons / Wing Edge.")]),
    "Gogo": dict(role="Mimic + configurable commands.", tips=["Mimic repeats the previous ally's action."],
                 gear=[("Whole game", "Versatile equipment.")]),
    "Umaro": dict(role="Fixed Berserk; automatic Throw.", tips=["Permanent Berserk equipment."],
                  gear=[("Whole game", "He uses relics but no weapons.")]),
}

SIDEQUESTS = [
    dict(title="Cursed Shld → Paladin Shld", text="The old man in Narshe gives the Cursed Shld. Fight 256 battles with a character other than Gogo wearing it to purify it into the Paladin Shld.", g=True),
    dict(title="Ragnarok", text="The Narshe weapon shop owner lets you choose the Ragnarok Esper OR the sword: picking one loses the other (the sword can be traded at the Colosseum).", g=True),
    dict(title="Colosseum", text="Wager an item to fight a monster and win a rare item (see More > Colosseum). The prizes are read from the ROM.", g=False),
    dict(title="Fanatics' Tower", text="A tower with no magic: Gem Box, Safety Bit, Genji Shld, Stunner, Force Armor, Air Anchor.", g=False),
    dict(title="Veldt / Rages", text="Gau learns Rages with Leap. The monsters met on the Veldt are in the Bestiary (World page).", g=True),
    dict(title="Water Harmony (Mog's dance)", text="Mog must fight in water during the World of Balance (Lete River or Serpent Trench), otherwise it is lost for good.", g=True),
    dict(title="Force Field (Lore)", text="Only learned from the Fiend statue in Kefka's Tower, in a single fight, with Strago present.", g=True),
]
LORE_HINT = "Who casts each Lore is read from the monsters' AI scripts (ROM)."

CONTENT = {"formulas": FORMULAS, "mods": [dict(group=g, title=t, text=x) for g, t, x in MODS],
           "sidequests": SIDEQUESTS, "lore_hint": LORE_HINT}
