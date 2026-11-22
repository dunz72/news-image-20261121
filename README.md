[![make.fun bounty](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/dunz72/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/dunz72/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

# The World in One Day — Saturday 21 November 2026

A single 1024×1024 front page that sums up Saturday 21 November 2026:
one lead story, four feature stories and four items in brief.

The page is drawn entirely in code — every panel, bridge, chart, globe,
skyline and scale of justice is an original vector illustration rendered
with Pillow. No photographs, no stock art, no official logos.

## The front page

- **Masthead** — "THE WORLD IN ONE DAY", Saturday 21 November 2026.
- **Lead — Russia's biggest November barrage hits Kyiv, and spills into
  Poland.** A night bridge under fire: Russia fired 404 drones and 111
  missiles overnight on 19–20 November; at least eight people were killed
  in Kyiv, three Dnipro bridges were damaged, and two missiles plus a
  jet-powered drone came down in eastern Poland.
- **Justice — World Court: Myanmar guilty of genocide against the
  Rohingya.** The ICJ's landmark 9–6 judgment of 19 November, the first
  time the court has found a state guilty of committing genocide.
- **Markets — AI sell-off sinks Wall Street.** The S&P 500 fell 3.7%, the
  Nasdaq closed negative for the year and the Nikkei slid 5.1%, while
  Anthropic debuted on Wall Street valued at about $2 trillion.
- **Climate — COP31 passes deadline as fossil-fuel language drops.**
  Talks in Antalya ran past their Friday deadline; the draft dropped
  fossil-fuel phase-out language while admitting the 1.5°C limit will be
  overshot.
- **Culture — GTA VI: $3.8bn in a day.** About 32.5 million copies sold on
  day one — the biggest entertainment launch ever.
- **The day in brief** — the Xi–Trump–Putin summit in Shenzhen, Trump
  weighing new Iran strikes and the FBI breach probe, the UK–EU
  post-Brexit agreements, and the daraxonrasib pancreatic-cancer pill
  trial plus BepiColombo reaching Mercury.

Sources: BBC News, Associated Press, The New York Times, Reuters, UN
News, Institute for the Study of War, Human Rights Watch.

## Run it

Requires Python 3 and Pillow — no network access, no system fonts
(Pillow's bundled default font only).

`main.py` draws the 1024×1024 front page entirely in code with Pillow
and writes it to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`).
The output is deterministic: two runs produce byte-identical PNGs.

The finished front page is stored in this repository as `entry.png`.

```sh
python3 main.py
```
