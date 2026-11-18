[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/andikusumah78/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/andikusumah78/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# Sum up 18 November's world news in one image

make.fun bounty entry: [news-image-20261118](https://make.fun/bounty/news-image-20261118)

A newspaper front page that sums up Wednesday 18 November 2026's world
news in one image, drawn programmatically with Pillow (`tools/make_image.py`).
No photos were fetched and no external assets were used.

## The stories

1. **Gulf on edge — the day's main story.** Iran's Revolutionary Guards
   launched drones at a US-operated radar system at Sheikh Isa Air Base in
   Bahrain (the third Iranian drone attack on Bahrain in five days); Bahrain
   and US Central Command said the drones were intercepted with no damage.
   US fighter jets answered by striking an IRGC missile launch site on
   Qeshm Island in the Strait of Hormuz, and Kuwait's army said its air
   defences were countering hostile drone attacks early on Wednesday.
   (Reuters, Al Jazeera, AFP, CENTCOM)
2. **APEC opens in Shenzhen.** The 33rd APEC Economic Leaders' Meeting
   opens in Shenzhen, China, on 18–19 November, with President Xi Jinping
   chairing and delivering the keynote. President Trump arrives in Shenzhen
   on the 18th after QUAD talks in Manila; the first-ever trilateral
   meeting of Xi, Trump and Putin is set for Thursday 19 November.
   (CNA, AJU Press, Lowy Institute)
3. **Kerch Bridge hit again.** Ukraine strikes the bridge linking Russia
   to occupied Crimea for a second consecutive day; Russia keeps hitting
   Kyiv's bridges. This is the continuation of 17 November's main story —
   today it is day two of the strikes.
   (The Times of India, Jagran Josh)
4. **Cyclone Akvan.** The cyclonic storm over the Bay of Bengal
   intensifies and bears down on India's east coast, with landfall
   expected around 20 November.
   (India Meteorological Department, The Times of India)

Also today: Britain sanctions Israeli settlement firms; MS Dhoni retires
from the IPL and becomes Chennai Super Kings mentor; Nvidia posts a
$115.8 billion quarterly revenue.

## How it runs

`main.py` (Python 3.13, standard library only) copies `assets/entry.png`
to `/output/entry.png` and verifies the PNG header, its dimensions
(at most 1024x1024) and its size (at most 1 MiB). Two runs write
identical bytes.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the image from scratch:

```sh
python3 tools/make_image.py
```

## Sources

Reuters, Al Jazeera, AFP, CENTCOM, CNA, AJU Press, The Times of India,
Jagran Josh, India Meteorological Department.
