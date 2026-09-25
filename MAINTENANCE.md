# Profile maintenance

The profile is intentionally built from repository-hosted Markdown, SVG, WebP and GitHub Actions. It does not require JavaScript or an external dashboard service.

## Update featured projects

Edit the numbered list in `README.md`, then update the matching card in `assets/projects/mission-grid.svg`. Keep six flagship cards so the visual remains readable on mobile. Link only to public repositories and preserve any important evidence or limitation language from the project itself.

## Update technologies

Edit `assets/stack/tech-arsenal.svg` and the supporting sentence in `README.md`. Add a technology only when a public repository demonstrates meaningful use; avoid turning the panel into an exhaustive badge wall.

## Update contact links

Edit the `Contact and Links` section in `README.md`. Verify every destination before committing. Omit email or portfolio links until the owner has explicitly approved the public address.

## Update the hero or portrait

Source artwork lives in:

- `assets/hero/jithu-ai-lab.png`
- `assets/hero/jithu-ai-lab-headturn-mid.png`
- `assets/hero/jithu-ai-lab-headturn-full.png`
- `assets/hero/jithu-ai-lab-greeting-*.webp`
- `assets/hero/jithu-retro-studio.webp`
- `assets/hero/jithu-retro-studio-wave-*.webp`
- `assets/hero/godzilla-window-*.webp`
- `assets/portrait/jithu-ascii-source-monochrome.webp`
- `assets/portrait/jithu-ascii-portrait-bw.png`
- `assets/portrait/jithu-ascii-portrait-reveal.webp`
- `assets/portrait/jithu-retro-avatar.webp`
- `assets/portrait/jithu-cyber-portrait.png`
- `assets/portrait/jithu-pixel-avatar.png`

The active hero uses a warm retro-Japanese studio, a resting frame and two natural hand positions. The three monitors show the human-AI decision process, model evaluation and responsible-AI assurance. The `window-city-clean.webp` crop provides the stable outdoor scene; the build script renders a small flock with staggered positions and wing phases, then masks the result strictly to the two outdoor window panes so the room and person remain untouched. Run `python scripts/build_retro_hero.py` after replacing the clean window source frame. The animation begins its greeting immediately, uses direct crisp cuts rather than a tinted flash, and rests before looping while the birds continue flying. The older cyberpunk sources remain as archive material and can still be rebuilt with `python scripts/build_animations.py`, but they are not referenced by the README. Run `python scripts/apply_retro_palette.py` to restore the muted amber, terracotta, indigo and sage palette across the first-party SVG panels. Run `python scripts/build_ascii_portrait.py` after replacing the monochrome ASCII source plate, then run `python scripts/build_ascii_reveal.py` to rebuild its top-to-bottom reveal without altering the underlying portrait. Keep the original private photograph outside this repository; only stylized outputs belong here.

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
- `pacman.yml` generates light and dark Pac-Man contribution games on the `output` branch.
- `validate.yml` checks local README targets, SVG parsing, forbidden placeholders and workflow YAML syntax.

The Pac-Man panel is generated daily from public contribution data. GitHub's native activity remains authoritative.

## Final check

Run:

```bash
python scripts/validate_profile.py
ruby -e 'require "yaml"; ARGV.each { |f| YAML.parse_file(f) }' .github/workflows/*.yml
```

Review the README once in GitHub light mode, dark mode and a narrow mobile viewport before publishing major visual changes.
