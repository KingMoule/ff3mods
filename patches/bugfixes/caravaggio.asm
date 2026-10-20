; Caravaggio v1.3 by Leet Sketcher
;
; Roulette used through Sketch or Rage shows its targeting pointer and can
; target the whole field again.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-Caravaggio-N.ips

hirom

assert read4($C21529) == $2011A98D && read4($C21555) == $1DBF20B6, "unexpected ROM state"
org $C21529
        db $20, $F0, $17, $AC, $17, $34, $30, $ED, $8E, $17, $34, $B9, $81, $3C, $9D, $81
        db $3C, $B9, $2D, $32, $9D, $2D, $32, $9C, $15, $34, $AD, $00, $34, $85, $B6, $A9
        db $FF, $8D, $00, $34, $A9, $01, $04, $B2, $A5, $B6, $20, $BF, $1D, $20, $B9, $03

assert read1($C2158C) == $54, "unexpected ROM state"
org $C2158C
        db $51

assert read1($C21985) == $54, "unexpected ROM state"
org $C21985
        db $51

assert read4($C2198C) == $11A98DA6 && read4($C21995) == $A40C20A9, "unexpected ROM state"
org $C2198C
        db $20, $0C, $A4, $11, $A9, $A6, $8D, $A9, $11, $A9, $01, $1C, $A2

assert read4($C219A2) == $11A98DA8 && read4($C219AE) == $317B4CBB, "unexpected ROM state"
org $C219A2
        db $40, $85, $BB, $A9, $A8, $80, $E9, $EA, $EA, $EA, $EA, $EA, $A9, $01, $14, $B3

assert read1($C21A03) == $B2, "unexpected ROM state"
org $C21A03
        db $AE

assert read4($C231D4) == $04303415 && read4($C231F1) == $3A7CADAA, "unexpected ROM state"
org $C231D4
        db $7C, $3A, $48, $A5, $B3, $4A, $B0, $06, $A9, $1E, $83, $01, $80, $09, $AD, $15
        db $34, $30, $04, $A9, $40, $04, $BA, $20, $66, $36, $AD, $17, $34, $30, $01, $AA
        db $68
