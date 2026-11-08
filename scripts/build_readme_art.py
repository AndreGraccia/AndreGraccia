"""Gera as artes animadas do README em assets/readme/ (SVG com animação SMIL, que o GitHub renderiza em <img>).
Mesmo visual do site: fundo escuro, azul #2997ff, nome com sobrenome em serifa itálica, janelas com bolinhas macOS.
Uso: python scripts/build_readme_art.py
"""
import os
from html import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "readme")
os.makedirs(OUT, exist_ok=True)
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
SERIF = "'Instrument Serif',Georgia,'Times New Roman',serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Courier New',monospace"
BLUE = "#2997ff"

DEFS = f"""<defs>
<radialGradient id="glow" cx="50%" cy="0%" r="75%"><stop offset="0" stop-color="{BLUE}" stop-opacity=".38"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="glow2" cx="88%" cy="30%" r="45%"><stop offset="0" stop-color="#0071e3" stop-opacity=".28"/><stop offset="1" stop-color="#0071e3" stop-opacity="0"/></radialGradient>
<linearGradient id="sur" x1="0" x2="1"><stop offset="0" stop-color="#8ec9ff"/><stop offset=".55" stop-color="{BLUE}"/><stop offset="1" stop-color="#7aa7ff"/></linearGradient>
<linearGradient id="ul" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
</defs>"""


