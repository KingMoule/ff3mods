"""Textes rédigés à la main (français) : formules, différences du mod, personnages, quêtes.

Les formules ont été relues dans le code (désassemblage everything8215/ff6 + patches/ du dépôt).
Les passages marqués « non vérifié » sont des connaissances de jeu non recoupées dans la ROM.
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
    dict(id="notation", title="Notations", blocks=[
        UL("Niv = niveau de l'attaquant ; Vigor = stat Vigor (« Strength »), Vig2 = Vigor x 2 plafonné à 255",
           "BP = Battle Power de l'arme ; Puiss = puissance du sort ; MagPwr = stat Magic Power (monstres : valeur x 1,5)",
           "Déf / MDéf = Defense / Magic Defense de la cible ; Évas / MBlock = Evade / Magic Block (en %)",
           "Tous les dégâts finaux sont plafonnés à 9999 par cible."),
    ]),
    dict(id="phys", title="Dégâts physiques", blocks=[
        P("Personnage (Fight, Capture, Blitz, SwdTech…). La puissance de base vient de l'arme (ou de la puissance du Blitz) :"),
        F("base = BP + 1,5 x (Niv² x (BP + Vig2) / 256)"),
        P("Monstre (stat Atk du monstre ; la « Vigor » d'un monstre vaut 56 à 63 au hasard) :"),
        F("base = Niv² x (4 x Atk + Vig_monstre) / 256     (pas de x1,5 ni de +BP)"),
        P("Ensuite, dans cet ordre :"),
        UL("Fight/Capture seulement (mod) : Offering ÷2 (arrondi supérieur), puis Genji Glove x3/4",
           "Atlas Armlet : +50 % ; (la mod conserve : Earring +100 % / simple +50 % pour la magie)",
           "Gauntlet : le BP compte pour 7/4 dans la formule ci-dessus",
           "Variance : x (224 à 255) / 256, soit environ 88 % à 100 %",
           "Défense : x (255 − Déf) / 256, puis +1 (ignorée par les attaques « ignore la défense »)",
           "Safe sur la cible : x 170/256 (≈ 2/3) ; rangée arrière ou Defend : ÷2 (cumulables : ÷4)",
           "Berserk, Morph (attaquant), coup critique : multiplicateur x(1 + n/2) ; critique = 1 chance sur 32, x2",
           "Attaque d'un personnage sur un autre personnage (Muddle…) : ÷2",
           "Faiblesse élémentaire x2 ; résistance ÷2 ; immunité 0 ; absorption : soigne"),
        MOD("Mod (Ultimate Damage) : plus de débordement au-delà de 65 535 (une attaque énorme ne retombe plus à presque 0) ; "
            "Offering et Genji Glove ne réduisent plus que Fight et Capture (pas Pummel, SwdTech, etc.)."),
    ]),
    dict(id="magic", title="Dégâts magiques", blocks=[
        F("base = 4 x Puiss + Niv x MagPwr x Puiss / 32"),
        UL("Earring : +100 % (deux Earrings) ou +50 % (un seul) ; appliqué avant la variance",
           "Variance : x (224 à 255) / 256",
           "Défense : x (255 − MDéf) / 256 + 1 (sauf sorts qui ignorent la défense)",
           "Shell sur la cible : x 170/256 ; cible en Morph : dégâts magiques ÷2 (d'après le code)",
           "Plusieurs cibles : le plus souvent les dégâts sont répartis ; certains sorts ne le sont pas (« dégâts non divisés »)",
           "Éléments : x2 faiblesse, ÷2 résistance, 0 immunité, absorption = soin"),
        P("Les soins : base = 4 x Puiss + Niv x MagPwr x Puiss / 32 également (sans défense), ils appliquent les mêmes éléments (inversés contre les morts-vivants)."),
    ]),
    dict(id="hit", title="Précision et esquive", blocks=[
        P("Attaque physique (mod : l'Evade fonctionne enfin) :"),
        F("touche si rand(0..99) < précision x (256 − 2 x Évas) / 256"),
        UL("précision : stat de l'arme (ou du monstre) ; Blind sur l'attaquant ÷2 ; cible avec Beads (esquive aléatoire) ÷2",
           "Évas ≥ 128 : multiplicateur minimal (1/256) → quasi impossible à toucher",
           "Image : une attaque physique sur trois ou quatre est absorbée (rand < 64/256) et retire Image",
           "Toujours touché : cible en Stop, Sleep, Petrify ou Frozen ; cible en position de Retort ; sorts « ne rate jamais »",
           "Attaque magique : mêmes calculs avec MBlock, sans Blind ni Beads."),
        MOD("Avant la mod, l'Evade n'était jamais utilisée (les attaques physiques lisaient MBlock) et Blind/Beads étaient sans effet. "
            "Une vingtaine de monstres à Evade élevée deviennent plus difficiles à toucher : Mover, Pugs, Scrapper, Punisher, Ursus, Borras, Cruller, Vindr…"),
        P("Mort instantanée (Doom, X-Zone, armes X…) : manque si la cible est protégée ; sinon test sur Stamina. "
          "La mod empêche Vanish de contourner la protection contre la mort."),
    ]),
    dict(id="steal", title="Vol (Steal / Mug)", blocks=[
        F("chance de réussite = Niv_voleur + 50 − Niv_cible  (en %)   ; x2 avec la Sneak Ring"),
        P("Si le vol réussit, l'emplacement tiré est le rare ou le commun ; un emplacement vide fait échouer le vol."),
        MOD("Mod (Locke) : objet rare 1 fois sur 4 (64/256) au lieu de 1 sur 8 (32/256)."),
        P("Butin en fin de combat : objet rare 1/8, commun 7/8 (une seule tentative par monstre, aucune modification de la mod)."),
    ]),
    dict(id="dice", title="Dice (Setzer)", blocks=[
        F("dégâts = (produit des dés) x Niv x 2     (ignore la défense ; bonus si les dés sont identiques)"),
        MOD("Mod (Better Dice) : un dé a toujours une répartition égale de 1 à 6, les autres s'en rapprochent "
            "(vanilla : 1-4 à 3/16, 5-6 à 1/8) ; le bonus de dés identiques s'applique aussi au Dice à 2 dés ; "
            "l'Offering divise les dégâts des dés."),
    ]),
    dict(id="swd", title="SwdTech (Cyan)", blocks=[
        P("Dans le jeu d'origine les SwdTech avaient leurs propres puissances. Dans cette mod, la jauge se remplit deux fois plus vite "
          "(un cran toutes les 64 images au lieu de 128) et toutes les SwdTech sont des attaques physiques basées sur l'arme et la Vigor :"),
        F("dégâts = multiplicateur x (dégâts d'un Fight)"),
        UL("Dispatch (niv. 1) : x1,25, une cible, ignore la défense",
           "Retort (niv. 6) : contre x1,5, ignore la défense",
           "Slash (niv. 12) : x1,5 + Sap ; fonctionne sur les boss (plus de test 50 % PV / mort)",
           "Quadra Slam (niv. 15) : 4 coups x0,75 sur cibles aléatoires",
           "Empowerer (niv. 24) : x1 en drain de PV, puis x0,25 en drain de PM",
           "Stunner (niv. 34) : x1 sur tous les ennemis + Stop (140/256)",
           "Quadra Slice (niv. 44) : 4 coups x1, ignore la défense",
           "Cleave (niv. 70) : x1,5 sur tous + Death (182/256)"),
        NOTE("Les niveaux d'apprentissage et les puissances ci-dessus sont relus dans la ROM modifiée (page Personnages > Cyan)."),
    ]),
    dict(id="blitz", title="Blitz (Sabin)", blocks=[
        P("Les Blitz sont des attaques physiques : la puissance du Blitz remplace le BP de l'arme dans la formule physique "
          "(plus Vigor). Sabin les apprend au niveau 1, 6, 10, 15, 23, 30, 42 et 70."),
        MOD("Mod : la commande Blitz ouvre une liste (comme Magitek) ; on choisit le Blitz puis la cible, "
            "plus de saisie de combinaisons. Les Blitz non appris apparaissent vides."),
    ]),
    dict(id="sketch", title="Sketch, Control, Rage, Lore", blocks=[
        UL("Sketch (Relm) : copie l'une des 2 attaques « Sketch » du monstre ; la réussite dépend du rapport des niveaux (Beret l'améliore) ; les monstres marqués « Non Sketchable » échouent",
           "Control : le monstre exécute l'une de ses 4 attaques « Control » ; Coronet améliore la réussite",
           "Rage (Gau) : Gau agit comme le monstre appris et utilise l'attaque de Rage de sa fiche ; « (Attaque spéciale) » = l'attaque spéciale du monstre",
           "Lore (Strago) : formules magiques avec la MagPwr de Strago ; s'apprennent en subissant l'attaque ; ne s'apprennent pas si Strago est KO"),
    ]),
    dict(id="exp", title="Expérience et progression", blocks=[
        P("PV, PM et statistiques évoluent par niveau selon les tables du jeu ; les bonus d'Espers s'ajoutent au prochain niveau (voir Plus > Espers). "
          "Les PV/PM max peuvent être augmentés par les accessoires (+12,5 %, +25 %, +50 %). Les tables PV/PM/EXP lues dans la ROM sont dans Plus > Tables."),
        P("Un personnage qui rejoint tardivement reçoit un niveau proche de la moyenne du groupe (décalage propre à chaque personnage : voir fiches)."),
    ]),
]

# (groupe, titre, texte)
MODS = [
    ("Correctifs de combat", "Evade (physique)", "Les attaques physiques utilisent Evade ; Blind et Beads fonctionnent. Une vingtaine de monstres deviennent plus durs à toucher."),
    ("Correctifs de combat", "Vanish / Doom", "Vanish ne permet plus à Doom ou X-Zone de tuer les cibles protégées contre la mort instantanée (boss compris)."),
    ("Correctifs de combat", "Ultimate Damage", "Plus de débordement au-delà de 65 535 ; Genji Glove et Offering ne réduisent que Fight et Capture."),
    ("Correctifs de combat", "Dead Hare", "Un monstre déjà retiré du combat (tué par le Scimitar, etc.) ne contre-attaque plus."),
    ("Correctifs de combat", "Item/Magic Counter", "Les monstres qui ne contrent qu'un sort/objet précis (SrBehemoth, FlameEater…) ne contrent plus tout ensuite."),
    ("Correctifs de combat", "Zombie/Rippler", "Rippler n'échange plus les statuts cachés ; un Zombie guéri par Rippler récupère 1/8 de ses PV."),
    ("Correctifs de combat", "Imp's Retort", "Cyan Imp dont le Retort échoue ne contre plus tout le combat."),
    ("Correctifs de combat", "Self Sneeze", "Le lien de Fake Mustache est coupé quand Relm utilise Palidor ou si un côté disparaît."),
    ("Correctifs de combat", "Dead in the Air", "Condemned en plein Jump : Wound au lieu de rester à 0 PV ; objets restaurés après chaque combat ; bonus Esper +30 % PV/PM corrigé."),
    ("Correctifs de combat", "Smoke and Mirrors", "Le Smoke Bomb d'un personnage Muddle ne retire plus les monstres (et donc la victoire) à sa place."),
    ("Correctifs de combat", "Soul Saved", "Les Soul Savers sont immunisés contre la mort instantanée : X-Zone ne peut plus terminer le combat Wrexsoul."),
    ("Correctifs de combat", "Morph Mayhem", "La jauge de Morph ne baisse plus pendant Sleep/Stop/Frozen, pendant un Quick, ni après la sortie du combat."),
    ("Correctifs de combat", "Rock Bottom", "Near Fatal est réappliqué quand Petrify est soigné sous 1/8 des PV."),
    ("Correctifs de combat", "Status Unknown", "Les statuts sans couleur de contour (Life 3, Float…) ne s'affichent plus vides."),
    ("Correctifs de combat", "Imp Skimp / Imp's Rage / Imp's Call", "Sprite Imp lié au statut ; Rage et Dance interdits en Imp ; un Esper annulé par Imp n'est plus perdu."),
    ("Correctifs de combat", "Shadow's Status", "Les statuts durables sont retirés à Shadow après le Continent flottant."),
    ("Correctifs de combat", "Stone Faced / Stone Cold", "Les monstres pétrifiés ne répètent plus leur attaque ; Petrify ne bloque plus Revivify."),
    ("Correctifs de combat", "Killer Life 3", "Un monstre mort-vivant tué par une arme X ne ressuscite plus avec Life 3 pour mourir encore."),
    ("Correctifs de combat", "Zombie/Tapir", "Tapir qui guérit Zombie rend 1/8 des PV max."),
    ("Correctifs de combat", "Double Block / Half Knife", "Un Fenix Down n'est plus bloqué deux fois par un bouclier ; l'Offering divise aussi le bonus de ValiantKnife."),
    ("Correctifs de combat", "Bye Bye Breath / Off Death Row / Throwback", "Plantages du 2e combat Phunbaba corrigés ; Safety Bit et Memento Ring retirent Condemned ; Shadow lance normalement vers une cible en Jump."),
    ("Correctifs d'événements", "Menu Malarky", "Plus de saut d'événements via le menu (Locke et le garde de South Figaro, Inferno, Poltergeist)."),
    ("Correctifs d'événements", "Returner's Day Off", "Deux événements corrigés pour Gau resté sur le Veldt (personnages oubliés, blocage après Esper World)."),
    ("Correctifs d'événements", "Shadow Gone / Shadow Copy", "Plus de groupe vide à Narshe sans Shadow ; Mimic ne copie plus Shadow au Colisée du cou du Dragon."),
    ("Correctifs d'événements", "Game Over", "Une défaite sur la carte du monde ne laisse plus de pointeur sur la pile (blocage après 52 défaites)."),
    ("Correctifs d'événements", "Map Mishap / Multiple Events / Bland Entrance", "Sept problèmes de carte, dix événements et l'ouverture du jeu corrigés (voir le readme de Leet Sketcher)."),
    ("Correctifs d'événements", "Stepping Out / Trigger Happy / Walk This Way", "Y maintenu n'interrompt plus les événements ; un événement de timer ne passe plus devant une case-événement ; escaliers diagonaux."),
    ("Correctifs d'événements", "Unequipium / Castle Party / Narshe's Door", "PV/PM rafraîchis quand un événement retire l'équipement ; ordre du groupe à Doma ; porte secrète de Narshe."),
    ("Correctifs d'événements", "Anonymous Attack / Caravaggio / Chain of Command", "Attaque de Kefka à la Porte scellée ; Roulette via Sketch/Rage ; noms des commandes de Gogo."),
    ("Correctifs d'événements", "Precious Jewels / Phoenix Chest / Off the Hook / Loud Music", "Gem Box sans embuscade ; coffre du Phoenix Cave ; personnage au-dessus du crochet ; orgue de l'Opéra."),
    ("Correctifs d'événements", "Save Point Switch", "Changer de groupe au Phoenix Cave/Tour de Kefka ne permet plus de sauvegarder ou dormir hors point de sauvegarde."),
    ("Équilibrage", "Cyan : SwdTech", "Jauge 2x plus rapide ; toutes les SwdTech physiques, basées sur l'arme et la Vigor (voir Formules)."),
    ("Équilibrage", "Locke : vol", "Objet rare volé 1 fois sur 4 au lieu de 1 sur 8."),
    ("Équilibrage", "Better Dice", "Dés de Setzer mieux répartis, bonus de dés identiques aussi pour Dice à 2 dés, Offering divise les dés."),
    ("Fonctionnalité", "Menu Blitz", "La commande Blitz de Sabin ouvre une liste ; on choisit le Blitz puis la cible."),
]

CHARS = {
    "Terra": dict(
        role="Magie + Morph. Apprend sa magie naturelle (voir tableau), puis par Espers.",
        tips=["Morph double ses dégâts physiques et magiques (durée limitée) ; la jauge est protégée par les correctifs.",
              "Magie naturelle : Terra et Celes apprennent des sorts à certains niveaux."],
        gear=[("Début", "MithrilKnife, Buckler : remplacez-les dès que possible par un bâton/épée."),
              ("Milieu du jeu", "Earrings + accessoire de PM ; une robe pour la défense magique."),
              ("Fin", "Rod/Brush forts, Ribbon ; Minerva (armure) très recherchée.")]),
    "Locke": dict(
        role="Voleur : Steal/Mug. La mod donne l'objet rare 1 fois sur 4.",
        tips=["Sneak Ring : double la chance de vol.", "Mug = Fight + vol ; Thief Glove (Capture) donne Capture."],
        gear=[("Début", "Dirk puis MithrilKnife/Guardian."), ("Milieu", "Dagues rapides (Tempest, Strato si dispo)."),
              ("Fin", "Valiant Knife, Strato, Gauntlet/Genji Glove ; Sneak Ring.")]),
    "Cyan": dict(
        role="SwdTech (mod : physiques, jauge x2 plus rapide).",
        tips=["Les SwdTech dépendent du BP de l'arme : équipez une arme à BP élevé (katanas).",
              "Retort sur contre-attaque : x1,5 ; Cleave au niveau 70."],
        gear=[("Début", "Katana de base."), ("Milieu", "Kotetsu, Murasame."), ("Fin", "Masamune/Aura etc., Genji Glove.")]),
    "Shadow": dict(
        role="Ninja : Throw ; peut partir à tout moment au Continent flottant.",
        tips=["Ne le laissez pas partir sans décompte : voir Marche > Continent flottant."],
        gear=[("Tout le jeu", "Shuriken/Ninja Star à lancer ; Tack Star ; armes rapides.")]),
    "Edgar": dict(
        role="Tools (Auto Crossbow, Bio Blaster, Chain Saw, Drill…).",
        tips=["Les Tools n'utilisent pas la Vigor de la même manière que Fight : le Chain Saw/Drill sont forts ; Auto Crossbow touche tout."],
        gear=[("Début", "Tools à acheter à Figaro Castle."), ("Fin", "Drill, Flash, Debilitator, Air Anchor selon besoin.")]),
    "Sabin": dict(
        role="Blitz (mod : menu), arts martiaux.",
        tips=["Blitz : Pummel, AuraBolt, Suplex, Fire Dance, Mantra, Air Blade, Spiraler, Bum Rush.",
              "Il peut combattre sans arme (griffes/gants)."],
        gear=[("Début", "Griffes de départ."), ("Fin", "Hauts BP de griffes, Hyper Wrist/Sprint.")]),
    "Celes": dict(
        role="Runic (absorbe la magie) + magie naturelle.",
        tips=["Runic absorbe les sorts offensifs : utile contre les boss de magie."],
        gear=[("Début", "Épée de chevalier."), ("Fin", "Épées fortes + armures magiques.")]),
    "Strago": dict(
        role="Lores (sorts appris des monstres).",
        tips=["Les Lores s'apprennent en subissant l'attaque ; voir Plus > Lores pour qui la lance."],
        gear=[("Tout le jeu", "Rods/Mithril Rod, robes magiques.")]),
    "Relm": dict(
        role="Sketch (copie une attaque).",
        tips=["Sketch peut échouer ou montrer une attaque aléatoire."],
        gear=[("Tout le jeu", "Brushes (Magical Brsh, Rainbow Brsh), chapeaux de magie.")]),
    "Setzer": dict(
        role="Slot (+ Dice avec la mod).",
        tips=["Joker Doom est très puissant mais fait échouer ; les Dice sont rééquilibrés par la mod."],
        gear=[("Début", "Cards."), ("Fin", "Fixed Dice, Dice à utiliser pour l'Offering.")]),
    "Mog": dict(role="Danses (selon le terrain).", tips=["Learn Dance en combat sur le terrain correspondant."],
                gear=[("Tout le jeu", "Lances : Mithril Pike, Trident... ; armes légères.")]),
    "Gau": dict(role="Rage : copie des monstres du Veldt.", tips=["Utilisez Leap sur le Veldt ; il apprend des Rages en combat."],
                gear=[("Tout le jeu", "Armes à mains nues/ Wing Edge.")]),
    "Gogo": dict(role="Mimic + commandes configurables.", tips=["Mimic répète l'action de l'allié précédent."],
                 gear=[("Tout le jeu", "Équipement polyvalent.")]),
    "Umaro": dict(role="Bersek fixe ; Throw automatique.", tips=["Équipement de Berserk permanent."],
                  gear=[("Tout le jeu", "Il utilise des accessoires mais pas d'armes.")]),
}

SIDEQUESTS = [
    dict(title="Cursed Shld → Paladin Shld", text="Le vieillard de Narshe donne la Cursed Shld (via Locke). 256 combats avec un autre personnage que Gogo pour la purifier en Paladin Shld.", g=True),
    dict(title="Ragnarok", text="Le vieillard de Narshe permet de choisir l'Esper Ragnarok OU l'épée : choisir l'un fait perdre l'autre (l'épée peut être volée à la fin).", g=True),
    dict(title="Colisée", text="Misez un objet pour affronter un monstre et gagner un objet rare (voir Plus > Colisée). Le gain est lu dans la ROM.", g=False),
    dict(title="Tour des Fanatiques", text="Tour sans magie : Gem Box, Safety Bit, Genji Shld, Stunner, Force Armor, Air Anchor.", g=False),
    dict(title="Veldt / Rages", text="Gau apprend des Rages en Leap. Les monstres rencontrés sur le Veldt sont dans le Bestiaire (page Monde).", g=True),
    dict(title="Danse Water Rondo", text="Mog doit combattre en eau pendant le Monde de la Balance (Lete River ou Serpent Trench), sinon elle est perdue.", g=True),
    dict(title="Force Field (Lore)", text="Uniquement depuis Doom, dans un seul combat, avec Strago présent.", g=True),
]
LORE_HINT = "Qui lance chaque Lore est lu dans les scripts d'IA des monstres (ROM)."

CONTENT = {"formulas": FORMULAS, "mods": [dict(group=g, title=t, text=x) for g, t, x in MODS],
           "sidequests": SIDEQUESTS, "lore_hint": LORE_HINT}
