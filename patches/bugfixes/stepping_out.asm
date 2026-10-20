; Stepping Out v1.0 by Leet Sketcher
;
; Holding Y while stepping on an event tile in split-party dungeons no longer
; switches parties before the event fires (skipping it).
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-SteppingOut-N.ips

hirom

assert read4($C00120) == $D0207578 && read4($C00139) == $6D2620CC, "unexpected ROM state"
org $C00120
        db $26, $6D, $20, $78, $75, $20, $D0, $2B, $20, $3C, $57, $20, $08, $1F, $20, $C2
        db $1F, $20, $81, $20, $20, $02, $21, $20, $2D, $5A, $20, $95, $CC
