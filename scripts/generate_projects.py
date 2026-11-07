#!/usr/bin/env python3
from pathlib import Path

Path("assets").mkdir(exist_ok=True)
items=[
 ("01","Wall.ia","FINTECH / FINANCIAL ORGANIZATION",("Organização de compromissos financeiros","com foco em clareza e experiência."),"REACT  ·  SPRING BOOT  ·  POSTGRESQL","#8C78FF"),
 ("02","Calculadora de Juros","BACKEND / FINANCIAL API",("API para simulações de juros simples e","compostos, com regras explícitas."),"JAVA 25  ·  SPRING BOOT  ·  MAVEN","#78CFFF"),
 ("03","Orbit.ia","AI / PERSONAL AUTOMATION",("Agente pessoal com interface própria e","workflows orquestrados pelo n8n."),"REACT  ·  N8N  ·  DOCKER","#9B8BFF"),
]
cards=[]
for i,(n,name,tag,desc,stack,color) in enumerate(items):
    x=20+i*373
    cards.append(f'''<g transform="translate({x} 18)">
      <rect width="353" height="258" rx="18" fill="#111522" stroke="{color}" stroke-opacity=".38"/>
      <rect x="1" y="1" width="351" height="3" rx="1.5" fill="{color}" opacity=".85"/>
      <text x="22" y="34" fill="{color}" font-family="monospace" font-size="11" letter-spacing="1.5">{n} / SELECTED PROJECT</text>
      <text x="22" y="83" fill="#F5F5FA" font-family="Manrope,Inter,Arial,sans-serif" font-size="25" font-weight="800">{name}</text>
      <text x="22" y="112" fill="#A6A9B8" font-family="monospace" font-size="9" letter-spacing="1">{tag}</text>
      <path d="M22 132H331" stroke="#A6A9B8" stroke-opacity=".14"/>
      <text x="22" y="158" fill="#C5C9D6" font-family="Inter,Arial,sans-serif" font-size="12">{desc[0]}</text><text x="22" y="178" fill="#C5C9D6" font-family="Inter,Arial,sans-serif" font-size="12">{desc[1]}</text>
      <text x="22" y="232" fill="{color}" font-family="monospace" font-size="10">{stack}</text>
    </g>''')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="294" viewBox="0 0 1120 294" role="img" aria-labelledby="t d">
<title id="t">Selected engineering projects</title><desc id="d">Três projetos: Wall.ia, Calculadora de Juros e Orbit.ia, com suas descrições e tecnologias.</desc>
<rect width="1120" height="294" rx="20" fill="#090B13" stroke="#A6A9B8" stroke-opacity=".14"/>
{''.join(cards)}
</svg>'''
Path("assets/projects.svg").write_text(svg,encoding="utf-8")
