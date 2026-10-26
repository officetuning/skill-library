---
name: dashboard-html-ia
description: Criar dashboard em HTML fora do Power BI com IA, a partir de CSV, Excel no OneDrive for Business ou SharePoint, ou planilha Google — fluxo em 6 etapas (perguntar, perfilar, calcular em código, gerar, conferir, compartilhar), contrato do arquivo HTML único (dados embutidos, total de controle, pt-BR, acessibilidade, segurança), snapshot × dado ao vivo, e o que usar em cada IA (Analyst e Copilot Code no Microsoft 365 Copilot, Canvas no Gemini e no Google Sheets, artefatos e Dashboards no Claude, análise de dados e Sites no ChatGPT). Use quando o usuário pedir dashboard, painel ou relatório em HTML feito por IA, "dashboard sem Power BI", painel a partir de planilha, CSV ou Google Sheets, comparar qual IA usar para dashboard, ou revisar um HTML gerado por IA. Para dashboard dentro do Power BI use dashboard-canvas e dashboard-layout.
---

# Dashboard HTML com IA

## Pergunta central

> Se alguém conferir três números deste painel contra a planilha de origem,
> os três batem, e dá para saber de onde e de quando eles vieram?

Painel bonito com número errado é pior que painel nenhum. A IA é rápida para
montar HTML e fraca para somar de cabeça: **número sai de código executado, não
de texto gerado.**

## Quando HTML e quando Power BI

| Situação | Caminho |
|---|---|
| Pergunta pontual, reunião desta semana, protótipo para validar indicador | Dashboard HTML com IA (esta skill) |
| Público sem licença Power BI, arquivo que abre offline ou vai anexado | Dashboard HTML com IA |
| Vários fatos, relacionamentos, RLS, histórico grande, refresh agendado com governança | Power BI (`dashboard-canvas` → `dashboard-layout`) |
| Indicador que vai virar oficial da empresa | Protótipo em HTML, produção no Power BI |

O HTML é ótimo para **explorar e comunicar**. Não substitui modelo semântico
quando a regra de negócio precisa ser única para todos.

## Fluxo em 6 etapas

1. **Perguntar.** Antes de qualquer gráfico, escreva a pergunta de negócio, o
   público e a decisão que o painel apoia. Para projeto maior, use os blocos de
   Descoberta do `dashboard-canvas`. Defina 3 a 5 KPIs com fórmula escrita
   (ex.: "Ticket médio = Receita ÷ Pedidos, só pedidos faturados").
2. **Perfilar os dados.** Peça à IA para ler o arquivo e devolver, **sem
   gráfico ainda**: colunas e tipos, período coberto, linhas, nulos,
   duplicados, categorias estranhas e o **total de controle** (ex.: soma da
   receita). Confira o total na planilha você mesmo.
3. **Calcular em código.** Agregações em Python (Analyst, ChatGPT, Claude) ou
   em JavaScript dentro do HTML, nunca digitadas pela IA. Pré-agregue
   (mês × categoria) antes de embutir: o navegador não precisa das linhas
   brutas.
4. **Gerar o HTML** pelo contrato abaixo. Parta de `assets/template-dashboard.html`
   (testado: filtros, AV × AA, CSV com `;`, modo escuro, celular, CDN fora do ar).
5. **Conferir.** Total do painel = total de controle; três valores sorteados
   batem com a fonte; cada filtro muda KPIs, gráficos e tabela juntos; console
   do navegador sem erro; abre no celular sem rolagem horizontal.
6. **Compartilhar** pelo caminho certo (seção Segurança). Quem recebe o HTML
   recebe **todos os dados embutidos**, mesmo os que o filtro esconde.

## Contrato do arquivo HTML

**Obrigatório**
- **Um arquivo só.** CSS e JS dentro do `.html`; bibliotecas por CDN com versão
  fixa (`chart.js@4.6.1`, nunca `@latest`) e, quando possível, `integrity` (SRI).
- **Dados num bloco próprio**: `<script type="application/json" id="dados">`
  com `meta` (título, fonte, extraído em, linhas na fonte, total de controle) e
  `linhas`. Trocar dado = trocar só esse bloco.
- **Rodapé com proveniência**: fonte, data dos dados, linhas e o resultado da
  conferência do total ("✔ confere" ou "⚠ diverge").
- **Sem dado inventado.** Amostra só quando o usuário pedir, com faixa visível
  "Dados de exemplo" (`meta.exemplo: true`).
