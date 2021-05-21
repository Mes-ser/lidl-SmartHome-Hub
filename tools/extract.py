#!/usr/bin/env python3

import sys

class FirmwarePart:
    def __init__(self, name, offset, size):
        self.name = name
        self.offset = offset
        self.size = size

firmware_parts = [
    FirmwarePart("bootloader", 0x0, 0x20000),
    FirmwarePart("kernel", 0x20000, 0x1e0000),
    FirmwarePart("rootfs", 0x200000, 0x200000),
    FirmwarePart("tuya-label", 0x400000, 0x20000),
    FirmwarePart("jffs2-fs", 0x420000, 0xbe0000 )
    
]

if sys.argv[1] == "unpack":
    f = open(sys.argv[2], "rb")
    for part in firmware_parts:
        outfile = open(part.name, "wb")
        f.seek(part.offset, 0)
        data = f.read(part.size)
        outfile.write(data)
        outfile.close()
        print(f"Wrote {part.name} - {hex(len(data))} bytes")
elif sys.argv[1] == "pack":
    f = open(sys.argv[2], "wb")
    for part in firmware_parts[0:]:
        i = open(part.name, "rb")
        data = i.read()
        f.write(data)
        padding = (part.size - len(data))
        print(f"Wrote {part.name} - {hex(len(data))} bytes")
        print(f"Padding: {hex(padding)}")
        f.write(b'\x00' * padding)
