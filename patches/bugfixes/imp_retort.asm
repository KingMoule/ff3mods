; Imp's Retort v1.5 by Leet Sketcher
;
; An Imp Cyan whose Retort fails no longer counters every physical attack for
; the rest of the battle; Retort is cleared after every Fight.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ImpRetort-N.ips

hirom

assert read1($C215CB) == $44, "unexpected ROM state"
org $C215CB
        db $4D

assert read4($C215D2) == $3EE5B93D && read4($C21662) == $FE0408A9, "unexpected ROM state"
org $C215D2
        db $3B, $C2, $20, $B9, $E4, $3E, $EB, $4A, $4A, $89, $89, $04, $E2, $20, $90, $2C
        db $D0, $2A, $A5, $B9, $F0, $26, $20, $5A, $4B, $29, $0F, $D0, $1F, $B9, $18, $30
        db $0C, $2F, $3F, $D0, $17, $B9, $D8, $3E, $C9, $0B, $90, $05, $C9, $0C, $D0, $0C
        db $3A, $09, $F0, $85, $B6, $A9, $10, $14, $B0, $4C, $14, $17, $C0, $08, $B0, $07
        db $B9, $D8, $3E, $C9, $0D, $F0, $28, $BB, $BD, $58, $3C, $4A, $A9, $01, $90, $02
        db $A9, $07, $8D, $70, $3A, $20, $4D, $5A, $20, $65, $38, $A9, $02, $14, $B2, $A5
        db $B5, $8D, $13, $34, $D0, $06, $5E, $4C, $3E, $1E, $4C, $3E, $4C, $7B, $31, $64
        db $FE, $A2, $02, $B9, $18, $30, $4D, $74, $3A, $D0, $01, $CA, $8A, $18, $69, $C4
        db $D9, $D0, $3C, $F0, $05, $D9, $D1, $3C, $D0, $07, $8A, $49, $03, $0A, $0A, $04
        db $FE, $CA, $D0, $E8

assert read1($C2167C) == $1B, "unexpected ROM state"
org $C2167C
        db $19

assert read1($C219D3) == $10, "unexpected ROM state"
org $C219D3
        db $0E
