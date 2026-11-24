# Dica de ferramenta: cartão único com título dinâmico

Substitui o par "cartão só do título + cartão de indicadores". **[verificado]**
em arquivo gravado pelo Desktop.

## Obrigatório
- **Um único `cardVisual`** com o **título ligado a uma medida de seleção**
  (`title.text.expr.Measure`, medida `SELECTEDVALUE ( 'Dim'[Campo], "-" )` na pasta
  Seleção) e o corpo só com **medidas numéricas** (indicadores).
- Layout **Grade** (`orientation 0D`), `autoGrid true`, `columnCount` e
  `maxTiles` iguais ao número de indicadores, `rowCount 1` (ou N linhas se a
  coluna for 1), `labelDisplayUnits 1D` em cada medida.
- **Rodapé padrão de drillthrough** nas Dicas que têm Detalhe irmão (Dica sem
  Detalhe não leva o texto): "🔍 Para explorar o detalhe: clique com o botão direito sobre o dado
  de interesse, selecione Drillthrough/Detalhamento e escolha a página de
  destino no menu." (negrito em "botão direito" e em "Drillthrough/Detalhamento",
  8 pt).
- **Ordem de tabulação:** cartão → gráfico → rodapé.

## Geometria (400×304, margem interna 8)
| Conteúdo | Cartão | Gráfico | Rodapé |
|---|---|---|---|
| 2 a 3 indicadores em 1 linha | `y8`, altura 72 | `y88`, altura 168 | `y256`, altura 48 |
| 5 indicadores de texto em 1 coluna × 5 linhas | `y8`, altura 240 | (sem gráfico) | `y256`, altura 48 |

## Preferir
- Fonte do valor e do rótulo partem do padrão do tema e só diminuem quando
  aparece "…". Texto longo (ex.: "Nome · Cargo") pode truncar em 384 px:
  confira no Desktop e reduza.
- Título que pode ter vários valores ("Feminino · 30 a 39 · …"): deixe
  `titleWrap` ligado e dê ao cartão altura para duas linhas.
- Texto alternativo da Dica: "o título mostra o item em análise; indicadores:
  A, B e C". **Não cite o nome técnico da medida de seleção** (ex.:
  `Você Está Vendo` ou `Estado Selecionado`); quando o cartão só tinha a medida de seleção, escreva
  "exibe o item em análise".

## Evitar
- Cartão solto só com o título, ao lado de outro cartão só com indicadores.
- Cartão só com colunas de texto (sai vazio): use medida de seleção.
- Gravar à mão `autoGrid false` ou colunas automáticas com "Ajustar ao espaço"
  desligado em cartão com vários campos (gera rolagem).
