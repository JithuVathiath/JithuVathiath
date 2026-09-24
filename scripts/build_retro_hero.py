#!/usr/bin/env python3
"""Build the warm retro-Japanese greeting animation used by the profile."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


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


def atomic_breath(progress: float, phase: float = 0.0) -> Image.Image:
    """Render one smooth atomic-breath state over the unchanged window crop."""

    scale = 4
    width, height = 232 * scale, 259 * scale
    breath = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    if progress <= 0:
        return breath

    # Begin inside the jaw so even the shortest ignition state stays connected
    # to the existing mouth glow instead of reading as a detached white dot.
    mouth_x, mouth_y = 87 * scale, 53 * scale
    length = max(9, round(126 * progress)) * scale
    end_x = min(width - 4 * scale, mouth_x + length)
    steps = max(12, round((end_x - mouth_x) / (3 * scale)))
    points: list[tuple[float, float]] = []
    for index in range(steps + 1):
        t = index / steps
        x = mouth_x + (end_x - mouth_x) * t
        y = mouth_y + (1.35 * scale * (1 - t)) * __import__("math").sin(t * 9 + phase)
        points.append((x, y))

    def ribbon(half_width: float) -> list[tuple[float, float]]:
        upper: list[tuple[float, float]] = []
        lower: list[tuple[float, float]] = []
        for index, (x, y) in enumerate(points):
            t = index / steps
            taper = max(0.10, (1 - t) ** 0.42)
            flare = 0.45 + 0.55 * min(1.0, t * 4)
            radius = half_width * scale * taper * flare
            upper.append((x, y - radius))
            lower.append((x, y + radius))
        return upper + list(reversed(lower))

    glow = Image.new("RGBA", breath.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.polygon(ribbon(9.5), fill=(58, 192, 255, 150))
    glow_draw.ellipse(
        (mouth_x - 8 * scale, mouth_y - 8 * scale, mouth_x + 14 * scale, mouth_y + 8 * scale),
        fill=(75, 205, 255, 170),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(5.5 * scale))
    breath.alpha_composite(glow)

    stream = Image.new("RGBA", breath.size, (0, 0, 0, 0))
    stream_draw = ImageDraw.Draw(stream)
    stream_draw.polygon(ribbon(5.2), fill=(92, 213, 255, 205))
    stream_draw.line(points, fill=(225, 249, 255, 245), width=round(2.4 * scale))
    stream = stream.filter(ImageFilter.GaussianBlur(0.65 * scale))
    breath.alpha_composite(stream)

    detail = ImageDraw.Draw(breath)
    for offset, alpha in ((-7, 125), (7, 100)):
        wisp: list[tuple[float, float]] = []
        for index, (x, y) in enumerate(points):
            t = index / steps
            if t < 0.18:
                continue
            wave = __import__("math").sin(t * 15 + phase + offset) * 1.8 * scale
            wisp.append((x, y + offset * scale * (0.45 + 0.55 * t) + wave))
        if len(wisp) > 1:
            detail.line(wisp, fill=(119, 225, 255, alpha), width=scale)

    return breath.resize((232, 259), Image.Resampling.LANCZOS)


def with_godzilla_window(image: Image.Image, progress: float, phase: float = 0.0) -> Image.Image:
    """Composite only the two outdoor window panes onto an existing frame."""

    left, top, right, bottom = scaled_window_box()
    width, height = right - left, bottom - top
    overlay = Image.open(HERO / "godzilla-window-charge.webp").convert("RGBA")
    overlay.alpha_composite(atomic_breath(progress, phase))
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
    # Preserve the original greeting frame-for-frame. Only the outdoor window
    # panes receive the charge -> emerging flame -> full beam sequence. The
    # final resting hold is split into identical body frames so the fire can
    # pulse without changing anything else in the image.
    # Keep the original body-pose timings while adding enough breath states for
    # a fluid ignition, extension, sustained fire and decay. The longer pose
    # holds are split into identical body frames, so the wave itself is not
    # sped up and only the window animation gains extra motion.
    sequence: list[tuple[Image.Image, float, float, int]] = [
        (resting, 0.00, 0.0, 80),
        (wave_a, 0.05, 0.2, 110), (wave_a, 0.12, 0.5, 110), (wave_a, 0.22, 0.8, 110),
        (wave_b, 0.35, 1.1, 140), (wave_b, 0.50, 1.4, 140),
        (wave_a, 0.68, 1.7, 140), (wave_a, 0.84, 2.0, 140),
        (wave_b, 0.96, 2.3, 140), (wave_b, 1.00, 2.6, 140),
        (wave_a, 0.96, 2.9, 127), (wave_a, 0.91, 3.2, 127), (wave_a, 0.84, 3.5, 126),
        (resting, 0.66, 3.8, 90), (resting, 0.46, 4.1, 90),
        (resting, 0.31, 4.4, 120), (resting, 0.18, 4.7, 120),
        (resting, 0.08, 5.0, 120), (resting, 0.00, 5.3, 120),
        (resting, 0.00, 0.0, 2040),
    ]
    frames = [with_godzilla_window(pose, progress, phase) for pose, progress, phase, _ in sequence]
    durations = [duration for _, _, _, duration in sequence]

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
