"""Source écrite à la main du walkthrough (français).

Les COFFRES ne sont pas écrits ici : ils sont lus dans la ROM (extract.py) puis rattachés aux lieux
via la liste `maps` de chaque lieu. Ici : l'ordre des chapitres, les événements (personnages, espers,
récompenses, boss, objets manquables) et les astuces.

Niveau de fiabilité : chaque événement porte `g=True` quand le détail est une déduction non
vérifiée dans la ROM (le script build_data.py recoupe seulement les objets/espers donnés par script).
Types d'événement (k) : item, esper, char, boss, learn, note, shop.
"""


def E(k, text, m=False, g=False, item=None, esper=None, mon=None):
    d = {"k": k, "t": text}
    if m:
        d["m"] = True
    if g:
        d["g"] = True
    if item:
        d["item"] = item
    if esper:
        d["esper"] = esper
    if mon:
        d["mon"] = mon
    return d


# id -> (nom, maps de la ROM). Les maps servent aux coffres et aux rencontres aléatoires.
LOC = {
    "narshe_town": ("Narshe (ville)", [20, 104, 105, 106, 107]),
    "narshe_mines": ("Mines de Narshe", [41, 42, 48, 49, 50, 51, 52]),
    "narshe_wor": ("Narshe (Monde de la Ruine)", [30, 32, 33, 34, 35, 36, 37, 38, 39, 43, 44]),
    "umaro_cave": ("Grotte d'Umaro (Narshe)", [281, 282]),
    "figaro_wob": ("Château de Figaro", [55, 57, 58, 59, 60, 61]),
    "figaro_wor": ("Château de Figaro enfoui (sous-sols)", [53, 62, 63, 64, 65, 66]),
    "cave_sf_wob": ("Grotte vers South Figaro", [69, 70, 71, 72, 73]),
    "cave_sf_wor": ("Grotte vers South Figaro (Monde de la Ruine)", [68, 90, 92]),
    "south_figaro": ("South Figaro", [74, 75, 76, 77, 78, 80, 81, 83, 84, 85, 86, 87, 88, 89, 91]),
    "duncan": ("Cabane de Duncan", [93, 94]),
    "kolts": ("Mont Kolts", [95, 96, 97, 98, 100, 101, 102, 103]),
    "returners": ("Repaire des Returners", [108, 109, 110, 111, 112, 113]),
    "lete": ("Rivière Lete", [190]),
    "camp": ("Camp impérial", [117]),
    "doma": ("Château de Doma", [121, 123, 124, 285]),
    "doma_dream": ("Rêve de Cyan (Doma)", [125, 126]),
    "phantom_forest": ("Forêt fantôme", [132, 133, 134, 135, 140]),
    "phantom_train": ("Train fantôme", [141, 142, 143, 144, 146, 147, 149, 152, 153, 321, 322]),
    "baren": ("Chutes de Baren", [155, 156, 166]),
    "mobliz": ("Mobliz", [150, 154, 157, 158, 159, 160, 161, 162, 163, 164, 165]),
    "crescent": ("Mont Crescent", [167, 168]),
    "nikeah": ("Nikeah", [169, 171, 172, 173, 187]),
    "ferry": ("Ferry de Nikeah", [175]),
    "kohlingen": ("Kohlingen", [188, 189, 191, 194, 195, 197]),
    "jidoor": ("Jidoor", [198, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209]),
    "zozo": ("Zozo", [221, 225, 226]),
    "mt_zozo": ("Mont Zozo", [176, 177, 178, 179, 180, 181]),
    "opera": ("Opéra", [231, 232, 233, 234, 235, 237, 238]),
    "albrook": ("Albrook", [323, 324, 325, 326, 327, 328, 330, 332]),
    "tzen": ("Tzen", [305, 306, 307, 308, 309, 310, 312]),
    "collapsing": ("Maison qui s'effondre (Tzen)", [311]),
    "maranda": ("Maranda", [196, 284, 288, 289, 290]),
    "vector": ("Vector", [240, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253]),
    "factory": ("Usine Magitek", [262, 263]),
    "castle_vector": ("Palais impérial (Vector)", [276, 277, 278, 279, 280]),
    "magitek_res": ("Centre de recherche Magitek", [264, 269, 270, 271, 273, 274]),
    "espervillle": ("Esperville", [217, 218, 219]),
    "thamasa": ("Thamasa", [340, 341, 343, 344, 345, 346, 347, 348, 349, 350]),
    "burning": ("Maison en flammes (Thamasa)", [351]),
    "imperial_base": ("Base impériale (poste d'observation)", [377, 378]),
    "sealed_gate": ("Grotte de la Porte scellée", [382, 383, 384, 385, 386, 391]),
    "esper_caves": ("Grottes des Espers (Mont Esper)", [371, 372, 373, 374, 375]),
    "floating": ("Continent flottant", [393, 394]),
    "hero_cave": ("Grotte du nord-ouest", [185, 186]),
    "darill": ("Tombe de Darill", [297, 298, 299, 300]),
    "phoenix": ("Grotte du Phénix", [313, 314, 315, 316, 318, 317]),
    "veldt_cave": ("Grotte du Veldt", [353]),
    "fanatics": ("Tour des Fanatiques", [359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370]),
    "ancient_cave": ("Grotte du Château antique", [401, 402]),
    "ancient": ("Château antique", [396, 397, 398, 400, 406, 407, 408]),
    "zone_eater": ("Grotte de Zone Eater", [319, 320]),
    "kefka": ("Tour de Kefka", [267, 287, 291, 292, 293, 294, 295, 296, 303, 304, 329, 331, 334, 335, 337, 338, 339,
                                 352, 354, 355, 409, 410, 411, 412]),
    "colosseum": ("Colisée", [413]),
}

