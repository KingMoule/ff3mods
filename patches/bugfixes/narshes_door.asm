; Narshe's Door v1.3 by Leet Sketcher
;
; Narshe's secret cave door no longer closes again after opening the Main
; Menu in the World of Ruin.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-NarsheDoor-N.ips

hirom

assert read1($C404E3) == $8F, "unexpected ROM state"
org $C404E3
        db $8D

assert read1($CC3872) == $1B, "unexpected ROM state"
org $CC3872
        db $19

assert read4($CC3884) == $8004E001 && read4($CC38B9) == $F0D292F3, "unexpected ROM state"
org $CC3884
        db $05, $80, $CE, $E0, $60, $FC, $16, $FF, $FE, $CA, $F0, $01, $B4, $81, $B0, $81
        db $48, $B1, $02, $FE, $C0, $F0, $01, $BA, $38, $02, $73, $0E, $36, $03, $03, $F6
        db $F7, $D2, $52, $00, $F8, $62, $00, $61, $73, $0E, $76, $03, $03, $DB, $DB, $01
        db $DB, $DB, $DB, $DB, $FB, $F0, $FE, $FE, $FE

assert read4($CCD0E7) == $0901F0C0 && read4($CCD105) == $F0FBDBDB, "unexpected ROM state"
org $CCD0E7
        db $B2, $98, $38, $02, $B2, $BD, $36, $02, $FE, $FE, $FE, $FE, $FE, $FE, $FE, $FE
        db $FE, $FE, $FE, $FE, $FE, $FE, $FE, $FE, $FE, $FE, $FE, $FE, $FE, $FE, $B2, $98
        db $38, $02

assert read2($D1FA3C) == $D0E7, "unexpected ROM state"
org $D1FA3C
        db $05, $D1

assert read2($D1FA60) == $36BD, "unexpected ROM state"
org $D1FA60
        db $E7, $D0
