"""Lecture de la ROM Final Fantasy III (US) v1.1, sans header (HiROM).

Adresses SNES "bank/offset" (ex. 0xCF0000) -> offset fichier = addr - 0xC00000.
Les formats viennent du desassemblage everything8215/ff6 (src/data/*.asm).
"""

CRC32_CLEAN = 0xC0FA0464

# table de caracteres FF6 (text_en)
_CHARS = {}
for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    _CHARS[0x80 + i] = c
for i, c in enumerate("abcdefghijklmnopqrstuvwxyz"):
    _CHARS[0x9A + i] = c
for i, c in enumerate("0123456789"):
    _CHARS[0xB4 + i] = c
_CHARS.update({
    0xBE: "!", 0xBF: "?", 0xC0: "/", 0xC1: ":", 0xC2: '"', 0xC3: "'",
    0xC4: "-", 0xC5: ".", 0xC6: ",", 0xC7: "...", 0xC8: ";", 0xC9: "#",
    0xCA: "+", 0xCB: "(", 0xCC: ")", 0xCD: "%", 0xCE: "~", 0xD2: "=",
    0xFE: " ", 0xFF: "",
})


class Rom:
    def __init__(self, path):
        with open(path, "rb") as f:
            self.d = f.read()

    def off(self, addr):
        return addr - 0xC00000

    def b(self, addr, n=1):
        o = self.off(addr)
        return self.d[o:o + n]

    def u8(self, addr):
        return self.d[self.off(addr)]

    def u16(self, addr):
        o = self.off(addr)
        return self.d[o] | (self.d[o + 1] << 8)

    def u24(self, addr):
        o = self.off(addr)
        return self.d[o] | (self.d[o + 1] << 8) | (self.d[o + 2] << 16)

    def text(self, addr, n, skip_icon=False, stop_at_ff=False):
        raw = self.b(addr, n)
        if skip_icon:
            raw = raw[1:]
        out = []
        for c in raw:
            if c == 0xFF and stop_at_ff:
                break
            out.append(_CHARS.get(c, ""))
        return "".join(out).strip()


def bits(value, names):
    """Liste des noms dont le bit est actif (names[i] = bit i)."""
    return [n for i, n in enumerate(names) if n and value >> i & 1]


ELEMENTS = ["Fire", "Ice", "Lightning", "Poison", "Wind", "Holy", "Earth", "Water"]
# statuts 1-4 (32 bits : octet 0 = status1, 1 = status2, 2 = status3, 3 = status4)
STATUS = ["Blind", "Zombie", "Poison", "Magitek", "Vanish", "Imp", "Petrify", "Death",
          "Condemned", "Near Fatal", "Image", "Silence", "Berserk", "Confuse", "Sap", "Sleep",
          "Float(m)", "Regen", "Slow", "Haste", "Stop", "Shell", "Safe", "Reflect",
          "Rage", "Frozen", "Re-Raise", "Morph", "Control", "Hide", "Interceptor", "Float"]
STATUS[16] = "Dance/Fly"