CHAPTERS = [
    # ------------------------------------------------------------------ MONDE DE LA BALANCE
    dict(id="b1", world="B", title="Narshe : l'Esper gelé",
         intro="Terra, Biggs et Wedge marchent sur Narshe. Après le combat contre Whelk, Locke et les Moogles prennent le relais.",
         locs=[
             dict(loc="narshe_mines", title="Mines de Narshe (ouverture)", nochest=True, boss=["Whelk"], events=[
                 E("boss", "Boss : Whelk (ne frappez pas la coquille avec de la foudre ; visez la tête). Terra a la commande Magitek.", mon=["Whelk"]),
                 E("note", "Mettez tout le monde en rangée arrière : les dégâts reçus sont divisés par 2 (voir Formules).", g=True),
             ]),
             dict(loc="narshe_town", title="Narshe : ville, maison d'Arvis, école d'aventuriers", events=[
                 E("item", "Elixir : examiner l'horloge ouest de la pièce où Terra se réveille (objet caché)", g=True, item="Elixir"),
                 E("note", "École d'aventuriers (nord-ouest de la ville) : un seau (à examiner) restaure PV/PM et soigne les statuts, à volonté.", g=True),
             ]),
             dict(loc="narshe_mines", title="Mines de Narshe : défense des Moogles", boss=["Marshal"], events=[
                 E("learn", "Mog apprend la danse Dusk Requium s'il porte le dernier coup à l'ennemi (à éviter de rater)", m=True, g=True),
                 E("boss", "Combat : Marshal (chef des gardes) + 2 Lobo", mon=["Marshal"]),
                 E("note", "Les coffres de cette zone sont dans la liste ci-dessous (Fenix Down, Sleeping Bag).", g=True),
             ]),
         ]),
    dict(id="b2", world="B", title="Château de Figaro",
         intro="Terra, Locke et Edgar. Kefka attaque : le château s'enfonce sous le sable.",
         locs=[
             dict(loc="figaro_wob", events=[
                 E("char", "Edgar rejoint le groupe (Tools : Auto Crossbow, etc.)", g=True),
                 E("shop", "Boutique d'outils : achetez Noiseblaster / Bio Blaster si vous ne les avez pas (Edgar)", g=True),
                 E("note", "Le château quitte la carte après l'attaque de Kefka ; achats d'outils possibles plus tard dans le Monde de la Ruine.", g=True),
             ]),
         ]),
    dict(id="b3", world="B", title="Grotte vers South Figaro",
         intro="Fuite sous le désert. Attention : le contenu des 3 coffres change selon l'avancement (voir détail).",
         locs=[
             dict(loc="cave_sf_wob", events=[
                 E("note", "Les coffres de cette grotte partagent leur état : si vous les ouvrez à cette première visite, "
                           "ceux de la deuxième (scénario de Locke) sont déjà vides. Contenu de la 2e visite plus intéressant (Thunder Rod).", g=True),
             ]),
         ]),
    dict(id="b4", world="B", title="South Figaro",
         intro="Magasins, maison du riche et sous-sols. Shadow se tient dans le bar.",
         locs=[
             dict(loc="south_figaro", events=[
                 E("char", "Shadow : à recruter plus tard ; parlez-lui au bar (Gau/Shadow : voir Colisée et Continent flottant)", g=True),
                 E("note", "Quête de la clé : la clé Old Clock-Key et le Cider sont des objets de quête (voir « Objets rares » dans Plus).", g=True),
             ]),
         ]),
    dict(id="b5", world="B", title="Mont Kolts et la cabane de Duncan",
         intro="Edgar rejoint son frère jumeau Sabin. Combat contre Vargas.",
         locs=[
             dict(loc="duncan", events=[E("note", "Seau près de l'entrée : Tonic caché (examiner).", g=True)]),
             dict(loc="kolts", boss=["Vargas"], events=[
                 E("char", "Sabin rejoint le groupe après le combat contre Vargas (+ 2 Ipooh)", mon=["Vargas", "Ipooh"]),
                 E("learn", "Sabin possède déjà Pummel (Blitz niveau 1)"),
             ]),
         ]),
    dict(id="b6", world="B", title="Repaire des Returners",
         intro="Banon vous propose de rejoindre les Returners. Le groupe se sépare en trois scénarios (Terra/Edgar/Banon, Sabin, Locke).",
         locs=[
             dict(loc="returners", events=[
                 E("item", "Gauntlet OU Genji Glove selon vos réponses à Banon (3 « Non » consécutifs = Genji Glove) – exclusifs", m=True, g=True),
                 E("item", "Pots/seaux : Antidote et Tincture, Green Cherry (objets cachés)", g=True),
             ]),
             dict(loc="lete", boss=["Ultros"], events=[
                 E("boss", "Boss : Ultros (rivière Lete, premier combat)", mon=["Ultros"]),
                 E("learn", "Mog (si présent plus tard) : la danse Water Rondo s'apprend dans un combat en eau (Lete ou Serpent Trench)", g=True, m=True),
             ]),
         ]),
    dict(id="b7", world="B", title="Scénario de Sabin",
         intro="Camp impérial, Forêt fantôme, Train fantôme, Chutes de Baren, Veldt, Mobliz, Mont Crescent, Serpent Trench, Nikeah.",
         locs=[
             dict(loc="camp", events=[E("char", "Cyan rejoint Sabin ; il connaît les SwdTech", g=True)]),
             dict(loc="phantom_forest"),
             dict(loc="phantom_train", boss=["GhostTrain"], events=[
                 E("boss", "Boss : GhostTrain (sensible au feu ; Fenix Down le blesse)", mon=["GhostTrain"]),
                 E("item", "Phantom Train : le wagon-restaurant permet d'acheter des objets (Tent...)", g=True),
             ]),
             dict(loc="baren", events=[E("note", "Sauter dans la rivière avec Cyan et Sabin (Baren Falls) mène au Veldt.", g=True)]),
             dict(loc="mobliz", events=[E("item", "Tintinabar (récompense après le scénario de Sabin à Mobliz)", g=True, item="Tintinabar")]),
             dict(loc="crescent"),
             dict(loc="nikeah"),
             dict(loc="ferry"),
         ]),
    dict(id="b8", world="B", title="Veldt et Gau",
         intro="Gau apparaît sur le Veldt. Lancez-lui de la Dried Meat pour qu'il rejoigne l'équipe (Leap).",
         locs=[
             dict(loc="camp", title="Veldt (carte du monde)", events=[
                 E("char", "Gau : sur le Veldt, donnez-lui de la Dried Meat ; utilisez Leap pour apprendre un Rage", g=True),
                 E("note", "Les Rages s'apprennent en le faisant sauter (Leap) sur un groupe de monstres du Veldt ; voir fiche monstre.", g=True),
             ]),
         ]),
    dict(id="b9", world="B", title="À la recherche de Terra",
         intro="Les trois équipes se retrouvent à Narshe puis partent chercher Terra à travers le monde.",
         locs=[
             dict(loc="narshe_town", title="Narshe (retour)", events=[E("note", "Récupérer l'équipement des personnages ; l'Elder vous donne la Cursed Shld contre Locke (voir quêtes).", g=True)]),
             dict(loc="figaro_wob", title="Château de Figaro (désert)", events=[]),
             dict(loc="kohlingen", events=[
                 E("char", "Locke rencontre Rachel : le Phoenix Cave plus tard donnera Phoenix", g=True),
             ]),
             dict(loc="jidoor", boss=["Chupon"], events=[
                 E("shop", "Maison aux enchères : Esper Golem puis Zoneseek (achetables)", m=True, g=True),
                 E("item", "Relic Ring dans le sous-sol de la demeure d'Owzer (coffre)", g=True),
             ]),
             dict(loc="zozo", boss=["Dadaluma"], events=[
                 E("boss", "Boss : Dadaluma (Zozo, tour)", mon=["Dadaluma"]),
                 E("esper", "Ramuh, puis Siren, Kirin et Stray (scène de Zozo ; trois Magicites d'un coup)", g=True, esper="Ramuh"),
             ]),
             dict(loc="mt_zozo"),
             dict(loc="opera", events=[
                 E("char", "Setzer rejoint après la scène de l'opéra (Draco/Maria)", g=True),
                 E("char", "Celes est là : vous contrôlez le plan de l'opéra (scène optionnelle d'apprentissage)", g=True),
             ]),
             dict(loc="albrook"),
             dict(loc="tzen"),
             dict(loc="maranda"),
             dict(loc="vector", events=[E("note", "Infiltration impériale : coffres de l'usine et du palais.", g=True)]),
             dict(loc="factory", boss=["Ifrit", "Shiva"]),
             dict(loc="magitek_res", boss=["Ifrit", "Shiva"], events=[
                 E("esper", "Ifrit (après le combat Shiva/Ifrit)", m=True, esper="Ifrit"),
                 E("esper", "Shiva (après le combat Shiva/Ifrit)", esper="Shiva"),
             ]),
             dict(loc="castle_vector"),
         ]),
    dict(id="b10", world="B", title="Monde des Espers",
         intro="Strago, Relm, Gogo ; la Porte scellée, Esperville, Thamasa.",
         locs=[
             dict(loc="espervillle", events=[E("esper", "Maduin, Phantom, Unicorn, Bismark, Carbuncle, Shoat : donnés d'un coup après la scène du monde des Espers", g=True, esper="Maduin")]),
             dict(loc="thamasa", events=[
                 E("char", "Strago rejoint (Lores)", g=True),
                 E("char", "Relm rejoint après Ultros dans les Grottes des Espers (Sketch)", g=True),
             ]),
             dict(loc="burning", boss=["Flame Eater"], events=[
                 E("boss", "Boss : FlameEater (Maison en flammes ; ne l'attaquez pas avec du feu)", mon=["FlameEater"]),
                 E("item", "Fire Rod / Ice Rod : coffres de la Maison en flammes", g=True),
             ]),
             dict(loc="esper_caves", boss=["Ultros#302"], events=[
                 E("boss", "Boss : Ultros (3e combat)", mon=["Ultros#302"]),
             ]),
             dict(loc="imperial_base", events=[E("note", "Trésors verrouillés : s'ouvrent plus tard avec Setzer.", g=True)]),
             dict(loc="sealed_gate", boss=["AtmaWeapon"], events=[
                 E("boss", "Atma Weapon (coffre de la grotte : objet Atma Weapon)", mon=["AtmaWeapon"]),
                 E("item", "Genji Glove (coffre, grotte de la Porte scellée)", item="Genji Glove"),
             ]),
         ]),
    dict(id="b11", world="B", title="Château de Doma et Continent flottant",
         intro="Cyan, Shadow et la fin du Monde de la Balance.",
         locs=[
             dict(loc="doma_dream", title="Rêve de Cyan (Doma)", boss=["Wrexsoul"], events=[
                 E("boss", "Boss : Wrexsoul (Soul Savers ; la mod rend les SoulSaver immunisés contre la mort instantanée)", mon=["Wrexsoul", "SoulSaver"]),
                 E("learn", "Cyan apprend Retort, Slash...", g=True),
             ]),
             dict(loc="doma"),
             dict(loc="floating", boss=["Number 024", "Air Force", "Dadaluma"], events=[
                 E("char", "Shadow : attendez le décompte 0:05 sur l'île avant de revenir, sinon il est perdu définitivement", m=True, g=True),
                 E("boss", "Boss : Air Force (puis Kefka)", mon=["Air Force"]),
             ]),
         ]),
    # ------------------------------------------------------------------ MONDE DE LA RUINE
    dict(id="r1", world="R", title="L'île solitaire et premiers pas",
         intro="Celes se réveille seule. Retrouvez la carte puis le groupe.",
         locs=[
             dict(loc="albrook", title="Albrook"),
             dict(loc="collapsing", events=[E("item", "Heal Rod : unique exemplaire pour ceux qui ne l'ont pas pris au Mont Esper", m=True, g=True, item="Heal Rod")]),
             dict(loc="tzen", title="Tzen"),
             dict(loc="mobliz"),
             dict(loc="nikeah", title="Nikeah"),
             dict(loc="south_figaro", title="South Figaro (Ruine)"),
             dict(loc="cave_sf_wor"),
             dict(loc="figaro_wor"),
             dict(loc="kohlingen", title="Kohlingen (Ruine)"),
             dict(loc="darill", boss=["Dullahan"], events=[
                 E("boss", "Boss : Dullahan", mon=["Dullahan"]),
                 E("item", "Genji Helmet, Crystal Mail, Czarina Gown, Exp. Egg, Man Eater : coffres", g=True),
             ]),
         ]),
    dict(id="r2", world="R", title="Retrouver les personnages",
         intro="Dans l'ordre que vous voulez : Cyan, Gau, Relm, Strago, Mog, Umaro, Shadow, Locke, Gogo, Edgar, Sabin, Setzer, Terra.",
         locs=[
             dict(loc="narshe_wor", events=[
                 E("char", "Mog (grotte Moogle) : prenez la Moogle Charm", g=True),
                 E("item", "Salle au trésor de Narshe : Hyper Wrist, Sneak Ring, Wall Ring, ThiefKnife, Earrings, Elixir, 5000 gil", g=True),
             ]),
             dict(loc="umaro_cave", events=[
                 E("char", "Umaro : à battre dans sa grotte (Umaro 14 puis 33)", mon=["Umaro#271"], g=True),
             ]),
             dict(loc="phoenix", events=[
                 E("char", "Locke : Phoenix Cave, trois équipes. Ramassez la Phoenix/Esper Phoenix", g=True),
                 E("esper", "Phoenix (grotte du Phénix)", esper="Phoenix"),
             ]),
             dict(loc="veldt_cave", events=[E("item", "Rage Ring et Striker (grotte du Veldt)", g=True)]),
             dict(loc="zone_eater", boss=["Chupon#303"], events=[E("char", "Gogo : dans la Grotte de Zone Eater (Gogo = Mimic)", g=True)]),
         ]),
    dict(id="r3", world="R", title="Donjons optionnels",
         intro="Tour des Fanatiques, Château antique, grottes. Le coffre « Offering » est perdu si vous ouvrez le coffre-monstre puis fuyez.",
         locs=[
             dict(loc="fanatics"),
             dict(loc="ancient_cave"),
             dict(loc="ancient"),
             dict(loc="hero_cave"),
         ]),
    dict(id="r4", world="R", title="Tour de Kefka",
         intro="Dernier donjon : trois équipes, puis le combat final.",
         locs=[
             dict(loc="kefka", boss=["Kefka#282"], events=[
                 E("boss", "Boss final : Kefka (plusieurs formes), précédé de Goddess/Poltrgeist, Doom... ", mon=["Kefka#282", "Goddess", "Doom"]),
                 E("item", "Ribbon : coffres, et vols sur Atma Weapon et Guardian", g=True),
             ]),
             dict(loc="colosseum", events=[E("note", "Le Colisée permet de miser un objet pour gagner un objet rare (voir Plus > Colisée).", g=True)]),
         ]),
]
