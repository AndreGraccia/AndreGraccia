#!/usr/bin/env python3
"""Generate two self-hosted SVG cards for the GitHub profile README."""
import json
import os
import urllib.error
import urllib.request
from collections import Counter
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

BG = "#1a1b27"
PANEL = "#24283b"
BORDER = "#414868"
TEXT = "#c0caf5"
MUTED = "#a9b1d6"
ACCENT = "#7aa2f7"
PURPLE = "#bb9af7"
GREEN = "#9ece6a"
CYAN = "#7dcfff"

LANG_COLORS = {
    "Java": "#b07219", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "Python": "#3572A5", "HTML": "#e34c26", "CSS": "#563d7c",
    "Shell": "#89e051", "Kotlin": "#A97BFF", "Go": "#00ADD8",
    "C": "#555555", "C++": "#f34b7d", "C#": "#178600",
    "PHP": "#4F5D95", "Ruby": "#701516", "Dart": "#00B4AB",
    "Swift": "#F05138", "Rust": "#dea584", "Jupyter Notebook": "#DA5B0B",
}

def api_get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))

def get_repositories():
    repos = []
    page = 1
    while page <= 10:
        batch = api_get(f"{API}/users/{USERNAME}/repos?type=owner&sort=updated&per_page=100&page={page}")
        if not batch:
            break
        repos.extend(r for r in batch if not r.get("fork") and not r.get("archived"))
        if len(batch) < 100:
            break
        page += 1
    return repos

def svg_start(width, height, title, description):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(description)}</desc>',
        '<defs><linearGradient id="top" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#7aa2f7"/><stop offset="100%" stop-color="#bb9af7"/></linearGradient></defs>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="14" fill="{BG}" stroke="{BORDER}"/>',
    ]

def text(x, y, value, size=13, color=TEXT, weight=400):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}">{escape(str(value))}</text>'

def write_stats(user, repos):
    stars = sum(r.get("stargazers_count", 0) for r in repos)
    forks = sum(r.get("forks_count", 0) for r in repos)
    metrics = [
        ("REPOSITÓRIOS PÚBLICOS", user.get("public_repos", len(repos)), ACCENT),
        ("SEGUIDORES", user.get("followers", 0), PURPLE),
        ("STARS RECEBIDAS", stars, GREEN),
        ("FORKS", forks, CYAN),
    ]
    s = svg_start(760, 220, "GitHub Stats — AndreGraccia", "Estatísticas públicas do perfil e dos repositórios próprios.")
    s += [text(28, 35, "GitHub Stats", 19, TEXT, 700),
          text(28, 57, "Visão geral dos meus repositórios públicos", 11, MUTED)]
    positions = [(24, 76), (388, 76), (24, 145), (388, 145)]
    for (label, value, color), (x, y) in zip(metrics, positions):
        s.append(f'<rect x="{x}" y="{y}" width="348" height="56" rx="9" fill="{PANEL}" stroke="{BORDER}"/>')
        s.append(f'<rect x="{x}" y="{y}" width="4" height="56" rx="2" fill="{color}"/>')
        s.append(text(x+17, y+22, label, 10, MUTED, 600))
        s.append(text(x+17, y+45, f"{value:,}", 20, color, 700))
    s.append(text(28, 211, "Dados públicos • atualizado em " + datetime.now(timezone.utc).strftime("%d/%m/%Y"), 9, MUTED))
    s.append("</svg>")
    with open("assets/github-stats.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(s))

def write_languages(repos):
    totals = Counter()
    for repo in repos:
        url = repo.get("languages_url")
        if not url:
            continue
        try:
            totals.update(api_get(url))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            print(f"Skipping languages for {repo.get('full_name')}: {exc}")
    total_bytes = sum(totals.values())
    top = totals.most_common(8)
    s = svg_start(760, 300, "Top Languages — AndreGraccia", "Distribuição das linguagens por bytes nos repositórios públicos próprios.")
    s += [text(28, 35, "Top Languages", 19, TEXT, 700),
          text(28, 57, "Distribuição por volume de código nos repositórios públicos", 11, MUTED)]
    if not top or total_bytes == 0:
        s.append(text(28, 115, "Ainda não há dados de linguagens disponíveis.", 13, MUTED))
    else:
        for i, (lang, amount) in enumerate(top):
            y = 91 + i * 24
            pct = amount / total_bytes * 100
            color = LANG_COLORS.get(lang, ["#7aa2f7", "#bb9af7", "#9ece6a", "#7dcfff"][i % 4])
            s.append(text(28, y+12, lang, 11, TEXT, 600))
            s.append(f'<rect x="170" y="{y}" width="430" height="10" rx="5" fill="{PANEL}"/>')
            s.append(f'<rect x="170" y="{y}" width="{430*pct/100:.2f}" height="10" rx="5" fill="{color}"/>')
            s.append(text(620, y+10, f"{pct:.1f}%", 11, color, 600))
    s.append(text(28, 278, "Percentuais calculados pelo tamanho dos arquivos • atualizado em " + datetime.now(timezone.utc).strftime("%d/%m/%Y"), 9, MUTED))
    s.append("</svg>")
    with open("assets/top-languages.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(s))

def main():
    os.makedirs("assets", exist_ok=True)
    user = api_get(f"{API}/users/{USERNAME}")
    repos = get_repositories()
    write_stats(user, repos)
    write_languages(repos)
    print(f"Generated SVG cards for {USERNAME}: {len(repos)} repositories.")

if __name__ == "__main__":
    main()
