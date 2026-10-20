; Anonymous Attack v1.3 by Leet Sketcher
;
; Kefka's special attack during the Sealed Gate stall is loaded at battle
; start (it always missed and showed a blank name).
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-AnonymousAttack-N1.ips

hirom

assert read4($C1C030) == $6A2E9E03 && read4($C1C03D) == $618A9C62, "unexpected ROM state"
org $C1C030
        db $06, $9C, $8A, $61, $9E, $2E, $6A, $68, $DA, $AA, $BF, $48, $B7, $C1, $8D, $6E
        db $62

assert read2($C2303F) == $2D71, "unexpected ROM state"
org $C2303F
        db $AB, $F7

assert read1($C2E8FE) == $A8, "unexpected ROM state"
org $C2E8FE
        db $A1

assert read4($C2F79F) == $0E8D02A9 && read4($C2F7C9) == $7B0F8D7B, "unexpected ROM state"
org $C2F79F
        db $80, $6F, $20, $22, $FA, $20, $D1, $F7, $9C, $1B, $96, $60, $C2, $20, $99, $A8
        db $33, $DA, $20, $71, $2D, $48, $0A, $0A, $0A, $0A, $0A, $AA, $E2, $20, $BF, $1F
        db $00, $CF, $99, $2D, $32, $FA, $BF, $C0, $37, $CF, $99, $81, $3C, $FA
