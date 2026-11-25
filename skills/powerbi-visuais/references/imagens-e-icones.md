# Imagens e ícones em visuais

Tudo **[verificado]** no Desktop (Vendas, Finanças e Performance Comercial).

## Imagem dinâmica de uma entidade: visual `image`, não tabela
Regra do autor: **sempre que a seleção é de uma única entidade (Dica, Detalhe,
cartão de perfil) e se quer mostrar a imagem dela (estampa, vendedor, canal,
produto), use o visual `image` dinâmico**, não uma tabela de uma linha (a tabela
traz "Filtrar (0)", rolagem e cabeçalho).
- `objects.image[0].properties`: `sourceType 'imageData'`; `sourceField =
  Aggregation ( Function 3 ) da coluna Imagem…`; `fit 'Fill'` (use `'Fit'` se
  distorcer a proporção).
- A coluna precisa ter `dataCategory: ImageUrl`.
- Sem borda nem fundo; `altText` ("Imagem da <entidade> selecionada.").
- Tabela/matriz com várias linhas continua com **coluna de imagem**: cabeçalho
  curto ("Imagem", "Foto"), tamanho em `objects.grid[0].properties.imageHeight`
  e `imageWidth` (40 px cabem 6 linhas em 464 px).

## Ícones nos cartões
- Objeto `image` por medida: `selector.metadata = queryRef`, `show true`,
  `position 'Right'`, `scaling 'Fit'`, `imageAreaSize 20L`.
- PNG (48 a 96 px) com traço na cor de destaque do tema, registrado em
  `RegisteredResources` (`{ name, path, type: "Image" }` em `report.json`).
  Origem: Google Fonts Icons (exige download autorizado) **ou desenhados por
  código** (SVG → PNG com Playwright/Edge, sem download).
- **Só em cartões largos** (≥ 1500 px, altura 160 a 216). Em Dica (tile ≤ 170 px)
  o ícone empurra o valor e trunca ("R$ 7.8…"); `imageAreaSize` menor não
  resolve. Não use ícone em cartão de Dica.
- Mapa de ícones usado: Faturado = moeda, # Notas = recibo, Peças = camiseta,
  # Clientes = pessoas, Ticket = etiqueta, Prazo = relógio, Frete = caminhão,
  Frete % = percentual.
- Cartões estatísticos: pasta `Icones-Estatisticos` da coleção do Builder (Soma,
  Mínimo, Máximo, Média, Mediana, Desvio Padrão).

## Cor por Hexa: seletores corretos
Coluna `Hexa…` com a cor de cada valor, aplicada por `fill.solid.color.expr =
Aggregation { Column Hexa…, Function 3 }`:
- **Série** (ribbon, mapa, `Estação Cor`): `selector { data: [{ roles:
  ['Series'] }], hierarchyMatching: 1 }`.
- **Categoria** (rosca): `selector { data: [{ roles: ['Category'] }] }`.
- **Colunas por categoria**: `dataViewWildcard` com `matchingOption 1`.
- Sem isso a cor não aplica (o seletor por valor, `scopeId`, funciona mas é
  frágil). O diálogo "Cor por valor de campo" do Desktop pode falhar nesta versão.

## Outros
- **Barras em gradiente por valor:** `dataPoint.fillRule.linearGradient2 { min,
  max, nullColoringStrategy asZero }` com cores do tema.
- **Papel `Tooltips`** de um gráfico: medidas extras no tooltip padrão (ex.: `Δ%`
  na linha AV × AA).
- **Cartão estatístico / Grandes Números:** `layout.style 'Cards'`,
  `orientation '2D'`, `cellPadding 16`, título 15 pt Segoe UI com `titleWrap`.
