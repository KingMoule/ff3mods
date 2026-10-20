; Bland Entrance v1.2 by Leet Sketcher
;
; Fixes several problems in the opening events of the game.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-BlandEntrance-N.ips

hirom

assert read1($C403ED) == $1A, "unexpected ROM state"
org $C403ED
        db $1D

assert read4($CC9A7E) == $FFCC8200 && read4($CC9AD0) == $C1D20F36, "unexpected ROM state"
org $CC9A7E
        db $44, $00, $C0, $44, $0E, $C0, $44, $0F, $C0, $84, $B8, $0B, $39, $59, $04, $00
        db $02, $9C, $FF, $0F, $04, $94, $81, $80, $FF, $0E, $88, $88, $CF, $E0, $0A, $88
        db $81, $CC, $FF, $0F, $84, $E0, $08, $CF, $FF, $4B, $0B, $00, $78, $0E, $78, $0F
        db $0E, $82, $80, $FF, $0E, $03, $88, $D1, $FF, $0F, $84, $87, $88, $D1, $FF, $45
        db $00, $82, $80, $FF, $36, $0E, $36, $0F, $D2, $C1, $FE, $00, $83, $CE, $D7, $FF
        db $FE, $0E, $03, $84, $D1, $FF

assert read4($CC9B21) == $FFD78200, "unexpected ROM state"
org $CC9B21
        db $B2, $C9, $9A, $02

assert read4($CC9B57) == $D184030E && read4($CC9B5F) == $00FFD180, "unexpected ROM state"
org $CC9B57
        db $B2, $CF, $9A, $02, $0F, $84, $87, $80, $D1, $FF, $47, $31

assert read4($CC9B77) == $113D103D, "unexpected ROM state"
org $CC9B77
        db $B2, $A8, $9D, $02

assert read4($CC9C0E) == $113D103D && read4($CC9C2D) == $CE142DD5, "unexpected ROM state"
org $CC9C0E
        db $31, $82, $88, $FF, $3D, $10, $3D, $11, $3D, $12, $3D, $13, $10, $84, $D5, $2C
        db $13, $FF, $11, $84, $D5, $2D, $13, $FF, $12, $84, $D5, $2C, $14, $FF, $13, $84
        db $D5, $2D, $14

assert read4($CC9D97) == $B3812BC0 && read4($CC9DAE) == $FFCC8183, "unexpected ROM state"
org $CC9D97
        db $FE, $45, $36, $0E, $36, $0F, $FE, $45, $36, $00, $36, $0F, $FE, $FE, $FE, $FE
        db $FE, $31, $82, $CC, $FF, $3D, $10, $3D, $11, $FE, $FE

assert read4($CC9E1B) == $360E3645 && read4($CC9E1C) == $0F360E36, "unexpected ROM state"
org $CC9E1B
        db $47, $B2, $98, $9D, $02

assert read4($CC9EDD) == $36003645 && read4($CC9EDE) == $0F360036, "unexpected ROM state"
org $CC9EDD
        db $47, $B2, $9E, $9D, $02
