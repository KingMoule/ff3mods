; Throwback v1.1 by Leet Sketcher
;
; Shadow steps forward and throws normally when his target has Jumped.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-Throwback-N1.ips

hirom

assert read1($C1B782) == $C2, "unexpected ROM state"
org $C1B782
        db $BB

assert read1($C1B78C) == $E5, "unexpected ROM state"
org $C1B78C
        db $EF

assert read1($C1B79E) == $F4, "unexpected ROM state"
org $C1B79E
        db $FA

assert read1($C1B99E) == $22, "unexpected ROM state"
org $C1B99E
        db $F0

assert read1($C1B9A5) == $1B, "unexpected ROM state"
org $C1B9A5
        db $E9

assert read4($C1B9B7) == $9CB02009 && read4($C1BA20) == $BBDE4C0A, "unexpected ROM state"
org $C1B9B7
        db $D7, $4C, $7C, $BC, $20, $32, $BC, $A0, $02, $00, $B1, $76, $1A, $AA, $BF, $40
        db $00, $D1, $10, $0A, $7B, $91, $76, $8A, $C8, $91, $76, $4C, $CA, $BE, $E0, $AB
        db $00, $B0, $0E, $48, $5A, $20, $3E, $B9, $7A, $68, $90, $E8, $48, $20, $32, $BC
        db $68, $29, $0F, $18, $69, $14, $80, $6A, $EE, $BB, $EC, $20, $32, $BC, $A9, $25
        db $4C, $58, $BB, $B2, $78, $29, $02, $8D, $10, $EC, $20, $9F, $9A, $B2, $78, $0A
        db $A0, $02, $00, $90, $02, $C8, $C8, $B1, $78, $C8, $11, $78, $F0, $06, $90, $0D
        db $A9, $09, $80, $3E, $A9, $0A, $69, $00, $80, $38, $EA, $EA, $60
