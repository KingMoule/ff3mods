"""Check that build/ff3mods.sfc matches the vendor IPS files applied in order.

Usage: python scripts/verify_ips.py scripts/bugfixes_level1.json

Prints every byte range where the build differs from the clean ROM with the
IPS files applied in sequence; these should only be our own patches and the
SNES header checksum.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ips import apply_records, read_ips  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
rom = bytearray((ROOT / spec["rom"]).read_bytes())
for entry in spec["patches"]:
    apply_records(rom, read_ips(ROOT / spec["ips_dir"] / entry["ips"]))
build = (ROOT / "build" / "ff3mods.sfc").read_bytes()

start = None
for i in range(len(rom) + 1):
    differs = i < len(rom) and rom[i] != build[i]
    if differs and start is None:
        start = i
    elif not differs and start is not None:
        print(f"C{start >> 16:X}/{start & 0xFFFF:04X}-C{(i - 1) >> 16:X}/{(i - 1) & 0xFFFF:04X}")
        start = None
