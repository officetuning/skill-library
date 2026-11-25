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
- **Só em cartões largos** (≥ 1500 px, altura 168 a 240). Em Dica (tile ≤ 170 px)
  o ícone empurra o valor e trunca ("R$ 7.8…"); `imageAreaSize` menor não
  resolve. Não use ícone em cartão de Dica.
- Mapa de ícones usado: Faturado = moeda, # Notas = recibo, Peças = camiseta,
  # Clientes = pessoas, Ticket = etiqueta, Prazo = relógio, Frete = caminhão,
  Frete % = percentual.
- Cartões estatísticos: pasta `Icones-Estatisticos` da coleção do Builder (Soma,
  Mínimo, Máximo, Média, Mediana, Desvio Padrão).

### Tamanho do ícone: absoluto, uns 53 px [regra do autor, nov/2026]
`imageAreaSize` é uma **porcentagem da largura do bloco** do cartão. Com 20% fixos o
ícone fica pequeno em cartão de 7 blocos (bloco de 265 px → 53 px) e **grande demais
em cartão de 3 ou 4 blocos** (bloco de ~480 px → ~100 px), onde ele bate na margem
superior do cartão interno. Calcule pelo tamanho que se quer:

```
bloco = (largura do cartão − 32) ÷ número de medidas
imageAreaSize = round(53 ÷ bloco × 100)      # entre 10 e 20
```

Exemplos: 7 blocos → 20%; 5 blocos → 18%; 3 ou 4 blocos → 11%. O ícone fica com
**51 a 55 px em todos os cartões**, e o conjunto parece uma família. Preenchimento
interno e altura do cartão: `references/cartoes-e-titulos.md`.

### Ícones por código para um assunto novo
SVG de formas simples (círculos, retângulos, caminhos) na cor de destaque do tema,
renderizado a 96 px com o Edge ou o Chrome sem janela (`--default-background-color=00000000`),
dá um conjunto coerente em minutos: pessoas, pessoa com ✓ ou ✕ ou + ou −, moeda
(R$), ampulheta, setas de troca, balança, percentual, prédio, pino. Rode o Edge com
**perfil isolado** (`--user-data-dir=<pasta temporária>`) e **nunca use
`taskkill` no Edge**: encerra o navegador do usuário com as abas abertas. Os estatísticos
(Soma, Mínimo...) já vêm do Builder na cor do tema: reaproveite.

## Foto redonda e foto por posição (pódio)

**Foto redonda sobre uma moldura de arte.** O visual `image` é retangular; o corte
redondo vem do **contêiner**:
- visual **quadrado** (largura = altura), uns 8 px maior que o disco da moldura, para
  esconder a borda sob o aro;
- `visualContainerObjects.border` ligado, com `radius` = metade do lado (arredonda
  e recorta) e `width` pequeno (2) na cor do aro;
- `fit 'Fill'` (a foto cobre o círculo e o excesso é cortado pelo centro).
O visual `image` também tem `cornerRadius` próprio (confirmado no Desktop), como
plano B. Rosto muito acima ou abaixo do centro fica cortado.

**Foto de "quem está em 1º, 2º e 3º lugar".** Um visual `image` com
`sourceField = coluna Imagem` e filtro de visual `Ranking = k` **não separa os
vendedores**: os três mostram a mesma foto. O que funciona: **uma medida por
posição** que devolve a URL, com **`dataCategory: ImageUrl`** na medida, e o
`sourceField` do visual apontando para a **medida** (`expr › Measure`), sem filtro
de visual. **[verificado]**

```dax
Vendedor 1º =
MAXX ( FILTER ( ALL ( 'Vendas'[Nome do Vendedor] ),
                [Ranking de Vendedores] = 1 && NOT ISBLANK ( [Faturamento] ) ),
       'Vendas'[Nome do Vendedor] )

Foto 1º =
VAR vNome = [Vendedor 1º]
RETURN IF ( NOT ISBLANK ( vNome ),
            CALCULATE ( MAXX ( VALUES ( 'Vendas'[Imagem do Vendedor] ), 'Vendas'[Imagem do Vendedor] ),
                        'Vendas'[Nome do Vendedor] = vNome ) )
```
Faturamento da posição: `CALCULATE ( [Faturamento], FILTER ( ALL ( nome ), [Ranking] = k ) )`.
Ignore vendedor sem venda (`NOT ISBLANK`): com 2 vendedores, o 3º lugar fica vazio.

## Imagem de infográfico (storytelling)
Visual `image` com `sourceFile`: **ajuste Preencher** (`scaling 'Fill'`), com a caixa
do visual do mesmo formato da arte (3:1 → 1008×336 ou 1528×509; 2:1 → 768×384). Em
caixa de formato diferente o Preencher estica a arte e entorta aros e balões.
Método completo: `data-storytelling/references/storytelling-com-imagem.md`.

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
