#!/usr/bin/env python3
from pathlib import Path

Path("assets").mkdir(exist_ok=True)
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="330" viewBox="0 0 1200 330" role="img" aria-labelledby="title desc">
<title id="title">Andre Graccia — Backend, AI and Cloud Engineering</title>
<desc id="desc">Identidade visual técnica com arquitetura de sistemas, inteligência artificial e infraestrutura em nuvem.</desc>
<defs>
 <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#090B13"/><stop offset="1" stop-color="#10172A"/></linearGradient>
 <linearGradient id="line" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#8C78FF"/><stop offset="1" stop-color="#78CFFF"/></linearGradient>
 <radialGradient id="aura"><stop stop-color="#8C78FF" stop-opacity=".25"/><stop offset="1" stop-color="#8C78FF" stop-opacity="0"/></radialGradient>
 <filter id="blur"><feGaussianBlur stdDeviation="28"/></filter>
</defs>
<rect width="1200" height="330" rx="22" fill="url(#bg)"/>
<ellipse cx="930" cy="150" rx="300" ry="220" fill="url(#aura)" filter="url(#blur)"/>
<path d="M1 1H1199V329H1Z" fill="none" stroke="#A9B5D5" stroke-opacity=".13"/>
<path d="M40 44H1160" stroke="#A9B5D5" stroke-opacity=".12"/>
<text x="58" y="72" fill="#9C8CFF" font-family="monospace" font-size="12" letter-spacing="2.5">ENGINEERING / SOFTWARE / SYSTEMS</text>
<text x="56" y="151" fill="#F5F5FA" font-family="Manrope,Inter,Arial,sans-serif" font-size="58" font-weight="800" letter-spacing="-2.6">ANDRÉ GRACCIA</text>
<text x="60" y="190" fill="#C7CAD8" font-family="Inter,Arial,sans-serif" font-size="19">Backend Engineer · AI Engineering · Cloud</text>
<text x="60" y="238" fill="#A6A9B8" font-family="Inter,Arial,sans-serif" font-size="14">Building reliable software, intelligent workflows and scalable foundations.</text>
<g transform="translate(820 65)">
 <rect width="300" height="205" rx="22" fill="#111522" fill-opacity=".78" stroke="#A6B5D8" stroke-opacity=".24"/>
 <rect x="14" y="14" width="272" height="177" rx="16" fill="none" stroke="#8C78FF" stroke-opacity=".18"/>
 <g stroke="url(#line)" stroke-width="1.6" fill="none" opacity=".9">
  <path d="M150 101L72 52M150 101L228 52M150 101L72 153M150 101L228 153M72 52L72 153M228 52L228 153"/>
  <path d="M72 52H228M72 153H228" stroke-opacity=".35"/>
 </g>
 <g fill="#111522" stroke="url(#line)" stroke-width="2">
  <circle cx="150" cy="101" r="29"/><circle cx="72" cy="52" r="15"/><circle cx="228" cy="52" r="15"/><circle cx="72" cy="153" r="15"/><circle cx="228" cy="153" r="15"/>
 </g>
 <g fill="#F5F5FA" font-family="monospace" text-anchor="middle">
  <text x="150" y="106" font-size="12">AI</text><text x="72" y="56" font-size="8">API</text><text x="228" y="56" font-size="8">CLOUD</text><text x="72" y="157" font-size="8">DATA</text><text x="228" y="157" font-size="8">DEV</text>
 </g>
</g>
<text x="60" y="298" fill="#858B9D" font-family="monospace" font-size="10" letter-spacing="1.5">JAVA  /  SPRING  /  AI SYSTEMS  /  AWS</text>
<circle cx="1145" cy="296" r="3" fill="#78CFFF"/>
</svg>'''
Path("assets/hero.svg").write_text(svg, encoding="utf-8")
