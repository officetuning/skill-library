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
- **Imagens:** `grid.imageHeight`/`imageWidth` (40 px cabem 6 linhas em 464 px).

## Gráficos por Sexo (cor fixa por valor)
O mesmo valor tem a mesma cor em todas as páginas, mesmo quando a ordem das
séries muda.
- **Masculino:** `ThemeDataColor` com `ColorId = 2` (cor do tema).
- **Feminino:** `#C2185B` (rosa escuro), com contraste AA sobre fundo claro.
- **Por que não vermelho:** vermelho carrega significado de alerta ou resultado
  negativo (regra "cor só com significado") e se confunde com pior/meta não
  atingida; também piora para quem tem daltonismo.
- **Como gravar:** um `dataPoint` por valor da categoria (o seletor é o valor, não
  a posição). **[a confirmar no Desktop]**: copie a estrutura de um gráfico em que
  o autor já fixou a cor de um valor.

Ver também `references/exibir-unidades-nenhum.md` e `references/segmentacoes-padrao.md`.
