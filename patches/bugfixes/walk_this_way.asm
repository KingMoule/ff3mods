; Walk This Way v1.0 by Leet Sketcher
;
; Diagonal stairs run the normal per-step handling (poison damage, Tintinabar
; healing); Terra no longer walks an extra tile when Zone Eater's ceiling falls.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-WalkThisWay-N.ips

hirom

assert read4($C0496D) == $A94AEC20 && read4($C04973) == $078E9C57, "unexpected ROM state"
org $C0496D
        db $22, $3F, $4A, $C0, $AC, $03, $08, $4C, $03, $4B

assert read3($C049F6) == $08869C, "unexpected ROM state"
org $C049F6
        db $EA, $EA, $EA

assert read4($C04A15) == $868D01A9 && read4($C04A16) == $08868D01, "unexpected ROM state"
org $C04A15
        db $EA, $EA, $EA, $EA, $EA

assert read4($C04AEF) == $22D001C9 && read4($C04B5C) == $601ED98D, "unexpected ROM state"
org $C04AEF
        db $0A, $0A, $5A, $A8, $A9, $0F, $C2, $20, $0A, $88, $D0, $FC, $1C, $D8, $1E, $7A
        db $7B, $E2, $20, $60, $20, $77, $7E, $20, $08, $7E, $64, $85, $A9, $01, $8D, $86
        db $08, $20, $EC, $4A, $A9, $20, $1C, $B6, $1E, $A9, $80, $1C, $B7, $1E, $20, $A5
        db $C8, $4C, $33, $4A, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA
        db $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA
        db $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA
        db $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA
        db $EA
