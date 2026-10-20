; Ultimate Damage Fix v1.4 by Leet Sketcher, ported to asar for ff3mods
;
; - Physical and magical damage no longer overflow past 65,535 (a very
;   strong attack used to wrap around to almost no damage).
; - Genji Glove and Offering only reduce damage from Fight and Capture,
;   instead of every physical attack (Pummel, SwdTech, etc.).
;
; Rewrites CalcDmg (C2/2B69-C2/2C20) and merges in the Atlas Armlet/Earring
; routine (C2/0D4A-C2/0D86); the call site at C2/322B calls the new routine
; once. No free space used.

hirom

assert read1($C20D4A) == $08 && read1($C20D86) == $60, "unexpected relic damage code"
assert read1($C22B69) == $AD && read2($C22C1F) == $6028, "unexpected CalcDmg code"
assert read3($C2322B) == $2B9D20 && read3($C2322E) == $0D4A20, "unexpected CalcDmg call site"

org $C20D4A
add_acc_damage:                 ; add value in A to damage value
        clc
add_with_carry:
        pea $0000               ; pulled into the top two bytes below
        bra add_damage
one_point_five:
        lda $EA                 ; top two bytes of damage
        lsr a
        pha
        lda $E8                 ; bottom two bytes
        ror
add_damage:
        adc $E8
        sta $E8
        pla
add_overflow:
        adc $EA
        sta $EA
        rts

damage_part2:
        bit #$0002              ; Earring bits (the .asm says #$0003, the released IPS uses #$0002)
        bcs atlas               ; physical and not MP: check Atlas Armlet
        bne two_earrings
        xba
        lsr a
atlas:
        lsr a
        lda $E8
        bcc exit
        lsr a
        bra earrings
two_earrings:
        lda $E8
earrings:
        lsr a
        jsr add_acc_damage
exit:
        lda $EA
        beq real_damage         ; damage overflowed:
        tdc
        dec                     ; cap at 65,535
        bra finalize
real_damage:
        lda $E8
finalize:
        sta $11B0
        plp
        rts
assert pc() <= $C20D87, "overflows original routine"

org $C22B69
damage_alg:
        lda $11AF               ; attacker's level
        sta $E8
        tay
        lda $11A2
        lsr a                   ; carry = physical
        php                     ; kept for later physical/magical checks
        stz $EB
        tdc
        lda $11A6               ; battle power or spell power
        rep #$20
        bcc .magical
        cpx #$08                ; physical: quadruple power for monsters
        bra .quadruple
.magical:
        cpy #$01                ; magical: quadruple power if level is not 0
        tay                     ; keep spell power
.quadruple:
        bcc .after_quad
        asl a
        asl a
.after_quad:
        pha                     ; power
        lda $03,s
        lsr a
        tdc
        bcc .multiply           ; magical: no Gauntlet bonus
        lda $B2
        asl a
        asl a                   ; carry clear = Gauntlet bonus
        lda $01,s
        bcs .clear_carry
        lsr a                   ; BP / 2
        adc $01,s               ; BP * 3 / 2
        lsr a                   ; BP * 3 / 4
        adc $01,s               ; BP * 7 / 4
.clear_carry:
        clc
.multiply:
        sep #$20
        adc $11AE               ; + Vigor * 2 if physical, MagPwr if magical
        xba
        adc #$00
        xba
        jsr $47B7               ; 16-bit "attack" * 8-bit level
        tya                     ; level if physical, spell power if magical
        jsr $4781               ; Y * high byte of first product
        rep #$20
        pha
        lda $E8                 ; low 16 bits of first product
        sty $E8
        jsr $47B7
        pla
        jsr add_overflow
        lda $03,s
        lsr a
        php
        lda #$0004              ; magical: divide by 32
        bcc .divide
        asl a
        dec a                   ; physical: divide by 256
.divide:
        jsr $0DD1
        sta $E8
        plp
        pla                     ; power
        bcc .after_genjioff
        tay
        cpx #$08
        bcs .clear_acc          ; monsters: no character physical bonus
        jsr one_point_five
        tya
        jsr add_acc_damage      ; * 1.5 + battle power
        ldy $B5                 ; command
        beq .genjioff           ; Fight
        cpy #$06                ; Capture
        bne .clear_acc
.genjioff:
        lda $3C58,x
        lsr a                   ; Offering: halve damage, rounding up
        bcc .genji
        lsr $EA
        ror $E8
        pha
        tdc
        jsr add_with_carry
        pla
.genji:
        bit #$0008              ; Genji Glove: damage * 3/4, rounded
        beq .clear_acc
        jsr one_point_five
        inc $E8
        bne .after_round
        inc a
.after_round:
        lsr a
        sta $EA
        ror $E8
.clear_acc:
        tdc
.after_genjioff:
        jsr add_acc_damage      ; magical: + spell power * 4
        lda $11A4
        lsr a                   ; healing: skip Atlas Armlet/Earrings
        bcc .start_part2
        jmp exit
.start_part2:
        lda $11A2
        bmi .check_relics       ; carry clear if MP or magical
        lsr a
.check_relics:
        lda $3C44,x             ; relic effects
        jmp damage_part2
assert pc() <= $C22C21, "overflows original routine"

org $C2322B
        jsr damage_alg
        nop
        nop
        nop
