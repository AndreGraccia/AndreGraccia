/* Seletor de idioma PT/EN. Roda no fim do <body>, antes dos módulos (moments, motion, ui), então os componentes já nascem no idioma escolhido.
   Trocar de idioma guarda a escolha (localStorage) e recarrega a página. Sem escolha salva, usa o idioma do navegador (pt = português, o resto = inglês).
   As chaves do dicionário são comparadas sem pontuação nem caixa; a pontuação do começo e do fim de cada texto é preservada. */
(() => {
  let saved = null;
  try { saved = localStorage.getItem('lang'); } catch (e) { /* sem storage: segue o idioma do navegador */ }
  const lang = saved === 'en' || saved === 'pt' ? saved : ((navigator.language || 'pt').toLowerCase().startsWith('pt') ? 'pt' : 'en');
  document.documentElement.lang = lang === 'en' ? 'en' : 'pt-BR';

  document.querySelectorAll('[data-lang]').forEach(b => {
    b.setAttribute('aria-pressed', String(b.dataset.lang === lang));
    b.addEventListener('click', () => {
      if (b.dataset.lang === lang) return;
      try { localStorage.setItem('lang', b.dataset.lang); } catch (e) { /* sem storage: não troca */ return; }
      location.reload();
    });
  });
  if (lang !== 'en') return;

  const n = s => s.normalize('NFC').replace(/[^\p{L}\p{N}%$+]+/gu, ' ').trim().toLowerCase();
  const D = {};
  const add = (pt, en) => { D[n(pt)] = en; };

  // navegação e hero
  add('Ir para o conteúdo', 'Skip to content');
  add('Projetos', 'Projects'); add('Experiência', 'Experience'); add('Contato', 'Contact');
  add('Enviar e-mail', 'Send email'); add('Ver projetos', 'View projects'); add('Falar comigo', 'Talk to me');
  add('Engenheiro de software Java', 'Java software engineer'); add('em formação', 'in training');
  add('Do banco de dados à tela: APIs em Java e Spring Boot, interfaces responsivas em React e testes em Python. Gosto de cálculos com dinheiro, onde precisão e arredondamento são decisões de projeto.', 'From the database to the screen: Java and Spring Boot APIs, responsive React interfaces and Python tests. I like money calculations, where precision and rounding are design decisions.');
  // janela do hero
  add('R$ 1.000 a 2,5% ao mês', 'R$ 1,000 at 2.5% per month'); add('3 prazos', '3 terms');
  add('Prazo', 'Term'); add('Diferença', 'Difference'); add('Simples', 'Simple'); add('Composto', 'Compound');
  add('3 meses', '3 months'); add('6 meses', '6 months'); add('12 meses', '12 months'); add('a mais nos compostos', 'more with compound');
  [['+ R$ 1,89', '+ R$ 1.89'], ['+ R$ 9,69', '+ R$ 9.69'], ['+ R$ 44,89', '+ R$ 44.89'], ['R$ 1.075,00', 'R$ 1,075.00'], ['R$ 1.076,89', 'R$ 1,076.89'],
   ['R$ 1.150,00', 'R$ 1,150.00'], ['R$ 1.159,69', 'R$ 1,159.69'], ['R$ 1.300,00', 'R$ 1,300.00'], ['R$ 1.344,89', 'R$ 1,344.89']].forEach(([a, b]) => add(a, b));
  // projetos
  add('Projetos em Java, Python e IA.', 'Projects in Java, Python and AI.');
  add('APIs que cruzam dinheiro, agentes que usam suas ferramentas.', 'APIs that cross-check money, agents that use their tools.');
  add('Calculadora de Juros', 'Interest Calculator');
  add('API em Java 25 e Spring Boot que calcula juros simples e compostos com BigDecimal em vez de double, e arredonda só no resultado final.', 'Java 25 and Spring Boot API that calculates simple and compound interest with BigDecimal instead of double, rounding only the final result.');
  add('Código no GitHub', 'Code on GitHub'); add('1 regra', '1 rule');
  add('Regra: A = P × (1 + i)^n, tudo em BigDecimal.', 'Rule: A = P × (1 + i)^n, all in BigDecimal.');
  add('Taxa em porcentagem vira fração.', 'Percentage rate becomes a fraction.');
  add('Valor monetário com 2 casas, HALF_UP.', 'Monetary value with 2 decimals, HALF_UP.');
  add('Orquestrador de agentes com React, n8n e LangChain.', 'Agent orchestrator with React, n8n and LangChain.');
  add('Gestão financeira full-stack: API em Spring Boot com Spring Security e JWT, interface em React e dados em PostgreSQL.', 'Full-stack financial management: Spring Boot API with Spring Security and JWT, React interface and PostgreSQL data.');
  add('Orçamento usado', 'Budget used'); add('Este mês', 'This month'); add('abaixo do mês anterior', 'below last month');
  add('1 nov', 'Nov 1'); add('15 nov', 'Nov 15'); add('Hoje', 'Today');
  add('Automação de testes em Python', 'Test automation in Python');
  add('Testes automatizados que validam sistemas e ajudam a achar a causa das falhas.', 'Automated tests that validate systems and help find the cause of failures.');
  add('3 de 3 arquivos', '3 of 3 files'); add('8 testes', '8 tests'); add('12 testes', '12 tests'); add('6 testes', '6 tests');
  add('Arquivos', 'Files'); add('3 passaram', '3 passed'); add('Testes', 'Tests'); add('26 passaram', '26 passed'); add('Pronto', 'Done'); add('em 1,6s', 'in 1.6s');
  // stack
  add('Stack de backend, dados e automação.', 'Backend, data and automation stack.');
  add('Java no centro, Python na automação.', 'Java at the center, Python in automation.');
  add('como eu uso cada coisa', 'how I use each thing');
  add('Java 25 · API no ar, rotas de juros simples e compostos', 'Java 25 · API up, simple and compound interest routes');
  add('banco pronto na porta 5432', 'database ready on port 5432'); add('tabelas da carteira listadas', 'wallet tables listed');
  add('26 testes passaram em 1,6s', '26 tests passed in 1.6s'); add('n8n no ar na porta 5678, agente pronto', 'n8n up on port 5678, agent ready');
  add('build e testes rodando na pipeline', 'build and tests running in the pipeline');
  add('Linguagens', 'Languages'); add('Dados', 'Data'); add('Automação e IA', 'Automation and AI');
  add('Também: SQL, SQL Server, JPA, REST, JWT e JUnit.', 'Also: SQL, SQL Server, JPA, REST, JWT and JUnit.');
  // sobre
  add('Sobre', 'About');
  add('Penso o sistema inteiro: como o back e o front se conectam, como a tela se adapta ao celular e o que acontece quando algo falha. Uso IA como engenheiro, não como atalho: eu defino a', 'I think about the whole system: how back end and front end connect, how the screen adapts to a phone and what happens when something fails. I use AI as an engineer, not as a shortcut: I define the');
  add('estrutura e as regras', 'structure and the rules'); add('depois reviso e testo o que ela escreve. Estou em formação e evoluo a cada projeto, hoje também na prática, na Cielo.', 'then I review and test what it writes. I am in training and I grow with every project, now on the job too, at Cielo.');
  // experiência
  add('Experiência, formação e certificados.', 'Experience, education and certificates.');
  add('Aprendiz de Engenharia de Software', 'Software Engineering Apprentice');
  add('Automações em Python, testes automatizados, análise de falhas e validação de sistemas, em equipes multidisciplinares.', 'Python automation, automated testing, failure analysis and system validation, in cross-functional teams.');
  add('jul 2026 – atual', 'Jul 2026 – present'); add('Ciência da Computação', 'Computer Science');
  add('Bacharelado em andamento, com formatura prevista para dezembro de 2028.', "Bachelor's degree in progress, expected graduation in December 2028.");
  add('Idiomas e certificados', 'Languages and certificates'); add('Inglês B1', 'English B1');
  add('Inteligência Artificial e Produtividade, Lógica de Programação e Cloud Infrastructure Foundations.', 'Artificial Intelligence and Productivity, Programming Logic and Cloud Infrastructure Foundations.');
  add('Certificados', 'Certificates');
  add('Aprendiz de Engenharia de Software: automação e testes', 'Software Engineering Apprentice: automation and tests');
  add('Orbit.IA: agentes de IA com n8n e LangChain', 'Orbit.IA: AI agents with n8n and LangChain');
  add('Calculadora de Juros: API em Java com BigDecimal', 'Interest Calculator: Java API with BigDecimal');
  add('Primeiro commit: Java e curiosidade', 'First commit: Java and curiosity');
  add('Projetos no GitHub', 'GitHub projects'); add('Inglês', 'English'); add('Formatura', 'Graduation');
  // fechamento, rodapé e caixa de contato
  add('Vamos conversar sobre software.', "Let's talk about software.");
  add('Vaga, projeto ou dúvida sobre algo que construí. Respondo por e-mail.', 'A job, a project or a question about something I built. I reply by email.');
  add('Baixar currículo em PDF', 'Download resume (PDF)');
  add('Engenheiro de software Java em formação. São Paulo, Brasil.', 'Java software engineer in training. São Paulo, Brazil.');
  add('Perfis', 'Profiles'); add('E-mail', 'Email'); add('Currículo (PDF)', 'Resume (PDF)');
  add('Nomes e logos de produtos são marcas de seus donos.', 'Product names and logos are trademarks of their owners.');
  add('Vamos conversar?', "Let's talk?");
  add('Escreva sua mensagem e escolha onde enviar. Ela abre pronta no seu e-mail, é só apertar enviar.', 'Write your message and choose where to send it. It opens ready in your email, just hit send.');
  add('Seu nome', 'Your name'); add('Seu e-mail, para eu poder responder', 'Your email, so I can reply'); add('Assunto', 'Subject'); add('Mensagem', 'Message');
  add('Abrir no Gmail', 'Open in Gmail'); add('App de e-mail', 'Email app'); add('Ou copie meu e-mail:', 'Or copy my email:');
  add('Contato pelo portfólio', 'Contact via portfolio'); add('Fechar', 'Close'); add('Principal', 'Main');
  add('Calculadora de Juros comparando juros simples e compostos de R$ 1.000 a 2,5% ao mês em 3, 6 e 12 meses', 'Interest Calculator comparing simple and compound interest on R$ 1,000 at 2.5% per month over 3, 6 and 12 months');
  add('Terminal mostrando como cada tecnologia entra no meu dia a dia: Spring Boot, Docker, PostgreSQL, Python, n8n, LangChain, Git e GitHub Actions.', 'Terminal showing how each technology fits into my day to day: Spring Boot, Docker, PostgreSQL, Python, n8n, LangChain, Git and GitHub Actions.');
  add('Histórico de carreira em formato de git log: engenharia de software, Orbit.IA, Calculadora de Juros e o primeiro commit', 'Career history as a git log: software engineering, Orbit.IA, Interest Calculator and the first commit');

  const tr = s => {
    const m = s.match(/^(\s*[^\p{L}\p{N}$+]*)([\s\S]*?)([^\p{L}\p{N}%)]*\s*)$/u);
    if (!m) return null;
    const en = D[n(m[2])];
    if (en === undefined) return null;
    return m[1] + (m[3].includes('.') ? en.replace(/\.+$/, '') : en) + m[3];
  };
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode: x => x.parentElement && !/^(SCRIPT|STYLE)$/.test(x.parentElement.tagName) && x.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT });
  const nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
  nodes.forEach(x => { const t = tr(x.nodeValue); if (t !== null) x.nodeValue = t; });
  document.querySelectorAll('[aria-label],[data-note]').forEach(e => ['aria-label', 'data-note'].forEach(a => {
    const v = e.getAttribute(a), t = v && tr(v); if (t) e.setAttribute(a, t); }));
  document.querySelectorAll('input[name=assunto]').forEach(i => { const t = tr(i.value); if (t) i.value = t; });

  document.title = 'André Graccia: Java software engineer in training';
  const md = document.querySelector('meta[name=description]');
  if (md) md.content = 'Java software engineer in training, full stack. Java and Spring Boot APIs, responsive React interfaces, Python tests and AI agents. Projects on GitHub.';
  document.querySelectorAll('a[href$="curriculo-andre-graccia.pdf"]').forEach(a => { a.href = 'resume-andre-graccia-en.pdf'; });
})();
