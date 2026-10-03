---
name: dax-udf
description: Funções DAX definidas pelo usuário (UDF) no padrão OfficeTuning — onde criar (DAX Query View, TMDL view, Model Explorer), sintaxe FUNCTION, tipos de parâmetro (ANYVAL, SCALAR, TABLE, MEASUREREF, COLUMNREF, TABLEREF, CALENDARREF), VAL × EXPR, parâmetro opcional, documentação com /// @param, nome com ponto, teste com EVALUATE, objeto function no TMDL e UDF em formato dinâmico de medida. Use ao criar, revisar, documentar ou depurar uma UDF, ao transformar lógica repetida em várias medidas numa função, ao escolher entre VAL e EXPR ou ao montar formato dinâmico reutilizável. Para nomear medidas use bi-nomenclatura; para regras de DAX use powerbi-boas-praticas.
---

# UDF DAX

Uma UDF empacota lógica DAX com nome e parâmetros para reutilizar em medidas,
colunas calculadas, cálculos visuais, formatos dinâmicos e outras UDFs.
GA no Desktop e no Service desde **junho/2026**; exige nível de
compatibilidade **1702** ou superior.

Antes de escrever uma função do zero, procure na **Code Library UDF DAX**
(functionlibrary.officetuning.com.br/dax/udf/biblioteca): calendário,
comparativo AV/AA/Δ (`Delta.*`), datas fiscais, feriados, texto, estatística.

## Fluxo de trabalho

1. **Escreva e teste na DAX Query View** com `DEFINE FUNCTION … EVALUATE`.
   Nada vai para o modelo até você aprovar.
2. **Grave no modelo**: CodeLens *Update model: Add new function* (uma) ou
   *Update model with changes* (todas). Na TMDL view, botão *Apply*.
3. **Use** na medida e confira o resultado num visual.
4. Em `.pbip`, a função fica em `definition/functions.tmdl` e entra no Git
   como qualquer medida (ver `tmdl-pbir`).

## Anatomia (padrão da casa)

```dax
DEFINE
    /// Aplica imposto sobre um valor.
    /// @param {NUMERIC} valor - Valor antes do imposto
    /// @param {NUMERIC} [aliquota] - Alíquota opcional; padrão 0,1 (10%)
    /// @returns O valor com imposto
    FUNCTION Fiscal.ComImposto =
        ( valor : NUMERIC, aliquota : NUMERIC = 0.1 ) =>
            valor * ( 1 + aliquota )

EVALUATE
    ROW (
        "Padrão", Fiscal.ComImposto ( 100 ),
        "Alíquota 20%", Fiscal.ComImposto ( 100, 0.2 )
    )
-- 110 e 120
```

| Regra | Padrão OfficeTuning |
|---|---|
| Nome da função | `Grupo.Acao` com ponto para agrupar: `Vendas.Margem`, `Delta.AA`, `Formato.Escala`. Sem espaço, sem ponto no início/fim, sem nome de função nativa ou palavra reservada |
| Nome do parâmetro | camelCase, sem ponto. Parâmetro `EXPR` termina em `Expr` (`valorExpr`) para quem chama saber que será calculado dentro da função |
| Documentação | `///` acima da função com `@param {TIPO} nome - descrição`, `[nome]` para opcional e `@returns`. Comentário `//` não aparece no IntelliSense |
| Tipo | O mais específico que resolve: o IntelliSense e a validação recusam o argumento errado já na chamada |
| Teste | Todo exemplo traz um `EVALUATE` com o resultado esperado em comentário |

## Tipos de parâmetro

Forma: `nome : [tipo] [subtipo] [modo] [= padrão]`. Sem nada, vale `ANYVAL VAL`.

| Família | Tipo | Aceita | Modo |
|---|---|---|---|
| Valor | `ANYVAL` | Escalar ou tabela | `VAL` (padrão) ou `EXPR` |
| Valor | `SCALAR` + subtipo | Escalar | `VAL` (padrão) ou `EXPR` |
| Valor | `TABLE` | Tabela | `VAL` (padrão) ou `EXPR` |
| Expressão | `ANYREF` | Qualquer referência | sempre `EXPR` |
| Expressão | `MEASUREREF` / `COLUMNREF` / `TABLEREF` / `CALENDARREF` | Referência daquele tipo | sempre `EXPR` |

