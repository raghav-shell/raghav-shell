"""Build the v8 hero scene and tech-stack panel for the profile README.

The hero widens the pixel garden into a full scene: sky, layered hills, a
ground strip, and a desk where a laptop terminal types out each project in
turn. The stack panel gathers the tool logos into one composed card.
"""

from pathlib import Path
import re
from build_artwork_v4 import pixel, text, svg, star, MONO

ASSETS = Path(__file__).resolve().parents[1] / 'assets'

THEMES = {
    'light': dict(
        sky_top='#d9edf9', sky_bot='#f5fbfe', hill_far='#cfe5ec', hill_near='#b4dbc9',
        grass='#6cad8c', grass_dark='#4f9174', soil='#c79a68', soil_dark='#a87d50',
        ink='#19364b', muted='#4c6e83', blue='#2869a4', mint='#237d72',
        frame='#46697e', bar='#f2f8fc', shadow='#c9dce8', cloud='#ffffff',
        laptop='#8bbbd8', laptop_base='#c3ddeb', crate='#d8a96b', crate_dark='#a8794a',
        screen='#13293d', term='#c2ead8', term_dim='#7fa7bf', term_ok='#8fdcb5',
        chip='#e6f1f8', chip_line='#cfe0ea', panel='#f2f8fc',
        cat_d='#446b85', cat_l='#bbdcef', cat_k='#19364b', cat_p='#e9be66'),
    'dark': dict(
        sky_top='#0a1520', sky_bot='#16304a', hill_far='#1b3549', hill_near='#1d443b',
        grass='#3f8a6c', grass_dark='#2c6a52', soil='#5a4630', soil_dark='#3f3122',
        ink='#e1edf5', muted='#abc3d3', blue='#8bc9f4', mint='#92d8c0',
        frame='#4d728c', bar='#101e2b', shadow='#080f17', cloud='#2a4459',
        laptop='#558bae', laptop_base='#314f64', crate='#8a6640', crate_dark='#5e4429',
        screen='#060e16', term='#c2ead8', term_dim='#6f93ab', term_ok='#8fdcb5',
        chip='#152a3b', chip_line='#24425a', panel='#101e2b',
        cat_d='#7fb3d6', cat_l='#d5ebf7', cat_k='#0b1622', cat_p='#e9be66'),
}

# What the laptop types, in order. Short enough for the screen (24 columns).
PROJECTS = [('aegis', 'local AI workbench'), ('visionx', 'vision model review'),
            ('razorflow', 'payment recovery'), ('competeiq', 'research to reports'),
            ('lexguard', 'contract risk notes'), ('os_shell', 'a shell, in Java')]
SLOT = 3.5
CYCLE = SLOT * len(PROJECTS)


def cat(p, x, y, scale=4):
    rows = ['.dd.....dd.', '.dld...dld.', '.dllllllld.', '.dllldlldd.', '.dlklllkld.', '.dllllllld.',
            '..dllplld..', '..ddddddd..', '.dlllldlld.', '.dlllldlld.', '..dd...dd..']
    return pixel(rows, {'d': p['cat_d'], 'l': p['cat_l'], 'p': p['cat_p'], 'k': p['cat_k']}, x, y, scale)


def sprout(p, x, y, scale=4):
    return pixel(['.gg...', '.ggg..', '...g..', '...ggg', '...gg.', '...g..'], {'g': p['grass']}, x, y, scale)


def flower(p, x, y, petal, scale=3):
    return pixel(['.p.', 'pyp', '.p.', '.g.', '.g.'], {'p': petal, 'y': '#f6d277', 'g': p['grass_dark']}, x, y, scale)


def hills(x0, base, heights, block, color):
    """A stepped pixel ridge: one column of `block` width per height."""
    d = f'M{x0} {base}'
    for i, h in enumerate(heights):
        d += f'V{base - h * block}H{x0 + (i + 1) * block}'
    return f'<path d="{d}V{base}Z" fill="{color}" shape-rendering="crispEdges"/>'


def cloud(p, x, y, scale=6):
    return pixel(['..xxx...', '.xxxxxx.', 'xxxxxxxx'], {'x': p['cloud']}, x, y, scale)


