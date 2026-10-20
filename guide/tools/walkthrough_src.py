"""Source écrite à la main du walkthrough (français).

Les COFFRES ne sont pas écrits ici : ils sont lus dans la ROM (extract.py) puis rattachés au PREMIER
chapitre qui cite leur carte. Chaque entrée de chapitre peut donc limiter les cartes avec `maps=[...]`
(sinon : toutes les cartes du lieu). C'est ce qui évite de montrer, dès Narshe, un coffre qui n'est
accessible que bien plus tard.

Recoupement : l'ordre et les récompenses ont été comparés au walkthrough de Caves of Narshe
(cavesofnarshe.com, version GBA : les noms diffèrent un peu) ; `c=True` = confirmé par ce guide,
`g=True` = déduit, non vérifié (ni ROM, ni guide).

Types d'événement (k) : item, esper, char, boss, learn, note, shop.
Drapeaux : m = manquable (exclusif / fenêtre limitée) ; lost="raison" = PERDU À JAMAIS si on ne le
fait pas à ce moment (affiché en rouge, compté et filtrable).
Sur une entrée de chapitre : lost="raison" s'applique à tous les coffres de l'entrée.
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


# id -> (nom, maps de la ROM). Les maps servent aux coffres et aux rencontres aléatoires.
LOC = {
    "narshe_town": ("Narshe (ville)", [20, 104, 105, 106, 107]),
    "narshe_elder": ("Maison de l'Ancien (Narshe)", [30]),
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
    "doma_dream": ("Rêve de Cyan (Doma)", [125, 126, 144, 321, 322]),
    "phantom_forest": ("Forêt fantôme", [132, 133, 134, 135, 140]),
    "phantom_train": ("Train fantôme", [141, 142, 143, 146, 147, 149, 152, 153]),
    "baren": ("Chutes de Baren", [155, 156, 166]),
    "mobliz": ("Mobliz", [150, 154, 157, 158, 159, 160, 161, 162, 163, 164, 165]),
    "crescent": ("Mont Crescent", [167, 168]),
    "trench": ("Serpent Trench", [175]),
    "nikeah": ("Nikeah", [169, 171, 172, 173, 187]),
    "ferry": ("Ferry de Nikeah", []),
    "kohlingen": ("Kohlingen", [188, 189, 191, 194, 195, 197]),
    "owzer_wob": ("Demeure d'Owzer (Jidoor)", [209]),
    "owzer_wor": ("Demeure d'Owzer : les peintures", [207]),
    "jidoor": ("Jidoor", [198, 200, 201, 202, 203, 204, 205, 206, 208]),
    "zozo": ("Zozo", [221, 225, 226]),
    "mt_zozo": ("Mont Zozo", [176, 177, 178, 179, 180, 181]),
    "opera": ("Opéra", [231, 232, 233, 234, 235, 237, 238]),
    "albrook": ("Albrook", [323, 324, 325, 326, 327, 328, 330, 332]),
    "tzen": ("Tzen", [305, 306, 307, 308, 309, 310, 312]),
    "collapsing": ("Maison qui s'effondre (Tzen)", [311]),
    "maranda": ("Maranda", [196, 284, 288, 289, 290]),
    "vector": ("Vector", [240, 242, 243, 244, 245, 246, 247, 248, 249, 251, 252, 253]),
    "castle_vector": ("Palais impérial (Vector)", [250]),
    "factory": ("Centre de recherche Magitek : convoyeurs", [262, 263]),
    "magitek_res": ("Centre de recherche Magitek : laboratoire", [264, 269, 270, 271, 273, 274]),
    "espervillle": ("Esperville", [217, 218, 219]),
    "thamasa": ("Thamasa", [340, 341, 343, 344, 345, 346, 347, 348, 349, 350]),
    "burning": ("Maison en flammes (Thamasa)", [351]),
    "imperial_base": ("Base impériale (poste d'observation)", [377, 378]),
    "sealed_gate": ("Grotte de la Porte scellée", [382, 383, 384, 385, 386, 391]),
    "esper_caves": ("Montagne de Thamasa (Ultros, Relm)", [371, 372, 373, 374, 375]),
    "floating": ("Continent flottant", [393, 394]),
    "hero_cave": ("Grotte du nord-ouest", [185, 186]),
    "darill": ("Tombe de Darill", [297, 298, 299, 300]),
    "phoenix": ("Grotte du Phénix", [313, 314, 315, 316, 318, 317]),
    "veldt_cave": ("Grotte du Veldt", [353]),
    "fanatics": ("Tour des Fanatiques", [359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370]),
    "ancient_cave": ("Grotte du Château antique", [401, 402]),
    "ancient": ("Château antique", [396, 397, 398, 400, 406, 407, 408]),
    "zone_eater": ("Intérieur de la Zone Eater", [276, 277, 278, 279, 280]),
    "kefka": ("Tour de Kefka", [267, 287, 291, 292, 293, 294, 295, 296, 303, 304, 329, 331, 334, 335, 337, 338, 339,
                                 352, 354, 355, 409, 410, 411, 412]),
    "colosseum": ("Colisée", [413]),
}

L_WORLD = "Le Monde de la Balance est détruit après le Continent flottant : aucun retour possible"

CHAPTERS = [
    # ------------------------------------------------------------------ MONDE DE LA BALANCE
    dict(id="b1", world="B", title="Narshe : l'attaque (Terra)",
         intro="Terra, Biggs et Wedge marchent sur Narshe en armures Magitek. Rien à ramasser avant la scène de l'Esper.",
         locs=[
             dict(loc="narshe_mines", title="Mines de Narshe (ouverture)", nochest=True, boss=["Whelk"], events=[
                 E("boss", "Boss : Whelk (coquille + tête). Ne frappez pas la coquille de foudre : elle contre. Visez la tête ; Terra a la commande Magitek.", mon=["Whelk"], c=True),
                 E("note", "Mettez tout le monde en rangée arrière : dégâts physiques reçus divisés par 2 (voir Formules).", c=True),
             ]),
         ]),
    dict(id="b2", world="B", title="Narshe : la fuite (Locke et les Moogles)",
         intro="Terra se réveille chez un vieil homme, puis Locke prend le relais dans les mines avec les Moogles.",
         locs=[
             dict(loc="narshe_town", title="Maison du vieil homme (réveil de Terra)", nochest=True, events=[
                 E("item", "Elixir : examiner l'horloge de la pièce où Terra se réveille (objet caché)", c=True, item="Elixir"),
                 E("item", "Sleeping Bag ×2 : donnés par le vieil homme au réveil", c=True),
             ]),
             dict(loc="narshe_mines", title="Mines de Narshe : tunnels (coffres variables)", maps=[50], boss=["Marshal"], events=[
                 E("learn", "Mog apprend la danse Twilight Requiem (Dusk Requiem) dès le premier combat avec les Moogles.", c=True),
                 E("item", "Mythril Knife : vol commun sur le Chef des gardes (Locke). Volez-le avant de le tuer.", c=True, item="Mythril Knife"),
                 E("boss", "Boss : Marshal / chef des gardes (avec 2 Lobo)", mon=["Marshal"], c=True),
                 E("note", "Les 2 coffres de cette étape CHANGENT plus tard : à gauche Sleeping Bag → Elixir ; à droite Phoenix Down → Guard Bracelet (Monde de la Ruine). "
                           "Laissez le coffre de DROITE fermé si vous voulez le Guard Bracelet.", c=True),
             ]),
         ]),
    dict(id="b3", world="B", title="École d'aventuriers et route de Figaro",
         intro="Narshe vous ferme la porte. L'école d'aventuriers (nord-ouest) contient 3 salles avec butin avant de partir vers Figaro.",
         locs=[
             dict(loc="narshe_town", title="École d'aventuriers", maps=[105, 106, 107], events=[
                 E("note", "Seau de l'école (à examiner) : restaure PV/PM et soigne les statuts, à volonté.", c=True),
                 E("note", "Salle « Environmental Science » (la plus à droite) : un coffre est un monstre (Lobo) ; une marmite contient un Ether.", c=True),
             ]),
         ]),
    dict(id="b4", world="B", title="Château de Figaro",
         intro="Terra et Edgar. Prenez le Mythril Shield de Locke AVANT de parler à Edgar : Locke repart ensuite. Kefka attaque, le château s'enfonce.",
         locs=[
             dict(loc="figaro_wob", lost="Le château s'enfouit dans le sable après le Continent flottant : ces 4 coffres ne se rouvrent pas dans le Monde de la Ruine", events=[
                 E("char", "Edgar rejoint le groupe (Auto Crossbow). Il fait partie du scénario sans choix.", c=True),
                 E("shop", "Boutique d'outils : Noiseblaster et Bio Blaster (pratiques contre les Magitek). Remises si Edgar est chef de groupe.", c=True),
                 E("note", "Prenez les 4 coffres du château maintenant : il disparaîtra du Monde de la Balance (le sous-sol du Monde de la Ruine est un donjon différent).", g=True),
             ]),
         ]),
    dict(id="b5", world="B", title="Grotte de Figaro (première visite)",
         intro="Fuite sous le désert. Les 3 coffres de la grotte sont des coffres à contenu variable : Phoenix Down / Ether maintenant, X-Potion / Thunder Rod avec Locke, Hero Ring dans le Monde de la Ruine. Un seul tirage.",
         locs=[
             dict(loc="cave_sf_wob", maps=[72, 73, 69, 70], events=[
                 E("note", "Conseil : ne touchez à AUCUN de ces coffres maintenant. Chaque coffre se remplit d'un objet unique selon l'avancement : celui que vous ouvrez en premier est le seul que vous recevrez (le plus utile est dans le Monde de la Ruine : Hero Ring).", c=True),
                 E("item", "Vol possible sur Urok : Remedy préférable à Potion.", c=True),
                 E("note", "Ne marchez pas sur la case juste devant la sortie : cela supprime définitivement la scène du « flipping-out » en combat.", c=True),
             ]),
         ]),
    dict(id="b6", world="B", title="South Figaro",
         intro="Magasins, ville et maison du riche. Les contenus des barils changent après le scénario de Locke (l'objet affiché « plus tard » est meilleur).",
         locs=[
             dict(loc="south_figaro", title="South Figaro (visite 1)", maps=[75, 74, 84, 86], events=[
                 E("note", "Plusieurs objets de la ville sont variables (Tonic → X-Potion, Eyedrop → Remedy, Antidote → Tent, Green Cherry → Tent, Gold Needle → Elixir) : ouvrir maintenant = ne pas avoir la version « plus tard ».", c=True),
                 E("note", "Elixir : horloge de la grande maison au nord-ouest (pièce cachée derrière).", c=True),
                 E("shop", "Boutique d'armes : Great Sword (Terra), Mythril Sword (Locke), outils d'Edgar.", c=True),
                 E("shop", "Boutique de reliques : Jeweled Ring (anti-Pierre, indispensable plus tard) et Star Pendants.", c=True),
                 E("note", "Un passage secret mène à un marchand en haut (3e porte : 500/1500/1000 gil et un coffre monstre).", c=True),
             ]),
         ]),
    dict(id="b7", world="B", title="Cabane de Duncan et Mont Kolts",
         intro="Edgar retrouve son frère Sabin. Combat contre Vargas.",
         locs=[
             dict(loc="duncan", events=[E("note", "Potion : seau dans la cabane de départ du chapitre.", c=True)]),
             dict(loc="kolts", boss=["Vargas"], events=[
                 E("char", "Sabin rejoint le groupe en plein combat contre Vargas (+ 2 Ipooh). Terminez avec le Blitz Raging Fist.", mon=["Vargas", "Ipooh"], c=True),
                 E("note", "Pummel (Blitz 1) est déjà connu de Sabin.", c=True),
             ]),
         ]),
    dict(id="b8", world="B", title="Repaire des Returners",
         intro="Banon vous propose de rejoindre les Returners. Le groupe se sépare ensuite en trois scénarios.",
         locs=[
             dict(loc="returners", lost="Repaire des Returners inaccessible dans le Monde de la Ruine (à confirmer)", events=[
                 E("item", "Gauntlet : uniquement si vous ACCEPTEZ immédiatement l'offre de Banon.", c=True, item="Gauntlet", lost="Gauntlet : obtenu seulement en acceptant tout de suite l'offre de Banon (ailleurs vous recevez le Genji Glove)"),
                 E("item", "Genji Glove : refuser l'offre de Banon (1 « Non » = le Returner du dépôt, 3 « Non » = celui qui interrompt la conversation). Exclusif avec le Gauntlet ici ; un autre Genji Glove existe dans la Porte scellée.", c=True, item="Genji Glove"),
                 E("note", "Notez par où vous sortez du repaire : un passage caché dans la chambre de Banon mène à la rivière Lete et plus tard au Veldt.", c=True),
                 E("shop", "Boutique du repaire : premiers Hi-Potions et Eyedrops.", c=True),
             ]),
         ]),
    dict(id="b9", world="B", title="Rivière Lete et scénario de Terra",
         intro="Fuite en radeau puis les trois équipes : Terra (Narshe), Sabin (Mont Kolts → Veldt), Locke (South Figaro). Ordre conseillé : Terra, Sabin, Locke.",
         locs=[
             dict(loc="lete", boss=["Ultros"], events=[
                 E("boss", "Boss : Ultros (premier combat, sur le radeau). Si Banon tombe : Game Over. Terra et Banon en rangée arrière.", mon=["Ultros"], c=True),
                 E("learn", "Mog : Water Harmony ne s'apprend QUE dans l'eau (rivière Lete ou Serpent Trench). Ces deux zones ne sont plus accessibles ensuite.",
                   lost="Water Harmony (danse de Mog) : combattre dans l'eau (Lete ou Serpent Trench) avec Mog dans le groupe. Impossible après le Monde de la Balance", g=True),
             ]),
             dict(loc="narshe_mines", title="Narshe : scénario de Terra (cave des Moogles)", maps=[52], events=[
                 E("note", "Le coffre de la salle des Moogles contient la Rune Edge. Dans le Monde de la Ruine il contiendra un Ribbon : prenez l'un OU l'autre, pas les deux. "
                           "Rune Edge : plus forte que la Great Sword, mais coûte 12–18 PM par coup critique garanti ; beaucoup de joueurs préfèrent laisser le coffre pour le Ribbon.", c=True),
                 E("note", "Contrôle de sécurité : suivez la lumière scintillante, sinon 9 lumières rotatives déclenchent un combat. Ici seulement : Darkside (Rage) ; apparaît à 25 % dans le contrôle.", c=True),
             ]),
         ]),
    dict(id="b10", world="B", title="Scénario de Sabin : camp, forêt, Train fantôme",
         intro="Camp impérial près de Doma (Cyan), Forêt fantôme, Train fantôme. Shadow est recrutable (optionnel).",
         locs=[
             dict(loc="camp", title="Camp impérial (Cyan)", lost="Le camp impérial n'est plus visitable après ce scénario (≈)", events=[
                 E("char", "Cyan rejoint Sabin ; il connaît ses SwdTech (la jauge se remplit 2× plus vite dans le mod).", c=True),
                 E("note", "Star Pendant : coffre de la grande tente → Frapper / « Hit » (déguisement de chat) pour l'ouvrir ; si vous le laissez, rien.", c=True, g=True),
                 E("note", "Green Beret : butin du Satellite (coffre-monstre de la tente à 2 coffres).", c=True),
                 E("item", "Black Belt : butin rare du Capitaine ; pas d'autre pour longtemps.", c=True, lost="Black Belt (butin rare du Capitaine du camp)"),
                 E("char", "Shadow : recrutement optionnel (3 000 gil à Kohlingen plus tard, sinon ici au camp). Il peut partir au hasard avant le Train fantôme.", c=True, g=True),
             ]),
             dict(loc="phantom_forest", events=[E("note", "Source de soin dans la forêt (sortie du haut). Trois combats de fantômes avant le train.", c=True)]),
             dict(loc="phantom_train", boss=["GhostTrain"], lost="On ne peut pas revenir dans le Train fantôme", events=[
                 E("boss", "Boss : Ghost Train (sensible au feu ; les Phoenix Down le blessent). Optionnel : Siegfried (100 PV) → Green Cherry ; Apparition (coffre-monstre) → Hyper Wrist.", mon=["GhostTrain"], c=True),
                 E("note", "Tent caché dans le coin haut-gauche du wagon de la cabine ; Tent à gauche dans le compartiment de Siegfried (vous ne pouvez pas viser la case de droite : Fairy Ring perdu).", c=True),
                 E("note", "Earring : coffre du wagon-restaurant derrière les serveurs.", c=True),
                 E("note", "Wagon suivant : 4 coffres (Phoenix Down, Sniper Eye, Phoenix Down, coffre-monstre M-TekArmor). Le Train n'a plus de retour.", c=True),
             ]),
         ]),
    dict(id="b11", world="B", title="Scénario de Sabin : Baren, Veldt, Mobliz, Crescent, Trench",
         intro="Sabin et Cyan sautent dans les chutes de Baren, rencontrent Gau au Veldt, traversent Mobliz et le Serpent Trench jusqu'à Nikeah.",
         locs=[
             dict(loc="baren", events=[
                 E("note", "Shadow quitte le groupe aux chutes. Avant : déséquipez ses objets, reliques et Esper (Ninja Gear et Hermes Sandals à Sabin, Gigas Glove à Cyan).", c=True),
                 E("boss", "Boss : Rhizopas (60 s après les Opinicus). Butin commun : Remedy.", c=True),
             ]),
             dict(loc="mobliz", events=[
                 E("char", "Gau : sur le Veldt, jetez-lui de la Dried Meat (acheter à Mobliz). Sabin et Cyan doivent être vivants pour la scène.", c=True),
                 E("note", "Elixir : horloge de la maison du pigeon voyageur.", c=True),
                 E("item", "Tintinnabulum : récompense du soldat blessé après l'envoi des 5 colis.", c=True, item="Tintinnabulum", g=True),
                 E("shop", "Boutique de Mobliz : Dried Meat (au moins 1), Kotetsu pour Cyan. Gardez 2 500 gil.", c=True),
             ]),
             dict(loc="crescent", events=[
                 E("note", "La scène de Gau vous prend 500 gil si vous les avez (sinon Cyan les garde).", c=True),
                 E("item", "Potion : petite case à gauche (là où Gau la trouve).", c=True),
             ]),
             dict(loc="trench", lost="Le Serpent Trench n'est plus accessible après ce chapitre : prenez les deux coffres (embranchements de DROITE)", events=[
                 E("note", "Prenez les embranchements de droite : X-Potion (1ère fourche), Green Beret (2e fourche, case marquée pour vider l'eau).", c=True),
             ]),
             dict(loc="nikeah", events=[E("note", "Elixir : horloge de l'auberge de Nikeah.", c=True)]),
         ]),
    dict(id="b12", world="B", title="Scénario de Locke : South Figaro",
         intro="Locke infiltre South Figaro et suit un passage secret (mot de passe : « Courage »).",
         locs=[
             dict(loc="south_figaro", title="South Figaro (scénario de Locke)", maps=[87, 89], events=[
                 E("note", "Marchand / officier : volez leurs vêtements (Plumed Hat, Main Gauche) pour continuer. Donnez le Cider au vieux domestique pour révéler le passage secret.", c=True),
                 E("char", "Celes est libérée : elle rejoint le groupe (Runic, magie). Premier objet : Clock Key.", c=True),
             ]),
             dict(loc="cave_sf_wob", title="Grotte de Figaro (scénario de Locke)", maps=[69, 70], boss=["TunnelArmr"], events=[
                 E("note", "Contenu du coffre du haut maintenant : Thunder Rod (se brise) ; plus tard, Hero's Ring (Monde de la Ruine). Mieux vaut laisser fermé.", c=True),
                 E("boss", "Boss : Tunnel Armor (1 300 PV). Volez Air Knife (rare) avec Locke.", c=True),
             ]),
         ]),
    dict(id="b13", world="B", title="Retrouvailles à Narshe",
         intro="Les équipes se rejoignent à Narshe pour défendre l'Esper. Combat contre Hell's Rider puis Kefka. Après : repos et préparatifs.",
         locs=[
             dict(loc="narshe_mines", title="Narshe : défense de l'Esper", nochest=True, boss=["Kefka#298"], events=[
                 E("boss", "Boss : Hell's Rider (niv. 14) puis Kefka (niv. 18, 3 000 PV, vulnérable à Stop). Si l'équipe est battue, retour au Save point à 1 PV pour revoler.", c=True),
                 E("item", "Peace Ring : butin de Kefka (peu utile).", c=True),
             ]),
             dict(loc="narshe_elder", title="Narshe : maison de l'Ancien (salle au trésor)", events=[
                 E("note", "Elixir : horloge de la maison de l'Ancien.", c=True),
                 E("note", "Salle au trésor (cabane de l'est) : Hyper Wrist, Sneak Ring, Wall Ring, ThiefKnife, Earrings, Elixir, 5 000 gil.", c=True),
             ]),
             dict(loc="narshe_town", title="Narshe (reste de la ville)", maps=[20], events=[
                 E("note", "Le coffre de Sprint Shoes de Narshe n'est accessible qu'une fois la ville ouverte (après la défense de l'Esper).", g=True),
                 E("shop", "Boutique d'armes : Moonring Blade pour Locke ; boutique d'armures : Mythril Shield pour tous.", c=True),
             ]),
         ]),
    dict(id="b14", world="B", title="Kohlingen, Jidoor et Zozo",
         intro="Vous retrouvez Rachel à Kohlingen (Locke), puis la tour de Zozo où Terra est retenue.",
         locs=[
             dict(loc="kohlingen", events=[
                 E("note", "Elixir : horloge de la maison de Rachel.", c=True),
                 E("note", "Green Beret : coffre de la grande maison du nord-est (entrée arrière).", c=True),
                 E("char", "Shadow : 3 000 gil à l'auberge de Kohlingen. Il quitte le groupe au hasard ensuite ; avant le Continent flottant il faut décider de l'emmener (voir Continent flottant).", c=True),
                 E("shop", "Fuma/Flame Scrolls (Shadow) à la boutique d'armes.", c=True),
             ]),
             dict(loc="owzer_wob", events=[E("note", "Ether : l'un des seaux de la demeure d'Owzer.", c=True)]),
             dict(loc="zozo", boss=["Dadaluma"], events=[
                 E("note", "Chainsaw : coffre derrière un mur qui s'ouvre quand l'horloge est réglée sur 6 h 10 min 50 s.", c=True),
                 E("note", "Ether (tour du haut), Hi-Potion et Ether (marmites de l'escalier tournant), Burning Fist (petite pièce), Brigand's Glove (High Tower).", c=True),
                 E("note", "Hermes Sandals et X-Potion : 2 coffres de la salle de Dadaluma.", c=True),
                 E("boss", "Boss : Dadaluma (Zozo, niv. 22). Vol commun Thief's Knife, rare Thief's Bracer.", mon=["Dadaluma"], c=True),
                 E("esper", "Ramuh : Magicite trouvée à Zozo (récupérée après l'épisode avec Terra).", c=True, esper="Ramuh"),
             ]),
         ]),
    dict(id="b15", world="B", title="Opéra, Albrook, Tzen, Maranda et Vector",
         intro="Opéra d'Ultros contre Setzer, puis l'infiltration de Vector.",
         locs=[
             dict(loc="jidoor", events=[
                 E("shop", "Maison aux enchères : Golem et Zone Seeker (Espers achetables), Angel Wings, Angel Ring — tirage aléatoire.", c=True),
             ]),
             dict(loc="opera", boss=["Ultros#301"], events=[
                 E("char", "Setzer rejoint après l'opéra (plan du ballon). L'opéra a des échecs limités : 3 essais puis Game Over.", c=True),
                 E("boss", "Boss : Ultros (4e position, 2 550 PV chacune). Utilisez Ramuh et des Earrings.", mon=["Ultros#301"], c=True),
             ]),
             dict(loc="albrook", events=[
                 E("note", "Elixir : horloge entre la boutique d'armures et le café.", c=True),
                 E("note", "Hi-Potion : baril près de l'auberge ; Ether : marmite de la boutique d'armes ; Teleport Stone : caisse du port.", c=True),
                 E("shop", "Reflect Ring ×4 (boss), Earrings, Hero's Ring (1–2), Venom Claws pour Sabin.", c=True),
             ]),
             dict(loc="tzen", events=[
                 E("esper", "Seraph : à acheter à un escroc de Tzen (3 000 gil) ; plus tard seulement 10 gil dans le Monde de la Ruine.", c=True),
             ]),
             dict(loc="maranda", events=[
                 E("note", "Holy Water (caisse du bas, ouest de la sortie sud) et Remedy (l'une des 2 caisses près du couple) : gratuits.", c=True),
                 E("note", "Dialogue de Lola : dépend du colis de Mobliz. Pigeon voyageur : lisez-le avant de partir.", c=True),
             ]),
             dict(loc="vector", maps=[252], events=[
                 E("shop", "Boutique d'armes : Sakura (dague de vent). Achetez-la maintenant si vous la voulez.", c=True),
                 E("note", "Gardien : indestructible. Fuyez ou confondez un membre qui utilise la Smoke Bomb.", c=True),
             ]),
         ]),
    dict(id="b16", world="B", title="Centre de recherche Magitek",
         intro="Descente dans la fosse puis le laboratoire. Après Number 128, on ne revient plus. Ramassez TOUT avant de partir.",
         locs=[
             dict(loc="factory", lost="Centre de recherche Magitek inaccessible ensuite : tout coffre non ouvert est perdu", events=[
                 E("note", "Convoyeurs : Flametongue (à gauche par la conduite), Ether, X-Potion, Thunder Blade, Remedy, Dragoon Boots (relique), Golden Shield, Golden Helm, Golden Armor, Tent.", c=True),
                 E("note", "Icebrand et Zephyr Cloak : pièce cachée parmi les caisses impériales, sous la 5e caisse (face à la première caisse : 5 pas en bas, droite, 1 pas en arrière).", c=True),
             ]),
             dict(loc="magitek_res", boss=["Ifrit", "Shiva"], lost="Centre de recherche inaccessible ensuite", events=[
                 E("boss", "Boss : Number 024 (salle des Espers), puis Ifrit (3 300 PV) et Shiva (3 000 PV).", mon=["Ifrit", "Shiva"], c=True),
                 E("esper", "Ifrit : Magicite après le combat contre Ifrit/Shiva. Prenez les deux.", m=True, esper="Ifrit", lost="Ifrit et Shiva : les Magicites sont perdues si vous quittez la salle sans les récupérer", c=True),
                 E("esper", "Shiva : Magicite après le combat.", esper="Shiva", lost="Ifrit et Shiva (voir ci-dessus)", c=True),
                 E("note", "Stoneblade : coffre caché à gauche du tube en bas à gauche de la salle des tubes (sort : Break).", c=True),
                 E("boss", "Boss : Number 128 (3 276 PV) + lames. Après le combat : 6 Espers (Bismarck, Maduin, Unicorn, Catoblepas, Phantom, Carbuncle).", c=True),
                 E("note", "Number 128 : vol rare Kazekiri (aussi butin commun) ; un autre Kazekiri est dans la Porte scellée.", c=True),
             ]),
         ]),
    dict(id="b17", world="B", title="Narshe : alliance, Mog et la Porte scellée",
         intro="Les Espers de Vector, le flash-back de Terra, puis la défense de Narshe et la caverne de la Porte scellée.",
         locs=[
             dict(loc="narshe_town", title="Narshe (Mog, boutiques)", nochest=True, events=[
                 E("char", "Mog : en défendant le Moogle contre Lone Wolf. Si vous poursuivez le trésor (Gold Hairpin), Mog est PERDU.", c=True, lost="Mog : sauvez le Moogle (ne poursuivez pas Lone Wolf pour le Gold Hairpin)"),
                 E("learn", "Danses de Mog déjà apprises à ce stade : Wind Rhapsody (plaines près de Narshe), Forest Nocturne, Desert Lullaby, Earth Blues (pentes du Mont Kolts), Twilight Requiem, Love Serenade (Zozo).", c=True),
                 E("shop", "Boutiques de Narshe : Hawkeye pour Locke, Tiara pour Terra, Golden Shield/Helm.", c=True),
             ]),
             dict(loc="sealed_gate", lost=L_WORLD, boss=["AtmaWeapon"], events=[
                 E("note", "Coffres : Assassin's Dagger, Kazekiri, X-Potion, Hi-Ether, Genji Glove (à gauche, après le puzzle), Elixir, Hi-Ether… et la petite grotte derrière la case de pas : 2 Magicite Shard, Hi-Ether, Ultima Weapon.", c=True),
                 E("boss", "Boss : Atma Weapon (vol possible). Ninja optionnel (faible à la foudre).", mon=["AtmaWeapon"], c=True),
                 E("boss", "Kefka (déclenche la Porte scellée). Ensuite Esper Valigarmanda/Midgardsormr (Narshe Ruine).", c=True),
             ]),
         ]),
    dict(id="b18", world="B", title="Palais impérial (banquet de Gestahl)",
         intro="Après la Porte scellée, Gestahl organise un banquet : votre score (max 93) décide de vos récompenses.",
         locs=[
             dict(loc="castle_vector", lost=L_WORLD + " (≈)", events=[
                 E("note", "Score de banquet : 50+ = Doma libéré ; 67+ = la maison du poste d'observation s'ouvre ; 77+ = Tintinnabulum (Gestahl) ; 90+ = Ward Bangle (Élite impériale).", c=True,
                   lost="Récompenses de score du banquet (≥ 50, 67, 77, 90) : la porte du poste d'observation, Tintinnabulum, Ward Bangle"),
                 E("note", "Dans le palais après le banquet : Alarm Earring, Gale Hairpin, Holy Water, X-Potion, Ether.", c=True),
             ]),
             dict(loc="imperial_base", lost=L_WORLD + " (≈)", events=[
                 E("note", "Maison du poste d'observation (si score ≥ 67) : X-Potion, Angel Wings…, 41 000 gil au total (8 000 + 13 000 + 20 000), Elixir caché au sud, Flametongue dans le poêle.", c=True),
             ]),
         ]),
    dict(id="b19", world="B", title="Thamasa et les Espers",
         intro="Cyan, Strago, Relm : le Mont Esper derrière Thamasa, la maison en flammes puis l'attaque de Kefka.",
         locs=[
             dict(loc="thamasa", events=[
                 E("char", "Strago rejoint (Lores) après la maison en flammes. Il apprend un Lore quand il voit un ennemi le lancer.", c=True),
                 E("note", "Barils (Echo Screen, Green Cherry, Gold Needle, Eyedrop, Phoenix Down), Memento Ring : chambre de Strago à l'étage.", c=True),
                 E("note", "Si vous n'avez pas déséquipé Shadow avant sa sieste, il emporte ses objets en partant.", c=True),
             ]),
             dict(loc="burning", boss=["FlameEater"], lost="La maison en flammes disparaît après l'incendie", events=[
                 E("boss", "Boss : Flame Eater (maison en flammes ; évitez le feu).", mon=["FlameEater"], c=True),
                 E("note", "Fire Rod (3e salle, porte de droite) et Ice Rod (3e salle, porte de gauche, salle suivante, porte de droite).", c=True),
                 E("learn", "Lore : Self-Destruct, en confondant les Balloons.", c=True),
             ]),
             dict(loc="esper_caves", boss=["Ultros#302"], lost="La montagne n'est plus accessible une fois Relm recrutée (≈)", events=[
                 E("boss", "Boss : Ultros (3e combat, 22 000 PV). Relm rejoint quand ses PV tombent à ~10 240 ; « Sketch » le fait fuir.", mon=["Ultros#302"], c=True),
                 E("note", "Healing Rod (1ère salle), Chocobo Suit et Tabby Suit (labyrinthe de ponts cassés, via la case d'effondrement du haut), X-Potion (case lâche tout à droite).", c=True),
                 E("learn", "Lore : White Wind, quand Venobennu l'utilise devant Strago.", c=True),
             ]),
             dict(loc="espervillle", events=[
                 E("note", "Après l'attaque de Kefka, les Espers sont tués (Magicites). Interceptor est abandonné à Thamasa.", c=True),
             ]),
         ]),
    dict(id="b20", world="B", title="Veldt, Rages et Lores avant la fin",
         intro="C'est la dernière occasion avant la bascule : Rages et Lores hors du Monde de la Ruine. Doma, Esper Gau.",
         locs=[
             dict(loc="doma", maps=[], title="Veldt et Lores (derniers préparatifs)", nochest=True, events=[
                 E("note", "Aucune danse, Rage ou Lore n'est perdue pour toujours ici, sauf Water Harmony (déjà traitée). Beaucoup d'ennemis ne se rencontrent que dans le Monde de la Balance : Rage de Grenade, Gaia Gear (vol sur Briareus, rare), Magic Urn…", c=True, g=True),
                 E("learn", "Lores à apprendre maintenant avec Strago : Doom, Dischord, Lv.3 Confuse, Lv.4 Flare, Lv.5 Death, Transfusion, Roulette, Traveler (confondre un Unseelie hors de South Figaro).", c=True),
             ]),
         ]),
    dict(id="b21", world="B", title="Continent flottant",
         intro="Dernier donjon du Monde de la Balance. Il n'y a PAS de retour : le continent s'effondre. Emmenez Shadow si vous le voulez, sinon il reste.",
         locs=[
             dict(loc="floating", lost=L_WORLD, boss=["Number 024", "Air Force", "Dadaluma"], events=[
                 E("char", "Shadow (optionnel) : pour qu'il survive, attendez le compte à rebours à 0:05 sur l'île avant de revenir. Sauter trop tôt = Shadow perdu définitivement.", c=True,
                   lost="Shadow : dans l'évasion, attendez 0:05 avant de sauter (6:00 au total), sinon il est perdu"),
                 E("note", "Murasame : orbe bleu à l'est de l'entrée. Beret : orbe bleu sous le Save point (Relm). Elixir : petit plateau avec orbe (fissures au sol).", c=True),
                 E("boss", "Boss : Air Force (puis Ultima Weapon 24 000 PV, Kefka et Gestahl). Vol sur Ultima Weapon : Ribbon (commun), Elixir (rare).", mon=["Air Force"], c=True),
                 E("note", "Dernière chance : Genji Glove (vol rare sur le Dragon, avec Thief's Knife), Earring/Angel Ring (vols), Rages et Lores propres au Monde de la Balance.", c=True, g=True),
             ]),
         ]),
    # ------------------------------------------------------------------ MONDE DE LA RUINE
    dict(id="r1", world="R", title="Île solitaire et premiers pas",
         intro="Celes se réveille seule avec Cid. Nourrissez-le avec des poissons : sa santé (cachée) décide de sa survie, et sa mort est définitive.",
         locs=[
             dict(loc="albrook", title="Île solitaire et Albrook", maps=[], nochest=True, events=[
                 E("note", "Cid : donnez-lui des poissons (Poisson +16, Yummy +32, Rotten −4, Slow −16). À 256 il est guéri pour de bon ; en dessous de 30 il meurt (définitif, et ça change les dialogues de Celes).", c=True),
                 E("note", "Équipez Celes d'un Amulet ou Ribbon contre Bone Powder (Zombie = Game Over).", c=True),
                 E("esper", "Quetzalli : Magicite rejetée sur la plage de l'île solitaire.", c=True),
                 E("note", "Albrook, Tzen, Mobliz, Nikeah, South Figaro, Kohlingen : mêmes coffres que dans le Monde de la Balance (rien de plus s'ils ont déjà été pris).", c=True),
             ]),
             dict(loc="tzen", title="Tzen et la maison qui s'effondre", events=[
                 E("char", "Sabin : sauvez l'enfant avant l'écroulement (6:00). Boutique : Jeweled Ring (dernière chance), Venom Claws.", c=True),
                 E("esper", "Seraph : 10 gil seulement ici si vous ne l'avez pas acheté avant.", c=True),
             ]),
             dict(loc="collapsing", events=[E("note", "Healing Rod (au bout du couloir) — ne le ratez pas ; Holy Rod, Ether, Magicite, Blood Sword (optionnel).", c=True)]),
         ]),
    dict(id="r2", world="R", title="Mobliz, Nikeah, South Figaro, Figaro enfoui",
         intro="Le trio : Terra (Mobliz), puis la quête des Crimson Robbers (Edgar déguisé en Gerad).",
         locs=[
             dict(loc="mobliz", title="Mobliz : Terra et les enfants", events=[
                 E("esper", "Fenrir : donné par l'enfant de l'entrée après le départ de Humbaba.", c=True),
                 E("note", "Terra ne rejoint pas encore : revenez après avoir vaincu Humbaba (Narshe).", c=True),
             ]),
             dict(loc="nikeah", title="Nikeah (Ruine)", events=[E("shop", "Enhancers ×3 (+7 magie), Diamond Vest, Gale Hairpin.", c=True)]),
             dict(loc="south_figaro", title="South Figaro (Ruine)", maps=[], nochest=True, events=[
                 E("shop", "Golden Spear, Diamond Armor, Amulets (suffisamment pour 4), Hermes Sandals.", c=True),
                 E("note", "Gerad (Edgar) quitte l'auberge avec les Crimson Robbers : suivez-le.", c=True),
             ]),
             dict(loc="cave_sf_wor", events=[
                 E("note", "Ne rien ouvrir avant ? Hi-Ether, X-Potion, Hero's Ring (les coffres de la grotte ne se remplissent qu'une fois : si vous les avez déjà pris dans le Monde de la Balance, ce sont les anciens objets).", c=True),
             ]),
             dict(loc="figaro_wor", boss=["Tentacle"], events=[
                 E("note", "Coffres du château enfoui : Crystal Helm, Gravity Rod, X-Potion, Hi-Ether (salle à 4 coffres) ; Royal Crown (porte de gauche) ; Soul Sabre (armure du milieu de la salle au trésor).", c=True),
                 E("boss", "Boss : 4 Tentacles (Grab). Vous pouvez laisser partir les Robbers.", c=True),
             ]),
         ]),
    dict(id="r3", world="R", title="Kohlingen, Tombe de Darill, Setzer",
         intro="Setzer se noie dans l'alcool à Kohlingen. Sa tombe de Darill renferme de l'équipement fort.",
         locs=[
             dict(loc="kohlingen", title="Kohlingen (Ruine)", maps=[], nochest=True, events=[
                 E("char", "Setzer : au bar de Kohlingen ; Celes le ramène à lui. Achetez Gambler Dice (5 000 gil) et Viper Darts (Colisée).", c=True),
             ]),
             dict(loc="darill", boss=["Dullahan"], events=[
                 E("note", "Genji Helmet (chemin bas-droite), Crystal Mail (salle bas-gauche), Czarina Gown (Relm), Man Eater (salle après la 2e tortue), Exp. Egg caché derrière la sculpture de la tombe.", c=True),
                 E("boss", "Boss : Dullahan. Coffre-monstre Angler Whelk : tuez tête ET coquille ensemble pour 2 Dragon Claws.", c=True,
                   lost="Dragon Claws : seule source = Angler Whelk, la tête et la coquille doivent mourir ensemble"),
                 E("esper", "Bahamut : butin de Deathgaze (rencontre aérienne aléatoire).", c=True),
             ]),
             dict(loc="maranda", title="Maranda (Ruine)", maps=[], nochest=True, events=[
                 E("shop", "Crystal Shield/Mail (×2), Black Garb (Sabin).", c=True),
             ]),
         ]),
    dict(id="r4", world="R", title="Narshe : Mog, Umaro, Valigarmanda",
         intro="Narshe revisité : la mine, les Moogles, la neige, Umaro.",
         locs=[
             dict(loc="narshe_wor", maps=[38, 44], events=[
                 E("char", "Mog : dans la grotte Moogle (mur que Mog fixe) ; vous obtenez Molulu's Charm (évite les combats). Avec 4 persos, Mog attend sur le Falcon.", c=True),
                 E("note", "Ribbon : seulement si la Rune Edge est restée dans le coffre. Elixir et Guard Bracelet : seulement si les coffres de la mine sont intacts.", c=True),
                 E("note", "Boutique d'armes : verrouillée, nécessite Locke (il crochète la porte).", c=True),
                 E("esper", "Valigarmanda : champs de neige ; Force Shield du Dragon de glace.", c=True),
                 E("learn", "Mog : Snowman Rondo (dernière danse).", c=True),
             ]),
             dict(loc="umaro_cave", boss=["Umaro#272"], events=[
                 E("char", "Umaro : Mog doit lui parler. Sans Mog, il ne rejoint pas (vous pouvez revenir).", c=True),
                 E("esper", "Midgardsormr : os sculpté de la salle du Sasquatch (déclenche le Yeti).", c=True),
                 E("note", "Gauntlet : coffre du bas après la salle du haut ; Hi-Ether : coffre haut ; X-Ether.", c=True),
             ]),
         ]),
    dict(id="r5", world="R", title="Mobliz : Humbaba et Terra",
         intro="Humbaba (2) supprime 2 persos du groupe ; Terra se transforme définitivement.",
         locs=[
             dict(loc="mobliz", title="Mobliz (Terra et Humbaba)", maps=[], nochest=True, events=[
                 E("char", "Terra : après le deuxième combat contre Humbaba (60 000 PV). Elle a gagné Morph permanent.", c=True),
                 E("note", "Humbaba Breath retire 2 persos du groupe : vous les retrouvez dans le Falcon.", c=True),
             ]),
         ]),
    dict(id="r6", world="R", title="Zozo, Mont Zozo, Cyan",
         intro="Le pigeon, le Mont Zozo et le Dragon Tempête.",
         locs=[
             dict(loc="mt_zozo", maps=[177, 179], boss=["Storm Drgn"], events=[
                 E("note", "Ice Shield, Red Cap (+25 % PV), Thunder Shield, Aegis Shield (coffres de la grotte), Gold Hairpin (ouverture de gauche à l'extérieur).", c=True),
                 E("boss", "Boss : Storm Dragon (42 000 PV, faible à la foudre). Le coffre piégé libère le dragon.", c=True),
                 E("char", "Cyan : seulement avec 3 persos au combat ; sinon il attend dans le Falcon. Machinery Manual / Book of Secrets : coffre de Cyan.", c=True),
             ]),
             dict(loc="zozo", title="Zozo (Ruine)", maps=[], nochest=True, events=[
                 E("note", "Rust-Rid (1 000 gil) : en vente seulement si le pigeon a été envoyé à Zozo.", c=True),
             ]),
         ]),
    dict(id="r7", world="R", title="Veldt, Gau, Shadow, Relm",
         intro="Gau se recrute dans les combats du Veldt. La grotte du Veldt cache Relm (ou Shadow).",
         locs=[
             dict(loc="veldt_cave", boss=["SrBehemoth#281"], events=[
                 E("char", "Gau : combats du Veldt avec une place libre (≈57 % de chance de rencontre).", c=True),
                 E("char", "Shadow : sauvé ici seulement si vous l'aviez attendu sur le Continent flottant ; sinon Relm.", c=True),
                 E("note", "Berserker Ring (salle des 4 chasseurs), Ichigeki (salle d'interrupteur), Tigerfang (après Death Warden).", c=True),
             ]),
             dict(loc="owzer_wor", boss=["Chadarnook"], events=[
                 E("esper", "Lakshmi : butin de Chadarnook. Relm rejoint après.", c=True),
                 E("note", "Moogle Suit (porte gauche de la 1ère salle), Lich Ring (caché derrière les 3 portes). Seule la porte de GAUCHE continue le donjon.", c=True),
             ]),
             dict(loc="thamasa", title="Thamasa (Ruine)", maps=[], nochest=True, events=[
                 E("char", "Strago : jouez avec Relm dans le groupe. Interceptor est perdu si un monstre lui prend Dog Block.", c=True),
             ]),
         ]),
    dict(id="r8", world="R", title="Rêve de Cyan (Doma)",
         intro="Le Rêve de Cyan est accessible seulement ici. Prenez tout avant de finir.",
         locs=[
             dict(loc="doma", boss=["Curley"], events=[
                 E("note", "Elixir et Hi-Ether (horloge de la chambre), X-Potion, Phoenix Down, Prayer Beads (petite pièce sur le mur extérieur).", c=True),
             ]),
             dict(loc="doma_dream", boss=["Wrexsoul"], lost="Le Rêve de Cyan ne se refait pas : tout non pris est perdu", events=[
                 E("esper", "Alexander : Magicite dans la salle du trône.", c=True),
                 E("boss", "Boss : Wrexsoul (+ 2 Soul Savers). N'utilisez PAS Banish : sans lui avoir fait de dégâts vous perdez le Guard Bracelet.", mon=["Wrexsoul", "SoulSaver"], c=True),
                 E("learn", "Cyan apprend toutes les SwdTech restantes (Tempest, Oblivion).", c=True),
                 E("note", "Genji Glove (1er wagon), Flame Shield (2e wagon, il faut Lump of Metal), Ice Shield et X-Potion (labyrinthe de wagons), Masamune après Wrexsoul.", c=True),
                 E("note", "Ennemis uniques au rêve (Weredragon, Alluring Rider, Pandora, Parasite, Coco) : pour la liste de Rages et Lores (Holy, Doom, Roulette).", c=True,
                   lost="Rages/Lores du Rêve de Cyan : à encontrer avant de finir"),
             ]),
         ]),
    dict(id="r9", world="R", title="Château antique et Grotte du Phénix",
         intro="Deux donjons optionnels majeurs.",
         locs=[
             dict(loc="ancient_cave", events=[
                 E("note", "Wing Edge (salle d'entrée gauche), Hi-Ether (droite), Death Tarot (grotte du Master Tonberry), X-Potion et Magicite Shard (grotte de gauche).", c=True),
                 E("boss", "Master Tonberry (coffre-monstre, 22 000 PV). Dormez-le, magie seulement.", c=True),
             ]),
             dict(loc="ancient", boss=["Blue Drgn"], events=[
                 E("esper", "Odin : statue de la salle du trône ; Raiden : reine pétrifiée (il faut Odin).", c=True),
                 E("note", "Rod Punisher (droite), Master's Scroll (gauche, gardé par Samurai Soul : ne fuyez pas), Blizzard Orb et Gold Hairpin (salle droite), X-Ether (seau de la chambre de la reine).", c=True,
                   lost="Master's Scroll : si vous fuyez Samurai Soul vous ne pourrez plus l'affronter"),
                 E("boss", "Boss : Blue Dragon (dans le hall souterrain) → Zantetsuken.", c=True),
             ]),
             dict(loc="phoenix", boss=["Red Dragon"], events=[
                 E("char", "Locke : trois équipes dans la grotte du Phénix.", c=True),
                 E("esper", "Phoenix : coffre de Locke.", esper="Phoenix", c=True),
                 E("note", "Wing Edge (pont ou chute : 400 dégâts), Ribbon (lave solidifiée), Dragon Horn (gardé par le Red Dragon).", c=True),
             ]),
         ]),
    dict(id="r10", world="R", title="Zone Eater (Gogo) et autres",
         intro="Gogo est le dernier personnage.",
         locs=[
             dict(loc="zone_eater", events=[
                 E("char", "Gogo : le dernier personnage à recruter (dans la Zone Eater).", c=True),
                 E("note", "Genji Armor (côté droit), Magical Brush (gauche), Fake Mustache (extrême gauche), Zephyr Cloak, Hero's Ring (entre deux chutes), Pinwheel (chute du plafond), Thunder Shield, Hi-Ether, Red Jacket.", c=True),
             ]),
             dict(loc="fanatics", events=[
                 E("note", "Safety Bit, Air Anchor (coffre caché à droite), Genji Shield, Kagenui, Force Armor, Soul of Thamasa (toit : Magic Master, Ultima à sa mort).", c=True),
                 E("note", "Tour des Fanatiques : seuls Magic Urn (Rage utile) et Holy Dragon (Holy Lance) sont à ne pas rater.", c=True),
             ]),
             dict(loc="hero_cave", events=[E("note", "Grotte du nord-ouest : Hero Ring.", g=True)]),
         ]),
    dict(id="r11", world="R", title="Tour de Kefka et Colisée",
         intro="Trois équipes, un seul chemin. Dernière chance pour tout : Rages, Lores, objets.",
         locs=[
             dict(loc="kefka", boss=["Kefka#282"], events=[
                 E("note", "Hypno Crown, Fixed Dice, Minerva Bustier, Pinwheel, Force Shield, Force Armor, Ribbon (plusieurs), Red Cap, Gauntlet, Nutkin Suit, Hero's Ring, Aegis Shield (caché, parcours en 11 pas), Megalixir, Rainbow Brush.", c=True),
                 E("esper", "Crusader : après le Skull Dragon (Dragon Seal).", c=True),
                 E("boss", "Boss : Guardian (cycle de 4 programmes), les 3 Statues (Demon, Fiend, Goddess) puis Kefka. Fiend : Force Field s'apprend seulement ici.", c=True,
                   lost="Force Field (Lore) : seulement contre Fiend dans la Tour de Kefka"),
             ]),
             dict(loc="colosseum", events=[E("note", "Le Colisée permet de miser un objet pour gagner un objet rare (voir Plus > Colisée).", c=True)]),
         ]),
]


# Indices de position des coffres (carte, x, y) -> texte. Source : Caves of Narshe ; recoupés avec les objets lus dans la ROM.
CHEST_HINT = {
    (30, 55, 30): "Examiner l'horloge de la maison de l'Ancien",
    (86, 7, 31): "Horloge de la grande maison du nord-ouest (pièce cachée derrière)",
    (94, 74, 27): "Seau dans la cabane de départ",
    (171, 57, 37): "Horloge de l'auberge",
    (163, 51, 12): "Horloge de la maison du pigeon voyageur",
    (330, 35, 7): "Horloge du couloir entre la boutique d'armures et le café",
    (197, 42, 10): "Horloge de la maison de Rachel",
    (195, 37, 53): "Coffre à peine visible de la grande maison nord-est : entrée arrière",
    (209, 125, 11): "Dans l'un des seaux de la demeure d'Owzer",
    (225, 111, 52): "Derrière un mur qui s'ouvre quand l'horloge indique 6:10:50",
    (225, 35, 11): "Petite pièce derrière la porte évidente",
    (226, 72, 26): "Salle de Dadaluma, coffre latéral",
    (226, 92, 27): "Salle de Dadaluma, coffre latéral",
    (271, 8, 37): "Caché à gauche du tube en bas à gauche de la salle des tubes",
    (263, 55, 34): "Pièce cachée sous la 5e caisse impériale (5 pas en bas depuis la 1re caisse, à droite, 1 pas en arrière)",
    (263, 60, 33): "Même pièce cachée sous les caisses",
    (117, 45, 5): "Grande tente : frapper / « Hit » le coffre (sinon rien)",
    (117, 19, 18): "Tente à 2 coffres, coffre de droite",
    (117, 17, 18): "Tente à 2 coffres, coffre de gauche = monstre (Satellite)",
    (117, 15, 8): "Tente derrière la tente à 2 coffres",
    (147, 5, 5): "Wagon-restaurant, derrière les serveurs",
    (146, 20, 7): "Wagon de la cabine, coin haut-gauche (caché)",
    (153, 20, 7): "Compartiment de Siegfried, case vide à gauche",
    (153, 21, 7): "Case de droite : on ne peut pas se placer en face, donc inaccessible",
    (100, 30, 33): "Pièce cachée à droite du chemin/escalier",
    (110, 60, 19): "Passage caché à droite des 3 coffres extérieurs",
    (110, 43, 11): "L'un des 3 coffres extérieurs (Knight's Code)",
    (110, 43, 13): "L'un des 3 coffres extérieurs",
    (110, 45, 13): "L'un des 3 coffres extérieurs (Air Knife/Lancet)",
    (52, 98, 53): "Salle des Moogles (Rune Edge ; Ribbon dans le Monde de la Ruine)",
    (351, 4, 52): "3e salle, porte de droite",
    (351, 45, 7): "3e salle, porte de gauche puis salle suivante, porte de droite",
    (375, 46, 27): "1re salle de la montagne : Healing Rod",
    (354, 0, 0): "",
}
