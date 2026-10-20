; Off the Hook v1.3 by Leet Sketcher
;
; A party member can no longer end up above the hook near the Phoenix Cave
; entrance.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-OffTheHook-N.ips

hirom

assert read4($CC20EE) == $DCC28631 && read4($CC2105) == $FFC68231, "unexpected ROM state"
org $CC20EE
        db $10, $81, $FF, $31, $86, $C2, $DC, $A3, $C7, $0F, $FF, $92, $10, $03, $C1, $98
        db $FF, $31, $86, $C1, $98, $E0, $04, $C6, $FF, $97, $5C
