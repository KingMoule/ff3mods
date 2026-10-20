; Game Over v1.0 by Leet Sketcher
;
; A defeat on the world map no longer leaves an event pointer on the stack
; (52 defeats in a row overwrote RAM and could freeze the game).
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-GameOver-N.ips

hirom

assert read4($C0A5F3) == $F18D01A9 && read4($C0A5F9) == $9B704C01, "unexpected ROM state"
org $C0A5F3
        db $20, $12, $B9, $A9, $01, $8D, $F1, $11, $80, $40

assert read4($C0B8D9) == $3A05C4BD && read4($C0B916) == $9A6D4C08, "unexpected ROM state"
org $C0B8D9
        db $DE, $C4, $05, $F0, $12, $BD, $F1, $05, $85, $E5, $BD, $F2, $05, $85, $E6, $BD
        db $F3, $05, $85, $E7, $4C, $6D, $9A, $20, $14, $B9, $BD, $94, $05, $85, $E5, $BD
        db $95, $05, $85, $E6, $BD, $96, $05, $85, $E7, $E4, $00, $D0, $09, $AC, $03, $08
        db $B9, $7D, $08, $99, $7C, $08, $4C, $6D, $9A, $A6, $E8, $CA, $CA, $CA, $86, $E8
        db $60
