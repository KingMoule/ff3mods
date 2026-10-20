; Off Death Row v1.2 by Leet Sketcher
;
; Safety Bit and Memento Ring clear Condemned when they save the character
; instead of leaving the status active.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-OffDeathRow-N.ips

hirom

assert read1($C25B04) == $D0, "unexpected ROM state"
org $C25B04
        db $D5

assert read4($C25BB2) == $302F43AD && read4($C25BD1) == $45F02F45, "unexpected ROM state"
org $C25BB2
        db $08, $C2, $20, $AD, $42, $2F, $30, $5F, $20, $F9, $51, $7B, $3A, $8D, $42, $2F
        db $28, $BB, $80, $07, $EA, $5E, $E5, $3E, $1E, $E5, $3E, $A9, $0D, $85, $B8, $7B
        db $80, $23, $EA

assert read1($C25BDA) == $16, "unexpected ROM state"
org $C25BDA
        db $11

assert read4($C25BE3) == $33F02F45 && read4($C25BEC) == $D03A97AD, "unexpected ROM state"
org $C25BE3
        db $38, $3A, $F0, $33, $AD, $97, $3A, $D0, $2E, $AD, $45, $2F, $F0

assert read2($C25BF7) == $2AA9, "unexpected ROM state"
org $C25BF7
        db $69, $26
