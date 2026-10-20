; Morph Mayhem v1.2 by Leet Sketcher
;
; The Morph gauge no longer drains while Terra is asleep, stopped or frozen,
; while someone uses Quick, or after she leaves battle.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-MorphMayhem-N.ips

hirom

assert read4($C21211) == $AD3820C2 && read4($C21233) == $3F31AD4E, "unexpected ROM state"
org $C21211
        db $BD, $A0, $3A, $4A, $90, $1C, $89, $08, $D0, $1F, $C2, $20, $AD, $30, $3F, $ED
        db $32, $3F, $8D, $30, $3F, $E2, $20, $EB, $B0, $0C, $9C, $31, $3F, $A9, $04, $20
        db $52, $67, $20, $F7, $A7, $7B

assert read4($C220E2) == $A920C27F && read4($C2215F) == $60629E20, "unexpected ROM state"
org $C220E2
        db $FA, $AD, $38, $3A, $F0, $F5, $F4, $02, $09, $48, $A5, $B1, $4A, $4A, $68, $B0
        db $65, $85, $B8, $9C, $38, $3A, $20, $00, $64, $A2, $06, $BD, $18, $30, $14, $B8
        db $F0, $3E, $EB, $BD, $19, $32, $D0, $38, $BD, $A0, $3A, $89, $50, $D0, $31, $4A
        db $90, $2E, $BD, $E4, $3E, $89, $02, $D0, $27, $BD, $F9, $3E, $89, $20, $D0, $20
        db $EB, $04, $B8, $0C, $39, $3A, $0C, $4C, $2F, $A9, $40, $20, $AB, $5B, $9B, $A9
        db $40, $20, $4C, $46, $20, $C8, $07, $EC, $E2, $3E, $D0, $03, $20, $E7, $0A, $9B
        db $CA, $CA, $10, $B7, $68, $68, $A5, $B8, $F0, $91, $F4, $06, $22, $64, $B9, $BB
        db $20, $C2, $57, $20, $DB, $63, $C2, $20, $68, $8D, $28, $3A, $E2, $20, $4C, $9E
        db $62

assert read4($C26752) == $FFFFFFFF && read4($C26757) == $FFFFFFFF, "unexpected ROM state"
org $C26752
        db $CD, $7A, $3A, $F0, $03, $4C, $EE, $4C, $60

assert read4($C2A7F7) == $FFFFFFFF && read4($C2A7FC) == $FFFFFFFF, "unexpected ROM state"
org $C2A7F7
        db $BD, $04, $3B, $F0, $03, $4C, $36, $0B, $60
