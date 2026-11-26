# Medidas de tempo nos dois modos

Base de exemplo: `Faturado (AV)` na tabela `Vendas`. Nome e sufixo seguem
`bi-nomenclatura`: `(AA)`, `(Δ)`, `(Δ%)`, `(Δi)` e, para período, a sigla
maiúscula entre parênteses: `(YTD)`, `(QTD)`, `(MTD)`, `(WTD)`, `(12M)`.
Toda medida leva `///` dizendo o período exato.

| Medida | Modo calendário (`'Gregoriano'`) | Modo clássico (`'Calendário'[Data]`) |
|---|---|---|
| Ano anterior | `CALCULATE ( [Faturado (AV)], SAMEPERIODLASTYEAR ( 'Gregoriano' ) )` | `CALCULATE ( [Faturado (AV)], SAMEPERIODLASTYEAR ( 'Calendário'[Data] ) )` |
| Acumulado no ano | `TOTALYTD ( [Faturado (AV)], 'Gregoriano' )` | `TOTALYTD ( [Faturado (AV)], 'Calendário'[Data] )` |
| Acumulado no trimestre | `TOTALQTD ( [Faturado (AV)], 'Gregoriano' )` | `TOTALQTD ( [Faturado (AV)], 'Calendário'[Data] )` |
| Acumulado no mês | `TOTALMTD ( [Faturado (AV)], 'Gregoriano' )` | `TOTALMTD ( [Faturado (AV)], 'Calendário'[Data] )` |
| Acumulado na semana | `TOTALWTD ( [Faturado (AV)], 'Gregoriano' )` | — (só no modo calendário) |
| Mês anterior | `CALCULATE ( [Faturado (AV)], DATEADD ( 'Gregoriano', -1, MONTH ) )` | `CALCULATE ( [Faturado (AV)], DATEADD ( 'Calendário'[Data], -1, MONTH ) )` |
| Semana anterior | `CALCULATE ( [Faturado (AV)], DATEADD ( 'Gregoriano', -1, WEEK ) )` | — |
| Ano anterior inteiro | `CALCULATE ( [Faturado (AV)], PARALLELPERIOD ( 'Gregoriano', -1, YEAR ) )` | `CALCULATE ( [Faturado (AV)], PARALLELPERIOD ( 'Calendário'[Data], -1, YEAR ) )` |

A regra de `(Δ)` e `(Δ%)` é a de
`powerbi-visuais/references/comparativo-ano-anterior.md`.

## Padrão completo (modo calendário)

```dax
/// Faturamento do mesmo período no ano anterior, pelo calendário Gregoriano.
Faturado (AA) =
CALCULATE ( [Faturado (AV)], SAMEPERIODLASTYEAR ( 'Gregoriano' ) )

/// Diferença entre o ano vigente e o ano anterior; em branco se faltar um deles.
Faturado (Δ) =
VAR vAV = [Faturado (AV)]
VAR vAA = [Faturado (AA)]
RETURN
    IF ( NOT ISBLANK ( vAV ) && NOT ISBLANK ( vAA ), vAV - vAA )

/// Variação percentual sobre o módulo do ano anterior; em branco com base zero.
Faturado (Δ%) = DIVIDE ( [Faturado (Δ)], ABS ( [Faturado (AA)] ) )

/// Faturamento acumulado de 1º de janeiro até a última data do contexto.
Faturado (YTD) = TOTALYTD ( [Faturado (AV)], 'Gregoriano' )

/// Faturamento dos últimos 12 meses fechados até a última data do contexto.
Faturado (12M) =
CALCULATE (
    [Faturado (AV)],
    DATESINPERIOD ( 'Gregoriano', MAX ( 'Calendário'[Data] ), -12, MONTH, ENDALIGNED )
)
```

- `DATESINPERIOD` com calendário: a data inicial precisa ter o mesmo tipo da
  coluna principal da categoria Data (`'Calendário'[Data]`, tipo data).
- `ENDALIGNED` evita que um contexto terminando em 28/02 puxe 29 a 31/08 e
  vire uma janela de 7 meses; com `PRECISE` (padrão) isso acontece.

## DATEADD: Extension e Truncation (só modo calendário)

