#!/usr/bin/env python3
"""Build a compact metrics SVG using GitHub's GraphQL contribution totals."""
import json, os, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape

TOKEN=os.environ["GITHUB_TOKEN"]
USER=os.environ.get("GITHUB_REPOSITORY_OWNER","AndreGraccia")
def api(url,payload=None):
    data=json.dumps(payload).encode() if payload else None
    req=urllib.request.Request(url,data=data,headers={"Authorization":f"Bearer {TOKEN}","Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"profile-metrics"})
    with urllib.request.urlopen(req,timeout=30) as r: return json.loads(r.read())
def collect():
    end=datetime.now(timezone.utc); start=end-timedelta(days=364)
    query="""query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(from:$from,to:$to){totalCommitContributions totalPullRequestContributions totalIssueContributions repositoriesContributedTo(first:1){totalCount}}}}"""
    data=api("https://api.github.com/graphql",{"query":query,"variables":{"login":USER,"from":start.isoformat(),"to":end.isoformat()}})
    if data.get("errors"): raise RuntimeError(data["errors"])
    c=data["data"]["user"]["contributionsCollection"]
    stars=0; page=1
    while True:
        repos=api(f"https://api.github.com/users/{USER}/repos?type=owner&per_page=100&page={page}")
        stars+=sum(int(r.get("stargazers_count",0)) for r in repos)
        if len(repos)<100: break
        page+=1
    return [stars,int(c["totalCommitContributions"]),int(c["totalPullRequestContributions"]),int(c["totalIssueContributions"]),int(c["repositoriesContributedTo"]["totalCount"])]
def render(v):
    from build_visuals import STYLE, DEFS, pane, INK, MUTED, DIM, SKY
    labels=[("ESTRELAS","repos públicos"),("COMMITS","últimos 12 meses"),("PULL REQUESTS","últimos 12 meses"),("ISSUES","últimos 12 meses"),("REPOSITÓRIOS","contribuídos")]
    W,H,cw,gap=1200,200,216,18
    parts=[]
    for i,((label,hint),value) in enumerate(zip(labels,v)):
        shown=f"{value:,}" if isinstance(value,int) else value
        x=24+i*(cw+gap)
        parts.append(f'{pane(x,24,cw,152,22)}<text x="{x+22}" y="58" class="m" font-size="10" fill="{SKY}">{label}</text><text x="{x+22}" y="110" font-size="42" font-weight="800" letter-spacing="-1.5" fill="{INK}">{shown}</text><text x="{x+22}" y="142" font-size="12" fill="{MUTED}">{hint}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Atividade no GitHub</title><desc id="d">Estrelas, commits, pull requests, issues e repositórios, atualizados automaticamente.</desc>
{STYLE}{DEFS}
<clipPath id="c"><rect width="{W}" height="{H}" rx="28"/></clipPath>
<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle class="b1" cx="140" cy="200" r="130" fill="#4F6BFF" opacity=".32" filter="url(#blur)"/>
<circle class="b2" cx="1060" cy="0" r="140" fill="#9C8BFF" opacity=".3" filter="url(#blur)"/>
{''.join(parts)}
<text x="{W-24}" y="{H-8}" text-anchor="end" font-size="10" fill="{DIM}">atualizado em {datetime.now(timezone.utc).strftime("%Y-%m-%d")} UTC</text></g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="28" fill="none" stroke="url(#rim)"/>
</svg>'''
if __name__=="__main__":
    Path("assets").mkdir(exist_ok=True)
    Path("assets/metrics.svg").write_text(render(collect()),encoding="utf-8")
