"""Minimal IPS reader shared by the helper scripts."""

from pathlib import Path


def read_ips(path):
    """Return a list of (offset, bytes) records from an IPS file."""
    data = Path(path).read_bytes()
    if data[:5] != b"PATCH":
        raise ValueError(f"{path}: not an IPS file")
    pos = 5
    records = []
    while True:
        if data[pos:pos + 3] == b"EOF":
            return records
        offset = int.from_bytes(data[pos:pos + 3], "big")
        size = int.from_bytes(data[pos + 3:pos + 5], "big")
        pos += 5
        if size:
            records.append((offset, data[pos:pos + size]))
            pos += size
        else:  # RLE record
            count = int.from_bytes(data[pos:pos + 2], "big")
            records.append((offset, data[pos + 2:pos + 3] * count))
            pos += 3


def apply_records(rom, records):
    for offset, chunk in records:
        if offset + len(chunk) > len(rom):
            rom.extend(b"\xff" * (offset + len(chunk) - len(rom)))
        rom[offset:offset + len(chunk)] = chunk
