"""Enhance the v5 garden in place with a greeting, colour, and gentle motion."""

from pathlib import Path
import re
import xml.etree.ElementTree as ET
import build_artwork_v4 as pixel

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', NS[1:-1])
PHRASES = ['Thoughtful code. A little imagination.',
           'From a small idea to a useful workflow.',
           'Learning, building, getting better.']
TITLES = [('about', 'A little about me'), ('projects', 'Things I’ve been building'),
          ('progress', 'A little progress lately'), ('tools', 'Tools I reach for'),
          ('stack', 'Tech stack')]


def palette(theme):
    if theme == 'dark':
        return dict(ink='#e1edf5', muted='#abc3d3', blue='#8bc9f4', mint='#92d8c0',
                    border='#4d728c', bg='#101e2b', shadow='#080f17', chip='#25485f')
    return dict(ink='#19364b', muted='#4c6e83', blue='#2869a4', mint='#237d72',
                border='#46697e', bg='#f2f8fc', shadow='#c9dce8', chip='#dcecf8')


def gradient(p):
    return f'<defs><linearGradient id="ink" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{p["blue"]}"/><stop offset="1" stop-color="{p["mint"]}"/></linearGradient></defs>'


def motion():
    return '''<style>
    .wave{transform-box:fill-box;transform-origin:50% 90%;animation:wave 5s ease-in-out infinite}
    .cursor{animation:cursor 1.4s step-end infinite}
    .phrase{animation:phrase 18s ease-in-out infinite}
    .phrase.second{animation-delay:-12s}.phrase.third{animation-delay:-6s}
    @keyframes wave{0%,35%,100%{transform:rotate(0)}5%,15%,25%{transform:rotate(16deg)}10%,20%,30%{transform:rotate(-10deg)}}
    @keyframes cursor{50%{opacity:0}}
    @keyframes phrase{0%,27%,100%{opacity:1;transform:translateY(0)}31%,96%{opacity:0;transform:translateY(-5px)}97%{opacity:0;transform:translateY(5px)}}
    @media(prefers-reduced-motion:reduce){.wave,.cursor,.phrase{animation:none}.phrase.second,.phrase.third{opacity:0}}
    </style>'''


def wave(x, y, scale=4):
    hand = f'<g transform="translate({x} {y}) scale({scale/4})"><path d="M8 24V10a3 3 0 0 1 6 0v11V5a3 3 0 0 1 6 0v16V8a3 3 0 0 1 6 0v15V14a3 3 0 0 1 6 0v21q0 12-12 12h-5q-5 0-8-6L1 30q-3-5 1-7q3-1 6 1Z" fill="#f6d277" stroke="#806535" stroke-width="2" stroke-linejoin="round"/><path d="M10 29q9-4 15 2" fill="none" stroke="#bd964e" stroke-width="2" stroke-linecap="round"/></g>'
    return f'<g class="wave">{hand}</g>'


def phrases(x, y, size, color):
    content = ''
    for i, line in enumerate(PHRASES):
        cls = ['first', 'second', 'third'][i]
        content += pixel.text(x, y, line, size, color, 500,
                              f'class="phrase {cls}" opacity="{1 if i == 0 else 0}"')
    return content


def desktop_header(theme):
    p = palette(theme)
    raw = (ASSETS / f'profile-header-v5-{theme}.svg').read_text()
    raw = raw.replace('</defs>', '</defs>' + gradient(p) + motion(), 1)
    raw, n = re.subn(r'<text[^>]*>Raghav\.</text>',
        pixel.text(29, 247, 'Raghav.', 82, 'url(#ink)', 800, 'letter-spacing="-4"') +
        f'<rect class="cursor" x="325" y="241" width="24" height="6" rx="2" fill="{p["mint"]}"/>', raw)
    assert n == 1
    raw, n = re.subn(r'<text[^>]*>Thoughtful code\. A little imagination\.</text>',
                    phrases(36, 286, 20, p['muted']), raw)
    assert n == 1
    raw = raw.replace('translateY(-6px)', 'translateY(-10px)')
    raw = raw.replace('</g></svg>', wave(273, 121) + '</g></svg>')
    (ASSETS / f'profile-header-v7-{theme}.svg').write_text(raw)


