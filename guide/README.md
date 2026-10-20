# Guide FF6 (PWA hors-ligne)

Guide de jeu pour **Final Fantasy III US v1.1 (FF6 SNES) avec les modifications du mod ff3mods**.
Site statique (HTML/CSS/JS, sans framework ni étape de build obligatoire), installable sur iPhone,
100 % hors-ligne après la première visite. Interface en français ; noms d'objets, monstres et sorts
en anglais comme dans le jeu US.

## Contenu

- **Marche** : chapitres Balance puis Ruine, lieu par lieu, avec cases à cocher (progression par lieu,
  par chapitre et globale ; filtres « Non cochés » et « Manquables seulement » ; recherche), monstres
  de chaque lieu liés au bestiaire. Suivis des 27 Espers, 14 personnages et 24 Lores.
- **Bestiaire** : tous les monstres nommés (stats, faiblesses, statuts, vol/butin, attaques lues dans les
  scripts d'IA, Rage, Sketch, Control, Metamorph, lieux), recherche et filtres.
- **Persos** : stats de départ, commandes, techniques (magie naturelle, SwdTech et Blitz de la version mod,
  danses, outils…), meilleur équipement par catégorie (avec la source de chaque objet).
- **Formules** (version moddée) + petits calculateurs.
- **Plus** : Espers, objets (sources : coffres, boutiques, vol, butin, Colisée, Metamorph), boutiques,
  Colisée, Lores, carte des rencontres du monde (8×8 secteurs), tables PV/PM/EXP, liste des différences
  du mod, quêtes, réglages (thème, export/import/effacement de la progression).

## Navigation

- Bottom tabs: **Walkthrough**, **Bestiary**, **Characters**, **Items** (`#/more/items`) and **Espers**
  (`#/more/espers`), plus **More**: a two-column grid of the remaining sections (Formulas at `#/formulas`, shops,
  Colosseum, Lores, techniques, encounter map, tables, mod changes, quests, quest items, settings).
- Walkthrough home: a "Continue" button to the last opened chapter (`ff6g.lastChap`), then the chapters as a
  two-column grid with progress and lost-forever counts.
- Chapter page: a sticky strip of chapter numbers (1–21, R1–R11, Espers/Chars/Lores; ✓ = fully checked) to jump
  in one tap, previous/All/next links at the bottom, and location headers that collapse when tapped.
- Bestiary and items: the search box and filter chips stay sticky; chips scroll horizontally.

## Fiabilité des données

| Donnée | Source |
| --- | --- |
| Monstres, objets, sorts, Espers, personnages, boutiques, Colisée, Metamorph, tables, SwdTech/Blitz | lues dans la ROM moddée (`extract.py`) |
| Coffres (position, contenu), rencontres aléatoires par carte et par secteur du monde | lues dans la ROM |
| Attaques d'un monstre | décodées des scripts d'IA de la ROM (commande « attaque ») |
| Qui lance quel Lore | idem (scripts d'IA) |
| Ordre des chapitres, cartes accessibles à chaque étape, événements, récompenses, « perdu à jamais » | écrits à la main, **recoupés avec le walkthrough Caves of Narshe** (balise « guide ») ; ce qui n'est confirmé par aucune source reste marqué « ≈ » |
| Noms des lieux, regroupement des cartes en lieux, événements (personnages, Espers, boss, objets cachés, manquables), conseils d'équipement | **écrits à la main**, déduits des dialogues/contenus de la ROM et de connaissances du jeu : **non vérifiés** (marqués « ≈ » dans l'application) |
| « ROM » (étiquette verte) | l'objet/l'Esper figure bien dans un script d'événement de la ROM (recoupement grossier par recherche d'octets) |
| Lieux des Espers | indices : carte dont un déclencheur démarre juste avant l'octet « donner un Esper » (peut être faux) |

Chaque coffre de la ROM est rattaché au **premier chapitre dont l'entrée liste sa carte** (`maps=[...]` dans
`walkthrough_src.py` ; sans `maps`, toutes les cartes du lieu). Les coffres au contenu variable (même bit d'événement
sur plusieurs cartes) sont fusionnés. **Perdu à jamais** : `lost="raison"` sur une entrée de chapitre (tous ses coffres)
ou sur un événement ; en rouge seulement pour l'équipement, les reliques et les objets rares, les autres coffres de
la même entrée affichent « dernière chance » (ambre).