def sky_light(p, theme):
    if theme == 'light':
        sun = ['..yyyy..', '.yyyyyy.', 'yyyyyyyy', 'yyyyyyyy', 'yyyyyyyy', '.yyyyyy.', '..yyyy..']
        return pixel(sun, {'y': '#f6d277'}, -8, -8, 8)
    moon = ['..mmm...', '.mmm....', 'mmm.....', 'mmm.....', 'mmm.....', '.mmm....', '..mmm...']
    return pixel(moon, {'m': '#f3e7b8'}, -8, -8, 8)


def terminal(p, x, y, width):
    """The focal point: a terminal that types `$ ship <project>` then its result."""
    s = f'<rect x="{x}" y="{y}" width="{width}" height="15" fill="#ffffff" fill-opacity=".06"/>'
    for i, c in enumerate(['#e98b8b', '#f6d277', '#8fdcb5']):
        s += f'<circle cx="{x + 9 + i * 9}" cy="{y + 7.5}" r="2.6" fill="{c}"/>'
    s += text(x + width - 8, y + 11, 'garden.sh', 8, p['term_dim'], 500, f'text-anchor="end" font-family="{MONO}"')
    s += text(x + 9, y + 34, '~/garden', 10, p['term_dim'], 500, f'font-family="{MONO}"')
    char = 6.02  # monospace advance at 10px
    for i, (slug, result) in enumerate(PROJECTS):
        command = f'$ ship {slug}'
        mask_w = round(len(command) * char + 4, 1)
        s += f'<g class="slot{" first" if i == 0 else ""}" style="animation-delay:{i * SLOT}s">'
        s += text(x + 9, y + 54, command, 10, p['term'], 600, f'font-family="{MONO}"')
        s += (f'<rect class="mask" x="{x + 7}" y="{y + 44}" width="{mask_w}" height="14" fill="{p["screen"]}" '
              f'style="animation-delay:{i * SLOT}s;animation-timing-function:steps({len(command)})"/>')
        s += text(x + 9, y + 72, f'✓ {result}', 10, p['term_ok'], 500, f'class="answer" style="animation-delay:{i * SLOT}s" font-family="{MONO}"')
        s += '</g>'
    s += f'<rect class="caret" x="{x + 9}" y="{y + 80}" width="6" height="10" fill="{p["term"]}"/>'
    return s


def motion():
    type_end = round(1.1 / CYCLE * 100, 2)
    slot_end = round(SLOT / CYCLE * 100, 2)
    answer_on = round(1.5 / CYCLE * 100, 2)
    return f'''<style>
    .slot{{opacity:0;animation:slot {CYCLE}s step-end infinite}}
    .mask{{transform-box:fill-box;transform-origin:100% 50%;animation:type {CYCLE}s infinite}}
    .answer{{opacity:0;animation:answer {CYCLE}s step-end infinite}}
    .caret{{animation:caret 1.1s step-end infinite}}
    @keyframes slot{{0%{{opacity:1}}{slot_end}%,100%{{opacity:0}}}}
    @keyframes type{{0%{{transform:scaleX(1)}}{type_end}%,100%{{transform:scaleX(0)}}}}
    @keyframes answer{{0%{{opacity:0}}{answer_on}%{{opacity:1}}{slot_end}%,100%{{opacity:0}}}}
    @keyframes caret{{50%{{opacity:0}}}}
    .wave{{transform-box:fill-box;transform-origin:50% 90%;animation:wave 5s ease-in-out infinite}}
    @keyframes wave{{0%,35%,100%{{transform:rotate(0)}}5%,15%,25%{{transform:rotate(16deg)}}10%,20%,30%{{transform:rotate(-10deg)}}}}
    @media(prefers-reduced-motion:reduce){{.slot,.mask,.answer,.caret,.wave{{animation:none}}.first,.first .answer{{opacity:1}}.mask{{display:none}}}}
    </style>'''


def wave(x, y, scale=1):
    hand = (f'<g transform="translate({x} {y}) scale({scale})"><path d="M8 24V10a3 3 0 0 1 6 0v11V5a3 3 0 0 1 6 0v16V8a3 3 0 0 1 6 0v15V14a3 3 0 0 1 6 0v21q0 12-12 12h-5q-5 0-8-6L1 30q-3-5 1-7q3-1 6 1Z" '
            'fill="#f6d277" stroke="#806535" stroke-width="2" stroke-linejoin="round"/><path d="M10 29q9-4 15 2" fill="none" stroke="#bd964e" stroke-width="2" stroke-linecap="round"/></g>')
    return f'<g class="wave">{hand}</g>'


