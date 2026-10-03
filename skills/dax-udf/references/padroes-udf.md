# Padrões de UDF DAX

Todos os exemplos rodam na DAX Query View. Troque `Vendas`, `Cliente` e
`'Calendário'` pelas tabelas do modelo.

## 1. TABLE VAL × TABLE EXPR

```dax
DEFINE
    /// Recebe a tabela já filtrada: o ALL de dentro não tem efeito.
    FUNCTION Contagem.LinhasAgora = ( t : TABLE VAL ) =>
        COUNTROWS ( CALCULATETABLE ( t, ALL ( 'Calendário' ) ) )

    /// Recebe a expressão: o ALL de dentro remove o filtro de ano.
    FUNCTION Contagem.LinhasDepois = ( t : TABLE EXPR ) =>
        COUNTROWS ( CALCULATETABLE ( t, ALL ( 'Calendário' ) ) )

EVALUATE
    ROW (
        "VAL (só 2025)", CALCULATE ( Contagem.LinhasAgora ( Vendas ), 'Calendário'[Ano] = 2025 ),
        "EXPR (todos os anos)", CALCULATE ( Contagem.LinhasDepois ( Vendas ), 'Calendário'[Ano] = 2025 )
    )
```

## 2. Iterar e recalcular: MEASUREREF × SCALAR EXPR

```dax
DEFINE
    /// Soma a medida dos N maiores clientes.
    /// @param {MEASUREREF} medida - Medida a ranquear e somar
    /// @param {INT64} [n] - Quantidade de clientes; padrão 10
    FUNCTION Vendas.TopClientesMedida =
        ( medida : MEASUREREF, n : INT64 = 10 ) =>
            SUMX ( TOPN ( n, VALUES ( Cliente[Nome do Cliente] ), medida ), medida )

    /// Aceita qualquer expressão escalar: o CALCULATE garante a transição
    /// de contexto em cada cliente.
    /// @param {SCALAR} valorExpr - Medida ou expressão a ranquear e somar
    /// @param {INT64} [n] - Quantidade de clientes; padrão 10
    FUNCTION Vendas.TopClientes =
        ( valorExpr : SCALAR EXPR, n : INT64 = 10 ) =>
            SUMX (
                TOPN ( n, VALUES ( Cliente[Nome do Cliente] ), CALCULATE ( valorExpr ) ),
                CALCULATE ( valorExpr )
            )

EVALUATE
    ROW (
        "Top 10 (medida)", Vendas.TopClientesMedida ( [Total de Vendas] ),
        "Top 5 (expressão)", Vendas.TopClientes ( SUM ( Vendas[Valor da Venda] ), 5 )
    )
```

Sem o `CALCULATE` em volta de `valorExpr`, `SUM ( ... )` devolveria o total
geral em cada cliente.

## 3. Checagem de tipo no corpo

| Categoria | Funções |
|---|---|
| Numérico | `ISNUMERIC`, `ISNUMBER` |
| Inteiro | `ISINT64`, `ISINTEGER` |
| Decimal fixo | `ISDECIMAL`, `ISCURRENCY` |
| Ponto flutuante | `ISDOUBLE` |
| Texto | `ISSTRING`, `ISTEXT` |
| Lógico | `ISBOOLEAN`, `ISLOGICAL` |
| Data/hora | `ISDATETIME` |

```dax
DEFINE
    /// Tamanho do texto, ou BLANK se não for texto.
    FUNCTION Texto.Tamanho = ( s ) =>
        IF ( ISSTRING ( s ), LEN ( s ), BLANK () )

EVALUATE
    { Texto.Tamanho ( "Power BI" ), Texto.Tamanho ( 123 ) }
-- 8 e BLANK
```

`TABLEOF ( ref )` devolve a tabela de uma coluna, medida ou calendário;
`NAMEOF ( ref )` devolve o nome do objeto como texto. Úteis com `ANYREF` e
`COLUMNREF`.

## 4. Formato dinâmico: `Formato.Escala`

Cadeia de formato com escala automática (mil, mi, bi). A cadeia usa os
símbolos invariantes (vírgula de milhar, ponto decimal); o Power BI exibe
conforme o idioma do modelo. Cada vírgula no fim da parte numérica divide
por mil.

```dax
DEFINE
    /// Cadeia de formato com escala automática (mil, mi, bi).
    /// Use no formato dinâmico da medida: Formato.Escala ( SELECTEDMEASURE () ).
    /// @param {NUMERIC} valor - Valor que será exibido
    /// @param {INT64} [decimais] - Casas decimais; padrão 1
    /// @returns Cadeia de formato (texto) para a propriedade de formato
    FUNCTION Formato.Escala =
        ( valor : NUMERIC, decimais : INT64 = 1 ) =>
            VAR _abs = ABS ( valor )
            VAR _casas = IF ( decimais > 0, "." & REPT ( "0", decimais ), "" )
            RETURN
                SWITCH (
                    TRUE (),
                    ISBLANK ( valor ), "#,0",
                    _abs >= 1000000000, "#,0" & _casas & ",,,"" bi""",
                    _abs >= 1000000, "#,0" & _casas & ",,"" mi""",
                    _abs >= 1000, "#,0" & _casas & ","" mil""",
                    "#,0" & _casas
                )

EVALUATE
    ADDCOLUMNS (
        { 950, 12345, 4567890, 1234567890 },
        "Formato", Formato.Escala ( [Value] ),
        "Exibido", FORMAT ( [Value], Formato.Escala ( [Value] ) )
    )
-- Esperado em pt-BR: 950,0 | 12,3 mil | 4,6 mi | 1,2 bi
```

Uso em várias medidas, cada uma com **Formato → Dinâmico**:

| Medida | Expressão de formato |
|---|---|
| Total de Vendas | `Formato.Escala ( SELECTEDMEASURE () )` |
| Custo Total | `Formato.Escala ( SELECTEDMEASURE () )` |
| # Pedidos | `Formato.Escala ( SELECTEDMEASURE (), 0 )` |

Mudou a regra (ex.: passar a usar "k" em vez de "mil")? Altere só a função.

⚠️ No visual, **Unidades de exibição = Nenhum**. Para desligar em todos os
visuais, use um tema de relatório.

⚠️ O `EVALUATE` acima testa a cadeia com `FORMAT`. Confirme também num cartão
e num gráfico de barras antes de aplicar no modelo de produção.

## 5. UDF no TMDL

```tmdl
createOrReplace

    /// Aplica imposto sobre um valor.
    /// @param {NUMERIC} valor - Valor antes do imposto
    function 'Fiscal.ComImposto' = (valor : NUMERIC, aliquota : NUMERIC = 0.1) => valor * (1 + aliquota)
```

Em `.pbip`, as funções ficam em `definition/functions.tmdl`. A TMDL view
mostra a função pronta para editar: clique com o botão direito no nó
**Functions** do Model Explorer → *Script TMDL to*.

## Fontes

- [DAX user-defined functions](https://learn.microsoft.com/dax/best-practices/dax-user-defined-functions)
- [Dynamic format strings for measures](https://learn.microsoft.com/power-bi/create-reports/desktop-dynamic-format-strings)
- [TMDL overview](https://learn.microsoft.com/analysis-services/tmdl/tmdl-overview)
