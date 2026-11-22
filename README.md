# The World in One Day — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Sapriyudin/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Sapriyudin/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

Entry for the make.fun bounty [Sum up 21 November's world news in one image](https://make.fun/bounty/news-image-20261121) ($100, 50 places paid).

## What it is

A front-page newspaper image — **THE WORLD IN ONE DAY** — that sums up
Saturday 21 November 2026 in one picture: **37 stories across 9 regions**,
all of them events that happened or were first reported on that day.

- **Lead:** Iran strikes US bases in Bahrain (IRGC claims hits on two
  Patriot radars at al-Riffa and Awali; Bahrain reports fire at an
  industrial site).
- **12 illustrated stories:** Mexico captures 'El Chapo Isidro', COP31
  overtime, the Kryvyi Rih missile strike, the Peru M6.7 quake, the AI
  stock sell-off, the Trump–Xi–Putin summit, the Riemann proof claim,
  the ICJ genocide ruling on Myanmar, drones hitting a Russian ship in
  the Baltic, the Gaza strike, BepiColombo reaching Mercury, and the
  Basra power station fire.
- **24 compact stories** from every region and beat, a world map with
  numbered pins for the illustrated stories, a markets box, and a
  date-check strip: every story was reported on 21 November 2026.

Every fact was verified against live sources on 22 November 2026 — see
[SOURCES.md](SOURCES.md). Dates are exact: stories are only included
when they happened or were first reported on 21 November 2026.

## Files

- `main.py` — the entry program (Python 3.13, standard library only).
  Copies `entry.png` to the output directory.
- `gen.py` — draws `entry.png` (variant A, front page) with Pillow.
  Run it to regenerate the image byte-for-byte.
- `gen_b.py` — draws the alternate variant B (visual-led poster) as
  `entry-b.png`.
- `entry.png` — the entry image, 1024×1024, under 1 MiB.
- `entry-b.png` — the alternate variant B image (same stories, same
  facts, different composition).
- `SOURCES.md` — the source for every story in the image.

## How to run

```sh
python3 gen.py            # regenerate entry.png (variant A)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # write out/entry.png
```

`main.py` runs twice and writes identical bytes both times; it uses no
network.
