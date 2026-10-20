; Dead in the Air v2.4 by Leet Sketcher
;
; A Condemned character whose timer runs out mid-Jump gets Wound instead of
; staying alive at 0 HP; items are restored after every battle ending; the
; Esper +30% HP/MP bonus is computed correctly.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-DeadInAir-N.ips

hirom

assert read4($C247F1) == $3A6EAD09 && read4($C248FE) == $2248EB48, "unexpected ROM state"
org $C247F1
        db $12, $20, $E6, $48, $AE, $6E, $3A, $7C, $99, $61, $A9, $FF, $8D, $05, $02, $A9
        db $10, $80, $1B, $AD, $D1, $1D, $29, $20, $D0, $14, $AD, $95, $3A, $D0, $DC, $AD
        db $74, $3A, $D0, $27, $AD, $8A, $3A, $CD, $8D, $3A, $D0, $0A, $A9, $80, $0C, $BC
        db $3E, $20, $03, $49, $80, $6D, $AD, $39, $3A, $D0, $CF, $AD, $97, $3A, $D0, $06
        db $A9, $29, $80, $02, $A9, $36, $20, $CA, $5F, $80, $58, $AD, $77, $3A, $D0, $AB
        db $AD, $E0, $3E, $D0, $03, $20, $76, $4A, $AE, $0B, $30, $30, $19, $A9, $01, $1C
        db $E4, $11, $F0, $12, $20, $5A, $4B, $C9, $A0, $B0, $0B, $AD, $BD, $3E, $29, $02
        db $0D, $76, $3A, $4A, $D0, $5C, $AE, $03, $30, $30, $25, $AD, $1F, $20, $D0, $20
        db $AD, $76, $3A, $4A, $F0, $1A, $BD, $E4, $3E, $89, $C2, $D0, $13, $20, $5A, $4B
        db $C9, $10, $B0, $0C, $A9, $08, $2C, $BD, $3E, $D0, $05, $2C, $DE, $1E, $D0, $0B
        db $20, $57, $5D, $20, $36, $49, $68, $68, $4C, $C5, $00, $1C, $DE, $1E, $20, $E3
        db $47, $C2, $10, $BC, $10, $30, $A9, $FF, $99, $1E, $16, $E2, $10, $3A, $20, $92
        db $07, $A9, $02, $0C, $49, $2F, $A2, $0B, $68, $68, $A9, $23, $20, $91, $4E, $4C
        db $19, $00, $BD, $18, $30, $20, $A7, $61, $A9, $04, $0C, $46, $3A, $20, $26, $49
        db $A2, $1B, $80, $E4, $AE, $0B, $30, $20, $E3, $47, $A9, $08, $1C, $DF, $1E, $20
        db $07, $4A, $4C, $22, $48, $A2, $06, $BD, $F4, $3B, $1D, $F5, $3B, $D0, $0C, $BD
        db $E4, $3E, $89, $82, $D0, $05, $09, $80, $9D, $E4, $3E, $CA, $CA, $10, $E8, $4C
        db $B9

assert read1($C25EB7) == $33, "unexpected ROM state"
org $C25EB7
        db $7B

assert read1($C260E1) == $14, "unexpected ROM state"
org $C260E1
        db $5E

assert read4($C260EE) == $FCAA0A05 && read4($C261B2) == $D880FCA5, "unexpected ROM state"
org $C260EE
        db $4F, $C9, $09, $B0, $32, $C9, $06, $F0, $28, $B0, $45, $C9, $03, $90, $02, $E9
        db $03, $AA, $BF, $96, $61, $C2, $48, $7B, $2A, $0A, $AA, $68, $EB, $B5, $FC, $20
        db $81, $47, $EB, $D0, $01, $1A, $18, $75, $FC, $95, $FC, $90, $23, $F6, $FD, $80
        db $1F, $7B, $AA, $A5, $FC, $80, $EF, $3A, $4A, $08, $5A, $C2, $21, $63, $01, $A8
        db $68, $28, $B9, $16, $16, $69, $01, $C9, $81, $90, $02, $A9, $80, $99, $16, $16
        db $FA, $7A, $C2, $21, $5A, $DA, $9B, $7B, $AA, $A9, $0F, $27, $20, $5D, $61, $E8
        db $E8, $C8, $C8, $C8, $C8, $A9, $E7, $03, $20, $5D, $61, $FA, $7A, $28, $60, $18
        db $48, $B9, $0B, $16, $48, $29, $00, $C0, $85, $EE, $68, $29, $FF, $3F, $75, $FC
        db $C3, $01, $90, $02, $A3, $01, $05, $EE, $99, $0B, $16, $68, $60, $5A, $A0, $35
        db $00, $B1, $F4, $C9, $80, $D0, $0C, $A9, $FF, $91, $F4, $8C, $35, $2F, $A9, $32
        db $20, $D4, $5F, $88, $10, $EB, $7A, $60, $1A, $4D, $80, $04, $48, $FB, $47, $D5
        db $48, $35, $48, $22, $48, $E0, $48, $22, $4A, $0C, $4E, $2F, $0C, $40, $3A, $60
        db $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA
