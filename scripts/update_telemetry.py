#!/usr/bin/env python3
"""Refresh the repository-hosted GitHub telemetry SVG using the public API."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets/telemetry/system-telemetry.svg"
USERNAME = "JithuVathiath"


def fetch_profile() -> dict[str, object]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "JithuVathiath-profile-telemetry",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/users/{USERNAME}", headers=headers)
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def render(profile: dict[str, object]) -> str:
    repos = int(profile["public_repos"])
    followers = int(profile["followers"])
    following = int(profile["following"])
    synced = datetime.now(timezone.utc).strftime("%Y-%m-%d UTC")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="260" viewBox="0 0 1200 260" role="img" aria-labelledby="title desc">
  <title id="title">GitHub system telemetry</title><desc id="desc">{repos} public repositories, {followers} followers and {following} following, verified from the GitHub public API on {synced}.</desc>
  <defs><linearGradient id="g"><stop stop-color="#D8A25E"/><stop offset=".5" stop-color="#596C78"/><stop offset="1" stop-color="#C46D48"/></linearGradient><style>text{{font-family:Georgia,'Times New Roman',serif}}.line{{stroke-dasharray:7 13;animation:f 7s linear infinite}}.p{{animation:p 5s ease-in-out infinite}}@keyframes f{{to{{stroke-dashoffset:-80}}}}@keyframes p{{50%{{opacity:.55}}}}@media(prefers-reduced-motion:reduce){{.line,.p{{animation:none}}}}</style></defs>
  <rect width="1200" height="260" rx="18" fill="#1D1714"/><rect x="2" y="2" width="1196" height="256" rx="16" fill="none" stroke="url(#g)" stroke-width="2"/>
  <text x="42" y="52" fill="#D8A25E" font-size="15" letter-spacing="4">SYSTEM TELEMETRY // PUBLIC GITHUB API</text><path class="line" d="M42 78H1158" stroke="#5C5146" stroke-width="2"/>
  <g transform="translate(42 104)">
    <g><rect width="250" height="110" rx="12" fill="#2B241F" stroke="#D8A25E"/><text x="20" y="32" fill="#A89E8C" font-size="13">PUBLIC REPOSITORIES</text><text x="20" y="78" fill="#F4EADB" font-size="36" font-weight="700">{repos}</text></g>
    <g transform="translate(272)"><rect width="250" height="110" rx="12" fill="#2B241F" stroke="#596C78"/><text x="20" y="32" fill="#A89E8C" font-size="13">FOLLOWERS</text><text x="20" y="78" fill="#F4EADB" font-size="36" font-weight="700">{followers}</text></g>
    <g transform="translate(544)"><rect width="250" height="110" rx="12" fill="#2B241F" stroke="#C46D48"/><text x="20" y="32" fill="#A89E8C" font-size="13">FOLLOWING</text><text x="20" y="78" fill="#F4EADB" font-size="36" font-weight="700">{following}</text></g>
    <g transform="translate(816)"><rect width="300" height="110" rx="12" fill="#2B241F" stroke="#85966D"/><text x="20" y="32" fill="#A89E8C" font-size="13">LAST TELEMETRY SYNC</text><text x="20" y="72" fill="#F4EADB" font-size="19" font-weight="700">{synced}</text><circle class="p" cx="268" cy="26" r="5" fill="#85966D"/></g>
  </g>
</svg>
'''


if __name__ == "__main__":
    OUTPUT.write_text(render(fetch_profile()), encoding="utf-8")
    print(f"updated {OUTPUT.relative_to(ROOT)}")
