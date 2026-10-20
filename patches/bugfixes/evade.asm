; Evade bug fix
;
; In the SNES release the hit check for physical attacks reads the target's
; MBlock instead of its Evade, and then skips the Blind and Beads checks:
; Evade does nothing, Beads are useless and Blind doesn't make attackers miss.
; Physical attacks now use Evade (and the Blind / Beads checks), magical
; attacks keep using MBlock. This is the BUGFIX_EVADE variant of the
; everything8215/ff6 disassembly; the later ports fixed it the same way.

hirom

!Evade      = $3B54
!MagicEvade = $3B55

EvadeChecksDone = $C22388      ; past the physical-only Blind / Beads checks

; physical attack, target without Image: go to the Evade load
assert read2($C2232C) == $11F0, "unexpected hit check code"
org $C2232C
        beq PhysicalEvade

; vanilla, 11 bytes: lda Evade / bcs + / lda MagicEvade / + pha / bcc $2388
; (carry is always clear here, so physical attacks also got MagicEvade)
assert read4($C2233F) == $B03B54B9 && read4($C22343) == $3B55B903 && read3($C22347) == $3E9048, "unexpected hit check code"
org $C2233F
MagicalEvade:                   ; magical attacks branch here
        lda !MagicEvade,y
        pha
        bra EvadeChecksDone
PhysicalEvade:
        lda !Evade,y
        pha
        nop                     ; fall through to the Blind / Beads checks
assert pc() == $C2234A, "Evade fix must stay 11 bytes"
