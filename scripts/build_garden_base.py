"""Draw the README's final garden scene in both themes and screen sizes."""
from pathlib import Path

from build_artwork_v4 import MONO, cat, pixel, star, svg, text
from build_artwork_v5 import recolour

ASSETS = Path(__file__).resolve().parents[1] / 'assets'


def scene(theme, mobile=False):
    dark = theme == 'dark'
    width, height = (420, 314) if mobile else (960, 282)
    ink, muted = ('#e1edf5', '#9fb8ca') if dark else ('#19364b', '#597487')
    grass, grass_light = ('#4b967b', '#8bc8a8') if dark else ('#79b79c', '#b5ddc6')
    soil, underside = ('#213c4c', '#142b3e') if dark else ('#d0e4ef', '#b6d1e1')
    outline, wood = ('#62879b', '#294758') if dark else ('#729bb1', '#dfedf4')
    gold = '#f5cf77' if dark else '#d2a043'
    ground = 244 if mobile else 210
    center = width / 2
    sky, water = ('#79c5d4', '#244b60') if dark else ('#91c9dd', '#b2dce4')
    content = f'''<defs><radialGradient id="lantern-glow"><stop stop-color="#f8ce73" stop-opacity=".48"/><stop offset="1" stop-color="#f8ce73" stop-opacity="0"/></radialGradient><radialGradient id="horizon"><stop stop-color="{sky}" stop-opacity=".18"/><stop offset=".6" stop-color="{grass_light}" stop-opacity=".08"/><stop offset="1" stop-color="{sky}" stop-opacity="0"/></radialGradient><linearGradient id="earth" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{soil}"/><stop offset="1" stop-color="{underside}"/></linearGradient></defs>'''
    content += '''<style>
.firefly{animation:drift 7s ease-in-out infinite}.lamp{animation:warmth 5s ease-in-out infinite}.friend{animation:rest 6s ease-in-out infinite}.spark{animation:twinkle 5s ease-in-out infinite}.spark.second{animation-delay:-2s}.spark.third{animation-delay:-4s}
.leaves{transform-box:fill-box;transform-origin:50% 100%;animation:breeze 7s ease-in-out infinite}.water-ring{transform-box:fill-box;transform-origin:center;animation:ripple 5s ease-out infinite}.water-ring.second{animation-delay:-2.5s}.paw{transform-origin:1px 12px;animation:wave 8s ease-in-out infinite}.eyes{animation:blink 7s step-end infinite}.comet{animation:crossing 13s ease-in-out infinite;opacity:0}
@keyframes drift{50%{transform:translate(9px,-5px)}}@keyframes warmth{50%{opacity:.6}}@keyframes rest{50%{transform:translateY(-2px)}}@keyframes twinkle{50%{opacity:.35}}@keyframes breeze{50%{transform:rotate(2deg)}}@keyframes ripple{0%{transform:scale(.6);opacity:.7}100%{transform:scale(1.4);opacity:0}}@keyframes wave{0%,65%,100%{transform:rotate(0)}70%,80%{transform:rotate(-16deg)}75%,85%{transform:rotate(5deg)}}@keyframes blink{0%,93%,98%,100%{opacity:1}94%,97%{opacity:0}}@keyframes crossing{0%,8%,27%,100%{opacity:0;transform:translate(0,0)}12%{opacity:.8;transform:translate(15px,-3px)}24%{opacity:0;transform:translate(120px,-19px)}}
@media(prefers-reduced-motion:reduce){.firefly,.lamp,.friend,.spark,.leaves,.water-ring,.paw,.eyes,.comet{animation:none}.comet{display:none}.water-ring.second{display:none}}
</style>
'''
    content += text(center, 44, 'Thanks for stopping by.', 27 if mobile else 32, ink, 750,
                    'text-anchor="middle" letter-spacing="-.7"')
    content += text(center, 76, 'Hope something here made you smile. :)', 14 if mobile else 16,
                    muted, extra='text-anchor="middle"')
    # A fading horizon keeps the upper scene transparent against either theme.
    content += f'<ellipse cx="{center}" cy="{ground-40}" rx="{width*.46}" ry="90" fill="url(#horizon)"/>'
    if not mobile:
        content += f'<path d="M58 181Q230 121 417 164T903 158" stroke="{sky}" stroke-opacity=".24" stroke-width="1.2"/><path d="M79 189Q273 139 456 173T884 171" stroke="{grass_light}" stroke-opacity=".3" stroke-width="1.2"/>'
    for i, (x, y, scale) in enumerate([(37, 119, 2), (width-55, 106, 2), (center-70, 127, 1.4)]):
        content += f'<g class="spark {("first","second","third")[i]}">' + star(x, y, scale, gold) + '</g>'
    comet_x = 85 if mobile else 243
    content += f'<g class="comet"><path d="M{comet_x-26} 119L{comet_x} 115" stroke="{sky}" stroke-width="1.5" stroke-linecap="round"/>{star(comet_x-3,112,1.2,gold)}</g>'
    # A stepped grass edge and two blue earth layers form a clear visual base.
    for x in range(12, width-12, 12):
        rise = [0, 3, 0, 0, 6, 0, 3, 0][(x//12) % 8]
        content += f'<rect x="{x}" y="{ground-rise}" width="12" height="{10+rise}" fill="{grass}"/>'
    content += f'<path d="M12 {ground+10}H{width-12}V{height-17}H{width-24}V{height-9}H24V{height-17}H12Z" fill="url(#earth)"/>'
    content += f'<path d="M24 {height-21}H{width-24}V{height-9}H24Z" fill="{underside}"/>'
    content += f'<path d="M36 {height-8}H{width-36}" stroke="{outline}" stroke-opacity=".5" stroke-width="2"/>'
    # Tiny plants grow out of the platform rather than floating above it.
    plant = ['...g...', '...gg..', '..ggg..', '...g...', '.ggg...', '..gg...', '...g...', '...ggg.', '...gg..', '...g...']
    for x, scale in ([(33, 3), (352, 4)] if mobile else [(74, 4), (139, 6), (822, 4), (882, 5)]):
        content += '<g class="leaves">' + pixel(plant, {'g': grass}, x, ground-10*scale, scale) + '</g>'
        content += pixel(['.g..', 'ggg.', '.ggg', '..g.'], {'g': grass_light}, x+8, ground-12, 3)
    # Blue and mint trees, little wildflowers and water make the finish feel lived in.
    tree = ['....gg....', '...gggg...', '..gglggg..', '.gggglggg.', '..gggggg..', '...gggg...', '....dd....', '....dd....']
    for x, scale in ([(25, 5), (362, 4)] if mobile else [(91, 7), (825, 8)]):
        content += '<g class="leaves">' + pixel(tree, {'g': grass, 'l': grass_light, 'd': outline}, x, ground-8*scale, scale) + '</g>'
    bloom = ['..b..', '.byb.', '..b..', '..g..', '.gg..', '..g..']
    for x, colour in ([(86, sky), (377, gold)] if mobile else [(190, sky), (767, gold), (808, sky)]):
        content += pixel(bloom, {'b': colour, 'y': '#f4d88c', 'g': grass}, x, ground-18, 3)
    pond_x = 60 if mobile else 264
    content += f'<ellipse cx="{pond_x}" cy="{ground+7}" rx="{27 if mobile else 43}" ry="7" fill="{water}"/>'
    for cls in ['first', 'second']:
        content += f'<ellipse class="water-ring {cls}" cx="{pond_x}" cy="{ground+7}" rx="{15 if mobile else 25}" ry="3" stroke="{sky}" stroke-width=".8" opacity=".5"/>'
    for i, x in enumerate([198, 224] if mobile else [485, 514, 545]):
        content += f'<rect x="{x}" y="{ground+6+i%2*3}" width="18" height="5" rx="2" fill="{wood}" stroke="{outline}" stroke-opacity=".3" stroke-width=".8"/>'
    cat_x = 111 if mobile else 399
    cat_y = ground-49.5
    content += '<g class="friend">'
    content += pixel(['b....','bf...','bf...','bffb.','.bbb.'], {'b':'#446b85','f':'#bbdcef'}, cat_x-10, ground-20, 3)
    content += recolour(cat(cat_x, cat_y, 4.5).replace('#34304b','#e3cff4'), theme)
    content += f'<g class="eyes" fill="#24465c"><rect x="{cat_x+9}" y="{cat_y+18}" width="4.5" height="4.5"/><rect x="{cat_x+27}" y="{cat_y+18}" width="4.5" height="4.5"/></g>'
    content += f'<path d="M{cat_x+9} {cat_y+35}H{cat_x+35}" stroke="{gold}" stroke-width="3"/>'
    content += f'<g transform="translate({cat_x+43} {ground-26})"><g class="paw"><rect x="-1" y="1" width="8" height="13" rx="1" fill="#446b85"/><rect x="1" y="1" width="4" height="8" fill="#bbdcef"/></g></g></g>'
    # The lantern brings a warm focal point beside the resting mascot.
    lamp_x = 87 if mobile else 360
    content += f'<g class="lamp"><circle cx="{lamp_x}" cy="{ground-23}" r="38" fill="url(#lantern-glow)"/></g>'
    content += pixel(['..ddd..', '.ddddd.', '.dyyyd.', '.dywyd.', '.dyyyd.', '.ddddd.', '..ddd..', '...d...'],
                     {'d': outline, 'y': gold, 'w': '#fff2bd'}, lamp_x-10.5, ground-25, 3)
    content += '<g class="firefly">' + star(cat_x+68, ground-68, 2, gold) + '</g>'
    # A miniature sign makes the finish intentional, like the edge of a game world.
    sx, sy, sw = (181, ground-63, 170) if mobile else (568, ground-66, 218)
    content += f'<rect x="{sx+sw/2-3}" y="{sy+29}" width="6" height="{ground-sy-27}" fill="{outline}"/>'
    content += f'<path d="M{sx+6} {sy}H{sx+sw-6}V{sy+4}H{sx+sw}V{sy+33}H{sx+sw-6}V{sy+37}H{sx+6}V{sy+33}H{sx}V{sy+4}H{sx+6}Z" fill="{wood}" stroke="{outline}" stroke-width="1.5"/>'
    content += text(sx+sw/2, sy+23, 'see you in the next build.', 11 if mobile else 14,
                    ink, 550, 'text-anchor="middle"')
    # Embedded little stones and a quiet final line close the entire composition.
    for x, y, size in [(46, ground+27, 4), (width-55, ground+34, 5), (width-93, ground+21, 3)]:
        content += f'<rect x="{x}" y="{y}" width="{size}" height="3" fill="{outline}" opacity=".55"/>'
    content += text(center, height-31, '// ideas keep growing', 12, muted, 500,
                    f'text-anchor="middle" font-family="{MONO}"')
    return svg(width, height, 'Thanks for stopping by. Hope something here made you smile. A waving blue pixel cat, warm lantern, trees, flowers and a gently rippling pond close the garden, beside a sign reading: see you in the next build.', content)


if __name__ == '__main__':
    for theme in ['light', 'dark']:
        for mobile in [False, True]:
            suffix = '-mobile' if mobile else ''
            (ASSETS / f'garden-base{suffix}-{theme}.svg').write_text(scene(theme, mobile))
