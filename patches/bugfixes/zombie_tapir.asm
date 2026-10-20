; Zombie/Tapir v1.2, fix A by Leet Sketcher
;
; Tapir curing Zombie heals 1/8 of max HP instead of leaving the character
; alive at 0 HP.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ZombieTapirA-N.ips

hirom

assert read2($C23DFB) == $3CA2, "unexpected ROM state"
org $C23DFB
        db $5D, $67

assert read4($C2675D) == $FFFFFFFF && read4($C2676E) == $FFFFFFFF, "unexpected ROM state"
org $C2675D
        db $C2, $20, $B9, $F4, $3B, $D0, $09, $B9, $1C, $3C, $4A, $4A, $4A, $99, $E4, $33
        db $E2, $20, $4C, $A2, $3C
