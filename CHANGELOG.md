# Changelog

Histórico de versões do pacote `data-analyst-advisor`. A versão mais recente também aparece em "Novidades", no [README](README.md).

## 2.4.3 (25/11/2026)

Correção e duas melhorias no `auditar_visuais.py`.

- **`bi-qa-documentacao`:** `auditar_visuais.py` deixou de quebrar (`KeyError: 'SourceRef'`)
  em visual com campo de **hierarquia** (por exemplo, `FY » FQ » FM` do calendário),
  que não tem `Property` nem `Expression.SourceRef` direto; agregações também passam
  a ser lidas. Duas melhorias: **formatação com seletor órfão** (entrada em
  `objects`/`visualContainerObjects` cujo `selector.metadata` não é nenhum campo do
  visual: sobra de campo trocado ou removido, ou de visual copiado de outro modelo) e
  uma só pergunta [decidir] para **tabela/matriz sem título e/ou subtítulo**, que
  diz o que falta e sugere o subtítulo ("medidas por dimensões") com os campos do
  próprio visual. Título ligado sem texto agora também conta como ausente.

## 2.4.2 (25/11/2026)

Lições de editar por script dois relatórios de RH e Recrutamento no Desktop.

- **`powerbi-visuais`:** tabela e matriz: nunca gravar `"active": false` nas projeções
  de `Values` (o Desktop mostra só a 1ª coluna); gráficos por Sexo: procurar antes a
  coluna "Cor/Hexa" no modelo e, sem ela, usar um azul e um vermelho derivados do
  tema (substitui o rosa `#C2185B`); ícones: Edge com perfil isolado, nunca `taskkill`.
- **`tmdl-pbir`:** onde achar o nome de uma propriedade sem pedir ao usuário (scripts
  `minerva` do Desktop e tema base); o script de gravação deve **travar** se o
  Desktop estiver aberto.
- **`powerbi-boas-praticas`:** Idade e Tempo de Casa em anos completos (`DATEDIFF` com
  `YEAR` errou ~49%) e o fuso de `UTCTODAY` em coluna calculada.
- **`powerbi-mcp`:** dados de pessoas vão ao provedor de IA (consultas agregadas),
  EULA no 1º uso, não editar `.tmdl` à mão com o MCP conectado.
- **`bi-qa-documentacao`:** `auditar_visuais.py` aponta projeção com `active:false`.

## 2.4.1 (25/11/2026)

Só documentação; nenhuma skill mudou.

- Novo `docs/prompt-checkup-projeto-existente.md`: prompt modelo para o Claude Code
  fazer o **checkup (somente leitura)** e a **implementação em lotes** (A higiene do
  modelo, B tema, segmentações e tabelas, C coleção do Builder e Sobre, D cartões,
  comparativos e interações, E storytelling) de um projeto `.pbip` já existente, com
  as regras de conduta, as fases, os pontos de parada e as variantes curtas. Pressupõe
  o plugin 2.4.0 ou posterior e o Background Builder.

## 2.4.0 (25/11/2026)

Aprendizados do checkup de um relatório de RH e dos infográficos de um relatório
comercial, ambos montados com o Background Builder. As regras foram conferidas no
Desktop; as coordenadas pressupõem o layout do Builder (1920×1080, corpo de
(376, 128) a (1904, 1064), barra lateral em x40 com 296 de largura).

- **`powerbi-visuais`:**
  - nova referência `eixo-temporal-e-interacoes.md`: gráfico de eixo de tempo
    (Calendário **e Tempo de Casa**) sob a segmentação de data relativa pode perder o
    sentido; decidir gráfico a gráfico entre respeitar o filtro e editar interações
    (`visualInteractions` com `NoFilter`, formato PBIR confirmado);
  - segmentação de data: fontes de **Intervalo de datas e Resumo em 12** (substitui
    10,8), filtro `DateSpan` precisa estar gravado, barra de destaque desligada;
  - **altura padrão do cartão de Grandes Números: 168 sem e 240 com etiquetas de
    referência**, visuais abaixo de `S = y + altura + 16` a 1064, tudo em múltiplos de
    8; preenchimento interno 10 e `spaceAboveDivider 4`;
  - ícone com **tamanho absoluto de ~53 px** (`imageAreaSize` calculado pelo bloco),
    ícones por código, **foto redonda** (contêiner arredondado, `Fill`), foto por
    posição com **medida de URL** (filtro de visual em ranking não separa as linhas) e
    infográfico em **Preencher**;
  - `comparativo-ano-anterior.md`: `Δ` não vale em nome de **variável** DAX (`vDelta`),
    comparativo de **fluxo do período** com `EDATE`, farol invertido para "menor é
    melhor"; gauge e pizza que repetem um cartão saem.
