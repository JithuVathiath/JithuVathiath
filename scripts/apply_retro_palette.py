#!/usr/bin/env python3
"""Apply the profile's muted retro-Japanese palette to first-party SVGs."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = (
    "assets/hero/system-header.svg",
    "assets/dividers/signal-divider.svg",
    "assets/research/human-ai-decision-intelligence.svg",
    "assets/stack/tech-arsenal.svg",
    "assets/projects/mission-grid.svg",
    "assets/telemetry/contribution-stream.svg",
    "assets/telemetry/system-telemetry.svg",
    "assets/footer/transmission.svg",
)

PALETTE = {
    "#050816": "#1D1714",  # ink brown
    "#09122C": "#2B241F",  # charcoal umber
    "#17234A": "#4A3F35",  # weathered wood
    "#17366C": "#5C5146",  # warm slate
    "#6F84B4": "#7C756D",  # stone
    "#8FA8D8": "#A89E8C",  # aged paper shadow
    "#B8C4E0": "#D6C9B5",  # rice paper
    "#F4F7FF": "#F4EADB",  # warm ivory
    "#00F5FF": "#D8A25E",  # amber
    "#008CFF": "#B56A3C",  # rust
    "#38BDF8": "#6F8791",  # dusty indigo
    "#8B5CF6": "#596C78",  # blue-grey
    "#A78BFA": "#8E9682",  # pale sage
    "#FF2E88": "#C46D48",  # terracotta
    "#FF39E6": "#BC7C5C",  # clay
    "#FF5AA7": "#D28B66",  # faded coral
    "#39FF14": "#85966D",  # sage
    "#77FF62": "#9CAB83",  # pale moss
}


def apply() -> None:
    for relative in ASSETS:
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        for old, new in PALETTE.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    apply()
