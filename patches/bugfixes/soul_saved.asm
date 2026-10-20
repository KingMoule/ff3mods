; Soul Saved v1.4, fix A by Leet Sketcher
;
; Soul Savers are immune to instant death, so X-Zone can no longer end the
; Wrexsoul battle early.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-SoulSavedA-N.ips

hirom

assert read1($CF2CF4) == $24, "unexpected ROM state"
org $CF2CF4
        db $A4
