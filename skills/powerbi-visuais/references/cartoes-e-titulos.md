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
- Sem sufixos técnicos ("(Abreviado)") e sem prefixos de modelo ("Nome do/da
  …"): "Ano/Mês (Abreviado)" → "Ano/Mês"; "Nome da UF" → "UF".
- Faça no visual: na projeção, `displayName` **e** `nativeQueryRef`; `queryRef`
  não muda; não renomeie a coluna no modelo. [verificado]
- Não sobrescreva `displayName` que o autor já definiu.

## Teste antes de entregar
Estimar (não adivinhar) largura de rótulos e valores e altura por linha; dizer
ao usuário que o render não foi visto; pedir captura de tela.
