#!/usr/bin/env python3
"""Assemble generated blue poses using the original greeting's pose timings."""
from pathlib import Path
from PIL import Image

HERO = Path(__file__).resolve().parents[1] / "assets/hero"
SIZE = (1440, 480)


def build():
    poses = [Image.open(HERO / name).convert("RGB").resize(SIZE, Image.Resampling.LANCZOS)
             for name in ("jithu-blue-studio.webp", "jithu-blue-studio-wave-a.webp",
                          "jithu-blue-studio-wave-b.webp")]
    # Original greeting: desk, wave A/B/A/B/A, then return to the monitors.
    # Consecutive resting holds are combined; total loop remains 4.33 seconds.
    frames = [poses[index] for index in (0, 1, 2, 1, 2, 1, 0)]
    frames[0].save(HERO / "jithu-blue-studio-greeting.webp", format="WEBP",
                   save_all=True, append_images=frames[1:],
                   duration=[80, 330, 280, 280, 280, 380, 2700],
                   loop=0, quality=86, method=6, minimize_size=True)


if __name__ == "__main__":
    build()
