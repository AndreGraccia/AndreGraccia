"""Gera as artes animadas do README em assets/readme/ (SVG com animação SMIL, que o GitHub renderiza em <img>).
Mesmo visual do site: fundo escuro, azul #2997ff, "André" em Geist e "Graccia" em Instrument Serif itálico,
janelas com bolinhas macOS. As fontes (scripts/fonts/*.woff2, latin, licença OFL) vão embutidas no SVG,
porque o GitHub não carrega fontes externas dentro de imagens.
Uso: python scripts/build_readme_art.py
"""
import base64
import os
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "readme")
os.makedirs(OUT, exist_ok=True)
BLUE = "#2997ff"
SANS, SERIF, MONO = "Geist,Helvetica,Arial,sans-serif", "'Instrument Serif',Georgia,serif", "'Geist Mono',ui-monospace,Menlo,Consolas,monospace"


def font_css(*files):
    faces = {
        "geist-500": ("Geist", "normal", "500"),
        "geist-mono-400": ("Geist Mono", "normal", "400"),
        "instrument-serif-italic": ("Instrument Serif", "italic", "400"),
    }
    css = ""
    for f in files:
        fam, style, weight = faces[f]
        b64 = base64.b64encode(open(os.path.join(HERE, "fonts", f + ".woff2"), "rb").read()).decode()
        css += f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
    return f"<style>{css}</style>"


