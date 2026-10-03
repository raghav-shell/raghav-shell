"""An original firefly-and-cat contribution garden, using GitHub's visible calendar.

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

from build_artwork_v4 import cat, pixel, star, svg, text
from build_artwork_v5 import recolour

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


def layout(snapshot, mobile):
    last = date.fromisoformat(snapshot['as_of'])
    # Mobile displays 13 complete calendar columns; desktop displays the year.
    sunday = last - timedelta(days=(last.weekday() + 1) % 7)
    first = sunday - timedelta(weeks=12) if mobile else date.fromisoformat(snapshot['from'])
    origin = first - timedelta(days=(first.weekday() + 1) % 7)
    days = [item for item in snapshot['days'] if date.fromisoformat(item['date']) >= first]
    columns = (last - origin).days // 7 + 1
    pitch, size, gx, gy = (23, 17, 69, 162) if mobile else (16, 12, 76, 141)
    cells = []
    for item in days:
        day = date.fromisoformat(item['date'])
        column, row = (day - origin).days // 7, (day.weekday() + 1) % 7
        cells.append(dict(item, x=gx + column * pitch, y=gy + row * pitch, column=column))
    # Traverse every week, pausing at its busiest day. Quiet weeks remain quiet.
    route = []
    for column in range(columns):
        week = [cell for cell in cells if cell['column'] == column]
        target = max(week, key=lambda cell: (cell['count'], cell['date']))
        route.append((target['x'] + size / 2, target['y'] + size / 2))
    return days, cells, route, (pitch, size, gx, gy, columns), first


def render(snapshot, theme='light', mobile=False):
    dark = theme == 'dark'
    bg, panel, border = ('#101e2b', '#132b36', '#365469') if dark else ('#f2f8fc', '#e9f5ef', '#b8d0de')
    ink, muted = ('#e1edf5', '#9fb8ca') if dark else ('#19364b', '#597487')
    levels = ['#233b45', '#345f57', '#4d8f77', '#6cbaa0', '#9ee8c1'] if dark else ['#dbe8e5', '#b0d9c5', '#83bea1', '#559c7b', '#327b5c']
    gold = '#ffda7a' if dark else '#b57718'
    days, cells, route, (pitch, size, gx, gy, columns), first = layout(snapshot, mobile)
    width, height = (400, 435) if mobile else (960, 397)
    duration = 36 if mobile else 48
    # Move out and back without a teleport at the loop boundary.
    stops = route + route[-2:0:-1] + [route[0]]
    frames = ''.join(f'{i / (len(stops) - 1) * 100:.4f}%{{transform:translate({x:g}px,{y:g}px)}}' for i, (x, y) in enumerate(stops))
    count = sum(item['count'] for item in days)
    period = f'{first:%d %b %Y} — {date.fromisoformat(snapshot["as_of"]):%d %b %Y}'
    title = f'Firefly Trail. {count} contributions in the visible GitHub calendar, {period}. A blue cat follows a golden firefly through the contribution garden.'
    s = f'''<defs><linearGradient id="name"><stop stop-color="{ink}"/><stop offset="1" stop-color="{'#9ee8c1' if dark else '#327b5c'}"/></linearGradient><radialGradient id="glow"><stop stop-color="#ffdb7c" stop-opacity=".6"/><stop offset="1" stop-color="#ffdb7c" stop-opacity="0"/></radialGradient></defs>
<style>.fly{{animation:journey {duration}s linear infinite}}.cat{{animation:journey {duration}s linear infinite;animation-delay:-{duration-0.8}s}}.wings{{animation:wings 1s ease-in-out infinite}}.halo{{animation:breathe 3s ease-in-out infinite}}.bloom{{animation:bloom {duration}s ease-in-out infinite}}@keyframes journey{{{frames}}}@keyframes wings{{50%{{opacity:.4}}}}@keyframes breathe{{50%{{opacity:.5}}}}@keyframes bloom{{0%,3%,97%,100%{{opacity:0}}1.5%{{opacity:.85}}}}@media(prefers-reduced-motion:reduce){{.fly,.cat,.wings,.halo,.bloom{{animation:none}}.bloom{{opacity:0}}}}</style>
<rect x="2" y="2" width="{width-4}" height="{height-4}" rx="20" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
'''
    s += text(25, 31, 'A LITTLE LIGHT, EVERY DAY', 10 if mobile else 11, muted, 650, 'letter-spacing="1.5"')
    s += text(24, 70, 'Firefly Trail', 30 if mobile else 33, 'url(#name)', 750, 'letter-spacing="-.8"')
    s += text(25, 96, 'My commits have a tiny night-shift companion.', 13 if mobile else 16, muted)
    if not mobile:
        s += text(925, 43, f'{count} contributions', 17, ink, 650, 'text-anchor="end"')
        s += text(925, 67, 'the last 365 days', 12, muted, 400, 'text-anchor="end"')
    else:
        s += text(25, 125, f'{count} contributions · the latest 13 weeks', 13, ink, 600)
    # Recessed chart panel, enough room for the travelling companion below it.
    s += f'<rect x="18" y="{gy-29}" width="{width-36}" height="{pitch*7+60}" rx="13" fill="{panel}"/>'
    for row, label in [(1, 'Mon'), (3, 'Wed'), (5, 'Fri')]:
        s += text(29, gy + row * pitch + size - 2, label, 10, muted)
    previous_month = None
    for cell in cells:
        day = date.fromisoformat(cell['date'])
        if day.month != previous_month and (day.day <= 7 or previous_month is None):
            if cell['column'] < columns - 1:
                s += text(cell['x'], gy-10, day.strftime('%b'), 10, muted)
            previous_month = day.month
        label = f'{cell["date"]}: {cell["count"]} contributions'
        s += f'<rect x="{cell["x"]}" y="{cell["y"]}" width="{size}" height="{size}" rx="3" fill="{levels[cell["level"]]}"><title>{label}</title></rect>'
        if cell['count']:
            # Light active squares as the firefly crosses their week, both directions.
            visits = {cell['column'], len(stops)-1-cell['column']}
            for visit in visits:
                if visit == len(stops)-1:
                    continue  # The loop's first visit already covers this point.
                arrival = visit / (len(stops)-1) * duration
                s += f'<rect class="bloom" style="animation-delay:{arrival-duration:.4f}s" x="{cell["x"]}" y="{cell["y"]}" width="{size}" height="{size}" rx="3" fill="#f6c85b" opacity="0"/>'
    x, y = route[0]
    s += f'<g class="cat" style="transform:translate({x:g}px,{y:g}px)"><g transform="translate(-24 12)">{recolour(cat(0,0,2), theme)}</g></g>'
    s += f'<g class="fly" style="transform:translate({x:g}px,{y:g}px)"><circle class="halo" r="17" fill="url(#glow)"/><g class="wings" fill="{gold}" opacity=".65"><ellipse cx="-5" cy="-5" rx="4" ry="2" transform="rotate(25)"/><ellipse cx="5" cy="-5" rx="4" ry="2" transform="rotate(-25)"/></g>{star(-3,-3,1.2,gold)}</g>'
    foot = 376 if mobile else 330
    s += text(25, foot, 'quiet days', 10, muted)
    for level in range(5):
        s += f'<rect x="{88+level*18}" y="{foot-10}" width="12" height="12" rx="3" fill="{levels[level]}"/>'
    s += text(184, foot, 'bright days', 10, muted)
    if mobile:
        s += text(25, 403, period, 11, muted)
        s += text(25, 421, 'Real calendar. A little make-believe.', 10, muted)
    else:
        s += text(925, foot, period, 11, muted, 400, 'text-anchor="end"')
        s += text(25, 367, 'Real calendar. A little make-believe. Follow the glow; the cat knows the way.', 13, muted)
        s += pixel(['..g..','..g..','.ggg.','ggggg','..d..','..d..'], {'g': levels[3], 'd': gold}, 892, 349, 3)
    return svg(width, height, title, s)


def readme_block(snapshot):
    day = snapshot['as_of']
    alt = escape(f'Firefly Trail: a blue pixel cat follows a golden firefly through my real contribution garden. {snapshot["total"]} contributions from {snapshot["from"]} to {day}; mobile shows the latest 13 calendar weeks.', quote=True)
    return f'''{START}
<a name="firefly-trail"></a>
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
    print(f'Firefly Trail: {snapshot["total"]} contributions · {snapshot["from"]} to {day}')


if __name__ == '__main__':
    main()