def scene(p, theme):
    """The desk scene in local coordinates: 400 wide, ground line at y=200."""
    s = f'<g transform="translate(318 0)">{sky_light(p, theme)}</g>'
    s += cloud(p, 0, 40, 6) + cloud(p, 236, 76, 5)
    if theme == 'dark':
        for sx, sy, sc in [(40, 10, 2), (150, 20, 1), (260, 6, 2), (380, 96, 1), (110, 96, 1)]:
            s += star(sx, sy, sc, '#f3e7b8')
    s += hills(-40, 200, [3, 4, 5, 6, 7, 8, 8, 9, 9, 8, 7, 6, 6, 7, 8, 9, 10, 10, 9, 8, 7, 6, 5, 5, 6, 7, 8], 16, p['hill_far'])
    s += hills(-40, 200, [2, 3, 4, 4, 5, 4, 3, 3, 2, 2, 3, 3, 4, 4, 5, 5, 4, 3, 3, 4, 5, 5, 4, 3, 3, 2, 3], 16, p['hill_near'])
    # The crate desk.
    s += f'<rect x="88" y="160" width="204" height="40" fill="{p["crate"]}"/>'
    s += f'<path d="M88 173H292M88 186H292" stroke="{p["crate_dark"]}" stroke-width="2"/>'
    s += f'<path d="M100 160V200M280 160V200" stroke="{p["crate_dark"]}" stroke-width="4"/>'
    # The laptop and its terminal.
    s += f'<rect x="100" y="28" width="180" height="126" rx="9" fill="{p["laptop"]}" stroke="{p["frame"]}" stroke-width="3"/>'
    s += f'<rect x="109" y="37" width="162" height="106" rx="4" fill="{p["screen"]}"/>'
    s += terminal(p, 109, 37, 162)
    s += f'<path d="M100 154L84 164H296L280 154Z" fill="{p["laptop_base"]}" stroke="{p["frame"]}" stroke-width="3" stroke-linejoin="round"/>'
    s += f'<rect x="170" y="156" width="40" height="4" rx="2" fill="{p["laptop"]}"/>'
    # Garden company.
    s += cat(p, 314, 156)
    s += sprout(p, 40, 176) + sprout(p, 364, 180, 3)
    s += flower(p, 66, 185, '#f0a8c0') + flower(p, 300, 185, '#c7a6ef')
    return s


def ground(p, width, top, bottom):
    s = f'<rect x="0" y="{top}" width="{width}" height="{bottom - top}" fill="{p["soil"]}"/>'
    s += f'<rect x="0" y="{top}" width="{width}" height="10" fill="{p["grass"]}"/>'
    bumps = ''.join(f'<rect x="{x}" y="{top - 4}" width="8" height="4" fill="{p["grass"]}"/>' for x in range(4, width, 36))
    tufts = ''.join(f'<rect x="{x}" y="{top + 10}" width="8" height="4" fill="{p["grass_dark"]}"/>' for x in range(20, width, 52))
    pebbles = ''.join(f'<rect x="{x}" y="{top + 24 + (x // 7) % 3 * 6}" width="6" height="4" fill="{p["soil_dark"]}"/>' for x in range(30, width, 70))
    return s + f'<g shape-rendering="crispEdges">{bumps}{tufts}{pebbles}</g>'


def frame(p, width, height, label):
    s = f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{p["sky_top"]}"/><stop offset="1" stop-color="{p["sky_bot"]}"/></linearGradient>'
    s += f'<linearGradient id="ink" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{p["blue"]}"/><stop offset="1" stop-color="{p["mint"]}"/></linearGradient>'
    s += f'<clipPath id="window"><rect x="2" y="2" width="{width - 10}" height="{height - 10}" rx="20"/></clipPath></defs>'
    s += f'<rect x="8" y="8" width="{width - 10}" height="{height - 10}" rx="20" fill="{p["shadow"]}"/>'
    return s, f'<rect x="2" y="2" width="{width - 10}" height="{height - 10}" rx="20" fill="none" stroke="{p["frame"]}" stroke-width="2"/>'


def bar(p, width, bar_h, label, size):
    s = f'<rect x="0" y="0" width="{width}" height="{bar_h}" fill="{p["bar"]}"/><path d="M0 {bar_h}H{width}" stroke="{p["frame"]}" stroke-width="1.5"/>'
    for i, c in enumerate(['#8bbddd', '#f6cf69', '#a1d7b0']):
        s += f'<circle cx="{24 + i * 17}" cy="{bar_h / 2 + 1}" r="5" fill="{c}"/>'
    s += text(84, bar_h / 2 + 5, label, size, p['muted'], 500, f'font-family="{MONO}"')
    return s


