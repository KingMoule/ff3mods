; Map Mishap v1.8 by Leet Sketcher
;
; Fixes seven map glitches (see Leet Sketcher's readme for the list).
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-MapMishap-N.ips

hirom

assert read4($CA0DD3) == $0B70382D, "unexpected ROM state"
org $CA0DD3
        db $12, $38, $70, $02

assert read1($CA0DE5) == $1C, "unexpected ROM state"
org $CA0DE5
        db $0A

assert read4($CA37FD) == $190BD50C && read4($CA3839) == $FF80C080, "unexpected ROM state"
org $CA37FD
        db $03, $FC, $11, $FF, $FE, $41, $09, $09, $03, $FC, $19, $FF, $FE, $41, $08, $08
        db $03, $FC, $21, $FF, $FE, $41, $07, $07, $03, $FC, $29, $FF, $FE, $73, $0D, $32
        db $03, $04, $90, $90, $90, $A0, $A0, $07, $B0, $B0, $17, $76, $77, $E1, $73, $0D
        db $72, $03, $04, $BA, $BA, $C4, $56, $57, $CC, $08, $18, $DA, $BA, $BA, $BA, $FE

assert read2($CA7938) == $ECF8, "unexpected ROM state"
org $CA7938
        db $1A, $38

assert read1($CAECF4) == $01, "unexpected ROM state"
org $CAECF4
        db $81

assert read4($CAED02) == $17B0B007 && read4($CAED05) == $E1777617, "unexpected ROM state"
org $CAED02
        db $A0, $B0, $B0, $B0, $E1, $76, $77

assert read4($CAED10) == $CC5756C4 && read4($CAED13) == $DA1808CC, "unexpected ROM state"
org $CAED10
        db $BA, $BA, $56, $57, $BA, $08, $18

assert read3($CC5180) == $451505, "unexpected ROM state"
org $CC5180
        db $61, $32, $42

assert read2($CC5188) == $0113, "unexpected ROM state"
org $CC5188
        db $D3, $E3

assert read4($D1FE35) == $B3005EB3 && read4($D1FE3A) == $005EB300, "unexpected ROM state"
org $D1FE35
        db $7B, $51, $02, $7B, $51, $02, $7B, $51, $02

assert read1($D9B131) == $04, "unexpected ROM state"
org $D9B131
        db $02

assert read1($DAD01A) == $0B, "unexpected ROM state"
org $DAD01A
        db $B3

assert read1($DAD466) == $25, "unexpected ROM state"
org $DAD466
        db $DE

assert read4($DB2943) == $1106F2EE && read4($DB294A) == $DBD80847, "unexpected ROM state"
org $DB2943
        db $3F, $07, $A0, $A0, $11, $E0, $1B, $3A, $47, $55, $04

assert read3($DB2989) == $7776E1, "unexpected ROM state"
org $DB2989
        db $76, $77, $E1

assert read4($DB2D36) == $3214339E && read4($DB2D42) == $3B5DE485, "unexpected ROM state"
org $DB2D36
        db $6E, $0B, $18, $B0, $B0, $60, $33, $5C, $E3, $E4, $5D, $13, $85, $C4, $68, $0C

assert read4($DB2D5A) == $577F560B && read4($DB2D64) == $25193D92, "unexpected ROM state"
org $DB2D5A
        db $03, $56, $9F, $57, $CC, $66, $67, $DA, $36, $07, $92, $3D, $25, $8C

assert read2($DB2D74) == $BCDF, "unexpected ROM state"
org $DB2D74
        db $BC, $EF

assert read4($DB2D7C) == $18AF08BA, "unexpected ROM state"
org $DB2D7C
        db $08, $18, $DA, $D7

assert read4($DB2D89) == $0796B589 && read4($DB2D8B) == $24CA0796, "unexpected ROM state"
org $DB2D89
        db $B5, $8B, $81, $81, $C9, $2C

assert read1($DBEB30) == $1D, "unexpected ROM state"
org $DBEB30
        db $0D

assert read4($DBEB36) == $810DB826 && read4($DBEB3E) == $7151ECC7, "unexpected ROM state"
org $DBEB36
        db $FD, $15, $81, $FC, $24, $FE, $46, $8E, $61, $A1, $DC, $CD

assert read4($DD459A) == $F82BF839 && read4($DD45A9) == $A979F957, "unexpected ROM state"
org $DD459A
        db $69, $F8, $8B, $D0, $48, $F8, $3A, $F8, $2C, $F8, $0E, $F9, $08, $30, $F9, $52
        db $F9, $74, $D1

assert read4($DD45D3) == $01604913 && read4($DD45D8) == $9DF84BF8, "unexpected ROM state"
org $DD45D3
        db $36, $49, $60, $01, $59, $F8, $7B, $F8, $0D

assert read1($DDDF56) == $A9, "unexpected ROM state"
org $DDDF56
        db $A8

assert read1($DEAEB2) == $00, "unexpected ROM state"
org $DEAEB2
        db $04

assert read1($DEAFBA) == $00, "unexpected ROM state"
org $DEAFBA
        db $03

assert read1($DEB0BD) == $00, "unexpected ROM state"
org $DEB0BD
        db $01

assert read1($DEB1C3) == $00, "unexpected ROM state"
org $DEB1C3
        db $01

assert read1($DEB2C8) == $00, "unexpected ROM state"
org $DEB2C8
        db $24

assert read4($DEB3F0) == $114BF540 && read4($DEB40E) == $1925BF0C, "unexpected ROM state"
org $DEB3F0
        db $50, $F5, $4B, $21, $1C, $07, $14, $1C, $2C, $00, $15, $0C, $35, $1A, $2C, $09
        db $24, $23, $34, $0C, $04, $20, $FF, $1B, $36, $04, $39, $04, $4C, $04, $BD, $24
        db $50, $14

assert read3($DEB47B) == $0E174D, "unexpected ROM state"
org $DEB47B
        db $35, $14, $26
