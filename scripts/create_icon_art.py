#!/usr/bin/env python3
"""Generate the app icon assets for the Swift app."""

from __future__ import annotations

import math
import struct
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "swiftyapp" / "swiftyapp" / "Assets.xcassets" / "AppIcon.appiconset"

CONTENTS_JSON = """{
  "images" : [
    { "idiom" : "iphone", "size" : "20x20", "scale" : "2x", "filename" : "AppIcon-20@2x.png" },
    { "idiom" : "iphone", "size" : "20x20", "scale" : "3x", "filename" : "AppIcon-20@3x.png" },
    { "idiom" : "ipad", "size" : "20x20", "scale" : "1x", "filename" : "AppIcon-20-ipad.png" },
    { "idiom" : "ipad", "size" : "20x20", "scale" : "2x", "filename" : "AppIcon-20@2x-ipad.png" },
    { "idiom" : "iphone", "size" : "29x29", "scale" : "2x", "filename" : "AppIcon-29@2x.png" },
    { "idiom" : "iphone", "size" : "29x29", "scale" : "3x", "filename" : "AppIcon-29@3x.png" },
    { "idiom" : "ipad", "size" : "29x29", "scale" : "1x", "filename" : "AppIcon-29-ipad.png" },
    { "idiom" : "ipad", "size" : "29x29", "scale" : "2x", "filename" : "AppIcon-29@2x-ipad.png" },
    { "idiom" : "iphone", "size" : "40x40", "scale" : "2x", "filename" : "AppIcon-40@2x.png" },
    { "idiom" : "iphone", "size" : "40x40", "scale" : "3x", "filename" : "AppIcon-40@3x.png" },
    { "idiom" : "ipad", "size" : "40x40", "scale" : "1x", "filename" : "AppIcon-40-ipad.png" },
    { "idiom" : "ipad", "size" : "40x40", "scale" : "2x", "filename" : "AppIcon-40@2x-ipad.png" },
    { "idiom" : "ipad", "size" : "76x76", "scale" : "1x", "filename" : "AppIcon-76-ipad.png" },
    { "idiom" : "ipad", "size" : "76x76", "scale" : "2x", "filename" : "AppIcon-76@2x-ipad.png" },
    { "idiom" : "ipad", "size" : "83.5x83.5", "scale" : "2x", "filename" : "AppIcon-83.5@2x-ipad.png" },
    { "idiom" : "iphone", "size" : "60x60", "scale" : "2x", "filename" : "AppIcon-60@2x.png" },
    { "idiom" : "iphone", "size" : "60x60", "scale" : "3x", "filename" : "AppIcon-60@3x.png" },
    { "idiom" : "ios-marketing", "size" : "1024x1024", "scale" : "1x", "filename" : "AppIcon-1024.png" }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
"""

SIZES = {
    "AppIcon-20@2x.png": 40,
    "AppIcon-20@3x.png": 60,
    "AppIcon-20-ipad.png": 20,
    "AppIcon-20@2x-ipad.png": 40,
    "AppIcon-29@2x.png": 58,
    "AppIcon-29@3x.png": 87,
    "AppIcon-29-ipad.png": 29,
    "AppIcon-29@2x-ipad.png": 58,
    "AppIcon-40@2x.png": 80,
    "AppIcon-40@3x.png": 120,
    "AppIcon-40-ipad.png": 40,
    "AppIcon-40@2x-ipad.png": 80,
    "AppIcon-76-ipad.png": 76,
    "AppIcon-76@2x-ipad.png": 152,
    "AppIcon-83.5@2x-ipad.png": 167,
    "AppIcon-60@2x.png": 120,
    "AppIcon-60@3x.png": 180,
    "AppIcon-1024.png": 1024,
}


def clamp(value: float) -> int:
    return max(0, min(255, int(value)))


def pixel_color(nx: float, ny: float) -> tuple[int, int, int, int]:
    # Background gradient.
    r = 14 + 18 * nx + 28 * ny
    g = 20 + 12 * nx + 18 * ny
    b = 34 + 40 * nx + 66 * ny

    # Warm glow behind the mark.
    dx = nx - 0.46
    dy = ny - 0.42
    dist = math.sqrt(dx * dx + dy * dy)
    glow = max(0.0, 1.0 - dist / 0.48)
    r += 58 * glow
    g += 22 * glow
    b += 74 * glow

    # Dark rounded panel.
    panel_dx = abs(nx - 0.5)
    panel_dy = abs(ny - 0.5)
    panel = 1.0 if panel_dx <= 0.34 and panel_dy <= 0.34 else 0.0
    if panel:
        edge = max(panel_dx / 0.34, panel_dy / 0.34)
        panel = max(0.0, 1.0 - edge)
        r = r * 0.48 + 44 * panel
        g = g * 0.48 + 54 * panel
        b = b * 0.48 + 82 * panel

    # Orb ring and the stylized R.
    outer = math.sqrt((nx - 0.50) ** 2 + (ny - 0.50) ** 2)
    if 0.16 < outer < 0.22:
        r, g, b = 235, 175, 82
    elif outer <= 0.16:
        r, g, b = 50, 62, 92

    if 0.33 <= nx <= 0.40 and 0.29 <= ny <= 0.71:
        r, g, b = 248, 250, 255
    if 0.40 <= nx <= 0.58 and 0.29 <= ny <= 0.37:
        r, g, b = 248, 250, 255
    if 0.40 <= nx <= 0.53 and 0.44 <= ny <= 0.52:
        r, g, b = 248, 250, 255
    if 0.42 <= nx <= 0.59 and 0.52 <= ny <= 0.71:
        diag = (nx - 0.42) * 1.15 + 0.52
        if diag - 0.045 <= ny <= diag + 0.028:
            r, g, b = 248, 250, 255

    # Hollow bowl.
    hole = (nx - 0.48) ** 2 / (0.12**2) + (ny - 0.44) ** 2 / (0.09**2) <= 1.0
    if hole:
        r, g, b = 50, 62, 92

    # Shine.
    if 0.30 <= ny <= 0.34 and 0.34 <= nx <= 0.53:
        r += 16
        g += 16
        b += 20

    return clamp(r), clamp(g), clamp(b), 255


def write_png(path: Path, size: int) -> None:
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        ny = y / (size - 1)
        for x in range(size):
            nx = x / (size - 1)
            raw.extend(pixel_color(nx, ny))

    png = bytearray(b"\x89PNG\r\n\x1a\n")

    def chunk(tag: bytes, data: bytes) -> None:
        png.extend(struct.pack(">I", len(data)))
        png.extend(tag)
        png.extend(data)
        crc = zlib.crc32(tag)
        crc = zlib.crc32(data, crc)
        png.extend(struct.pack(">I", crc & 0xFFFFFFFF))

    chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
    chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    chunk(b"IEND", b"")
    path.write_bytes(png)


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    (ASSET_DIR / "Contents.json").write_text(CONTENTS_JSON, encoding="utf-8")

    for filename, size in SIZES.items():
        write_png(ASSET_DIR / filename, size)


if __name__ == "__main__":
    main()