- **`data-storytelling`:** teste dos **5 segundos** (se precisa explicar a piada, ela
  falhou: a banheira foi trocada pelo ponto de ônibus), **uma analogia por página**
  (mesma família visual, cenas diferentes), **identidade provada antes do desenho** e
  desenho neutro; arte 3D vem de gerador de imagem: novo `prompt-imagem-storytelling.md`
  e o script **`medir_png.py`** (mede balões e retângulos de segmentação no PNG, só
  biblioteca padrão).
- **`bi-qa-documentacao`:** novo script **`auditar_visuais.py`** (segmentações, tabelas,
  cartões, eixo de tempo, grade de 8 px, tema registrado) e checagens 19 a 25.
- **`background-builder-automacao`:** `exportar-colecao.cjs` não trava mais esperando
  `networkidle` (cai para `domcontentloaded`); como comparar a coleção nova com os
  fundos atuais.
- **`dashboard-layout`:** como medir onde ficam as segmentações no fundo novo e criar a
  nova; o **tema registrado precisa ser o da Ficha**.
- **`tmdl-pbir`:** 12 propriedades confirmadas (interações, `Fill`, borda arredondada,
  campos do cartão, preenchimento, `innerRadiusRatio`), e armadilhas de fluxo
  (`python -I` e `PYTHONIOENCODING`, script grande fora do heredoc, BPA e medida
  oculta, tabela sem colchete entre aspas).

## 2.3.0 (24/11/2026)

Aprendizados da construção do relatório Vendas (referências: Finanças e
Performance Comercial).

- **`data-storytelling`:** nova referência `storytelling-com-imagem.md`. A imagem
  nasce de uma **analogia escolhida para os dados** (fases → estrada; níveis →
  degraus; partes → anatomia; comparação; território; meta), com método de
  visual thinking (Dan Roam) e design-by-analogy, e a regra de ouro: **verdadeira
  com qualquer filtro**. Nunca adaptar a ilustração de outro relatório.
- **`powerbi-visuais`:** `comparativo-ano-anterior.md` (família `(AV)`…`(Δ Cor)` e
  cartão único de 216 com AA e Δ%); `imagens-e-icones.md` (visual `image`
  dinâmico como padrão para a entidade selecionada, ícones só em cartões largos,
  cor por Hexa com seletores `roles`); segmentações com Pesquisar e data relativa
  confirmados; tabela e matriz com `BoldHeader`, `growToFit` e cabeçalho
  `ColorId 2`; cartões com preenchimento 14/16/16/16.
- **`powerbi-detalhe-dica`:** Dica sem `pageBinding` e sem `type` no
  `visualTooltip` (com eles o hover mostra o tooltip padrão); Dica com imagem;
  molde único de Detalhe.
- **`tmdl-pbir`:** propriedades confirmadas (Pesquisar, data relativa, estilo de
  tabela, imagem, botão Limpar filtros) e armadilhas de fluxo (`.pbix` por zip,
  Desktop aberto, `cache.abf`, blocos TMDL duplicados, renomeação em lote).
- **`bi-qa-documentacao`:** dicionário: conferir os dados antes de descrever;
  regenerar a cada mudança; ordem do visual.
- **`powerbi-boas-praticas`:** ranking robusto, participação e item líder.
- **`dashboard-layout`:** zonas fixas do corpo (Limpar filtros, faixa de
  indicadores, storytelling).

## 2.2.1 (24/11/2026)

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

## 2.2.0 (24/11/2026)

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

## 2.1.0 (24/11/2026)

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

## 2.0.0 (24/11/2026)

Revisão completa das 13 skills. A versão é maior porque **a nomenclatura mudou**:
o pacote adota o padrão oficial da Microsoft para o modelo semântico
(`skills-for-fabric`, *semantic-model-authoring*) no lugar dos prefixos no modelo.

### O que muda na nomenclatura (`bi-nomenclatura`)

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

### Outras mudanças por skill

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

### Guia de migração de um modelo 1.x

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

## 1.7.1 (23/11/2026)

Ajustes de revisão em `tmdl-pbir` (`edicao-por-script-e-desktop.md`):

