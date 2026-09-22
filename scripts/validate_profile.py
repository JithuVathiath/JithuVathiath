#!/usr/bin/env python3
"""Validate repository-local README targets and profile assets."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def main() -> int:
    text = README.read_text(encoding="utf-8")
    failures: list[str] = []

    forbidden = ("YOUR_USERNAME", "your-email@example.com", "Lorem ipsum", "COMING SOON", "TODO")
    for marker in forbidden:
        if marker in text:
            failures.append(f"forbidden placeholder in README: {marker}")

    targets = set(re.findall(r"\]\((\.?/?(?:assets|MAINTENANCE\.md)[^)]+)\)", text))
    targets.update(re.findall(r'src="(\.?/?assets/[^"]+)"', text))
    for target in sorted(targets):
        clean = target.split("#", 1)[0]
        path = ROOT / clean.removeprefix("./")
        if not path.exists():
            failures.append(f"missing README target: {target}")

    for svg in ROOT.glob("assets/**/*.svg"):
        try:
            ET.parse(svg)
        except ET.ParseError as error:
            failures.append(f"invalid SVG {svg.relative_to(ROOT)}: {error}")

    expected = (
        ROOT / "assets/hero/jithu-ai-lab-live.webp",
        ROOT / "assets/portrait/jithu-cyber-portrait-animated.webp",
        ROOT / "assets/portrait/jithu-pixel-avatar.webp",
    )
    for asset in expected:
        if not asset.exists() or asset.stat().st_size == 0:
            failures.append(f"missing or empty core asset: {asset.relative_to(ROOT)}")

    if failures:
        print("profile validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"validated {len(targets)} local README targets and {len(list(ROOT.glob('assets/**/*.svg')))} SVG assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
