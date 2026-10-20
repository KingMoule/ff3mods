; Better Dice v1.3 by Leet Sketcher
;
; Setzer's Dice: one die always has an even 1-6 distribution and the others
; are closer to even (vanilla rolled 1-4 at 3/16 and 5-6 at 1/8); the
; matching-dice bonus also applies to the 2-die Dice; the Offering halves
; Dice damage (replaces Chance Offering, which only fixed that last part).
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-BetterDice-N.ips

hirom

assert read4($C2415B) == $A40C20A9 && read4($C241E1) == $B58526A9, "unexpected ROM state"
org $C2415B
        db $A5, $B5, $48, $BD, $58, $3C, $48, $A9, $20, $0C, $A4, $11, $A9, $0F, $85, $B7
        db $7B, $AC, $A8, $11, $88, $5A, $20, $5A, $4B, $A2, $06, $20, $92, $47, $8A, $BB
        db $95, $B5, $AD, $1E, $02, $88, $F0, $F1, $10, $EC, $FA, $DA, $A9, $01, $EB, $B5
        db $B5, $1A, $20, $81, $47, $CA, $10, $F6, $EB, $A3, $02, $4A, $AD, $AF, $11, $B0
        db $01, $0A, $20, $81, $47, $C2, $20, $8D, $B0, $11, $E2, $20, $FA, $68, $A5, $B5
        db $D5, $B5, $D0, $16, $CA, $D0, $F9, $AA, $7B, $C2, $21, $6D, $B0, $11, $B0, $05
        db $CA, $10, $F8, $80, $02, $7B, $3A, $8D, $B0, $11, $C2, $20, $A5, $B6, $EB, $85
        db $B6, $E2, $20, $7B, $A5, $B5, $0A, $0A, $0A, $0A, $04, $B7, $68, $D0, $02, $A9
        db $26, $85, $B5, $60, $EA, $EA, $EA, $EA, $EA, $EA
