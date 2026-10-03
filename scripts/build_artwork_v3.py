"""Build the pastel stationery artwork accompanying the illustrated v3 banner."""

from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"
PROJECTS = [
    ("aegis", "AEGIS", "local AI, kept close to home", "#f2edf8", "#75608d", "team project · interface + integration", "Next.js / FastAPI / Ollama", "shield"),
    ("visionx", "VisionX", "making AI evidence easier to review", "#edf5ee", "#4a7864", "team project · branding + frontend", "TypeScript / Next.js / Tailwind", "eye"),
    ("razorflow", "RazorFlow", "a thoughtful path after a failed payment", "#fcf0e7", "#a36a4e", "test-mode project · policies + workers", "FastAPI / PostgreSQL / Celery", "path"),
    ("competeiq", "CompeteIQ", "from research signals to useful reports", "#edf3fa", "#5d7b96", "agent workflow · bounded reflection", "LangGraph / Tavily / Supabase", "stars"),
    ("lexguard", "Lexguard", "a clearer view of contract clauses", "#faeef2", "#a16d85", "AI prototype · provider fallback", "Next.js / FastAPI / Gemini", "paper"),
    ("shell", "Os_Shell", "a little closer to how computers work", "#f5f5e5", "#7f854e", "CodeCrafters · parsing + pipelines", "Java / ProcessBuilder / Maven", "terminal"),
]


def text(x, y, value, size=22, color="#59584f", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def svg(w, h, title, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><g font-family="{FONT}">{body}</g></svg>\n'


def doodle(kind, color):
    common = f'stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "shield":
        return f'<path d="M0 -34Q15 -30 29 -23V0Q26 23 0 36Q-27 23 -29 0V-23Q-15 -30 0 -34Z" {common}/><path d="M-13 1L-3 11L17 -12" {common}/>'
    if kind == "eye":
        return f'<path d="M-41 0Q0 -38 41 0Q0 38 -41 0Z" {common}/><circle r="14" {common}/><circle cx="3" cy="-3" r="5" fill="{color}"/><path d="M-33 -27L-39 -36M0 -34V-45M33 -27L39 -36" {common}/>'
    if kind == "path":
        return f'<path d="M-34 22Q-45 -22 -9 -22Q28 -22 7 4Q-10 30 32 28" {common}/><path d="M24 17L36 28L24 39" {common}/><circle cx="-34" cy="22" r="6" fill="{color}"/>'
    if kind == "stars":
        return f'<path d="M0 -36L8 -9L34 0L8 9L0 35L-8 9L-34 0L-8 -9Z" {common}/><path d="M39 -35V-19M31 -27H47M-39 25V41M-47 33H-31" {common}/>'
    if kind == "paper":
        return f'<path d="M-25 -34H12L28 -18V35H-25Z" {common}/><path d="M12 -34V-18H28M-13 -6H14M-13 5H8M-13 16H12" {common}/>'
    return f'<rect x="-37" y="-28" width="74" height="58" rx="9" {common}/><path d="M-24 -3L-15 5L-24 13M0 14H15" {common}/><circle cx="-24" cy="-16" r="2" fill="{color}"/><circle cx="-15" cy="-16" r="2" fill="{color}"/>'


def cards():
    for slug, name, tagline, bg, ink, role, stack, kind in PROJECTS:
        body = f'<rect x="1" y="8" width="598" height="251" rx="20" fill="{bg}" stroke="{ink}" stroke-opacity=".18"/><path d="M241 1H355L358 20Q300 25 239 21Z" fill="#eee3cb" fill-opacity=".7"/>'
        body += f'<g transform="translate(522 75) rotate(8)">{doodle(kind,ink)}</g>'
        body += text(29, 53, role, 14, ink, 500)
        body += text(27, 111, name, 47, ink, 500, f'font-family="{SERIF}" letter-spacing="-1"')
        body += text(29, 153, tagline, 22)
        body += f'<path d="M30 181Q300 178 568 181" stroke="{ink}" stroke-opacity=".2"/>'
        body += text(29, 218, stack, 16, ink, 500)
        body += text(549, 219, "↗", 25, ink)
        (ASSETS / f"project-{slug}-v3.svg").write_text(svg(600, 270, f"{name}. {tagline}. {role}. {stack}", body))


def garden():
    s = '<style>.star{animation:twinkle 4s ease-in-out infinite}.bud{transform-origin:480px 28px;animation:sway 5s ease-in-out infinite}@keyframes twinkle{50%{opacity:.4}}@keyframes sway{50%{transform:rotate(5deg)}}@media(prefers-reduced-motion:reduce){.star,.bud{animation:none}}</style>'
    s += '<path d="M24 27Q212 24 430 27M530 27Q746 24 936 27" stroke="#dbd2c1" stroke-dasharray="2 8" stroke-linecap="round"/>'
    s += '<g class="bud" stroke="#739077" stroke-width="1.8" stroke-linecap="round"><path d="M480 39V19"/><path d="M480 27Q462 29 463 16Q476 15 480 27Z" fill="#d8e5cb"/><path d="M480 23Q494 26 498 12Q484 10 480 23Z" fill="#e4ebd7"/></g>'
    s += '<g class="star" stroke="#c5a15e" stroke-width="1.5"><path d="M448 17V27M443 22H453M515 27V35M511 31H519"/></g>'
    (ASSETS / 'garden-v3.svg').write_text(svg(960, 52, "A small sprout and gently twinkling stars", s))


def footer():
    body = '<rect x="1" y="1" width="958" height="158" rx="18" fill="#f2f5eb" stroke="#cdd7c6"/>'
    body += text(32, 40, "GOOD PROJECTS OFTEN START WITH A HELLO.", 12, "#657c61", 500, 'letter-spacing="1.3"')
    body += text(31, 91, "Let’s make something lovely — and useful.", 33, "#4d6750", 400, f'font-family="{SERIF}"')
    body += text(33, 126, "Hackathons, thoughtful software, and people who care about what they build.", 16, "#687060")
    body += '<g transform="translate(870 77)" stroke="#8b9e78" stroke-width="2"><path d="M0 24V-20M0 3Q-28 4 -26 -17Q-4 -19 0 3ZM0 -7Q22 -1 25 -24Q2 -26 0 -7Z" fill="#d7e3c5"/></g>'
    (ASSETS / 'connect-v3.svg').write_text(svg(960,160,"Let's make something lovely and useful. Connect with Raghav on LinkedIn.",body))


if __name__ == '__main__':
    cards()
    garden()
    footer()
