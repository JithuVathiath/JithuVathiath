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


def warm_flash(image: Image.Image, strength: float) -> Image.Image:
    """Use a brief analog light blink to hide the pose cut without ghosting."""

    amber = Image.new("RGB", image.size, (216, 166, 102))
    return Image.blend(image, amber, strength)


def transition(start: Image.Image, end: Image.Image) -> list[Image.Image]:
    return (
        warm_flash(start, 0.12),
        warm_flash(start, 0.28),
        warm_flash(end, 0.28),
        warm_flash(end, 0.12),
    )


def build() -> None:
    resting = load("jithu-retro-studio.webp")
    wave_a = load("jithu-retro-studio-wave-a.webp")
    wave_b = load("jithu-retro-studio-wave-b.webp")

    frames: list[Image.Image] = [resting, resting]
    durations: list[int] = [220, 180]

    greeting = transition(resting, wave_a)
    frames.extend(greeting)
    durations.extend([45] * len(greeting))

    # A restrained wrist movement feels like a greeting, not a looping GIF.
    for _ in range(3):
        frames.extend((wave_a, wave_a, wave_b, wave_b))
        durations.extend((95, 95, 95, 95))

    returning = transition(wave_a, resting)
    frames.extend(returning)
    durations.extend([45] * len(returning))

    frames.extend([resting] * 10)
    durations.extend([220] * 10)

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
