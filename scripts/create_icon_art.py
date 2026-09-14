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


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def smoothstep(edge0: float, edge1: float, x: float) -> float:
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)


def mix_color(base: tuple[float, float, float], color: tuple[int, int, int], alpha: float) -> tuple[float, float, float]:
    return (
        lerp(base[0], color[0], alpha),
        lerp(base[1], color[1], alpha),
        lerp(base[2], color[2], alpha),
    )


def rotated_ellipse(px: float, py: float, cx: float, cy: float, rx: float, ry: float, angle_deg: float) -> float:
    angle = math.radians(angle_deg)
    dx = px - cx
    dy = py - cy
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    x = dx * cos_a + dy * sin_a
    y = -dx * sin_a + dy * cos_a
    return (x / rx) ** 2 + (y / ry) ** 2


def rounded_rect_mask(px: float, py: float, cx: float, cy: float, half_w: float, half_h: float, radius: float) -> float:
    dx = abs(px - cx) - half_w + radius
    dy = abs(py - cy) - half_h + radius
    ax = max(dx, 0.0)
    ay = max(dy, 0.0)
    outside = math.sqrt(ax * ax + ay * ay) - radius
    inside = min(max(dx, dy), 0.0)
    return outside + inside


def pixel_color(nx: float, ny: float) -> tuple[int, int, int, int]:
    # Background: dark, slightly iridescent glass.
    r = lerp(12, 20, ny) + 10 * nx
    g = lerp(16, 24, ny) + 12 * nx
    b = lerp(30, 58, ny) + 18 * nx

    # Soft nebula glow.
    glow = max(0.0, 1.0 - math.hypot(nx - 0.42, ny - 0.40) / 0.62)
    r += 42 * glow
    g += 24 * glow
    b += 70 * glow

    # Glass panel.
    panel_dist = rounded_rect_mask(nx, ny, 0.5, 0.5, 0.36, 0.36, 0.12)
    panel_alpha = smoothstep(0.10, -0.01, panel_dist)
    if panel_alpha > 0:
        r, g, b = mix_color((r, g, b), (20, 30, 54), panel_alpha * 0.78)
        r, g, b = mix_color((r, g, b), (90, 112, 178), panel_alpha * 0.20)

    # Vignette and shadow.
    vignette = max(0.0, 1.0 - math.hypot(nx - 0.5, ny - 0.5) / 0.88)
    r *= 0.88 + 0.12 * vignette
    g *= 0.90 + 0.10 * vignette
    b *= 0.94 + 0.06 * vignette

    # Main swifty ribbon.
    main_outer = rotated_ellipse(nx, ny, 0.46, 0.46, 0.29, 0.14, -28)
    main_inner = rotated_ellipse(nx, ny, 0.50, 0.49, 0.20, 0.08, -28)
    main_fill = smoothstep(1.18, 0.92, main_outer) * (1.0 - smoothstep(1.12, 0.97, main_inner))
    if main_fill > 0:
        r, g, b = mix_color((r, g, b), (235, 245, 255), main_fill * 0.92)
        r, g, b = mix_color((r, g, b), (111, 190, 255), main_fill * 0.16)

    # Secondary warm ribbon to give it a more artsy, layered feel.
    accent_outer = rotated_ellipse(nx, ny, 0.55, 0.54, 0.23, 0.10, 154)
    accent_inner = rotated_ellipse(nx, ny, 0.52, 0.51, 0.16, 0.06, 154)
    accent_fill = smoothstep(1.20, 0.96, accent_outer) * (1.0 - smoothstep(1.12, 0.98, accent_inner))
    if accent_fill > 0:
        r, g, b = mix_color((r, g, b), (255, 196, 124), accent_fill * 0.84)
        r, g, b = mix_color((r, g, b), (255, 142, 96), accent_fill * 0.18)

    # A subtle trailing arc.
    trail = rotated_ellipse(nx, ny, 0.56, 0.41, 0.22, 0.07, 24)
    trail_alpha = smoothstep(1.04, 0.96, trail) * (1.0 - smoothstep(1.20, 1.02, trail))
    if trail_alpha > 0:
        r, g, b = mix_color((r, g, b), (164, 232, 255), trail_alpha * 0.34)

    # Sparkle and orbit points.
    spark = max(0.0, 1.0 - math.hypot(nx - 0.78, ny - 0.25) / 0.04)
    if spark > 0:
        r, g, b = mix_color((r, g, b), (255, 250, 238), spark)
        r, g, b = mix_color((r, g, b), (255, 182, 92), spark * 0.55)

    orb = max(0.0, 1.0 - math.hypot(nx - 0.28, ny - 0.70) / 0.028)
    if orb > 0:
        r, g, b = mix_color((r, g, b), (255, 173, 92), orb)

    # Gentle highlight line near the top.
    shine = smoothstep(0.34, 0.30, ny) * smoothstep(0.34, 0.48, nx) * smoothstep(0.58, 0.34, nx)
    if shine > 0:
        r, g, b = mix_color((r, g, b), (255, 255, 255), shine * 0.10)

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
