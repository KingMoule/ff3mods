; Vanish/Doom bug fix
;
; A magical attack against a Vanished target is declared a hit before the
; "miss if protected from instant death" check, so Vanish followed by X-Zone
; or Doom kills almost anything, bosses included. Magical attacks on Vanished
; targets still always hit, except attacks that miss death-protected targets,
; which now miss them as usual. (Fixed the same way in the GBA port.)
;
; Free space used: C2/A65A-C2/A66F

hirom

!InstantDeathProt = $3AA1       ; bit 2: protected from instant death

; CheckHit, target has Vanish and the attack doesn't remove it:
; lda $11A2 / lsr / jmp $22B3 (bcc $22E8 hit / fall through to $22B5 miss)
assert read3($C2222A) == $22B34C, "unexpected Vanish hit check"
assert read2($C222B3) == $3390, "unexpected hit check code"
org $C2222A
        jmp VanishHitCheck

assert read4($C2A65A) == $FFFFFFFF && read4($C2A66C) == $FFFFFFFF, "free space in use"
org $C2A65A
VanishHitCheck:
        bcs .miss               ; physical attacks miss Vanished targets
        lda $11A2
        bit #$02                ; miss if target is protected from instant death?
        beq .hit
        lda !InstantDeathProt,y
        bit #$04
        bne .miss
.hit:
        jmp $22E8               ; return carry clear (hit)
.miss:
        jmp $22B5
assert pc() <= $C2A670, "Vanish fix overflows its free space"
