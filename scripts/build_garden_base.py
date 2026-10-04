"""Draw the README's final garden scene in both themes and screen sizes."""
from pathlib import Path

from build_artwork_v4 import MONO, cat, pixel, star, svg, text
from build_artwork_v5 import recolour

ASSETS = Path(__file__).resolve().parents[1] / 'assets'


def scene(theme, mobile=False):
    dark = theme == 'dark'
    width, height = (420, 282) if mobile else (960, 248)
    ink, muted = ('#e1edf5', '#9fb8ca') if dark else ('#19364b', '#597487')
    grass, grass_light = ('#4b967b', '#8bc8a8') if dark else ('#79b79c', '#b5ddc6')
    soil, underside = ('#213c4c', '#142b3e') if dark else ('#d0e4ef', '#b6d1e1')
    outline, wood = ('#62879b', '#294758') if dark else ('#729bb1', '#dfedf4')
    gold = '#f5cf77' if dark else '#d2a043'
    ground = 202 if mobile else 174
    center = width / 2
    content = '''<defs><radialGradient id="lantern-glow"><stop stop-color="#f8ce73" stop-opacity=".5"/><stop offset="1" stop-color="#f8ce73" stop-opacity="0"/></radialGradient></defs>
<style>.firefly{animation:drift 7s ease-in-out infinite}.lamp{animation:warmth 5s ease-in-out infinite}.friend{animation:rest 6s ease-in-out infinite}.spark{animation:twinkle 5s ease-in-out infinite}@keyframes drift{50%{transform:translate(9px,-5px)}}@keyframes warmth{50%{opacity:.55}}@keyframes rest{50%{transform:translateY(-2px)}}@keyframes twinkle{50%{opacity:.35}}@media(prefers-reduced-motion:reduce){.firefly,.lamp,.friend,.spark{animation:none}}</style>
'''
    content += text(center, 40, 'Thanks for stopping by.', 27 if mobile else 31, ink, 750,
                    'text-anchor="middle" letter-spacing="-.7"')
    content += text(center, 68, 'Hope something here made you smile. :)', 14 if mobile else 16,
                    muted, extra='text-anchor="middle"')
    # Transparent sky lets the scene sit naturally on the GitHub page itself.
    for x, y, scale in [(37, 105, 2), (width-55, 92, 2), (center-87, 94, 1.4)]:
        content += '<g class="spark">' + star(x, y, scale, gold) + '</g>'
    # A stepped grass edge and two blue earth layers form a clear visual base.
    for x in range(12, width-12, 12):
        rise = [0, 3, 0, 0, 6, 0, 3, 0][(x//12) % 8]
        content += f'<rect x="{x}" y="{ground-rise}" width="12" height="{10+rise}" fill="{grass}"/>'
    content += f'<path d="M12 {ground+10}H{width-12}V{height-17}H{width-24}V{height-9}H24V{height-17}H12Z" fill="{soil}"/>'
    content += f'<path d="M24 {height-21}H{width-24}V{height-9}H24Z" fill="{underside}"/>'
    content += f'<path d="M36 {height-8}H{width-36}" stroke="{outline}" stroke-opacity=".5" stroke-width="2"/>'
    # Tiny plants grow out of the platform rather than floating above it.
    plant = ['...g...', '...gg..', '..ggg..', '...g...', '.ggg...', '..gg...', '...g...', '...ggg.', '...gg..', '...g...']
    for x, scale in ([(33, 3), (352, 4)] if mobile else [(74, 4), (139, 6), (822, 4), (882, 5)]):
        content += pixel(plant, {'g': grass}, x, ground-10*scale, scale)
        content += pixel(['.g..', 'ggg.', '.ggg', '..g.'], {'g': grass_light}, x+8, ground-12, 3)
    cat_x = 111 if mobile else 399
    content += '<g class="friend">' + recolour(cat(cat_x, ground-49.5, 4.5), theme) + '</g>'
    # A small lantern connects the closing scene to the firefly contribution card.
    lamp_x = 87 if mobile else 360
    content += f'<g class="lamp"><circle cx="{lamp_x}" cy="{ground-23}" r="27" fill="url(#lantern-glow)"/></g>'
    content += pixel(['..ddd..', '.ddddd.', '.dyyyd.', '.dywyd.', '.dyyyd.', '.ddddd.', '..ddd..', '...d...'],
                     {'d': outline, 'y': gold, 'w': '#fff2bd'}, lamp_x-10.5, ground-25, 3)
    content += '<g class="firefly">' + star(cat_x+68, ground-68, 2, gold) + '</g>'
    # A miniature sign makes the finish intentional, like the edge of a game world.
    sx, sy, sw = (181, ground-61, 163) if mobile else (502, ground-66, 296)
    content += f'<rect x="{sx+sw/2-3}" y="{sy+29}" width="6" height="{ground-sy-27}" fill="{outline}"/>'
    content += f'<path d="M{sx+6} {sy}H{sx+sw-6}V{sy+4}H{sx+sw}V{sy+33}H{sx+sw-6}V{sy+37}H{sx+6}V{sy+33}H{sx}V{sy+4}H{sx+6}Z" fill="{wood}" stroke="{outline}" stroke-width="1.5"/>'
    content += text(sx+sw/2, sy+23, 'see you in the next build.', 11 if mobile else 15,
                    ink, 550, 'text-anchor="middle"')
    # Embedded little stones and a quiet final line close the entire composition.
    for x, y, size in [(46, ground+27, 4), (width-55, ground+34, 5), (width-93, ground+21, 3)]:
        content += f'<rect x="{x}" y="{y}" width="{size}" height="3" fill="{outline}" opacity=".55"/>'
    content += text(center, height-31, '// ideas keep growing', 12, muted, 500,
                    f'text-anchor="middle" font-family="{MONO}"')
    return svg(width, height, 'Thanks for stopping by. Hope something here made you smile. A blue pixel cat and warm lantern rest on a garden platform, beside a sign reading: see you in the next build.', content)


if __name__ == '__main__':
    for theme in ['light', 'dark']:
        for mobile in [False, True]:
            suffix = '-mobile' if mobile else ''
            (ASSETS / f'garden-base{suffix}-{theme}.svg').write_text(scene(theme, mobile))
