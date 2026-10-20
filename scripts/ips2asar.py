"""Convert IPS patches into asar files for the patch list.

Usage: python scripts/ips2asar.py spec.json

spec.json lists the IPS files in the order they are applied:
  {"rom": "rom/ff3_us_11.sfc", "ips_dir": "vendor/leet",
   "patches": [{"ips": "...", "out": "patches/bugfixes/x.asm",
                "title": "...", "desc": ["line", ...]}, ...]}
Several entries may share the same "out" file (stacked variants). An entry
without "out" is applied to the ROM state only (patch already ported by hand).

Each IPS is applied on top of the previous ones; only the bytes that change
relative to that state are emitted, so asar output matches applying the IPS
files in sequence. Every run of changed bytes gets an assertion on its
original first and last bytes, so a patch applied to the wrong ROM state
fails to assemble instead of corrupting it.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ips import apply_records, read_ips  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MAX_GAP = 4  # merge runs separated by up to this many unchanged bytes


def changed_runs(before, after):
    runs = []
    for i in range(min(len(before), len(after))):
        if before[i] == after[i]:
            continue
        if runs and i - runs[-1][1] <= MAX_GAP:
            runs[-1][1] = i + 1
        else:
            runs.append([i, i + 1])
    return runs


def snes(offset):
    return 0xC00000 + offset


def emit_runs(lines, before, after):
    for start, end in changed_runs(before, after):
        first = min(4, end - start)
        old_first = int.from_bytes(before[start:start + first], "little")
        cond = f"read{first}(${snes(start):06X}) == ${old_first:0{first * 2}X}"
        if end - start > 4:
            old_last = int.from_bytes(before[end - 4:end], "little")
            cond += f" && read4(${snes(end - 4):06X}) == ${old_last:08X}"
        lines.append(f'assert {cond}, "unexpected ROM state"')
        lines.append(f"org ${snes(start):06X}")
        chunk = after[start:end]
        for i in range(0, len(chunk), 16):
            lines.append("        db " + ", ".join(f"${b:02X}" for b in chunk[i:i + 16]))
        lines.append("")


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    rom = bytearray((ROOT / spec["rom"]).read_bytes())
    files = {}
    entries = spec["patches"]
    i = 0
    while i < len(entries):
        # consecutive entries with the same "out" become one diff: asar's
        # read functions see the ROM as it was before the file was applied
        group = [entries[i]]
        while i + len(group) < len(entries) and "out" in group[0] and                 entries[i + len(group)].get("out") == group[0]["out"]:
            group.append(entries[i + len(group)])
        i += len(group)
        before = bytes(rom)
        for entry in group:
            apply_records(rom, read_ips(ROOT / spec["ips_dir"] / entry["ips"]))
        first = group[0]
        if "out" not in first:  # already ported by hand, only update the state
            continue
        if first["out"] in files:
            sys.exit(f"{first['out']}: entries must be consecutive")
        lines = [f"; {first['title']}", ";"]
        lines += [f"; {d}" if d else ";" for d in first["desc"]]
        lines += [";", "; Generated from the released IPS by scripts/ips2asar.py:"]
        lines += [f";   {Path(e['ips']).name}" for e in group]
        lines += ["", "hirom", ""]
        emit_runs(lines, before, bytes(rom))
        files[first["out"]] = lines
    for out, lines in files.items():
        (ROOT / out).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
