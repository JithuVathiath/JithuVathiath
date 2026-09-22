#!/usr/bin/env python3
"""Build animated WebP assets from the generated source artwork."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


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

    neural_nodes = (
        (178, 322),
        (211, 342),
        (247, 320),
        (278, 354),
        (316, 333),
        (193, 384),
        (231, 407),
        (270, 390),
        (320, 412),
    )
    neural_edges = (
        (0, 1),
        (0, 2),
        (1, 2),
        (1, 5),
        (1, 6),
        (2, 3),
        (2, 6),
        (3, 4),
        (3, 7),
        (4, 8),
        (5, 6),
        (6, 7),
        (7, 8),
    )
    chart_points = (
        (691, 232),
        (709, 220),
        (727, 226),
        (745, 202),
        (763, 212),
        (781, 180),
        (799, 190),
        (817, 160),
        (835, 171),
    )
    rain_streaks = (
        (1077, 52),
        (1108, 141),
        (1137, 88),
        (1168, 205),
        (1197, 119),
        (1224, 37),
        (1252, 171),
    )

    for index in range(60):
        phase = index / 60
        frame = source.convert("RGBA")
        bloom = Image.new("RGBA", frame.size)
        bloom_draw = ImageDraw.Draw(bloom)
        detail = Image.new("RGBA", frame.size)
        draw = ImageDraw.Draw(detail)

        # Keep the scene stable while each monitor emits its own soft pulse.
        cyan_alpha = int(7 + 7 * (1 + math.sin(phase * math.tau * 2)) / 2)
        magenta_alpha = int(5 + 7 * (1 + math.sin(phase * math.tau * 2 + 2.1)) / 2)
        bloom_draw.rectangle((127, 280, 390, 474), fill=(0, 245, 255, cyan_alpha))
        bloom_draw.rectangle((404, 280, 817, 495), fill=(255, 46, 136, magenta_alpha))
        bloom_draw.rectangle((828, 284, 1124, 500), fill=(0, 245, 255, cyan_alpha))

        # Neural-network traffic visibly travels between nodes on the left display.
        for start, end in neural_edges:
            draw.line((neural_nodes[start], neural_nodes[end]), fill=(24, 126, 202, 105), width=2)
        for node_index, (x, y) in enumerate(neural_nodes):
            node_pulse = (index + node_index * 5) % 30
            colour = (255, 46, 216, 230) if node_index % 3 == 0 else (0, 245, 255, 230)
            radius = 4 if node_pulse < 8 else 3
            bloom_draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(*colour[:3], 95))
            draw.rectangle((x - radius, y - radius, x + radius, y + radius), fill=colour)
        for signal in range(3):
            edge_index = (index // 10 + signal * 4) % len(neural_edges)
            start, end = neural_edges[edge_index]
            travel = ((index % 10) + signal * 3) / 10
            x = int(neural_nodes[start][0] + (neural_nodes[end][0] - neural_nodes[start][0]) * travel)
            y = int(neural_nodes[start][1] + (neural_nodes[end][1] - neural_nodes[start][1]) * travel)
            bloom_draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(0, 245, 255, 150))
            draw.rectangle((x - 3, y - 3, x + 3, y + 3), fill=(220, 255, 255, 255))

        # Code lines scroll on the centre display and a block cursor keeps typing.
        code_palette = ((0, 245, 255, 215), (255, 46, 216, 210), (72, 148, 255, 210))
        for row in range(10):
            y = 302 + ((row * 15 - (index * 2)) % 150)
            indent = (row % 4) * 8
            length = 28 + ((row * 17) % 74)
            colour = code_palette[row % len(code_palette)]
            draw.rectangle((427 + indent, y, 427 + indent + length, y + 3), fill=colour)
            if row % 3 == 0:
                draw.rectangle((535, y, 555 + (row % 2) * 14, y + 3), fill=(105, 126, 205, 190))
        if index % 12 < 7:
            cursor_y = 302 + ((8 * 15 - (index * 2)) % 150)
            bloom_draw.rectangle((568, cursor_y - 4, 576, cursor_y + 9), fill=(0, 245, 255, 145))
            draw.rectangle((568, cursor_y, 575, cursor_y + 6), fill=(223, 255, 255, 250))

        # Market/telemetry graph: bright trace, live candles, and a moving data point.
        draw.line(chart_points, fill=(0, 245, 255, 225), width=3)
        draw.line(tuple((x, y + 18) for x, y in chart_points), fill=(255, 46, 216, 155), width=2)
        segment = int(phase * (len(chart_points) - 1))
        segment_phase = phase * (len(chart_points) - 1) - segment
        x0, y0 = chart_points[segment]
        x1, y1 = chart_points[min(segment + 1, len(chart_points) - 1)]
        trace_x = int(x0 + (x1 - x0) * segment_phase)
        trace_y = int(y0 + (y1 - y0) * segment_phase)
        bloom_draw.ellipse((trace_x - 11, trace_y - 11, trace_x + 11, trace_y + 11), fill=(0, 245, 255, 175))
        draw.rectangle((trace_x - 4, trace_y - 4, trace_x + 4, trace_y + 4), fill=(240, 255, 255, 255))
        for candle in range(6):
            x = 704 + candle * 23
            wobble = int(5 * math.sin(phase * math.tau * 2 + candle))
            y = 128 + ((candle * 17) % 31) + wobble
            colour = (47, 255, 156, 225) if candle % 2 == 0 else (255, 46, 136, 225)
            draw.line((x + 3, y - 8, x + 3, y + 20), fill=colour, width=2)
            draw.rectangle((x, y, x + 6, y + 12), fill=colour)

        # Workflow statuses on the right monitor complete in sequence.
        for status_index, (x, y) in enumerate(((1043, 346), (1074, 381), (1043, 420))):
            active = (index // 10) % 3 == status_index
            colour = (57, 255, 20, 245) if active else (0, 245, 255, 135)
            bloom_draw.rectangle((x - 5, y - 5, x + 13, y + 13), fill=(*colour[:3], 95 if active else 35))
            draw.rectangle((x, y, x + 8, y + 8), outline=colour, width=2)
            if active:
                draw.line((x + 2, y + 4, x + 4, y + 6, x + 7, y + 2), fill=colour, width=2)

        # Server activity, keyboard taps, city windows, and digital rain make the lab breathe.
        for led_index, (x, y) in enumerate(
            ((1152, 371), (1181, 393), (1210, 417), (1138, 446), (1174, 473), (1217, 500), (1157, 530))
        ):
            on = (index + led_index * 7) % 20 < 11
            colour = (57, 255, 20, 240) if on else (0, 245, 255, 70)
            bloom_draw.rectangle((x - 4, y - 4, x + 8, y + 7), fill=(*colour[:3], 80 if on else 18))
            draw.rectangle((x, y, x + 4, y + 3), fill=colour)
        for key_index, (x, y) in enumerate(((478, 542), (501, 550), (524, 540), (547, 549), (570, 541), (593, 550))):
            if (index // 3 + key_index * 2) % 13 < 3:
                colour = (0, 245, 255, 225) if key_index % 2 else (255, 46, 216, 215)
                bloom_draw.rectangle((x - 3, y - 3, x + 12, y + 9), fill=(*colour[:3], 85))
                draw.rectangle((x, y, x + 8, y + 5), fill=colour)
        for window_index, (x, y) in enumerate(((1102, 111), (1136, 151), (1174, 91), (1211, 184), (1244, 126))):
            lit = (index // 8 + window_index) % 4 != 0
            colour = (255, 46, 216, 180) if window_index % 2 else (0, 245, 255, 185)
            draw.rectangle((x, y, x + 3, y + 10), fill=colour if lit else (12, 45, 92, 120))
        for streak_index, (x, start_y) in enumerate(rain_streaks):
            y = 52 + ((start_y + index * (5 + streak_index % 3)) % 245)
            draw.line((x, y, x - 3, y + 15), fill=(85, 211, 255, 90), width=1)

        # Rotating hologram cube on the desk.
        cube_cx, cube_cy = 1221, 574
        skew = int(9 * math.sin(phase * math.tau))
        front = (
            (cube_cx - 25 + skew, cube_cy - 24),
            (cube_cx + 25, cube_cy - 24 + skew),
            (cube_cx + 25 - skew, cube_cy + 24),
            (cube_cx - 25, cube_cy + 24 - skew),
        )
        back = tuple((x - 10, y - 12) for x, y in front)
        hologram_colour = (125, 84, 255, 205)
        bloom_draw.polygon(front, outline=(125, 84, 255, 150), width=5)
        draw.line(front + (front[0],), fill=hologram_colour, width=2)
        draw.line(back + (back[0],), fill=(0, 245, 255, 180), width=2)
        for front_point, back_point in zip(front, back):
            draw.line((front_point, back_point), fill=(255, 46, 216, 180), width=2)

        # A restrained scanline ties the individual animations together.
        scan_y = 270 + int(260 * ((index % 30) / 30))
        draw.rectangle((120, scan_y, 1128, scan_y + 2), fill=(0, 245, 255, 28))

        bloom = bloom.filter(ImageFilter.GaussianBlur(radius=4.2))
        frame = Image.alpha_composite(frame, bloom)
        frame = Image.alpha_composite(frame, detail)
        frames.append(frame.convert("RGB"))

    _save(frames, ROOT / "assets/hero/jithu-ai-lab-live.webp", 100, 82)


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
