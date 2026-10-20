; Phoenix Chest v1.3 by Leet Sketcher
;
; The Phoenix Cave chest Locke opened no longer closes again for good.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-PhoenixChest-N.ips

hirom

assert read4($CC23E7) == $FA82D0C0 && read4($CC2437) == $0225CEB2, "unexpected ROM state"
org $CC23E7
        db $B0, $1F, $51, $9F, $05, $07, $B1, $C0, $D0, $02, $10, $24, $02, $B0, $02, $51
        db $3F, $07, $07, $B1, $B0, $03, $51, $3F, $06, $06, $B1, $B0, $04, $51, $3F, $05
        db $05, $B1, $B0, $18, $51, $9F, $60, $6F, $B1, $C0, $A8, $02, $1A, $24, $02, $B2
        db $70, $25, $02, $C0, $AA, $02, $2A, $24, $02, $B2, $FE, $25, $02, $C0, $2F, $02
        db $2E, $24, $02, $B2, $CE, $25, $02, $C0, $D7, $00, $B3, $5E, $00, $73, $06, $2F
        db $01, $01, $12, $FE
