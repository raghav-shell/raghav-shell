"""Refresh profile SVGs from public GitHub commits; Python standard library only.

Fetch every repository before writing anything. API failures preserve the last
successful snapshot and fail the workflow rather than publishing invented data.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import textwrap
import urllib.request
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
USER = "raghav-shell"
PROJECTS = [
    ("aegis", "AEGIS", "kartikeyajay2006/Sovereign-On_Premise-Agentic-AI-Workbench", "#c4b5fd"),
    ("visionx", "VisionX", "raghav-shell/VisionX", "#67e8f9"),
    ("razorflow", "RazorFlow", "raghav-shell/RazorFlow", "#fda4af"),
    ("competeiq", "CompeteIQ", "raghav-shell/Compete_latest", "#93c5fd"),
    ("lexguard", "Lexguard", "raghav-shell/Lexguard", "#f0abfc"),
    ("shell", "Os_Shell", "raghav-shell/Os_Shell", "#bef264"),
]
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

# Source colours map to coordinated light and dark GitHub artwork.
LIGHT = {
    "#131728": "#f2f8fc", "#38394f": "#b8d0de", "#c4b5fd": "#3a719c",
    "#67e8f9": "#35795f", "#fda4af": "#956e25", "#93c5fd": "#377f89",
    "#f0abfc": "#526f8b", "#bef264": "#6b7c39", "#d6ddef": "#597487",
    "#f5f4ff": "#19364b", "#a6b1cb": "#597487", "#abb7cf": "#597487",
    "#33374c": "#d6e5ed", "#8995b3": "#6b8395", "#a9a1d4": "#597487",
    "#191d31": "#f2f8fc", "#383d56": "#b8d0de", "#cbd3e8": "#597487",
}
DARK = {
    **LIGHT,
    "#131728": "#101e2b", "#38394f": "#365469", "#c4b5fd": "#8cc2e8",
    "#67e8f9": "#90cdb0", "#fda4af": "#e0bd72", "#93c5fd": "#8bc8cf",
    "#f0abfc": "#a9c3dc", "#bef264": "#b4ce85", "#d6ddef": "#b9cedd",
    "#f5f4ff": "#e1edf5", "#a6b1cb": "#9fb8ca", "#abb7cf": "#9fb8ca",
    "#33374c": "#30495d", "#8995b3": "#8aa6ba", "#a9a1d4": "#9fb8ca",
    "#191d31": "#101e2b", "#383d56": "#365469", "#cbd3e8": "#b9cedd",
}


def api(path):
    headers = {"User-Agent": "raghav-shell-profile", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request("https://api.github.com/" + path, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def date(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def normalize(project, payload):
    slug, name, repo, color = project
    if not isinstance(payload, list):
        raise ValueError(f"Unexpected commit response for {repo}")
    result = {"slug": slug, "name": name, "repo": repo, "color": color, "commit": None}
    if not payload:
        return result
    item = payload[0]
    sha = item["sha"]
    if not re.fullmatch(r"[a-f0-9]{40}", sha):
        raise ValueError(f"Invalid commit SHA for {repo}")
    authored_at = item["commit"]["author"]["date"]
    date(authored_at)
    result["commit"] = {
        "sha": sha,
        "url": f"https://github.com/{repo}/commit/{sha}",
        "message": " ".join(item["commit"]["message"].splitlines()[0].split()),
        "authored_at": authored_at,
    }
    return result


def fetch_project(project):
    return normalize(project, api(f"repos/{project[2]}/commits?author={USER}&per_page=1"))


def txt(x, y, content, size=18, color="#d6ddef", weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(str(content))}</text>'


def frame(width, height, title, content, theme="light"):
    palette = DARK if theme == "dark" else LIGHT
    content = re.sub(r'(fill|stroke)="(#[0-9a-fA-F]{6})"', lambda m: f'{m[1]}="{palette.get(m[2].lower(), m[2])}"', content)
    if 'class="commit-dot"' in content:
        content = '<style>.commit-dot{animation:pulse 4s ease-in-out infinite}@keyframes pulse{50%{opacity:.4}}@media(prefers-reduced-motion:reduce){.commit-dot{animation:none}}</style>' + content
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><g font-family="{FONT}">{content}</g></svg>\n'


def short(value, maximum):
    return value if len(value) <= maximum else value[:maximum - 1] + "…"


MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', monospace"
# Terminal colours: the build log reads as a real `git log`, echoing the hero's laptop.
TERMINAL = {
    "light": dict(shadow="#c9dce8", frame="#46697e", bar="#f2f8fc", bar_text="#4c6e83", screen="#13293d"),
    "dark": dict(shadow="#080f17", frame="#4d728c", bar="#101e2b", bar_text="#abc3d3", screen="#060e16"),
}
INK = dict(text="#c2ead8", dim="#7fa7bf", sha="#f6d277", ok="#8fdcb5")
NAME_COLOURS = {"aegis": "#8cc2e8", "visionx": "#8fdcb5", "razorflow": "#f2c46d",
                "competeiq": "#7fd6db", "lexguard": "#b9b4f0", "shell": "#c3df8a"}


def recent(snapshot, limit):
    return sorted((p for p in snapshot["projects"] if p["commit"]), key=lambda p: date(p["commit"]["authored_at"]), reverse=True)[:limit]


def mono(x, y, content, size, color, weight=500, extra=""):
    return txt(x, y, content, size, color, weight, f'font-family="{MONO}" {extra}')


def terminal(width, height, label, body, theme):
    t = TERMINAL[theme]
    s = f'<rect x="8" y="8" width="{width - 10}" height="{height - 10}" rx="18" fill="{t["shadow"]}"/>'
    s += f'<defs><clipPath id="window"><rect x="2" y="2" width="{width - 10}" height="{height - 10}" rx="18"/></clipPath></defs>'
    s += f'<g clip-path="url(#window)"><rect width="{width}" height="{height}" fill="{t["screen"]}"/>'
    s += f'<rect width="{width}" height="44" fill="{t["bar"]}"/><path d="M0 44H{width}" stroke="{t["frame"]}" stroke-width="1.5"/>'
    for i, c in enumerate(["#8bbddd", "#f6cf69", "#a1d7b0"]):
        s += f'<circle cx="{24 + i * 17}" cy="23" r="5" fill="{c}"/>'
    s += mono(84, 28, label, 12, t["bar_text"]) + body + "</g>"
    s += f'<rect x="2" y="2" width="{width - 10}" height="{height - 10}" rx="18" fill="none" stroke="{t["frame"]}" stroke-width="2"/>'
    return s


def svg_document(width, height, title, content):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><g font-family="{FONT}">{content}</g></svg>\n'


def render_activity(snapshot, theme="light"):
    updated = date(snapshot["updated_at"]).astimezone(ZoneInfo("Asia/Kolkata")).strftime("%d %b %Y · %H:%M IST")
    projects = recent(snapshot, 6)
    rows = max(len(projects), 1)
    width, height = 960, 196 + rows * 36
    s = mono(30, 86, "$ git log --author=raghav-shell --latest-per-project", 14, INK["text"], 700)
    for index, project in enumerate(projects):
        y = 126 + index * 36
        commit = project["commit"]
        s += mono(30, y, commit["sha"][:7], 14, INK["sha"])
        s += mono(108, y, project["name"], 14, NAME_COLOURS.get(project["slug"], INK["text"]), 700)
        s += mono(212, y, short(commit["message"], 62), 14, INK["text"])
        s += mono(922, y, date(commit["authored_at"]).strftime("%d %b %Y"), 13, INK["dim"], 500, 'text-anchor="end"')
    if not projects:
        s += mono(30, 126, "# No public authored commits found in the selected repositories.", 14, INK["dim"])
    footer = 126 + rows * 36 + 6
    s += mono(30, footer, f"# snapshot {updated} · {len(snapshot['projects'])} repositories watched", 12, INK["dim"])
    s += mono(30, footer + 30, "$", 14, INK["text"], 700) + f'<rect x="46" y="{footer + 18}" width="8" height="15" fill="{INK["text"]}"/>'
    title = "Build log: latest authored commits. " + "; ".join(p["name"] + ": " + p["commit"]["message"] for p in projects) + ". Snapshot " + updated
    return svg_document(width, height, title, terminal(width, height, "~/garden — git log", s, theme))


def render_mobile_activity(snapshot, theme="light"):
    updated = date(snapshot["updated_at"]).astimezone(ZoneInfo("Asia/Kolkata")).strftime("%d %b %Y · %H:%M IST")
    projects = recent(snapshot, 4)
    rows = max(len(projects), 1)
    width, height = 420, 150 + rows * 62
    s = mono(20, 78, "$ git log --latest", 13, INK["text"], 700)
    for index, project in enumerate(projects):
        y = 112 + index * 62
        commit = project["commit"]
        s += mono(20, y, commit["sha"][:7], 12, INK["sha"])
        s += mono(84, y, project["name"], 12, NAME_COLOURS.get(project["slug"], INK["text"]), 700)
        s += mono(396, y, date(commit["authored_at"]).strftime("%d %b %Y"), 11, INK["dim"], 500, 'text-anchor="end"')
        s += mono(20, y + 22, short(commit["message"], 52), 11, INK["text"])
    if not projects:
        s += mono(20, 112, "# No public authored commits found.", 12, INK["dim"])
    s += mono(20, 112 + rows * 62, f"# {updated}", 11, INK["dim"])
    return svg_document(width, height, "Build log: latest public authored commits. Snapshot " + updated, terminal(width, height, "~/garden — git log", s, theme))


def render_badge(project):
    commit = project["commit"]
    value = date(commit["authored_at"]).strftime("%d %b %Y") if commit else "not found"
    label = project["name"] + " · my latest commit"
    # Fixed, comfortably sized slots avoid layout changes on the next refresh.
    s = f'<rect x=".5" y=".5" width="419" height="31" rx="8" fill="#191d31" stroke="#383d56"/><circle cx="14" cy="16" r="3" fill="{project["color"]}"/>'
    s += txt(25, 21, label, 12, "#cbd3e8", 500)
    s += txt(405, 21, value, 12, project["color"], 600, 'text-anchor="end"')
    return frame(420, 32, f"{label}: {value}", s)


def render_files(snapshot):
    files = {
        "activity.svg": render_activity(snapshot),
        "activity-mobile.svg": render_mobile_activity(snapshot),
        "activity-dark.svg": render_activity(snapshot, "dark"),
        "activity-mobile-dark.svg": render_mobile_activity(snapshot, "dark"),
    }
    for project in snapshot["projects"]:
        files["latest-" + project["slug"] + ".svg"] = render_badge(project)
    files["snapshot.json"] = json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n"
    return files


def refresh(output, now=None):
    with ThreadPoolExecutor(max_workers=3) as pool:
        projects = list(pool.map(fetch_project, PROJECTS))
    snapshot = {"user": USER, "updated_at": (now or datetime.now(timezone.utc)).isoformat(), "source": "GitHub REST API: latest commit filtered by author on each repository's default branch", "projects": projects}
    files = render_files(snapshot)
    output.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        temporary = output / (name + ".tmp")
        temporary.write_text(content)
        temporary.replace(output / name)
    return snapshot


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "assets" / "live")
    args = parser.parse_args()
    snapshot = refresh(args.output)
    print(f"Refreshed {len(snapshot['projects'])} repositories at {snapshot['updated_at']}")
