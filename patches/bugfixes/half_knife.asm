; Half Knife v1.1 by Leet Sketcher
;
; The Offering also halves the ValiantKnife's bonus damage.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-HalfKnife-N.ips

hirom

assert read4($C23F54) == $A20C60A9 && read4($C23F58) == $34149C11, "unexpected ROM state"
org $C23F54
        db $20, $FE, $40, $B9, $F4, $3B, $80, $41

assert read4($C23F62) == $C26011B0 && read4($C23F9B) == $6011B08D, "unexpected ROM state"
org $C23F62
        db $36, $3A, $60, $A9, $80, $0C, $A3, $11, $A9, $08, $0C, $A2, $11, $A9, $02, $0C
        db $A4, $11, $60, $A9, $01, $0C, $A4, $11, $A9, $20, $0C, $A2, $11, $60, $20, $7A
        db $3F, $C2, $20, $B9, $58, $3C, $4A, $08, $38, $B9, $1C, $3C, $F9, $F4, $3B, $28
        db $90, $02, $4A, $18, $6D, $B0, $11, $90, $5D, $7B, $3A, $80, $59

assert read3($C242EB) == $6E3F73, "unexpected ROM state"
org $C242EB
        db $6A, $3F, $65

assert read4($C242F5) == $3F9F3F89 && read4($C242F6) == $7E3F9F3F, "unexpected ROM state"
org $C242F5
        db $80, $3F, $9F, $3F, $75

assert read1($C24303) == $65, "unexpected ROM state"
org $C24303
        db $5C