Quando a seleção é mais fina que o deslocamento (dias selecionados, deslocando
por mês):

| Parâmetro | Valor | 25 a 28/02 → +1 mês | 31/03 → −1 mês |
|---|---|---|---|
| Extension | `EXTENDING` (padrão) | 25 a 31/03 | |
| | `PRECISE` | 25 a 28/03 | |
| | `ENDALIGNED` | 28/02 vira 31/03; 27/02 vira 27/03 | |
| Truncation | `BLANKS` (padrão) | | em branco |
| | `ANCHORED` | | 28/02 (ou 29) |

```dax
/// Mês anterior ancorado no último dia válido (31/03 → 28/02).
Faturado (Mês Anterior) =
CALCULATE ( [Faturado (AV)], DATEADD ( 'Gregoriano', -1, MONTH, EXTENDING, ANCHORED ) )
```

## Não aninhar

```dax
-- falha com calendário
PREVIOUSDAY ( PREVIOUSMONTH ( 'Gregoriano' ) )

-- funciona
CALCULATETABLE ( PREVIOUSDAY ( 'Gregoriano' ), PREVIOUSMONTH ( 'Gregoriano' ) )
```

## Manter o filtro de uma coluna relacionada ao tempo

Funções que mudam de nível (`TOTALYTD`, `PARALLELPERIOD`…) limpam o filtro das
colunas relacionadas ao tempo. Para manter, devolva o filtro com `VALUES`:

```dax
Faturado (YTD no Semestre Filtrado) =
CALCULATE ( [Faturado (AV)], DATESYTD ( 'Gregoriano' ), VALUES ( 'Calendário'[Semestre] ) )
```

`DATEADD` e `SAMEPERIODLASTYEAR` só deslocam no mesmo nível e mantêm o filtro
de todas as colunas da tabela.

## UDF com CALENDARREF

Uma função para todos os comparativos, no padrão de `dax-udf`:

```dax
DEFINE
    /// Valor da medida no mesmo período do ano anterior.
    /// @param {MEASUREREF} medida - Medida a comparar.
    /// @param {CALENDARREF} calendario - Calendário de referência ('Gregoriano').
    /// @returns Valor no ano anterior.
    FUNCTION Tempo.AnoAnterior = ( medida : MEASUREREF, calendario : CALENDARREF ) =>
        CALCULATE ( medida, SAMEPERIODLASTYEAR ( calendario ) )

    /// Variação percentual da medida sobre o ano anterior.
    /// @param {MEASUREREF} medida - Medida a comparar.
    /// @param {CALENDARREF} calendario - Calendário de referência.
    /// @returns Variação percentual; em branco se faltar um período ou a base for zero.
    FUNCTION Tempo.VariacaoAnoAnterior = ( medida : MEASUREREF, calendario : CALENDARREF ) =>
        VAR vAtual = medida
        VAR vAnterior = Tempo.AnoAnterior ( medida, calendario )
        RETURN
            IF (
                NOT ISBLANK ( vAtual ) && NOT ISBLANK ( vAnterior ),
                DIVIDE ( vAtual - vAnterior, ABS ( vAnterior ) )
            )

EVALUATE
    SUMMARIZECOLUMNS (
        'Calendário'[Ano],
        "AV", [Faturado (AV)],
        "AA", Tempo.AnoAnterior ( [Faturado (AV)], 'Gregoriano' ),
        "Δ%", Tempo.VariacaoAnoAnterior ( [Faturado (AV)], 'Gregoriano' )
    )
-- AA de cada ano = AV da linha anterior
```

Depois de testada na DAX Query View, **Atualizar modelo** grava as funções.
No modo clássico não existe `CALENDARREF`: use `COLUMNREF` com
`'Calendário'[Data]`.

## Teste rápido

```dax
EVALUATE
    SUMMARIZECOLUMNS (
        'Calendário'[Ano/Mês],
        "AV", [Faturado (AV)],
        "AA", [Faturado (AA)],
        "YTD", [Faturado (YTD)]
    )
ORDER BY 'Calendário'[Ano/Mês]
```

Confira três linhas à mão: o AA de um mês igual ao AV do mesmo mês um ano
antes, e o YTD de janeiro igual ao AV de janeiro.
