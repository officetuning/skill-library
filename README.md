# skill-library

Biblioteca de skills para IAs, facilitando a importação de habilidades a partir do GitHub.

Primeiro pacote: **Data Analyst Advisor** — Power BI, DAX, Power Query M,
modelagem dimensional, storytelling, layout, TMDL/PBIR e QA, convertido da base
de conhecimento `conhecimento-01` a `09` (v3.0, 2026-09-07).

## Skills

| Skill | Use quando | Origem |
|---|---|---|
| [`powerbi-visuais`](skills/powerbi-visuais/SKILL.md) | Qual visual usar, configurar ou criticar gráfico, formatação condicional, tooltip, SVG/HTML por DAX | 01 |
| [`powerbi-boas-praticas`](skills/powerbi-boas-praticas/SKILL.md) | Modelo lento, revisar DAX, auditar modelo, severidade das 76 regras do BPA | 02 |
| [`power-query-m`](skills/power-query-m/SKILL.md) | Query Folding, refresh lento no ETL, função M, Incremental Refresh | 03 |
| [`bi-nomenclatura`](skills/bi-nomenclatura/SKILL.md) | Nomear tabela, view, consulta, coluna ou medida; AV/AA/Δ/Δ%/Δi | 04 |
| [`data-storytelling`](skills/data-storytelling/SKILL.md) | Mensagem principal, Big Idea, poluição visual, apresentação executiva | 05 |
| [`dashboard-canvas`](skills/dashboard-canvas/SKILL.md) | Briefing, 12 blocos, 5W2H, escopo e cronograma antes do Desktop | 06 |
| [`dashboard-layout`](skills/dashboard-layout/SKILL.md) | Wireframe, grid 8px, Background Builder, fuso horário da "última atualização" | 07 |
| [`tmdl-pbir`](skills/tmdl-pbir/SKILL.md) | Script TMDL, `.pbip`, `visual.json`, versionar em Git | 08 |
| [`bi-qa-documentacao`](skills/bi-qa-documentacao/SKILL.md) | Descrição com `///`, BPA por CLI, binding de visuais, CI/CD, `.docx` do modelo | 09 |

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
        └── scripts/         # código testado (só em bi-qa-documentacao)
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

## Versionamento

Edite a skill, suba a `version` em `.claude-plugin/plugin.json` e registre no
commit o que mudou. Datas de vigência (preview, descontinuações) ficam no
próprio texto da skill.

## Licença

MIT — ver [LICENSE](LICENSE).
