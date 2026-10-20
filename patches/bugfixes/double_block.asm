; Double Block v1.1 by Leet Sketcher
;
; A living character with a shield no longer blocks a Fenix Down twice.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-DoubleBlock-N.ips

hirom

assert read4($D02165) == $21992199 && read4($D02168) == $99219921, "unexpected ROM state"
org $D02165
        db $86, $21, $86, $21, $86, $21, $86

assert read4($D02199) == $830F1FE9 && read4($D021A7) == $08070605, "unexpected ROM state"
org $D02199
        db $82, $00, $00, $C2, $C0, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF, $FF
        db $FF, $FF

assert read4($D07A53) == $1F07899A && read4($D07A69) == $FFC0C200, "unexpected ROM state"
org $D07A53
        db $DB, $01, $FF, $9A, $89, $07, $1F, $8A, $80, $8B, $82, $06, $04, $89, $20, $80
        db $88, $83, $67, $83, $2F, $1E, $8A, $FA, $99, $21
