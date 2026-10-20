; Zombie/Rippler v1.2, fix A + B by Leet Sketcher
;
; Rippler no longer swaps hidden statuses (Morph, Dog Block...). A target
; freed from Zombie by Rippler is healed 1/8 of its max HP (like Revivify)
; instead of staying alive at 0 HP.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ZombieRipA-N.ips
;   FF3-ZombieRipB-N.ips

hirom

assert read4($C23C09) == $393EE4BD && read4($C23C48) == $603E1099, "unexpected ROM state"
org $C23C09
        db $38, $A9, $AA, $11, $85, $EE, $BD, $E4, $3E, $39, $E4, $3E, $49, $FF, $FF, $32
        db $EE, $85, $EE, $90, $06, $20, $BE, $65, $20, $BE, $65, $38, $BD, $E4, $3E, $25
        db $EE, $99, $D4, $3D, $9D, $FC, $3D, $DA, $BB, $7A, $90, $03, $18, $80, $ED, $8A
        db $69, $14, $00, $AA, $98, $69, $14, $00, $A8, $A9, $AC, $11, $E0, $28, $90, $C4
        db $60, $EA, $EA

assert read4($C265BE) == $FFFFFFFF && read4($C265D1) == $FFFFFFFF, "unexpected ROM state"
org $C265BE
        db $B9, $F4, $3B, $D0, $0E, $BD, $F4, $3B, $F0, $09, $B9, $1C, $3C, $4A, $4A, $4A
        db $99, $E4, $33, $DA, $BB, $7A, $60

assert read1($C4736B) == $03, "unexpected ROM state"
org $C4736B
        db $02