def hero(theme, mobile=False):
    p = THEMES[theme]
    alt = ("Hi, I’m Raghav, a student developer in India building full-stack apps and AI workflows for international hackathons. "
           "A pixel garden scene: a laptop on a crate types out each project in turn while a blue cat sits beside it.")
    if mobile:
        width, height, bar_h, gy = 420, 600, 40, 520
        open_, close = frame(p, width, height, '')
        body = f'<rect width="{width}" height="{height}" fill="url(#sky)"/>'
        body += f'<g transform="translate(12 {gy - 200})">{scene(p, theme)}</g>'
        body += ground(p, width, gy, height)
        body += bar(p, width, bar_h, 'raghav’s little internet garden', 10)
        body += text(26, 98, 'hi, I’m', 34, p['ink'], 700, 'letter-spacing="-1"')
        body += wave(150, 64, .8)
        body += text(20, 172, 'Raghav', 84, 'url(#ink)', 800, 'letter-spacing="-4"')
        body += f'<rect class="caret" x="302" y="164" width="22" height="7" rx="2" fill="{p["mint"]}"/>'
        for i, line in enumerate(['I build full-stack apps and AI', 'workflows, and take them to', 'international hackathons.']):
            body += text(26, 214 + i * 26, line, 18, p['muted'], 450)
        body += status(p, 26, 302, 11)
    else:
        width, height, bar_h, gy = 960, 440, 48, 384
        open_, close = frame(p, width, height, '')
        body = f'<rect width="{width}" height="{height}" fill="url(#sky)"/>'
        body += hills(-10, gy, [1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1], 12, p['hill_far'])
        body += cloud(p, 470, 92, 6)
        body += f'<g transform="translate(500 {gy - 220}) scale(1.1)">{scene(p, theme)}</g>'
        body += ground(p, width, gy, height)
        body += bar(p, width, bar_h, 'raghav’s little internet garden', 12)
        body += text(width - 26, bar_h / 2 + 5, 'hello, world :)', 12, p['muted'], 500, f'text-anchor="end" font-family="{MONO}"')
        body += text(42, 128, 'hi, I’m', 46, p['ink'], 700, 'letter-spacing="-1.5"')
        body += wave(206, 84, 1.05)
        body += text(34, 236, 'Raghav', 118, 'url(#ink)', 800, 'letter-spacing="-6"')
        body += f'<rect class="caret" x="446" y="226" width="30" height="9" rx="2" fill="{p["mint"]}"/>'
        for i, line in enumerate(['I build full-stack apps and AI workflows,', 'and take them to international hackathons.']):
            body += text(44, 280 + i * 28, line, 20, p['muted'], 450)
        body += status(p, 44, 352, 12)
    content = open_ + motion() + f'<g clip-path="url(#window)">{body}</g>' + close
    return svg(width, height, alt, content)


def status(p, x, y, size):
    """Location and availability, each with a small pixel marker."""
    pin = pixel(['.pp.', 'pppp', 'pppp', '.pp.', '.pp.'], {'p': p['blue']}, x, y - 9, 2)
    s = pin + text(x + 14, y, 'India', size + 1, p['ink'], 600)
    dot_x = x + 14 + 0.62 * (size + 1) * 5 + 22
    s += f'<rect x="{dot_x}" y="{y - 8}" width="8" height="8" fill="{p["grass"]}" shape-rendering="crispEdges"/>'
    s += text(dot_x + 14, y, 'open to hackathon teams', size + 1, p['ink'], 600)
    return s


STACK = [
    ('Interfaces', 'what people see and touch', ['typescript', 'react', 'nextjs', 'tailwindcss', 'vitejs']),
    ('APIs & data', 'where the work gets done', ['python', 'fastapi', 'pydantic', 'postgresql', 'sqlalchemy', 'sqlite', 'redis', 'celery']),
    ('AI workflows', 'models, retrieval, and agents', ['langgraph', 'ollama', 'googlegemini', 'openrouter', 'tavily']),
    ('Build & check', 'shipping it with confidence', ['git', 'docker', 'pytest', 'java']),
]
NAMES = {'tailwindcss': 'Tailwind', 'vitejs': 'Vite', 'nextjs': 'Next.js', 'typescript': 'TypeScript', 'googlegemini': 'Gemini',
         'postgresql': 'Postgres', 'fastapi': 'FastAPI', 'sqlite': 'SQLite', 'pytest': 'pytest', 'sqlalchemy': 'SQLAlchemy', 'openrouter': 'OpenRouter', 'langgraph': 'LangGraph', 'docker': 'Docker'}


