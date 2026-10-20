; Status Unknown v1.1 by Leet Sketcher
;
; Statuses with no outline color no longer display blank and hide other
; statuses such as Life 3 or Float.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-StatusUnknown-N1.ips

hirom

assert read4($C14589) == $A2EB11F0 && read4($C145BB) == $186038AA, "unexpected ROM state"
org $C14589
        db $EB, $85, $48, $BD, $BF, $2E, $EB, $85, $4A, $7B, $AA, $A8, $06, $4A, $26, $48
        db $90, $07, $BF, $E1, $AD, $C2, $1A, $D0, $0C, $8A, $18, $69, $0A, $00, $AA, $C8
        db $C0, $1F, $00, $D0, $E7, $98, $E2, $20, $60, $60, $AA, $BD, $D6, $64, $0A, $08
        db $0A, $0A, $0A, $0A, $28, $AA

assert read3($C145C7) == $9045B0, "unexpected ROM state"
org $C145C7
        db $B3, $45, $B0

assert read3($C145D4) == $9045B0, "unexpected ROM state"
org $C145D4
        db $B3, $45, $B0

assert read3($C145E1) == $9045B0, "unexpected ROM state"
org $C145E1
        db $B3, $45, $B0

assert read3($C145EE) == $9045B0, "unexpected ROM state"
org $C145EE
        db $B3, $45, $B0
