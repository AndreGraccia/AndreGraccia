// Gera assets/icons/*.svg (tile escuro + logo na cor da marca) a partir do simple-icons.
// Uso: npm i --no-save simple-icons && node scripts/build-icons.mjs
// python/aws/n8n/openai já são tiles locais (não existem no simple-icons atual) e não são sobrescritos.
import * as si from "simple-icons";
import { writeFileSync } from "node:fs";

const light = "#F3F5FF"; // marcas pretas viram claras sobre o tile escuro
const icons = {
  java: ["siOpenjdk", "#F89820"], spring: ["siSpring"], javascript: ["siJavascript"], typescript: ["siTypescript"],
  postgresql: ["siPostgresql"], git: ["siGit"], github: ["siGithub", light], docker: ["siDocker"], maven: ["siApachemaven"],
  react: ["siReact"], html5: ["siHtml5"], css3: ["siCss3"], postman: ["siPostman"], junit: ["siJunit5"],
  "github-actions": ["siGithubactions"], vercel: ["siVercel", light], linux: ["siLinux"], vite: ["siVite"],
};
for (const [name, [key, color]] of Object.entries(icons)) {
  const i = si[key];
  const fill = color ?? "#" + i.hex;
  writeFileSync(`assets/icons/${name}.svg`,
    `<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256" role="img" aria-label="${i.title}"><title>${i.title}</title><rect width="256" height="256" rx="60" fill="#242938"/><path transform="translate(52 52) scale(6.5)" fill="${fill}" d="${i.path}"/></svg>\n`);
}
