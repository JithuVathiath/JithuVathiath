#!/usr/bin/env python3
"""Reveal the unchanged monochrome ASCII portrait from top to bottom."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/portrait/jithu-ascii-portrait-bw.png"
OUTPUT = ROOT / "assets/portrait/jithu-ascii-portrait-reveal.webp"
STEPS = 14


def build() -> None:
    portrait = Image.open(SOURCE).convert("RGB")
    blank = Image.new("RGB", portrait.size, "black")
    frames: list[Image.Image] = [blank]
    durations: list[int] = [100]

    for step in range(1, STEPS + 1):
        boundary = round(portrait.height * step / STEPS)
        frame = blank.copy()
        frame.paste(portrait.crop((0, 0, portrait.width, boundary)), (0, 0))
        frames.append(frame)
        durations.append(85)

    # Let the complete portrait remain readable before the reveal restarts.
    frames.append(portrait)
    durations.append(3000)

    frames[0].save(
        OUTPUT,
        format="WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        lossless=True,
        method=6,
    )


if __name__ == "__main__":
    build()
