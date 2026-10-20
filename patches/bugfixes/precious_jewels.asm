; Precious Jewels v1.0 by Leet Sketcher
;
; Standing next to the Gem Box at the top of the Fanatics' Tower without
; taking it no longer triggers the cultists' ambush.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-PreciousJewels-N.ips

hirom

assert read1($C05314) == $C1, "unexpected ROM state"
org $C05314
        db $B3

assert read2($C09A52) == $B91A, "unexpected ROM state"
org $C09A52
        db $BE, $BA

assert read4($C0BA96) == $B6AD0A10 && read4($C0BAA7) == $601EB68D, "unexpected ROM state"
org $C0BA96
        db $0A, $A9, $10, $90, $04, $0C, $B6, $1E, $60, $1C, $B6, $1E, $60, $20, $ED, $BA
        db $B9, $40, $1E, $80, $0E

assert read4($C0BAB1) == $C0BAFC3F && read4($C0BAE8) == $C0BAFC3F, "unexpected ROM state"
org $C0BAB1
        db $80, $06, $20, $ED, $BA, $B9, $E0, $1E, $3F, $FC, $BA, $C0, $60, $C2, $20, $A5
        db $EB, $30, $0D, $E2, $20, $20, $A3, $BA, $F0, $10, $A0, $06, $00, $4C, $FF, $B2
        db $29, $FF, $7F, $E2, $20, $20, $A3, $BA, $F0, $F0, $A0, $03, $00, $4C, $14, $B3
        db $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA

assert read3($C416F3) == $544008, "unexpected ROM state"
org $C416F3
        db $0B, $B4, $FF

assert read4($CCFFB4) == $FFFFFFFF && read4($CCFFB7) == $FFFFFFFF, "unexpected ROM state"
org $CCFFB4
        db $FC, $B8, $80, $40, $54, $02, $FE
