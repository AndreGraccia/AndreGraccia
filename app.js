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
const targets = $$(".hero .eyebrow, .hero h1, .hero .sub, .hero .meta, .hero .lead, .hero .cta, .hero .tags, .hero .showcase, section > .wrap > .eyebrow, .head, .cards > *, .contact");
const reveal = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add("in"); reveal.unobserve(e.target); }
}), { threshold: .08, rootMargin: "0px 0px -8% 0px" });
targets.forEach((el, i) => { el.classList.add("rv"); el.style.setProperty("--d", (i % 4) * 80 + "ms"); reveal.observe(el); });

/* spotlight nos cards */
if (fine && !calm) {
  $$(".card").forEach(c => c.addEventListener("pointermove", e => {
    const r = c.getBoundingClientRect();
    c.style.setProperty("--mx", (e.clientX - r.left) / r.width * 100 + "%");
    c.style.setProperty("--my", (e.clientY - r.top) / r.height * 100 + "%");
  }, { passive: true }));
}

/* copiar e-mail */
const toast = $("#toast"), copy = $("#copy"), label = copy.textContent;
copy.addEventListener("click", async () => {
  const mail = copy.dataset.mail;
  try { await navigator.clipboard.writeText(mail); toast.textContent = "E-mail copiado"; } catch { toast.textContent = mail; }
  toast.classList.add("show"); copy.textContent = "✓ Copiado";
  setTimeout(() => { toast.classList.remove("show"); copy.textContent = label; }, 2200);
});
setTimeout(place, 300);
