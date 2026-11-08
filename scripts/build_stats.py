"""Gera assets/activity.svg (contribuições por dia, 30 dias) e assets/langs.svg (linguagens por bytes)
no mesmo visual do site: janela escura com bolinhas macOS, azul #2997ff, Geist e Geist Mono embutidas,
barras que crescem uma a uma (SMIL, que o GitHub renderiza em <img>).
Uso: GITHUB_TOKEN=... python scripts/build_stats.py [usuario] [--out DIR] [--demo]
Sem token só langs.svg é gerado (a API de contribuições exige autenticação). --demo usa dados fictícios
na atividade, só para ver o desenho localmente.
"""
import base64, json, os, random, sys, urllib.request
from datetime import date, timedelta
from html import escape

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
USER = ARGS[0] if ARGS else "AndreGraccia"
OUT = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "assets"
DEMO = "--demo" in sys.argv
TOKEN = os.environ.get("GITHUB_TOKEN")
HERE = os.path.dirname(os.path.abspath(__file__))
BLUE, MUTE = "#2997ff", "#a1a1a6"
SANS, MONO = "Geist,Helvetica,Arial,sans-serif", "'Geist Mono',ui-monospace,Menlo,Consolas,monospace"


def fonts():
    css = ""
    for f, fam in (("geist-500", "Geist"), ("geist-mono-400", "Geist Mono")):
        b64 = base64.b64encode(open(os.path.join(HERE, "fonts", f + ".woff2"), "rb").read()).decode()
        css += f"@font-face{{font-family:'{fam}';font-weight:{'500' if fam == 'Geist' else '400'};src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
    return f"<style>{css}</style>"


def api(url, body=None):
    req = urllib.request.Request(url, json.dumps(body).encode() if body else None)
    req.add_header("User-Agent", "profile-stats")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


PT = dict(lang_sub="linguagens mais usadas nos repositórios públicos", lang_title="linguagens", lang_tag="por bytes de código", act_sub="contribuições por dia",
          act_title="atividade", act_tag="últimos 30 dias", total="no total", mx="máximo em um dia", active="dias ativos", streak="dias seguidos", fmt="%d/%m")
EN = dict(lang_sub="most used languages in public repositories", lang_title="languages", lang_tag="by bytes of code", act_sub="contributions per day",
          act_title="activity", act_tag="last 30 days", total="total", mx="best single day", active="active days", streak="day streak", fmt="%m/%d")
L = PT


def window(w, h, title, tag, body):
    dots = "".join(f'<circle cx="{28 + i * 20}" cy="27" r="6" fill="{c}"/>' for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">{fonts()}'
            '<defs><linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ec9ff"/><stop offset="1" stop-color="#2997ff"/></linearGradient>'
            '<linearGradient id="seg" x1="0" x2="1"><stop offset="0" stop-color="#2997ff"/><stop offset="1" stop-color="#8ec9ff"/></linearGradient>'
            '<radialGradient id="glow" cx="50%" cy="0%" r="80%"><stop offset="0" stop-color="#2997ff" stop-opacity=".18"/><stop offset="1" stop-color="#2997ff" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="{w}" height="{h}" rx="18" fill="#161618"/><rect width="{w}" height="{h}" rx="18" fill="url(#glow)"/>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="17.5" fill="none" stroke="#fff" stroke-opacity=".1"/>'
            f'{dots}<text x="100" y="32" font-family="{MONO}" font-size="13" fill="{MUTE}">{escape(title)}</text>'
            f'<text x="{w - 28}" y="32" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTE}">{escape(tag)}</text>'
            f'<path d="M0 54H{w}" stroke="#fff" stroke-opacity=".08"/>{body}</svg>')


