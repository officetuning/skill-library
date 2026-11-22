# skill-library

Biblioteca de skills para IAs, facilitando a importação de habilidades a partir do GitHub.

Primeiro pacote: **Data Analyst Advisor** — Power BI, DAX, UDF, Power Query M,
modelagem dimensional, storytelling, layout, TMDL/PBIR, Git, MCP, QA e dashboard HTML
com IA, convertido da base
de conhecimento `conhecimento-01` a `09` (v3.0, 2026-09-07).

## Skills

| Skill | Use quando | Origem |
|---|---|---|
| [`powerbi-visuais`](skills/powerbi-visuais/SKILL.md) | Qual visual usar, configurar ou criticar gráfico, formatação condicional, tooltip, SVG/HTML por DAX | 01 |
| [`powerbi-boas-praticas`](skills/powerbi-boas-praticas/SKILL.md) | Modelo lento, revisar DAX, auditar modelo, 90 regras (BPA, PBI-Inspector, Measure Killer e storytelling) e pontuação do Measure Killer | 02 |
| [`power-query-m`](skills/power-query-m/SKILL.md) | Query Folding, refresh lento no ETL, função M, Incremental Refresh | 03 |
| [`bi-nomenclatura`](skills/bi-nomenclatura/SKILL.md) | Nomear tabela, view, consulta, coluna ou medida; AV/AA/Δ/Δ%/Δi | 04 |
| [`data-storytelling`](skills/data-storytelling/SKILL.md) | Mensagem principal, Big Idea, poluição visual, apresentação executiva | 05 |
| [`dashboard-canvas`](skills/dashboard-canvas/SKILL.md) | Briefing, 12 blocos, 5W2H, escopo e cronograma antes do Desktop | 06 |
| [`dashboard-layout`](skills/dashboard-layout/SKILL.md) | Wireframe, grid 8px, Background Builder, fuso horário da "última atualização" | 07 |
| [`tmdl-pbir`](skills/tmdl-pbir/SKILL.md) | Script TMDL, `.pbip`, `visual.json`, rotina de Git, edição em lote na TMDL view | 08 |
| [`bi-qa-documentacao`](skills/bi-qa-documentacao/SKILL.md) | Descrição com `///`, BPA por CLI, binding de visuais, CI/CD, `.docx` do modelo | 09 |
| [`dax-udf`](skills/dax-udf/SKILL.md) | Criar, documentar e testar UDF DAX; VAL × EXPR; formato dinâmico com UDF (`Formato.Escala`) | 1.1.0 |
| [`powerbi-detalhe-dica`](skills/powerbi-detalhe-dica/SKILL.md) | Página de Detalhe (drillthrough) e Dica de Ferramenta; medida de seleção; tamanhos de Dica do Builder | 1.3.0 |
| [`powerbi-mcp`](skills/powerbi-mcp/SKILL.md) | Agente alterando o modelo via Power BI Authoring MCP com segurança; convivência com `skills-for-fabric` | 1.1.0 |
| [`dashboard-html-ia`](skills/dashboard-html-ia/SKILL.md) | Dashboard HTML fora do Power BI com IA a partir de CSV, Excel no OneDrive/SharePoint ou Google Sheets; qual IA usar (Copilot, Gemini, Claude, ChatGPT) | 1.4.0 |

O arquivo `10-fora-de-cobertura` não virou skill: é uma trava de escopo (preço,
licença, Fabric fora de BI, tenant, roadmap) e continua nas instruções do projeto.

## Estrutura

```
skill-library/
├── .claude-plugin/
│   ├── plugin.json          # pacote "data-analyst-advisor"
│   └── marketplace.json     # permite instalar pelo Claude Code
└── skills/
    └── <nome-da-skill>/
        ├── SKILL.md         # frontmatter (name, description) + instruções
        ├── references/      # conteúdo longo, lido só quando preciso
        ├── scripts/         # código testado (bi-qa-documentacao)
        └── assets/          # modelos prontos (template HTML em dashboard-html-ia)
```

## Como instalar

Guia completo para Claude, ChatGPT, Gemini e Copilot: [docs/como-usar-skills.md](docs/como-usar-skills.md).

**Claude Code**

```
/plugin marketplace add officetuning/skill-library
/plugin install data-analyst-advisor@officetuning
```

