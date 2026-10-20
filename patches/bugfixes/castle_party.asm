; Castle Party v1.3 by Leet Sketcher
;
; Sabin's party is no longer reordered when switching back from Cyan's scenes
; in Doma during the Imperial Camp infiltration.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-CastleParty-N.ips

hirom

assert read4($CB0BC7) == $3D010BCF && read4($CB0BE6) == $3AFF8282, "unexpected ROM state"
org $CB0BC7
        db $CC, $0B, $01, $3D, $03, $3D, $05, $3E, $02, $46, $01, $47, $45, $5C, $91, $6B
        db $75, $20, $24, $02, $C0, $59, $08, $31, $82, $82, $FF, $3A, $FE, $FE, $FE, $FE
        db $FE, $FE, $FE

assert read4($CB1318) == $8994C385 && read4($CB1333) == $01033F45, "unexpected ROM state"
org $CB1318
        db $88, $C3, $94, $81, $81, $81, $80, $80, $FF, $39, $DA, $12, $DB, $11, $DB, $0B
        db $DA, $01, $D0, $32, $42, $31, $C0, $F3, $02, $37, $13, $01, $3D, $03, $45

assert read4($CB133E) == $01053F45, "unexpected ROM state"
org $CB133E
        db $46, $01, $47, $45

assert read4($CB9AAE) == $B901BEDE && read4($CB9AC5) == $053E0005, "unexpected ROM state"
org $CB9AAE
        db $40, $02, $02, $37, $02, $02, $43, $02, $04, $3D, $02, $3F, $02, $02, $D4, $E2
        db $3E, $03, $3E, $05, $46, $02, $B2, $C9, $9A, $01, $FE

assert read4($CBA0EC) == $B901BEDE && read4($CBA0FA) == $45053E00, "unexpected ROM state"
org $CBA0EC
        db $3D, $02, $46, $02, $47, $3E, $03, $3E, $05, $45, $B2, $FE, $A0, $01, $FE, $FE
        db $FE, $FE
