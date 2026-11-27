# The World in One Day — 26 November 2026

[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/akbare12/news-26-b134-numbers/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/akbare12/news-26-b134-numbers/reward.svg)](https://make.fun/bounty/news-image-20261126)

One image summing up Thursday 26 November 2026: 50 stories across 10 regions.

Layout V130: masthead + DATE CHECK strip on top, a vertical timeline rail
on the right edge, three heroes in one row (art above, text below), ten
cards in a 5×2 grid, and a world map beside the ALSO column at the bottom.

## What's inside

- **Hero trio:** Macy's 100th Thanksgiving Parade postponed (first weather
  postponement ever) · IRGC claims 2 tankers hit by mines in the Strait of
  Hormuz · Trump tariffs: global markets rebound.
- **10 cards:** Gaza, Kyiv, Bogor (13 dead / 13 missing), Jerusalem,
  Pyongyang, Washington, London, Moscow, Bangkok, Cologne — each with a
  literal [C] / [R] / [CL] tag.
- **ALSO TODAY:** 37 further items, each tagged [C] / [R] / [CL]; every
  25 Nov item carries [CL] plus the explicit text "25 Nov".
- **DATE CHECK:** 7 stories deliberately excluded because they are not
  26 Nov news (COP31, Shenzhou-24, Cairo tanker, Cartagena hostages,
  Australia–Solomon pact, UK energy +26%, Huawei verdict).
- **Map + timeline:** 10 numbered pins on a world map with a legend, and a
  vertical "The Day in Order" rail.
- **Tags:** [C] confirmed · [R] reported · [CL] claim / 25 Nov event.

## How it is built

- `gen.py` (Pillow, build time only) renders `entry.png` (1024×1024).
  Every text block is measured before drawing: hero decks fit in full,
  card decks clear their stat lines, ALSO items fit their columns, the
  timeline fits its rail, and no art pixel ever overlaps a text pixel
  (art is drawn on its own layer, sized exactly to its box; the map is
  clipped to its panel).
- `main.py` (standard library only) copies `entry.png` to
  `MAKEFUN_OUTPUT_DIR/entry.png` for the grader.

## Verification

- entry.png: 1024×1024, 170,286 bytes, sha256
  `aea75672acd7a10324e88584aa4edf0ac96a990f93e0e0e5c0e19817b02c8f53`
- Deterministic: re-running `python3 gen.py` reproduces the same sha256.
- Stdlib-venv simulation: `main.py` runs with no Pillow installed, from a
  different working directory, into an empty output directory, exit 0,
  output sha256 matches.
- 50 stories = 3 heroes + 10 cards + 37 ALSO items; 10 regions.
