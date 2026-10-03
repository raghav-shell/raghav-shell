"""Refine the approved pixel garden with light/dark artwork and local logos."""

from pathlib import Path
import re
import tempfile
import xml.etree.ElementTree as ET
import build_artwork_v4 as garden

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
ET.register_namespace('', 'http://www.w3.org/2000/svg')

# Recolour the same layout atomically, keeping previous design versions intact.
LIGHT = {
    '#34304b': '#19364b', '#514567': '#46697e', '#f6f2fd': '#f2f8fc',
    '#d9ccef': '#c9dce8', '#e4ddf1': '#dce8ef', '#6f6381': '#597487',
    '#766486': '#597487', '#6b6079': '#597487', '#edaabd': '#8bbddd',
    '#ddd0f5': '#cce3f3', '#c9e9d1': '#c9e9d9', '#ffe6a1': '#ffe5a1',
    '#e4dcf1': '#dce8ef', '#b8a0d9': '#8bbbd8', '#d8efda': '#d7efe2',
    '#efaabd': '#edd294', '#d6c7eb': '#c3ddeb', '#8fbe97': '#6eb298',
    '#5a4770': '#446b85', '#e3cff4': '#bbdcef', '#ed99b2': '#e9be66',
    '#9573b9': '#6399b8', '#9977be': '#6399b8', '#bda9d4': '#8aafc6',
    '#a788bd': '#699db9', '#c4dfcb': '#bbd9d7', '#e6f3e9': '#edf7f5',
    '#547460': '#527e7b', '#587161': '#527e7b', '#a58aba': '#7aa7c0',
    '#70657d': '#597487', '#6c6177': '#597487',
    '#ece0fa': '#e4f0fa', '#d3b7f0': '#bdd9ee',
    '#e0f3e5': '#e5f4ed', '#afdcb9': '#b4dfca',
    '#fff0d3': '#fff2d8', '#f2d284': '#efd28d',
    '#e2edfb': '#e1f2f3', '#b7d1ee': '#afd8dc',
    '#fbe3eb': '#eaf0f6', '#efb4c8': '#c3d2e0',
    '#eef0d6': '#eef3df', '#d2d99e': '#cedea9',
}
DARK = {
    **LIGHT,
    '#34304b': '#e1edf5', '#514567': '#4d728c', '#f6f2fd': '#101e2b',
    '#d9ccef': '#080f17', '#e4ddf1': '#223548', '#6f6381': '#9fb8ca',
    '#766486': '#9fb8ca', '#6b6079': '#9fb8ca',
    '#ddd0f5': '#25485f', '#c9e9d1': '#234b3e', '#ffe6a1': '#554728',
    '#e4dcf1': '#263c50', '#b8a0d9': '#558bae', '#d8efda': '#a9d3bf',
    '#d6c7eb': '#314f64', '#c4dfcb': '#081613', '#e6f3e9': '#112925',
    '#547460': '#4f8c80', '#587161': '#a2c8bf',
    '#70657d': '#9fb8ca', '#6c6177': '#9fb8ca',
    '#ece0fa': '#142b3e', '#d3b7f0': '#294d67',
    '#e0f3e5': '#152f28', '#afdcb9': '#2d5746',
    '#fff0d3': '#302919', '#f2d284': '#65532e',
    '#e2edfb': '#142d32', '#b7d1ee': '#2c5760',
    '#fbe3eb': '#1d2a38', '#efb4c8': '#3c5269',
    '#eef0d6': '#26301d', '#d2d99e': '#4e6333',
}


def recolour(document, theme):
    palette = DARK if theme == 'dark' else LIGHT
    document = re.sub(r'#[0-9a-fA-F]{6}', lambda m: palette.get(m[0].lower(), m[0]), document)
    if theme == 'dark':
        # Text stays bright; outlines use a gentler contrast against dark cards.
        document = document.replace('stroke="#e1edf5"', 'stroke="#527287"')
        document = re.sub(r'(<g transform="translate\(523 56\) scale\(\.62\)">)(.*?)(</g>)', lambda m: m[1] + m[2].replace('#527287', '#d1e3ef') + m[3], document)
    return document


