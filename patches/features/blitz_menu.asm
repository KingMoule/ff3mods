; Blitz menu
;
; Sabin's Blitz command opens a list of the Blitzes he knows (same window as
; the Magitek list: 4 rows x 2 columns) instead of asking for a button combo.
; Pick a Blitz, then a target, like Lore or Magitek. Blitzes not learned yet
; show as blank lines and can't be selected.
;
; - The battle menu reuses the Magitek window states; the list drawing and the
;   A button handler check whether the current command is Blitz.
; - The button combo code (C1/6F67-C1/7092) is no longer reachable and its
;   space holds the new code.
; - Blitz is removed from the battle "retarget" command list so the chosen
;   target is used (vanilla picked Blitz targets automatically).
;   Single-target Blitzes (Pummel, AuraBolt, Suplex, Bum Rush) let you pick
;   the enemy; Fire Dance and Air Blade target all enemies; Mantra and
;   Spiraler target the party.

hirom

!CmdBlitz          = $0A
!FirstBlitzAttack  = $5D

!KnownBlitzes      = $1D28      ; bit n = Blitz n learned
!ActionBufCmd      = $2BAF      ; wPlayerActionBuf::BattleCmd,y
!RowText           = $5755      ; list row text buffer
!AttackSel         = $7A85      ; attack chosen in the menu
!TargetFlagsSel    = $7A84      ; targeting flags for the target cursor
!CursorSfx         = $96        ; inc = play cursor sound
!ErrorSfx          = $95        ; inc = play error sound

GetActionBufPtr    = $C16D53    ; Y = current character's action buffer offset
InitListTextTfr    = $C14E04
DrawListText       = $C163A8
InitTargetSelect   = $C17792
InitMagitekSelect  = $C15980

; ------------------------------------------------------------------------------
; Blitz command opens the Magitek list window instead of the combo input

assert read2($C17CFA) == $7768, "unexpected battle command table"
org $C17CFA
        dw InitMagitekSelect&$FFFF

; draw list row: Magitek or Blitz (vanilla: phy / asl / tay)
assert read3($C14D2B) == $A80A5A, "unexpected Magitek list code"
org $C14D2B
        jmp DrawListRow
DrawMagitekRowBody:             ; C1/4D2E, rest of the vanilla routine

; A button in the Magitek list: X = cursor index (vanilla: lda $62CA)
assert read3($C18667) == $62CAAD, "unexpected Magitek select code"
assert read2($C18694) == $95E6, "unexpected Magitek select code"
org $C18667
        jmp ListSelect
MagitekSelectResume:            ; C1/866A
org $C18694
MagitekSelectInvalid:           ; inc error sound, redraw cursor

; ------------------------------------------------------------------------------
; Battle: keep the targets chosen in the menu (remove Blitz from the
; retarget list, bit 2 of the second byte)

assert read4($C24E46) == $000B0480, "unexpected retarget command list"
org $C24E47
        db $00

; ------------------------------------------------------------------------------
; New code in the space of the old combo input (index registers are 16-bit
; in this part of the battle menu, A is 8-bit)

assert read2($C16F67) == $FFFF && read1($C17092) == $60, "unexpected Blitz combo code"
org $C16F67

; carry set if the current command is Blitz; preserves A, X, Y
IsBlitz:
        pha
        phy
        tdc                     ; clear B so GetActionBufPtr's tay is clean
        jsr GetActionBufPtr
        lda !ActionBufCmd,y
        and #$7F
        cmp #!CmdBlitz
        beq .yes
        clc
        bra .done
.yes:
        sec
.done:
        ply
        pla
        rts

DrawListRow:                    ; A = row (0-3)
        jsr IsBlitz
        bcs .blitz
        phy
        asl
        tay
        jmp DrawMagitekRowBody
.blitz:
        phy
        asl                     ; first Blitz on this row
        pha
        ldx #$000C
-       lda.l BlitzRowText,x
        sta !RowText,x
        dex
        bpl -
        pla
        ldx #$0004              ; left column
        jsr SetRowEntry
        inc
        ldx #$000A              ; right column
        jsr SetRowEntry
        jsr InitListTextTfr
        jsr DrawListText
        ply
        rts

; write the name of Blitz A at row offset X (blank if not learned); keeps A
SetRowEntry:
        pha
        phx
        rep #$20
        and #$00FF
        tax
        sep #$20
        lda.l BlitzBit,x
        plx
        and !KnownBlitzes
        beq .blank
        lda #$19                ; text code: attack name
        sta !RowText,x
        pla
        pha
        clc
        adc #!FirstBlitzAttack
        sta !RowText+1,x
        pla
        rts
.blank:
        lda #$FF                ; two spaces
        sta !RowText,x
        sta !RowText+1,x
        pla
        rts

ListSelect:                     ; X = cursor index
        jsr IsBlitz
        bcs .blitz
        lda $62CA
        jmp MagitekSelectResume
.blitz:
        lda !KnownBlitzes
        and.l BlitzBit,x
        beq .invalid
        inc !CursorSfx
        txa
        sta !AttackSel          ; Blitz index, the battle code adds $5D
        ldy $36
        lda.l BlitzTargetFlags,x
        sta !TargetFlagsSel
        jmp InitTargetSelect
.invalid:
        jmp MagitekSelectInvalid

; "{tab:4}{color:0x21}{attack}{tab:2}{color:0x21}{attack}": same spacing as
; the Rage list, whose 10-letter monster names line up like attack names
BlitzRowText:
        db $05, $04, $04, $21, $19, $00, $05, $02, $04, $21, $19, $00, $00

BlitzBit:
        db $01, $02, $04, $08, $10, $20, $40, $80

; target cursor flags: $43 one enemy, $6A all enemies, $2E all party members
BlitzTargetFlags:
        db $43                  ; Pummel
        db $43                  ; AuraBolt
        db $43                  ; Suplex
        db $6A                  ; Fire Dance
        db $2E                  ; Mantra
        db $6A                  ; Air Blade
        db $2E                  ; Spiraler
        db $43                  ; Bum Rush

assert pc() <= $C17093, "Blitz menu code overflows the old combo code"
