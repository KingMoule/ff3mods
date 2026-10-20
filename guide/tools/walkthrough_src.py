"""Hand-written walkthrough source (English).

CHESTS are not written here: they are read from the ROM (extract.py) and attached to the FIRST chapter
whose entry lists their map. Each chapter entry can therefore limit the maps it covers with `maps=[...]`
(otherwise: every map of the location). This avoids showing, from the very start of Narshe, a chest that
is only reachable much later.

Cross-check: order and rewards were compared with the Caves of Narshe walkthrough
(cavesofnarshe.com, GBA version: some names differ); `c=True` = confirmed by that guide,
`g=True` = inferred, unverified (neither ROM nor guide).
Item names below are the SNES US ROM names (Tonic = Potion, Potion = Hi-Potion, Tincture = Ether,
Ether = Hi-Ether, Fenix Down = Phoenix Down, Revivify = Holy Water, Soft = Gold Needle,
RunningShoes = Hermes Sandals, Atlas Armlet = Gigas Glove, Pod Bracelet = Guard Bracelet).

Event kinds (k): item, esper, char, boss, learn, note, shop.
Flags: m = missable (exclusive / limited window); lost="reason" = LOST FOR GOOD if not done at that moment
(shown in red, counted and filterable). On a chapter entry, lost="reason" applies to every chest of the entry.
"""


def E(k, text, m=False, g=False, item=None, esper=None, mon=None, c=False, lost=None):
    d = {"k": k, "t": text}
    if m:
        d["m"] = True
    if g:
        d["g"] = True
    if c:
        d["c"] = True
    if item:
        d["item"] = item
    if esper:
        d["esper"] = esper
    if mon:
        d["mon"] = mon
    if lost:
        d["lost"] = lost
        d["m"] = True
    return d


# id -> (name, ROM maps). Maps are used for chests and random encounters.
LOC = {
    "narshe_town": ("Narshe (town)", [20, 104, 105, 106, 107]),
    "narshe_elder": ("Elder's House (Narshe)", [30]),
    "narshe_mines": ("Narshe Mines", [41, 42, 48, 49, 50, 51, 52]),
    "narshe_wor": ("Narshe (World of Ruin)", [30, 32, 33, 34, 35, 36, 37, 38, 39, 43, 44]),
    "umaro_cave": ("Umaro's Cave (Narshe)", [281, 282]),
    "figaro_wob": ("Figaro Castle", [55, 57, 58, 59, 60, 61]),
    "figaro_wor": ("Buried Figaro Castle (basement)", [53, 62, 63, 64, 65, 66]),
    "cave_sf_wob": ("Cave to South Figaro", [69, 70, 71, 72, 73]),
    "cave_sf_wor": ("Cave to South Figaro (World of Ruin)", [68, 90, 92]),
    "south_figaro": ("South Figaro", [74, 75, 76, 77, 78, 80, 81, 83, 84, 85, 86, 87, 88, 89, 91]),
    "duncan": ("Duncan's Hut", [93, 94]),
    "kolts": ("Mt. Kolts", [95, 96, 97, 98, 100, 101, 102, 103]),
    "returners": ("Returner Hideout", [108, 109, 110, 111, 112, 113]),
    "lete": ("Lete River", [190]),
    "camp": ("Imperial Camp", [117]),
    "doma": ("Doma Castle", [121, 123, 124, 285]),
    "doma_dream": ("Cyan's Dream (Doma)", [125, 126, 144, 321, 322]),
    "phantom_forest": ("Phantom Forest", [132, 133, 134, 135, 140]),
    "phantom_train": ("Phantom Train", [141, 142, 143, 146, 147, 149, 152, 153]),
    "baren": ("Baren Falls", [155, 156, 166]),
    "mobliz": ("Mobliz", [150, 154, 157, 158, 159, 160, 161, 162, 163, 164, 165]),
    "crescent": ("Crescent Mountain", [167, 168]),
    "trench": ("Serpent Trench", [175]),
    "nikeah": ("Nikeah", [169, 171, 172, 173, 187]),
    "ferry": ("Nikeah Ferry", []),
    "kohlingen": ("Kohlingen", [188, 189, 191, 194, 195, 197]),
    "owzer_wob": ("Owzer's Mansion (Jidoor)", [209]),
    "owzer_wor": ("Owzer's Mansion: the paintings", [207]),
    "jidoor": ("Jidoor", [198, 200, 201, 202, 203, 204, 205, 206, 208]),
    "zozo": ("Zozo", [221, 225, 226]),
    "mt_zozo": ("Mt. Zozo", [176, 177, 178, 179, 180, 181]),
    "opera": ("Opera House", [231, 232, 233, 234, 235, 237, 238]),
    "albrook": ("Albrook", [323, 324, 325, 326, 327, 328, 330, 332]),
    "tzen": ("Tzen", [305, 306, 307, 308, 309, 310, 312]),
    "collapsing": ("Collapsing House (Tzen)", [311]),
    "maranda": ("Maranda", [196, 284, 288, 289, 290]),
    "vector": ("Vector", [240, 242, 243, 244, 245, 246, 247, 248, 249, 251, 252, 253]),
    "castle_vector": ("Imperial Palace (Vector)", [250]),
    "factory": ("Magitek Research Facility: conveyors", [262, 263]),
    "magitek_res": ("Magitek Research Facility: laboratory", [264, 269, 270, 271, 273, 274]),
    "espervillle": ("Esper World", [217, 218, 219]),
    "thamasa": ("Thamasa", [340, 341, 343, 344, 345, 346, 347, 348, 349, 350]),
    "burning": ("Burning House (Thamasa)", [351]),
    "imperial_base": ("Imperial Base (observation post)", [377, 378]),
    "sealed_gate": ("Sealed Gate Cave", [382, 383, 384, 385, 386, 391]),
    "esper_caves": ("Thamasa mountain (Ultros, Relm)", [371, 372, 373, 374, 375]),
    "floating": ("Floating Continent", [393, 394]),
    "hero_cave": ("Northwest Cave", [185, 186]),
    "darill": ("Darill's Tomb", [297, 298, 299, 300]),
    "phoenix": ("Phoenix Cave", [313, 314, 315, 316, 318, 317]),
    "veldt_cave": ("Cave on the Veldt", [353]),
    "fanatics": ("Fanatics' Tower", [359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370]),
    "ancient_cave": ("Cave to the Ancient Castle", [401, 402]),
    "ancient": ("Ancient Castle", [396, 397, 398, 400, 406, 407, 408]),
    "zone_eater": ("Inside the Zone Eater", [276, 277, 278, 279, 280]),
    "kefka": ("Kefka's Tower", [267, 287, 291, 292, 293, 294, 295, 296, 303, 304, 329, 331, 334, 335, 337, 338, 339,
                                 352, 354, 355, 409, 410, 411, 412]),
    "colosseum": ("Colosseum", [413]),
}

