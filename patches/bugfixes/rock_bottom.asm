; Rock Bottom v1.3 by Leet Sketcher
;
; Near Fatal is applied again when Petrify is cured on a character under 1/8
; of max HP.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-RockBottom-N.ips

hirom

assert read4($C245F5) == $204000A9 && read4($C245F7) == $46562040, "unexpected ROM state"
org $C245F5
        db $20, $53, $46, $20, $39, $5B

assert read1($C25A8E) == $52, "unexpected ROM state"
org $C25A8E
        db $60

assert read1($C25A96) == $52, "unexpected ROM state"
org $C25A96
        db $57

assert read1($C25AA2) == $46, "unexpected ROM state"
org $C25AA2
        db $4B

assert read1($C25AAC) == $3C, "unexpected ROM state"
org $C25AAC
        db $41

assert read1($C25AB7) == $31, "unexpected ROM state"
org $C25AB7
        db $36

assert read4($C25AD9) == $0A07299B && read4($C25AFF) == $E95AE95A, "unexpected ROM state"
org $C25AD9
        db $4A, $B0, $12, $4A, $B0, $04, $A9, $08, $80, $05, $4A, $B0, $08, $A9, $10, $1D
        db $4C, $3E, $9D, $4C, $3E, $60, $E9, $0A, $0A, $AA, $7C, $FA, $5A, $EA, $EA, $EA
        db $EA, $B2, $5B, $FC, $5B, $EE, $5A, $EE, $5A, $EE

assert read4($C25B08) == $F03F0CBD && read4($C25B4A) == $3E4C9D08, "unexpected ROM state"
org $C25B08
        db $A9, $02, $DA, $BC, $0C, $3F, $F0, $07, $DE, $0C, $3F, $D0, $02, $04, $B8, $0A
        db $E8, $C9, $08, $90, $EE, $FA, $BC, $F9, $3C, $F0, $07, $DE, $F9, $3C, $D0, $02
        db $04, $B8, $A5, $B8, $F0, $C0, $A9, $29, $4C, $91, $4E, $EA, $EA, $EA, $EA, $EA
        db $EA, $B9, $1C, $3C, $4A, $4A, $4A, $D9, $F4, $3B, $90, $0A, $A9, $00, $02, $39
        db $1C, $33, $04, $F8, $14, $F4
