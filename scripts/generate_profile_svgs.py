#!/usr/bin/env python3
"""Generate a self-hosted GitHub activity SVG for AndreGraccia's profile."""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html import escape

USERNAME = "AndreGraccia"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "AndreGraccia-profile-analytics",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

BG, PANEL, BORDER = "#1a1b27", "#24283b", "#414868"
TEXT, MUTED = "#c0caf5", "#a9b1d6"
BLUE, PURPLE, GREEN, CYAN = "#7aa2f7", "#bb9af7", "#9ece6a", "#7dcfff"

def api_get(url):
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))

def search_count(query, kind):
    encoded = urllib.parse.quote(query, safe=":")
    result = api_get(f"{API}/search/{kind}?q={encoded}&per_page=1")
    return int(result.get("total_count", 0))

def svg_text(x, y, value, size=13, color=TEXT, weight=400):
    return (f'<text x="{x}" y="{y}" fill="{color}" '
            f'font-family="Inter,Segoe UI,Arial,sans-serif" '
            f'font-size="{size}" font-weight="{weight}">{escape(str(value))}</text>')

def main():
    user = api_get(f"{API}/users/{USERNAME}")
    commits = search_count(f"author:{USERNAME}", "commits")
    pull_requests = search_count(f"author:{USERNAME} type:pr", "issues")
    issues = search_count(f"author:{USERNAME} type:issue", "issues")
    repos = int(user.get("public_repos", 0))
    followers = int(user.get("followers", 0))

    # Activity tier is a transparent profile-activity indicator, not a code-quality score.
    score = commits + (pull_requests * 3) + (issues * 2) + (repos * 2) + followers
    if score >= 500:
        tier, tier_color = "A", GREEN
    elif score >= 150:
        tier, tier_color = "B", BLUE
    else:
        tier, tier_color = "C", PURPLE

    width, height = 760, 238
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">GitHub Activity — AndreGraccia</title>',
        '<desc id="desc">Commits, pull requests, issues, repositórios públicos e nível estimado de atividade.</desc>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="14" fill="{BG}" stroke="{BORDER}"/>',
        svg_text(28, 36, "GitHub Activity", 20, TEXT, 700),
        svg_text(28, 57, "Contribuições públicas e participação em projetos", 11, MUTED),
        f'<rect x="638" y="18" width="92" height="66" rx="10" fill="{PANEL}" stroke="{BORDER}"/>',
        svg_text(655, 39, "RANK", 10, MUTED, 700),
        svg_text(665, 72, tier, 31, tier_color, 700),
    ]
    metrics = [
        ("COMMITS", commits, BLUE, 24, 93),
        ("PULL REQUESTS", pull_requests, PURPLE, 388, 93),
        ("ISSUES", issues, GREEN, 24, 158),
        ("REPOSITÓRIOS PÚBLICOS", repos, CYAN, 388, 158),
    ]
    for label, value, color, x, y in metrics:
        parts.append(f'<rect x="{x}" y="{y}" width="348" height="54" rx="9" fill="{PANEL}" stroke="{BORDER}"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="4" height="54" rx="2" fill="{color}"/>')
        parts.append(svg_text(x+17, y+20, label, 10, MUTED, 600))
        parts.append(svg_text(x+17, y+43, f"{value:,}", 19, color, 700))
    parts.append(svg_text(28, 226, "Rank de atividade estimado a partir dos dados públicos; não representa avaliação de qualidade.", 9, MUTED))
    parts.append("</svg>")

    os.makedirs("assets", exist_ok=True)
    with open("assets/github-activity.svg", "w", encoding="utf-8") as output:
        output.write("\n".join(parts))
    print(f"Updated activity SVG: {commits} commits, {pull_requests} PRs, {issues} issues.")

if __name__ == "__main__":
    main()
