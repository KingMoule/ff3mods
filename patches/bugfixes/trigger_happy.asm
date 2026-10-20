; Trigger Happy v1.0 by Leet Sketcher
;
; A timer event no longer overrides a tile event firing on the same frame
; (Zone Eater's cave: skipping an exit or surviving the falling ceiling).
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-TriggerHappy-N.ips

hirom

assert read4($C09996) == $B91AB91A, "unexpected ROM state"
org $C09996
        db $2F, $D8, $37, $D8

assert read4($C0D82F) == $FFFFFFFF && read4($C0D8B5) == $FFFFFFFF, "unexpected ROM state"
org $C0D82F
        db $F4, $6C, $9A, $F4, $A5, $D8, $80, $06, $F4, $6C, $9A, $F4, $6B, $D8, $C2, $20
        db $A5, $82, $0A, $AA, $BF, $02, $00, $C4, $85, $1E, $BF, $00, $00, $C4, $C5, $1E
        db $F0, $13, $AA, $BF, $00, $00, $C4, $C5, $AF, $F0, $4B, $8A, $18, $69, $05, $00
        db $AA, $E4, $1E, $D0, $EE, $68, $7B, $E2, $20, $1A, $4C, $70, $9B, $A4, $E8, $A5
        db $E5, $1A, $99, $94, $05, $C9, $01, $00, $7B, $E2, $20, $A5, $E7, $B0, $01, $1A
        db $99, $96, $05, $C2, $21, $BF, $02, $00, $C4, $85, $E5, $99, $F4, $05, $7B, $E2
        db $20, $BF, $04, $00, $C4, $69, $CA, $85, $E7, $99, $F6, $05, $C8, $C8, $C8, $84
        db $E8, $A9, $01, $99, $C4, $05, $60, $BF, $02, $00, $C4, $85, $E5, $7B, $E2, $20
        db $BF, $04, $00, $C4, $18, $69, $CA, $85, $E7, $60

assert read4($CB8149) == $71FB583B && read4($CB819D) == $01812C01, "unexpected ROM state"
org $CB8149
        db $9F, $C0, $C2, $01, $A9, $5E, $00, $3B, $58, $FB, $71, $00, $80, $C1, $F1, $01
        db $B5, $81, $77, $81, $01, $C1, $F1, $01, $BF, $81, $83, $81, $01, $91, $71, $00
        db $00, $F4, $BB, $58, $F8, $94, $5A, $01, $5C, $B2, $66, $E5, $02, $FE, $91, $31
        db $04, $C8, $02, $09, $FF, $B2, $88, $81, $01, $FE, $91, $31, $02, $09, $FF, $71
        db $00, $00, $F4, $BB, $35, $31, $92, $58, $F8, $B5, $06, $C0, $27, $01, $2C, $81
        db $01, $FE, $FE, $FE, $FE, $FE, $FE, $FE
