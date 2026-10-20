# Free space

Unused ROM regions (filled with `$FF` in the clean 1.1 ROM) and what uses them.
Update this file whenever a patch claims space.

| Region | Size | Used by |
|---|---|---|
| C0/D613-C0/DF9F | 2445 | |
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
| C2/67F2-C2/67F4 | 3 | |
| C2/67F5-C2/67FF | 11 | `bugfixes/chance_offering.asm` |
| C2/A65A-C2/A66F | 22 | `bugfixes/vanish_doom.asm` |
| C2/A670-C2/A7F6 | 391 | |
| C2/A7F7-C2/A7FF | 9 | `bugfixes/morph_mayhem.asm` |
| C2/FAAB-C2/FC6C | 450 | |
| C3/F091-C3/FFFF | 3951 | |

Bank C1 (battle graphics and menus) has no free run of 64+ bytes; code
needed there will have to `jsl` to another bank.

To see which bytes a build changed inside these regions, compare
`build/clean.sfc` and `build/ff3mods.sfc`.
