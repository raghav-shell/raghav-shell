"""Larger, legible motion and matching typography for the existing profile."""

from pathlib import Path
import re
import build_artwork_v4 as pixel

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
PALETTES = {
    'light': {'ink': '#19364b', 'muted': '#527187', 'blue': '#477fa3', 'line': '#b6d1e1', 'panel': '#f2f8fc', 'mint': '#c9e9d9', 'green': '#3e8464'},
    'dark': {'ink': '#e1edf5', 'muted': '#a5bdce', 'blue': '#8cc2e8', 'line': '#395a70', 'panel': '#101e2b', 'mint': '#254b3f', 'green': '#90cdb0'},
}


def text(x, y, value, size, colour, weight=400, extra=''):
    return pixel.text(x, y, value, size, colour, weight, extra)


def header(theme):
    raw = (ASSETS / f'profile-header-v5-{theme}.svg').read_text()
    raw = raw.replace('.sun{animation:float 6s ease-in-out infinite}', '.sun{animation:float 4s ease-in-out infinite}')
    raw = raw.replace('transform:translateY(-6px)', 'transform:translateY(-11px)')
    raw = raw.replace('<style>', '<style>.computer{animation:computer 4s ease-in-out infinite}@keyframes computer{50%{transform:translateY(-7px)}}@media(prefers-reduced-motion:reduce){.computer{animation:none}}')
    start = raw.index('<rect x="639" y="142"')
    end = raw.index('<path d="M578 318H903"', start)
    raw = raw[:start] + '<g class="computer">' + raw[start:end] + '</g>' + raw[end:]
    (ASSETS / f'profile-header-v6-{theme}.svg').write_text(raw)


def intro(theme):
    p = PALETTES[theme]
    css = '''<style>.phrase{animation:words 15s ease-in-out infinite}.two{animation-delay:-10s}.three{animation-delay:-5s}.beacon{animation:beacon 2.5s ease-in-out infinite}@keyframes words{0%,26%{opacity:1;transform:translateY(0)}29%,96%{opacity:0;transform:translateY(-8px)}97%{opacity:0;transform:translateY(8px)}100%{opacity:1;transform:translateY(0)}}@keyframes beacon{50%{opacity:.55;transform:scale(1.18)}}.beacon{transform-box:fill-box;transform-origin:center}@media(prefers-reduced-motion:reduce){.phrase,.beacon{animation:none;transform:none}.one{opacity:1}.two,.three{opacity:0}}</style>'''
    s = css + f'<rect x="1" y="1" width="958" height="82" rx="14" fill="{p["panel"]}" stroke="{p["line"]}"/>'
    s += f'<circle class="beacon" cx="30" cy="41" r="7" fill="{p["green"]}"/>'
    s += text(52, 27, 'BUILD. LEARN. REPEAT.', 11, p['muted'], 650, f'font-family="{pixel.MONO}" letter-spacing="1.2"')
    phrases = ['making useful things with a creative touch.', 'connecting interfaces to real workflows.', 'exploring local AI & agent workflows.']
    for index, phrase in enumerate(phrases):
        s += f'<g class="phrase {["one", "two", "three"][index]}" opacity="{1 if index == 0 else 0}">' + text(51, 59, phrase, 26, p['ink'], 650, 'letter-spacing="-.5"') + '</g>'
    (ASSETS / f'intro-v6-{theme}.svg').write_text(pixel.svg(960, 84, 'Build, learn, repeat. Making useful things with a creative touch; connecting interfaces to real workflows; exploring local AI and agent workflows.', s))
    mobile = css + f'<rect x="1" y="1" width="418" height="108" rx="14" fill="{p["panel"]}" stroke="{p["line"]}"/>'
    mobile += f'<circle class="beacon" cx="23" cy="24" r="5" fill="{p["green"]}"/>'
    mobile += text(38, 28, 'BUILD. LEARN. REPEAT.', 10, p['muted'], 650, f'font-family="{pixel.MONO}" letter-spacing="1.1"')
    mobile_phrases = [('making useful things', 'with a creative touch.'), ('connecting interfaces', 'to real workflows.'), ('exploring local AI', '& agent workflows.')]
    for index, lines in enumerate(mobile_phrases):
        mobile += f'<g class="phrase {["one", "two", "three"][index]}" opacity="{1 if index == 0 else 0}">'
        mobile += text(22, 65, lines[0], 23, p['ink'], 650) + text(22, 94, lines[1], 23, p['ink'], 650) + '</g>'
    (ASSETS / f'intro-v6-mobile-{theme}.svg').write_text(pixel.svg(420, 110, 'Build, learn, repeat. Making useful things with a creative touch; connecting interfaces to real workflows; exploring local AI and agent workflows.', mobile))


