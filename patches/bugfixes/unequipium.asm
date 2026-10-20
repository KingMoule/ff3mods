; Unequipium v1.1 by Leet Sketcher
;
; Events that remove gear from characters outside the party now refresh their
; stats, so HP/MP no longer display wrong after swapping members.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-Unequipium-N.ips

hirom

assert read1($C09958) == $3A, "unexpected ROM state"
org $C09958
        db $3F

assert read4($C0A035) == $5C4C02A9 && read4($C0A078) == $9B5C4C03, "unexpected ROM state"
org $C0A035
        db $A5, $EB, $22, $06, $00, $C2, $A9, $02, $80, $2B, $20, $AD, $9D, $A5, $EC, $48
        db $8D, $02, $42, $A9, $06, $8D, $03, $42, $85, $EC, $EA, $EA, $AE, $16, $42, $DA
        db $5A, $BF, $C0, $78, $C4, $99, $02, $16, $E8, $C8, $C6, $EC, $D0, $F3, $7A, $FA
        db $68, $85, $EC, $A9, $03, $4C, $5C, $9B, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA
        db $EA, $EA, $EA, $EA, $EA, $EA, $EA
