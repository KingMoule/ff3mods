; Locke: better odds for the rare steal
;
; Once a Steal (or Mug) succeeds, the game takes the rare item with a 32/256
; (1/8) chance, otherwise the common one. The rare item now comes out with a
; 64/256 (1/4) chance. The success roll itself is unchanged:
; (thief level + 50 - target level)%, doubled by the Sneak Ring.
; If the chosen slot is empty the steal still fails, as in vanilla.

hirom

; phy / jsr Rand / cmp #$20 / bcc + / iny / + lda StealItems,y
assert read4($C239D8) == $4B5A205A && read4($C239DC) == $019020C9, "unexpected steal code"
org $C239DD
        db $40
