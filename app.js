const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
document.documentElement.classList.add("js");

/* ---------- progresso de rolagem ---------- */
const prog = $("#prog");
addEventListener("scroll", () => prog.style.setProperty("--p", scrollY / Math.max(1, document.documentElement.scrollHeight - innerHeight)), { passive: true });

/* ---------- menu: seção ativa + indicador deslizante ---------- */
const nav = $("nav"), ind = $("#ind"), links = $$("nav a.l");
function place() {
  const a = $("a.l.on", nav);
  if (!a || getComputedStyle(a).display === "none") { ind.style.opacity = 0; return; }
  const ar = a.getBoundingClientRect(), nr = nav.getBoundingClientRect();
  ind.style.opacity = 1; ind.style.width = ar.width + "px"; ind.style.transform = `translateX(${ar.left - nr.left}px)`;
}
const spy = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { links.forEach(a => a.classList.toggle("on", a.hash === "#" + e.target.id)); place(); }
}), { rootMargin: "-45% 0px -50% 0px" });
$$("main section").forEach(s => spy.observe(s));
addEventListener("resize", place);
setTimeout(place, 300);

/* ---------- revelação progressiva ---------- */
const targets = $$(".hero .status, .hero h1 .rv-line, .hero .role, .hero .lead, .hero .rotator, .hero .cta, section .eyebrow, .card:not(.proj), .proj, .contact p, .contact .cta");
const reveal = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add("in"); reveal.unobserve(e.target); }
}), { threshold: .1, rootMargin: "0px 0px -6% 0px" });
targets.forEach((el, i) => { el.classList.add("rv"); el.style.setProperty("--d", (i % 5) * 70 + "ms"); reveal.observe(el); });

/* ---------- terminais: digitam o comando e revelam a saída linha a linha ---------- */
const caret = () => Object.assign(document.createElement("i"), { className: "caret" });
async function play(term) {
  term.classList.add("live");
  const lines = $$(".ln", term);
  for (const ln of lines) {
    if (ln.hasAttribute("data-cmd")) {
      const cmd = $(".cmd", ln), text = cmd.dataset.text ?? "";
      ln.classList.add("show");
      const c = caret(); ln.append(c);
      for (const ch of text) { cmd.textContent += ch; await sleep(26 + Math.random() * 38); }
      if (ln.hasAttribute("data-last")) return;
      await sleep(260); c.remove();
    } else { ln.classList.add("show"); await sleep(70); }
  }
}
$$(".term[data-play]").forEach(term => {
  $$(".cmd", term).forEach(c => { c.dataset.text = c.textContent; });
  if (calm) {
    $$(".ln", term).forEach(l => l.classList.add("show"));
    const last = $(".ln[data-last]", term); if (last) last.append(caret());
    return;
  }
  $$(".cmd", term).forEach(c => { c.textContent = ""; });
  new IntersectionObserver((es, o) => es.forEach(e => {
    if (e.isIntersecting) { o.disconnect(); setTimeout(() => play(term), 350); }
  }), { threshold: .35 }).observe(term);
});

/* ---------- hero: comando rotativo ---------- */
const rot = $("#rot");
if (rot && !calm) {
  const cmds = ["java --version", "mvn -q test", "python -m pytest tests/", "docker compose up -d", "n8n start --tunnel", "git push origin main"];
  let i = 0;
  (async () => {
    await sleep(2200);
    for (;;) {
      for (let n = rot.textContent.length; n > 0; n--) { rot.textContent = rot.textContent.slice(0, n - 1); await sleep(16); }
      i = (i + 1) % cmds.length;
      for (const ch of cmds[i]) { rot.textContent += ch; await sleep(48 + Math.random() * 40); }
      await sleep(2400);
    }
  })();
}

