; Dead Hare v1.5 by Leet Sketcher
;
; Monsters already removed from battle (e.g. killed by the Scimitar's instant
; kill) no longer counterattack.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-DeadHare-N.ips

hirom

assert read3($C21C41) == $3290BC, "unexpected ROM state"
org $C21C41
        db $20, $3A, $5A

assert read4($C259DE) == $D0048948 && read4($C25A48) == $FAB874AA, "unexpected ROM state"
org $C259DE
        db $C9, $04, $F0, $57, $89, $04, $D0, $41, $AD, $1F, $20, $4A, $3A, $30, $3A, $2A
        db $49, $01, $9B, $C0, $08, $AA, $D0, $0B, $A9, $0C, $EB, $A9, $03, $2A, $49, $01
        db $4A, $80, $08, $AD, $AD, $2E, $EB, $AD, $AC, $2E, $C8, $90, $07, $39, $18, $30
        db $F0, $11, $80, $0E, $34, $B8, $F0, $11, $EB, $34, $B8, $F0, $0C, $20, $53, $4B
        db $90, $01, $EB, $49, $FF, $35, $B8, $95, $B8, $A5, $B8, $F0, $0E, $A5, $B9, $F0
        db $0A, $20, $5A, $4B, $DA, $29, $01, $AA, $74, $B8, $FA, $60, $48, $B9, $F9, $3E
        db $0A, $0A, $0A, $68, $B0, $04, $BC, $90, $32, $60, $A0, $EF, $60, $EA
