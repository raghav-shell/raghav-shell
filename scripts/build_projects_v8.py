"""Build the v8 project cards: a small pixel scene of what each project does,
standing on the same garden ground as the hero, with the details below."""

from build_artwork_v4 import pixel, text, svg, MONO
from build_artwork_v8 import ASSETS, THEMES, cat, sprout, flower, hills, cloud

W, H, SCENE = 400, 336, 148  # card size; the scene's ground line sits at SCENE

# slug, name, kind, line, description, part label, part, stack, sky tints (light, dark)
PROJECTS = [
    ('aegis', 'AEGIS', 'team project', 'Local AI. Human oversight.', 'An industrial AI workbench, kept on premise.',
     'My part', 'interface, integration, PDF extraction', ['Next.js', 'FastAPI', 'Ollama'],
     ('#cfe4f5', '#e9f3fb'), ('#14304a', '#1c3d5a')),
    ('visionx', 'VisionX', 'team project', 'Make AI evidence easier to review.', 'An offline computer-vision assurance workspace.',
     'My part', 'branding, frontend, API integration', ['Next.js', 'TypeScript', 'Tailwind'],
     ('#cdeedd', '#eaf7f0'), ('#123128', '#1c4436')),
    ('razorflow', 'RazorFlow', 'test-mode project', 'A second chance for a payment.', 'Recovery decisions with explicit policy checks.',
     'Inside', 'policies, workers, audit trails', ['FastAPI', 'PostgreSQL', 'Celery'],
     ('#fbe3b0', '#fdf4df'), ('#33280f', '#46391a')),
    ('competeiq', 'CompeteIQ', 'AI workflow', 'Research that becomes a report.', 'An agent workflow with bounded reflection.',
     'Inside', 'research, snapshots, integrations', ['LangGraph', 'Tavily', 'Supabase'],
     ('#c8e8ea', '#e8f5f6'), ('#11303a', '#1a434d')),
    ('lexguard', 'Lexguard', 'AI prototype', 'A clearer look at contract clauses.', 'Document extraction and AI risk summaries.',
     'Inside', 'provider fallback, demo data on failure', ['Next.js', 'FastAPI', 'Gemini'],
     ('#dbe3f3', '#eff3fa'), ('#1b2740', '#263656')),
    ('shell', 'Os_Shell', 'systems exploration', 'Under the hood of a terminal.', 'A Java shell from the CodeCrafters challenge.',
     'Inside', 'parsing, pipelines, background jobs', ['Java', 'ProcessBuilder', 'Maven'],
     ('#e1ecc4', '#f3f7e6'), ('#232f15', '#33421f')),
]

INK_ON_SCENE = {'light': '#19364b', 'dark': '#e1edf5'}


