; Killer Life 3 v1.4 by Leet Sketcher
;
; An Undead monster killed by an X-weapon instant kill no longer revives with
; Life 3 only to die again.
;
; Generated from the released IPS by scripts/ips2asar.py:
;   FF3-KillerLife3-N.ips

hirom

assert read2($C206FE) == $0799, "unexpected ROM state"
org $C206FE
        db $72, $67

assert read4($C26772) == $FFFFFFFF && read4($C2677A) == $FFFFFFFF, "unexpected ROM state"
org $C26772
        db $BD, $95, $3C, $30, $06, $BD, $F9, $3E, $4C, $99, $07, $60
