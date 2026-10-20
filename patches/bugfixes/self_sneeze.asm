; Self Sneeze v2.0 by Leet Sketcher
;
; The Fake Mustache control link is cut when Relm jumps with Palidor or when
; either side is removed from battle.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-SelfSneeze-N.ips

hirom

assert read1($C207B2) == $03, "unexpected ROM state"
org $C207B2
        db $23

assert read1($C207CC) == $28, "unexpected ROM state"
org $C207CC
        db $24

assert read4($C207D6) == $B88504A9 && read4($C20815) == $DA073033, "unexpected ROM state"
org $C207D6
        db $A2, $00, $A0, $02, $98, $0A, $85, $B8, $A9, $24, $20, $91, $4E, $A2, $08, $88
        db $D0, $F2, $A9, $FF, $8D, $F8, $33, $8D, $F9, $33, $FA, $DA, $20, $0B, $08, $8A
        db $69, $28, $AA, $20, $0B, $08, $FA, $EC, $04, $34, $D0, $08, $A9, $FF, $8D, $04
        db $34, $8D, $02, $34, $60, $BD, $6C, $33, $30, $04, $A8, $20, $36, $08, $BD, $6D
        db $33, $30, $06

assert read4($C2081E) == $3404ECFA && read4($C20839) == $95993394, "unexpected ROM state"
org $C2081E
        db $BB, $60, $BD, $04, $32, $29, $BF, $9D, $04, $32, $60, $EA, $EA, $EA, $EA, $EA
        db $EA, $EA, $EA, $EA, $EA, $EA, $EA, $EA, $A9, $FF, $9D, $6C, $33, $99, $6D

assert read4($C20B72) == $293205BD && read4($C20B7F) == $60322C9D, "unexpected ROM state"
org $C20B72
        db $1E, $05, $32, $5E, $05, $32, $9E, $B5, $3A, $A9, $E0, $9D, $2C, $32, $4C, $20
        db $08

assert read4($C21450) == $12A220C2, "unexpected ROM state"
org $C21450
        db $A2, $12, $C2, $20

assert read1($C2145B) == $18, "unexpected ROM state"
org $C2145B
        db $17

assert read4($C21467) == $093EF9BD && read4($C21475) == $28DC10CA, "unexpected ROM state"
org $C21467
        db $5A, $9B, $20, $00, $1F, $20, $C8, $07, $20, $B9, $07, $7A, $CA, $CA, $10, $DB
        db $28, $60