def dots(x, y):
    return "".join(f'<circle cx="{x + i * 20}" cy="{y}" r="6" fill="{c}"/>' for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")))


def fade(begin, dur=0.5):
    return f'<animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'


# ---------------------------------------------------------------- cabeçalho: o nome surge da esquerda para a direita, depois o sublinhado
header = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="320" viewBox="0 0 1000 320" role="img" aria-label="André Graccia, engenheiro de software backend em Java">
{DEFS}
<clipPath id="reveal"><rect x="0" y="0" width="0" height="320"><animate attributeName="width" from="0" to="1000" begin="0.4s" dur="2.4s" fill="freeze"/></rect></clipPath>
<rect width="1000" height="320" rx="22" fill="#0b0b0d"/>
<rect width="1000" height="320" rx="22" fill="url(#glow)"/><rect width="1000" height="320" rx="22" fill="url(#glow2)"/>
<rect x=".5" y=".5" width="999" height="319" rx="21.5" fill="none" stroke="#ffffff" stroke-opacity=".1"/>
<g opacity="0">{fade(0, .8)}
<rect x="338" y="36" width="324" height="34" rx="17" fill="#ffffff" fill-opacity=".08" stroke="#ffffff" stroke-opacity=".16"/>
<text x="500" y="58" text-anchor="middle" font-family="{MONO}" font-size="14" fill="#f5f5f7">Java · Python · Spring Boot</text></g>
<g clip-path="url(#reveal)">
<text x="500" y="168" text-anchor="middle" font-size="92" letter-spacing="-3" font-family="{SANS}" font-weight="500" fill="#f5f5f7">André <tspan font-family="{SERIF}" font-style="italic" font-weight="400" font-size="108" letter-spacing="-1" fill="url(#sur)">Graccia</tspan></text>
</g>
<path d="M300 190H700" stroke="url(#ul)" stroke-width="2.5" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" begin="2.8s" dur="1.4s" fill="freeze"/></path>
<g opacity="0">{fade(3.2, 1)}
<text x="500" y="250" text-anchor="middle" font-family="{SANS}" font-size="30" font-weight="500" fill="#f5f5f7">Engenheiro de software backend em <tspan fill="{BLUE}">Java</tspan></text>
<text x="500" y="286" text-anchor="middle" font-family="{SANS}" font-size="16" fill="#a1a1a6">APIs em Java e Spring Boot · automação de testes em Python · agentes de IA</text></g>
</svg>
"""

# ---------------------------------------------------------------- terminal da stack: cada linha entra uma a uma
LINES = [
    ("~/calc-juros", "./mvnw spring-boot:run", "Spring Boot", "Java 25 · API no ar, rotas de juros simples e compostos"),
    ("~/wall.ia", "docker compose up -d postgres", "Docker", "banco pronto na porta 5432"),
    ("~/wall.ia", 'psql -c "\\dt"', "PostgreSQL", "tabelas da carteira listadas"),
    ("~/qa/testes", "pytest -q", "Python", "26 testes passaram em 1,6s"),
    ("~/orbit", "n8n start && python agente.py", "n8n · LangChain", "workflows ativos, agente chamando as ferramentas"),
    ("~/orbit", "git push origin main", "Git · GitHub Actions", "build e testes rodando na pipeline"),
]


def terminal():
    h = 96 + len(LINES) * 62 + 20
    rows, t = "", 0.6
    for cwd, cmd, tag, out in LINES:
        y = 112 + LINES.index((cwd, cmd, tag, out)) * 62
        tag_w = 14 + len(tag) * 8
        rows += (f'<g opacity="0">{fade(round(t, 2), .5)}'
                 f'<text x="36" y="{y}" font-family="{MONO}" font-size="16" fill="#6cb6ff">{escape(cwd)}</text>'
                 f'<text x="{36 + len(cwd) * 9.6 + 12}" y="{y}" font-family="{MONO}" font-size="16" fill="#a1a1a6">$</text>'
                 f'<text x="{36 + len(cwd) * 9.6 + 32}" y="{y}" font-family="{MONO}" font-size="16" fill="#f5f5f7">{escape(cmd)}</text>'
                 f'<rect x="{964 - tag_w}" y="{y - 17}" width="{tag_w}" height="24" rx="12" fill="#ffffff" fill-opacity=".08" stroke="#ffffff" stroke-opacity=".12"/>'
                 f'<text x="{964 - tag_w / 2}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="#f5f5f7">{escape(tag)}</text>'
                 f'<text x="52" y="{y + 26}" font-family="{MONO}" font-size="14.5" fill="#a1a1a6"><tspan fill="#28c840">→</tspan> {escape(out)}</text></g>')
        t += 0.9
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{h}" viewBox="0 0 1000 {h}" role="img" aria-label="Terminal mostrando como uso Spring Boot, Docker, PostgreSQL, Python, n8n, LangChain, Git e GitHub Actions">
<rect width="1000" height="{h}" rx="18" fill="#161618"/><rect x=".5" y=".5" width="999" height="{h - 1}" rx="17.5" fill="none" stroke="#ffffff" stroke-opacity=".1"/>
{dots(30, 28)}<text x="104" y="33" font-family="{MONO}" font-size="13" fill="#a1a1a6">como eu uso cada coisa</text><text x="966" y="33" text-anchor="end" font-family="{MONO}" font-size="13" fill="#a1a1a6">zsh</text>
<path d="M0 54H1000" stroke="#ffffff" stroke-opacity=".08"/>
{rows}
</svg>
"""


# ---------------------------------------------------------------- janela de código: trecho real do JurosCalculator.java (recortado)
CODE = [
    ("50", "BigDecimal periodicRate = ratePercent", False),
    ("51", "    .divide(ONE_HUNDRED, CTX);", False),
    ("52", "BigDecimal factor = ONE.add(periodicRate);", True),
    ("53", "BigDecimal acc = factor.pow(periods, CTX);", False),
    ("54", "return principal.multiply(acc, CTX)", False),
    ("55", "    .setScale(2, HALF_UP);", False),
]


def code():
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
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="{h}" viewBox="0 0 600 {h}" role="img" aria-label="Trecho do JurosCalculator.java: juros compostos com BigDecimal">
<rect width="600" height="{h}" rx="16" fill="#1d1d1f"/><rect x=".5" y=".5" width="599" height="{h - 1}" rx="15.5" fill="none" stroke="#ffffff" stroke-opacity=".1"/>
{dots(26, 26)}<rect x="96" y="12" width="190" height="28" rx="8" fill="#ffffff" fill-opacity=".08"/><text x="110" y="31" font-family="{MONO}" font-size="13" fill="#f5f5f7">J  JurosCalculator.java</text>
<path d="M0 52H600" stroke="#ffffff" stroke-opacity=".08"/>
{rows}
<path d="M0 {foot - 4}H600" stroke="#ffffff" stroke-opacity=".08"/>
<g opacity="0">{fade(t + 0.2, .6)}<circle cx="28" cy="{foot + 24}" r="4" fill="{BLUE}"/><text x="44" y="{foot + 29}" font-family="{SANS}" font-size="14" fill="#a1a1a6">Regra: A = P × (1 + i)^n, tudo em BigDecimal.</text></g>
</svg>
"""


for name, svg in (("header.svg", header), ("terminal.svg", terminal()), ("code.svg", code())):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("ok", name)
