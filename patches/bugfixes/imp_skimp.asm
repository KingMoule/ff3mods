; Imp Skimp v1.4 by Leet Sketcher
;
; The Imp sprite follows the Imp status instead of the Imp spell (a missed
; Imp no longer turns the target, a Runic-absorbed Imp no longer flashes Celes).
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ImpSkimp-N1.ips

hirom

assert read2($C11116) == $2579, "unexpected ROM state"
org $C11116
        db $18, $D7

assert read4($C12F7C) == $0A0A0A0A && read4($C13048) == $7B78EE20, "unexpected ROM state"
org $C12F7C
        db $4A, $6A, $6A, $6A, $AA, $BD, $CD, $61, $F0, $03, $4C, $17, $30, $1A, $9D, $CE
        db $61, $2D, $4B, $2F, $D0, $16, $BD, $C0, $2E, $29, $08, $F0, $04, $A9, $12, $80
        db $0E, $BD, $BD, $2E, $29, $20, $F0, $04, $A9, $0F, $80, $03, $BD, $AE, $2E, $D9
        db $6C, $7B, $F0, $0A, $99, $6C, $7B, $20, $54, $31, $7B, $99, $70, $7B, $AD, $4B
        db $2F, $4A, $B0, $1E, $BD, $BD, $2E, $29, $10, $F0, $17, $B9, $70, $7B, $D0, $31
        db $AD, $6A, $7B, $D0, $2C, $EE, $6A, $7B, $20, $4D, $30, $20, $03, $31, $A9, $01
        db $80, $17, $B9, $70, $7B, $F0, $1A, $AD, $6A, $7B, $D0, $15, $EE, $6A, $7B, $20
        db $4D, $30, $B9, $6C, $7B, $20, $54, $31, $7B, $99, $70, $7B, $A9, $1E, $9D, $CD
        db $61, $9E, $CE, $61, $20, $6E, $30, $20, $21, $2F, $C2, $20, $BD, $BD, $2E, $9D
        db $C1, $2E, $BD, $BF, $2E, $9D, $C3, $2E, $7B, $E2, $20, $EE, $78, $7B, $60, $F4
        db $BD, $25, $7B, $AA, $A8, $5E, $C2, $62, $90, $01, $C8, $1E, $C2, $62, $E8, $E0
        db $06, $00, $D0, $F1, $98, $F0, $03, $4C, $79, $25, $4C, $5A, $32, $BD, $EC, $3E
        db $29, $20, $59, $C2, $62, $4A, $F0, $08, $0A, $59, $C2, $62, $1A, $99, $C2, $62

assert read4($C13244) == $CF37BFAA && read4($C13263) == $64BBEE20, "unexpected ROM state"
org $C13244
        db $69, $37, $CF, $AA, $A0, $C4, $64, $A9, $07, $00, $8B, $54, $7E, $C2, $AB, $7B
        db $E2, $20, $EE, $BB, $64, $60, $FA, $E0, $BD, $25, $F0, $01, $DA, $60, $1A, $0C
        db $C2, $62, $60

assert read2($C191D2) == $2579, "unexpected ROM state"
org $C191D2
        db $18, $D7

assert read2($C19367) == $2579, "unexpected ROM state"
org $C19367
        db $18, $D7

assert read2($C193C3) == $2579, "unexpected ROM state"
org $C193C3
        db $18, $D7

assert read4($C1C8A8) == $D724D73B && read4($C1C8A9) == $31D724D7, "unexpected ROM state"
org $C1C8A8
        db $3C, $D7, $2C, $D7, $39

assert read4($C1D6E5) == $306A39BD && read4($C1D74B) == $20E27B6A, "unexpected ROM state"
org $C1D6E5
        db $20, $EE, $D6, $CA, $20, $EE, $D6, $E8, $60, $BD, $39, $6A, $DA, $30, $17, $29
        db $03, $8D, $78, $7B, $0A, $A8, $0A, $0A, $0A, $0A, $AA, $B9, $E4, $3E, $9D, $BD
        db $2E, $20, $76, $2F, $FA, $60, $69, $7C, $A8, $0A, $AA, $20, $39, $30, $20, $1B
        db $30, $FA, $60, $7B, $AA, $A8, $20, $62, $32, $20, $39, $30, $E8, $E8, $C8, $C0
        db $06, $00, $D0, $F5, $4C, $1E, $30, $20, $5B, $18, $AE, $F6, $7A, $9D, $D8, $74
        db $9E, $D9, $74, $60, $7B, $80, $F3, $C2, $20, $AE, $F6, $7A, $BD, $82, $6F, $9D
        db $3A, $6A, $BD, $84, $6F, $9D, $3C, $6A, $80, $23

assert read4($D01F51) == $8C00078B, "unexpected ROM state"
org $D01F51
        db $FA, $7A, $1F, $FF

assert read4($D01F6C) == $78BF1F78 && read4($D01FA4) == $3F833F83, "unexpected ROM state"
org $D01F6C
        db $8C, $1F, $BF, $8C, $1F, $BF, $8C, $1F, $BF, $8C, $1F, $80, $13, $FF, $8B, $07
        db $00, $8C, $80, $13, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF
        db $E9, $1F, $00, $8B, $03, $80, $65, $00, $80, $65, $00, $8C, $89, $09, $83, $CF
        db $80, $65, $03, $80, $65, $03, $8A, $89, $04, $83, $3F, $8A

assert read3($D03433) == $FF03AD, "unexpected ROM state"
org $D03433
        db $FA, $0D, $5F

assert read4($D05F02) == $2C890A72 && read4($D05F15) == $8A00A7FF, "unexpected ROM state"
org $D05F02
        db $13, $89, $2C, $A6, $00, $00, $FF, $A7, $00, $8A, $FF, $AD, $03, $80, $13, $FF
        db $D1, $00, $80, $13, $FF, $FF, $FF

assert read3($D0790C) == $FF00D1, "unexpected ROM state"
org $D0790C
        db $FA, $12, $5F