def mobile_header(theme):
    p = palette(theme)
    source = ET.parse(ASSETS / f'profile-header-v5-{theme}.svg').getroot()
    art = list(source)[1]
    # Reuse the exact original computer, plants, and cat, without external images.
    objects = list(art)
    start = next(i for i, node in enumerate(objects) if node.tag == NS + 'rect' and node.get('x') == '639')
    end = next(i for i, node in enumerate(objects) if node.tag == NS + 'text' and node.get('x') == '742')
    scene = ''.join(ET.tostring(node, encoding='unicode') for node in objects[start:end])
    s = gradient(p) + motion()
    s += '<style>.eyes{animation:blink 7s step-end infinite}@keyframes blink{95%,97%{opacity:0}}@media(prefers-reduced-motion:reduce){.eyes{animation:none}}</style>'
    s += f'<rect x="5" y="7" width="411" height="370" rx="18" fill="{p["shadow"]}"/><rect x="1" y="1" width="412" height="370" rx="18" fill="{p["bg"]}" stroke="{p["border"]}" stroke-width="2"/><path d="M2 39H412" stroke="{p["border"]}"/>'
    for x, color in [(19, '#8bbddd'), (35, '#f6cf69'), (51, '#a1d7b0')]:
        s += f'<circle cx="{x}" cy="20" r="4" fill="{color}"/>'
    s += pixel.text(71, 24, "raghav’s little internet garden", 10, p['muted'], 600)
    s += pixel.text(23, 92, "hi, i'm", 39, p['ink'], 750, 'letter-spacing="-1"')
    s += pixel.text(20, 161, 'Raghav.', 68, 'url(#ink)', 800, 'letter-spacing="-3"')
    s += f'<rect class="cursor" x="266" y="157" width="22" height="5" rx="2" fill="{p["mint"]}"/>'
    s += wave(231, 61, 3)
    s += phrases(24, 192, 18, p['muted'])
    for x, width, label, color in [(24, 103, 'full-stack', p['chip']), (135, 113, 'AI workflows', '#c9e9d9' if theme == 'light' else '#234b3e'), (256, 118, 'hackathons', '#ffe5a1' if theme == 'light' else '#554728')]:
        s += f'<rect x="{x}" y="210" width="{width}" height="26" rx="13" fill="{color}"/>'
        s += pixel.text(x + width / 2, 227, label, 11, p['ink'], 600, 'text-anchor="middle"')
    s += f'<svg x="82" y="246" width="252" height="95" viewBox="550 137 380 185">{scene}</svg>'
    s += pixel.text(207, 354, 'small ideas grow here.', 12, p['muted'], 500, 'text-anchor="middle"')
    (ASSETS / f'profile-header-v7-mobile-{theme}.svg').write_text(pixel.svg(420, 380, 'Hi, I’m Raghav. Full-stack applications, AI workflows, and hackathons.', s))


def headings(theme):
    p = palette(theme)
    for index, (slug, title) in enumerate(TITLES):
        for mobile in [False, True]:
            width, size = (420, 27) if mobile else (960, 32)
            s = gradient(p)
            s += f'<rect x="1" y="8" width="34" height="34" rx="10" fill="{p["chip"]}"/>'
            # A pixel sparkle, a folder, a sprout, brackets, and a stack.
            icons = [pixel.star(10, 17, 3, p['blue']),
                     f'<path d="M9 19H17L20 22H28V33H9Z" stroke="{p["blue"]}" stroke-width="2"/>',
                     f'<path d="M18 34V22M18 26Q8 26 9 18Q18 18 18 26M18 30Q29 30 28 22Q18 22 18 30" stroke="{p["mint"]}" stroke-width="2"/>',
                     pixel.text(7, 32, '</>', 13, p['blue'], 700),
                     f'<path d="M9 21L18 16L27 21L18 26ZM9 27L18 32L27 27M9 32L18 37L27 32" stroke="{p["blue"]}" stroke-width="2"/>']
            s += icons[index] + pixel.text(48, 35, title, size, 'url(#ink)', 750, 'letter-spacing="-.7"')
            # The title stays still; GitHub adds its native heading underline.
            suffix = '-mobile' if mobile else ''
            (ASSETS / f'heading-{slug}-v7{suffix}-{theme}.svg').write_text(pixel.svg(width, 48, title, s))


def companions(theme):
    raw = (ASSETS / f'garden-v5-{theme}.svg').read_text()
    raw = raw.replace('translate(462 8) scale(3)', 'translate(456 10) scale(4)')
    raw = raw.replace('@keyframes hop{0%,40%,60%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}',
        '@keyframes hop{0%,100%{transform:translate(0,0)}25%{transform:translate(-18px,-6px)}50%{transform:translate(0,0)}75%{transform:translate(18px,-6px)}}')
    (ASSETS / f'garden-v7-{theme}.svg').write_text(raw)
    for slug in ['aegis', 'visionx', 'razorflow', 'competeiq', 'lexguard', 'shell']:
        root = ET.parse(ASSETS / f'project-{slug}-v5-{theme}.svg').getroot()
        g = list(root)[1]
        style = ET.Element(NS + 'style')
        style.text = '.project-mark{animation:drift 6s ease-in-out infinite}@keyframes drift{50%{transform:translateY(-5px)}}@media(prefers-reduced-motion:reduce){.project-mark{animation:none}}'
        g.insert(0, style)
        icon = next(n for n in g if n.tag == NS + 'g' and n.get('transform') == 'translate(523 56) scale(.62)')
        position = list(g).index(icon)
        g.remove(icon)
        wrapper = ET.Element(NS + 'g', {'class': 'project-mark'})
        wrapper.append(icon)
        g.insert(position, wrapper)
        (ASSETS / f'project-{slug}-v7-{theme}.svg').write_text(ET.tostring(root, encoding='unicode') + '\n')
    raw = (ASSETS / f'connect-v5-{theme}.svg').read_text()
    raw = raw.replace('<g transform="translate(909 49)', '<g class="invite-star" transform="translate(909 49)')
    style = '<style>.invite-star{animation:glow 4s ease-in-out infinite}@keyframes glow{50%{opacity:.3}}@media(prefers-reduced-motion:reduce){.invite-star{animation:none}}</style>'
    raw = raw.replace('</title>', '</title>' + style)
    (ASSETS / f'connect-v7-{theme}.svg').write_text(raw)


if __name__ == '__main__':
    for theme in ['light', 'dark']:
        desktop_header(theme)
        mobile_header(theme)
        headings(theme)
        companions(theme)