**Claude (app web e desktop)**
Compacte a pasta de uma skill (ex.: `skills/power-query-m/`) em `.zip` e envie
na área de Skills das configurações.

**Outras IAs**
Cada `SKILL.md` é Markdown puro. Dá para usar como arquivo de conhecimento em
qualquer ferramenta que aceite documentos.

## Correções feitas na conversão

Conferidas na documentação oficial em 2026-09-23:

- **`Number.ToText` e `Table.Max` existem.** A base listava as duas como
  inexistentes. `Table.Max` devolve a **linha**, não o valor; ver
  `power-query-m/references/funcoes-m.md`.
- **Tabular Editor 2 não tem `--error-on-violation`.** O CLI falha com exit
  code 1 quando uma regra de severidade ≥ 3 é violada. `-B` salva o modelo
  como `.bim` (não é "modo build") e `-O` é opção de deploy (não arquivo de
  saída). Comandos corrigidos em `bi-qa-documentacao`.
- **Script de binding** reescrito em Python e testado: o PowerShell original
  lia o arquivo errado dentro do loop.
- **Regra 6.1:** o exemplo usava `FORMAT()` dentro da medida, que devolve texto.
  Agora mostra a propriedade `formatString`.
- **Incremental Refresh** é suportado em Pro, PPU, Premium e Embedded; a base
  dizia "Premium/Fabric" em um trecho.
- **Regra 2.7:** acrescentado o aviso de que `FILTER(ALL(Tabela), ...)` e o
  predicado direto não são equivalentes.

## Novidades

**1.5.1 (nov/2026)**, atualização de `dashboard-layout` com as mudanças do
Background Builder 1.029 a 1.031:

- **Correção:** o nome do PNG da dica tem o tamanho entre parênteses, como em
  `Visual único (320x240).png`.
- **Menu:** passo único em múltiplos de 8 px, margens de 24 px, fonte que
  reduz por degraus e menu centralizado.
- **H2 opcional:** em branco não há texto nem sublinhado, e a tagline sobe 96 px.
- **Cor dos nichos (`customSlot`):** seletor opcional; o `Tema.json` não muda.
- **Assinatura e white label**, versão do contrato da Ficha e campos do JSON.
- **`dax-udf`:** a referência às UDFs usa o nome atual, "UDFs da Biblioteca",
  em `officetuning.ai/biblioteca/udf`.
- **`dashboard-canvas`:** alinhada à página de metodologia: os 12 blocos são do
  Canvas ETL & Modelagem, a Data Visualization é por página (5 blocos) e o
  Bloco 12 é o Encerramento do Projeto (QA e publicação).

