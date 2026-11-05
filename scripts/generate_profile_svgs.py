#!/usr/bin/env python3
"""Generate a self-hosted GitHub activity stats card for AndreGraccia's profile."""
import json
import os
import urllib.parse
import urllib.request
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


def text(x, y, value, size=13, color=TEXT, weight=400):
    return (
        f'<text x="{x}" y="{y}" fill="{color}" '
        'font-family="Inter,Segoe UI,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}">{escape(str(value))}</text>'
    )


def metric_card(label, value, color, x, y):
    return [
        f'<rect x="{x}" y="{y}" width="348" height="58" rx="10" fill="{PANEL}" stroke="{BORDER}"/>',
        f'<rect x="{x}" y="{y}" width="4" height="58" rx="2" fill="{color}"/>',
        f'<circle cx="{x + 23}" cy="{y + 29}" r="8" fill="{color}" fill-opacity=".16" stroke="{color}" stroke-opacity=".65"/>',
        text(x + 42, y + 24, label, 10, MUTED, 700),
        text(x + 42, y + 46, f"{value:,}", 20, color, 700),
    ]


def main():
    user = api_get(f"{API}/users/{USERNAME}")
    commits = search_count(f"author:{USERNAME}", "commits")
    pull_requests = search_count(f"author:{USERNAME} type:pr", "issues")
    issues = search_count(f"author:{USERNAME} type:issue", "issues")
    repos = int(user.get("public_repos", 0))
    followers = int(user.get("followers", 0))

    # This is a transparent activity tier, not an official GitHub rank or code-quality score.
    score = commits + (pull_requests * 3) + (issues * 2) + (repos * 2) + followers
    if score >= 500:
        tier, tier_color = "A", GREEN
    elif score >= 150:
        tier, tier_color = "B", BLUE
    else:
        tier, tier_color = "C", PURPLE

    width, height = 760, 250
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">GitHub Activity — AndreGraccia</title>',
        '<desc id="desc">Cartão de estatísticas públicas do GitHub com commits, pull requests, issues, repositórios e nível estimado de atividade.</desc>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="16" fill="{BG}" stroke="{BORDER}"/>',
        text(28, 38, "GitHub Stats", 21, TEXT, 700),
        text(28, 59, "Public contributions and project activity", 11, MUTED),
        f'<rect x="638" y="17" width="92" height="70" rx="12" fill="{PANEL}" stroke="{BORDER}"/>',
        text(655, 39, "RANK", 10, MUTED, 700),
        text(665, 74, tier, 32, tier_color, 700),
    ]
    cards = [
        ("COMMITS", commits, BLUE, 24, 101),
        ("PULL REQUESTS", pull_requests, PURPLE, 388, 101),
        ("ISSUES", issues, GREEN, 24, 169),
        ("PUBLIC REPOSITORIES", repos, CYAN, 388, 169),
    ]
    for item in cards:
        parts.extend(metric_card(*item))
    parts.extend([
        text(28, 242, "Activity tier calculated from public GitHub data · Not an official GitHub ranking", 9, MUTED),
        "</svg>",
    ])

    os.makedirs("assets", exist_ok=True)
    with open("assets/github-activity.svg", "w", encoding="utf-8") as output:
        output.write("\n".join(parts))
    print(f"Updated activity SVG: {commits} commits, {pull_requests} PRs, {issues} issues, {repos} public repositories.")


if __name__ == "__main__":
    main()
