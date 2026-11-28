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
| [`bi-nomenclatura`](skills/bi-nomenclatura/SKILL.md) | Nomear tabela, view, consulta, grupo, coluna ou medida; (AV)/(AA)/(Δ)/(Δ%)/(Δi) | 04 | 1.0.0 |
| [`data-storytelling`](skills/data-storytelling/SKILL.md) | Mensagem principal, Big Idea, poluição visual, apresentação executiva | 05 | 1.0.0 |
| [`dashboard-canvas`](skills/dashboard-canvas/SKILL.md) | Briefing, 12 blocos, 5W2H, escopo e cronograma antes do Desktop | 06 | 1.0.0 |
| [`dashboard-layout`](skills/dashboard-layout/SKILL.md) | Wireframe, grid 8px, Background Builder, fuso horário da "última atualização" | 07 | 1.0.0 |
| [`tmdl-pbir`](skills/tmdl-pbir/SKILL.md) | Script TMDL, `.pbip`, `visual.json`, rotina de Git, edição em lote na TMDL view | 08 | 1.0.0 |
| [`bi-qa-documentacao`](skills/bi-qa-documentacao/SKILL.md) | Descrição com `///`, BPA por CLI, binding de visuais, CI/CD, `.docx` do modelo | 09 | 1.0.0 |
| [`dax-udf`](skills/dax-udf/SKILL.md) | Criar, documentar e testar UDF DAX; VAL × EXPR; formato dinâmico com UDF (`Formato.Escala`) | — | 1.1.0 |
| [`powerbi-detalhe-dica`](skills/powerbi-detalhe-dica/SKILL.md) | Página de Detalhe (drillthrough) e Dica de Ferramenta; medida de seleção; tamanhos de Dica do Builder | — | 1.3.0 |
| [`powerbi-mcp`](skills/powerbi-mcp/SKILL.md) | Agente alterando o modelo via Power BI Authoring MCP com segurança; convivência com `skills-for-fabric` | — | 1.1.0 |
| [`dashboard-html-ia`](skills/dashboard-html-ia/SKILL.md) | Dashboard HTML fora do Power BI com IA a partir de CSV, Excel no OneDrive/SharePoint ou Google Sheets; qual IA usar (Copilot, Gemini, Claude, ChatGPT) | — | 1.4.0 |
| [`background-builder-automacao`](skills/background-builder-automacao/SKILL.md) | Agente preenche o Background Builder a partir do PBIP e baixa o ZIP sozinho (ficha JSON + script Playwright) | — | 2.1.0 |
| [`calendario-inteligencia-tempo`](skills/calendario-inteligencia-tempo/SKILL.md) | Comparativo com ano anterior, YTD/MTD/WTD, 12M; calendário da prévia (TMDL) ou tabela de data clássica, escolhidos sozinhos | — | 2.2.0 |

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
        ├── scripts/         # código testado (bi-qa-documentacao, background-builder-automacao)
        └── assets/          # modelos prontos (template HTML em dashboard-html-ia)