**1.5.0 (22/11/2026)**, alinhada ao Background Builder 1.031
([backgroundbuilder.officetuning.ai](https://backgroundbuilder.officetuning.ai/)):

- **`dashboard-layout`**: referência `background-builder.md` reescrita. Barra
  lateral de filtros a partir de 1 filtro (fim dos modos `header-1`/`header-2`),
  com Encaixe 1/1, 1/2 e 1/3, cabeçalhos 5W2H, "Fim do painel" e botões nativos.
  Última atualização vira card no cabeçalho (sem rodapé reservado); Detalhe com
  ícone de olho, card da seleção e Voltar em coordenadas exatas; faixa de marca
  x=1904–1920; 9 fundos de página; conteúdo da coleção (inclusive nomes dos PNG
  de dica); guia de montagem em 13 passos; script TMDL atual (fuso no Power
  Query, `Idioma do Projeto` como fonte única, `USERCULTURE`, refresh manual do
  calendário, `VocêEstáVendo` como medida-modelo).
- **`powerbi-detalhe-dica`**: cabeçalho da Detalhe no padrão novo e uso da
  medida-modelo `[VocêEstáVendo]`.
- **`dashboard-canvas`**: importação da Ficha Técnica do Builder.
- **`tmdl-pbir`**: `scaling = 'Fit'` confirmado como "Ajuste = Alongar".
- **`powerbi-visuais`**: novo endereço do Builder e ícones estatísticos.
- **Endereços novos**: Dashboard Canvas em `dashboardcanvas.officetuning.ai`;
  Function Library incorporada à [Biblioteca](https://officetuning.ai/biblioteca)
  (UDF em `/biblioteca/udf`, guia do MCP em `/biblioteca/guias/dax-mcp-setup`).

**1.4.0 (22/11/2026)**:

- Nova skill **`dashboard-html-ia`**: dashboard HTML fora do Power BI feito por
  IA a partir de CSV, Excel no OneDrive for Business/SharePoint ou Google Sheets.
  Fluxo em 6 etapas, contrato do arquivo HTML (dados embutidos com total de
  controle, pt-BR, datas sem fuso, `textContent`, acessibilidade), snapshot × ao
  vivo e o que usar em cada IA: Analyst e Copilot Code (Microsoft 365 Copilot),
  Sheets canvas e Canvas (Gemini), artefatos e Claude Dashboards (Claude),
  análise de dados e Sites (ChatGPT). Template testado em `assets/`.

**1.3.0 (22/11/2026)**, a partir do uso das skills em projetos reais em PBIP/PBIR:

- Nova skill **`powerbi-detalhe-dica`**: par Detalhe + Dica de um mesmo campo,
  chave do drillthrough, medida de seleção (`SELECTEDVALUE`/`LOOKUPVALUE`),
  cartão único com rodapé padrão e fiação em PBIR.
- **Tooltip em três tamanhos** do Background Builder, escolhidos pelo
  conteúdo: 320×240 (visual único), 400×304 (vários visuais) e 600×456 (mini
  relatório). Substitui o 400×304 fixo em `powerbi-visuais` e `dashboard-layout`.
- Novas referências: `powerbi-visuais/references/cartoes-e-titulos.md`,
  `powerbi-boas-praticas/references/medidas-para-visuais.md`,
  `tmdl-pbir/references/edicao-por-script-e-desktop.md`,
  `bi-qa-documentacao/references/acessibilidade-pbir.md` e
  `dashboard-layout/references/background-builder-ciclo.md`.
- **`tmdl-pbir`**: seção "Editar por script" (ciclo seguro). **`bi-qa-documentacao`**:
  sete checagens baratas na camada 3 e acessibilidade no PBIR.
  **`data-storytelling`**: "Identidade do relatório". **`dashboard-canvas`**:
  filtros por 5W2H. **`dashboard-layout`**: margem e vão de 16 px.
- **`powerbi-boas-praticas`**: regra 6.1 ganha a exceção do `FORMAT()` em
  medida de texto usada só como título.

**1.2.0 (07/10/2026)**, alinhada à página de boas práticas da Function Library:

- **`powerbi-boas-praticas`**: 90 regras em 8 seções. Seção 7 creditada ao
  PBI-Inspector (7.1 a 7.11) e ao Measure Killer (7.12 a 7.14), com o nome da
  regra na ferramenta, limites padrão e severidades do Measure Killer. Nova regra
  7.14 (indicadores). A 7.8 passa a contar campos por visual (máx. 6). Página
  padrão Full HD, sem rolagem. Nova Seção 8, Storytelling e comunicação, de
  revisão manual. Pontuação e vereditos do Measure Killer.
- **`data-storytelling`**: pizza até 4 fatias e ligação com a Seção 8.
- **`powerbi-visuais`**, **`powerbi-mcp`** e **`bi-qa-documentacao`**: limites
  novos, referência às seções certas e PBI-Inspector no pipeline.

**1.1.0 (03/10/2026)**, inspirada em [4 Skills Power BI Developers Should Learn Before 2027](https://datatraining.io/blog/4-skills-power-bi-developers-should-learn-before-2027):

- Nova skill **`dax-udf`**: UDF no padrão OfficeTuning, tipos de parâmetro, VAL × EXPR,
  teste com `EVALUATE`, UDF no TMDL e `Formato.Escala` para formato dinâmico.
- Nova skill **`powerbi-mcp`**: fluxo seguro para o agente alterar o modelo pelo
  Power BI Authoring MCP (backup, PBIP + Git, inventário só leitura, plano aprovado,
  transação, validação com DAX) e convivência com as skills oficiais da Microsoft.
- **`tmdl-pbir`**: PBIR em GA e formato padrão; rotina mínima de Git (commit, diff,
  restaurar, `.gitignore`); receitas de edição em lote na TMDL view; objeto `function`.

## Versionamento

Edite a skill, suba a `version` em `.claude-plugin/plugin.json` e registre no
commit o que mudou. Datas de vigência (preview, descontinuações) ficam no
próprio texto da skill.

## Licença

MIT — ver [LICENSE](LICENSE).
