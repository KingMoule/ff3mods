; Imp's Rage v1.1 by Leet Sketcher
;
; Rage and Dance can no longer be used while the character is an Imp.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ImpRage-N.ips

hirom

assert read4($C245AD) == $469C2013 && read4($C245E5) == $08B008C0, "unexpected ROM state"
org $C245AD
        db $14, $20, $9C, $46, $80, $0C, $18, $B9, $18, $30, $0C, $53, $2F, $90, $06, $1C
        db $53, $2F, $B9, $18, $30, $29, $FF, $00, $0C, $4A, $3A, $60, $60, $18, $B9, $19
        db $30, $29, $FF, $00, $0C, $44, $2F, $90, $03, $1C, $44, $2F, $60, $A9, $88, $00
        db $20, $4C, $46, $C0, $08, $B0, $0D, $A9, $01, $01, $04, $F6

assert read3($C246B8) == $DF45CB, "unexpected ROM state"
org $C246B8
        db $CA, $45, $DA

assert read3($C246F8) == $DF45D5, "unexpected ROM state"
org $C246F8
        db $CB, $45, $DA

assert read1($C2470A) == $BB, "unexpected ROM state"
org $C2470A
        db $B4

assert read1($C24720) == $E5, "unexpected ROM state"
org $C24720
        db $E0
