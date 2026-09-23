# Profile maintenance

The profile is intentionally built from repository-hosted Markdown, SVG, WebP and GitHub Actions. It does not require JavaScript or an external dashboard service.

## Update featured projects

Edit the numbered list in `README.md`, then update the matching card in `assets/projects/mission-grid.svg`. Keep six flagship cards so the visual remains readable on mobile. Link only to public repositories and preserve any important evidence or limitation language from the project itself.

## Update technologies

Edit `assets/stack/tech-arsenal.svg` and the supporting sentence in `README.md`. Add a technology only when a public repository demonstrates meaningful use; avoid turning the panel into an exhaustive badge wall.

## Update contact links

Edit the `Establish uplink` section in `README.md`. Verify every destination before committing. Omit email, LinkedIn or portfolio links until the owner has explicitly approved the public address.

## Update the hero or portrait

Source artwork lives in:

- `assets/hero/jithu-ai-lab.png`
- `assets/hero/jithu-ai-lab-headturn-mid.png`
- `assets/hero/jithu-ai-lab-headturn-full.png`
- `assets/hero/jithu-ai-lab-greeting-*.webp`
- `assets/portrait/jithu-cyber-portrait.png`
- `assets/portrait/jithu-pixel-avatar.png`

The hero animation composites video-guided head-turn, shoulder, elbow and hand-wave keyframes over the stable lab scene, then adds the live monitor, lighting and environmental effects. Dedicated return keyframes keep the head, neck, shoulders and torso rotating back toward the monitors together. Optimized static WebP files sit beside the sources. Run `python scripts/build_animations.py` after replacing the optimized hero, its keyframes or the portrait WebP. Keep the source portrait private outside this repository; only the stylized outputs belong here.

## Update research evidence

Change the prose in `README.md` and the matching values in `assets/research/human-ai-decision-intelligence.svg` together. Re-check every number against the current public research repository. Preserve the experimental, causal and fairness boundaries.

## Update project cards

Each card in `assets/projects/mission-grid.svg` has a project number, domain, title, one evidence line and a concise stack line. Keep text short enough to remain readable at 320-pixel viewport width.

## Update telemetry

`scripts/update_telemetry.py` reads the GitHub public API and rewrites `assets/telemetry/system-telemetry.svg`. The scheduled `telemetry.yml` workflow runs weekly and commits a change only when values differ.

Run locally with network access:

```bash
python scripts/update_telemetry.py
```

## Automated visuals

- `telemetry.yml` updates the first-party telemetry card.
- `snake.yml` generates an optional contribution snake on the `output` branch.
- `validate.yml` checks local README targets, SVG parsing, forbidden placeholders and workflow YAML syntax.

## Final check

Run:

```bash
python scripts/validate_profile.py
ruby -e 'require "yaml"; ARGV.each { |f| YAML.parse_file(f) }' .github/workflows/*.yml
```

Review the README once in GitHub light mode, dark mode and a narrow mobile viewport before publishing major visual changes.
