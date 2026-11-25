---
name: dashboard-layout
description: Wireframe, grid e sistema visual de relatórios Power BI — base 8px, grid 12×9 sobre canvas 1920×1080, conversão para x/y/width/height do visual.json, zonas reservadas, barra lateral de filtros (Encaixe 1/1, 1/2, 1/3) e slots do cabeçalho do Background Builder, tooltip em três tamanhos (320×240, 400×304, 600×456), paleta derivada de Accent/Navy e o bug de fuso horário em "última atualização" no Service. Use para definir onde cada visual fica, padronizar layout entre páginas, montar um relatório a partir do Background Builder, diagnosticar relatório desalinhado ou data de atualização errada no Service. Para escolher o visual use powerbi-visuais.
---

# Layout e sistema visual

## Pergunta central

> Se eu desenhasse esta página em papel antes de abrir o Power BI, ela ficaria
> consistente com as outras páginas?

## Hierarquia do padrão

1. **Base 8px + zonas reservadas do Background Builder** — fonte de verdade,
   não negociável.
2. **Grid 12 colunas × 9 linhas** — convenção subordinada. Troque o número de
   colunas ou linhas quando o projeto pedir, **desde que a divisão continue
   múltipla de 8**.

O grid não é recurso nativo do Power BI. É convenção de design aplicada pelas
posições X/Y/Width/Height, que o `visual.json` do PBIR persiste em pixels.

## Regras

**Obrigatório**
- Wireframe antes de abrir o Desktop, em canvas **1920×1080**.
- Toda largura e altura de célula múltipla de 8.
- Mesmo tipo de visual na mesma célula em todas as páginas (filtros sempre no
  mesmo lugar, KPIs sempre na mesma linha).
- Intenção e Cálculo de cada bloco herdados do Painel Visual do Canvas (skill
  `dashboard-canvas`). O wireframe decide **onde**, não **o quê**.
- Margem e vão de **16 px** entre visuais, bordas, cabeçalho e painel;
  posições `x`/`y`/`width`/`height` sempre **inteiras**.
- **Refazer a posição do navegador de páginas depois de toda regeneração do
  Builder**: o menu do PNG depende do H1 e a ordem das páginas pode mudar
  (`references/background-builder-regeneracao.md`).

**Preferir**
- Elemento dominante ocupa **mais colunas**, não necessariamente a linha de cima.
- Anotar o `tabOrder` pretendido no wireframe.
- Página **Início** como abertura (`landingPageName`) e versão e data da página
  **Sobre** atualizadas a cada leva de edições: `references/pagina-inicial-e-sobre.md`.
- Congelar o wireframe com aprovação do stakeholder antes do primeiro visual.

**Evitar**
- "Montar e ir ajustando" em relatório com mais de 2–3 páginas.
- Tratar o grid como camisa de força (mapa costuma pedir proporção livre).

## Grid 12×9

| | Conta | Valor | Múltiplo de 8 |
|---|---|---|---|
| Coluna | 1920 ÷ 12 | 160 px | ✔️ |
| Linha | 1080 ÷ 9 | 120 px | ✔️ |

⚠️ Não use 8 linhas: 1080 ÷ 8 = 135 px, que não é múltiplo de 8.

| Bloco | Colunas | Largura | Uso |
|---|---|---|---|
| 1/4 | 3 | 480 | Cartão de KPI |
| 1/3 | 4 | 640 | Gráfico secundário |
| 1/2 | 6 | 960 | Gráfico principal |
| 2/3 | 8 | 1280 | Protagonista |
| Inteira | 12 | 1920 | Faixa de filtros, mapa |

| Linhas | Altura | Uso |
|---|---|---|
| 1 | 120 | Filtros e título, **só sem Background Builder** |
| 2–3 | 240 | KPIs |
| 4–9 | 720 | Corpo |

## Grid → pixel

```
x      = (coluna_inicial − 1) × 160
y      = (linha_inicial − 1) × 120      (+ altura do cabeçalho, com Background Builder)
width  = número_de_colunas × 160
height = número_de_linhas × 120
```