- **pt-BR de verdade**: `Intl.NumberFormat("pt-BR")` para moeda, número e
  percentual; datas `dd/mm/aaaa`; meses abreviados em português.
- **Data sem fuso**: `"2026-01-01"` lido com `new Date()` vira UTC e aparece
  como 31/12 no Brasil. Leia ano, mês e dia como texto (mesma família do bug de
  "última atualização" descrito em `dashboard-layout`).
- **Texto dos dados com `textContent`**, nunca `innerHTML`. Uma categoria
  chamada `<img onerror=...>` não pode virar código.
- **Acessibilidade**: contraste AA, variação com sinal e seta além da cor
  (▲ +4,0%), `aria-label` no gráfico com o resumo, tabela como alternativa ao
  gráfico, foco visível, controles com `<label>`.
- **Funciona sem gráfico**: se a CDN falhar, KPIs e tabela continuam e o painel
  avisa.

**Preferir**
- **Título-conclusão calculado** ("Receita cresceu 4,0%; Nordeste caiu 8,6%"),
  gerado pelo código a partir dos números, não escrito pela IA
  (`data-storytelling`).
- 3 a 5 KPIs no topo, 1 gráfico protagonista, 1 de apoio, tabela de detalhe.
  Filtros no cabeçalho, no mesmo lugar em todas as páginas.
- Comparativo com a convenção **AV / AA / Δ / Δ%** de `bi-nomenclatura`, com AA
  nos **mesmos meses** do AV.
- Espaçamento em múltiplos de 8 px; cores como tokens em `:root` (copie
  `dataColors` do tema `.json` do Background Builder para manter a identidade).
- Modo escuro por `prefers-color-scheme` e estilo de impressão.
- Linha para tempo; barras horizontais ordenadas para ranking; pizza só até 4
  fatias (`powerbi-visuais`).

**Evitar**
- Embutir dado pessoal linha a linha (nome, CPF, e-mail) num arquivo que vai
  circular. Agregue.
- Chave de API, token ou senha no HTML. Tudo que está no arquivo é legível.
- Mais de ~10 mil linhas embutidas; mais de 50 categorias num gráfico de barras.
- Gráfico 3D, gauge no lugar de KPI, eixo duplo sem necessidade.
- Biblioteca carregada de CDN desconhecida ou sem versão.

Detalhes de CSV brasileiro, Excel, OneDrive, Google Sheets e tamanho:
`references/fontes-de-dados.md`.

## Snapshot × dado ao vivo

| | Snapshot (HTML com dados embutidos) | Ao vivo (painel dentro da plataforma) |
|---|---|---|
| Atualização | Gerar de novo | Lê a fonte a cada abertura ou por agenda |
| Abre offline, anexa por e-mail | ✔ | ✖ |
| Permissão por pessoa | ✖ quem tem o arquivo vê tudo | ✔ cada um vê o que já pode ver na fonte |
| Onde | Qualquer IA, arquivo `.html` | Copilot Code, Sheets canvas, Claude Dashboards, ChatGPT Sites |

Regra prática: **snapshot** para fechamento, apresentação e anexo; **ao vivo**
quando a mesma pergunta volta toda semana e o público já tem acesso à fonte.

## Qual IA usar

| IA | Onde se destaca | Ferramenta | Fonte natural |
|---|---|---|---|
| **Microsoft 365 Copilot** | Dado que já vive no OneDrive for Business e no SharePoint, sob as regras do tenant | **Analyst** (análise em Python, gráficos, relatório) + **Copilot Code** (Frontier: constrói, pré-visualiza e publica o painel na organização) | Excel e CSV no OneDrive / SharePoint |
| **Google Gemini** | Dado no Google Sheets, editado pela equipe | **Sheets canvas** (painel ao vivo dentro da planilha) e **Canvas** do app Gemini (app HTML portátil) | Google Sheets |
| **Claude** | HTML único com mais controle de design, acessibilidade e conferência, seguindo esta skill; lê os dois ecossistemas | **Artefato HTML** (CSV, Excel, Google Drive, Microsoft 365) e **Claude Dashboards** (beta, SQL por gráfico sobre warehouse e apps conectados) | Upload, Google Drive, OneDrive / SharePoint, warehouse |
| **ChatGPT** | Painel que se atualiza sozinho a partir de uma planilha aprovada | **Análise de dados** (Python) + **Sites** (site privado) + tarefa agendada | Upload, Google Drive, OneDrive / SharePoint |

