#!/usr/bin/env python3
from pathlib import Path

Path("assets").mkdir(exist_ok=True)
groups = [
 ("BACKEND ENGINEERING", "Java 25  ·  Spring Boot  ·  REST APIs  ·  PostgreSQL  ·  Maven", "01"),
 ("AI & AUTOMATION", "Python  ·  n8n  ·  AI workflows  ·  API integration", "02"),
 ("CLOUD & DEV TOOLS", "AWS  ·  Docker  ·  Git  ·  GitHub  ·  Linux", "03"),
 ("FRONTEND", "React  ·  TypeScript  ·  JavaScript  ·  Vite", "04"),
]
cards=[]
for i,(title,items,num) in enumerate(groups):
    x=24+(i%2)*562
    y=22+(i//2)*136
    cards.append(f'''<g transform="translate({x} {y})">
      <rect width="536" height="112" rx="16" fill="#111522" stroke="#8C78FF" stroke-opacity=".24"/>
      <text x="22" y="29" fill="#8C78FF" font-family="monospace" font-size="10" letter-spacing="1.8">{num} /</text>
      <text x="68" y="30" fill="#F5F5FA" font-family="Inter,Arial,sans-serif" font-size="14" font-weight="700">{title}</text>
      <path d="M22 45H514" stroke="#A6A9B8" stroke-opacity=".12"/>
      <text x="22" y="76" fill="#BFC4D3" font-family="Inter,Arial,sans-serif" font-size="13">{items}</text>
    </g>''')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="272" viewBox="0 0 1120 272" role="img" aria-labelledby="t d">
<title id="t">Engineering toolkit</title><desc id="d">Competências agrupadas em backend, inteligência artificial e automação, cloud e frontend.</desc>
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#8C78FF"/><stop offset="1" stop-color="#78CFFF"/></linearGradient></defs>
<rect width="1120" height="272" rx="20" fill="#090B13" stroke="#A6A9B8" stroke-opacity=".14"/>
{''.join(cards)}
</svg>'''
Path("assets/tech-stack.svg").write_text(svg,encoding="utf-8")
