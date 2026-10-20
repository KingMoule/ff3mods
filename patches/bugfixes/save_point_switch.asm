; Save Point Switch v1.2 by Leet Sketcher
;
; In Phoenix Cave and Kefka's Tower, switching to a party that isn't on a
; Save Point no longer lets it save or use Tents and Sleeping Bags.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-SavePoint-N.ips

hirom

assert read4($C06D2C) == $0084AD49 && read4($C06D33) == $3FD0055E, "unexpected ROM state"
org $C06D2C
        db $F8, $AD, $84, $00, $D0, $F3, $AD, $5E, $05, $D0, $EE

assert read1($C06D3D) == $38, "unexpected ROM state"
org $C06D3D
        db $E7

assert read1($C06D43) == $32, "unexpected ROM state"
org $C06D43
        db $E1

assert read1($C06D4B) == $2A, "unexpected ROM state"
org $C06D4B
        db $D9

assert read4($C06D52) == $086CB923 && read4($C06D54) == $1ED0086C, "unexpected ROM state"
org $C06D52
        db $D2, $B9, $6C, $08, $D0, $CD

assert read1($C06D5E) == $17, "unexpected ROM state"
org $C06D5E
        db $C6

assert read4($C06D6B) == $0762AD0A && read4($C06D73) == $60018007, "unexpected ROM state"
org $C06D6B
        db $B9, $AD, $62, $07, $F0, $B4, $9C, $62, $07, $20, $1D, $4A
