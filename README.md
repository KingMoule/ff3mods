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

| Patch | Effet |
|---|---|
| `patches/bugfixes/ultimate_damage.asm` | Plus de débordement des dégâts au-delà de 65 535; Genji Glove et Offering ne réduisent que Fight/Capture (Leet Sketcher) |
| `patches/balance/cyan_swdtech.asm` | Jauge SwdTech 2x plus rapide; toutes les SwdTech basées sur l'arme et la Vigor (multiple d'un Fight). Requiert `ultimate_damage` |

L'espace libre utilisé dans la ROM est tenu à jour dans `docs/freespace.md`.

## Crédits

Les correctifs de bugs marqués (Leet Sketcher) sont des ports en asar des
patchs de Leet Sketcher (<https://l33t5k37ch3r.altervista.org/>), vérifiés
octet par octet contre ses IPS publiés.
