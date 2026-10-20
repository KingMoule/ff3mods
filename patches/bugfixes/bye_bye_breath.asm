; Bye Bye Breath v1.2 by Leet Sketcher
;
; Fixes two crashes in the second Phunbaba fight (a Charmed Phunbaba blowing a
; member out of a full party, and an empty party after a lone KO).
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-ByeByeBreath-N.ips

hirom

assert read1($C2408A) == $2F, "unexpected ROM state"
org $C2408A
        db $04

assert read3($CF86D6) == $2236FD, "unexpected ROM state"
org $CF86D6
        db $FA, $36, $1A

assert read4($CFBDF3) == $000012FC && read4($CFBE41) == $783606FC, "unexpected ROM state"
org $CFBDF3
        db $FF, $FF, $FF, $FF, $FF, $FF, $FF, $F0, $EE, $EE, $EF, $FD, $F0, $07, $07, $0B
        db $FD, $F0, $07, $90, $EF, $FF, $FC, $1C, $00, $00, $FC, $05, $00, $00, $FC, $06
        db $36, $A0, $F1, $36, $C2, $FE, $FF, $F0, $EE, $EE, $EF, $FD, $F0, $07, $07, $0B
        db $FD, $F0, $07, $90, $EF, $FF, $FC, $12, $00, $00, $FC, $13, $00, $01, $F1, $44
        db $EA, $FE, $FC, $1C, $00, $00, $FC, $05, $00, $00, $FC, $06, $36, $78, $FC, $13
        db $00, $01