Subtipos de `SCALAR` (declarar o subtipo já implica `SCALAR`): `INT64`,
`DECIMAL`, `DOUBLE`, `NUMERIC` (qualquer dos três), `STRING`, `DATETIME`,
`BOOLEAN`, `VARIANT`. Tipos de valor convertem implicitamente (`"5"` vira 5
num `INT64`); tipos de expressão não.

## VAL × EXPR — a decisão que mais erra

| Modo | Quando calcula | Herda do chamador |
|---|---|---|
| `VAL` | Uma vez, antes de entrar na função | Contexto de linha **e** de filtro |
| `EXPR` | Dentro da função, onde aparece (pode ser várias vezes, em outro contexto) | Só o contexto de filtro |

- Use `VAL` para número, texto, data, tabela pronta.
- Use `EXPR` quando a função precisa **mudar o contexto** da expressão
  (`CALCULATE`, `ALL`, iterar e recalcular por linha).
- Dentro de iterador, `MEASUREREF` faz transição de contexto sozinha;
  `SCALAR EXPR` com `SUM(...)` **não** — envolva em `CALCULATE ( valorExpr )`.

Exemplos completos (TABLE VAL × EXPR, TOP N com MEASUREREF, checagem de tipo):
`references/padroes-udf.md`.

## UDF em formato dinâmico de medida

O caso que mais economiza: a mesma lógica de formato em várias medidas.
Na medida: **Formato → Dinâmico** e, na expressão de formato:

```dax
Formato.Escala ( SELECTEDMEASURE () )
```

A medida continua **numérica** (gráficos funcionam), ao contrário de `FORMAT()`
dentro da medida, que devolve texto. No visual, deixe **Unidades de exibição =
Nenhum**, senão o visual reescala por cima. Código da `Formato.Escala` e
variações: `references/padroes-udf.md`.

## Onde usar e cuidados

| Onde | Cuidado |
|---|---|
| Medida | — |
| Coluna calculada | A função deve devolver sempre o mesmo tipo; fixe com `CONVERT` |
| Cálculo visual | Só enxerga campos do visual; sem IntelliSense para UDF |
| Outra UDF | Sem recursão |
| Formato dinâmico | Unidades de exibição = Nenhum no visual |

## Limitações (confira a data no Microsoft Learn)

- Sem recursão (nem mútua), sem sobrecarga, sem tipo de retorno declarado.
- Não dá para ocultar, colocar em pasta de exibição nem traduzir a função.
- Não funciona em modelo sem tabelas.
- Conexão dinâmica: medidas de relatório chamam a UDF, sem IntelliSense.
  Modelo composto: medidas do modelo local não chamam UDF do modelo de origem.
- ⚠️ **OLS não passa para a função.** Não exponha objeto protegido em nome ou
  descrição de função.
- Nome sem tabela (`[Valor]`) é lido como medida: dentro de UDF, sempre
  qualifique colunas (`Vendas[Valor]`).
- Parâmetro `EXPR` não usado no corpo nunca é calculado.

## Listar e auditar

```dax
EVALUATE INFO.USERDEFINEDFUNCTIONS ()   -- nome, expressão, estado, erro
```

Metadados completos podem exigir permissão de escrita ou de administrador do
modelo, conforme o host. `State = Error` + `ErrorMessage` mostram
função quebrada depois de renomear tabela ou coluna.

## Fontes

- [DAX user-defined functions](https://learn.microsoft.com/dax/best-practices/dax-user-defined-functions)
- [FUNCTION (DAX)](https://learn.microsoft.com/dax/function-statement-dax)
- [UDF no Power BI Desktop](https://learn.microsoft.com/power-bi/transform-model/desktop-user-defined-functions-overview)
- [Dynamic format strings](https://learn.microsoft.com/power-bi/create-reports/desktop-dynamic-format-strings)
- [INFO.USERDEFINEDFUNCTIONS](https://learn.microsoft.com/dax/info-userdefinedfunctions-function-dax)