```

## Como instalar

Guia completo para Claude, ChatGPT, Gemini e Copilot: [docs/como-usar-skills.md](docs/como-usar-skills.md).

**Projeto Power BI já existente?** Prompt modelo para auditar (somente leitura) e evoluir em lotes, com o Background Builder: [docs/prompt-checkup-projeto-existente.md](docs/prompt-checkup-projeto-existente.md).

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

### 2.12.0 (28/11/2026)

Check-up do banco SQL Server, janela de histórico com virada automática, conferência de
hierarquias nos visuais e seis correções. O Incremental Refresh descrito na janela ainda
não foi testado. Detalhe no [CHANGELOG](CHANGELOG.md).

### 2.11.0 (27/11/2026)

Lições de um relatório real: carga de pasta com vários arquivos, validação da carga,
acumulado fiscal, Dica em 600×456, valor central da rosca e a sequência de
conferência antes de dar um visual por pronto. Detalhe no [CHANGELOG](CHANGELOG.md).

### 2.10.0 (26/11/2026)

`powerbi-mcp`: reaproveitar medidas, tratar resultado cortado, limitar novas tentativas e
tratar o conteúdo do modelo como dado. Detalhe no [CHANGELOG](CHANGELOG.md).

### 2.9.0 (26/11/2026)

Script que cria o modelo sintético de teste em um relatório em branco; testes conferidos no
PowerShell 5.1 e 7 contra um Desktop local. Detalhe no [CHANGELOG](CHANGELOG.md).

### 2.8.0 (26/11/2026)

Teste das medidas gravadas no modelo e de UDFs com `CALENDARREF`, com valores de controle
calculados fora do DAX (executado em um Desktop local, com dados sintéticos). Detalhe no
[CHANGELOG](CHANGELOG.md).

### 2.7.0 (26/11/2026)

Teste de medidas com valores esperados em `bi-qa-documentacao`, com os cinco casos do
comparativo (teste da regra, executado em um Desktop local). Detalhe no [CHANGELOG](CHANGELOG.md).

### 2.6.1 (26/11/2026)

Correção do comparativo com o ano anterior: uma só regra para `(Δ)`, `(Δ%)` e `(Δi)`, com
casos de teste. Detalhe no [CHANGELOG](CHANGELOG.md).

### 2.6.0 (26/11/2026)

Storytelling com cena em SVG por medida DAX como padrão: regra de escolha, exemplo testável com
dados fictícios e checagem automática (`checar_svg.py`). Detalhe no [CHANGELOG](CHANGELOG.md).

### 2.5.0 (26/11/2026)

Auditoria com novas checagens (título de gráfico, Dica, botão Voltar), medidas fora da tabela só
de medidas, ano fiscal, infográfico SVG por medida, manual do usuário e exportação sem marca.

### 2.4.3 (25/11/2026)

Correção do `auditar_visuais.py` em visual com campo de hierarquia, checagem de
formatação com seletor órfão e uma só pergunta [decidir] para tabela/matriz sem título
e/ou subtítulo, com sugestão de subtítulo.
Detalhe no [CHANGELOG](CHANGELOG.md).

### 2.4.2 (25/11/2026)

Lições de editar relatórios por script (tabelas, cores por sexo, idade em anos
completos, MCP com dados de pessoas). Detalhe no [CHANGELOG](CHANGELOG.md).

### 2.4.1 (25/11/2026)

Documentação: **prompt modelo** para checkup e implementação em lotes de um projeto
Power BI já existente, independente de máquina e de memória
([docs/prompt-checkup-projeto-existente.md](docs/prompt-checkup-projeto-existente.md)).
Nenhuma skill mudou. Detalhe no [CHANGELOG](CHANGELOG.md).

### 2.4.0 (25/11/2026)

Aprendizados do checkup de um relatório de RH e dos infográficos de um relatório
comercial, ambos com o Background Builder. Detalhe completo no
[CHANGELOG](CHANGELOG.md).

- **Eixo de tempo:** gráfico com eixo de Calendário ou **Tempo de Casa** pode perder o
  sentido sob "Este ano"; decidir entre respeitar o filtro e editar interações
  (`powerbi-visuais`).
- **Cartões:** altura padrão **168 sem e 240 com** etiquetas de referência, visuais
  abaixo na grade de 8 px, ícones de ~53 px e segmentação de data com fontes 12.
- **Storytelling:** teste dos 5 segundos, uma analogia por página, identidade provada
  antes do desenho, prompt para o gerador de imagem e `medir_png.py` para posicionar
  cartões nos balões (`data-storytelling`).
- **QA:** `auditar_visuais.py` e checagens 19 a 25 (`bi-qa-documentacao`).
- **Builder:** `exportar-colecao.cjs` com fallback para redes que nunca ficam
  ociosas; tema registrado = tema da Ficha.

### 2.3.0 (24/11/2026)

Aprendizados da construção do relatório Vendas, com o Finanças e o Performance
Comercial como referência. Detalhe completo no [CHANGELOG](CHANGELOG.md).

- **Storytelling por analogia:** a imagem nasce de uma analogia escolhida para os
  dados (fases, níveis, partes, comparação, território, meta), com método de
  visual thinking e design-by-analogy, e precisa continuar verdadeira com
  qualquer filtro. Nunca se reaproveita a ilustração de outro relatório
  (`data-storytelling`).
- **Visuais:** comparativo com o ano anterior (cartão único de 216 com AA e Δ%),
  visual `image` dinâmico como padrão para a entidade selecionada, ícones só em
  cartões largos e propriedades de segmentação, tabela e matriz confirmadas
  (`powerbi-visuais`).
- **Dica e Detalhe:** Dica sem `pageBinding`, Dica com imagem e molde único de
  Detalhe (`powerbi-detalhe-dica`).
- **Fluxo e QA:** armadilhas de edição por script (`tmdl-pbir`), dicionário com
  dados conferidos (`bi-qa-documentacao`), ranking robusto e item líder
  (`powerbi-boas-praticas`) e zonas fixas do corpo (`dashboard-layout`).

### 2.2.1 (24/11/2026)

Correções vindas do uso do Background Builder, junto com o Builder 1.034.

- **Aspas simples em DAX:** a medida `Data da Última Atualização` gerada pelo
  Builder até a 1.033 usava `Atualização[...]` sem aspas e dava erro por causa
  do `ç`. Regra da casa na `bi-nomenclatura`: em DAX, toda tabela entre aspas
  simples (`'Atualização'[...]`). A `tmdl-pbir` agora deixa claro que "acento
  não exige aspas" vale só para a declaração TMDL, não para a fórmula DAX.
  `dashboard-layout` traz a correção para quem usou o 1.033, e a
  `background-builder-automacao` confere as aspas no `Script.TMDL`.
- **Card de última atualização:** fonte 12, valor centralizado e rótulo
  desligado.
- **Página Sobre:** Equipe Técnica com nomes (Idealização, Especificação de
  Negócio, Realização; `especificacaoNegocio` passa a 300 caracteres na Ficha);
  Dicionário de Dados como visual Tabela com Campo/Medida, Tipo de Dados, Tipo
  (Campo, Campo Calculado, Medida), Tabela e Descrição; Versão e Data em caixas
  de texto Segoe UI Semibold 12, centralizadas (`1.001`, `Ter 24/11/2026`).

### 2.2.0 (24/11/2026)

Nova skill **`calendario-inteligencia-tempo`**: inteligência de tempo a partir
do Calendário do Background Builder.

- Detecta se a inteligência de tempo baseada em calendário (prévia) está
  disponível: calendário já existente, `INFO.CALENDARS()`, nível de
  compatibilidade 1701+ ou teste real na TMDL view. Se não estiver, usa o modo
  clássico com "Marcar como tabela de data" pela coluna `Data`.
- Script TMDL do calendário `'Gregoriano'` com o mapa das colunas do Builder
  (Ano, Trimestre, Mês, Semana, Data, Dia), Semestre, Quinzena e Estação como
  relacionadas ao tempo e Fim de Semana fora do calendário.
- Medidas (AA), (YTD), (QTD), (MTD), (WTD), (12M) nos dois modos, `DATEADD` com
  Extension e Truncation, limites da prévia e UDF com `CALENDARREF`.
- `bi-nomenclatura` e `dax-udf` apontam para a skill nova.
- Requer o Background Builder 1.033 (colunas `Ano/Semana` e `Mês do Trimestre`
  e ordenação de `Ano/Mês (Abreviado)`); com versões anteriores, a skill diz o
  que tirar do script.

### 2.1.0 (24/11/2026)

Nova skill **`background-builder-automacao`**: o agente preenche o Background
Builder e baixa a coleção sem o usuário abrir o site.

- Estuda o PBIP e propõe H1, H2, tagline, tema, páginas e filtros (5W2H e
  Encaixe 1/1, 1/2, 1/3), com tabela de motivos para o ok do usuário.
- Grava a Ficha Técnica em JSON (contrato completo em
  `references/ficha-json.md`, conferido no Builder 1.032).
- `scripts/exportar-colecao.cjs` (Playwright, Edge já instalado no Windows)
  abre o Builder sem janela, carrega a ficha, exporta e salva o ZIP na pasta do
  projeto; só salva se a verificação de pixels do Builder passar.
- Fluxo testado no Builder publicado com um exemplo de 7 páginas.

### 2.0.0 (24/11/2026)

Revisão completa das 13 skills. A versão é maior porque **a nomenclatura mudou**:
o pacote adota o padrão oficial da Microsoft para o modelo semântico
(`skills-for-fabric`, *semantic-model-authoring*) no lugar dos prefixos no modelo.

#### O que muda na nomenclatura (`bi-nomenclatura`)

- **SQL continua igual:** `Tab`/`Vw`/`Pr`/`Fn` e `TabFat`/`TabDim`/`TabPon`/`TabFlt`.
- **Modelo semântico sem prefixo:** fato no plural (`Vendas`), dimensão no
  singular (`Cliente`, `Calendário`), ponte com as duas entidades
  (`Cliente Produto`), monolítica com o recorte (`Vendas Camisetas`).
- **Power Query:** grupos de consultas Funções, Parâmetros, Internas, Dimensões,
  Fatos, Monolíticas, Pontes e Listas, com subgrupo `<Grupo>/Preparo`. `Cns` para
  preparo, `Lista` para listas, `Grupo.Acao` para funções M (sem acento),
  parâmetros em camelCase.
- **Colunas:** nome amigável completo e único no modelo (`Nome do Cliente`);
  chaves ocultas.
- **Medidas:** o nome de negócio mais curto (`Faturado`), **sem "Total"**, `#`
  para contagem, `///` obrigatório, e cada medida na tabela a que pertence (sem
  tabela única de medidas).
