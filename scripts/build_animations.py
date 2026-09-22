#!/usr/bin/env python3
"""Build restrained animated WebP assets from the generated source artwork."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]


def _save(frames: list[Image.Image], path: Path, duration: int, quality: int) -> None:
    frames[0].save(
        path,
        format="WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        quality=quality,
        method=6,
        minimize_size=True,
    )


def build_hero() -> None:
    source = Image.open(ROOT / "assets/hero/jithu-ai-lab.webp").convert("RGB")
    source = source.resize((1280, 853), Image.Resampling.LANCZOS)
    frames: list[Image.Image] = []

    for index in range(48):
        phase = index / 48
        pulse = 1.0 + 0.008 * math.sin(phase * math.tau)
        frame = ImageEnhance.Brightness(source).enhance(pulse).convert("RGBA")
        glow = Image.new("RGBA", frame.size)
        draw = ImageDraw.Draw(glow)

        monitor_alpha = int(9 + 9 * (1 + math.sin(phase * math.tau * 1.5)) / 2)
        draw.rectangle((122, 267, 1090, 510), fill=(0, 245, 255, monitor_alpha))

        scan_y = int((frame.height + 18) * phase) - 9
        draw.rectangle((0, scan_y, frame.width, scan_y + 5), fill=(0, 245, 255, 14))

        if index % 12 < 4:
            for x, y in ((1160, 390), (1176, 418), (1144, 446), (1200, 472)):
                draw.rectangle((x, y, x + 5, y + 5), fill=(57, 255, 20, 135))

        glow = glow.filter(ImageFilter.GaussianBlur(radius=1.1))
        frames.append(Image.alpha_composite(frame, glow).convert("RGB"))

    _save(frames, ROOT / "assets/hero/jithu-ai-lab-animated.webp", 120, 80)


def build_portrait() -> None:
    source = Image.open(ROOT / "assets/portrait/jithu-cyber-portrait.webp").convert("RGB")
    source = source.resize((560, 672), Image.Resampling.LANCZOS)
    frames: list[Image.Image] = []

    for index in range(45):
        phase = index / 45
        frame = source.convert("RGBA")
        overlay = Image.new("RGBA", frame.size)
        draw = ImageDraw.Draw(overlay)
        scan_y = int((frame.height + 36) * phase) - 18

        draw.rectangle((0, scan_y - 12, frame.width, scan_y + 12), fill=(0, 245, 255, 24))
        draw.rectangle((0, scan_y, frame.width, scan_y + 2), fill=(0, 245, 255, 190))

        if index in {6, 7, 21, 22, 36}:
            offset = 7 if index % 2 else -7
            y0 = 130 + (index * 17) % 300
            strip = frame.crop((0, y0, frame.width, y0 + 10))
            frame.alpha_composite(strip, (offset, y0))
            draw.rectangle((0, y0, 72, y0 + 2), fill=(255, 46, 136, 125))

        frames.append(Image.alpha_composite(frame, overlay).convert("RGB"))

    _save(frames, ROOT / "assets/portrait/jithu-cyber-portrait-animated.webp", 110, 82)


if __name__ == "__main__":
    build_hero()
    build_portrait()
