; Menu Malarky v1.3 by Leet Sketcher
;
; Timing tricks with the Main Menu can no longer skip events: Locke passing
; the South Figaro guard (missing Celes), Inferno and Poltergeist in Kefka's
; Tower. Applied after save_point_switch.asm as the author requires.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-MenuMalarky-N.ips

hirom

assert read2($C05264) == $7CE1, "unexpected ROM state"
org $C05264
        db $DB, $87

assert read4($C06D48) == $D9D00869 && read4($C06D5B) == $C6D00F29, "unexpected ROM state"
org $C06D48
        db $6A, $08, $19, $6D, $08, $29, $0F, $19, $69, $08, $19, $6C, $08, $05, $59, $05
        db $4A, $D0, $CA, $EA, $EA, $EA, $EA

assert read4($C087D1) == $9C21809C && read4($C0882E) == $6021809C, "unexpected ROM state"
org $C087D1
        db $A2, $20, $00, $9C, $80, $21, $CA, $D0, $FA, $60, $B9, $7E, $08, $20, $03, $7D
        db $B9, $6A, $08, $19, $6D, $08, $29, $0F, $19, $69, $08, $19, $6C, $08, $F0, $2B
        db $B9, $7E, $08, $C9, $05, $B0, $24, $89, $02, $D0, $12, $C2, $20, $B9, $7A, $08
        db $AA, $0A, $38, $E5, $1E, $99, $7A, $08, $86, $1E, $7B, $E2, $20, $A6, $1E, $BF
        db $00, $20, $7E, $10, $06, $A5, $1B, $9F, $00, $20, $7E, $60, $EA, $EA, $EA, $EA
        db $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA
        db $EA
