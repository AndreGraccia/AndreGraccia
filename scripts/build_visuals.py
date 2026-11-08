#!/usr/bin/env python3
"""Gera assets/hero.svg e assets/projects.svg (liquid glass, tipografia e paleta únicas)."""
import base64
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# Design tokens (espelham o site: styles.css)
SANS = "Inter, 'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, 'SFMono-Regular', Menlo, Consolas, monospace"
INK, MUTED, DIM = "#F3F5FF", "#B4B9D6", "#7C83A6"
SKY, VIOLET, BLUE = "#78CFFF", "#9C8BFF", "#4F6BFF"

STYLE = f"""<style>
text{{font-family:{SANS}}}
.m{{font-family:{MONO};letter-spacing:.14em}}
@keyframes d1{{to{{transform:translate(40px,22px)}}}}
@keyframes d2{{to{{transform:translate(-36px,-18px)}}}}
@keyframes fl{{50%{{transform:translateY(-6px)}}}}
.b1{{animation:d1 14s ease-in-out infinite alternate}}
.b2{{animation:d2 17s ease-in-out infinite alternate}}
.fl{{animation:fl 6s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{.b1,.b2,.fl{{animation:none}}}}
</style>"""

DEFS = f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#070914"/><stop offset="1" stop-color="#0D1124"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff" stop-opacity=".16"/><stop offset=".5" stop-color="#fff" stop-opacity=".04"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".12"/></linearGradient>
<linearGradient id="rim" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fff" stop-opacity=".55"/><stop offset=".4" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity=".18"/></linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{SKY}"/><stop offset=".6" stop-color="{VIOLET}"/><stop offset="1" stop-color="#E8A6FF"/></linearGradient>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="18" stdDeviation="16" flood-color="#000" flood-opacity=".5"/></filter>
</defs>"""


def icon(name):
    data = base64.b64encode((ROOT / f"assets/icons/{name}.svg").read_bytes()).decode()
    return f"data:image/svg+xml;base64,{data}"


def pane(x, y, w, h, r):
    """Painel de vidro: preenchimento, aro de luz e sombra."""
    return (f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#glass)"/></g>'
            f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="url(#rim)"/>')


def pill(x, y, text, w):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="15" fill="#fff" fill-opacity=".07" stroke="#fff" stroke-opacity=".2"/>'
            f'<text x="{x+w/2}" y="{y+19.5}" text-anchor="middle" class="m" font-size="11" fill="{INK}">{escape(text)}</text>')


def hero():
    W, H = 1200, 380
    tags = [("JAVA", 70), ("SPRING BOOT", 122), ("PYTHON", 90), ("AGENTES DE IA", 134)]
    x, pills = 64, []
    for t, w in tags:
        pills.append(pill(x, 296, t, w))
        x += w + 10
    tiles = [("java", 0, 0), ("spring", 1, 0), ("postgresql", 2, 0), ("python", 0, 1), ("docker", 1, 1), ("langchain", 2, 1)]
    ts = []
    for i, (n, c, r) in enumerate(tiles):
        tx, ty = 820 + c * 98, 112 + r * 98
        ts.append(f'<g class="fl" style="animation-delay:{-i*.9}s"><rect x="{tx}" y="{ty}" width="82" height="82" rx="22" fill="url(#glass)" stroke="url(#rim)"/>'
                  f'<image href="{icon(n)}" x="{tx+16}" y="{ty+16}" width="50" height="50"/></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">André Graccia — Desenvolvedor Backend Java e Engenheiro de IA</title>
<desc id="d">Banner com nome, função e ícones das principais tecnologias.</desc>
{STYLE}{DEFS}
<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle class="b1" cx="180" cy="40" r="170" fill="{BLUE}" opacity=".45" filter="url(#blur)"/>
<circle class="b2" cx="1010" cy="300" r="190" fill="{VIOLET}" opacity=".38" filter="url(#blur)"/>
<circle class="b1" cx="640" cy="400" r="130" fill="{SKY}" opacity=".22" filter="url(#blur)"/>
{pane(792, 84, 320, 212, 30)}
{''.join(ts)}
<text x="64" y="86" class="m" font-size="12" fill="{SKY}">ENGENHEIRO DE SOFTWARE NA CIELO · SÃO PAULO, BR</text>
<rect x="64" y="104" width="52" height="3" rx="1.5" fill="url(#acc)"/>
<text x="62" y="186" font-size="68" font-weight="800" letter-spacing="-2.5" fill="{INK}">André Graccia</text>
<text x="64" y="232" font-size="24" font-weight="600" letter-spacing="-.4" fill="{INK}">Backend Java &amp; Engenheiro de Sistemas de IA</text>
<text x="64" y="264" font-size="16" fill="{MUTED}">Spring Boot, automação de testes em Python e agentes de IA.</text>
{''.join(pills)}
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="28" fill="none" stroke="url(#rim)"/>
</svg>
'''


PROJECTS = [
    ("01", "Orbit.IA", "2026 · AGENTES DE IA", ["Orquestrador de agentes com React/Vite,", "n8n, LangChain e OpenRouter."], ["react", "n8n", "langchain"], "#E8A6FF"),
    ("02", "wall.ia", "2025 · FULL-STACK", ["Gestão financeira em Java 17 e Spring Boot,", "com JWT e PostgreSQL em Docker."], ["java", "spring", "postgresql"], VIOLET),
    ("03", "Calculadora de Juros", "2025 · APIS OFICIAIS", ["Serviço Java integrado às APIs do Banco", "Central: Selic, IPCA e CDI em tempo real."], ["java", "spring", "maven"], SKY),
]


def projects():
    W, H, cw, gap = 1200, 330, 368, 20
    cards = []
    for i, (n, name, tag, desc, stack, col) in enumerate(PROJECTS):
        x = 24 + i * (cw + gap)
        icons = ''.join(f'<image href="{icon(s)}" x="{x+28+j*46}" y="248" width="38" height="38"/>' for j, s in enumerate(stack))
        lines = ''.join(f'<text x="{x+28}" y="{176+k*22}" font-size="14" fill="{MUTED}">{escape(l)}</text>' for k, l in enumerate(desc))
        cards.append(f'''{pane(x, 24, cw, 282, 26)}
<rect x="{x+28}" y="50" width="34" height="3" rx="1.5" fill="{col}"/>
<text x="{x+28}" y="82" class="m" font-size="11" fill="{col}">{n} / PROJETO</text>
<text x="{x+28}" y="124" font-size="28" font-weight="800" letter-spacing="-.8" fill="{INK}">{escape(name)}</text>
<text x="{x+28}" y="148" class="m" font-size="10" fill="{DIM}">{escape(tag)}</text>
{lines}{icons}''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Projetos selecionados</title>
<desc id="d">Calculadora de Juros, Wall.ia e Orbit.ia, com descrição e tecnologias de cada um.</desc>
{STYLE}{DEFS}
<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle class="b1" cx="200" cy="320" r="150" fill="{BLUE}" opacity=".35" filter="url(#blur)"/>
<circle class="b2" cx="1040" cy="40" r="160" fill="{VIOLET}" opacity=".32" filter="url(#blur)"/>
{''.join(cards)}
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="28" fill="none" stroke="url(#rim)"/>
</svg>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "hero.svg").write_text(hero(), encoding="utf-8")
    (OUT / "projects.svg").write_text(projects(), encoding="utf-8")
