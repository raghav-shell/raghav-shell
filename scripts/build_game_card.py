"""Build the README's local, theme-aware invitation to Garden Pairs."""
from pathlib import Path
import build_artwork_v4 as art
from build_artwork_v5 import recolour

ASSETS = Path(__file__).resolve().parents[1] / 'assets'


def card(theme, mobile=False):
    width, height = (420, 220) if mobile else (960, 174)
    ink, muted, bg, line = ('#e1edf5', '#abc3d3', '#142b3e', '#4d728c') if theme == 'dark' else ('#19364b', '#597487', '#e8f4fc', '#8bbbd8')
    s = '<style>.friend{animation:hop 5s ease-in-out infinite}.twinkle{animation:twinkle 4s ease-in-out infinite}@keyframes hop{50%{transform:translateY(-5px)}}@keyframes twinkle{50%{opacity:.35}}@media(prefers-reduced-motion:reduce){.friend,.twinkle{animation:none}}</style>'
    s += f'<rect x="2" y="2" width="{width-4}" height="{height-4}" rx="19" fill="{bg}" stroke="{line}" stroke-width="1.5"/>'
    s += art.text(26, 31, 'A TINY PAUSE, A LITTLE PLAY', 10, muted, 650, 'letter-spacing="1.6"')
    s += art.text(24, 76, 'Garden Pairs.', 37 if mobile else 39, ink, 750, 'letter-spacing="-1.2"')
    if mobile:
        s += art.text(26, 108, 'Find four pairs. Collect a little smile.', 15, muted, 500)
        s += f'<rect x="26" y="140" width="158" height="40" rx="12" fill="{ink}"/>'
        s += art.text(105, 165, 'Let’s play  ↗', 14, bg, 700, 'text-anchor="middle"')
        x, y = 259, 141
    else:
        s += art.text(26, 108, 'Eight cards, four pairs, one small happy break.', 18, muted, 500)
        s += art.text(26, 142, 'Tap or use your keyboard · no timer, no rush', 12, muted, 500)
        s += f'<rect x="708" y="105" width="211" height="40" rx="12" fill="{ink}"/>'
        s += art.text(812, 130, 'Let’s play Garden Pairs  ↗', 14, bg, 700, 'text-anchor="middle"')
        x, y = 691, 37
    s += '<g class="friend">' + recolour(art.cat(x, y, 4), theme) + '</g>'
    s += '<g class="twinkle">' + art.star(x + 73, y + 4, 4, '#e9be66') + art.star(x + 107, y + 27, 2, '#8bbbd8') + '</g>'
    suffix = '-mobile' if mobile else ''
    (ASSETS / f'game-card{suffix}-{theme}.svg').write_text(art.svg(width, height, 'Garden Pairs. A tiny matching game. Eight cards, four pairs. Play with taps or a keyboard.', s))


if __name__ == '__main__':
    for theme in ['light', 'dark']:
        card(theme)
        card(theme, mobile=True)
