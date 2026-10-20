; Shadow Gone v1.3 by Leet Sketcher
;
; When Shadow leaves an all-Gau party entering Narshe, the party selection
; screen opens instead of leaving an empty party (forced reset).
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ShadowGone-N.ips

hirom

assert read4($C40434) == $2702D35C && read4($C4043B) == $5C3A0F02, "unexpected ROM state"
org $C40434
        db $54, $D3, $02, $27, $30, $46, $D3, $02, $0F, $3A, $54

assert read4($CCD332) == $B301A3C0 && read4($CCD3C1) == $3902E499, "unexpected ROM state"
org $CCD332
        db $C1, $A3, $01, $5D, $80, $B3, $5E, $00, $31, $83, $81, $CE, $FF, $C0, $2F, $02
        db $54, $D3, $02, $FE, $DE, $C1, $A3, $01, $5D, $80, $B3, $5E, $00, $31, $83, $83
        db $CE, $FF, $DE, $C1, $A3, $01, $5D, $80, $B3, $5E, $00, $47, $B2, $AC, $C6, $00
        db $3C, $FF, $03, $FF, $FF, $B2, $34, $2E, $01, $38, $31, $03, $C2, $CE, $FF, $33
        db $04, $C2, $81, $CE, $FF, $34, $04, $C2, $83, $CE, $FF, $B2, $C1, $C5, $00, $39
        db $38, $03, $84, $C2, $82, $CC, $FF, $92, $4B, $D3, $06, $03, $82, $8A, $FF, $94
        db $03, $82, $63, $FF, $94, $03, $82, $9A, $FF, $42, $03, $45, $33, $03, $83, $CE
        db $FF, $34, $03, $81, $CE, $FF, $31, $84, $CE, $E0, $08, $FF, $3F, $03, $00, $3E
        db $03, $45, $D5, $F3, $B2, $99, $E4, $02, $39, $C0, $A0, $81, $4D, $C2, $02, $B2
        db $95, $CB, $00
