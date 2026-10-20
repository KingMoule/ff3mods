# Free space

Unused ROM regions (filled with `$FF` in the clean 1.1 ROM) and what uses them.
Update this file whenever a patch claims space.

| Region | Size | Used by |
|---|---|---|
| C0/D613-C0/DF9F | 2445 | |
| C0/EC20-C0/EE9F | 640 | |
| C2/6469-C2/64CF | 103 | `balance/cyan_swdtech.asm` |
| C2/64D0-C2/67FF | 816 | |
| C2/A65A-C2/A7FF | 422 | |
| C2/FAAB-C2/FC6C | 450 | |
| C3/F091-C3/FFFF | 3951 | |

Bank C1 (battle graphics and menus) has no free run of 64+ bytes; code
needed there will have to `jsl` to another bank.
