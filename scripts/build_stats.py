#!/usr/bin/env python3
"""Gera assets/stats.svg: números do perfil, heatmap de 12 meses e linguagens.

Fontes públicas (sem token obrigatório): API REST do GitHub e a página pública de contribuições.
Se GITHUB_TOKEN existir, é usado só para ampliar o limite da API REST.
"""
import json, os, re, sys, urllib.request
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from html import unescape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_visuals import BLUE, DEFS, DIM, INK, MUTED, OUT, SKY, STYLE, VIOLET, pane  # noqa: E402

USER = os.environ.get("GITHUB_REPOSITORY_OWNER", "AndreGraccia")
TOKEN = os.environ.get("GITHUB_TOKEN")
LANG_COLORS = {"Java": "#F89820", "HTML": "#E34F26", "CSS": "#1572B6", "Python": "#3776AB", "JavaScript": "#F7DF1E",
               "TypeScript": "#3178C6", "Shell": "#89E051", "Dockerfile": "#2496ED"}
LEVELS = ["#ffffff", "#2c0d74", "#5119d4", "#a88bf9", "#e0d6ff"]  # nível 0 usa opacidade baixa


def get(url, api=False):
    h = {"User-Agent": "profile-stats"}
    if api:
        h["Accept"] = "application/vnd.github+json"
        if TOKEN:
            h["Authorization"] = f"Bearer {TOKEN}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
        return r.read().decode("utf-8")