Combinações que funcionam bem:
- **Copilot**: Analyst confere os números → Copilot Code monta e publica. Sem
  Frontier, peça ao Analyst o HTML como arquivo para baixar (a Microsoft não
  documenta essa saída no Analyst; teste no seu tenant) ou leve os números
  conferidos para outra IA gerar o HTML pelo template.
- **Gemini**: Sheets canvas para o time que vive na planilha; Canvas do app
  quando precisar de HTML para levar para fora.
- **Claude**: perfile e calcule no chat, gere o artefato pelo template; para
  warehouse, Dashboards mostra a consulta de cada gráfico.
- **ChatGPT**: análise de dados para validar → Sites para publicar → tarefa
  agendada para atualizar.

Planos, limites, status de preview e o passo a passo de cada uma, com fontes:
`references/plataformas.md`.

## Prompt mestre

Funciona em qualquer IA. Versões por plataforma e o prompt de conferência:
`references/prompts.md`.

```text
Quero um dashboard em HTML de arquivo único a partir do arquivo anexado.

Pergunta de negócio: [ex.: onde a receita cresceu ou caiu frente ao ano anterior?]
Público: [ex.: diretoria comercial, leitura no celular antes da reunião]
KPIs: [nome = fórmula, até 5]
Filtros: [ex.: ano, região]

Antes de construir:
1. Liste colunas, tipos, período, linhas, nulos e duplicados.
2. Calcule em código o total de [coluna] e me mostre. Espere meu "ok".

Depois:
- Calcule tudo em código (Python ou JavaScript); não digite números.
- Embuta os dados agregados em <script type="application/json" id="dados">
  com meta: fonte, data dos dados, linhas e total de controle.
- Rodapé confere o total do painel contra o total de controle.
- Formato pt-BR (R$, 1.234,56, dd/mm/aaaa); comparativo AV/AA/Δ%.
- Título como conclusão, calculado a partir dos números.
- Texto dos dados com textContent; acessível; responsivo; modo escuro.
- Chart.js com versão fixa; se não carregar, KPIs e tabela continuam.
- Não invente dados. Se faltar algo, pergunte.
```

## Segurança e LGPD

- Antes de anexar à IA, confira se a política da empresa permite aquele dado
  naquela ferramenta (conta corporativa ≠ conta pessoal).
- Planilha Google **publicada na Web** ou link "qualquer pessoa" é pública de
  fato. Use só para dado que poderia estar num site.
- Link público de app do Canvas do Gemini dá a quem tem o link acesso para ver
  **e editar** os dados associados ao app.
- Dashboard ao vivo (Copilot Code, Claude Dashboards, ChatGPT Sites) respeita a
  permissão de cada visitante na fonte; snapshot HTML não respeita.
- Revise o HTML antes de publicar: procure e-mails, CPFs, tokens e colunas que
  não deveriam estar lá.

## Checklist antes de entregar

- [ ] Total do painel = total de controle da fonte
- [ ] Três valores conferidos à mão contra a planilha
- [ ] Filtros mudam KPIs, gráficos e tabela juntos
- [ ] Datas e moeda em pt-BR; janeiro não aparece como dezembro
- [ ] Rodapé com fonte, data dos dados e linhas
- [ ] Sem faixa "Dados de exemplo" (ou com ela, se for amostra)
- [ ] Sem dado pessoal linha a linha nem segredo no arquivo
- [ ] Console sem erro; abre no celular sem rolagem horizontal

## Relação com outras skills

| Precisa de | Use |
|---|---|
| Briefing, KPIs, 5W2H | `dashboard-canvas` |
| Mensagem principal, título-conclusão, poluição visual | `data-storytelling` |
| Qual gráfico, pizza × barras | `powerbi-visuais` |
| Grid 8 px, paleta Accent/Navy, fuso de "última atualização" | `dashboard-layout` |
| Nome de KPI e AV/AA/Δ/Δ% | `bi-nomenclatura` |

## Fontes

Conferidas em 26/10/2026. Lista completa por plataforma em
`references/plataformas.md`.

- [Analyst no Microsoft 365 Copilot](https://support.microsoft.com/en-US/Microsoft-365-Copilot/use-analyst-for-deep-data-analysis)
- [Copilot Code (Frontier)](https://learn.microsoft.com/copilot/code/overview)
- [Sheets canvas](https://support.google.com/docs/answer/17035851)
- [Canvas no app Gemini](https://support.google.com/gemini/answer/16047321)
- [Claude Dashboards](https://support.claude.com/en/articles/17454700-get-started-with-claude-dashboards)
- [ChatGPT Sites](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites)
- [Análise de dados no ChatGPT](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt)
