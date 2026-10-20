; Shadow Copy v1.1 by Leet Sketcher
;
; Gogo's Mimic can no longer copy Shadow's actions when Shadow is fought in
; the Dragon's Neck Colosseum.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ShadowCopy-N.ips

hirom

assert read4($C20220) == $40B008E0 && read4($C20262) == $FA283F26, "unexpected ROM state"
org $C20220
        db $BD, $18, $30, $F0, $37, $2C, $40, $3A, $D0, $32, $5A, $AC, $7C, $3A, $C0, $1E
        db $B0, $29, $98, $0A, $AA, $BF, $00, $FE, $CF, $89, $02, $F0, $1E, $A2, $12, $8E
        db $28, $3F, $8E, $24, $3F, $A2, $00, $C0, $17, $D0, $02, $A2, $04, $C2, $20, $AD
        db $7C, $3A, $9D, $20, $3F, $AD, $30, $3A, $9D, $22, $3F, $7A, $28, $FA, $60, $EA
        db $EA, $EA, $EA, $EA, $EA, $EA
