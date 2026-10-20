; Shadow's Status v1.2 by Leet Sketcher
;
; Lasting statuses (Vanish, Float...) are removed from Shadow after the
; Floating Continent so he doesn't carry them to the Colosseum.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ShadowStatus-N.ips

hirom

assert read2($CA57E7) == $5806, "unexpected ROM state"
org $CA57E7
        db $A5, $59

assert read4($CA598F) == $7E4D00A1 && read4($CA59B7) == $96005EA9, "unexpected ROM state"
org $CA598F
        db $B2, $0B, $5A, $00, $A0, $80, $01, $9A, $59, $80, $FE, $B2, $0B, $5A, $00, $A0
        db $40, $01, $B7, $59, $80, $FE, $88, $03, $00, $40, $B2, $06, $58, $00, $FE, $FE
        db $FE, $FE, $FE, $FE, $FE, $FE, $FE, $FE, $B2, $0B, $5A, $00