Limites connues : l'analyse complète des scripts d'événement n'est pas faite (les récompenses d'événements
sont donc écrites à la main) ; les noms de zones des cartes sans titre sont des déductions ; plusieurs coffres
existent en variantes (même coffre, contenu qui dépend de l'avancement) : ils sont fusionnés en une seule case
marquée « variable » ; l'apprentissage des danses par terrain n'est pas détaillé.

## Régénérer les données

Prérequis : Python 3.11+ ; la ROM propre `rom/ff3_us_11.sfc` (CRC32 `C0FA0464`, jamais versionnée) ;
pour décrire le jeu moddé, la ROM produite par `python build.py` (`build/ff3mods.sfc`). Depuis la racine du dépôt :

```bash
python -I guide/tools/extract.py --rom rom/ff3_us_11.sfc --mod build/ff3mods.sfc
python -I guide/tools/build_data.py
```

- `extract.py` écrit `guide/data/raw/*.json` (non versionné), `attacks.json`, `espers.json`, `misc.json`,
  `mod_diff.json`. Sans `--mod`, le guide décrit le jeu non modifié.
- `build_data.py` fusionne ces données avec `tools/walkthrough_src.py` (chapitres et événements) et
  `tools/content.py` (formules, liste du mod, conseils), écrit les JSON finaux et **régénère `sw.js`**
  (version = empreinte des fichiers → le cache hors-ligne se met à jour tout seul).
- Icônes : `python -I guide/tools/make_icons.py` (nécessite Pillow ; les PNG sont déjà fournis).

Les JSON de `guide/data/` (hors `raw/`) sont versionnés pour que le site fonctionne sans ROM.
Aucun fichier `.sfc` ni la ROM ne sont jamais écrits ni commités.

## Tester en local

```bash
python -m http.server 8791 --bind 127.0.0.1 --directory guide
```

puis ouvrir <http://127.0.0.1:8791/>. Au gabarit mobile (375×812) : toutes les sections s'affichent, les cases
cochées persistent (localStorage), les liens checklist → bestiaire fonctionnent.
Note : le service worker n'a pas pu être testé dans le navigateur intégré de l'outil de développement (il
refuse tout service worker) ; la liste des fichiers mis en cache a été vérifiée (tous répondent 200). À
confirmer dans Safari/Chrome (onglet Application > Service Workers).

## Installer sur l'iPhone

Safari n'installe une PWA et ne garde le cache hors-ligne que depuis un hébergement **HTTPS** (ou `localhost`).
La solution la plus simple, gratuite : **GitHub Pages**.

1. Pousser le dossier `guide/` (ex. branche `gh-pages`, ou paramètres du dépôt › Pages › « Deploy from a
   branch », dossier `/guide` si vous le servez depuis la branche principale — GitHub n'accepte que `/` ou `/docs` :
   dans ce cas copiez `guide/` vers `docs/` ou publiez `guide/` seul sur une branche dédiée).
2. Ouvrir l'URL `https://<utilisateur>.github.io/<dépôt>/` **dans Safari** sur l'iPhone, laisser la page se charger
   entièrement (premier chargement en ligne = mise en cache).
3. Bouton Partager › **Sur l'écran d'accueil**. Lancer l'icône « Guide FF6 » : mode plein écran, hors-ligne.
4. Pour mettre à jour : relancer l'app avec du réseau (le service worker récupère la nouvelle version ; fermez
   et rouvrez l'app une fois).

Rien n'est publié ni poussé automatiquement : à faire par vous.

## Structure

```
guide/
  index.html, manifest.webmanifest, sw.js (généré), icons/, css/app.css
  js/   app.js (routeur) · walk.js · bestiary.js · chars.js · formulas.js · more.js · state.js · util.js
  data/ *.json générés (raw/ ignoré)
  tools/ ff6rom.py · extract.py · build_data.py · walkthrough_src.py · content.py · make_icons.py · sw.template.js
```

Formats de la ROM : désassemblage everything8215/ff6 (monstres CF/0000, noms CF/C050, sorts C4/6AC0,
objets D8/5000, Espers D8/6E00, personnages ED/7CA0, coffres ED/8634, groupes de rencontres CF/4800-CF/5600…).
