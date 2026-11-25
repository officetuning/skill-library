# Tabelas, matrizes e cores fixas por valor

Padrões sugeridos pelo autor (convenção, não regra universal). **[a confirmar no
Desktop]** = copie a propriedade de um visual configurado e salvo pelo Desktop
antes de escrever em lote; não deduza o nome nem o valor.

## Tabela e matriz
- **Estilo:** `visualContainerObjects.stylePreset = 'BoldHeader'` ("Cabeçalho em
  negrito"). **[verificado]**
- **Largura das colunas:** `columnHeaders.columnAdjustment = 'growToFit'`
  (na interface, "Aumentar para ajustar"). **[verificado]**
- **Cabeçalho:** fundo na **Cor do tema 1**, que é `ThemeDataColor { ColorId: 2,
  Percent: 0 }` (referência ao tema, não hexadecimal). **`ColorId 0` é branco**:
  o cabeçalho some. **[verificado]**
- **Matriz (`pivotTable`):** mesmos objetos da tabela, inclusive `rowHeaders`.
  **[verificado]**
- **Linhas:** sem faixa no cabeçalho de linha (`values.bandedRowHeaders = false`).
- **Título e subtítulo manuais** (o gráfico usa o padrão do Power BI): título =
  o que é; subtítulo = "medidas por dimensões". Ao **trocar o tipo do visual**,
  zere o título que o tipo anterior deixou.
- **Cabeçalho de coluna:** nome curto no visual (`displayName` + `nativeQueryRef`):
  "Faturado", não "Faturado (AV)"; "Δ%", não "Faturado (Δ%)". Coluna de imagem:
  "Imagem" ou "Foto". Confira **toda** tabela nova: um visual sem `displayName`
  mostra o nome técnico da medida.
- **Nunca grave `"active": false` nas projeções de `Values`** (`tableEx` e
  `pivotTable`): o Desktop passa a mostrar **só a primeira coluna**. Tabela feita
  pelo Desktop não traz `active`; ao gerar por script, copie a projeção sem ele e,
  para esconder uma coluna, tire-a do `queryState`. **[verificado]**
- **Imagens:** `grid.imageHeight`/`imageWidth` (40 px cabem 6 linhas em 464 px).

## Gráficos por Sexo (cor fixa por valor)
O mesmo valor tem a mesma cor em todas as páginas, mesmo quando a ordem das
séries muda.
- **Antes de escolher cor, procure no modelo** uma coluna ou medida tipo "Cor do
  Sexo" ou "Hexa do Sexo" (`grep -ri "Hexa\|Cor d" *.SemanticModel`) e use-a
  (formatação condicional por campo). Vale para qualquer dimensão com coluna
  "Hexa da Área", "Cor do Status" etc.: use as cores do modelo, não invente.
- **Sem coluna de cor:** **Masculino = um azul e Feminino = um vermelho**,
  derivados da paleta do tema e harmoniosos com ela, conferindo contraste AA sobre
  o fundo. Não fixe Masculino na Cor do tema 1 nem Feminino em rosa. Exemplo
  aplicado: Masculino `#1E88E5`, Feminino `#D8344A`.
- **Atenção ao vermelho:** ele costuma sinalizar alerta; aqui o par azul/vermelho
  é escolha do autor, então evite usar o mesmo vermelho para "pior" na mesma página.
- **Como gravar:** um `dataPoint` por valor da categoria (o seletor é o valor, não
  a posição). **[a confirmar no Desktop]**: copie a estrutura de um gráfico em que
  o autor já fixou a cor de um valor.

Ver também `references/exibir-unidades-nenhum.md` e `references/segmentacoes-padrao.md`.