/* ---------- ticker de tecnologias ---------- */
const stack = [["java", "Java"], ["spring", "Spring Boot"], ["python", "Python"], ["postgresql", "PostgreSQL"], ["docker", "Docker"], ["langchain", "LangChain"], ["n8n", "n8n"], ["react", "React"], ["git", "Git"], ["maven", "Maven"], ["junit", "JUnit"], ["linux", "Linux"], ["mysql", "MySQL"], ["spring-security", "Spring Security"]];
const item = ([f, n]) => `<span class="skill"><img src="assets/icons/${f}.svg" alt="" width="30" height="30">${n}</span>`;
$("#track").innerHTML = stack.map(item).join("") + stack.map(item).join("");

/* ---------- spotlight, lente e parallax (ponteiro fino) ---------- */
if (fine && !calm) {
  $$(".card, .contact, nav.glass").forEach(c => c.addEventListener("pointermove", e => {
    const r = c.getBoundingClientRect();
    c.style.setProperty("--mx", e.clientX - r.left + "px"); c.style.setProperty("--my", e.clientY - r.top + "px");
  }, { passive: true }));

  const hero = $(".hero"), lens = $("#lens");
  let tx = 0, ty = 0, x = 0, y = 0, raf = 0;
  const loop = () => {
    x += (tx - x) * .12; y += (ty - y) * .12;
    lens.style.transform = `translate(${x - lens.offsetWidth / 2}px,${y - lens.offsetHeight / 2}px)`;
    raf = Math.abs(tx - x) + Math.abs(ty - y) > .5 ? requestAnimationFrame(loop) : 0;
  };
  hero.addEventListener("pointermove", e => {
    const r = hero.getBoundingClientRect();
    tx = e.clientX - r.left; ty = e.clientY - r.top;
    if (!lens.classList.contains("on")) { x = tx; y = ty; lens.classList.add("on"); }
    if (!raf) raf = requestAnimationFrame(loop);
  }, { passive: true });
  hero.addEventListener("pointerleave", () => lens.classList.remove("on"));
}

/* ---------- copiar (e-mail e git clone) ---------- */
const toast = $("#toast");
const say = msg => { toast.textContent = msg; toast.classList.add("show"); clearTimeout(say.t); say.t = setTimeout(() => toast.classList.remove("show"), 2200); };
async function copyText(text, ok) { try { await navigator.clipboard.writeText(text); say(ok); } catch { say(text); } }
const copyBtn = $("#copy"), copyLabel = copyBtn.textContent;
copyBtn.addEventListener("click", () => {
  copyText(copyBtn.dataset.mail, "E-mail copiado"); copyBtn.textContent = "✓ Copiado";
  setTimeout(() => { copyBtn.textContent = copyLabel; }, 2200);
});
$$(".clone").forEach(b => b.addEventListener("click", () => {
  copyText(b.dataset.copy, "Comando copiado"); const em = $("em", b); b.classList.add("ok"); em.textContent = "copiado ✓";
  setTimeout(() => { b.classList.remove("ok"); em.textContent = "copiar"; }, 2000);
}));

