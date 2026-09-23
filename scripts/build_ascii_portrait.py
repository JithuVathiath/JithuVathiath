#!/usr/bin/env python3
"""Build a crisp, true-character monochrome portrait for the profile README."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/portrait/jithu-ascii-source-monochrome.webp"
OUTPUT = ROOT / "assets/portrait/jithu-ascii-portrait-bw.png"

FONT_PATH = Path("/System/Library/Fonts/Menlo.ttc")
PALETTE = " .:-=+*#%@"
COLS = 64
CELL_WIDTH = 14
LINE_HEIGHT = 25
FONT_SIZE = 21
MARGIN = 12


def build() -> None:
    source = Image.open(SOURCE).convert("L")
    # Keep the face, glasses, raised hand, and shoulders large enough to read
    # when GitHub displays the image at 340 px wide.
    source = source.crop((45, 10, source.width - 20, source.height - 39))
    source = ImageOps.autocontrast(source, cutoff=1)
    source = ImageEnhance.Contrast(source).enhance(1.12)
    source = source.filter(ImageFilter.UnsharpMask(radius=1.4, percent=135, threshold=3))

    rows = round((source.height / source.width) * COLS * CELL_WIDTH / LINE_HEIGHT)
    sample = source.resize((COLS, rows), Image.Resampling.LANCZOS)

    width = COLS * CELL_WIDTH + MARGIN * 2
    height = rows * LINE_HEIGHT + MARGIN * 2
    portrait = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(portrait)
    font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)

    for row in range(rows):
        for col in range(COLS):
            value = sample.getpixel((col, row))
            # Suppress the black background, lift facial midtones, and encode
            # brightness using glyph density. Every visible mark is a real
            # monospaced ASCII character rendered in white.
            normalized = max(0.0, min(1.0, (value - 6) / 249)) ** 0.95
            index = round(normalized * (len(PALETTE) - 1))
            char = PALETTE[index]
            if char == " ":
                continue
            x = MARGIN + col * CELL_WIDTH
            y = MARGIN + row * LINE_HEIGHT
            fill = round(96 + normalized * 159)
            draw.text((x, y), char, font=font, fill=fill, anchor="lt")

    portrait.save(OUTPUT, format="PNG", optimize=True)


if __name__ == "__main__":
    build()
