"""Build the modded FF3 US 1.1 ROM and distributable patches.

Usage: python build.py [--rom PATH]

Reads the clean ROM (default: rom/ff3_us_11.sfc), applies every patch listed
in patches.txt in order with asar, then writes:
  build/ff3mods.sfc  - patched ROM
  build/ff3mods.ips  - IPS patch against the clean ROM
  build/ff3mods.bps  - BPS patch against the clean ROM
"""

import argparse
import hashlib
import shutil
import subprocess
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASAR = ROOT / "tools" / "asar" / "asar.exe"
FLIPS = ROOT / "tools" / "flips" / "flips.exe"
PATCH_LIST = ROOT / "patches.txt"
BUILD = ROOT / "build"

ROM_SIZE = 0x300000
ROM_CRC32 = 0xC0FA0464  # Final Fantasy III (USA) (Rev 1), unheadered
ROM_SHA1 = "057ada1c641e3e0b3ca34e6e4f4eb1b05a87143a"
COPIER_HEADER = 0x200


def load_clean_rom(path):
    data = path.read_bytes()
    if len(data) == ROM_SIZE + COPIER_HEADER:
        data = data[COPIER_HEADER:]
    if zlib.crc32(data) != ROM_CRC32 or hashlib.sha1(data).hexdigest() != ROM_SHA1:
        sys.exit(f"{path}: not a clean Final Fantasy III (USA) Rev 1 ROM")
    return data


def read_patch_list():
    patches = []
    for line in PATCH_LIST.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            patches.append(ROOT / line)
    return patches


def run(cmd):
    result = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    if output:
        print(output)
    if result.returncode != 0:
        sys.exit(f"failed: {' '.join(str(c) for c in cmd)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=Path, default=ROOT / "rom" / "ff3_us_11.sfc")
    args = parser.parse_args()

    clean = load_clean_rom(args.rom)
    BUILD.mkdir(exist_ok=True)
    clean_path = BUILD / "clean.sfc"
    out_path = BUILD / "ff3mods.sfc"
    clean_path.write_bytes(clean)
    shutil.copyfile(clean_path, out_path)

    for patch in read_patch_list():
        print(f"asar {patch.relative_to(ROOT)}")
        run([ASAR, "--no-title-check", "--fix-checksum=on", patch, out_path])

    for ext, flag in (("ips", "--ips"), ("bps", "--bps")):
        run([FLIPS, "--create", flag, clean_path, out_path, BUILD / f"ff3mods.{ext}"])

    print(f"built {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