L_WORLD = "The World of Balance is destroyed after the Floating Continent: no way back"

CHAPTERS = [
    # ------------------------------------------------------------------ WORLD OF BALANCE
    dict(id="b1", world="B", title="Narshe: the assault (Terra)",
         intro="Terra, Biggs and Wedge march on Narshe in Magitek Armor. Nothing to collect before the Esper scene.",
         locs=[
             dict(loc="narshe_mines", title="Narshe Mines (opening)", nochest=True, boss=["Whelk"], events=[
                 E("boss", "Boss: Whelk (shell + head). Do not hit the shell with lightning: it counters. Aim at the head; Terra has the Magitek command.", mon=["Whelk"], c=True),
                 E("note", "Put everyone in the back row: physical damage taken is halved (see Formulas).", c=True),
             ]),
         ]),
    dict(id="b2", world="B", title="Narshe: the escape (Locke and the Moogles)",
         intro="Terra wakes up at an old man's house, then Locke takes over in the mines with the Moogles.",
         locs=[
             dict(loc="narshe_town", title="Old man's house (Terra wakes up)", nochest=True, events=[
                 E("item", "Elixir: examine the clock in the room where Terra wakes up (hidden item).", c=True, item="Elixir"),
                 E("item", "Sleeping Bag x2: given by the old man when you wake up.", c=True),
             ]),
             dict(loc="narshe_mines", title="Narshe Mines: tunnels (variable chests)", maps=[50], boss=["Marshal"], events=[
                 E("learn", "Mog learns the dance Twilight Requiem (Dusk Requiem) in the very first fight with the Moogles.", c=True),
                 E("item", "MithrilKnife: common steal from the Guard Leader (Locke). Steal it before killing him.", c=True, item="MithrilKnife"),
                 E("boss", "Boss: Marshal / Guard Leader (with 2 Lobo).", mon=["Marshal"], c=True),
                 E("note", "The 2 chests here CHANGE later: left one Sleeping Bag → Elixir; right one Fenix Down → Pod Bracelet (Guard Bracelet, World of Ruin). "
                           "Leave the RIGHT chest closed if you want the Pod Bracelet.", c=True),
             ]),
         ]),
    dict(id="b3", world="B", title="Adventurers' school and the road to Figaro",
         intro="Narshe shuts its doors on you. The adventurers' school (northwest) has 3 rooms with loot before you head to Figaro.",
         locs=[
             dict(loc="narshe_town", title="Adventurers' school", maps=[105, 106, 107], events=[
                 E("note", "School bucket (examine it): restores HP/MP and cures statuses, unlimited.", c=True),
                 E("note", "Rightmost room (Environmental Science): one chest is a monster (Lobo); one pot holds a Tincture (Ether).", c=True),
             ]),
         ]),
    dict(id="b4", world="B", title="Figaro Castle",
         intro="Terra and Edgar. Take Locke's Mithril Shield BEFORE talking to Edgar: Locke leaves afterwards. Kefka attacks and the castle sinks.",
         locs=[
             dict(loc="figaro_wob", lost="The castle sinks into the sand after the Floating Continent: these 4 chests cannot be reopened in the World of Ruin", events=[
                 E("char", "Edgar joins the party (Auto Crossbow). Story event, no choice.", c=True),
                 E("shop", "Tool shop: NoiseBlaster and Bio Blaster (handy against Magitek). Discounts when Edgar is the party leader.", c=True),
                 E("note", "Grab the 4 chests of the castle now: it will vanish from the World of Balance (the World of Ruin basement is a different dungeon).", g=True),
             ]),
         ]),
    dict(id="b5", world="B", title="Figaro Cave (first visit)",
         intro="Escape under the desert. The 3 chests in the cave are variable-content chests: Fenix Down / Tincture now, X-Potion / Thunder Rod with Locke, Hero Ring in the World of Ruin. One roll only.",
         locs=[
             dict(loc="cave_sf_wob", maps=[72, 73, 69, 70], events=[
                 E("note", "Advice: do NOT touch any of these chests now. Each chest is filled with a single item depending on progress: the first one you open is the only one you will get (the best one is in the World of Ruin: Hero Ring).", c=True),
                 E("item", "Possible steal from Urok: Remedy is better than Tonic.", c=True),
                 E("note", "Do not step on the tile just in front of the exit: it permanently removes the chance to see the flipping-out scene in battle.", c=True),
             ]),
         ]),
    dict(id="b6", world="B", title="South Figaro",
         intro="Shops, town and the rich man's house. Barrel contents change after Locke's scenario (the \"later\" item is better).",
         locs=[
             dict(loc="south_figaro", title="South Figaro (visit 1)", maps=[75, 74, 84, 86], events=[
                 E("note", "Several town items are variable (Tonic → X-Potion, Eyedrop → Remedy, Antidote → Tent, Green Cherry → Tent, Soft → Elixir): opening now = missing the \"later\" version.", c=True),
                 E("note", "Elixir: clock in the big house in the northwest (hidden room behind it).", c=True),
                 E("shop", "Weapon shop: RegalCutlass (Terra), MithrilBlade (Locke), Edgar's tools.", c=True),
                 E("shop", "Relic shop: Jewel Ring (anti-Petrify, essential later) and Star Pendants.", c=True),
                 E("note", "A secret passage leads to a merchant upstairs (3rd door: 500/1500/1000 gil and a monster chest).", c=True),
             ]),
         ]),
    dict(id="b7", world="B", title="Duncan's Hut and Mt. Kolts",
         intro="Edgar finds his brother Sabin. Fight against Vargas.",
         locs=[
             dict(loc="duncan", events=[E("note", "Tonic: bucket in the starting hut of the chapter.", c=True)]),
             dict(loc="kolts", boss=["Vargas"], events=[
                 E("char", "Sabin joins mid-fight against Vargas (+ 2 Ipooh). Finish with the Raging Fist Blitz.", mon=["Vargas", "Ipooh"], c=True),
                 E("note", "Pummel (Blitz 1) is already known by Sabin.", c=True),
             ]),
         ]),
    dict(id="b8", world="B", title="Returner Hideout",
         intro="Banon invites you to join the Returners. The group then splits into three scenarios.",
         locs=[
             dict(loc="returners", lost="Returner Hideout is not accessible in the World of Ruin (to be confirmed)", events=[
                 E("item", "Gauntlet: only if you ACCEPT Banon's offer immediately.", c=True, item="Gauntlet", lost="Gauntlet: obtained only by accepting Banon's offer right away (otherwise you get the Genji Glove)"),
                 E("item", "Genji Glove: decline Banon's offer (1 \"No\" = the Returner in the storeroom, 3 \"No\" = the one who interrupts the conversation). Exclusive with the Gauntlet here; another Genji Glove is in the Sealed Gate cave.", c=True, item="Genji Glove"),
                 E("note", "Note where you exit the hideout: a hidden passage in Banon's room leads to the Lete River and later to the Veldt.", c=True),
                 E("shop", "Hideout shop: first Potions (Hi-Potions) and Eyedrops.", c=True),
             ]),
         ]),
    dict(id="b9", world="B", title="Lete River and Terra's scenario",
         intro="Raft escape then the three teams: Terra (Narshe), Sabin (Mt. Kolts → Veldt), Locke (South Figaro). Suggested order: Terra, Sabin, Locke.",
         locs=[
             dict(loc="lete", boss=["Ultros"], events=[
                 E("boss", "Boss: Ultros (first fight, on the raft). If Banon falls: Game Over. Terra and Banon in the back row.", mon=["Ultros"], c=True),
                 E("learn", "Mog: Water Harmony can ONLY be learned in water (Lete River or Serpent Trench). Neither area is accessible afterwards.",
                   lost="Water Harmony (Mog's dance): fight in water (Lete or Serpent Trench) with Mog in the party. Impossible after the World of Balance", g=True),
             ]),
             dict(loc="narshe_mines", title="Narshe: Terra's scenario (Moogle cave)", maps=[52], events=[
                 E("note", "The chest in the Moogle room holds the Rune Edge. In the World of Ruin it will hold a Ribbon: take one OR the other, not both. "
                           "Rune Edge: stronger than the RegalCutlass but costs 12-18 MP per guaranteed critical; many players leave the chest for the Ribbon.", c=True),
                 E("note", "Security checkpoint: follow the sparkling light, otherwise the 9 rotating lights trigger a battle. Only here: Darkside (Rage); appears at 25% in the checkpoint.", c=True),
             ]),
         ]),
    dict(id="b10", world="B", title="Sabin's scenario: camp, forest, Phantom Train",
         intro="Imperial Camp near Doma (Cyan), Phantom Forest, Phantom Train. Shadow is recruitable (optional).",
         locs=[
             dict(loc="camp", title="Imperial Camp (Cyan)", lost="The Imperial Camp can no longer be visited after this scenario (≈)", events=[
                 E("char", "Cyan joins Sabin; he knows his SwdTechs (the gauge fills 2x faster in the mod).", c=True),
                 E("note", "Star Pendant: big tent chest → Kick / \"Hit\" (cat disguise) to open it; if you leave it, nothing.", c=True),
                 E("note", "Green Beret: dropped by the Satellite (monster chest in the 2-chest tent).", c=True),
                 E("item", "Black Belt: rare drop from the Captain; no other for a long time.", c=True, lost="Black Belt (rare drop from the camp Captain)"),
                 E("char", "Shadow: optional recruit (3,000 gil in Kohlingen later, otherwise here at the camp). He may leave at random before the Phantom Train.", c=True, g=True),
             ]),
             dict(loc="phantom_forest", events=[E("note", "Healing spring in the forest (top exit). Three ghost fights before the train.", c=True)]),
             dict(loc="phantom_train", boss=["GhostTrain"], lost="You cannot return to the Phantom Train", events=[
                 E("boss", "Boss: Ghost Train (weak to fire; Fenix Downs hurt it). Optional: Siegfried (100 HP) → Green Cherry; Apparition (monster chest) → Hyper Wrist.", mon=["GhostTrain"], c=True),
                 E("note", "Hidden Tent in the top-left corner of the cabin car; Tent on the left of Siegfried's compartment (you cannot face the right tile: Fairy Ring lost).", c=True),
                 E("note", "Earrings: dining car chest behind the waiters.", c=True),
                 E("note", "Next car: 4 chests (Fenix Down, Sniper Sight, Fenix Down, monster chest M-TekArmor). There is no way back to the Train.", c=True),
             ]),
         ]),
    dict(id="b11", world="B", title="Sabin's scenario: Baren, Veldt, Mobliz, Crescent, Trench",
         intro="Sabin and Cyan jump into Baren Falls, meet Gau on the Veldt, cross Mobliz and the Serpent Trench to Nikeah.",
         locs=[
             dict(loc="baren", events=[
                 E("note", "Shadow leaves the group at the falls. Before that: unequip his items, relics and Esper (Ninja Gear and RunningShoes to Sabin, Atlas Armlet to Cyan).", c=True),
                 E("boss", "Boss: Rhizopas (60 s after the Opinicus). Common drop: Remedy.", c=True),
             ]),
             dict(loc="mobliz", events=[
                 E("char", "Gau: on the Veldt, throw him Dried Meat (buy it in Mobliz). Sabin and Cyan must be alive for the scene.", c=True),
                 E("item", "Tintinabar: reward from the wounded soldier after delivering the 5 parcels.", c=True, item="Tintinabar", g=True),
                 E("shop", "Mobliz shop: Dried Meat (at least 1), Kotetsu for Cyan. Keep 2,500 gil.", c=True),
             ]),
             dict(loc="crescent", events=[
                 E("note", "Gau's scene takes 500 gil from you if you have it (otherwise Cyan keeps it).", c=True),
                 E("item", "Tonic: small tile on the left (where Gau finds it).", c=True),
             ]),
             dict(loc="trench", lost="The Serpent Trench is no longer accessible after this chapter: take both chests (RIGHT forks)", events=[
                 E("note", "Take the right-hand forks: X-Potion (1st fork), Green Beret (2nd fork, marked tile to drain the water).", c=True),
             ]),
             dict(loc="nikeah", events=[E("note", "Elixir: clock in the Nikeah inn.", c=True)]),
         ]),
    dict(id="b12", world="B", title="Locke's scenario: South Figaro",
         intro="Locke infiltrates South Figaro and follows a secret passage (password: \"Courage\").",
         locs=[
             dict(loc="south_figaro", title="South Figaro (Locke's scenario)", maps=[87, 89], events=[
                 E("note", "Merchant / officer: steal their clothes (Plumed Hat, Dirk) to proceed. Give the Cider to the old servant to reveal the secret passage.", c=True),
                 E("char", "Celes is freed: she joins the party (Runic, magic). First item: Clock Key.", c=True),
             ]),
             dict(loc="cave_sf_wob", title="Figaro Cave (Locke's scenario)", maps=[69, 70], boss=["TunnelArmr"], events=[
                 E("note", "Contents of the upper chest now: Thunder Rod (it breaks); later, Hero Ring (World of Ruin). Better to leave it closed.", c=True),
                 E("boss", "Boss: Tunnel Armor (1,300 HP). Steal Air Lancet (rare) with Locke.", c=True),
             ]),
         ]),
    dict(id="b13", world="B", title="Reunion in Narshe",
         intro="The teams meet in Narshe to defend the Esper. Fight against Hell's Rider then Kefka. Afterwards: rest and preparations.",
         locs=[
             dict(loc="narshe_mines", title="Narshe: defending the Esper", nochest=True, boss=["Kefka#298"], events=[
                 E("boss", "Boss: Hell's Rider (Lv 14) then Kefka (Lv 18, 3,000 HP, vulnerable to Stop). If the team is wiped you return to the save point at 1 HP and can steal again.", c=True),
                 E("item", "Peace Ring: dropped by Kefka (not very useful).", c=True),
             ]),
             dict(loc="narshe_elder", title="Narshe: Elder's House (treasure room)", events=[
                 E("note", "Elixir: clock in the Elder's House.", c=True),
                 E("note", "Treasure room (east shack): Hyper Wrist, Sneak Ring, Wall Ring, ThiefKnife, Earrings, Elixir, 5,000 gil.", c=True),
             ]),
             dict(loc="narshe_town", title="Narshe (rest of the town)", maps=[20], events=[
                 E("note", "The Sprint Shoes chest in Narshe is only accessible once the town is open (after defending the Esper).", g=True),
                 E("shop", "Weapon shop: Hawk Eye... for Locke; armor shop: Mithril Shld for everyone.", c=True),
             ]),
         ]),
    dict(id="b14", world="B", title="Kohlingen, Jidoor and Zozo",
         intro="You find Rachel in Kohlingen (Locke), then the Zozo tower where Terra is held.",
         locs=[
             dict(loc="kohlingen", events=[
                 E("note", "Elixir: clock in Rachel's house. Green Beret: big house to the northeast (back entrance).", c=True),
                 E("char", "Shadow: 3,000 gil at the Kohlingen inn. He leaves at random afterwards; before the Floating Continent decide whether to bring him (see Floating Continent).", c=True),
                 E("shop", "Fuma/Flame Scrolls (Shadow) at the weapon shop.", c=True),
             ]),
             dict(loc="owzer_wob", events=[E("note", "Tincture: one of the buckets of Owzer's mansion.", c=True)]),
             dict(loc="zozo", boss=["Dadaluma"], events=[
                 E("note", "Chain Saw: chest behind a wall that opens when the clock is set to 6:10:50.", c=True),
                 E("note", "Tincture (top tower), Potion and Tincture (pots on the spiral stairs), Fire Knuckle (small room), Thief Glove (High Tower), RunningShoes and X-Potion (two chests in Dadaluma's room).", c=True),
                 E("boss", "Boss: Dadaluma (Zozo, Lv 22). Common steal ThiefKnife, rare Thief Glove.", mon=["Dadaluma"], c=True),
                 E("esper", "Ramuh: Magicite found in Zozo (collected after the episode with Terra).", c=True, esper="Ramuh"),
             ]),
         ]),
    dict(id="b15", world="B", title="Opera House, Albrook, Tzen, Maranda and Vector",
         intro="Ultros at the opera against Setzer, then the infiltration of Vector.",
         locs=[
             dict(loc="jidoor", events=[
                 E("shop", "Auction House: Golem and Zone Seeker (Espers for sale), Angel Wings, Angel Ring: random rotation.", c=True),
             ]),
             dict(loc="opera", boss=["Ultros#301"], events=[
                 E("char", "Setzer joins after the opera (balloon plan). The opera allows limited failures: 3 retries then Game Over.", c=True),
                 E("boss", "Boss: Ultros (4th position, 2,550 HP each). Use Ramuh and Earrings.", mon=["Ultros#301"], c=True),
             ]),
             dict(loc="albrook", events=[
                 E("note", "Elixir: clock in the hallway between the armor shop and the cafe. Potion: barrel near the inn; Tincture: pot in the weapon shop; Warp Stone: dock crate.", c=True),
                 E("shop", "Wall Ring x4 (bosses), Earrings, Hero Ring (1-2), Poison Claw for Sabin.", c=True),
             ]),
             dict(loc="tzen", events=[
                 E("esper", "Seraph: buy it from a crook in Tzen (3,000 gil); later only 10 gil in the World of Ruin.", c=True),
             ]),
             dict(loc="maranda", events=[
                 E("note", "Revivify (bottom crate, west of the south exit) and Remedy (one of the 2 crates near the couple): free.", c=True),
                 E("note", "Lola's dialogue depends on the Mobliz parcel. Carrier pigeon: read it before leaving.", c=True),
             ]),
             dict(loc="vector", maps=[252], events=[
                 E("shop", "Weapon shop: Blossom (wind dirk). Buy it now if you want it.", c=True),
                 E("note", "Guardian: indestructible. Run, or Confuse a member who uses the Smoke Bomb.", c=True),
             ]),
         ]),
    dict(id="b16", world="B", title="Magitek Research Facility",
         intro="Descend into the pit then the lab. After Number 128 there is no coming back. Pick up EVERYTHING before leaving.",
         locs=[
             dict(loc="factory", lost="Magitek Research Facility is inaccessible afterwards: every unopened chest is lost", events=[
                 E("note", "Conveyors: Flame Sabre (far left through the pipe), Tincture, X-Potion, ThunderBlade, Remedy, DragoonBoots (relic), Gold Shld, Gold Helmet, Gold Armor, Tent.", c=True),
                 E("note", "Blizzard and Zephyr Cape: hidden room among the Imperial crates, under the 5th crate (facing the first crate: 5 steps down, right, 1 step back).", c=True),
             ]),
             dict(loc="magitek_res", boss=["Ifrit", "Shiva"], lost="Research Facility inaccessible afterwards", events=[
                 E("boss", "Boss: Number 024 (Esper room), then Ifrit (3,300 HP) and Shiva (3,000 HP).", mon=["Ifrit", "Shiva"], c=True),
                 E("esper", "Ifrit: Magicite after the Ifrit/Shiva fight. Take both.", m=True, esper="Ifrit", lost="Ifrit and Shiva: the Magicites are lost if you leave the room without picking them up", c=True),
                 E("esper", "Shiva: Magicite after the fight.", esper="Shiva", lost="Ifrit and Shiva (see above)", c=True),
                 E("note", "Break Blade (Stoneblade): hidden chest to the left of the bottom-left tube in the tube room (spell: Break).", c=True),
                 E("boss", "Boss: Number 128 (3,276 HP) + blades. After the fight: 6 Espers (Bismarck, Maduin, Unicorn, Catoblepas, Phantom, Carbuncle).", c=True),
                 E("note", "Number 128: rare steal Tempest (Kazekiri) (also a common drop); another Tempest is in the Sealed Gate.", c=True),
             ]),
         ]),
    dict(id="b17", world="B", title="Narshe: alliance, Mog and the Sealed Gate",
         intro="The Espers of Vector, Terra's flashback, then the defense of Narshe and the Sealed Gate cave.",
         locs=[
             dict(loc="narshe_town", title="Narshe (Mog, shops)", nochest=True, events=[
                 E("char", "Mog: by defending the Moogle against Lone Wolf. If you chase the treasure (Gold Hairpin), Mog is LOST.", c=True, lost="Mog: save the Moogle (do not chase Lone Wolf for the Gold Hairpin)"),
                 E("learn", "Mog dances already learned at this stage: Wind Rhapsody (plains near Narshe), Forest Nocturne, Desert Lullaby, Earth Blues (slopes of Mt. Kolts), Twilight Requiem, Love Serenade (Zozo).", c=True),
                 E("shop", "Narshe shops: Hawk Eye for Locke, Tiara for Terra, Gold Shld/Helmet.", c=True),
             ]),
             dict(loc="sealed_gate", lost=L_WORLD, boss=["AtmaWeapon"], events=[
                 E("note", "Chests: Assassin, Tempest, X-Potion, Ether, Genji Glove (left, after the puzzle), Elixir, Ether... and the small cave behind the stepping tile: 2 Magicite Shards, Ether, Atma Weapon.", c=True),
                 E("boss", "Boss: Atma Weapon (steal possible). Optional Ninja (weak to lightning).", mon=["AtmaWeapon"], c=True),
                 E("boss", "Kefka (triggers the Sealed Gate). Then Esper Valigarmanda/Midgardsormr (Narshe, World of Ruin).", c=True),
             ]),
         ]),
    dict(id="b18", world="B", title="Imperial Palace (Gestahl's banquet)",
         intro="After the Sealed Gate, Gestahl hosts a banquet: your score (max 93) decides your rewards.",
         locs=[
             dict(loc="castle_vector", lost=L_WORLD + " (≈)", events=[
                 E("note", "Banquet score: 50+ = Doma liberated; 67+ = the observation post house opens; 77+ = Tintinabar (Gestahl); 90+ = Merit Award (Imperial Elite).", c=True,
                   lost="Banquet score rewards (50, 67, 77, 90): the observation post door, Tintinabar, Merit Award"),
                 E("note", "In the palace after the banquet: Back Guard, Gale Hairpin, Revivify, X-Potion, Tincture.", c=True),
             ]),
             dict(loc="imperial_base", lost=L_WORLD + " (≈)", events=[
                 E("note", "Observation post house (if score ≥ 67): X-Potion, Cherub Down..., 41,000 gil in total (8,000 + 13,000 + 20,000), hidden Elixir to the south, Flame Sabre in the stove.", c=True),
             ]),
         ]),
    dict(id="b19", world="B", title="Thamasa and the Espers",
         intro="Cyan, Strago, Relm: the mountain behind Thamasa, the burning house, then Kefka's attack.",
         locs=[
             dict(loc="thamasa", events=[
                 E("char", "Strago joins (Lores) after the burning house. He learns a Lore when he sees an enemy cast it.", c=True),
                 E("note", "Barrels (Echo Screen, Green Cherry, Soft, Eyedrop, Fenix Down), Memento Ring: Strago's room upstairs.", c=True),
                 E("note", "If you did not unequip Shadow before his nap, he takes his gear with him when he leaves.", c=True),
             ]),
             dict(loc="burning", boss=["FlameEater"], lost="The burning house disappears after the fire", events=[
                 E("boss", "Boss: Flame Eater (burning house; avoid fire).", mon=["FlameEater"], c=True),
                 E("note", "Fire Rod (3rd room, right door) and Ice Rod (3rd room, left door, next room, right door).", c=True),
                 E("learn", "Lore: Self-Destruct, by Confusing the Balloons.", c=True),
             ]),
             dict(loc="esper_caves", boss=["Ultros#302"], lost="The mountain is no longer accessible once Relm is recruited (≈)", events=[
                 E("boss", "Boss: Ultros (3rd fight, 22,000 HP). Relm joins when his HP drops to ~10,240; Sketch makes him flee.", mon=["Ultros#302"], c=True),
                 E("note", "Heal Rod (1st room), Chocobo Suit and Tabby Suit (broken-bridge maze, via the upper collapse tile), X-Potion (loose tile far right).", c=True),
                 E("learn", "Lore: White Wind, when Venobennu uses it in front of Strago.", c=True),
             ]),
             dict(loc="espervillle", events=[
                 E("note", "After Kefka's attack the Espers are killed (Magicites). Interceptor is left behind in Thamasa.", c=True),
             ]),
         ]),
    dict(id="b20", world="B", title="Veldt, Rages and Lores before the end",
         intro="This is the last chance before the switch: Rages and Lores outside the World of Ruin.",
         locs=[
             dict(loc="doma", maps=[], title="Veldt and Lores (final preparations)", nochest=True, events=[
                 E("note", "No dance, Rage or Lore is lost for good here, except Water Harmony (already covered). Many enemies are only met in the World of Balance: Grenade Rage, Gaia Gear (rare steal from Briareus), Magic Urn...", c=True, g=True),
                 E("learn", "Lores to learn now with Strago: Doom, Dischord, Lv.3 Confuse, Lv.4 Flare, Lv.5 Death, Transfusion, Roulette, Traveler (Confuse an Unseelie outside South Figaro).", c=True),
             ]),
         ]),
    dict(id="b21", world="B", title="Floating Continent",
         intro="Last dungeon of the World of Balance. There is NO way back: the continent collapses. Bring Shadow if you want him, otherwise he stays.",
         locs=[
             dict(loc="floating", lost=L_WORLD, boss=["Number 024", "Air Force", "Dadaluma"], events=[
                 E("char", "Shadow (optional): for him to survive, wait for the countdown to hit 0:05 on the island before coming back. Jumping too early = Shadow lost for good.", c=True,
                   lost="Shadow: during the escape wait until 0:05 before jumping (6:00 total), otherwise he is lost"),
                 E("note", "Murasame: blue orb east of the entrance. Beret: blue orb below the save point (Relm). Elixir: small plateau with an orb (cracks in the floor).", c=True),
                 E("boss", "Boss: Air Force (then Ultima Weapon 24,000 HP, Kefka and Gestahl). Steal from Ultima Weapon: Ribbon (common), Elixir (rare).", mon=["Air Force"], c=True),
                 E("note", "Last chance: Genji Glove (rare steal from the Dragon, with ThiefKnife), Earrings/Angel Ring (steals), Rages and Lores unique to the World of Balance.", c=True, g=True),
             ]),
         ]),
    # ------------------------------------------------------------------ WORLD OF RUIN
    dict(id="r1", world="R", title="Solitary Island and first steps",
         intro="Celes wakes up alone with Cid. Feed him fish: his hidden health decides whether he survives, and his death is permanent.",
         locs=[
             dict(loc="albrook", title="Solitary Island and Albrook", maps=[], nochest=True, events=[
                 E("note", "Cid: give him fish (Fish +16, Yummy +32, Rotten −4, Slow −16). At 256 he is cured for good; below 30 he dies (permanent, and it changes Celes' dialogue).", c=True),
                 E("note", "Equip Celes with an Amulet or Ribbon against Bone Powder (Zombie = Game Over).", c=True),
                 E("esper", "Quetzalli: Magicite washed up on the Solitary Island beach.", c=True),
                 E("note", "Albrook, Tzen, Mobliz, Nikeah, South Figaro, Kohlingen: same chests as in the World of Balance (nothing more if they were already taken).", c=True),
             ]),
             dict(loc="tzen", title="Tzen and the Collapsing House", events=[
                 E("char", "Sabin: save the child before the collapse (6:00). Shop: Jewel Ring (last chance), Poison Claw.", c=True),
                 E("esper", "Seraph: only 10 gil here if you did not buy it earlier.", c=True),
             ]),
             dict(loc="collapsing", events=[E("note", "Heal Rod (end of the hallway): do not miss it; Pearl Rod, Tincture, Magicite, Drainer (optional).", c=True)]),
         ]),
    dict(id="r2", world="R", title="Mobliz, Nikeah, South Figaro, buried Figaro",
         intro="The trio: Terra (Mobliz), then the Crimson Robbers quest (Edgar disguised as Gerad).",
         locs=[
             dict(loc="mobliz", title="Mobliz: Terra and the children", events=[
                 E("esper", "Fenrir: given by the child at the entrance after Humbaba leaves.", c=True),
                 E("note", "Terra does not join yet: come back after beating Humbaba (Narshe).", c=True),
             ]),
             dict(loc="nikeah", title="Nikeah (Ruin)", events=[E("shop", "Enhancers x3 (+7 magic), Diamond Vest, Gale Hairpin.", c=True)]),
             dict(loc="south_figaro", title="South Figaro (Ruin)", maps=[], nochest=True, events=[
                 E("shop", "Gold Lance, DiamondArmor, Amulets (enough for 4), RunningShoes.", c=True),
                 E("note", "Gerad (Edgar) leaves the inn with the Crimson Robbers: follow him.", c=True),
             ]),
             dict(loc="cave_sf_wor", events=[
                 E("note", "Ether, X-Potion, Hero Ring: the cave chests only fill once; if you already took them in the World of Balance, these are the old items.", c=True),
             ]),
             dict(loc="figaro_wor", boss=["Tentacle"], events=[
                 E("note", "Buried castle chests: Crystal Helm, Gravity Rod, X-Potion, Ether (4-chest room); Regal Crown (left door); Soul Sabre (middle armor of the treasure room).", c=True),
                 E("boss", "Boss: 4 Tentacles (Grab). You can let the Robbers go.", c=True),
             ]),
         ]),
    dict(id="r3", world="R", title="Kohlingen, Darill's Tomb, Setzer",
         intro="Setzer drowns his sorrows in Kohlingen. Darill's Tomb holds strong equipment.",
         locs=[
             dict(loc="kohlingen", title="Kohlingen (Ruin)", maps=[], nochest=True, events=[
                 E("char", "Setzer: at the Kohlingen bar; Celes brings him around. Buy Dice (5,000 gil) and Doom Darts (Colosseum).", c=True),
             ]),
             dict(loc="darill", boss=["Dullahan"], events=[
                 E("note", "Genji Helmet (bottom-right path), Crystal Mail (bottom-left room), Czarina Gown (Relm), Man Eater (room after the 2nd turtle), Exp. Egg hidden behind the tomb carving.", c=True),
                 E("boss", "Boss: Dullahan. Monster chest Angler Whelk: kill head AND shell together for 2 Dragon Claws.", c=True,
                   lost="Dragon Claw: only source = Angler Whelk, head and shell must die together"),
                 E("esper", "Bahamut: drop from Deathgaze (random flying encounter).", c=True),
             ]),
             dict(loc="maranda", title="Maranda (Ruin)", maps=[], nochest=True, events=[
                 E("shop", "Crystal Shld/Mail (x2), Dark Gear (Sabin).", c=True),
             ]),
         ]),
    dict(id="r4", world="R", title="Narshe: Mog, Umaro, Valigarmanda",
         intro="Narshe revisited: the mine, the Moogles, the snow, Umaro.",
         locs=[
             dict(loc="narshe_wor", maps=[38, 44], events=[
                 E("char", "Mog: in the Moogle cave (wall Mog stares at); you get the Moogle Charm (avoids battles). With 4 characters, Mog waits on the Falcon.", c=True),
                 E("note", "Ribbon: only if the Rune Edge was left in the chest. Elixir and Pod Bracelet: only if the mine chests are untouched.", c=True),
                 E("note", "Weapon shop: locked, needs Locke (he picks the lock).", c=True),
                 E("esper", "Valigarmanda: snowfields; Force Shld from the Ice Dragon.", c=True),
                 E("learn", "Mog: Snowman Rondo (last dance).", c=True),
             ]),
             dict(loc="umaro_cave", boss=["Umaro#272"], events=[
                 E("char", "Umaro: Mog must talk to him. Without Mog he will not join (you can come back).", c=True),
                 E("esper", "Midgardsormr: carved bone in the Sasquatch room (triggers the Yeti).", c=True),
                 E("note", "Gauntlet: lower chest after the upper room; Ether: upper chest; X-Ether.", c=True),
             ]),
         ]),
    dict(id="r5", world="R", title="Mobliz: Humbaba and Terra",
         intro="Humbaba (2) removes 2 characters from the party; Terra transforms permanently.",
         locs=[
             dict(loc="mobliz", title="Mobliz (Terra and Humbaba)", maps=[], nochest=True, events=[
                 E("char", "Terra: after the second fight against Humbaba (60,000 HP). She has permanent Morph.", c=True),
                 E("note", "Humbaba Breath removes 2 characters from the party: you find them again on the Falcon.", c=True),
             ]),
         ]),
    dict(id="r6", world="R", title="Zozo, Mt. Zozo, Cyan",
         intro="The pigeon, Mt. Zozo and the Storm Dragon.",
         locs=[
             dict(loc="mt_zozo", maps=[177, 179], boss=["Storm Drgn"], events=[
                 E("note", "Ice Shld, Red Cap (+25% HP), Thunder Shld, Aegis Shld (cave chests), Gold Hairpin (left opening outside).", c=True),
                 E("boss", "Boss: Storm Dragon (42,000 HP, weak to lightning). The trapped chest releases the dragon.", c=True),
                 E("char", "Cyan: only with 3 characters in the fight; otherwise he waits on the Falcon. Machinery Manual / Book of Secrets: Cyan's chest.", c=True),
             ]),
             dict(loc="zozo", title="Zozo (Ruin)", maps=[], nochest=True, events=[
                 E("note", "Rust-Rid (1,000 gil): on sale only if the pigeon was sent to Zozo.", c=True),
             ]),
         ]),
    dict(id="r7", world="R", title="Veldt, Gau, Shadow, Relm",
         intro="Gau is recruited in Veldt fights. The Cave on the Veldt hides Relm (or Shadow).",
         locs=[
             dict(loc="veldt_cave", boss=["SrBehemoth#281"], events=[
                 E("char", "Gau: Veldt fights with a free slot (about 57% encounter chance).", c=True),
                 E("char", "Shadow: rescued here only if you waited for him on the Floating Continent; otherwise Relm.", c=True),
                 E("note", "Rage Ring (room with the 4 hunters), Striker (switch room), Tiger Fangs (after Death Warden).", c=True),
             ]),
             dict(loc="owzer_wor", boss=["Chadarnook"], events=[
                 E("esper", "Lakshmi: drop from Chadarnook. Relm joins afterwards.", c=True),
                 E("note", "Moogle Suit (left door of the 1st room), Relic Ring (hidden behind the 3 doors). Only the LEFT door continues the dungeon.", c=True),
             ]),
             dict(loc="thamasa", title="Thamasa (Ruin)", maps=[], nochest=True, events=[
                 E("char", "Strago: play with Relm in the party. Interceptor is lost if a monster takes Dog Block from him.", c=True),
             ]),
         ]),
    dict(id="r8", world="R", title="Cyan's Dream (Doma)",
         intro="Cyan's Dream is only accessible here. Take everything before finishing.",
         locs=[
             dict(loc="doma", boss=["Curley"], events=[
                 E("note", "Elixir and Ether (clock in the bedroom), X-Potion, Fenix Down, Beads (small room on the outside wall).", c=True),
             ]),
             dict(loc="doma_dream", boss=["Wrexsoul"], lost="Cyan's Dream cannot be replayed: anything not taken is lost", events=[
                 E("esper", "Alexander: Magicite in the throne room.", c=True),
                 E("boss", "Boss: Wrexsoul (+ 2 Soul Savers). Do NOT use Banish: without having damaged him you lose the Pod Bracelet.", mon=["Wrexsoul", "SoulSaver"], c=True),
                 E("learn", "Cyan learns all remaining SwdTechs (Tempest, Oblivion).", c=True),
                 E("note", "Genji Glove (1st train car), Flame Shld (2nd car, needs the Lump of Metal), Ice Shld and X-Potion (train maze), Masamune after Wrexsoul.", c=True),
                 E("note", "Enemies unique to the dream (Weredragon, Alluring Rider, Pandora, Parasite, Coco): for your Rage and Lore lists (Holy, Doom, Roulette).", c=True,
                   lost="Rages/Lores from Cyan's Dream: encounter them before finishing"),
             ]),
         ]),
    dict(id="r9", world="R", title="Ancient Castle and Phoenix Cave",
         intro="Two major optional dungeons.",
         locs=[
             dict(loc="ancient_cave", events=[
                 E("note", "Wing Edge (left entrance room), Ether (right), Doom Darts (Master Tonberry's cave), X-Potion and Magicite Shard (left cave).", c=True),
                 E("boss", "Master Tonberry (monster chest, 22,000 HP). Put it to sleep, magic only.", c=True),
             ]),
             dict(loc="ancient", boss=["Blue Drgn"], events=[
                 E("esper", "Odin: statue in the throne room; Raiden: petrified queen (needs Odin).", c=True),
                 E("note", "Punisher (right), Master's Scroll (left, guarded by Samurai Soul: do not flee), Blizzard Orb and Gold Hairpin (right room), X-Ether (bucket in the queen's room).", c=True,
                   lost="Master's Scroll: if you flee Samurai Soul you can no longer fight it"),
                 E("boss", "Boss: Blue Dragon (underground hall) → Zantetsuken.", c=True),
             ]),
             dict(loc="phoenix", boss=["Red Dragon"], events=[
                 E("char", "Locke: three teams in the Phoenix Cave.", c=True),
                 E("esper", "Phoenix: Locke's chest.", esper="Phoenix", c=True),
                 E("note", "Wing Edge (bridge or fall: 400 damage), Ribbon (solidified lava), Dragon Horn (guarded by the Red Dragon).", c=True),
             ]),
         ]),
    dict(id="r10", world="R", title="Zone Eater (Gogo) and others",
         intro="Gogo is the last character.",
         locs=[
             dict(loc="zone_eater", events=[
                 E("char", "Gogo: the last character to recruit (inside the Zone Eater).", c=True),
                 E("note", "Genji Armor (right side), Magical Brsh (left), FakeMustache (far left), Zephyr Cape, Hero Ring (between two falls), Tack Star (falling ceiling), Thunder Shld, Ether, Red Jacket.", c=True),
             ]),
             dict(loc="fanatics", events=[
                 E("note", "Safety Bit, Air Anchor (hidden chest on the right), Genji Shld, Stunner, Force Armor, Gem Box (roof: Magic Master, Ultima on his death).", c=True),
                 E("note", "Fanatics' Tower: only Magic Urn (useful Rage) and Holy Dragon (Holy Lance) are worth not missing.", c=True),
             ]),
             dict(loc="hero_cave", events=[E("note", "Northwest Cave: Hero Ring.", g=True)]),
         ]),
    dict(id="r11", world="R", title="Kefka's Tower and Colosseum",
         intro="Three teams, a single path. Last chance for everything: Rages, Lores, items.",
         locs=[
             dict(loc="kefka", boss=["Kefka#282"], events=[
                 E("note", "Coronet, Fixed Dice, Minerva, Tack Star, Force Shld, Force Armor, Ribbon (several), Red Cap, Gauntlet, Nutkin Suit, Hero Ring, Aegis Shld (hidden, 11-step route), Megalixir, Rainbow Brsh.", c=True),
                 E("esper", "Crusader: after the Skull Dragon (Dragon Seal).", c=True),
                 E("boss", "Boss: Guardian (4-program cycle), the 3 Statues (Demon, Fiend, Goddess) then Kefka. Fiend: Force Field is only learned here.", c=True,
                   lost="Force Field (Lore): only from Fiend in Kefka's Tower"),
             ]),
             dict(loc="colosseum", events=[E("note", "The Colosseum lets you wager an item to win a rare item (see More > Colosseum).", c=True)]),
         ]),
]

