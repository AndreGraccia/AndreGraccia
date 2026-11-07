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
    query="""query($from:DateTime!,$to:DateTime!){viewer{login contributionsCollection(from:$from,to:$to){totalCommitContributions totalPullRequestContributions totalIssueContributions repositoriesContributedTo(first:1){totalCount}}}}"""
    data=api("https://api.github.com/graphql",{"query":query,"variables":{"from":start.isoformat(),"to":end.isoformat()}})
    if data.get("errors"): raise RuntimeError(data["errors"])
    c=data["data"]["viewer"]["contributionsCollection"]
    stars=0; page=1
    while True:
        repos=api(f"https://api.github.com/users/{USER}/repos?type=owner&per_page=100&page={page}")
        stars+=sum(int(r.get("stargazers_count",0)) for r in repos)
        if len(repos)<100: break
        page+=1
    return [stars,int(c["totalCommitContributions"]),int(c["totalPullRequestContributions"]),int(c["totalIssueContributions"]),int(c["repositoriesContributedTo"]["totalCount"])]
def render(v):
    labels=[("STARS","public repos"),("COMMITS","last 12 months"),("PULL REQUESTS","last 12 months"),("ISSUES","last 12 months"),("REPOSITORIES","contributed to")]
    parts=[]
    for i,((label,hint),value) in enumerate(zip(labels,v)):
        x=18+i*221
        parts.append(f'<g transform="translate({x} 72)"><rect width="205" height="118" rx="15" fill="#111522" stroke="#8C78FF" stroke-opacity=".25"/><text x="16" y="28" fill="#A6A9B8" font-family="monospace" font-size="10" letter-spacing="1">{label}</text><text x="16" y="72" fill="#F5F5FA" font-family="Inter,Arial,sans-serif" font-size="30" font-weight="700">{value:,}</text><text x="16" y="96" fill="#858B9D" font-family="Inter,Arial,sans-serif" font-size="10">{hint}</text></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1123" height="220" viewBox="0 0 1123 220" role="img" aria-labelledby="t d">
<title id="t">GitHub activity metrics</title><desc id="d">Stars públicos e contribuições dos últimos doze meses, atualizados automaticamente.</desc>
<defs><linearGradient id="a"><stop stop-color="#8C78FF"/><stop offset="1" stop-color="#78CFFF"/></linearGradient></defs>
<rect x="1" y="1" width="1121" height="218" rx="20" fill="#090B13" stroke="#A6A9B8" stroke-opacity=".16"/>
<text x="20" y="36" fill="#9B8BFF" font-family="monospace" font-size="11" letter-spacing="2">GITHUB / ENGINEERING ACTIVITY</text>
<text x="1100" y="36" text-anchor="end" fill="#858B9D" font-family="Inter,Arial,sans-serif" font-size="10">AUTO-UPDATED · {datetime.now(timezone.utc).strftime("%Y-%m-%d")} UTC</text>
{''.join(parts)}</svg>'''
if __name__=="__main__":
    Path("assets").mkdir(exist_ok=True)
    Path("assets/metrics.svg").write_text(render(collect()),encoding="utf-8")
