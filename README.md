# skill-library

Biblioteca de skills para IAs, facilitando a importação de habilidades a partir do GitHub.

Primeiro pacote: **Data Analyst Advisor** — Power BI, DAX, UDF, Power Query M,
modelagem dimensional, storytelling, layout, TMDL/PBIR, Git, MCP, QA e dashboard HTML
com IA, convertido da base
de conhecimento `conhecimento-01` a `09` (v3.0, 2026-09-07).

## Skills

| Skill | Use quando | Origem | Versão |
|---|---|---|---|
| [`powerbi-visuais`](skills/powerbi-visuais/SKILL.md) | Qual visual usar, configurar ou criticar gráfico, formatação condicional, tooltip, SVG/HTML por DAX | 01 | 1.0.0 |
| [`powerbi-boas-praticas`](skills/powerbi-boas-praticas/SKILL.md) | Modelo lento, revisar DAX, auditar modelo, 90 regras (BPA, PBI-Inspector, Measure Killer e storytelling) e pontuação do Measure Killer | 02 | 1.0.0 |
| [`power-query-m`](skills/power-query-m/SKILL.md) | Query Folding, refresh lento no ETL, função M, Incremental Refresh | 03 | 1.0.0 |
| [`bi-nomenclatura`](skills/bi-nomenclatura/SKILL.md) | Nomear tabela, view, consulta, coluna ou medida; AV/AA/Δ/Δ%/Δi | 04 | 1.0.0 |
| [`data-storytelling`](skills/data-storytelling/SKILL.md) | Mensagem principal, Big Idea, poluição visual, apresentação executiva | 05 | 1.0.0 |
| [`dashboard-canvas`](skills/dashboard-canvas/SKILL.md) | Briefing, 12 blocos, 5W2H, escopo e cronograma antes do Desktop | 06 | 1.0.0 |
| [`dashboard-layout`](skills/dashboard-layout/SKILL.md) | Wireframe, grid 8px, Background Builder, fuso horário da "última atualização" | 07 | 1.0.0 |
| [`tmdl-pbir`](skills/tmdl-pbir/SKILL.md) | Script TMDL, `.pbip`, `visual.json`, rotina de Git, edição em lote na TMDL view | 08 | 1.0.0 |
| [`bi-qa-documentacao`](skills/bi-qa-documentacao/SKILL.md) | Descrição com `///`, BPA por CLI, binding de visuais, CI/CD, `.docx` do modelo | 09 | 1.0.0 |
| [`dax-udf`](skills/dax-udf/SKILL.md) | Criar, documentar e testar UDF DAX; VAL × EXPR; formato dinâmico com UDF (`Formato.Escala`) | — | 1.1.0 |
| [`powerbi-detalhe-dica`](skills/powerbi-detalhe-dica/SKILL.md) | Página de Detalhe (drillthrough) e Dica de Ferramenta; medida de seleção; tamanhos de Dica do Builder | — | 1.3.0 |
| [`powerbi-mcp`](skills/powerbi-mcp/SKILL.md) | Agente alterando o modelo via Power BI Authoring MCP com segurança; convivência com `skills-for-fabric` | — | 1.1.0 |
| [`dashboard-html-ia`](skills/dashboard-html-ia/SKILL.md) | Dashboard HTML fora do Power BI com IA a partir de CSV, Excel no OneDrive/SharePoint ou Google Sheets; qual IA usar (Copilot, Gemini, Claude, ChatGPT) | — | 1.4.0 |

**Origem:** número do arquivo da base `conhecimento-01` a `09` de que a skill foi
convertida (— quando nasceu depois). **Versão:** versão do pacote em que a skill
entrou.

O arquivo `10-fora-de-cobertura` não virou skill: é uma trava de escopo (preço,
licença, Fabric fora de BI, tenant, roadmap) e continua nas instruções do projeto.

## Estrutura

```
skill-library/
├── .claude-plugin/
│   ├── plugin.json          # pacote "data-analyst-advisor"
│   └── marketplace.json     # permite instalar pelo Claude Code
├── .github/workflows/
│   └── versao.yml           # confere plugin.json, marketplace.json, README e CHANGELOG
├── CHANGELOG.md             # histórico completo de versões
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

### 1.7.1 (23/11/2026)

Ajustes de revisão em `tmdl-pbir` (`edicao-por-script-e-desktop.md`):

- O passo 6 do ciclo seguro diz que `git diff --cached --stat` mostra o que entra
  no commit; separar o trabalho do autor só vale quando o arquivo mistura os dois.
- Comandos por shell: `tasklist | grep -i PBIDesktop` no Git Bash, e
  `$env:TEMP` (PowerShell) ou `$TEMP` (Git Bash) para temporários.
- Arquivo novo sem HEAD: seguir o fim de linha dos arquivos vizinhos do mesmo tipo.

### 1.7.0 (23/11/2026)

Lições de edição por script e de QA vindas de projetos reais, mais higiene do
repositório. Itens do relato do autor vêm marcados **[relato do autor]** e os que
dependem do Desktop, **[a confirmar no Desktop]**.

- **`tmdl-pbir`:** o ciclo seguro agora manda conferir que o Desktop está fechado
  antes e depois de escrever (`Get-Process PBIDesktop`). Git com
  `core.autocrlf=true`: `git ls-files --eol`, `hash-object --no-filters` com o fim
  de linha do HEAD e `git diff --cached --stat` antes do commit. Também
  `git -c safe.directory=...`, `.encode("utf-8")` e temporários fora de `/tmp`.
  O adendo foi **fundido** em `edicao-por-script-e-desktop.md`.
- **`bi-qa-documentacao`:** checagens 16 (campo do modelo antigo no `.Report`) e 17
  (qualquer unidade diferente de `1D`); acessibilidade em português, porque o
  `pbip_a11y.py` só gera italiano.
- **`powerbi-boas-praticas`:** nova referência `diagnostico-memoria.md`
  ("Não há memória suficiente" numa tabela de detalhe).
- **`powerbi-visuais`:** `tabelas-matrizes-e-cores-fixas.md` (`growToFit`,
  cabeçalho, `rowHeaders`, cor fixa por Sexo).
- **`dashboard-layout`:** `pagina-inicial-e-sobre.md` (`landingPageName`, versão e
  data na página Sobre).
- **Repositório:** `CHANGELOG.md` com o histórico completo; tabela de skills com
  as colunas Origem e Versão; verificação das versões no GitHub Actions.

Histórico completo: [CHANGELOG.md](CHANGELOG.md).

## Versionamento

Edite a skill, suba a `version` em `.claude-plugin/plugin.json` **e em**
`.claude-plugin/marketplace.json`, registre a versão nova no `CHANGELOG.md` e no
bloco "Novidades" acima. O workflow `.github/workflows/versao.yml` confere se as
quatro versões coincidem. Registre no commit o que mudou. Datas de vigência (preview, descontinuações) ficam no
próprio texto da skill.

## Licença

MIT — ver [LICENSE](LICENSE).
