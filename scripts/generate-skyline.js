const fs = require("node:fs");

async function main() {
  const end = new Date();
  end.setUTCHours(23, 59, 59, 999);
  const start = new Date(end);
  start.setUTCDate(start.getUTCDate() - 364);
  start.setUTCHours(0, 0, 0, 0);
  const query = `query($login: String!, $from: DateTime!, $to: DateTime!) { user(login: $login) { contributionsCollection(from: $from, to: $to) { contributionCalendar { totalContributions weeks { contributionDays { contributionCount date } } } } } }`;
  const response = await fetch("https://api.github.com/graphql", { method: "POST", headers: { Authorization: "Bearer " + process.env.GH_TOKEN, "Content-Type": "application/json", "User-Agent": "AndreGraccia-profile-skyline" }, body: JSON.stringify({ query, variables: { login: process.env.GH_LOGIN, from: start.toISOString(), to: end.toISOString() } }) });
  const payload = await response.json();
  if (!response.ok || payload.errors || !payload.data?.user) throw new Error(JSON.stringify(payload.errors || payload));
  const calendar = payload.data.user.contributionsCollection.contributionCalendar;
  const colors = ["#161D31", "#30284E", "#51418A", "#8C78FF", "#78CFFF"];
  const max = Math.max(1, ...calendar.weeks.map(w => w.contributionDays.reduce((s,d) => s + d.contributionCount, 0)));
  const towers = calendar.weeks.map((week, i) => {
    const total = week.contributionDays.reduce((s,d) => s + d.contributionCount, 0);
    const level = total === 0 ? 0 : Math.min(4, Math.max(1, Math.ceil(Math.sqrt(total / max) * 4)));
    const h = 24 + level * 22, x = 280 + i * 17.8, y = 404 - h;
    const top = colors[level], front = ["#111827","#292342","#43356F","#6E5BE0","#56A9D8"][level], side = ["#0C1322","#201C38","#342B5B","#5141A4","#397FAF"][level];
    let windows = "";
    for (let k = 0; k < Math.min(5, level + (total > 0 ? 1 : 0)); k++) windows += "<rect x=\"" + (x + 4 + (k % 2) * 5) + "\" y=\"" + (y + 9 + Math.floor(k / 2) * 9) + "\" width=\"2.5\" height=\"4\" rx=\"1\" fill=\"#DDF6FF\"><animate attributeName=\"opacity\" values=\".35;1;.35\" dur=\"" + (2.5 + (i % 4) * .35) + "s\" begin=\"" + ((i % 9) * .22 + k * .13) + "s\" repeatCount=\"indefinite\"/></rect>";
    return "<g><path d=\"M" + x + " " + y + "l8 -5v" + h + "l-8 5Z\" fill=\"" + side + "\"/><path d=\"M" + (x+8) + " " + (y-5) + "l8 5v" + h + "l-8 -5Z\" fill=\"" + front + "\"/><path d=\"M" + x + " " + y + "l8 -5l8 5l-8 5Z\" fill=\"" + top + "\" stroke=\"#DDE7FF\" stroke-opacity=\".45\"/>" + windows + "<title>" + week.contributionDays[0].date + ": " + total + " contributions this week</title></g>";
  }).join("\\n");
  const svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="560" viewBox="0 0 1500 560" role="img" aria-labelledby="title desc">',
    '<title id="title">Orbital City — GitHub contribution skyline</title><desc id="desc">A futuristic glass city in orbit. Each tower represents one week of GitHub contributions over the last 365 days; tower height and illuminated windows show activity.</desc>',
    '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#080C18"/><stop offset=".58" stop-color="#11172B"/><stop offset="1" stop-color="#1B1735"/></linearGradient><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#8C78FF"/><stop offset="1" stop-color="#78CFFF"/></linearGradient><linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#FFFFFF" stop-opacity=".2"/><stop offset=".5" stop-color="#78CFFF" stop-opacity=".035"/><stop offset="1" stop-color="#8C78FF" stop-opacity=".14"/></linearGradient><radialGradient id="glow"><stop stop-color="#8C78FF" stop-opacity=".25"/><stop offset="1" stop-color="#8C78FF" stop-opacity="0"/></radialGradient><radialGradient id="blue"><stop stop-color="#78CFFF" stop-opacity=".18"/><stop offset="1" stop-color="#78CFFF" stop-opacity="0"/></radialGradient><pattern id="stars" width="112" height="84" patternUnits="userSpaceOnUse"><circle cx="15" cy="18" r="1" fill="#E4ECFF" opacity=".6"/><circle cx="74" cy="55" r=".8" fill="#78CFFF" opacity=".7"/><circle cx="101" cy="12" r=".7" fill="#FFFFFF" opacity=".45"/></pattern></defs>',
    '<rect width="1500" height="560" rx="26" fill="url(#bg)"/><rect width="1500" height="560" rx="26" fill="url(#stars)"/><ellipse cx="780" cy="315" rx="700" ry="260" fill="url(#glow)"/><ellipse cx="1190" cy="350" rx="360" ry="200" fill="url(#blue)"/>',
    '<path d="M58 98H1442" stroke="url(#accent)" stroke-opacity=".5"/><text x="58" y="54" fill="#FFFFFF" font-family="Inter,Arial,sans-serif" font-size="20" font-weight="700" letter-spacing="1.8">ORBITAL CITY / CONTRIBUTIONS</text><text x="58" y="78" fill="#A7B4D0" font-family="monospace" font-size="10" letter-spacing="1.5">365-DAY ACTIVITY / WEEKLY ARCHITECTURE</text>',
    '<g transform="translate(1310 38)"><rect width="132" height="32" rx="16" fill="url(#glass)" stroke="url(#accent)" stroke-opacity=".55"/><circle cx="17" cy="16" r="3.5" fill="#78CFFF"><animate attributeName="r" values="2.5;4.5;2.5" dur="2s" repeatCount="indefinite"/></circle><text x="31" y="20" fill="#DDE7F8" font-family="monospace" font-size="9" letter-spacing="1">IN ORBIT</text></g>',
    '<ellipse cx="770" cy="352" rx="660" ry="120" transform="rotate(-8 770 352)" fill="none" stroke="#78CFFF" stroke-opacity=".13" stroke-width="1.2" stroke-dasharray="3 11"><animate attributeName="stroke-dashoffset" values="0;-56" dur="14s" repeatCount="indefinite"/></ellipse><ellipse cx="770" cy="352" rx="580" ry="88" transform="rotate(-8 770 352)" fill="none" stroke="#8C78FF" stroke-opacity=".12"/>',
    '<path d="M218 420L1282 420L1360 458L140 458Z" fill="url(#glass)" stroke="#DDE7FF" stroke-opacity=".22"/><path d="M218 420L1282 420" stroke="#FFFFFF" stroke-opacity=".42"/><path d="M245 434H1260M290 447H1210" stroke="#78CFFF" stroke-opacity=".24"/><path d="M245 405H1255" stroke="#DDE7FF" stroke-opacity=".25"/>',
    towers,
    '<g><path d="M0 0L24 8L0 16L5 8Z" fill="#E9F6FF" transform="translate(320 158)"/><path d="M320 166Q650 70 1050 165" fill="none" stroke="#78CFFF" stroke-opacity=".18" stroke-dasharray="2 9"/><circle r="3.5" fill="#78CFFF"><animateMotion dur="13s" repeatCount="indefinite" path="M320 158Q650 70 1050 165"/></circle></g>',
    '<rect x="24" y="20" width="1452" height="520" rx="24" fill="none" stroke="#FFFFFF" stroke-opacity=".13"/><path d="M58 494H1442" stroke="#FFFFFF" stroke-opacity=".14"/><path d="M58 494H1442" stroke="url(#accent)" stroke-opacity=".45" stroke-dasharray="2 12"><animate attributeName="stroke-dashoffset" values="0;-70" dur="10s" repeatCount="indefinite"/></path>',
    '<text x="58" y="526" fill="#AAB7D2" font-family="monospace" font-size="10" letter-spacing="1.2">QUIET ORBIT</text><g transform="translate(165 514)"><rect width="14" height="9" rx="2" fill="#161D31"/><rect x="20" width="14" height="9" rx="2" fill="#30284E"/><rect x="40" width="14" height="9" rx="2" fill="#51418A"/><rect x="60" width="14" height="9" rx="2" fill="#8C78FF"/><rect x="80" width="14" height="9" rx="2" fill="#78CFFF"/></g><text x="280" y="526" fill="#AAB7D2" font-family="monospace" font-size="10" letter-spacing="1.2">HIGH ACTIVITY</text>',
    '<text x="1442" y="526" text-anchor="end" fill="#8592AE" font-family="monospace" font-size="10" letter-spacing=".8">' + calendar.totalContributions + ' CONTRIBUTIONS / THROUGH ' + calendar.weeks.at(-1).contributionDays.at(-1).date + '</text><path d="M0 0H1500" stroke="url(#accent)" stroke-width="2" stroke-opacity=".8"><animate attributeName="stroke-opacity" values=".25;.9;.25" dur="5s" repeatCount="indefinite"/></path></svg>'
  ].join("\\n");
  fs.mkdirSync("assets", { recursive: true });
  fs.writeFileSync("assets/skyline.svg", svg);
}
main().catch(error => { console.error(error); process.exit(1); });