def sprout(x, y, scale=4, petal=None):
    return garden.pixel(['......', '.gg...', '.ggg..', '...g..', '...ggg', '...gg.', '...g..', '..dddd', '..dddd'], {'g': '#6cad8c', 'd': '#bd9160'}, x, y, scale)


def artwork():
    with tempfile.TemporaryDirectory() as temp:
        garden.ASSETS = Path(temp)
        garden.flower = sprout
        garden.header()
        garden.cards()
        garden.divider()
        garden.footer()
        for source in Path(temp).glob('*.svg'):
            raw = source.read_text().replace('cat, flowers, and sunshine', 'cat, greenery, and sunshine').replace('flower garden', 'pixel garden')
            for theme in ['light', 'dark']:
                target = source.name.replace('-v4.svg', f'-v5-{theme}.svg')
                (ASSETS / target).write_text(recolour(raw, theme))


GROUPS = [
    ('Interfaces', [('typescript', 'TypeScript'), ('react', 'React'), ('nextjs', 'Next.js'), ('tailwindcss', 'Tailwind CSS'), ('vitejs', 'Vite')]),
    ('APIs & data', [('python', 'Python'), ('fastapi', 'FastAPI'), ('pydantic', 'Pydantic'), ('postgresql', 'PostgreSQL'), ('sqlalchemy', 'SQLAlchemy'), ('sqlite', 'SQLite'), ('redis', 'Redis'), ('celery', 'Celery')]),
    ('AI workflows', [('langgraph', 'LangGraph'), ('ollama', 'Ollama'), ('googlegemini', 'Gemini'), ('openrouter', 'OpenRouter'), ('tavily', 'Tavily')]),
    ('Build & check', [('git', 'Git'), ('docker', 'Docker Compose'), ('pytest', 'pytest'), ('java', 'Java')]),
]
BRAND = {'pydantic': '#e92063', 'celery': '#5ba84c', 'langgraph': '#438876', 'ollama': '#243947', 'googlegemini': '#648de5', 'openrouter': '#597fbc', 'tavily': '#243947'}


def logo(slug, theme):
    root = ET.parse(ASSETS / 'icons' / (slug + '.svg')).getroot()
    assert not any(node.tag.split('}')[-1] in ['script', 'foreignObject', 'image'] for node in root.iter())
    root.set('x', '40')
    root.set('y', '16')
    root.set('width', '44')
    root.set('height', '44')
    root.set('preserveAspectRatio', 'xMidYMid meet')
    root.set('fill', BRAND.get(slug, '#000000'))
    # Plain black marks get light ink; preserve multicolour brand artwork.
    if theme == 'dark' and slug not in ['nextjs']:
        if root.get('fill') in ['#000000', '#243947']:
            root.set('fill', '#dce9f3')
        for node in root.iter():
            for attr in ['fill', 'stroke']:
                if node.get(attr, '').lower() in ['#000', '#000000', 'black', '#231f20', '#020202', '#333', '#333333', '#1f1e1e']:
                    node.set(attr, '#dce9f3')
    return ET.tostring(root, encoding='unicode')


def tiles():
    (ASSETS / 'stack').mkdir(exist_ok=True)
    for _, technologies in GROUPS:
        for slug, name in technologies:
            for theme in ['light', 'dark']:
                bg, border, ink = ('#f4f9fc', '#d6e5ed', '#34546a') if theme == 'light' else ('#142331', '#30495d', '#bfd3e1')
                content = f'<rect x="1" y="1" width="122" height="98" rx="14" fill="{bg}" stroke="{border}"/>'
                content += logo(slug, theme)
                size = 10 if len(name) > 11 else 12
                content += garden.text(62, 83, name, size, ink, 600, 'text-anchor="middle"')
                (ASSETS / 'stack' / f'{slug}-{theme}.svg').write_text(garden.svg(124, 100, name + ' logo', content))


if __name__ == '__main__':
    artwork()
    tiles()
