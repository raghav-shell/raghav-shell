"""Build the v8 "How I build" strip: interface, API, and workflow as three
stations along the garden path, joined by a dashed route."""

from build_artwork_v4 import text, svg, MONO
from build_artwork_v8 import ASSETS, THEMES, cat, sprout, flower
from build_closing_v8 import shell


def interface(p, x, ground):
    paper = '#ffffff' if p['bar'] == '#f2f8fc' else '#2b4a63'
    s = f'<rect x="{x}" y="{ground - 96}" width="112" height="80" rx="8" fill="{paper}" stroke="{p["frame"]}" stroke-width="3"/>'
    s += f'<rect x="{x + 1.5}" y="{ground - 94.5}" width="109" height="14" rx="6" fill="{p["laptop_base"]}"/>'
    for i, c in enumerate(['#e98b8b', '#f6d277', '#8fdcb5']):
        s += f'<circle cx="{x + 10 + i * 9}" cy="{ground - 87.5}" r="2.6" fill="{c}"/>'
    s += f'<rect x="{x + 10}" y="{ground - 72}" width="44" height="8" rx="2" fill="{p["blue"]}"/>'
    s += f'<rect x="{x + 10}" y="{ground - 58}" width="92" height="4" fill="{p["term_dim"]}"/><rect x="{x + 10}" y="{ground - 50}" width="70" height="4" fill="{p["term_dim"]}"/>'
    s += f'<rect x="{x + 10}" y="{ground - 40}" width="40" height="14" rx="7" fill="{p["mint"]}"/>'
    s += f'<rect x="{x + 50}" y="{ground - 16}" width="12" height="16" fill="{p["frame"]}"/>'
    return s


def api(p, x, ground):
    s = f'<rect x="{x}" y="{ground - 92}" width="84" height="92" rx="6" fill="{p["laptop_base"]}" stroke="{p["frame"]}" stroke-width="3"/>'
    for i in range(3):
        y = ground - 82 + i * 27
        s += f'<rect x="{x + 9}" y="{y}" width="66" height="19" rx="3" fill="{p["screen"]}"/>'
        s += f'<rect x="{x + 15}" y="{y + 7}" width="5" height="5" fill="{p["term_ok"]}"/>'
    s += text(x + 50, ground - 67, '{ }', 11, p['term'], 700, f'text-anchor="middle" font-family="{MONO}"')
    s += text(x + 50, ground - 40, 'GET', 9, p['term'], 700, f'text-anchor="middle" font-family="{MONO}"')
    s += text(x + 50, ground - 13, 'POST', 9, p['term'], 700, f'text-anchor="middle" font-family="{MONO}"')
    return s


def workflow(p, x, ground):
    s = ''
    nodes = [(x, ground - 74), (x + 58, ground - 100), (x + 58, ground - 48), (x + 116, ground - 74)]
    for a, b in [(0, 1), (0, 2), (1, 3), (2, 3)]:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        s += f'<path d="M{x1 + 14} {y1 + 10}L{x2 + 4} {y2 + 10}" stroke="{p["frame"]}" stroke-width="3"/>'
    for i, (nx, ny) in enumerate(nodes):
        fill = p['grass'] if i == 3 else p['laptop']
        s += f'<rect x="{nx}" y="{ny}" width="20" height="20" rx="5" fill="{fill}" stroke="{p["frame"]}" stroke-width="2.5"/>'
    s += f'<path d="M{x + 121} {ground - 64}L{x + 125} {ground - 60}L{x + 132} {ground - 68}" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<rect x="{x + 62}" y="{ground - 26}" width="12" height="26" fill="{p["frame"]}"/>'
    return s


def arrow(p, x1, x2, y):
    s = f'<path d="M{x1} {y}H{x2 - 8}" stroke="{p["mint"]}" stroke-width="3" stroke-dasharray="7 6"/>'
    return s + f'<path d="M{x2 - 12} {y - 7}L{x2} {y}L{x2 - 12} {y + 7}" fill="none" stroke="{p["mint"]}" stroke-width="3" stroke-linejoin="round"/>'


def strip(theme, mobile=False):
    p = THEMES[theme]
    labels = ['a thoughtful interface', 'a working API', 'a clear workflow']
    if mobile:
        width, height, ground = 420, 206, 166
        open_, close = shell(p, 'build', width, height, ground)
        s = open_ + text(22, 38, 'How I build', 18, p['ink'], 750)
        g = f'<g transform="translate(14 {ground}) scale(.62) translate(0 {-ground})">'
        g += interface(p, 10, ground) + arrow(p, 136, 206, ground - 56) + api(p, 216, ground)
        g += arrow(p, 314, 384, ground - 56) + workflow(p, 398, ground) + '</g>'
        s += g
        for lx, label in zip([55, 174, 303], ['interface', 'API', 'workflow']):
            s += text(lx, 88, label, 13, p['ink'], 650, 'text-anchor="middle"')
        s += sprout(p, 386, ground - 18, 3)
    else:
        width, height, ground = 960, 230, 190
        open_, close = shell(p, 'build', width, height, ground)
        s = open_ + text(30, 44, 'How I build', 20, p['ink'], 750)
        stations = [(96, interface, 112, labels[0]), (414, api, 84, labels[1]), (700, workflow, 136, labels[2])]
        for x, draw, w, label in stations:
            s += draw(p, x, ground)
            s += text(x + w / 2, ground - 116, label, 15, p['ink'], 650, 'text-anchor="middle"')
        s += arrow(p, 228, 400, ground - 56) + arrow(p, 518, 688, ground - 56)
        s += cat(p, 870, ground - 44) + sprout(p, 40, ground - 24, 4) + flower(p, 352, ground - 15, '#f0a8c0') + flower(p, 620, ground - 15, '#c7a6ef')
    s += close
    suffix = '-mobile' if mobile else ''
    title = 'How I build: a thoughtful interface, then a working API, then a clear workflow.'
    (ASSETS / f'how-i-build-v8{suffix}-{theme}.svg').write_text(svg(width, height, title, s))


if __name__ == '__main__':
    for theme in THEMES:
        strip(theme)
        strip(theme, mobile=True)