def logo(slug, theme, x, y, size):
    raw = (ASSETS / 'stack' / f'{slug}-{theme}.svg').read_text()
    # The tile is: frame rect, nested logo <svg>, then a text label. Keep only the logo.
    start = raw.index('<svg', raw.index('<rect'))
    inner = raw[start:raw.rindex('<text')]
    opening = inner[:inner.index('>') + 1]
    placed = re.sub(r' (x|y|width|height)="[\d.]+"', '', opening)
    placed = placed.replace('<svg ', f'<svg x="{x}" y="{y}" width="{size}" height="{size}" ', 1)
    inner = placed + inner[len(opening):]
    for ident in set(re.findall(r'\bid="([^"]+)"', inner)):
        new = f'{slug}-{ident}'
        inner = inner.replace(f'id="{ident}"', f'id="{new}"').replace(f'#{ident})', f'#{new})').replace(f'"#{ident}"', f'"#{new}"')
    return inner


def name(slug):
    return NAMES.get(slug, slug.capitalize())


def stack(theme, mobile=False):
    p = THEMES[theme]
    alt = 'Tech stack. ' + ' '.join(f'{title}: ' + ', '.join(name(t) for t in tools) + '.' for title, _, tools in STACK)
    if mobile:
        width, col_w, per_row, tile, gap, row_h = 420, 404, 5, 68, 10, 78
    else:
        width, col_w, per_row, tile, gap, row_h = 960, 468, 8, 46, 8, 72

    def panel_h(tools):
        return 70 + -(-len(tools) // per_row) * row_h + 8

    if mobile:
        positions, y = [], 0
        for _, _, tools in STACK:
            positions.append((8, y))
            y += panel_h(tools) + 14
        height = y
    else:
        top = max(panel_h(t) for _, _, t in STACK[:2])
        positions = [(0, 0), (492, 0), (0, top + 20), (492, top + 20)]
        height = top + 20 + max(panel_h(t) for _, _, t in STACK[2:]) + 4
    s = ''
    for (title, note, tools), (px, py) in zip(STACK, positions):
        h = panel_h(tools) if mobile else (positions[2][1] - 20 if py == 0 else height - py - 4)
        s += f'<rect x="{px + 1}" y="{py + 1}" width="{col_w - 2}" height="{h}" rx="16" fill="{p["panel"]}" stroke="{p["chip_line"]}"/>'
        s += text(px + 22, py + 34, title, 18, p['ink'], 700, 'letter-spacing="-.3"')
        s += text(px + 22, py + 52, note, 12, p['muted'], 450)
        for i, slug in enumerate(tools):
            r, c = divmod(i, per_row)
            tx = px + 18 + c * (tile + gap)
            ty = py + 70 + r * row_h
            if mobile:
                s += f'<rect x="{tx}" y="{ty}" width="{tile}" height="{tile}" rx="12" fill="{p["chip"]}"/>'
                s += logo(slug, theme, tx + tile / 2 - 15, ty + 10, 30)
                s += text(tx + tile / 2, ty + tile - 9, name(slug), 9, p['muted'], 600, 'text-anchor="middle"')
            else:
                s += f'<rect x="{tx}" y="{ty}" width="{tile}" height="{tile}" rx="12" fill="{p["chip"]}"/>'
                s += logo(slug, theme, tx + 11, ty + 11, tile - 22)
                s += text(tx + tile / 2, ty + tile + 15, name(slug), 9, p['muted'], 600, 'text-anchor="middle"')
    return svg(width, height, alt, s)


def build():
    for theme in THEMES:
        (ASSETS / f'profile-header-v8-{theme}.svg').write_text(hero(theme))
        (ASSETS / f'profile-header-v8-mobile-{theme}.svg').write_text(hero(theme, mobile=True))
        (ASSETS / f'stack-panel-v8-{theme}.svg').write_text(stack(theme))
        (ASSETS / f'stack-panel-v8-mobile-{theme}.svg').write_text(stack(theme, mobile=True))


if __name__ == '__main__':
    build()
