"""Publish one playful Raghav joke per Indian calendar day, without API calls."""

from __future__ import annotations

import argparse
from datetime import date, datetime
from html import escape
import json
from pathlib import Path
import random
import textwrap
from zoneinfo import ZoneInfo

import build_artwork_v4 as art
from build_artwork_v5 import recolour

ROOT = Path(__file__).resolve().parents[1]
ZONE = ZoneInfo('Asia/Kolkata')
EPOCH = date(2026, 10, 4)
START, END = '<!-- RAGHAV_FACT_START -->', '<!-- RAGHAV_FACT_END -->'


def load_facts(path):
    facts = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(facts, list) or len(facts) < 2:
        raise ValueError('Provide at least two distinct jokes.')
    if any(not isinstance(fact, str) or not fact.strip() or len(fact) > 120 or '\n' in fact for fact in facts):
        raise ValueError('Jokes must be nonempty single lines of at most 120 characters.')
    if len(set(facts)) != len(facts):
        raise ValueError('Duplicate jokes would repeat the daily grin.')
    return facts


def choose_fact(facts, day):
    # A shuffled deck guarantees a fresh joke tomorrow and stable same-day reruns.
    deck = list(facts)
    random.Random('raghav-garden-facts-v1').shuffle(deck)
    return deck[(day - EPOCH).days % len(deck)]


def render_card(fact, day, theme='light', mobile=False):
    dark = theme == 'dark'
    ink, muted, bg, line, accent = ('#f1e4cc', '#c8b894', '#282419', '#665738', '#efd080') if dark else ('#19364b', '#6f715c', '#fff8e9', '#e5d09f', '#a27b23')
    width = 420 if mobile else 960
    lines = textwrap.wrap(fact, width=29 if mobile else 57, break_long_words=False, break_on_hyphens=False)
    height = max(246 if mobile else 216, (106 if mobile else 117) + (len(lines) - 1) * 29 + 52)
    s = '<style>.think{animation:think 5s ease-in-out infinite}.spark{animation:spark 4s ease-in-out infinite}@keyframes think{50%{transform:translateY(-4px)}}@keyframes spark{50%{opacity:.35}}@media(prefers-reduced-motion:reduce){.think,.spark{animation:none}}</style>'
    s += f'<rect x="2" y="2" width="{width-4}" height="{height-4}" rx="19" fill="{bg}" stroke="{line}" stroke-width="1.5"/>'
    s += art.text(23 if mobile else 28, 30, 'PLAYFUL DEVELOPER LORE', 9 if mobile else 10, accent, 700, 'letter-spacing="1.5"')
    s += art.text(21 if mobile else 26, 71, 'Raghav Fact of the Day.', 26 if mobile else 32, ink, 750, 'letter-spacing="-.8"')
    for index, value in enumerate(lines):
        s += art.text(23 if mobile else 28, (106 if mobile else 117) + index * 29, value, 19 if mobile else 22, ink, 550)
    caption = day.strftime('%d %b %Y') + ' · IST'
    s += art.text(23 if mobile else 28, height - 22, caption, 11, muted, 550)
    if mobile:
        # Small, legible decoration stays outside the joke's reading area.
        s += '<g class="think">' + recolour(art.cat(355, 17, 2.5), theme) + '</g>'
        s += art.text(335, 33, ';', 22, accent, 700, f'class="spark" font-family="{art.MONO}"')
    else:
        s += art.text(926, 31, 'ONE FRESH JOKE EACH DAY', 10, muted, 550, 'text-anchor="end" letter-spacing=".8"')
        s += '<g class="think">'
        s += f'<rect x="815" y="80" width="87" height="47" rx="14" fill="{bg}" stroke="{line}" stroke-width="2"/><path d="M837 127L827 137L852 127" fill="{bg}" stroke="{line}" stroke-width="2"/>'
        s += art.text(858, 112, ';', 29, accent, 700, f'text-anchor="middle" font-family="{art.MONO}"') + '</g>'
        s += recolour(art.cat(827, 151, 4), theme)
        s += '<g class="spark">' + art.star(907, 143, 3, '#d8ad57') + '</g>'
    title = f'Raghav Fact of the Day — {caption}. Playful fictional developer humor: {fact}'
    return art.svg(width, height, title, s)


def readme_block(fact, day):
    label = escape(f'Raghav Fact of the Day, {day.isoformat()} IST. Playful developer joke: {fact}', quote=True)
    stamp = f'?day={day.isoformat()}'
    return f'''{START}
<a name="raghav-fact-of-the-day"></a>
<p align="center">
  <picture><source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/facts/fact-mobile-dark.svg{stamp}"><source media="(prefers-color-scheme: dark)" srcset="assets/facts/fact-dark.svg{stamp}"><source media="(max-width: 600px)" srcset="assets/facts/fact-mobile-light.svg{stamp}"><img src="assets/facts/fact-light.svg{stamp}" width="100%" alt="{label}" /></picture>
</p>
{END}'''


def refresh(readme=ROOT / 'README.md', output=ROOT / 'assets' / 'facts', bank=ROOT / 'data' / 'raghav-facts.json', day=None):
    day = day or datetime.now(ZONE).date()
    facts = load_facts(bank)
    fact = choose_fact(facts, day)
    source = readme.read_text(encoding='utf-8')
    if source.count(START) != 1 or source.count(END) != 1 or source.index(START) > source.index(END):
        raise ValueError('README must contain one correctly ordered fact marker pair.')
    replacement = source[:source.index(START)] + readme_block(fact, day) + source[source.index(END) + len(END):]
    files = {readme: replacement}
    for theme in ['light', 'dark']:
        for mobile in [False, True]:
            suffix = '-mobile' if mobile else ''
            files[output / f'fact{suffix}-{theme}.svg'] = render_card(fact, day, theme, mobile)
    snapshot = {'date': day.isoformat(), 'timezone': 'Asia/Kolkata', 'type': 'fictional developer humor', 'fact': fact, 'collection_size': len(facts)}
    files[output / 'fact.json'] = json.dumps(snapshot, indent=2, ensure_ascii=False) + '\n'
    # Validate and render everything before touching the last published version.
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + '.tmp')
        temporary.write_text(content, encoding='utf-8')
    for path in files:
        path.with_name(path.name + '.tmp').replace(path)
    return snapshot


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', type=date.fromisoformat, help='Optional Indian calendar date for a reproducible render.')
    args = parser.parse_args()
    snapshot = refresh(day=args.date)
    print(f'Published the daily grin for {snapshot["date"]} IST.')
