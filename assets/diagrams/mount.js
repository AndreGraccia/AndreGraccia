/*
  taste-skill diagrams/mount.js - draws every [data-diagram] on the page. One line in the page:
    <link rel="stylesheet" href="assets/diagrams/diagram.css">
    <script type="module" src="assets/diagrams/mount.js"></script>
  The icons a diagram names are the files scripts/icons.mjs wrote (icons.mjs scan index.html --out assets/icons),
  read from assets/icons/ or from data-icon-base. See references/diagrams.md.
*/
// Lazy: o diagrama (93 KB + reflows) só carrega e monta perto de entrar na tela.
const go = () => {
  const io = new IntersectionObserver((es) => {
    for (const e of es) {
      if (!e.isIntersecting) continue;
      io.unobserve(e.target);
      import('./diagram.js').then(({ default: dg }) => dg.auto(e.target.parentElement));
    }
  }, { rootMargin: '500px 0px' });
  document.querySelectorAll('[data-diagram]').forEach((el) => io.observe(el));
};
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go, { once: true });
else go();