- O passo 6 do ciclo seguro diz que `git diff --cached --stat` mostra o que entra
  no commit; separar o trabalho do autor só vale quando o arquivo mistura os dois.
- Comandos por shell: `tasklist | grep -i PBIDesktop` no Git Bash, e
  `$env:TEMP` (PowerShell) ou `$TEMP` (Git Bash) para temporários.
- Arquivo novo sem HEAD: seguir o fim de linha dos arquivos vizinhos do mesmo tipo.

## 1.7.0 (23/11/2026)

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

## 1.6.0 (nov/2026)

Oito referências novas das lições dos projetos de
portfólio, e ajustes em seis skills:

- **`dashboard-layout`:** regenerar o fundo sem quebrar o relatório (menu
  deslocado pelo H1, ordem das páginas, ficha de ida e volta).
- **`data-storytelling`:** identidade do relatório (teste do H1, combinações de
  H2 e tagline, Período como "Quando").
- **`powerbi-detalhe-dica`:** Dica com cartão único em Grade e **rodapé de
  drillthrough em todas as Dicas** (antes, só nas que tinham Detalhe).
- **`powerbi-visuais`:** Exibir unidades = Nenhum e padrão das segmentações.
- **`bi-qa-documentacao`:** dicionário de dados no modelo e checagens 8 a 15.
- **`tmdl-pbir`:** adendo sobre edição por script e Git.
- Itens **a confirmar no Desktop** vêm marcados nas referências (`tabOrder`,
  texto alternativo vazio, rótulo "Alongar" e a propriedade Pesquisar).

## 1.5.1 (nov/2026)

Atualização de `dashboard-layout` com as mudanças do
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

## 1.5.0 (22/11/2026)

Alinhada ao Background Builder 1.031
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

## 1.4.0 (22/11/2026)

- Nova skill **`dashboard-html-ia`**: dashboard HTML fora do Power BI feito por
  IA a partir de CSV, Excel no OneDrive for Business/SharePoint ou Google Sheets.
  Fluxo em 6 etapas, contrato do arquivo HTML (dados embutidos com total de
  controle, pt-BR, datas sem fuso, `textContent`, acessibilidade), snapshot × ao
  vivo e o que usar em cada IA: Analyst e Copilot Code (Microsoft 365 Copilot),
  Sheets canvas e Canvas (Gemini), artefatos e Claude Dashboards (Claude),
  análise de dados e Sites (ChatGPT). Template testado em `assets/`.

## 1.3.0 (22/11/2026)

A partir do uso das skills em projetos reais em PBIP/PBIR:

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

## 1.2.0 (07/10/2026)

Alinhada à página de boas práticas da Function Library:

- **`powerbi-boas-praticas`**: 90 regras em 8 seções. Seção 7 creditada ao
  PBI-Inspector (7.1 a 7.11) e ao Measure Killer (7.12 a 7.14), com o nome da
  regra na ferramenta, limites padrão e severidades do Measure Killer. Nova regra
  7.14 (indicadores). A 7.8 passa a contar campos por visual (máx. 6). Página
  padrão Full HD, sem rolagem. Nova Seção 8, Storytelling e comunicação, de
  revisão manual. Pontuação e vereditos do Measure Killer.
- **`data-storytelling`**: pizza até 4 fatias e ligação com a Seção 8.
- **`powerbi-visuais`**, **`powerbi-mcp`** e **`bi-qa-documentacao`**: limites
  novos, referência às seções certas e PBI-Inspector no pipeline.

## 1.1.0 (03/10/2026)

Inspirada em [4 Skills Power BI Developers Should Learn Before 2027](https://datatraining.io/blog/4-skills-power-bi-developers-should-learn-before-2027):

- Nova skill **`dax-udf`**: UDF no padrão OfficeTuning, tipos de parâmetro, VAL × EXPR,
  teste com `EVALUATE`, UDF no TMDL e `Formato.Escala` para formato dinâmico.
- Nova skill **`powerbi-mcp`**: fluxo seguro para o agente alterar o modelo pelo
  Power BI Authoring MCP (backup, PBIP + Git, inventário só leitura, plano aprovado,
  transação, validação com DAX) e convivência com as skills oficiais da Microsoft.
- **`tmdl-pbir`**: PBIR em GA e formato padrão; rotina mínima de Git (commit, diff,
  restaurar, `.gitignore`); receitas de edição em lote na TMDL view; objeto `function`.
