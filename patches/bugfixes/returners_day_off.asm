; Returner's Day Off v1.4 by Leet Sketcher
;
; Two events account for Gau being left on the Veldt; this could leave
; characters behind and freeze the game after the Esper World flashback.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ReturnersDayOff-N.ips

hirom

assert read4($CAAB99) == $ABC0E191 && read4($CAABB8) == $19DC0B8D, "unexpected ROM state"
org $CAAB99
        db $E1, $C0, $AB, $01, $BB, $AB, $00, $41, $0B, $0B, $85, $D5, $36, $2A, $49, $FF
        db $DE, $C0, $AB, $81, $BB, $AB, $00, $0B, $85, $D5, $3E, $2A, $CF, $FF, $8D, $0B
        db $DC, $19, $DE

assert read1($CAABEF) == $92, "unexpected ROM state"
org $CAABEF
        db $93

assert read4($CAAC03) == $01ABC0E1 && read4($CAAC36) == $02E00505, "unexpected ROM state"
org $CAAC03
        db $DE, $C0, $A2, $81, $0F, $AC, $00, $02, $03, $C2, $8D, $FF, $C0, $A4, $81, $1C
        db $AC, $00, $04, $05, $E0, $03, $C2, $8D, $FF, $C0, $A5, $81, $29, $AC, $00, $05
        db $05, $E0, $02, $C2, $8D, $FF, $C0, $AB, $81, $3D, $AC, $00, $E1, $C0, $AB, $01
        db $3D, $AC, $00, $0B, $05, $E0, $01

assert read4($CAC458) == $01ABC0E1 && read4($CAC4AC) == $35D60000, "unexpected ROM state"
org $CAC458
        db $DE, $C0, $A2, $81, $6D, $C4, $00, $77, $02, $8B, $02, $7F, $8C, $02, $7F, $88
        db $02, $00, $00, $D6, $33, $C0, $A4, $81, $81, $C4, $00, $77, $04, $8B, $04, $7F
        db $8C, $04, $7F, $88, $04, $00, $00, $D6, $34, $C0, $A5, $81, $95, $C4, $00, $77
        db $05, $8B, $05, $7F, $8C, $05, $7F, $88, $05, $00, $00, $D6, $35, $C0, $AB, $81
        db $B0, $C4, $00, $E1, $C0, $AB, $01, $B0, $C4, $00, $77, $0B, $8B, $0B, $7F, $8C
        db $0B, $7F, $88, $0B, $00, $00, $D6, $36
