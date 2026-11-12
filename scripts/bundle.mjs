// Junta os CSS do <head> em 2 arquivos (antes e depois do <style> inline) para cortar requisições. Rode: node scripts/bundle.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
const A = ['assets/system.css','assets/ui/cards.css','assets/motion/motion.css','assets/backgrounds/backgrounds.css','assets/layout/layout.css','assets/icons/icon.css'];
const B = ['assets/ui/base.css','assets/ui/code/fragment.css','assets/ui/stat/fragment.css','assets/ui/terminal-run/fragment.css','assets/diagrams/diagram.css'];
const join = (l) => l.map((f) => readFileSync(f, 'utf8')).join('\n');
writeFileSync('assets/bundle-a.css', join(A));
writeFileSync('assets/bundle-b.css', join(B));
for (const f of ['assets/bundle-a.css', 'assets/bundle-b.css']) execSync(`npx --yes esbuild ${f} --minify --allow-overwrite --outfile=${f}`, { stdio: 'ignore' });
