; Chance Offering v1.0 by Leet Sketcher
;
; The Offering halves Dice/Fixed Dice damage like other weapons.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ChanceOffering-N.ips

hirom

assert read4($C241BE) == $0A11AFAD, "unexpected ROM state"
org $C241BE
        db $20, $F5, $67, $EA

assert read4($C267F5) == $FFFFFFFF && read4($C267FC) == $FFFFFFFF, "unexpected ROM state"
org $C267F5
        db $B9, $58, $3C, $4A, $AD, $AF, $11, $B0, $01, $0A, $60