Exemplo: KPI em col 1–3, linha 2–3 → `x=0, y=120, width=480, height=240`.

Confirme o formato exato do bloco de posição no
[JSON Schema do PBIR](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition)
antes de editar em lote (skill `tmdl-pbir`).

Exemplo trabalhado completo (página "Performance Comercial"), fluxo do Canvas
ao visual construído e checklist: `references/wireframe.md`.

## Com Background Builder

O fundo gerado reserva, em pixel exato, onde cada visual real deve ficar.
Relatório "torto" = visual fora da área reservada. Três mudanças:

1. **Filtros saem do grid** e vão para a **barra lateral** (344×936 em x=16,
   y=128), que aparece a partir de 1 filtro. Cada filtro ocupa 1/1, 1/2 ou 1/3
   da linha (data completa: 296×120), agrupado por 5W2H. Com barra, o corpo
   vai de x=376 a 1904; na Detalhe, sem barra, de x=16 a 1904.
2. **O corpo vai de y=128 a y=1064**, abaixo do cabeçalho; não há rodapé
   reservado. A faixa x=1904–1920 é de marca e fica livre. A última
   atualização é um card no cabeçalho, (1728, 48) 160×32, ausente na Detalhe.
   Se o Builder mudar, vale o guia de montagem exportado; não chute.
3. **Tooltip tem canvas próprio, fora do grid**, em um dos três tamanhos do
   Builder: **320×240** (visual único), **400×304** (vários visuais) ou
   **600×456** (mini relatório). Todos múltiplos de 8; a escolha fica em
   `powerbi-detalhe-dica`.

Evite posicionar visual sobre os cantos reservados à ilustração.

O que vem na coleção, estrutura das páginas, slots do cabeçalho, barra lateral,
paleta, script TMDL, guia de montagem em 13 passos e
o que revisar num relatório feito com o Background Builder:
`references/background-builder.md`. Ciclo de trabalho (regenerar PNG e
fundos), células do menu, painel de filtros e coordenadas do corpo:
`references/background-builder-ciclo.md`. Regenerar sem quebrar o relatório
(menu deslocado pelo H1, ordem das páginas, ficha de ida e volta, cópias do
fundo por Detalhe): `references/background-builder-regeneracao.md`.
Para o agente gerar e baixar a coleção sozinho, sem o usuário abrir o
Builder: skill `background-builder-automacao`.

## Zonas do corpo que se repetem [verificado no Vendas]
- **Botão Limpar filtros** em (200, 152) 136×32, em todas as páginas de corpo
  (`powerbi-visuais`, `tmdl-pbir`).
- **Faixa de indicadores** em (376, 128) 1528×160 ou **216** quando o cartão
  traz AA e Δ% (`powerbi-visuais/references/comparativo-ano-anterior.md`).
- **Storytelling** em (888, 720) 1016×344 com cartões de uma medida sobre as
  chamadas (`data-storytelling/references/storytelling-com-imagem.md`).
- Margem de **16 px** até a borda direita do corpo (x=1904); larguras e alturas
  **simétricas** entre blocos da mesma linha; vão de 16.

## Bug: fuso horário em "última atualização"

`TODAY()` e `NOW()` usam o fuso local no Desktop, mas rodam em **UTC no
Service**. A data exibida diverge assim que o relatório é publicado.

Solução: capturar o momento do refresh no Power Query, já em hora local,
numa tabela interna (`Atualização`, grupo Internas), e comparar com
`UTCNOW()` deslocado na medida `[Última Atualização]`. O script TMDL do
Background Builder cria tudo isso (o 1.031 ainda com os nomes antigos: tabela
de renomeação na referência). Até o 1.033, a medida `Data da Última
Atualização` sai sem aspas na tabela (`Atualização[...]`) e dá erro: em DAX a
tabela vai sempre entre aspas simples, `'Atualização'[...]`. O card fica com
fonte 12, centralizado e sem rótulo. Estrutura
completa em `references/background-builder.md`.
