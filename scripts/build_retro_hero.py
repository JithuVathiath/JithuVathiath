#!/usr/bin/env python3
"""Build the warm retro-Japanese greeting animation used by the profile."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
HERO = ROOT / "assets/hero"
OUTPUT = HERO / "jithu-retro-studio-greeting.webp"
AVATAR = ROOT / "assets/portrait/jithu-retro-avatar.webp"
SIZE = (1280, 853)
SOURCE_SIZE = (1536, 1024)
SOURCE_WINDOW_BOX = (1304, 87, 1536, 346)


def scaled_window_box() -> tuple[int, int, int, int]:
    x_scale = SIZE[0] / SOURCE_SIZE[0]
    y_scale = SIZE[1] / SOURCE_SIZE[1]
    left, top, right, bottom = SOURCE_WINDOW_BOX
    return (
        round(left * x_scale),
        round(top * y_scale),
        round(right * x_scale),
        round(bottom * y_scale),
    )


def load(name: str) -> Image.Image:
    image = Image.open(HERO / name).convert("RGB")
    return image.resize(SIZE, Image.Resampling.LANCZOS)


def with_godzilla_window(image: Image.Image, state: str) -> Image.Image:
    """Composite only the two outdoor window panes onto an existing frame."""

    left, top, right, bottom = scaled_window_box()
    width, height = right - left, bottom - top
    overlay = Image.open(HERO / f"godzilla-window-{state}.webp").convert("RGB")
    overlay = overlay.resize((width, height), Image.Resampling.LANCZOS)

    # The crop also contains the window mullion. Mask it out so the original
    # frame, curtain, blind, plant and room remain untouched.
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((round(8 / 232 * width), 0, round(160 / 232 * width), height), fill=255)
    draw.rectangle((round(178 / 232 * width), 0, width, height), fill=255)

    result = image.copy()
    result.paste(overlay, (left, top), mask)
    return result


def build() -> None:
    resting = load("jithu-retro-studio.webp")
    wave_a = load("jithu-retro-studio-wave-a.webp")
    wave_b = load("jithu-retro-studio-wave-b.webp")

    # Start the greeting as soon as the README loads. The two generated wave
    # poses share the same room, chair and monitor layout, so direct cuts keep
    # the subject crisp and avoid the yellow flash or cross-fade halo.
    # Preserve the original greeting frame-for-frame. Only the outdoor window
    # panes receive the charge -> emerging flame -> full beam sequence. The
    # final resting hold is split into identical body frames so the fire can
    # pulse without changing anything else in the image.
    frames: list[Image.Image] = [
        with_godzilla_window(resting, "charge"),
        with_godzilla_window(wave_a, "charge"),
        with_godzilla_window(wave_b, "charge"),
        with_godzilla_window(wave_a, "emerge"),
        with_godzilla_window(wave_b, "full"),
        with_godzilla_window(wave_a, "full"),
        with_godzilla_window(resting, "emerge"),
        with_godzilla_window(resting, "full"),
        with_godzilla_window(resting, "charge"),
    ]
    durations: list[int] = [80, 330, 280, 280, 280, 380, 180, 480, 2040]

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