def box(x, y, w, h, fill, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" shape-rendering="crispEdges" {extra}/>'


def outline(x, y, w, h, fill, line, r=4, sw=3):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{line}" stroke-width="{sw}"/>'


def check(cx, cy, color):
    return f'<path d="M{cx - 6} {cy}L{cx - 2} {cy + 5}L{cx + 6} {cy - 5}" fill="none" stroke="{color}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'


def cross(cx, cy, color):
    return f'<path d="M{cx - 5} {cy - 5}L{cx + 5} {cy + 5}M{cx + 5} {cy - 5}L{cx - 5} {cy + 5}" stroke="{color}" stroke-width="3.5" stroke-linecap="round"/>'


# Each vignette draws in card coordinates; the ground line is y=SCENE.
def aegis(p, t):
    line = p['frame']
    s = outline(132, 52, 64, 96, p['laptop_base'], line, 6)
    for i in range(3):
        s += outline(142, 64 + i * 26, 44, 16, p['screen'], line, 3, 2)
        s += box(148, 70 + i * 26, 5, 5, p['term_ok']) + box(157, 70 + i * 26, 5, 5, p['term_dim'])
    s += (f'<path d="M222 58L256 71V98Q256 126 222 142Q188 126 188 98V71Z" fill="{p["blue"] if t == "light" else "#5d9ccb"}" '
          f'stroke="{line}" stroke-width="3" stroke-linejoin="round"/>')
    s += '<path d="M207 99L218 110L238 87" fill="none" stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    s += cat(p, 268, 104)
    s += sprout(p, 92, 124, 4)
    return s


def visionx(p, t):
    line = p['frame']
    # A photo on an easel, a camera, and the cat inside a detection box.
    s = outline(58, 56, 76, 58, '#ffffff' if t == 'light' else '#2b4a63', line, 4)
    s += f'<path d="M64 108L84 84L98 98L108 88L128 108Z" fill="{p["grass"]}"/>' + box(112, 64, 10, 10, '#f6d277')
    s += f'<path d="M84 114L76 148M108 114L116 148" stroke="{p["crate_dark"]}" stroke-width="4"/>'
    s += outline(150, 98, 40, 28, p['laptop'], line, 5) + f'<circle cx="170" cy="112" r="8" fill="{p["screen"]}" stroke="{line}" stroke-width="2"/>'
    s += f'<circle cx="170" cy="112" r="3" fill="{p["term_ok"]}"/>' + box(156, 92, 10, 6, line)
    s += f'<path d="M194 108L246 104M194 116L246 130" stroke="{p["term_ok"]}" stroke-width="2" stroke-dasharray="4 4"/>'
    s += cat(p, 268, 104)
    s += f'<rect x="258" y="94" width="64" height="58" rx="2" fill="none" stroke="#e05f8a" stroke-width="2.5" stroke-dasharray="6 4"/>'
    s += f'<rect x="258" y="76" width="64" height="18" fill="#e05f8a"/>'
    s += text(290, 89, 'cat 0.98', 11, '#ffffff', 700, f'text-anchor="middle" font-family="{MONO}"')
    return s


def razorflow(p, t):
    line = p['frame']
    s = outline(52, 86, 84, 54, p['laptop'], line, 7)
    s += box(52, 98, 84, 10, line) + box(64, 116, 16, 12, '#f6d277') + box(88, 120, 34, 4, p['laptop_base'])
    s += f'<circle cx="122" cy="80" r="14" fill="#e05f5f" stroke="{line}" stroke-width="2"/>' + cross(122, 80, '#ffffff')
    s += f'<path d="M148 92Q210 24 272 86" stroke="{p["mint"]}" stroke-width="4" fill="none" stroke-dasharray="8 6"/>'
    s += f'<path d="M262 74L274 90L284 72" stroke="{p["mint"]}" stroke-width="4" fill="none" stroke-linejoin="round"/>'
    s += text(210, 50, 'retry', 12, INK_ON_SCENE[t], 700, f'text-anchor="middle" font-family="{MONO}"')
    coin = ['..xxxx..', '.xyyyyx.', 'xyyxxyyx', 'xyxyyyyx', 'xyyxxyyx', 'xyyyyxyx', '.xyxxyx.', '..xxxx..']
    s += pixel(coin, {'x': '#a87a1f', 'y': '#f6d277'}, 262, 100, 5)
    s += f'<circle cx="320" cy="92" r="14" fill="{p["grass"]}" stroke="{line}" stroke-width="2"/>' + check(320, 92, '#ffffff')
    return s


def competeiq(p, t):
    line = p['frame']
    paper = '#ffffff' if t == 'light' else '#2b4a63'
    s = ''
    for i, (x, y) in enumerate([(52, 70), (64, 62), (76, 54)]):
        s += outline(x, y, 56, 72, paper, line, 3, 2)
        for j in range(4):
            s += box(x + 8, y + 12 + j * 11, 40 - (j % 2) * 12, 4, p['term_dim'])
    s += f'<circle cx="126" cy="96" r="20" fill="{p["cloud"]}" fill-opacity=".55" stroke="{line}" stroke-width="5"/>'
    s += f'<path d="M140 110L158 128" stroke="{line}" stroke-width="8" stroke-linecap="round"/>'
    s += f'<path d="M176 100H226M216 90L228 100L216 110" stroke="{p["mint"]}" stroke-width="4" fill="none" stroke-linejoin="round"/>'
    s += outline(244, 50, 92, 92, paper, line, 4, 3)
    for i, (h, c) in enumerate([(26, p['laptop']), (44, p['mint']), (34, p['laptop']), (60, p['grass'])]):
        s += box(256 + i * 19, 130 - h, 12, h, c)
    s += box(254, 130, 74, 3, line)
    return s


def lexguard(p, t):
    line = p['frame']
    paper = '#ffffff' if t == 'light' else '#2b4a63'
    s = f'<path d="M140 40H220L244 64V148H140Z" fill="{paper}" stroke="{line}" stroke-width="3" stroke-linejoin="round"/>'
    s += f'<path d="M220 40V64H244" fill="none" stroke="{line}" stroke-width="3" stroke-linejoin="round"/>'
    for j, w in enumerate([64, 80, 72, 84, 56, 76, 60]):
        y = 64 + j * 11
        if j == 3:
            s += box(148, y - 4, 90, 11, '#f6d277', 'fill-opacity=".85"')
        s += box(152, y, w, 4, p['term_dim'] if j != 3 else '#806535')
    s += f'<path d="M258 140V76" stroke="{line}" stroke-width="4"/>'
    s += pixel(['xxxxxx', 'xxxxxxx', 'xxxxxx', 'xxxxx'], {'x': '#e05f5f'}, 260, 76, 5)
    s += f'<path d="M244 101H256" stroke="#e05f5f" stroke-width="3" stroke-dasharray="3 3"/>'
    s += cat(p, 62, 104)
    s += flower(p, 300, 133, '#f0a8c0') + sprout(p, 320, 124, 4)
    return s


def shell(p, t):
    line = p['frame']
    s = outline(70, 44, 168, 96, p['screen'], line, 8)
    s += box(73, 47, 162, 14, '#ffffff', 'fill-opacity=".07"')
    for i, c in enumerate(['#e98b8b', '#f6d277', '#8fdcb5']):
        s += f'<circle cx="{84 + i * 10}" cy="54" r="3" fill="{c}"/>'
    s += text(84, 84, '$ ls | grep cat', 11, p['term'], 700, f'font-family="{MONO}"')
    s += text(84, 102, 'cat.txt', 11, p['term_ok'], 500, f'font-family="{MONO}"')
    s += text(84, 120, '$ sleep 5 &', 11, p['term'], 700, f'font-family="{MONO}"')
    s += box(170, 112, 7, 10, p['term'])
    shellart = ['....xxxx....', '..xxyyyyxx..', '.xyyxxxxyyx.', 'xyyxyyyyxyyx', 'xyxyyxxyyxyx',
                'xyxyxyyxyxyx', 'xyxyyyyxyxyx', '.xyxxxxyyxx.', '..xyyyyyx...', '...xxxxx....']
    s += pixel(shellart, {'x': '#b77a5a', 'y': '#f3c6a5'}, 262, 98, 5)
    s += sprout(p, 330, 124, 4) + flower(p, 48, 133, '#c7a6ef')
    return s


VIGNETTES = dict(aegis=aegis, visionx=visionx, razorflow=razorflow, competeiq=competeiq, lexguard=lexguard, shell=shell)


def card(project, theme):
    slug, name, kind, line, desc, part_label, part, stack, sky_l, sky_d = project
    p = THEMES[theme]
    sky = sky_l if theme == 'light' else sky_d
    body = '#ffffff' if theme == 'light' else '#0f1c28'
    s = f'<defs><linearGradient id="sky-{slug}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{sky[0]}"/><stop offset="1" stop-color="{sky[1]}"/></linearGradient>'
    s += f'<clipPath id="card-{slug}"><rect x="2" y="2" width="{W - 10}" height="{H - 10}" rx="16"/></clipPath></defs>'
    s += f'<rect x="8" y="8" width="{W - 10}" height="{H - 10}" rx="16" fill="{p["shadow"]}"/>'
    s += f'<g clip-path="url(#card-{slug})"><rect width="{W}" height="{H}" fill="{body}"/>'
    s += f'<rect width="{W}" height="{SCENE + 14}" fill="url(#sky-{slug})"/>'
    s += hills(-6, SCENE, [2, 3, 3, 2, 2, 3, 4, 4, 3, 2, 2, 3, 3, 4, 5, 4, 3, 3, 2, 2, 3, 4, 4, 3, 2, 2], 16, sky[0])
    s += cloud(p, 300, 24, 4) if theme == 'light' else ''
    s += VIGNETTES[slug](p, theme)
    s += f'<rect y="{SCENE}" width="{W}" height="8" fill="{p["grass"]}"/><rect y="{SCENE + 8}" width="{W}" height="6" fill="{p["soil"]}"/>'
    s += ''.join(f'<rect x="{x}" y="{SCENE - 3}" width="6" height="3" fill="{p["grass"]}"/>' for x in range(10, W, 34))
    # The kind of project, as a small tag in the sky.
    tag_w = len(kind) * 6.4 + 22
    s += f'<rect x="16" y="16" width="{tag_w}" height="22" rx="11" fill="{body}" fill-opacity=".85"/>'
    s += text(16 + tag_w / 2, 31, kind, 11, p['ink'], 600, 'text-anchor="middle"')
    # Details.
    s += text(22, SCENE + 54, name, 30, p['ink'], 800, 'letter-spacing="-1"')
    s += text(W - 30, SCENE + 52, '↗', 22, p['muted'], 600, 'text-anchor="middle"')
    s += text(22, SCENE + 78, line, 15, p['ink'], 650)
    s += text(22, SCENE + 99, desc, 13, p['muted'], 450)
    s += text(22, SCENE + 122, f'{part_label}:', 12, p['ink'], 700)
    s += text(22 + len(part_label) * 7 + 10, SCENE + 122, part, 12, p['muted'], 500)
    x = 22
    for item in stack:
        w = len(item) * 6.65 + 18
        s += f'<rect x="{x}" y="{SCENE + 138}" width="{w}" height="24" rx="12" fill="{sky[1] if theme == "light" else sky[0]}"/>'
        s += text(x + w / 2, SCENE + 154, item, 11, p['ink'], 600, f'text-anchor="middle" font-family="{MONO}"')
        x += w + 8
    s += '</g>'
    s += f'<rect x="2" y="2" width="{W - 10}" height="{H - 10}" rx="16" fill="none" stroke="{p["frame"]}" stroke-width="2"/>'
    title = f'{name}, {kind}. {line} {desc} {part_label}: {part}. Built with {", ".join(stack)}.'
    return svg(W, H, title, s)


def build():
    for project in PROJECTS:
        for theme in THEMES:
            (ASSETS / f'project-{project[0]}-v8-{theme}.svg').write_text(card(project, theme))


if __name__ == '__main__':
    build()
