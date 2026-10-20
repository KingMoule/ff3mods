; Multiple Events Fix v1.10 by Leet Sketcher
;
; Fixes ten events that are wrong in different ways (see Leet Sketcher's
; readme for the list).
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-MultipleEvents-N.ips

hirom

assert read1($CA00EA) == $96, "unexpected ROM state"
org $CA00EA
        db $47

assert read4($CAF870) == $E010E006 && read4($CAF898) == $49FFCD08, "unexpected ROM state"
org $CAF870
        db $04, $E0, $38, $CF, $FF, $01, $04, $E0, $48, $CD, $FF, $10, $90, $E0, $10, $80
        db $E0, $04, $80, $E0, $04, $84, $E0, $04, $80, $E0, $04, $CF, $FF, $00, $88, $20
        db $E0, $18, $CE, $E0, $08, $CD, $FF, $49, $B2, $BD, $CF, $00

assert read4($CB3B63) == $8806B594 && read4($CB3BDB) == $03B5FFCE, "unexpected ROM state"
org $CB3B63
        db $B5, $0A, $88, $0F, $F7, $FF, $8B, $0F, $7F, $8C, $0F, $7F, $4D, $7A, $FF, $B2
        db $A9, $5E, $00, $F4, $C7, $3E, $0F, $3E, $16, $3E, $17, $3E, $18, $45, $42, $16
        db $42, $17, $42, $18, $3F, $00, $01, $3C, $00, $FF, $FF, $FF, $F3, $20, $37, $00
        db $00, $43, $00, $02, $B2, $80, $39, $01, $00, $05, $D5, $08, $11, $28, $FF, $32
        db $02, $28, $FF, $33, $02, $28, $FF, $34, $02, $28, $FF, $30, $83, $C3, $96, $FF
        db $B0, $1F, $51, $9F, $88, $8F, $B1, $59, $04, $5C, $B2, $58, $3C, $01, $B5, $0C
        db $30, $83, $C0, $92, $FF, $F6, $10, $39, $64, $32, $04, $E0, $0C, $09, $FF, $33
        db $04, $E0, $18, $09, $FF, $B5, $0A, $32, $02, $CE, $FF, $93

assert read1($CB4D1A) == $60, "unexpected ROM state"
org $CB4D1A
        db $20

assert read4($CB81DD) == $0C370C3D && read4($CB8245) == $01824D81, "unexpected ROM state"
org $CB81DD
        db $37, $0C, $0C, $43, $0C, $03, $7F, $0C, $0C, $98, $0C, $88, $0C, $08, $40, $8B
        db $0C, $7F, $8C, $0C, $7F, $50, $BC, $59, $10, $92, $B2, $15, $D0, $00, $41, $31
        db $93, $4B, $0E, $8A, $93, $10, $05, $1F, $E0, $04, $CE, $FF, $48, $0F, $8A, $10
        db $0B, $E0, $04, $20, $E0, $03, $CE, $E0, $06, $FC, $06, $FF, $49, $10, $82, $CE
        db $FF, $95, $10, $85, $1F, $E0, $04, $CE, $FF, $48, $10, $8A, $49, $78, $10, $93
        db $10, $84, $C2, $82, $D1, $FF, $3E, $10, $DB, $4B, $D0, $D4, $D4, $EC, $D4, $FC
        db $B2, $C1, $C5, $00, $C0, $A3, $81, $4D, $82, $01, $3D, $0C

assert read4($CBB197) == $05413142 && read4($CBB260) == $FFCE8231, "unexpected ROM state"
org $CBB197
        db $38, $42, $31, $41, $05, $93, $05, $09, $CF, $E0, $02, $0F, $E0, $02, $FC, $06
        db $FF, $4B, $8D, $82, $05, $09, $CE, $E0, $02, $16, $E0, $02, $FC, $06, $FF, $94
        db $10, $85, $C3, $99, $80, $81, $FF, $93, $10, $85, $81, $CE, $E0, $05, $FF, $73
        db $0F, $45, $03, $02, $37, $BA, $69, $8E, $0C, $8F, $93, $05, $82, $CE, $FF, $10
        db $89, $C2, $CD, $C7, $87, $C6, $82, $9B, $CD, $FF, $02, $82, $D7, $FF, $41, $02
        db $02, $86, $C2, $CF, $C7, $81, $C6, $FF, $02, $0E, $CE, $E0, $09, $CF, $E0, $04
        db $CE, $E0, $04, $CF, $E0, $05, $0F, $FF, $4B, $92, $82, $05, $02, $CD, $FF, $02
        db $04, $E0, $08, $CF, $FF, $05, $94, $CE, $1D, $E0, $01, $1E, $E0, $01, $1D, $E0
        db $01, $1E, $E0, $01, $1D, $E0, $01, $1E, $E0, $01, $FF, $05, $02, $CE, $FF, $4B
        db $8E, $82, $02, $8A, $E0, $05, $CE, $E0, $0A, $20, $E0, $0A, $23, $FF, $4B, $8F
        db $82, $05, $82, $20, $FF, $3C, $05, $02, $FF, $FF, $45, $02, $04, $E0, $20, $CF
        db $FF, $B2, $40, $B1, $01, $D2, $9D, $4B, $90, $82, $78, $02, $02, $83, $C2, $83
        db $FF, $36, $02, $B2, $95, $CB, $00, $3B, $31, $82, $CE, $FF, $39

assert read4($CBBD9F) == $3002DB48 && read4($CBBDA6) == $91FF8F9F, "unexpected ROM state"
org $CBBD9F
        db $30, $05, $C2, $9F, $9F, $8F, $FF, $91, $48, $DB, $02

assert read1($CC49BE) == $CE, "unexpected ROM state"
org $CC49BE
        db $CF

assert read1($CC5491) == $08, "unexpected ROM state"
org $CC5491
        db $09

assert read4($CC5499) == $800911FF && read4($CC54CA) == $CC808F80, "unexpected ROM state"
org $CC5499
        db $CD, $FF, $11, $09, $80, $A0, $A0, $A0, $80, $97, $80, $CD, $FF, $12, $08, $84
        db $A0, $A0, $A0, $80, $97, $CD, $FF, $13, $09, $88, $A0, $A0, $A0, $80, $93, $80
        db $CD, $FF, $14, $08, $8C, $A0, $A0, $A0, $80, $93, $CD, $FF, $15, $08, $90, $A0
        db $A0, $A0, $80, $8F, $80

assert read4($CCD5E8) == $0A370A3D && read4($CCD5EC) == $050A430A, "unexpected ROM state"
org $CCD5E8
        db $37, $0A, $0A, $43, $0A, $05, $D4, $FA

assert read4($CCD79D) == $0D370D3D && read4($CCD7A1) == $050D430D, "unexpected ROM state"
org $CCD79D
        db $37, $0D, $0D, $43, $0D, $05, $D4, $ED
