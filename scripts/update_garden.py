"""Contribution surf: animate the real calendar grid with a cat hoverboard.

No token or third-party graph service required. Fetch and validate the complete
rolling year before replacing anything; failed refreshes keep the last artwork.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request
from zoneinfo import ZoneInfo

from contribution_surf import layout, render, section_heading

ROOT = Path(__file__).resolve().parents[1]
USER = 'raghav-shell'
ZONE = ZoneInfo('Asia/Kolkata')
START, END = '<!-- FIREFLY_GARDEN_START -->', '<!-- FIREFLY_GARDEN_END -->'


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells, self.tooltips = {}, {}
        self.target, self.parts = None, []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'td' and 'data-date' in attrs:
            key = attrs['id']
            if key in self.cells:
                raise ValueError('Duplicate calendar cell')
            self.cells[key] = (date.fromisoformat(attrs['data-date']), int(attrs['data-level']))
        if tag == 'tool-tip' and attrs.get('for') in self.cells:
            self.target, self.parts = attrs['for'], []

    def handle_data(self, data):
        if self.target is not None:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.target is not None:
            if self.target in self.tooltips:
                raise ValueError('Duplicate calendar tooltip')
            self.tooltips[self.target] = ' '.join(''.join(self.parts).split())
            self.target = None


def parse_calendar(document):
    parser = CalendarParser()
    parser.feed(document)
    days = {}
    for key, (day, level) in parser.cells.items():
        label = parser.tooltips.get(key, '')
        count = re.fullmatch(r'(No|[\d,]+) contributions? on .+\.', label)
        if count is None or level not in range(5):
            raise ValueError('Unrecognized GitHub contribution calendar')
        number = 0 if count[1] == 'No' else int(count[1].replace(',', ''))
        if (number == 0) != (level == 0) or day in days:
            raise ValueError('Inconsistent or duplicate contribution day')
        days[day] = {'date': day.isoformat(), 'count': number, 'level': level}
    if not days:
        raise ValueError('GitHub returned no calendar days')
    return days


def calendar_url(day):
    return f'https://github.com/users/{USER}/contributions?to={day.isoformat()}'


def fetch_calendar(day):
    request = urllib.request.Request(calendar_url(day), headers={
        'User-Agent': 'raghav-shell-firefly-garden', 'Accept': 'text/html',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode('utf-8')


def collect(day, documents=None):
    first = day - timedelta(days=364)
    by_date = {}
    years = range(first.year, day.year + 1)
    for year in years:
        document = documents[year] if documents is not None else fetch_calendar(min(day, date(year, 12, 31)))
        parsed = parse_calendar(document)
        for current, value in parsed.items():
            if current in by_date and by_date[current] != value:
                raise ValueError('Conflicting calendar data')
            by_date[current] = value
    expected = [first + timedelta(days=i) for i in range(365)]
    if any(current not in by_date for current in expected):
        raise ValueError('Incomplete rolling contribution year; keeping the previous garden')
    days = [by_date[current] for current in expected]
    return {'user': USER, 'as_of': day.isoformat(), 'from': first.isoformat(),
            'source': f'https://github.com/{USER}?tab=overview',
            'total': sum(item['count'] for item in days), 'days': days}


def readme_block(snapshot):
    day = snapshot['as_of']
    alt = escape(f'Contribution surf: a blue pixel cat leans into hoverboard turns inside my real contribution grid, leaving a fading rainbow trail as nearby squares ripple and active squares glow. {snapshot["total"]} contributions from {snapshot["from"]} to {day}; mobile shows the latest 13 calendar weeks. Original activity levels and counts stay unchanged.', quote=True)
    return f'''{START}
<a name="contribution-surf"></a>
<h2><picture><source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/contributions/heading-mobile-dark.svg"><source media="(prefers-color-scheme: dark)" srcset="assets/contributions/heading-dark.svg"><source media="(max-width: 600px)" srcset="assets/contributions/heading-mobile-light.svg"><img src="assets/contributions/heading-light.svg" width="100%" alt="Small steps, cosmic ripples" /></picture></h2>
<p align="center">
  <picture><source media="(prefers-color-scheme: dark) and (max-width: 600px)" srcset="assets/contributions/garden-mobile-dark.svg?day={day}"><source media="(prefers-color-scheme: dark)" srcset="assets/contributions/garden-dark.svg?day={day}"><source media="(max-width: 600px)" srcset="assets/contributions/garden-mobile-light.svg?day={day}"><img src="assets/contributions/garden-light.svg?day={day}" width="100%" alt="{alt}" /></picture>
</p>
{END}'''


def refresh(readme, output, day=None, documents=None):
    day = day or datetime.now(ZONE).date()
    body = readme.read_text()
    if body.count(START) != 1 or body.count(END) != 1 or body.index(START) >= body.index(END):
        raise ValueError('The contribution garden needs exactly one ordered marker pair')
    snapshot = collect(day, documents)
    rendered = {f'garden-{prefix}{theme}.svg': render(snapshot, theme, mobile)
                for theme in ['light', 'dark'] for mobile, prefix in [(False, ''), (True, 'mobile-')]}
    rendered.update({f'heading-{prefix}{theme}.svg': section_heading(theme, mobile)
                     for theme in ['light', 'dark'] for mobile, prefix in [(False, ''), (True, 'mobile-')]})
    rendered['snapshot.json'] = json.dumps(snapshot, indent=2) + '\n'
    updated = body[:body.index(START)] + readme_block(snapshot) + body[body.index(END)+len(END):]
    # All fetches, validation, rendering and marker checks precede any writes.
    output.mkdir(parents=True, exist_ok=True)
    for name, value in rendered.items():
        path = output / name
        temporary = path.with_suffix(path.suffix + '.tmp')
        temporary.write_text(value)
        temporary.replace(path)
    temporary = readme.with_suffix('.md.tmp')
    temporary.write_text(updated)
    temporary.replace(readme)
    return snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', type=date.fromisoformat)
    parser.add_argument('--calendar-dir', type=Path, help='Use saved calendar-YEAR.html files for an offline refresh')
    args = parser.parse_args()
    day = args.date or datetime.now(ZONE).date()
    documents = None
    if args.calendar_dir:
        documents = {year: (args.calendar_dir / f'calendar-{year}.html').read_text()
                     for year in range((day-timedelta(days=364)).year, day.year+1)}
    snapshot = refresh(ROOT/'README.md', ROOT/'assets/contributions', day, documents)
    print(f'Contribution surf: {snapshot["total"]} contributions · {snapshot["from"]} to {day}')


if __name__ == '__main__':
    main()
