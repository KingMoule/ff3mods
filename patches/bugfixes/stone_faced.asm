; Stone Faced v1.2 by Leet Sketcher
;
; Petrified monsters no longer repeat their last attack after every turn.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-StoneFaced-N.ips

hirom

assert read1($C23BB3) == $FF, "unexpected ROM state"
org $C23BB3
        db $FC

assert read1($C23BCE) == $FF, "unexpected ROM state"
org $C23BCE
        db $FC

assert read1($C2439E) == $0D, "unexpected ROM state"
org $C2439E
        db $0C

assert read1($C243FD) == $FF, "unexpected ROM state"
org $C243FD
        db $FC

assert read3($C244D3) == $F944EA, "unexpected ROM state"
org $C244D3
        db $ED, $44, $EA

assert read4($C244EA) == $2511AAAD && read4($C2454A) == $F40402B0, "unexpected ROM state"
org $C244EA
        db $20, $D7, $44, $AD, $AA, $11, $25, $F8, $85, $F4, $AD, $AC, $11, $25, $FA, $85
        db $F6, $60, $7B, $99, $D4, $3D, $99, $E8, $3D, $99, $FC, $3D, $99, $10, $3E, $60
        db $EA, $EA, $B9, $FC, $3D, $85, $F4, $B9, $10, $3E, $85, $F6, $B9, $D4, $3D, $39
        db $1C, $33, $85, $FC, $B9, $E8, $3D, $39, $30, $33, $85, $FE, $B9, $E4, $3E, $85
        db $F8, $B9, $F8, $3E, $85, $FA, $B9, $1C, $3C, $4A, $4A, $4A, $D9, $F4, $3B, $A9
        db $00, $02, $90, $04, $04, $FC, $B0, $02, $04, $F4, $A5, $F8, $29, $40, $00, $F0
        db $03, $20, $0E, $46
