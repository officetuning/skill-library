# Cartões, títulos e rótulos

Lições de um relatório real em PBIP/PBIR. **[verificado]** = confirmado em
arquivo gravado pelo Desktop; **[regra do autor]** = decisão de projeto.

## Cartões (`cardVisual`)

**Obrigatório**
- **Fonte de valor e rótulo partem do tamanho padrão do tema e só diminuem
  quando aparece "…" ou o texto não cabe.** Reduza em passos, testando com o
  **maior valor possível** (não o do filtro atual). Não fixe o tamanho de
  antemão. Estimativa útil: valores monetários chegam a ~16 caracteres
  (`(R$ 509.623.123)`). [regra do autor]
- **Vários campos: "Ajustar ao espaço" ligado**, ou número de colunas fixo com
  `maxTiles` igual ao número de campos. Colunas automáticas com Ajustar ao
  espaço desligado geram rolagem. [regra do autor]
- **Unidade de exibição "nenhuma"** em valores monetários. [regra do autor]
- **Estilo (fundo, borda, barra de destaque) vem do tema**; não grave à mão.
  Exceção de espaçamento, regra do autor **[verificado]**: preenchimento do
  contêiner 14 (topo) / 16 / 16 / 16, `cellPadding 16` e vão de 16 entre cartões;
  **altura padrão do cartão de Grandes Números: 168 sem etiquetas de referência
  e 240 com** (seção abaixo).
- **Cartão de nicho ou segmentação sobre fundo do Builder:** tela de fundo,
  fronteira visual, efeitos, cabeçalho e título **desligados**. Cartão de
  storytelling (sobre a imagem): sem título, fundo, borda nem rótulo.
- **Reset de título:** ao converter um visual para outro tipo, zere o título e o
  subtítulo que o tipo anterior deixou.
- **Nunca** um cartão só com colunas de texto de tabelas diferentes: sai
  vazio. Use medidas de seleção (`SELECTEDVALUE`, `LOOKUPVALUE`). [verificado]

**Preferir**
- Lista vertical de indicadores (dica): Blocos, **Grade**, 1 coluna × N linhas,
  `maxTiles` N. Disposição Grade grava `orientation = 0D`. [verificado]
- Faixa de indicadores no topo da página, com título personalizado.

**Evitar**
- Deduzir o enum de `orientation` de outro projeto: `1D` e `2D` não são Grade;
  propriedade ausente = Horizontal. Peça ao usuário configurar no Desktop,
  salvar, e leia o arquivo.

## Altura padrão do cartão de Grandes Números e o que fica abaixo [regra do autor]

| O cartão tem... | Altura |
|---|---|
| **Layout das etiquetas de referência** (AA, Δ%, `referenceLabel*`) | **240** |
| só valor e rótulo | **168** |

Tudo em **múltiplos de 8** (a grade de 8 px do Background Builder vale para x, y,
largura e altura). Coordenadas do Builder: cartão em y=128; **os visuais abaixo começam 16 px depois** (`S = 128 + altura + 16`)
e **terminam em y=1064**.

| Cartão | Os visuais começam em | Duas linhas de gráfico |
|---|---|---|
| 168 | **y=312** | 312 a 680 (368) e 696 a 1064 (368) |
| 240 | **y=384** | 384 a 712 (328) e 728 a 1064 (336) |

- Linha 1 = `piso8((1064 − S − 16) ÷ 2)`; linha 2 = o resto. No cartão de 240, 664 ÷ 2
  = 332 não é múltiplo de 8: use 328 e 336.
- Visual que ocupa as duas linhas (mapa, tabela alta): de `S` até 1064 (752 no
  cartão de 168).
- Ao mudar a altura do cartão de uma página, **redistribua os visuais abaixo na
  mesma passada** (script: classifique cada visual por seu y antigo em "alto",
  "linha 1" e "linha 2") e confira que nada sai da grade nem se sobrepõe.
- **Preenchimento interno do bloco** (`layout` com `selector id default`):
  `paddingIndividual false` e `paddingUniform 10L`. Com 0 o rótulo cola no topo.
- **Cartão com etiquetas de referência:** `visualContainerObjects.spacing.
  spaceAboveDivider` em **4** (16 consome a altura e corta o rótulo) e
  `label.position 'aboveValue'`.
- Largura e x iguais em todas as páginas (376 e 1528 no corpo; 16 e 1888 no
  Detalhe). Cartão deslocado 8 px dos visuais abaixo é defeito, não estilo.

## Títulos e subtítulos

| Visual | Título |
|---|---|
| Gráficos (barras, colunas, área, cascata, rosca, mapa) | **Padrão do Power BI**; não gravar título personalizado |
| Cartão / indicador | Personalizado (descreve o conjunto); em dica, ligado à medida de seleção |
| Tabela, matriz, árvore hierárquica | Personalizado, **modelado como gráfico**: título = o que é; subtítulo = "medidas por dimensões" |
| Navegação, botões, segmentações, cartão de última atualização | **Sem título** |
| Visual dentro de um "nicho" que o fundo já nomeia | **Sem título** |

- Subtítulo curto, para não quebrar em duas linhas: cite só as medidas
  principais ("Movimentado e Realizado por pessoa").
- **Nunca** `title.show = true` sem `text`: gera tabela/matriz sem nome. [verificado]
- Título ligado a medida: `text = { expr: { Measure: … } }`. [verificado]

## Rótulos de campo no visual
- O visual mostra o nome mais curto que o contexto permite (princípio em
  `bi-nomenclatura`, seção 6): sem sufixos técnicos ("Ano/Mês (Abreviado)" →
  "Ano/Mês"), sem "Nome do/da" ("Nome da UF" → "UF"), sem a entidade que o
  visual ou a página já dizem ("Latitude do Município" → "Latitude" no mapa;
  "Cidade do Cliente" → "Cidade" no Detalhe do Cliente; "Ano do Calendário" →
  "Ano") e sem o nome da medida repetido sob o título ("Faturado (AV)" → "AV").
- Não encurte quando duas entidades dividem o visual ("Cidade do Cliente" ao
  lado de "Cidade da Loja") ou quando o nome curto colide com outro campo.
- Faça no visual: na projeção, `displayName` **e** `nativeQueryRef`; `queryRef`
  não muda; não renomeie a coluna no modelo. [verificado]
- Não sobrescreva `displayName` que o autor já definiu.

## Teste antes de entregar
Estimar (não adivinhar) largura de rótulos e valores e altura por linha; dizer
ao usuário que o render não foi visto; pedir captura de tela.
