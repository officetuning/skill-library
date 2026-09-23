---
name: dashboard-layout
description: Wireframe, grid e sistema visual de relatórios Power BI — base 8px, grid 12×9 sobre canvas 1920×1080, conversão para x/y/width/height do visual.json, zonas reservadas e modos de filtro do Background Builder, tooltip 400×304, paleta derivada de Accent/Navy e o bug de fuso horário em "última atualização" no Service. Use para definir onde cada visual fica, padronizar layout entre páginas, montar um relatório a partir do Background Builder, diagnosticar relatório desalinhado ou data de atualização errada no Service. Para escolher o visual use powerbi-visuais.
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

**Preferir**
- Elemento dominante ocupa **mais colunas**, não necessariamente a linha de cima.
- Anotar o `tabOrder` pretendido no wireframe.
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

1. **Filtros saem do grid** e vão para o cabeçalho, conforme o modo:
   1 filtro → `header-1` · 2 filtros → `header-2` · 3+ → `sidebar` (painel
   lateral que consome colunas do corpo).
2. **O corpo começa abaixo do cabeçalho e termina acima do rodapé.** Altura útil
   = 1080 − cabeçalho − rodapé. Recalcule a linha e confira o múltiplo de 8. A
   altura do cabeçalho vem do guia de montagem exportado do projeto; não chute.
3. **Tooltip tem canvas próprio de 400×304 px**, fora do grid.

Evite posicionar visual sobre os cantos reservados à ilustração.

Estrutura das páginas, modos de filtro, paleta, guia de montagem em 12 passos e
o que revisar num relatório feito com o Background Builder:
`references/background-builder.md`.

## Bug: fuso horário em "última atualização"

`TODAY()` e `NOW()` usam o fuso local no Desktop, mas rodam em **UTC no
Service**. A data exibida diverge assim que o relatório é publicado.

Solução: capturar o momento do refresh no Power Query numa tabela de interface
(`TabIntAtualização`) e aplicar o deslocamento de fuso numa medida. Estrutura
completa em `references/background-builder.md`.