/* ---------- paleta de comandos (⌘K / Ctrl+K / "/") ---------- */
const pal = $("#pal"), pq = $("#pq"), pl = $("#pl"), palBtn = $("#palBtn");
palBtn.textContent = isMac ? "⌘K" : "Ctrl K";
const go = id => () => { pal.close(); $(id).scrollIntoView({ behavior: calm ? "auto" : "smooth" }); };
const open = url => () => { pal.close(); window.open(url, "_blank", "noopener"); };
const cmds = [
  ["cd ~/sobre", "seção", go("#sobre")], ["cd ~/experiencia", "seção", go("#experiencia")], ["cd ~/stack", "seção", go("#stack")],
  ["cd ~/projetos", "seção", go("#projetos")], ["cd ~/contato", "seção", go("#contato")],
  ["curl -O curriculo.pdf", "ação", () => { pal.close(); $("a[download]").click(); }],
  ["pbcopy < email", "ação", () => { pal.close(); copyText("andregraccia2105@gmail.com", "E-mail copiado"); }],
  ["open linkedin", "link", open("https://www.linkedin.com/in/andregraccia/")], ["open github", "link", open("https://github.com/AndreGraccia")],
];
let sel = 0, shown = cmds;
function draw() {
  pl.innerHTML = "";
  shown.forEach((c, i) => {
    const li = document.createElement("li"); li.setAttribute("role", "option"); li.className = i === sel ? "on" : "";
    li.innerHTML = `<span class="p">$</span> ${c[0]} <small>${c[1]}</small>`;
    li.onclick = c[2]; li.onpointermove = () => { if (sel !== i) { sel = i; draw(); } }; pl.append(li);
  });
}
function openPal() { pq.value = ""; shown = cmds; sel = 0; draw(); pal.showModal(); pq.focus(); }
palBtn.addEventListener("click", openPal);
pq.addEventListener("input", () => { const q = pq.value.toLowerCase(); shown = cmds.filter(c => (c[0] + c[1]).toLowerCase().includes(q)); sel = 0; draw(); });
pq.addEventListener("keydown", e => {
  if (e.key === "ArrowDown") { sel = (sel + 1) % shown.length; draw(); e.preventDefault(); }
  if (e.key === "ArrowUp") { sel = (sel - 1 + shown.length) % shown.length; draw(); e.preventDefault(); }
  if (e.key === "Enter") { shown[sel]?.[2](); }
});
pal.addEventListener("click", e => { if (e.target === pal) pal.close(); });
addEventListener("keydown", e => {
  const typing = /INPUT|TEXTAREA/.test(document.activeElement.tagName);
  if ((e.key.toLowerCase() === "k" && (e.metaKey || e.ctrlKey)) || (e.key === "/" && !typing)) { e.preventDefault(); pal.open ? pal.close() : openPal(); }
});

/* ==========================================================================
   FX: títulos por palavra, direção alternada, parallax, trilho, tilt, magnético,
   ticker sensível à rolagem, destaque stack ↔ projetos
   ========================================================================== */
