"""Build the profile's original pixel-garden SVG design system."""

from html import escape
from pathlib import Path
from build_artwork_v3 import doodle

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
INK = '#34304b'
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"


def text(x, y, value, size=20, color=INK, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def svg(width, height, title, content):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><g font-family="{FONT}">{content}</g></svg>\n'


def pixel(rows, colors, x=0, y=0, scale=5):
    cells = ''.join(f'<rect x="{col}" y="{row}" width="1" height="1" fill="{colors[char]}"/>' for row, line in enumerate(rows) for col, char in enumerate(line) if char in colors)
    return f'<g transform="translate({x} {y}) scale({scale})" shape-rendering="crispEdges">{cells}</g>'


def star(x, y, scale=3, color='#e0a526'):
    return pixel(['..x..', '..x..', 'xxxxx', '..x..', '..x..'], {'x': color}, x, y, scale)


def flower(x, y, scale=4, petal='#e3b1f1'):
    return pixel(['..pp..', '.pppp.', 'ppyypp', 'ppyypp', '.pppp.', '..gg..', '.ggg..', '..ggg.', '..g...'], {'p': petal, 'y': '#ffd873', 'g': '#659d71'}, x, y, scale)


def cat(x, y, scale=4):
    rows = ['.dd.....dd.', '.dld...dld.', '.dllllllld.', '.dllldlldd.', '.dlklllkld.', '.dllllllld.', '..dllplld..', '..ddddddd..', '.dlllldlld.', '.dlllldlld.', '..dd...dd..']
    return pixel(rows, {'d': '#5a4770', 'l': '#e3cff4', 'p': '#ed99b2', 'k': '#34304b'}, x, y, scale)


def header():
    s = '''<defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#e4ddf1" stroke-width=".7"/></pattern></defs>
<style>.sun{animation:float 6s ease-in-out infinite}.eyes{animation:blink 7s step-end infinite}.spark{animation:spark 4s ease-in-out infinite}@keyframes float{50%{transform:translateY(-6px)}}@keyframes blink{0%,94%,98%,100%{opacity:1}95%,97%{opacity:0}}@keyframes spark{50%{opacity:.35}}@media(prefers-reduced-motion:reduce){.sun,.eyes,.spark{animation:none}}</style>
<rect x="8" y="9" width="946" height="378" rx="22" fill="#d9ccef"/>
<rect x="2" y="2" width="950" height="378" rx="20" fill="#f6f2fd" stroke="#514567" stroke-width="2"/>
<path d="M3 48H951" stroke="#514567" stroke-width="1.5"/>
<circle cx="25" cy="25" r="5" fill="#edaabd"/><circle cx="43" cy="25" r="5" fill="#f6cf69"/><circle cx="61" cy="25" r="5" fill="#a1d7b0"/>
<rect x="550" y="49" width="400" height="272" fill="url(#grid)"/>
'''
    s += text(85, 29, "raghav's little internet garden", 12, '#6f6381', 500, f'font-family="{MONO}"')
    s += text(921, 29, 'hello, world :)', 12, '#6f6381', 500, f'text-anchor="end" font-family="{MONO}"')
    s += text(37, 103, 'A CURIOUS MIND & A CREATIVE HEART', 12, '#766486', 650, 'letter-spacing="1.8"')
    s += text(33, 170, "hi, i'm", 55, INK, 750, 'letter-spacing="-2"')
    s += text(29, 247, 'Raghav.', 82, INK, 800, 'letter-spacing="-4"')
    s += text(36, 286, 'Thoughtful code. A little imagination.', 21, '#6b6079', 400)
    s += '<rect x="38" y="310" width="121" height="27" rx="13" fill="#ddd0f5"/><rect x="167" y="310" width="100" height="27" rx="13" fill="#c9e9d1"/><rect x="275" y="310" width="112" height="27" rx="13" fill="#ffe6a1"/>'
    for x, label in [(98, 'full-stack'), (217, 'AI workflows'), (331, 'hackathons')]:
        s += text(x, 328, label, 11, INK, 600, 'text-anchor="middle"')
    s += '<g class="sun">' + pixel(['..yyyy..', '.yyyyyy.', 'yyykykyy', 'yyyyyyyy', 'yykyykyy', '.yykkyy.', '..yyyy..'], {'y': '#f8cf65', 'k': '#8d6c31'}, 842, 76, 6) + '</g>'
    s += '<path d="M585 113H619V103H651V113H666V128H585Z" fill="#e4dcf1"/>'
    s += '<rect x="639" y="142" width="210" height="140" rx="13" fill="#b8a0d9" stroke="#514567" stroke-width="3"/><rect x="652" y="155" width="184" height="107" rx="5" fill="#d8efda" stroke="#514567" stroke-width="2"/>'
    s += '<g class="eyes"><rect x="704" y="193" width="10" height="17" rx="4" fill="#514567"/><rect x="774" y="193" width="10" height="17" rx="4" fill="#514567"/></g><ellipse cx="695" cy="217" rx="11" ry="5" fill="#efaabd"/><ellipse cx="793" cy="217" rx="11" ry="5" fill="#efaabd"/><path d="M730 214Q744 230 758 214" fill="none" stroke="#514567" stroke-width="3" stroke-linecap="round"/>'
    s += '<path d="M639 282L618 305H869L849 282Z" fill="#d6c7eb" stroke="#514567" stroke-width="3" stroke-linejoin="round"/><path d="M727 286H761L770 296H717Z" fill="#b8a0d9"/>'
    s += '<path d="M578 318H903" stroke="#8fbe97" stroke-width="3" stroke-dasharray="4 3"/>'
    s += flower(586, 276, 4, '#f3aec5') + flower(878, 270, 5, '#d5b0f2') + cat(570, 223, 4)
    s += '<g class="spark">' + star(866, 169, 3, '#9573b9') + star(610, 158, 2, '#d2a03c') + star(807, 108, 2, '#9977be') + '</g>'
    s += text(742, 351, 'small ideas grow here.', 13, '#6f6381', 500, f'font-family="{MONO}" text-anchor="middle"')
    (ASSETS / 'profile-header-v4.svg').write_text(svg(960, 390, "Hi, I'm Raghav. Thoughtful code, a little imagination. A smiling pixel computer, cat, flowers, and sunshine.", s))


PROJECTS = [
    ('aegis', 'AEGIS', 'Local AI. Human oversight.', 'An industrial AI workbench, kept on premise.', '#ece0fa', '#d3b7f0', '01 / TEAM PROJECT', 'interface · integration · PDF workflows', 'Next.js / FastAPI / Ollama', 'shield'),
    ('visionx', 'VisionX', 'Make AI evidence easier to review.', 'An offline computer-vision assurance workspace.', '#e0f3e5', '#afdcb9', '02 / TEAM PROJECT', 'branding · frontend · API integration', 'Next.js / TypeScript / Tailwind', 'eye'),
    ('razorflow', 'RazorFlow', 'A second chance for a payment.', 'Recovery decisions with explicit policy checks.', '#fff0d3', '#f2d284', '03 / TEST-MODE PROJECT', 'policies · workers · audit trails', 'FastAPI / PostgreSQL / Celery', 'path'),
    ('competeiq', 'CompeteIQ', 'Research that becomes a report.', 'An agent workflow with bounded reflection.', '#e2edfb', '#b7d1ee', '04 / AI WORKFLOW', 'research · snapshots · integrations', 'LangGraph / Tavily / Supabase', 'stars'),
    ('lexguard', 'Lexguard', 'A clearer look at contract clauses.', 'Document extraction and AI risk summaries.', '#fbe3eb', '#efb4c8', '05 / AI PROTOTYPE', 'provider fallback · demo data on failure', 'Next.js / FastAPI / Gemini', 'paper'),
    ('shell', 'Os_Shell', 'Under the hood of a terminal.', 'A Java shell from the CodeCrafters challenge.', '#eef0d6', '#d2d99e', '06 / SYSTEMS EXPLORATION', 'parsing · pipelines · background jobs', 'Java / ProcessBuilder / Maven', 'terminal'),
]


def cards():
    for slug, name, line, second, bg, accent, label, role, stack, icon in PROJECTS:
        s = f'<rect x="8" y="8" width="580" height="284" rx="18" fill="{accent}"/><rect x="2" y="2" width="580" height="284" rx="16" fill="{bg}" stroke="{INK}" stroke-width="1.7"/>'
        s += text(28, 36, label, 12, '#70657d', 600, f'font-family="{MONO}" letter-spacing=".5"')
        s += f'<rect x="487" y="19" width="73" height="73" rx="18" fill="{accent}"/><g transform="translate(523 56) scale(.62)">{doodle(icon, INK)}</g>'
        s += text(26, 96, name, 43, INK, 750, 'letter-spacing="-1.5"')
        s += text(28, 137, line, 21, INK, 650)
        s += text(28, 169, second, 17, '#6c6177')
        s += text(28, 207, role, 14, '#6c6177', 500)
        s += f'<path d="M28 225H554" stroke="{INK}" stroke-opacity=".16"/>'
        s += text(28, 258, stack, 15, INK, 500, f'font-family="{MONO}"')
        s += text(545, 258, '↗', 25, INK, 600)
        (ASSETS / f'project-{slug}-v4.svg').write_text(svg(600, 300, f'{name}. {line} {second} {role}. {stack}', s))


def divider():
    s = '<style>.friend{animation:hop 5s ease-in-out infinite}.star{animation:twinkle 4s ease-in-out infinite}@keyframes hop{0%,40%,60%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}@keyframes twinkle{50%{opacity:.35}}@media(prefers-reduced-motion:reduce){.friend,.star{animation:none}}</style>'
    s += '<path d="M32 37H393M567 37H928" stroke="#bda9d4" stroke-opacity=".65" stroke-dasharray="4 7"/>'
    s += '<g class="friend">' + cat(462, 8, 3) + '</g>'
    s += flower(415, 17, 3, '#d6b1ed') + flower(516, 17, 3, '#efaac2')
    s += '<g class="star">' + star(391, 17, 2, '#d1a14c') + star(551, 13, 2, '#a788bd') + '</g>'
    (ASSETS / 'garden-v4.svg').write_text(svg(960, 60, 'A tiny pixel cat in a flower garden, with gentle motion.', s))


def footer():
    s = '<rect x="5" y="6" width="948" height="161" rx="18" fill="#c4dfcb"/><rect x="1" y="1" width="948" height="161" rx="17" fill="#e6f3e9" stroke="#547460" stroke-width="1.6"/>'
    s += text(30, 38, 'GOOD IDEAS GROW BETTER TOGETHER.', 11, '#587161', 600, f'font-family="{MONO}" letter-spacing="1.3"')
    s += text(28, 87, 'Have something fun to build?', 35, INK, 750, 'letter-spacing="-1"')
    s += text(30, 122, 'Say hello. Let’s make something useful — and a little delightful.', 17, '#587161')
    s += flower(857, 77, 7, '#d3b0eb') + flower(817, 97, 5, '#f0acc1')
    s += star(909, 49, 3, '#a58aba')
    (ASSETS / 'connect-v4.svg').write_text(svg(960, 170, 'Have something fun to build? Say hello on LinkedIn for hackathons and software collaboration.', s))


if __name__ == '__main__':
    header()
    cards()
    divider()
    footer()
