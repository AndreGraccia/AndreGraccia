"""Gera assets/activity.svg (commits/dia, 30 dias) e assets/langs.svg (linguagens por bytes).
Uso: GITHUB_TOKEN=... python scripts/build_stats.py [usuario]
Sem token, só langs.svg é gerado (a API de contribuições exige autenticação).
"""
import json, os, sys, urllib.request
from datetime import date, timedelta

USER = sys.argv[1] if len(sys.argv) > 1 else "AndreGraccia"
TOKEN = os.environ.get("GITHUB_TOKEN")
BLUE, MUTE, GRID = "#2997ff", "#7a7a7a", "#8e8e9340"
STYLE = "<style>.t{fill:#1d1d1f}@media(prefers-color-scheme:dark){.t{fill:#f5f5f7}}</style>"
FONT = "font-family=\"-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif\""


def api(url, body=None):
    req = urllib.request.Request(url, json.dumps(body).encode() if body else None)
    req.add_header("User-Agent", "profile-stats")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def langs_svg():
    repos = api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
    total = {}
    for r in repos:
        if r["fork"]:
            continue
        for lang, n in api(r["languages_url"]).items():
            total[lang] = total.get(lang, 0) + n
    top = sorted(total.items(), key=lambda kv: -kv[1])[:6]
    s = sum(n for _, n in top) or 1
    rows = ""
    for i, (lang, n) in enumerate(top):
        y, pct = 56 + i * 32, n / s * 100
        rows += (f'<text x="0" y="{y}" class="t" font-size="14">{lang}</text>'
                 f'<rect x="110" y="{y-11}" width="300" height="8" rx="4" fill="{GRID}"/>'
                 f'<rect x="110" y="{y-11}" width="{max(pct*3,6):.0f}" height="8" rx="4" fill="{BLUE}"/>'
                 f'<text x="425" y="{y}" fill="{MUTE}" font-size="13">{pct:.1f}%</text>')
    h = 70 + len(top) * 32
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="{h}" viewBox="0 0 480 {h}" {FONT}>{STYLE}'
            f'<text x="0" y="20" class="t" font-size="17" font-weight="600">Linguagens mais usadas</text>'
            f'{rows}</svg>')


def activity_svg():
    start = date.today() - timedelta(days=29)
    q = ('query($u:String!,$f:DateTime!){user(login:$u){contributionsCollection(from:$f){'
         'contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}')
    d = api("https://api.github.com/graphql", {"query": q, "variables": {"u": USER, "f": f"{start}T00:00:00Z"}})
    days = {x["date"]: x["contributionCount"]
            for w in d["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
            for x in w["contributionDays"]}
    vals = [days.get(str(start + timedelta(days=i)), 0) for i in range(30)]
    W, H, L, B, T = 760, 220, 36, 190, 50
    mx = max(max(vals), 1)
    pts = [(L + i * (W - L - 10) / 29, B - v / mx * (B - T)) for i, v in enumerate(vals)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{L},{B} {line} {pts[-1][0]:.1f},{B}"
    grid = "".join(f'<line x1="{L}" x2="{W-10}" y1="{y}" y2="{y}" stroke="{GRID}"/>' for y in (T, (T + B) / 2, B))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" {FONT}>{STYLE}'
            f'<text x="0" y="20" class="t" font-size="17" font-weight="600">Contribuições nos últimos 30 dias</text>'
            f'<text x="0" y="38" fill="{MUTE}" font-size="13">{sum(vals)} no total · máximo {mx} por dia</text>'
            f'{grid}<polygon points="{area}" fill="{BLUE}" opacity=".15"/>'
            f'<polyline points="{line}" fill="none" stroke="{BLUE}" stroke-width="2" stroke-linejoin="round"/>'
            f'<text x="{L}" y="{H-8}" fill="{MUTE}" font-size="12">{start:%d/%m}</text>'
            f'<text x="{W-10}" y="{H-8}" fill="{MUTE}" font-size="12" text-anchor="end">{date.today():%d/%m}</text></svg>')


os.makedirs("assets", exist_ok=True)
open("assets/langs.svg", "w", encoding="utf-8").write(langs_svg())
if TOKEN:
    open("assets/activity.svg", "w", encoding="utf-8").write(activity_svg())
else:
    print("sem GITHUB_TOKEN: activity.svg não gerado")
