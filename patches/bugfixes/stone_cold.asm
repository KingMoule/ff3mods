; Stone Cold v1.2 by Leet Sketcher
;
; Petrify no longer blocks Revivify's healing, so a Petrified Zombie no longer
; ends up at 0 HP once Petrify is cured.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-StoneCold-N.ips

hirom

assert read4($C20B84) == $A6AD20E2 && read4($C20C1A) == $F126F006, "unexpected ROM state"
org $C20B84
        db $DA, $E2, $20, $AD, $A6, $11, $D0, $03, $FA, $28, $60, $AD, $A4, $11, $30, $05
        db $20, $9E, $0C, $80, $03, $20, $87, $0D, $64, $F2, $B9, $FC, $3D, $39, $E4, $3E
        db $89, $02, $D0, $06, $B9, $E4, $3E, $0A, $30, $50, $AD, $A4, $11, $85, $F2, $AD
        db $A2, $11, $89, $08, $F0, $1F, $B9, $95, $3C, $10, $0D, $AD, $AA, $11, $89, $82
        db $D0, $C6, $64, $F2, $A9, $02, $80, $05, $B9, $E4, $3E, $29, $02, $2D, $A4, $11
        db $4A, $45, $F2, $85, $F2, $AD, $A1, $11, $F0, $3F, $AD, $C8, $3E, $49, $FF, $2D
        db $A1, $11, $F0, $16, $BB, $AD, $A1, $11, $3C, $CC, $3B, $F0, $08, $A5, $F2, $49
        db $01, $85, $F2, $80, $24, $3C, $CD, $3B, $F0, $07, $64, $F0, $64, $F1, $FA, $80
        db $19, $3C, $E1, $3B, $F0, $06, $46, $F1, $66, $F0, $80, $0D, $3C, $E0, $3B, $F0
        db $08, $A5, $F1, $30, $04, $06, $F0, $26, $F1, $FA
