; Chain of Command v1.3 by Leet Sketcher
;
; Gogo's command names changed by relics (Slot -> GP Rain...) also show in
; his Status menu command selection.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ChainOfCommand-N.ips

hirom

assert read4($C35EC1) == $C27A5ED7 && read4($C35EDA) == $2E306835, "unexpected ROM state"
org $C35EC1
        db $D4, $5E, $C2, $21, $68, $69, $80, $00, $A8, $E2, $20, $FA, $E8, $E4, $E5, $D0
        db $E8, $80, $7C, $48, $20, $19, $35, $68, $30, $31, $20, $72, $61
