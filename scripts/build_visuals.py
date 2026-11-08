#!/usr/bin/env python3
"""Gera assets/hero.svg e assets/projects.svg na identidade do portfólio:
preto, brilho violeta na base, wordmark com cursor de bloco, mono em lavanda."""
import base64
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# Tokens (espelham styles.css; cores medidas nas artes da marca)
SANS = "'Inter Tight', Inter, 'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', ui-monospace, 'SFMono-Regular', Menlo, Consolas, monospace"
INK, MUTED, DIM = "#FFFFFF", "#B1AFBC", "#7F7A99"
SKY, VIOLET, BLUE = "#A88BF9", "#7C4DFF", "#5119D4"  # lavanda (rótulos), violeta, brilho de base
PANEL = "#10062B"

STYLE = f"""<style>
text{{font-family:{SANS}}}
.m{{font-family:{MONO};letter-spacing:.12em}}
@keyframes d1{{to{{transform:translate(40px,-14px)}}}}
@keyframes d2{{to{{transform:translate(-36px,10px)}}}}
@keyframes bl{{50%{{opacity:0}}}}
.b1{{animation:d1 14s ease-in-out infinite alternate}}
.b2{{animation:d2 17s ease-in-out infinite alternate}}
.cur{{animation:bl 1.1s steps(1) infinite}}
@media (prefers-reduced-motion:reduce){{.b1,.b2,.cur{{animation:none}}}}
</style>"""

DEFS = f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#000"/><stop offset="1" stop-color="#0A0420"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff" stop-opacity=".12"/><stop offset=".5" stop-color="#fff" stop-opacity=".03"/><stop offset="1" stop-color="{BLUE}" stop-opacity=".16"/></linearGradient>
<linearGradient id="rim" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#fff" stop-opacity=".5"/><stop offset=".4" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity=".16"/></linearGradient>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#fff"/><stop offset=".5" stop-color="#D8CCFF"/><stop offset="1" stop-color="{SKY}"/></linearGradient>
<radialGradient id="glow" cx=".5" cy="1" r=".75"><stop stop-color="{BLUE}"/><stop offset=".45" stop-color="#2C0D74"/><stop offset="1" stop-color="#190741" stop-opacity="0"/></radialGradient>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="55"/></filter>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="18" stdDeviation="16" flood-color="#000" flood-opacity=".6"/></filter>
</defs>"""


def icon(name):
    data = base64.b64encode((ROOT / f"assets/icons/{name}.svg").read_bytes()).decode()
    return f"data:image/svg+xml;base64,{data}"


def pane(x, y, w, h, r):
    """Painel de vidro: preenchimento, aro de luz e sombra."""
    return (f'<g filter="url(#sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{PANEL}" fill-opacity=".55"/></g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#glass)"/>'
            f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="url(#rim)"/>')


def hero():
    W, H = 1200, 320
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">andré graccia — Desenvolvedor backend Java</title>
<desc id="d">Software que não pode falhar. Backend Java, Spring Boot, Python e agentes de IA.</desc>
{STYLE}{DEFS}
<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="#000"/>
<ellipse class="b1" cx="600" cy="352" rx="640" ry="190" fill="url(#glow)"/>
<ellipse class="b2" cx="600" cy="380" rx="360" ry="110" fill="{BLUE}" opacity=".55" filter="url(#blur)"/>
<text x="600" y="62" text-anchor="middle" class="m" font-size="11" fill="{DIM}">~/ANDRE</text>
<text x="244" y="170" font-size="104" font-weight="800" fill="{INK}" textLength="640" lengthAdjust="spacingAndGlyphs">andré graccia</text>
<rect class="cur" x="906" y="102" width="28" height="68" rx="2" fill="{INK}"/>
<text x="600" y="224" text-anchor="middle" font-size="22" fill="{MUTED}">Desenvolvedor backend Java. Software que não pode falhar.</text>
<text x="600" y="262" text-anchor="middle" class="m" font-size="13" fill="{SKY}">java  /  spring boot  /  python  /  langchain</text>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="28" fill="none" stroke="url(#rim)"/>
</svg>
'''


PROJECTS = [
    ("conciliador", "conciliador.", ["Sua venda e seu extrato,", "finalmente de acordo."], "java 21  /  spring boot  /  postgresql", ["java", "spring", "postgresql"]),
    ("orbit-ia", "orbit.ia", ["Orquestrador de agentes de IA com", "React, n8n, LangChain e OpenRouter."], "react  /  n8n  /  langchain  /  vite", ["react", "n8n", "langchain"]),
    ("wall-ia", "wall.ia", ["Gestão financeira em Java 17 e Spring Boot,", "com JWT e PostgreSQL em Docker."], "java 17  /  spring security  /  docker", ["java", "spring", "docker"]),
    ("calculadora-de-juros", "calculadora de juros", ["Serviço Java integrado às APIs do Banco", "Central: Selic, IPCA e CDI em tempo real."], "java  /  spring boot  /  maven", ["java", "spring", "maven"]),
]


def projects():
    W, cw, ch, gap = 1200, 576, 262, 24
    H = 24 + 2 * ch + gap + 24
    cards = []
    for i, (slug, name, desc, stack, icons) in enumerate(PROJECTS):
        x, y = 24 + (i % 2) * (cw + gap), 24 + (i // 2) * (ch + gap)
        dots = "".join(f'<circle cx="{x+30+k*18}" cy="{y+30}" r="5.5" fill="{c}"/>' for k, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")))
        ic = "".join(f'<image href="{icon(n)}" x="{x+28+k*44}" y="{y+ch-62}" width="36" height="36"/>' for k, n in enumerate(icons))
        lines = "".join(f'<text x="{x+28}" y="{y+138+k*23}" font-size="16" fill="{MUTED}">{escape(l)}</text>' for k, l in enumerate(desc))
        cards.append(f'''{pane(x, y, cw, ch, 24)}
<rect x="{x}" y="{y+52}" width="{cw}" height="1" fill="#fff" fill-opacity=".1"/>
{dots}<text x="{x+cw/2}" y="{y+34}" text-anchor="middle" class="m" font-size="10" fill="{DIM}">~/andre/projetos/{slug}</text>
<text x="{x+28}" y="{y+104}" font-size="40" font-weight="800" letter-spacing="-2.2" fill="{INK}">{escape(name)}</text>
{lines}
<text x="{x+28}" y="{y+ch-78}" class="m" font-size="11" fill="{SKY}">{escape(stack)}</text>{ic}''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Projetos</title>
<desc id="d">Conciliador, Orbit.IA, wall.ia e Calculadora de Juros, com descrição e tecnologias de cada um.</desc>
{STYLE}{DEFS}
<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="#000"/>
<ellipse class="b1" cx="600" cy="{H+30}" rx="700" ry="200" fill="url(#glow)"/>
<ellipse class="b2" cx="1100" cy="40" rx="260" ry="140" fill="{BLUE}" opacity=".3" filter="url(#blur)"/>
{''.join(cards)}
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="28" fill="none" stroke="url(#rim)"/>
</svg>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "hero.svg").write_text(hero(), encoding="utf-8")
    (OUT / "projects.svg").write_text(projects(), encoding="utf-8")
