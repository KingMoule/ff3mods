# ff3mods

Mods pour **Final Fantasy III (USA) Rev 1** (v1.1, sans header) :
corrections de bugs, mini patch de balance et menu Blitz pour Sabin.

## Build

Prérequis : Python 3.11+, `tools/asar/asar.exe` (asar 1.91) et
`tools/flips/flips.exe` (Flips v198). Le dossier `tools/` n'est pas versionné.

1. Mettre la ROM propre dans `rom/ff3_us_11.sfc` (CRC32 `C0FA0464`).
   La ROM n'est jamais commitée.
2. `python build.py`

Résultats dans `build/` : `ff3mods.sfc`, plus `ff3mods.ips` et `ff3mods.bps`
à appliquer sur une ROM propre.

Les patchs appliqués sont listés dans `patches.txt`; commenter une ligne
désactive le patch.

## Patchs

**Bug fixes, niveau 1** (combat et bugs qui cassent le jeu), dans `patches/bugfixes/` :

- `evade.asm` : la stat Evade sert enfin aux attaques physiques (Blind et Beads fonctionnent)
- `vanish_doom.asm` : Vanish ne rend plus X-Zone/Doom mortels sur les cibles protégées
- `ultimate_damage.asm` : plus de débordement des dégâts; Genji Glove/Offering ne réduisent que Fight/Capture
- 25 correctifs de Leet Sketcher (Zombie/Rippler, Imp's Retort, Self Sneeze, Dead in the Air,
  Smoke and Mirrors, Soul Saved, Morph Mayhem, etc.); chaque fichier décrit le bug corrigé

**Bug fixes, niveau 2** (événements, cartes, softlocks hors combat) : 22 correctifs de Leet Sketcher
(Menu Malarky, Returner's Day Off, Shadow Gone, Game Over, Map Mishap, Multiple Events, etc.).

Le bug de Sketch est déjà corrigé dans la ROM 1.1 d'origine.

**Balance**, dans `patches/balance/` :

- `cyan_swdtech.asm` : jauge SwdTech 2x plus rapide; toutes les SwdTech basées sur l'arme et la
  Vigor (multiple d'un Fight). Requiert `ultimate_damage.asm`.

**Fonctionnalités**, dans `patches/features/` :

- `blitz_menu.asm` : la commande Blitz ouvre une liste des Blitz appris (fenêtre 4 x 2 comme Magitek);
  on choisit le Blitz puis la cible. Plus de combinaisons de touches.

L'espace libre utilisé dans la ROM est tenu à jour dans `docs/freespace.md`.

## Correctifs générés depuis des IPS

Les correctifs de Leet Sketcher sont générés depuis ses IPS publiés :

1. Mettre les IPS listés dans `scripts/leet_fixes.json` dans `vendor/leet/` (non versionné).
2. `python scripts/ips2asar.py scripts/leet_fixes.json` régénère les `.asm`.
3. Après `python build.py`, `python scripts/verify_ips.py scripts/leet_fixes.json` liste
   les octets où le build diffère des IPS appliqués en séquence (seulement nos propres patchs).

## Crédits

Les correctifs de bugs marqués (Leet Sketcher) sont des ports en asar des
patchs de Leet Sketcher (<https://l33t5k37ch3r.altervista.org/>), vérifiés
octet par octet contre ses IPS publiés.