def garden(theme):
    p = PALETTES[theme]
    s = '''<style>.friend{animation:patrol 5s ease-in-out infinite}.spark{animation:shine 3s ease-in-out infinite}@keyframes patrol{0%,100%{transform:translate(-23px,0)}25%{transform:translate(0,-9px)}50%{transform:translate(23px,0)}75%{transform:translate(0,-9px)}}@keyframes shine{50%{opacity:.35}}@media(prefers-reduced-motion:reduce){.friend,.spark{animation:none}}</style>'''
    s += f'<path d="M28 50H351M609 50H932" stroke="{p["line"]}" stroke-width="1.5" stroke-dasharray="5 8"/>'
    cat = pixel.cat(452, 14, 5).replace('#5a4770','#446b85').replace('#e3cff4','#bbdcef').replace('#ed99b2','#e9be66').replace('#34304b','#19364b')
    s += '<g class="friend">' + cat + '</g>'
    s += '<g class="spark">' + pixel.star(380, 33, 4, '#d4a849') + pixel.star(565, 23, 4, p['blue']) + '</g>'
    s += text(480, 91, 'little steps. real progress.', 12, p['muted'], 500, f'text-anchor="middle" font-family="{pixel.MONO}"')
    (ASSETS / f'garden-v6-{theme}.svg').write_text(pixel.svg(960, 104, 'A larger pixel cat gently hops along the garden path. Little steps, real progress.', s))


SECTIONS = [('about', 'a little about me.'), ('projects', 'things I’ve been building.'), ('progress', 'a little progress lately.'), ('tools', 'tools I reach for.'), ('stack', 'my tech stack.')]


def heading(theme, slug, label, number):
    p = PALETTES[theme]
    s = text(0, 39, label, 34, p['ink'], 750, 'letter-spacing="-.8"')
    s += text(929, 36, f'0{number}', 14, p['muted'], 500, f'font-family="{pixel.MONO}" text-anchor="end"')
    (ASSETS / f'heading-{slug}-v6-{theme}.svg').write_text(pixel.svg(960, 48, label, s))
    mobile = text(0, 33, label, 26, p['ink'], 750, 'letter-spacing="-.6"')
    (ASSETS / f'heading-{slug}-v6-mobile-{theme}.svg').write_text(pixel.svg(420, 42, label, mobile))


NOTES = [('build', 'I build', ['full-stack applications', 'interfaces + API workflows'], '#477fa3'), ('care', 'I care about', ['thoughtful interfaces', 'clear, useful behaviour'], '#3e8464'), ('explore', 'I’m exploring', ['local AI + agents', 'document workflows'], '#a27d30')]


def note(theme, slug, title, lines, accent):
    p = PALETTES[theme]
    s = f'<rect x="1" y="1" width="438" height="151" rx="14" fill="{p["panel"]}" stroke="{p["line"]}"/><rect x="18" y="23" width="5" height="106" rx="2" fill="{accent}"/>'
    s += text(38, 46, title, 26, p['ink'], 750)
    for y, line in zip([85, 117], lines):
        s += text(38, y, line, 23, p['muted'], 450)
    (ASSETS / f'about-{slug}-v6-{theme}.svg').write_text(pixel.svg(440, 154, title + ': ' + '; '.join(lines), s))


if __name__ == '__main__':
    for theme in ['light', 'dark']:
        header(theme)
        intro(theme)
        garden(theme)
        for index, (slug, label) in enumerate(SECTIONS, 1):
            heading(theme, slug, label, index)
        for slug, title, lines, accent in NOTES:
            note(theme, slug, title, lines, accent)
