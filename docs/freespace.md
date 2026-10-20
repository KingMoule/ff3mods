# Free space

Unused ROM regions (filled with `$FF` in the clean 1.1 ROM) and what uses them.
Update this file whenever a patch claims space.

| Region | Size | Used by |
|---|---|---|
| C0/D613-C0/D82E | 540 | |
| C0/D82F-C0/D8B8 | 138 | `bugfixes/trigger_happy.asm` |
| C0/D8B9-C0/DF9F | 1767 | |
| C0/EC20-C0/EE9F | 640 | |
| C2/6469-C2/64CF | 103 | `balance/cyan_swdtech.asm` |
| C2/64D0-C2/65BD | 238 | |
| C2/65BE-C2/65D4 | 23 | `bugfixes/zombie_rippler.asm` |
| C2/65D5-C2/6751 | 381 | |
| C2/6752-C2/675C | 11 | `bugfixes/morph_mayhem.asm` |
| C2/675D-C2/6771 | 21 | `bugfixes/zombie_tapir.asm` |
| C2/6772-C2/677D | 12 | `bugfixes/killer_life_3.asm` |
| C2/677E-C2/67E0 | 99 | |
| C2/67E1-C2/67F1 | 17 | `bugfixes/imp_call.asm` |
| C2/67F2-C2/67FF | 14 | |
| C2/A65A-C2/A66F | 22 | `bugfixes/vanish_doom.asm` |
| C2/A670-C2/A7F6 | 391 | |
| C2/A7F7-C2/A7FF | 9 | `bugfixes/morph_mayhem.asm` |
| C2/FAAB-C2/FC6C | 450 | |
| C3/F091-C3/FFFF | 3951 | |

Bank C1 (battle graphics and menus) has no `$FF` free space. Reclaimed code:

| Region | Size | Used by |
|---|---|---|
| C1/6F67-C1/7020 | 186 | `features/blitz_menu.asm` (old Blitz combo input, now unreachable) |
| C1/7021-C1/7092 | 114 | free (rest of the old Blitz combo input) |

Leet Sketcher's fixes also reuse some code and data they free up themselves
(outside these `$FF` regions); `scripts/verify_ips.py` and the generated
`.asm` files show every byte they write.

To see which bytes a build changed inside these regions, compare
`build/clean.sfc` and `build/ff3mods.sfc`.
