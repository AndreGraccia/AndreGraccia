#!/usr/bin/env python3
"""Generate the profile metrics SVG from GitHub's authenticated API."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER", "AndreGraccia")
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = Path("assets/metrics.svg")
API = "https://api.github.com"


def request(url: str, *, payload: dict | None = None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "AndreGraccia-profile-metrics",
            **({"Content-Type": "application/json"} if data else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode())


def collect_metrics() -> dict[str, int]:
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    query = """
    query($from: DateTime!, $to: DateTime!) {
      viewer {
        login
        contributionsCollection(from: $from, to: $to) {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          repositoriesContributedTo(first: 1) { totalCount }
        }
      }
    }
    """
    graph = request(
        "https://api.github.com/graphql",
        payload={"query": query, "variables": {"from": "2000-01-01T00:00:00Z", "to": now}},
    )
    if graph.get("errors"):
        raise RuntimeError(f"GitHub GraphQL error: {graph['errors']}")
    contributions = graph["data"]["viewer"]["contributionsCollection"]

    stars = 0
    page = 1
    while True:
        repos = request(
            f"{API}/users/{USERNAME}/repos?type=owner&per_page=100&page={page}&sort=updated"
        )
        if not repos:
            break
        stars += sum(int(repo.get("stargazers_count", 0)) for repo in repos)
        if len(repos) < 100:
            break
        page += 1

    return {
        "stars": stars,
        "commits": int(contributions["totalCommitContributions"]),
        "prs": int(contributions["totalPullRequestContributions"]),
        "issues": int(contributions["totalIssueContributions"]),
        "contributed_to": int(contributions["repositoriesContributedTo"]["totalCount"]),
    }


def build_svg(m: dict[str, int]) -> str:
    cards = [
        ("TOTAL STARS", m["stars"], "repositorios próprios"),
        ("TOTAL COMMITS", m["commits"], "contribuições de commit"),
        ("TOTAL PRS", m["prs"], "pull requests"),
        ("TOTAL ISSUES", m["issues"], "issues abertas/criadas"),
        ("CONTRIBUTED TO", m["contributed_to"], "repositórios"),
    ]
    card_w, gap, x0 = 196, 18, 24
    blocks = []
    for i, (label, value, hint) in enumerate(cards):
        x = x0 + i * (card_w + gap)
        blocks.append(f"""
        <g transform="translate({x} 76)">
          <rect width="{card_w}" height="142" rx="16" fill="#111522" stroke="#8C78FF" stroke-opacity=".24"/>
          <rect x="1" y="1" width="{card_w-2}" height="2" rx="1" fill="url(#accent)" opacity=".9"/>
          <text x="18" y="31" class="label">{escape(label)}</text>
          <text x="18" y="83" class="value">{value:,}</text>
          <text x="18" y="112" class="hint">{escape(hint)}</text>
        </g>""")
    activity = m["commits"] + m["prs"] + m["issues"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1094" height="250" viewBox="0 0 1094 250" role="img" aria-labelledby="title desc">
<title id="title">GitHub profile metrics — Andre Graccia</title>
<desc id="desc">Estatísticas públicas atualizadas automaticamente pelo GitHub Actions.</desc>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#8C78FF"/><stop offset="1" stop-color="#78CFFF"/></linearGradient>
  <radialGradient id="glow"><stop stop-color="#8C78FF" stop-opacity=".18"/><stop offset="1" stop-color="#8C78FF" stop-opacity="0"/></radialGradient>
  <style>
    .label{{font:600 10px Inter,Arial,sans-serif;letter-spacing:1.1px;fill:#A6A9B8}}
    .value{{font:700 34px Inter,Arial,sans-serif;letter-spacing:-1.5px;fill:#F5F5FA}}
    .hint{{font:12px Inter,Arial,sans-serif;fill:#858B9D}}
    .meta{{font:11px 'JetBrains Mono',Consolas,monospace;letter-spacing:1.2px;fill:#A99BFF}}
  </style>
</defs>
<rect x="1" y="1" width="1092" height="248" rx="20" fill="#090B13" stroke="#8C78FF" stroke-opacity=".25"/>
<ellipse cx="1000" cy="20" rx="230" ry="140" fill="url(#glow)"/>
<text x="24" y="35" class="meta">GITHUB / PROFILE METRICS</text>
<text x="1070" y="35" text-anchor="end" class="hint">Atualizado automaticamente</text>
{''.join(blocks)}
<circle cx="1050" cy="226" r="3" fill="#78CFFF"/>
<text x="1038" y="230" text-anchor="end" class="hint">ACTIVITY INDEX · {activity:,} contribuições</text>
</svg>
'''


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    metrics = collect_metrics()
    OUT.write_text(build_svg(metrics), encoding="utf-8")
    print(f"Updated {OUT}: {metrics}")


if __name__ == "__main__":
    main()
