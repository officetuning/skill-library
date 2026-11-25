# Medidas que sustentam o visual

Padrões DAX que evitaram telas incoerentes num relatório de fluxo de caixa com
painel global de filtros.

## Obrigatório
- **Valor com sinal vs valor absoluto.** Se recebimentos são positivos e
  pagamentos negativos, a medida-base é o **saldo**. Para ranking e dimensionamento
  use uma medida absoluta: `SUMX ( 'Fato', ABS ( 'Fato'[Valor] ) )`.
- **Medida que sobrescreve o filtro de uma coluna que também é segmentação**
  (`CALCULATE ( [M], 'Fato'[Tipo] = "X" )`) ignora a segmentação e mostra números
  que não se explicam entre si. Quando o filtro deve ser respeitado, use
  `KEEPFILTERS`.
- **Documente com `///`** toda medida e coluna e trate o **dicionário** como
  artefato gerado (regenere a cada mudança).

## Preferir
| Necessidade | Padrão |
|---|---|
| Ranking que respeita as segmentações | `RANKX ( ALLSELECTED ( Dim ), [Medida] )`: recomeça em 1 a cada filtro; com `ALL` deixa buracos |
| Ranking robusto com código e nome (foto na linha) | `IF ( HASONEVALUE ( Dim[Código] ) && NOT ISBLANK ( [Medida] ), RANKX ( ALLSELECTED ( Dim[Código], Dim[Nome] ), [Medida], , DESC, DENSE ) )`: código + nome no `ALLSELECTED` resolve a linha com foto; total e linhas vazias ficam em branco. Variante só com nome: `IF ( ISINSCOPE ( nome ), CALCULATE ( RANKX ( ALLSELECTED ( nome ), [Medida] ), REMOVEFILTERS ( código, imagem, e-mail ) ) )`; sem o `REMOVEFILTERS` todos viram 1 |
| Participação no contexto das segmentações | `DIVIDE ( [Medida], CALCULATE ( [Medida], ALLSELECTED ( 'Tabela' ) ) )` |
| Item líder (nome do campeão, para cartão de storytelling) | `MAXX ( TOPN ( 1, ADDCOLUMNS ( VALUES ( col ), "@M", [Medida] ), [@M], DESC, col, ASC ), col )`; pasta `Storytelling`, formato `@`. Muda com qualquer filtro |
| Saldo acumulado no período | `CALCULATE ( [Saldo], FILTER ( ALLSELECTED ( 'Calendário' ), 'Calendário'[Data] <= MAX ( 'Calendário'[Data] ) ) )`; começa em zero no início do período |
| Valor de seleção para título | `SELECTEDVALUE ( 'Dim'[Campo], "-" )`; pasta `Seleção`; nome `<Campo> Selecionado(a)`, diferente da coluna |
| Atributo do lado "um" a partir do lado "muitos" | `LOOKUPVALUE ( 'Um'[Atributo], 'Um'[Chave], SELECTEDVALUE ( 'Muitos'[Chave] ) )` |
| Número como texto no título | `FORMAT ( SELECTEDVALUE ( 'Calendário'[Ano] ), "0" )` |

> **Exceção à regra 6.1.** A regra 6.1 proíbe `FORMAT()` dentro da medida porque
> devolve texto. A exceção vale só para **medida de texto usada como título**
> (cartão, título dinâmico, card da seleção na página Detalhe), que nunca entra em eixo, soma
> ou ordenação. Medida numérica continua com a propriedade Formato.

## Idade e tempo em anos completos
`DATEDIFF ( nascimento; hoje; YEAR )` conta **viradas de ano-calendário**, não anos
completos: errou cerca de 49% dos casos numa base de pessoas. Use a data de
aniversário:
`VAR _h = TODAY ( ) RETURN DATEDIFF ( [Nascimento]; _h; YEAR ) - IF ( DATE ( YEAR ( _h ); MONTH ( [Nascimento] ); DAY ( [Nascimento] ) ) > _h; 1; 0 )`
(vale para Idade, Tempo de Casa e tempo de contrato). Numa coluna calculada,
`TODAY()`/`UTCTODAY()` fixam o valor no último refresh e `UTCTODAY` usa o fuso UTC:
próximo da meia-noite no Brasil o dia já virou. Para número sempre atual, prefira
medida; para faixa etária, use a coluna e avise a data de atualização.

## Avisar na descrição
- Calendário que termina em "hoje": valores por vencimento futuro ficam fora.
- Medida acumulada: o ponto inicial é zero, não o saldo de abertura.
- Medida que respeita ou ignora uma segmentação específica.

## Armadilha de nomes
Medida com o mesmo nome de uma coluna ou tabela é aceita pelo motor, mas o
padrão (`bi-nomenclatura`) não permite: o leitor da DAX e o Copilot confundem.
Nomeie pelo papel (`Transação Selecionada` medida de seleção vs `# Transações`
contagem) e deixe a descrição dizer a diferença.
