# Profile maintenance

The active profile uses native Markdown, a compact static WebP illustration, a source-backed research chart and a real software screenshot. Native text carries all essential facts, skills and links. The optional activity panel is collapsed by default.

## Content and evidence

Keep three featured projects: human–AI collaboration, the SBA credit-risk benchmark and the market microstructure lab. Put other projects in the expandable list. Describe each featured project through its question, implementation, evidence and links.

Verify study values against the public human–AI repository before changing either the prose or `scripts/build_research_chart.py`. Preserve the small-and-uncertain interpretation of the final-minus-initial difference. Do not copy participant-level material into this repository. Credit-risk results refer to future-vintage test data and already-approved loans; model selection is based on validation PR-AUC.

Education dates, graduation timing, role interests and the public email were supplied by the owner on 29 October 2026. Do not add a CV link until an actual public document is available. Keep current-focus items framed as future research priorities, not completed releases.

## Visual system

- Navy: `#0B1629`
- Slate surface: `#14243C`
- Primary blue: `#2563EB`
- Cyan accent: `#2695BE`
- Light surface: `#F1F6FC`
- Dark text: `#142D4E`

Use system sans-serif text, generous whitespace and restrained blue accents. The original animated ASCII portrait appears centred beneath the studio banner at 240 pixels wide, as requested by the owner. Keep its existing monochrome artwork and reveal animation. Avoid additional typing effects or dense text inside images. The banner is a static 3:1 image; its visualisations are decorative. Evidence graphics must be separately identified and linked to their source.

`scripts/apply_blue_palette.py` updates the legacy SVG panels and the telemetry generator. `scripts/apply_retro_palette.py` is a compatibility alias for the blue palette. Legacy source artwork is retained but not embedded in the active README.

Rebuild the research chart with Python and matplotlib:

```bash
python scripts/build_research_chart.py
```

The bar chart uses a zero-to-100% scale and public aggregate values. Its PNG counterpart is available for export. See `assets/README.md` for asset provenance and the illustration prompt.

## Automated activity

The telemetry workflow refreshes `assets/telemetry/system-telemetry.svg` weekly from the public GitHub API. Its generator uses the same blue palette, so scheduled refreshes preserve the design. The Pac-Man workflow updates contribution animations on the `output` branch daily.

```bash
python scripts/update_telemetry.py
```

## Validation

```bash
python scripts/validate_profile.py
ruby -e 'require "yaml"; ARGV.each { |f| YAML.parse_file(f) }' .github/workflows/*.yml
```

Review the README in light and dark appearances and at a narrow mobile width. Confirm images load, essential information remains available as text, section links work and the contact addresses are correct. Re-check external project destinations when changing links.
