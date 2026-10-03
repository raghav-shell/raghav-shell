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
    motion = '<style>.commit-dot{transform-box:fill-box;transform-origin:center;animation:commit 3s ease-in-out infinite}@keyframes commit{50%{opacity:.5;transform:scale(1.25)}}@media(prefers-reduced-motion:reduce){.commit-dot{animation:none}}</style>'
    content = motion + content
    content = re.sub(r'(fill|stroke)="(#[0-9a-fA-F]{6})"', lambda m: f'{m[1]}="{palette.get(m[2].lower(), m[2])}"', content)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><g font-family="{FONT}">{content}</g></svg>\n'


def short(value, maximum):
    return value if len(value) <= maximum else value[:maximum - 1] + "…"


def render_activity(snapshot, theme="light"):
    updated = date(snapshot["updated_at"]).astimezone(ZoneInfo("Asia/Kolkata")).strftime("%d %b %Y · %H:%M IST")
    projects = sorted((p for p in snapshot["projects"] if p["commit"]), key=lambda p: date(p["commit"]["authored_at"]), reverse=True)[:4]
    s = '<defs><clipPath id="messages"><rect x="244" y="110" width="556" height="250"/></clipPath></defs><rect x=".5" y=".5" width="959" height="429" rx="22" fill="#131728" stroke="#38394f"/><path d="M30 1H930" stroke="#c4b5fd" stroke-width="2"/>'
    s += txt(32, 37, "THE BUILD LOG", 12, "#c4b5fd", 650, 'letter-spacing="2"')
    s += txt(31, 81, "The latest little steps.", 31, "#f5f4ff", 750, 'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"')
    s += txt(929, 38, "UPDATED DAILY / GITHUB", 11, "#a6b1cb", 500, 'text-anchor="end" letter-spacing="1"')
    s += '<path d="M32 106H928" stroke="#33374c"/>'
    for index, project in enumerate(projects):
        y = 143 + index * 60
        commit = project["commit"]
        s += f'<circle class="commit-dot" cx="40" cy="{y-5}" r="6" fill="{project["color"]}"/>'
        s += txt(59, y, project["name"], 19, project["color"], 650)
        s += '<g clip-path="url(#messages)">' + txt(244, y, short(commit["message"], 54), 17) + '</g>'
        s += txt(928, y, date(commit["authored_at"]).strftime("%d %b %Y"), 13, "#abb7cf", 500, 'text-anchor="end"')
        s += txt(244, y + 20, commit["sha"][:7] + " · " + project["repo"].split('/')[0], 11, "#8995b3")
    if not projects:
        s += txt(32, 176, "No public authored commits found in the selected repositories.", 20)
    s += '<path d="M32 367H928" stroke="#33374c"/>'
    s += txt(32, 397, f"SNAPSHOT · {updated}", 11, "#abb7cf", 500, 'letter-spacing=".7"')
    s += txt(928, 397, f"{len(snapshot['projects'])} SELECTED REPOSITORIES", 11, "#a9a1d4", 500, 'text-anchor="end" letter-spacing=".7"')
    title = "Latest authored commits. " + "; ".join(p["name"] + ": " + p["commit"]["message"] for p in projects) + ". Snapshot " + updated
    return frame(960, 430, title, s, theme)


def render_mobile_activity(snapshot, theme="light"):
    updated = date(snapshot["updated_at"]).astimezone(ZoneInfo("Asia/Kolkata")).strftime("%d %b %Y · %H:%M IST")
    projects = sorted((p for p in snapshot["projects"] if p["commit"]), key=lambda p: date(p["commit"]["authored_at"]), reverse=True)[:4]
    s = '<defs><clipPath id="content"><rect x="22" y="102" width="376" height="405"/></clipPath></defs><rect x=".5" y=".5" width="419" height="559" rx="20" fill="#131728" stroke="#38394f"/>'
    s += txt(22, 33, "THE BUILD LOG", 11, "#c4b5fd", 650, 'letter-spacing="1.6"')
    s += txt(21, 73, "The latest little steps.", 25, "#f5f4ff", 750, 'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"')
    s += '<path d="M22 91H398" stroke="#33374c"/><g clip-path="url(#content)">'
    for index, project in enumerate(projects):
        y = 121 + index * 98
        commit = project["commit"]
        s += f'<circle class="commit-dot" cx="28" cy="{y-6}" r="4" fill="{project["color"]}"/>'
        s += txt(41, y, project["name"], 18, project["color"], 650)
        s += txt(398, y, date(commit["authored_at"]).strftime("%d %b %Y"), 12, "#abb7cf", 500, 'text-anchor="end"')
        lines = textwrap.wrap(commit["message"], width=43, max_lines=2, placeholder="…")
        for line, value in enumerate(lines):
            s += txt(22, y + 25 + line * 21, value, 15)
        s += txt(22, y + 65, commit["sha"][:7], 11, "#8995b3")
    if not projects:
        s += txt(22, 130, "No public authored commits found.", 17)
    s += '</g><path d="M22 511H398" stroke="#33374c"/>'
    s += txt(22, 538, updated, 11, "#abb7cf")
    return frame(420, 560, "Latest public authored commits. Snapshot " + updated, s, theme)


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
