; Item/Magic Counter v1.2 (Dead Hare compatible version) by Leet Sketcher
;
; Monsters that counter one specific spell or item (SrBehemoth, FlameEater...)
; no longer keep countering every attack after being hit by it.
; Requires dead_hare.asm first.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ItemMagicCounter-ND.ips

hirom

assert read4($C21B9A) == $4C4EAD20 && read4($C21BB3) == $1AB44C4E, "unexpected ROM state"
org $C21B9A
        db $80, $EC, $BB, $AD, $2D, $3A, $EB, $A9, $2B, $C2, $20, $8D, $7A, $3A, $AD, $2E
        db $3A, $85, $B8, $80, $D9, $A9, $FF, $9D, $48, $3D, $60, $EA, $EA

assert read1($C21BDB) == $49, "unexpected ROM state"
org $C21BDB
        db $48

assert read4($C21C1A) == $F0FCA518 && read4($C21C51) == $601802F0, "unexpected ROM state"
org $C21C1A
        db $A5, $FC, $F0, $32, $20, $2A, $52, $85, $FC, $38, $60, $20, $D7, $1B, $80, $75
        db $20, $34, $1D, $90, $08, $B9, $E0, $3B, $2C, $2F, $3A, $F0, $19, $60, $98, $69
        db $13, $A8, $C8, $BB, $20, $3A, $5A, $30, $0D, $BD, $48, $3D, $CD, $2E, $3A, $F0
        db $07, $CD, $2F, $3A, $F0, $02, $18, $60, $20, $AF, $1B

assert read4($C21D57) == $1C3F1C40 && read4($C21D58) == $3B1C3F1C, "unexpected ROM state"
org $C21D57
        db $3D, $1C, $3C, $1C, $38

assert read1($C21D67) == $26, "unexpected ROM state"
org $C21D67
        db $25

assert read1($C21D89) == $2C, "unexpected ROM state"
org $C21D89
        db $2A

assert read1($C21DA3) == $A0, "unexpected ROM state"
org $C21DA3
        db $9C
