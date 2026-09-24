#!/usr/bin/env python3
"""Build the warm retro-Japanese greeting animation used by the profile."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
HERO = ROOT / "assets/hero"
OUTPUT = HERO / "jithu-retro-studio-greeting.webp"
AVATAR = ROOT / "assets/portrait/jithu-retro-avatar.webp"
SIZE = (1280, 853)


def load(name: str) -> Image.Image:
    image = Image.open(HERO / name).convert("RGB")
    return image.resize(SIZE, Image.Resampling.LANCZOS)


def build() -> None:
    resting = load("jithu-retro-studio.webp")
    wave_a = load("jithu-retro-studio-wave-a.webp")
    wave_b = load("jithu-retro-studio-wave-b.webp")

    # Start the greeting as soon as the README loads. The two generated wave
    # poses share the same room, chair and monitor layout, so direct cuts keep
    # the subject crisp and avoid the yellow flash or cross-fade halo.
    frames: list[Image.Image] = [resting, wave_a, wave_b, wave_a, wave_b, wave_a, resting]
    durations: list[int] = [80, 330, 280, 280, 280, 380, 2700]

    frames[0].save(
        OUTPUT,
        format="WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        quality=84,
        method=6,
        minimize_size=True,
    )

    avatar = wave_a.crop((450, 190, 930, 670)).resize((512, 512), Image.Resampling.LANCZOS)
    avatar.save(AVATAR, format="WEBP", quality=88, method=6)


if __name__ == "__main__":
    build()
