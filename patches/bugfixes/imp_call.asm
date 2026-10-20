; Imp's Call v1.1 by Leet Sketcher
;
; An Esper summon cancelled by Imp no longer uses up the summon for the battle.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ImpCall-N.ips

hirom

assert read4($C202A7) == $1EC9B5A5, "unexpected ROM state"
org $C202A7
        db $20, $E1, $67, $EA

assert read4($C267E1) == $FFFFFFFF && read4($C267EE) == $FFFFFFFF, "unexpected ROM state"
org $C267E1
        db $A5, $B5, $C9, $19, $D0, $08, $BD, $18, $30, $1C, $2E, $3F, $A5, $B5, $C9, $1E
        db $60
