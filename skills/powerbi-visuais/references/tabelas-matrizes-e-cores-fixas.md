# Tabelas, matrizes e cores fixas por valor

Padrões sugeridos pelo autor (convenção, não regra universal). **[a confirmar no
Desktop]** = copie a propriedade de um visual configurado e salvo pelo Desktop
antes de escrever em lote; não deduza o nome nem o valor.

## Tabela e matriz
- **Largura das colunas:** `columnHeaders.columnAdjustment = 'growToFit'`
  (na interface, "Aumentar para ajustar"). As colunas ocupam a largura do visual.
- **Cabeçalho:** negrito, com fundo na **Cor do tema 1** (referência ao tema, não
  hexadecimal fixo), para o relatório inteiro mudar junto com o tema.
- **Matriz:** aplique o mesmo estilo também em `rowHeaders`; sem isso, o
  cabeçalho de linha fica fora do padrão da coluna.
- **Tipo do visual:** no tema base aparece só `tableEx`. Para a matriz
  (`pivotTable`), os mesmos objetos **[a confirmar no Desktop]**: leia um
  `pivotTable` gravado antes de replicar.

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