def grow(delay, dur=0.7):
    return f'begin="{delay:.2f}s" dur="{dur}s" fill="freeze" calcMode="spline" keySplines=".2 .7 .2 1" keyTimes="0;1"'


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
    W, X0, X1 = 1000, 36, 964
    shades = ["#2997ff", "#0071e3", "#5ab0ff", "#0b4fa8", "#8ec9ff", "#3a6ea5"]
    seg, x, rows = "", X0, ""
    for i, (lang, n) in enumerate(top):
        pct = n / s * 100
        sw = (X1 - X0) * n / s
        seg += (f'<rect x="{x:.1f}" y="82" width="0" height="14" fill="{shades[i]}"><animate attributeName="width" from="0" to="{max(sw - 2, 2):.1f}" {grow(0.2 + i * 0.12)}/></rect>')
        x += sw
        y = 148 + i * 38
        rows += (f'<g><circle cx="{X0 + 5}" cy="{y - 5}" r="5" fill="{shades[i]}"/>'
                 f'<text x="{X0 + 22}" y="{y}" font-family="{MONO}" font-size="15" fill="#f5f5f7">{escape(lang)}</text>'
                 f'<rect x="260" y="{y - 12}" width="600" height="8" rx="4" fill="#fff" fill-opacity=".07"/>'
                 f'<rect x="260" y="{y - 12}" width="0" height="8" rx="4" fill="url(#seg)"><animate attributeName="width" from="0" to="{max(pct / (top[0][1] / s * 100) * 600, 8):.0f}" {grow(0.5 + i * 0.12, 1)}/></rect>'
                 f'<text x="{X1}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="14" fill="{MUTE}">{pct:.1f}%</text></g>')
    h = 148 + len(top) * 38 + 18
    body = (f'<text x="{X0}" y="72" font-family="{SANS}" font-size="15" fill="{MUTE}" font-weight="500">{L["lang_sub"]}</text>'
            f'<clipPath id="r"><rect x="{X0}" y="82" width="{X1 - X0}" height="14" rx="7"/></clipPath><g clip-path="url(#r)">{seg}</g>{rows}')
    return window(W, h, L["lang_title"], L["lang_tag"], body)


def activity_data():
    start = date.today() - timedelta(days=29)
    if DEMO:
        random.seed(7)
        return start, [random.choice([0, 0, 1, 2, 3, 5, 8]) for _ in range(30)]
    q = ('query($u:String!,$f:DateTime!){user(login:$u){contributionsCollection(from:$f){'
         'contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}')
    d = api("https://api.github.com/graphql", {"query": q, "variables": {"u": USER, "f": f"{start}T00:00:00Z"}})
    days = {x["date"]: x["contributionCount"]
            for w in d["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
            for x in w["contributionDays"]}
    return start, [days.get(str(start + timedelta(days=i)), 0) for i in range(30)]


def activity_svg():
    start, vals = activity_data()
    total, mx, active = sum(vals), max(vals), sum(1 for v in vals if v)
    streak = 0
    for v in reversed(vals):
        if not v:
            break
        streak += 1
    W, H, X0, X1, TOP, BASE = 1000, 430, 36, 964, 220, 360
    mxv = max(mx, 1)
    step = (X1 - X0) / 30
    bw = step - 8
    bars = ""
    for i, v in enumerate(vals):
        hh = max(v / mxv * (BASE - TOP), 5)
        x = X0 + i * step
        last = i == 29
        fill = "url(#bar)" if last else "#fff"
        op = "" if last else ' fill-opacity=".14"'
        bars += (f'<rect x="{x:.1f}" y="{BASE}" width="{bw:.1f}" height="0" rx="4" fill="{fill}"{op}>'
                 f'<animate attributeName="height" from="0" to="{hh:.1f}" {grow(0.3 + i * 0.04)}/>'
                 f'<animate attributeName="y" from="{BASE}" to="{BASE - hh:.1f}" {grow(0.3 + i * 0.04)}/></rect>')
    grid = "".join(f'<path d="M{X0} {y}H{X1}" stroke="#fff" stroke-opacity=".06"/>' for y in (TOP, (TOP + BASE) / 2, BASE))
    labels = "".join(f'<text x="{X0 + i * step + bw / 2:.1f}" y="{BASE + 24}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTE}">{(start + timedelta(days=i)).strftime(L['fmt'])}</text>' for i in (0, 7, 14, 21, 29))

    def stat(x, big, small):
        return (f'<text x="{x}" y="150" font-family="{SANS}" font-weight="500" font-size="52" letter-spacing="-2" fill="#f5f5f7">{big}</text>'
                f'<text x="{x}" y="178" font-family="{MONO}" font-size="13" fill="{MUTE}">{small}</text>')
    body = (f'<text x="{X0}" y="86" font-family="{SANS}" font-size="15" fill="{MUTE}" font-weight="500">{L["act_sub"]}</text>'
            + stat(X0, total, L["total"])
            + stat(X0 + 220, mx, L["mx"])
            + stat(X0 + 470, active, L["active"])
            + stat(X0 + 680, streak, L["streak"])
            + grid + bars + labels)
    return window(W, H, L["act_title"], L["act_tag"], body)


os.makedirs(OUT, exist_ok=True)
for suf, L in (("", PT), ("-en", EN)):
    open(os.path.join(OUT, f"langs{suf}.svg"), "w", encoding="utf-8").write(langs_svg())
    if TOKEN or DEMO:
        open(os.path.join(OUT, f"activity{suf}.svg"), "w", encoding="utf-8").write(activity_svg())
    else:
        print("sem GITHUB_TOKEN: activity não gerado")