def dots(x, y):
    return "".join(f'<circle cx="{x + i * 20}" cy="{y}" r="6" fill="{c}"/>' for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")))


def fade(begin, dur=0.5):
    return f'<animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'


DEFS = f"""<defs>
<radialGradient id="glow" cx="50%" cy="0%" r="75%"><stop offset="0" stop-color="{BLUE}" stop-opacity=".38"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="glow2" cx="88%" cy="30%" r="45%"><stop offset="0" stop-color="#0071e3" stop-opacity=".28"/><stop offset="1" stop-color="#0071e3" stop-opacity="0"/></radialGradient>
<linearGradient id="sur" x1="0" x2="1"><stop offset="0" stop-color="#8ec9ff"/><stop offset=".55" stop-color="{BLUE}"/><stop offset="1" stop-color="#7aa7ff"/></linearGradient>
<linearGradient id="ul" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<linearGradient id="wipe" x1="0" x2="1"><stop offset=".45" stop-color="#fff"/><stop offset=".55" stop-color="#000"/></linearGradient>
<mask id="reveal" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="320"><rect x="-1250" y="0" width="2400" height="320" fill="url(#wipe)"><animateTransform attributeName="transform" type="translate" from="0 0" to="1300 0" begin="0.4s" dur="2.4s" fill="freeze" calcMode="linear"/></rect></mask>
</defs>"""

# ---------------------------------------------------------------- cabeçalho: igual ao nome do site (surge da esquerda para a direita, sublinhado depois)
def header(t):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="320" viewBox="0 0 1000 320" role="img" aria-label="André Graccia, {t['role']}">
{font_css("geist-500", "geist-mono-400", "instrument-serif-italic")}
{DEFS}
<rect width="1000" height="320" rx="22" fill="#0b0b0d"/>
<rect width="1000" height="320" rx="22" fill="url(#glow)"/><rect width="1000" height="320" rx="22" fill="url(#glow2)"/>
<rect x=".5" y=".5" width="999" height="319" rx="21.5" fill="none" stroke="#ffffff" stroke-opacity=".1"/>
<g opacity="0">{fade(0, .8)}
<rect x="338" y="36" width="324" height="34" rx="17" fill="#ffffff" fill-opacity=".08" stroke="#ffffff" stroke-opacity=".16"/>
<text x="500" y="58" text-anchor="middle" font-family="{MONO}" font-size="14" fill="#f5f5f7">Java · Python · Spring Boot</text></g>
<g mask="url(#reveal)">
<text x="500" y="168" text-anchor="middle" font-size="92" letter-spacing="-3.2" font-family="{SANS}" font-weight="500" fill="#f5f5f7">André <tspan font-family="{SERIF}" font-style="italic" font-weight="400" font-size="112" letter-spacing="-1" fill="url(#sur)">Graccia</tspan></text>
</g>
<path d="M300 190H700" stroke="url(#ul)" stroke-width="2.5" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" begin="2.8s" dur="1.4s" fill="freeze"/></path>
<g opacity="0">{fade(3.2, 1)}
<text x="500" y="250" text-anchor="middle" font-family="{SANS}" font-size="30" font-weight="500" letter-spacing="-.6" fill="#f5f5f7">{t['h1']} <tspan fill="{BLUE}">{t['hl']}</tspan></text>
<text x="500" y="286" text-anchor="middle" font-family="{SANS}" font-size="16" fill="#a1a1a6">{t['sub']}</text></g>
</svg>
"""


# ---------------------------------------------------------------- terminais (stack e um por projeto): cada linha entra uma a uma
def terminal(title, lines, width=1000, fs=16):
    cw = fs * 0.6
    step = fs * 3.9
    h = int(90 + len(lines) * step)
    rows, t = "", 0.6
    for i, (cwd, cmd, tag, out) in enumerate(lines):
        y = 106 + i * step
        tag_w = 16 + len(tag) * (fs * 0.5)
        x_cmd = 30 + len(cwd) * cw + 14 + cw * 2
        rows += (f'<g opacity="0">{fade(round(t, 2), .5)}'
                 f'<text x="30" y="{y}" font-family="{MONO}" font-size="{fs}" fill="#6cb6ff">{escape(cwd)}</text>'
                 f'<text x="{30 + len(cwd) * cw + 14}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="#a1a1a6">$</text>'
                 f'<text x="{x_cmd}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="#f5f5f7" xml:space="preserve">{escape(cmd)}</text>'
                 f'<rect x="{width - 28 - tag_w}" y="{y - fs * 1.05}" width="{tag_w}" height="{fs * 1.5}" rx="{fs * .75}" fill="#ffffff" fill-opacity=".08" stroke="#ffffff" stroke-opacity=".12"/>'
                 f'<text x="{width - 28 - tag_w / 2}" y="{y - 1}" text-anchor="middle" font-family="{MONO}" font-size="{fs * .78}" fill="#f5f5f7">{escape(tag)}</text>'
                 f'<text x="46" y="{y + fs * 1.6}" font-family="{MONO}" font-size="{fs * .9}" fill="#a1a1a6"><tspan fill="#28c840">→</tspan> {escape(out)}</text></g>')
        t += 0.9
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{h}" viewBox="0 0 {width} {h}" role="img" aria-label="{escape(title)}: {escape('; '.join(c for _, c, _, _ in lines))}">
{font_css("geist-mono-400")}
<rect width="{width}" height="{h}" rx="18" fill="#161618"/><rect x=".5" y=".5" width="{width - 1}" height="{h - 1}" rx="17.5" fill="none" stroke="#ffffff" stroke-opacity=".1"/>
{dots(28, 27)}<text x="100" y="32" font-family="{MONO}" font-size="13" fill="#a1a1a6">{escape(title)}</text><text x="{width - 28}" y="32" text-anchor="end" font-family="{MONO}" font-size="13" fill="#a1a1a6">zsh</text>
<path d="M0 52H{width}" stroke="#ffffff" stroke-opacity=".08"/>
{rows}
</svg>
"""


STACK = [
    ("~/calc-juros", "./mvnw spring-boot:run", "Spring Boot", "Java 25 · API no ar, rotas de juros simples e compostos"),
    ("~/wall.ia", "docker compose up -d postgres", "Docker", "banco pronto na porta 5432"),
    ("~/wall.ia", 'psql -c "\\dt"', "PostgreSQL", "tabelas da carteira listadas"),
    ("~/qa/testes", "pytest -q", "Python", "26 testes passaram em 1,6s"),
    ("~/orbit", "docker compose up -d", "n8n · LangChain", "n8n no ar na porta 5678, agente pronto"),
    ("~/orbit", "git push origin main", "Git · GitHub Actions", "build e testes rodando na pipeline"),
]
WALL = [
    ("~/wall.ia", "docker compose up -d", "Docker", "banco no ar"),
    ("~/wall.ia", "./mvnw spring-boot:run", "Spring Boot", "API no ar com Spring Security e JWT"),
    ("~/wall.ia", "./mvnw test", "JUnit", "testes passaram"),
]
ORBIT = [
    ("~/orbit", "docker compose up -d", "n8n", "n8n e PostgreSQL no ar"),
    ("~/orbit/frontend", "npm run dev", "React", "interface em localhost:5173"),
    ("~/orbit", "curl -X POST …/webhook/orbit-chat", "n8n", "o agente devolveu a resposta"),
]

STACK_EN = [
    ("~/calc-juros", "./mvnw spring-boot:run", "Spring Boot", "Java 25 · API up, simple and compound interest routes"),
    ("~/wall.ia", "docker compose up -d postgres", "Docker", "database ready on port 5432"),
    ("~/wall.ia", 'psql -c "\\dt"', "PostgreSQL", "wallet tables listed"),
    ("~/qa/tests", "pytest -q", "Python", "26 tests passed in 1.6s"),
    ("~/orbit", "docker compose up -d", "n8n · LangChain", "n8n up on port 5678, agent ready"),
    ("~/orbit", "git push origin main", "Git · GitHub Actions", "build and tests running in the pipeline"),
]
WALL_EN = [
    ("~/wall.ia", "docker compose up -d", "Docker", "database up"),
    ("~/wall.ia", "./mvnw spring-boot:run", "Spring Boot", "API up with Spring Security and JWT"),
    ("~/wall.ia", "./mvnw test", "JUnit", "tests passed"),
]
ORBIT_EN = [
    ("~/orbit", "docker compose up -d", "n8n", "n8n and PostgreSQL up"),
    ("~/orbit/frontend", "npm run dev", "React", "interface on localhost:5173"),
    ("~/orbit", "curl -X POST …/webhook/orbit-chat", "n8n", "the agent returned the answer"),
]

# ---------------------------------------------------------------- janela de código: trecho real do JurosCalculator.java (recortado)
CODE = [
    ("50", "BigDecimal periodicRate = ratePercent", False),
    ("51", "    .divide(ONE_HUNDRED, CTX);", False),
    ("52", "BigDecimal factor = ONE.add(periodicRate);", True),
    ("53", "BigDecimal acc = factor.pow(periods, CTX);", False),
    ("54", "return principal.multiply(acc, CTX)", False),
    ("55", "    .setScale(2, HALF_UP);", False),
]


def code(hint, aria):
    h = 70 + len(CODE) * 30 + 64
    rows, t = "", 0.5
    for i, (n, line, mark) in enumerate(CODE):
        y = 94 + i * 30
        bg = f'<rect x="1" y="{y - 20}" width="598" height="28" fill="{BLUE}" fill-opacity=".14"/><rect x="1" y="{y - 20}" width="3" height="28" fill="{BLUE}"/>' if mark else ""
        rows += (f'<g opacity="0">{fade(round(t, 2), .4)}{bg}'
                 f'<text x="28" y="{y}" font-family="{MONO}" font-size="14" fill="#6e6e73">{n}</text>'
                 f'<text x="64" y="{y}" font-family="{MONO}" font-size="15" fill="#f5f5f7" xml:space="preserve">{escape(line)}</text></g>')
        t += 0.45
    foot = 94 + len(CODE) * 30
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="{h}" viewBox="0 0 600 {h}" role="img" aria-label="{escape(aria)}">
{font_css("geist-500", "geist-mono-400")}
<rect width="600" height="{h}" rx="16" fill="#1d1d1f"/><rect x=".5" y=".5" width="599" height="{h - 1}" rx="15.5" fill="none" stroke="#ffffff" stroke-opacity=".1"/>
{dots(26, 26)}<rect x="96" y="12" width="190" height="28" rx="8" fill="#ffffff" fill-opacity=".08"/><text x="110" y="31" font-family="{MONO}" font-size="13" fill="#f5f5f7">J  JurosCalculator.java</text>
<path d="M0 52H600" stroke="#ffffff" stroke-opacity=".08"/>
{rows}
<path d="M0 {foot - 4}H600" stroke="#ffffff" stroke-opacity=".08"/>
<g opacity="0">{fade(t + 0.2, .6)}<circle cx="28" cy="{foot + 24}" r="4" fill="{BLUE}"/><text x="44" y="{foot + 29}" font-family="{SANS}" font-size="14" fill="#a1a1a6">{escape(hint)}</text></g>
</svg>
"""


LANGS = {
    "": dict(role="engenheiro de software Java em formação", h1="Engenheiro de software Java", hl="em formação", sub="APIs em Java e Spring Boot · interfaces em React · testes em Python · agentes de IA",
             stack=STACK, wall=WALL, orbit=ORBIT, title="como eu uso cada coisa", hint="Regra: A = P × (1 + i)^n, tudo em BigDecimal.",
             aria="Trecho do JurosCalculator.java: juros compostos com BigDecimal",
             links=(("portfolio", "Portfólio"), ("curriculo", "Currículo"), ("email", "E-mail"), ("linkedin", "LinkedIn"))),
    "-en": dict(role="Java software engineer in training", h1="Java software engineer", hl="in training", sub="Java and Spring Boot APIs · React interfaces · Python tests · AI agents",
                stack=STACK_EN, wall=WALL_EN, orbit=ORBIT_EN, title="how I use each thing", hint="Rule: A = P × (1 + i)^n, all in BigDecimal.",
                aria="Excerpt of JurosCalculator.java: compound interest with BigDecimal",
                links=(("portfolio", "Portfolio"), ("curriculo", "Resume"), ("email", "Email"), ("linkedin", "LinkedIn"))),
}
for suf, t in LANGS.items():
    for name, svg in ((f"header{suf}.svg", header(t)), (f"terminal{suf}.svg", terminal(t["title"], t["stack"])), (f"code{suf}.svg", code(t["hint"], t["aria"])),
                      (f"wall{suf}.svg", terminal("wall.ia", t["wall"], 600, 14.5)), (f"orbit{suf}.svg", terminal("Orbit.IA", t["orbit"], 600, 14.5))):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print("ok", name, len(svg) // 1024, "KB")

# ---------------------------------------------------------------- botões de link do README (ícone + rótulo; cada um vai dentro de um <a>)
ICONS = {
    "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "portfolio": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/>',
    "curriculo": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 11v6M8 7.5v.01M12 17v-6m0 3c0-2 1.2-3 3-3s2 1.2 2 3v3"/>',
}


def link_pill(icon, label):
    w = int(58 + len(label) * 9.4)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="44" viewBox="0 0 {w} 44" role="img" aria-label="{escape(label)}">{font_css("geist-500")}'
            f'<rect x=".5" y=".5" width="{w - 1}" height="43" rx="21.5" fill="#161618" stroke="#ffffff" stroke-opacity=".16"/>'
            f'<g transform="translate(16 10)" fill="none" stroke="{BLUE}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>'
            f'<text x="46" y="28" font-family="{SANS}" font-size="15" font-weight="500" fill="#f5f5f7">{escape(label)}</text></svg>\n')


for suf, t in LANGS.items():
    for icon, label in t["links"]:
        with open(os.path.join(OUT, f"link-{icon}{suf}.svg"), "w", encoding="utf-8") as f:
            f.write(link_pill(icon, label))
        print("ok", f"link-{icon}{suf}.svg")