- **Comparativo:** sufixo entre parênteses, maiúsculo e sem ponto:
  `Faturado (AV)`, `(AA)`, `(Δ)`, `(Δ%)`, `(Δi)`. AV e AA sempre existem.
- **Nome no visual:** o rótulo é encurtado quando o contexto já diz o resto
  (seis cenários, com exceções), via `displayName` no PBIR.
- **Aspas por linguagem:** DAX, M e TMDL.

#### Outras mudanças por skill

- **`powerbi-detalhe-dica`:** medida de seleção `<Campo> Selecionado(a)` na tabela
  do campo, pasta Seleção, `SELECTEDVALUE(col, "-")`; rodapé de drillthrough só na
  Dica que tem Detalhe irmão; tamanho da Dica pelo conteúdo (320×240, 400×304,
  600×456); "Você Está Vendo" é renomeada, não recriada.
- **`dashboard-layout`:** Background Builder 2.0.0 com `Atualização` e `Calendário`
  (Power Query), e a tabela de nomes antigos do Builder 1.031.
- **`tmdl-pbir`:** exemplos com nomes de negócio e `queryGroup`; acento não exige
  aspas; backups da conversão PBIR (30 dias no Desktop, 28 no Service); variante
  com o Power BI Desktop Bridge (preview).
