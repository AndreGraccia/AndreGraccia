const fs = require("node:fs");

async function main() {
  const end = new Date();
  end.setUTCHours(23, 59, 59, 999);
  const start = new Date(end);
  start.setUTCDate(start.getUTCDate() - 364);
  start.setUTCHours(0, 0, 0, 0);
  const query = `query($login: String!, $from: DateTime!, $to: DateTime!) {
    user(login: $login) {
      contributionsCollection(from: $from, to: $to) {
        contributionCalendar {
          totalContributions
          weeks { contributionDays { contributionCount date } }
        }
      }
    }
  }`;
  const response = await fetch("https://api.github.com/graphql", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.GH_TOKEN}`,
      "Content-Type": "application/json",
      "User-Agent": "AndreGraccia-profile-skyline"
    },
    body: JSON.stringify({ query, variables: {
      login: process.env.GH_LOGIN,
      from: start.toISOString(),
      to: end.toISOString()
    }})
  });
  const payload = await response.json();
  if (!response.ok || payload.errors || !payload.data?.user) {
    throw new Error(JSON.stringify(payload.errors || payload));
  }
  const calendar = payload.data.user.contributionsCollection.contributionCalendar;
  const colors = ["#171B2B","#30284E","#51418A","#8C78FF","#78CFFF"];
  const max = Math.max(1, ...calendar.weeks.flatMap(w => w.contributionDays.map(d => d.contributionCount)));
  const weekGroups = calendar.weeks.map((week, wi) => {
    const blocks = week.contributionDays.map(day => {
      const dow = new Date(day.date + "T00:00:00Z").getUTCDay();
      const x = 350 + wi * 17.4 - dow * 9.2;
      const base = 170 + wi * 4.65 + dow * 4.2;
      const intensity = day.contributionCount === 0 ? 0 :
        Math.min(4, Math.max(1, Math.ceil(Math.sqrt(day.contributionCount / max) * 4)));
      const h = day.contributionCount === 0 ? 3 : 8 + intensity * 10;
      const top = base - h;
      const front = intensity === 0 ? "#111522" : colors[Math.max(0, intensity - 1)];
      const side = intensity === 0 ? "#0C101B" : colors[Math.max(0, intensity - 2)];
      return `<g opacity="${intensity === 0 ? ".58" : ".98"}">
        <path d="M${x} ${top} l9 4.5 v${h} l-9 -4.5Z" fill="${front}"/>
        <path d="M${x} ${top} l-9 4.5 v${h} l9 -4.5Z" fill="${side}"/>
        <path d="M${x} ${top} l9 -4.5 l9 4.5 l-9 4.5 l-9 -4.5Z" fill="${colors[intensity]}" stroke="#DDE7FF" stroke-opacity="${intensity >= 3 ? ".42" : ".14"}" stroke-width=".7"/>
        ${intensity >= 3 ? `<path d="M${x-5} ${top+1}l7 -3.5" stroke="#FFFFFF" stroke-opacity=".62" stroke-width="1"/>` : ""}
        <title>${day.date}: ${day.contributionCount} contributions</title>
      </g>`;
    }).join("");
    return `<g>${blocks}<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="5.2s" begin="${(wi * .115).toFixed(2)}s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1"/></g>`;
  }).join("\n");
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="560" viewBox="0 0 1500 560" role="img" aria-labelledby="title desc">
<title id="title">André Graccia — Contribution Skyline</title>
<desc id="desc">Isometric city built from the real GitHub contribution calendar. Each building represents a day; height and violet-to-cyan color encode contribution activity. The city has a visible animated wave.</desc>
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#090B13"/><stop offset="1" stop-color="#11152A"/></linearGradient>
 <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#8C78FF"/><stop offset="1" stop-color="#78CFFF"/></linearGradient>
 <linearGradient id="scan" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#78CFFF" stop-opacity="0"/><stop offset=".5" stop-color="#78CFFF" stop-opacity=".24"/><stop offset="1" stop-color="#8C78FF" stop-opacity="0"/></linearGradient>
 <radialGradient id="glow"><stop stop-color="#8C78FF" stop-opacity=".20"/><stop offset="1" stop-color="#8C78FF" stop-opacity="0"/></radialGradient>
 <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#AAB7E8" stroke-opacity=".045"/></pattern>
 <clipPath id="cityClip"><rect x="285" y="105" width="1000" height="390"/></clipPath>
</defs>
<rect width="1500" height="560" rx="24" fill="url(#bg)"/>
<rect width="1500" height="560" rx="24" fill="url(#grid)"/>
<ellipse cx="780" cy="315" rx="670" ry="250" fill="url(#glow)"/>
<path d="M58 98H1442" stroke="url(#accent)" stroke-opacity=".46"/>
<text x="58" y="56" fill="#FFFFFF" font-family="Inter,Arial,sans-serif" font-size="20" font-weight="700" letter-spacing="1.5">CONTRIBUTION SKYLINE</text>
<text x="58" y="80" fill="#8994B0" font-family="monospace" font-size="11" letter-spacing="1.2">365-DAY ACTIVITY / ISOMETRIC CITY</text>
<g transform="translate(1322 40)"><rect width="120" height="30" rx="15" fill="#FFFFFF" fill-opacity=".045" stroke="url(#accent)" stroke-opacity=".42"/><circle cx="16" cy="15" r="3.2" fill="#78CFFF"><animate attributeName="r" values="2.5;4;2.5" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;.3;1" dur="1.8s" repeatCount="indefinite"/></circle><text x="29" y="19" fill="#C8D2EA" font-family="monospace" font-size="9" letter-spacing="1">LIVE DATA</text></g>
<g opacity=".24" stroke="url(#accent)" fill="none"><path d="M210 465L1290 145" stroke-dasharray="2 10"><animate attributeName="stroke-dashoffset" values="0;-48" dur="7s" repeatCount="indefinite"/></path><path d="M245 485L1320 166" stroke-dasharray="1 13"><animate attributeName="stroke-dashoffset" values="0;56" dur="9s" repeatCount="indefinite"/></path></g>
<g clip-path="url(#cityClip)">
 <path d="M285 470L1290 470" stroke="#AAB7E8" stroke-opacity=".12"/>
 <g>${weekGroups}</g>
 <g transform="translate(285 0)"><rect x="0" y="105" width="105" height="390" fill="url(#scan)" opacity=".85"><animate attributeName="x" values="-120;1010;-120" dur="8s" repeatCount="indefinite"/></rect></g>
</g>
<g fill="none" stroke-linecap="round"><path d="M58 505H1442" stroke="#FFFFFF" stroke-opacity=".12"/><path d="M58 505H1442" stroke="url(#accent)" stroke-opacity=".28" stroke-dasharray="2 12"><animate attributeName="stroke-dashoffset" values="0;-56" dur="12s" repeatCount="indefinite"/></path></g>
<text x="58" y="535" fill="#A8B1CB" font-family="monospace" font-size="10" letter-spacing="1">LOW ACTIVITY</text>
<g transform="translate(165 522)">${colors.map((c,i)=>`<rect x="${i*20}" y="0" width="14" height="10" rx="2" fill="${c}"/>`).join("")}</g>
<text x="285" y="535" fill="#A8B1CB" font-family="monospace" font-size="10" letter-spacing="1">HIGH ACTIVITY</text>
<text x="1442" y="535" text-anchor="end" fill="#78839F" font-family="monospace" font-size="10" letter-spacing=".8">${calendar.totalContributions} CONTRIBUTIONS / THROUGH ${calendar.weeks.at(-1).contributionDays.at(-1).date}</text>
<path d="M0 0H1500" stroke="url(#accent)" stroke-width="2" stroke-opacity=".72"><animate attributeName="stroke-opacity" values=".25;.9;.25" dur="5s" repeatCount="indefinite"/></path>
</svg>`;
  fs.mkdirSync("assets", { recursive: true });
  fs.writeFileSync("assets/skyline.svg", svg);
}
main().catch(error => { console.error(error); process.exit(1); });