(() => {
  const base = img => img.getAttribute("src").split("/").pop().replace(".svg", "");

  /* destaque stack -> projetos (funciona também com movimento reduzido) */
  const projs = $$(".proj");
  $$("#stack .skill").forEach(sk => {
    const img = $("img", sk); if (!img) return;
    const tech = base(img);
    const on = () => {
      let hit = false;
      projs.forEach(p => {
        const m = $$(".chips img", p).filter(i => base(i) === tech);
        m.forEach(i => i.classList.add("hl")); if (m.length) hit = true;
        p.dataset.m = m.length ? "1" : "";
      });
      if (hit) { projs.forEach(p => p.classList.toggle("dim", !p.dataset.m)); sk.classList.add("hl"); }
    };
    const off = () => { projs.forEach(p => p.classList.remove("dim")); $$(".chips img.hl").forEach(i => i.classList.remove("hl")); sk.classList.remove("hl"); };
    sk.addEventListener("pointerenter", on); sk.addEventListener("pointerleave", off);
  });

  /* trilho lateral de seções */
  const rail = document.createElement("nav");
  rail.className = "rail"; rail.setAttribute("aria-label", "Seções");
  [["topo", "Início"], ["sobre", "Sobre"], ["experiencia", "Experiência"], ["stack", "Stack"], ["projetos", "Projetos"], ["contato", "Contato"]].forEach(([id, t]) => {
    const a = document.createElement("a"); a.href = "#" + id; a.setAttribute("aria-label", t); a.innerHTML = `<span>${t}</span>`; rail.append(a);
  });
  document.body.append(rail);
  const railLinks = $$("a", rail);
  new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) railLinks.forEach(a => a.classList.toggle("on", a.hash === "#" + e.target.id));
  }), { rootMargin: "-45% 0px -50% 0px" }).observe($("#topo"));
  $$("main section").forEach(s => new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) railLinks.forEach(a => a.classList.toggle("on", a.hash === "#" + e.target.id));
  }), { rootMargin: "-45% 0px -50% 0px" }).observe(s));

  if (calm) return;

  /* títulos: palavra por palavra ao entrar na tela */
  const split = el => {
    let i = 0;
    const walk = n => [...n.childNodes].forEach(c => {
      if (c.nodeType === 3) {
        const f = document.createDocumentFragment();
        c.textContent.split(/(\s+)/).forEach(t => {
          if (!t.trim()) { f.append(t); return; }
          const w = document.createElement("span"), s = document.createElement("span");
          w.className = "w"; s.textContent = t; s.style.setProperty("--i", i++); w.append(s); f.append(w);
        });
        c.replaceWith(f);
      } else if (c.nodeType === 1) walk(c);
    });
    walk(el); el.classList.add("split");
  };
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { threshold: .3 });
  $$("section h2").forEach(h => { split(h); io.observe(h); });

  /* direção alternada na entrada dos cards */
  $$(".card").forEach(c => {
    const sibs = [...c.parentElement.children], i = sibs.indexOf(c);
    c.style.setProperty("--x", (i % 2 ? 30 : -30) + "px");
  });

  /* parallax + velocidade do ticker pela rolagem */
  const root = document.documentElement, hero = $(".hero");
  const anim = () => $("#track")?.getAnimations()[0];
  let last = scrollY, vel = 0, tick = false, raf2 = 0;
  const frame = () => {
    root.style.setProperty("--sy", scrollY);
    root.style.setProperty("--hs", Math.min(1, scrollY / Math.max(1, hero.offsetHeight * .8)));
    tick = false;
  };
  const spin = () => {
    const a = anim(); if (!a) return;
    a.playbackRate = 1 + vel;
    vel *= .9; if (Math.abs(vel) < .02) { vel = 0; a.playbackRate = 1; raf2 = 0; return; }
    raf2 = requestAnimationFrame(spin);
  };
  addEventListener("scroll", () => {
    const d = scrollY - last; last = scrollY;
    vel = Math.max(-14, Math.min(14, vel + d * .12));
    if (!tick) { tick = true; requestAnimationFrame(frame); }
    if (!raf2) raf2 = requestAnimationFrame(spin);
  }, { passive: true });
  frame();

  /* botões magnéticos + tilt nos cards (ponteiro fino) */
  if (fine) {
    $$(".btn").forEach(b => {
      b.addEventListener("pointermove", e => {
        const r = b.getBoundingClientRect();
        b.style.setProperty("--tx", ((e.clientX - r.left) / r.width - .5) * 8 + "px");
        b.style.setProperty("--ty", ((e.clientY - r.top) / r.height - .5) * 6 + "px");
      }, { passive: true });
      b.addEventListener("pointerleave", () => { b.style.setProperty("--tx", "0px"); b.style.setProperty("--ty", "0px"); });
    });
    $$(".card").forEach(c => {
      c.addEventListener("pointermove", e => {
        const r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        c.style.setProperty("--ry", x * 5 + "deg"); c.style.setProperty("--rx", -y * 5 + "deg");
      }, { passive: true });
      c.addEventListener("pointerleave", () => { c.style.setProperty("--rx", "0deg"); c.style.setProperty("--ry", "0deg"); });
    });
  }
})();

/* manifesto scrub: as palavras acendem conforme a rolagem */
(() => {
  const st = $("#statement"); if (!st) return;
  const label = st.textContent.trim();
  st.setAttribute("aria-label", label);
  st.innerHTML = label.split(/\s+/).map(w => `<span class="w" aria-hidden="true">${w}</span>`).join(" ");
  const words = $$(".w", st);
  if (calm) { words.forEach(w => w.classList.add("lit")); return; }
  let t = false;
  const update = () => {
    t = false;
    const r = st.getBoundingClientRect(), vh = innerHeight;
    const p = Math.min(1, Math.max(0, (vh * .88 - r.top) / (r.height + vh * .3)));
    const n = Math.round(p * words.length * 1.1);
    words.forEach((w, i) => w.classList.toggle("lit", i < n));
  };
  addEventListener("scroll", () => { if (!t) { t = true; requestAnimationFrame(update); } }, { passive: true });
  update();
})();
