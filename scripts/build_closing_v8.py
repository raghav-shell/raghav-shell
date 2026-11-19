"""Build the v8 Garden Pairs invitation and the closing "say hello" card.

Both stand on the same sky and garden ground as the v8 hero and project cards.
"""

from build_artwork_v4 import pixel, text, svg, star
from build_artwork_v8 import ASSETS, THEMES, cat, sprout, flower, hills, cloud


def shell(p, slug, width, height, ground):
    """Card frame with sky, distant hills, and the grass strip; returns (open, close)."""
    s = f'<defs><linearGradient id="sky-{slug}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{p["sky_top"]}"/><stop offset="1" stop-color="{p["sky_bot"]}"/></linearGradient>'
    s += f'<clipPath id="clip-{slug}"><rect x="2" y="2" width="{width - 10}" height="{height - 10}" rx="18"/></clipPath></defs>'
    s += f'<rect x="8" y="8" width="{width - 10}" height="{height - 10}" rx="18" fill="{p["shadow"]}"/>'
    s += f'<g clip-path="url(#clip-{slug})"><rect width="{width}" height="{height}" fill="url(#sky-{slug})"/>'
    ridge = [1, 2, 2, 3, 2, 2, 1, 1, 2, 3, 3, 2, 1, 1, 2, 2, 3, 4, 3, 2, 2, 1, 1, 2, 3, 3, 2, 2, 1, 1, 2, 2, 3, 2, 1, 1, 2, 3, 3, 2, 1, 2, 2, 3, 2, 1]
    s += hills(-8, ground, ridge[: width // 20 + 2], 22, p['hill_far'])
    close = f'<rect y="{ground}" width="{width}" height="10" fill="{p["grass"]}"/><rect y="{ground + 10}" width="{width}" height="{height}" fill="{p["soil"]}"/>'
    close += ''.join(f'<rect x="{x}" y="{ground - 4}" width="8" height="4" fill="{p["grass"]}"/>' for x in range(6, width, 36))
    close += ''.join(f'<rect x="{x}" y="{ground + 20}" width="6" height="4" fill="{p["soil_dark"]}"/>' for x in range(30, width, 70))
    close += '</g>' + f'<rect x="2" y="2" width="{width - 10}" height="{height - 10}" rx="18" fill="none" stroke="{p["frame"]}" stroke-width="2"/>'
    return s, close


def pill(p, x, y, label, width):
    """A dark call-to-action pill, matching the terminal colour."""
    s = f'<rect x="{x}" y="{y}" width="{width}" height="40" rx="12" fill="{p["screen"]}" stroke="{p["frame"]}" stroke-width="1.5"/>'
    return s + text(x + width / 2, y + 25, label, 14, p['term'], 700, 'text-anchor="middle"')


# ---- Garden Pairs -------------------------------------------------------

def memory_card(p, x, y, face=None):
    s = f'<rect x="{x}" y="{y}" width="56" height="74" rx="8" fill="{p["frame"]}"/>'
    if face is None:
        s += f'<rect x="{x + 4}" y="{y + 4}" width="48" height="66" rx="5" fill="{p["laptop"]}"/>'
        s += ''.join(f'<rect x="{x + 10 + c * 12}" y="{y + 10 + r * 12}" width="6" height="6" fill="{p["laptop_base"]}"/>' for r in range(5) for c in range(3) if (r + c) % 2 == 0)
    else:
        s += f'<rect x="{x + 4}" y="{y + 4}" width="48" height="66" rx="5" fill="{"#ffffff" if p["bar"] == "#f2f8fc" else "#2b4a63"}"/>' + face
    return s


def game(theme, mobile=False):
    p = THEMES[theme]
    width, height, ground = (420, 330, 290) if mobile else (960, 220, 180)
    open_, close = shell(p, 'pairs', width, height, ground)
    s = open_ + cloud(p, width - 120, 30, 5)
    tag_w = 128
    s += f'<rect x="20" y="20" width="{tag_w}" height="24" rx="12" fill="{p["bar"]}" fill-opacity=".85"/>'
    s += text(20 + tag_w / 2, 36, 'a tiny pause', 12, p['ink'], 600, 'text-anchor="middle"')
    s += text(24, 92, 'Garden Pairs', 38, p['ink'], 800, 'letter-spacing="-1.2"')
    if mobile:
        s += text(26, 120, 'Eight cards, four pairs, no timer.', 15, p['muted'], 500)
        s += pill(p, 26, 138, 'Play Garden Pairs ↗', 180)
        x0 = 70
    else:
        s += text(26, 122, 'Eight cards, four pairs, one small happy break.', 17, p['muted'], 500)
        s += pill(p, 26, 136, 'Play Garden Pairs ↗', 190)
        x0 = 560
    sun = pixel(['..yy..', '.yyyy.', 'yyyyyy', 'yyyyyy', '.yyyy.', '..yy..'], {'y': '#f6d277'}, 0, 0, 4)
    y = ground - 78
    s += memory_card(p, x0, y)
    s += memory_card(p, x0 + 66, y - 6, f'<g transform="translate({x0 + 66 + 16} {y - 6 + 25})">{sun}</g>')
    s += memory_card(p, x0 + 132, y - 6, f'<g transform="translate({x0 + 132 + 16} {y - 6 + 25})">{sun}</g>')
    s += memory_card(p, x0 + 198, y)
    s += f'<circle cx="{x0 + 160}" cy="{y - 20}" r="13" fill="{p["grass"]}" stroke="{p["frame"]}" stroke-width="2"/>'
    s += f'<path d="M{x0 + 154} {y - 20}L{x0 + 158} {y - 15}L{x0 + 166} {y - 25}" fill="none" stroke="#ffffff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
    s += '' if mobile else star(x0 + 112, y - 44, 3, '#e9be66')
    s += cat(p, x0 + 270, ground - 44)
    s += sprout(p, x0 - 44, ground - 24, 4) + flower(p, x0 + 330, ground - 15, '#f0a8c0')
    s += close
    suffix = '-mobile' if mobile else ''
    title = 'Play Garden Pairs: a tiny matching game with eight cards and four pairs, no timer. Memory cards stand on the grass beside a blue pixel cat.'
    (ASSETS / f'game-card-v8{suffix}-{theme}.svg').write_text(svg(width, height, title, s))


# ---- Say hello ----------------------------------------------------------

def mailbox(p, x, ground):
    s = f'<rect x="{x + 30}" y="{ground - 70}" width="10" height="70" fill="{p["crate_dark"]}"/>'
    s += f'<path d="M{x} {ground - 70}V{ground - 104}Q{x} {ground - 124} {x + 22} {ground - 124}H{x + 48}Q{x + 70} {ground - 124} {x + 70} {ground - 104}V{ground - 70}Z" fill="{p["laptop"]}" stroke="{p["frame"]}" stroke-width="3"/>'
    s += f'<path d="M{x + 10} {ground - 78}V{ground - 102}Q{x + 10} {ground - 114} {x + 22} {ground - 114}H{x + 40}" fill="none" stroke="{p["frame"]}" stroke-width="2"/>'
    s += f'<rect x="{x + 66}" y="{ground - 126}" width="5" height="40" fill="{p["frame"]}"/>'
    s += f'<rect x="{x + 71}" y="{ground - 126}" width="22" height="14" fill="#e05f5f"/>'
    return s


def letter(p, x, y):
    s = f'<g transform="rotate(-12 {x + 26} {y + 17})"><rect x="{x}" y="{y}" width="52" height="34" rx="3" fill="#ffffff" stroke="{p["frame"]}" stroke-width="2.5"/>'
    s += f'<path d="M{x + 2} {y + 3}L{x + 26} {y + 20}L{x + 50} {y + 3}" fill="none" stroke="{p["frame"]}" stroke-width="2.5" stroke-linejoin="round"/>'
    return s + f'<rect x="{x + 38}" y="{y + 22}" width="8" height="7" fill="#e05f5f"/></g>'


def connect(theme, mobile=False):
    p = THEMES[theme]
    width, height, ground = (420, 400, 360) if mobile else (960, 260, 220)
    open_, close = shell(p, 'hello', width, height, ground)
    s = open_ + ('' if mobile else cloud(p, 380, 34, 5))
    if mobile:
        s += text(24, 66, 'Have something', 32, p['ink'], 800, 'letter-spacing="-1"')
        s += text(24, 104, 'fun to build?', 32, p['ink'], 800, 'letter-spacing="-1"')
        s += text(26, 134, 'Hackathon teams and software collabs:', 15, p['muted'], 500)
        s += text(26, 154, 'I’d love to hear about it.', 15, p['muted'], 500)
        s += pill(p, 26, 172, 'Say hello on LinkedIn ↗', 210)
        mx, lx, ly = 240, 70, 250
    else:
        s += text(36, 88, 'Have something fun to build?', 40, p['ink'], 800, 'letter-spacing="-1.4"')
        s += text(38, 122, 'Hackathon teams and software collaborations: I’d love to hear about it.', 17, p['muted'], 500)
        s += pill(p, 38, 144, 'Say hello on LinkedIn ↗', 222)
        mx, lx, ly = 760, 610, 56
    s += mailbox(p, mx, ground)
    # A dashed flight path from the mailbox to the letter.
    if mobile:
        s += f'<path d="M{mx - 6} {ground - 110}Q{mx - 70} {ground - 150} {lx + 60} {ly + 18}" fill="none" stroke="{p["mint"]}" stroke-width="3" stroke-dasharray="7 6"/>'
    else:
        s += f'<path d="M{mx - 6} {ground - 110}Q{mx - 70} {ly - 10} {lx + 60} {ly + 18}" fill="none" stroke="{p["mint"]}" stroke-width="3" stroke-dasharray="7 6"/>'
    s += letter(p, lx, ly)
    s += star(lx - 18, ly - 6, 2, '#e9be66') + star(lx + 70, ly - 18, 3, '#e9be66')
    s += cat(p, mx + 96, ground - 44)
    s += sprout(p, mx - 60, ground - 24, 4) + flower(p, mx + 150, ground - 15, '#c7a6ef')
    s += close
    suffix = '-mobile' if mobile else ''
    title = ('Have something fun to build? Hackathon teams and software collaborations welcome. Say hello on LinkedIn. '
             'A blue pixel cat sits beside a mailbox with its flag up while a letter flies off.')
    (ASSETS / f'connect-v8{suffix}-{theme}.svg').write_text(svg(width, height, title, s))


if __name__ == '__main__':
    for theme in THEMES:
        for mobile in (False, True):
            game(theme, mobile)
            connect(theme, mobile)