- **`powerbi-mcp`:** pré-requisitos (readwrite/readonly, XMLA, configuração do
  tenant, service principal, log de auditoria), qual ferramenta edita o modelo,
  ordem da transação, validação com DAX e limite de 100 mil linhas.
- **`power-query-m`:** grupos de consultas, aspas no M e nova referência
  `funcoes-personalizadas-m.md` (padrão `Grupo.Acao`, documentação com
  `Value.ReplaceType`, consulta de teste).
- **`powerbi-visuais`:** Q&A sai em fev/2027; visuais R e Python saem em mai/2027;
  regra de encurtar rótulos.
- **`powerbi-boas-praticas`:** regras que valem sempre (nome de negócio, medidas
  distribuídas, calendário no Power Query, `discourageImplicitMeasures`) e 5.1
  reescrita.
- **`dax-udf`:** nome sem acento; parâmetro sem descrição própria; limitação em
  conexão dinâmica; `INFO.FUNCTIONS("ORIGIN", "2")`.
- **`bi-qa-documentacao`:** o script de documentação lê o papel da tabela pelo
  **grupo de consultas** (`queryGroup`), depois pelo prefixo antigo e, por último,
  pelos relacionamentos; o `.docx` ganha a coluna Grupo. Nova checagem 18 (visual
  R ou Python).
- **`dashboard-canvas`** e **`dashboard-html-ia`:** taxonomia com Ponte e Interna
  e comparativo no formato novo.

#### Guia de migração de um modelo 1.x

1. **Faça backup e versione** (PBIP + Git) antes de renomear.
2. **Renomeie as tabelas do modelo** para o nome de negócio: `TabFatVenda` →
   `Vendas`, `TabDimCliente` → `Cliente`, `TabDimCalendário` → `Calendário`. O SQL
   não muda; só a consulta carregada.
3. **Crie os grupos de consultas** e mova cada consulta para o seu (Fatos,
   Dimensões, Internas…). O script de documentação passa a usar o grupo.
4. **Distribua as medidas** da tabela única para a tabela a que cada uma
   pertence e apague a tabela vazia.
5. **Renomeie as medidas:** tire "Total" e passe o comparativo para parênteses
   (`Total de Vendas AV` → `Faturado (AV)`, `Δ% Total de Vendas` →
   `Faturado (Δ%)`).
6. **Rode a checagem 16** (`grep -rn '"Entity": "Tab' <pasta>.Report`) e corrija
   filtros e formatação condicional que ainda apontam para os nomes antigos.
7. **Relatório feito com o Builder 1.031:** use a tabela "Builder 1.031 e
   anteriores: nomes antigos" em `dashboard-layout/references/background-builder.md`.
8. **Regenere o dicionário** (tabela `Dicionário`) e a documentação `.docx`.

### 1.7.1 (23/11/2026)

Ajustes de revisão em `tmdl-pbir` (`edicao-por-script-e-desktop.md`):

- O passo 6 do ciclo seguro diz que `git diff --cached --stat` mostra o que entra
  no commit; separar o trabalho do autor só vale quando o arquivo mistura os dois.
- Comandos por shell: `tasklist | grep -i PBIDesktop` no Git Bash, e
  `$env:TEMP` (PowerShell) ou `$TEMP` (Git Bash) para temporários.
- Arquivo novo sem HEAD: seguir o fim de linha dos arquivos vizinhos do mesmo tipo.

Histórico completo: [CHANGELOG.md](CHANGELOG.md).

## Versionamento

Edite a skill, suba a `version` em `.claude-plugin/plugin.json` **e em**
`.claude-plugin/marketplace.json`, registre a versão nova no `CHANGELOG.md` e no
bloco "Novidades" acima. O workflow `.github/workflows/versao.yml` confere se as
quatro versões coincidem. Registre no commit o que mudou. Datas de vigência (preview, descontinuações) ficam no
próprio texto da skill.

## Licença

MIT — ver [LICENSE](LICENSE).
