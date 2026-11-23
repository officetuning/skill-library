# Changelog

Histórico de versões do pacote `data-analyst-advisor`. A versão mais recente também aparece em "Novidades", no [README](README.md).

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
