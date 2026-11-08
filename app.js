const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
document.documentElement.classList.add("js");

/* progresso de rolagem */
const prog = $("#prog");
addEventListener("scroll", () => prog.style.setProperty("--p", scrollY / Math.max(1, document.documentElement.scrollHeight - innerHeight)), { passive: true });

/* menu: seção ativa + indicador deslizante */
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

/* revelação progressiva */
const targets = $$(".hero .status, .hero h1 .rv-line, .hero .role, .hero .lead, .hero .cta, .hero-icons, section .eyebrow, section h2, .card, .contact p, .contact .cta");
const reveal = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add("in"); reveal.unobserve(e.target); }
}), { threshold: .1, rootMargin: "0px 0px -6% 0px" });
targets.forEach((el, i) => { el.classList.add("rv"); el.style.setProperty("--d", (i % 5) * 70 + "ms"); reveal.observe(el); });

if (fine && !calm) {
  /* aro de luz especular nos cards, no menu e no contato */
  $$(".card, .contact, nav.glass").forEach(c => c.addEventListener("pointermove", e => {
    const r = c.getBoundingClientRect();
    c.style.setProperty("--mx", e.clientX - r.left + "px");
    c.style.setProperty("--my", e.clientY - r.top + "px");
  }, { passive: true }));

  /* lente de vidro no hero: segue o ponteiro com inércia */
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

/* copiar e-mail */
const toast = $("#toast"), copy = $("#copy"), label = copy.textContent;
copy.addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(copy.dataset.mail); toast.textContent = "E-mail copiado"; } catch { toast.textContent = copy.dataset.mail; }
  toast.classList.add("show"); copy.textContent = "✓ Copiado";
  setTimeout(() => { toast.classList.remove("show"); copy.textContent = label; }, 2200);
});
setTimeout(place, 300);
