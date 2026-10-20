; Smoke and Mirrors v1.0 by Leet Sketcher
;
; A Muddled character's Smoke Bomb no longer removes the monsters (which won
; the battle) instead of the party.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-SmokeMirrors-N.ips

hirom

assert read4($C25938) == $08E07BB9 && read4($C2598B) == $0AB8A5B8, "unexpected ROM state"
org $C25938
        db $B8, $E0, $08, $26, $B9, $A5, $BA, $89, $10, $D0, $2C, $BD, $95, $33, $30, $02
        db $E6, $B9, $BD, $18, $30, $2C, $40, $3A, $F0, $02, $E6, $B9, $A5, $BB, $0A, $10
        db $02, $E6, $B9, $29, $18, $C9, $08, $F0, $05, $BD, $E4, $3E, $4A, $4A, $66, $B8
        db $BD, $E5, $3E, $29, $20, $F0, $10, $AD, $7A, $3A, $C9, $01, $D0, $07, $AD, $7B
        db $3A, $C9, $FC, $F0, $02, $E6, $B9, $46, $B9, $A5, $B8, $64, $B9, $80, $08, $EA
        db $EA, $EA, $EA, $EA, $EA, $EA, $EA