# Chest position hints (map, x, y) -> text. Source: Caves of Narshe; cross-checked against the items read from the ROM.
CHEST_HINT = {
    (30, 55, 30): "Examine the clock in the Elder's House",
    (86, 7, 31): "Clock in the big house in the northwest (hidden room behind)",
    (94, 74, 27): "Bucket in the starting hut",
    (171, 57, 37): "Inn clock",
    (163, 51, 12): "Clock in the carrier-pigeon house",
    (330, 35, 7): "Clock in the hallway between the armor shop and the cafe",
    (197, 42, 10): "Clock in Rachel's house",
    (195, 37, 53): "Barely visible chest in the big northeast house: back entrance",
    (209, 125, 11): "In one of the buckets of Owzer's mansion",
    (225, 111, 52): "Behind a wall that opens when the clock reads 6:10:50",
    (225, 35, 11): "Small room behind the obvious door",
    (226, 72, 26): "Dadaluma's room, side chest",
    (226, 92, 27): "Dadaluma's room, side chest",
    (271, 8, 37): "Hidden to the left of the bottom-left tube in the tube room",
    (263, 55, 34): "Hidden room under the 5th Imperial crate (5 steps down from the 1st crate, right, 1 step back)",
    (263, 60, 33): "Same hidden room under the crates",
    (117, 45, 5): "Big tent: kick / \"Hit\" the chest (otherwise nothing)",
    (117, 19, 18): "2-chest tent, right chest",
    (117, 17, 18): "2-chest tent, left chest = monster (Satellite)",
    (117, 15, 8): "Tent behind the 2-chest tent",
    (147, 5, 5): "Dining car, behind the waiters",
    (146, 20, 7): "Cabin car, top-left corner (hidden)",
    (153, 20, 7): "Siegfried's compartment, empty tile on the left",
    (153, 21, 7): "Right tile: you cannot stand facing it, so it is unreachable",
    (100, 30, 33): "Hidden room to the right of the path/stairway",
    (110, 60, 19): "Hidden passage to the right of the 3 outside chests",
    (110, 43, 11): "One of the 3 outside chests (True Knight)",
    (110, 43, 13): "One of the 3 outside chests",
    (110, 45, 13): "One of the 3 outside chests (Air Lancet)",
    (52, 98, 53): "Moogle room (Rune Edge; Ribbon in the World of Ruin)",
    (351, 4, 52): "3rd room, right door",
    (351, 45, 7): "3rd room, left door then next room, right door",
    (375, 46, 27): "1st room of the mountain: Heal Rod",
}
