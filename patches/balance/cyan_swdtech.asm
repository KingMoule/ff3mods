; Cyan SwdTech rebalance
;
; - The SwdTech gauge charges twice as fast (one level every 64 frames
;   instead of 128).
; - Every SwdTech becomes a physical attack based on the weapon's battle
;   power and Vigor (same formula as Fight). The spell power byte of each
;   SwdTech now holds a damage multiplier in eighths of a Fight.
;
;   Dispatch      1.25x            single target, ignores defense
;   Retort        1.5x counter     ignores defense
;   Slash         1.5x + Sap       works on bosses (no more 50% HP / death check)
;   Quadra Slam   4 hits x 0.75    random targets
;   Empowerer     1x HP drain, then 0.25x MP drain
;   Stunner       1x all enemies + Stop (140/256)
;   Quadra Slice  4 hits x 1       random targets, ignores defense
;   Cleave        1.5x all enemies + Death (182/256); death-immune targets
;                 still take the damage
;
; Free space used: C2/6469-C2/64C9

asar 1.90
hirom


!MagicProp = $C46AC0

macro spell_byte(id, offset, old, new)
    assert read1(!MagicProp+<id>*14+<offset>) == <old>, "unexpected spell data"
    org !MagicProp+<id>*14+<offset>
        db <new>
endmacro

; ------------------------------------------------------------------------------
; Gauge speed: increment the gauge counter every 2 frames instead of every 4.

assert read1($C17D84) == $03, "unexpected SwdTech gauge code"
org $C17D84
        db $01

; ------------------------------------------------------------------------------
; Spell data (14 bytes each): +2 flags, +4 flags, +6 power, +7 misc, +9 effect
;
; flag bits used here: byte 2 = $01 physical, $02 miss if death-immune,
; $10 random target, $20 ignore defense, $40 no damage split;
; byte 4 = $20 can't dodge, $80 fraction of HP

%spell_byte($55, 6, $78, $0A)   ; Dispatch: power 120 -> 1.25x

%spell_byte($56, 2, $20, $21)   ; Retort: physical
%spell_byte($56, 6, $38, $0C)   ;   power 56 -> 1.5x

%spell_byte($57, 2, $23, $21)   ; Slash: no death-immune miss
%spell_byte($57, 4, $A0, $20)   ;   no HP fraction
%spell_byte($57, 6, $08, $0C)   ;   1.5x

%spell_byte($58, 6, $48, $06)   ; Quadra Slam: power 72 -> 0.75x per hit

%spell_byte($59, 2, $28, $29)   ; Empowerer: physical
%spell_byte($59, 6, $31, $08)   ;   power 49 -> 1x (2nd hit on MP is /4)

%spell_byte($5A, 2, $50, $51)   ; Stunner: physical
%spell_byte($5A, 6, $61, $08)   ;   power 97 -> 1x

%spell_byte($5B, 6, $46, $08)   ; Quadra Slice: power 70 -> 1x per hit

%spell_byte($5C, 2, $32, $71)   ; Cleave: physical, no split, no death-immune miss
%spell_byte($5C, 4, $00, $20)   ;   can't dodge
%spell_byte($5C, 6, $00, $0C)   ;   1.5x
%spell_byte($5C, 7, $01, $00)   ;   don't miss when target is immune to status
%spell_byte($5C, 9, $23, $3F)   ;   Stunner effect: Death lands at hit rate/256

; ------------------------------------------------------------------------------
; Damage hook: replaces the start of CalcDmg (C2/2B9D: lda $11a2 / lsr / jcc).

assert read4($C22B9D) == $4A11A2AD, "unexpected CalcDmg code"
org $C22B9D
        jmp SwdTechCalcDmg

!CalcMagicDmg = $2B69
!CalcPhysDmg  = $2BA6           ; vanilla physical damage, ends with plp/rts
!LsrA         = $0DD1           ; A16 = ($E8..$EA) >> (A+1)
!Mult24       = $47B7           ; $E8..$EA = A16 * $E8

!AttackPower  = $11A6
!BaseDmg      = $11B0
!NameType     = $3412           ; attack name type, 4 = SwdTech
!RHandPower   = $3B68
!LHandPower   = $3B69

assert read1($C26469) == $FF && read1($C264C9) == $FF, "free space in use"
org $C26469
SwdTechCalcDmg:
        lda $11A2
        lsr
        bcs .physical
        jmp !CalcMagicDmg
.physical:
        cpx #$08
        bcs .monster
        lda !NameType
        cmp #$04
        bne .vanilla

; character SwdTech: damage = Fight damage * multiplier / 8
        lda !AttackPower        ; multiplier in eighths
        pha
        lda !RHandPower,x       ; use the stronger hand
        cmp !LHandPower,x
        bcs +
        lda !LHandPower,x
+       sta !AttackPower
        jsr !CalcPhysDmg
        pla
        sta !AttackPower        ; restore for multi-hit (Quadra) and Empowerer
        sta $E8
        rep #$20
        lda !BaseDmg
        jsr !Mult24
        lda #$0002
        jsr !LsrA
        sta !BaseDmg
        sep #$20
        rts

; monsters using SwdTech attacks (Cyan at the Imperial camp) keep the
; vanilla power since the power byte now holds a multiplier
.monster:
        lda $B6                 ; attack index
        sec
        sbc #$55
        cmp #$08
        bcs .vanilla
        phx
        tax
        lda.l VanillaPower,x
        plx
        sta !AttackPower
.vanilla:
        jmp !CalcPhysDmg

VanillaPower:
        db 120, 56, 8, 72, 49, 97, 70, 0

assert pc() <= $C264CA, "SwdTech hook overflows its free space"