def collect():
    user = json.loads(get(f"https://api.github.com/users/{USER}", api=True))
    repos = [r for r in json.loads(get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner", api=True)) if not r["fork"]]
    langs = Counter()
    for r in repos:
        for k, v in json.loads(get(r["languages_url"], api=True)).items():
            langs[k] += v

    page = get(f"https://github.com/users/{USER}/contributions")
    tips = {m.group(1): m.group(2) for m in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>', page, re.S)}
    days = {}
    for m in re.finditer(r"<td[^>]*>", page):
        tag = m.group(0)
        d, i, lv = (re.search(f'{k}="([^"]*)"', tag) for k in ("data-date", "id", "data-level"))
        if not (d and lv):
            continue
        n = re.match(r"(\d+)\s+contribution", unescape(tips.get(i.group(1), "")).strip()) if i else None
        days[d.group(1)] = (int(n.group(1)) if n else 0, int(lv.group(1)))
    if len(days) < 300:
        raise RuntimeError(f"calendário incompleto ({len(days)} dias): não vou publicar dados parciais")
    return user, repos, langs, days


def streaks(days):
    ordered = sorted(days)
    best = run = 0
    for d in ordered:
        run = run + 1 if days[d][0] > 0 else 0
        best = max(best, run)
    cur = 0
    for d in reversed(ordered):
        if days[d][0] > 0:
            cur += 1
        elif d != ordered[-1]:
            break
    return best, cur


def render(user, repos, langs, days):
    W, H = 1200, 560
    total = sum(n for n, _ in days.values())
    active = sum(1 for n, _ in days.values() if n)
    best, cur = streaks(days)
    stars = sum(r["stargazers_count"] for r in repos)
    tiles = [("REPOSITÓRIOS", len(repos), "públicos"), ("ESTRELAS", stars, "recebidas"), ("CONTRIBUIÇÕES", total, "últimos 12 meses"),
             ("DIAS ATIVOS", active, f"de {len(days)} dias"), ("MAIOR SEQUÊNCIA", best, f"dias seguidos · atual {cur}")]
    gap = 15
    tw = (W - 48 - 4 * gap) / 5
    tl = ""
    for i, (lab, val, hint) in enumerate(tiles):
        x = 24 + i * (tw + gap)
        tl += (f'{pane(x, 78, tw, 112, 22)}<text x="{x+20}" y="108" class="m" font-size="10" fill="{SKY}">{lab}</text>'
               f'<text x="{x+20}" y="156" font-size="44" font-weight="800" letter-spacing="-1.5" fill="{INK}">{val:,}</text>'
               f'<text x="{x+20}" y="180" font-size="12" fill="{MUTED}">{hint}</text>')

    # heatmap: colunas = semanas (domingo→sábado)
    ordered = sorted(days)
    first = date.fromisoformat(ordered[0])
    offset = (first.weekday() + 1) % 7
    cell, step, x0, y0 = 16, 19.55, 98, 252
    cells, months, seen = "", "", set()
    for d in ordered:
        idx = (date.fromisoformat(d) - first).days + offset
        col, row = divmod(idx, 7)
        n, lv = days[d]
        x, y = x0 + col * step, y0 + row * step
        op = ".07" if lv == 0 else "1"
        cells += (f'<rect class="c" style="animation-delay:{col*22}ms" x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4.5" '
                  f'fill="{LEVELS[lv]}" fill-opacity="{op}"><title>{d}: {n} contribuição(ões)</title></rect>')
        mk = d[:7]
        if row == 0 and mk not in seen and date.fromisoformat(d).day <= 7 or (row == 0 and not seen):
            seen.add(mk)
            months += f'<text x="{x}" y="{y0-12}" class="m" font-size="9" fill="{DIM}">{date.fromisoformat(d).strftime("%b").upper()}</text>'
    wd = "".join(f'<text x="{x0-16}" y="{y0+i*step+12}" text-anchor="end" font-size="9" class="m" fill="{DIM}">{t}</text>' for i, t in ((1, "SEG"), (3, "QUA"), (5, "SEX")))
    legend = "".join(f'<rect x="{1060+i*21}" y="{y0+7*step+14}" width="14" height="14" rx="4" fill="{LEVELS[i]}" fill-opacity="{".07" if i == 0 else "1"}"/>' for i in range(5))
    legend = (f'<text x="1050" y="{y0+7*step+26}" text-anchor="end" font-size="11" fill="{DIM}">menos</text>' + legend +
              f'<text x="{1060+5*21+6}" y="{y0+7*step+26}" font-size="11" fill="{DIM}">mais</text>')

    # linguagens
    tot = sum(langs.values()) or 1
    top = langs.most_common(5)
    bar, lg, x = "", "", 48
    bx, bw, by = 48, 1104, y0 + 7 * step + 96
    for name, v in top:
        w = bw * v / tot
        bar += f'<rect x="{bx}" y="{by}" width="{max(w-3,2):.1f}" height="12" rx="6" fill="{LANG_COLORS.get(name, VIOLET)}"/>'
        bx += w
        lg += (f'<circle cx="{x+5}" cy="{by+38}" r="5" fill="{LANG_COLORS.get(name, VIOLET)}"/>'
               f'<text x="{x+16}" y="{by+42}" font-size="13" fill="{INK}">{name}</text><text x="{x+16+len(name)*8+4}" y="{by+42}" font-size="13" fill="{DIM}">{100*v/tot:.1f}%</text>')
        x += 16 + len(name) * 8 + 8 + 56
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    css = "<style>@keyframes pop{from{opacity:0;transform:scale(.4)}}.c{transform-box:fill-box;transform-origin:center;animation:pop .5s cubic-bezier(.2,.8,.2,1) backwards}@media(prefers-reduced-motion:reduce){.c{animation:none}}</style>"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Atividade de {USER} no GitHub</title>
<desc id="d">{total} contribuições em {active} dias ativos nos últimos 12 meses, {len(repos)} repositórios públicos e linguagens mais usadas.</desc>
{STYLE}{css}{DEFS}
<clipPath id="cp"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<g clip-path="url(#cp)"><rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle class="b1" cx="120" cy="520" r="170" fill="{BLUE}" opacity=".3" filter="url(#blur)"/>
<circle class="b2" cx="1090" cy="40" r="180" fill="{VIOLET}" opacity=".26" filter="url(#blur)"/>
<text x="26" y="44" class="m" font-size="12" fill="{SKY}">ATIVIDADE NO GITHUB · ÚLTIMOS 12 MESES</text>
<text x="{W-26}" y="44" text-anchor="end" font-size="11" fill="{DIM}">@{USER} · atualizado em {now} UTC</text>
{tl}
{pane(24, 206, W-48, 220, 22)}{months}{wd}{cells}{legend}
<text x="48" y="{by-18}" class="m" font-size="10" fill="{SKY}">LINGUAGENS</text>{bar}{lg}
</g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="28" fill="none" stroke="url(#rim)"/></svg>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "stats.svg").write_text(render(*collect()), encoding="utf-8")
