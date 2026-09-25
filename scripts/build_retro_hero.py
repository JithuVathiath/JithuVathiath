#!/usr/bin/env python3
"""Build the warm retro-Japanese greeting animation used by the profile."""

from __future__ import annotations

import math
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


def flying_birds(phase: float) -> Image.Image:
    """Render a small, naturally staggered flock crossing the city sky."""

    scale = 4
    canvas = Image.new("RGBA", (232 * scale, 259 * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    flock = (
        (0.00, 35, 1.00, 0.0),
        (0.17, 51, 0.82, 1.1),
        (0.38, 27, 0.70, 2.4),
        (0.60, 63, 0.88, 3.2),
        (0.81, 43, 0.62, 4.5),
    )
    for offset, base_y, bird_scale, flap_offset in flock:
        travel = (phase + offset) % 1.0
        x = (-18 + travel * 268) * scale
        y = (base_y + math.sin((phase * math.tau * 2) + flap_offset) * 2.2) * scale
        wing = math.sin((phase * math.tau * 8) + flap_offset)
        span = 7.0 * bird_scale * scale
        lift = (2.0 + 2.6 * wing) * bird_scale * scale
        body = 1.15 * bird_scale * scale
        colour = (48, 45, 41, 220)
        highlight = (112, 83, 60, 145)

        # Two curved-looking strokes form a readable bird silhouette at the
        # small README scale. Independent wing phases keep the flock organic.
        draw.line((x - span, y - lift, x, y + body, x + span, y - lift), fill=colour, width=max(2, round(1.35 * bird_scale * scale)), joint="curve")
        draw.line((x - span * .82, y - lift - scale * .35, x, y + body - scale * .25, x + span * .82, y - lift - scale * .35), fill=highlight, width=max(1, round(.45 * bird_scale * scale)), joint="curve")

    return canvas.resize((232, 259), Image.Resampling.LANCZOS)


def with_bird_window(image: Image.Image, phase: float) -> Image.Image:
    """Composite the clean skyline and flying birds only into the window panes."""

    left, top, right, bottom = scaled_window_box()
    width, height = right - left, bottom - top
    overlay = Image.open(HERO / "window-city-clean.webp").convert("RGBA")
    overlay.alpha_composite(flying_birds(phase))
    overlay = overlay.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)

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
    # Preserve the exact greeting-pose timings while splitting each hold into
    # short frames so the flock keeps moving throughout the full 4.33 s loop.
    pose_segments: list[tuple[Image.Image, int]] = [
        (resting, 80),
        (wave_a, 330),
        (wave_b, 280),
        (wave_a, 280),
        (wave_b, 280),
        (wave_a, 380),
        (resting, 180),
        (resting, 480),
        (resting, 2040),
    ]
    total_duration = sum(duration for _, duration in pose_segments)
    frames: list[Image.Image] = []
    durations: list[int] = []
    elapsed = 0
    for pose, segment_duration in pose_segments:
        parts = max(1, math.ceil(segment_duration / 160))
        base_duration, remainder = divmod(segment_duration, parts)
        for part in range(parts):
            duration = base_duration + (1 if part < remainder else 0)
            phase = elapsed / total_duration
            frames.append(with_bird_window(pose, phase))
            durations.append(duration)
            elapsed += duration

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
