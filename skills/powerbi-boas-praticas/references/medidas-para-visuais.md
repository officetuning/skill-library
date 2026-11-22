# Medidas que sustentam o visual

Padrões DAX que evitaram telas incoerentes num relatório de fluxo de caixa com
painel global de filtros.

## Obrigatório
- **Valor com sinal vs valor absoluto.** Se recebimentos são positivos e
  pagamentos negativos, a medida-base é o **saldo**. Para ranking e dimensionamento
  use uma medida absoluta: `SUMX ( Fato, ABS ( Fato[Valor] ) )`.
- **Medida que sobrescreve o filtro de uma coluna que também é segmentação**
  (`CALCULATE ( [M], Fato[Tipo] = "X" )`) ignora a segmentação e mostra números
  que não se explicam entre si. Quando o filtro deve ser respeitado, use
  `KEEPFILTERS`.
- **Documente com `///`** toda medida e coluna e trate o **dicionário** como
  artefato gerado (regenere a cada mudança).

## Preferir
| Necessidade | Padrão |
|---|---|
| Ranking que respeita as segmentações | `RANKX ( ALLSELECTED ( Dim ), [Medida] )`: recomeça em 1 a cada filtro; com `ALL` deixa buracos |
| Saldo acumulado no período | `CALCULATE ( [Saldo], FILTER ( ALLSELECTED ( Calendario ), Calendario[Data] <= MAX ( Calendario[Data] ) ) )`; começa em zero no início do período |
| Valor de seleção para título | `SELECTEDVALUE ( Dim[Campo], "-" )`; pasta `Seleção`; nome = nome do campo |
| Atributo do lado "um" a partir do lado "muitos" | `LOOKUPVALUE ( Um[Atributo], Um[Chave], SELECTEDVALUE ( Muitos[Chave] ) )` |
| Número como texto no título | `FORMAT ( SELECTEDVALUE ( Cal[Ano] ), "0" )` |

> **Exceção à regra 6.1.** A regra 6.1 proíbe `FORMAT()` dentro da medida porque
> devolve texto. A exceção vale só para **medida de texto usada como título**
> (cartão, título dinâmico, card da seleção na página Detalhe), que nunca entra em eixo, soma
> ou ordenação. Medida numérica continua com a propriedade Formato.

## Avisar na descrição
- Calendário que termina em "hoje": valores por vencimento futuro ficam fora.
- Medida acumulada: o ponto inicial é zero, não o saldo de abertura.
- Medida que respeita ou ignora uma segmentação específica.

## Armadilha de nomes
Medida com o mesmo nome de uma coluna de outra tabela é permitida, mas um
cartão com `Nome` ambíguo no visual confunde: nomeie pelo papel (`Transação`
medida de seleção vs `Transações` contagem) e deixe a descrição dizer a
diferença.
