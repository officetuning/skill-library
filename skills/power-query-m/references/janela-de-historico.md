# Janela de histórico: quantos anos o modelo carrega

Para quando o relatório deve mostrar só os últimos N anos (muitas vezes N anos
**fiscais** completos).

**Verificação:** a parte SQL foi instalada em um banco e comparada mês a mês (N = 2,
ano fiscal de outubro a setembro). **A parte M não foi aberta no Desktop**, e o
comportamento do Incremental Refresh descrito aqui vem da documentação e da leitura
do TMDL: **não foi testado no Service**.

## Pergunta antes de corrigir

> Este limite de datas é uma regra de negócio?

Um calendário curto pode parecer defeito e ser decisão: mudança de plano de contas,
de centros de custo ou de sistema torna o passado incomparável. Pergunte a intenção;
se ela existe, o achado é outro: **a regra vale em todas as tabelas?**

## Regras

- **Um só lugar para a regra.** No SQL, uma view de uma linha com início e fim; para
  fonte em arquivo, uma expressão M compartilhada. Datas fixas repetidas em cada
  consulta se desencontram.
- **Fim exclusivo:** `>= início` e `< fim`, em fatos **e no calendário**. Com `<=`
  sobra um dia e nasce um ano a mais no filtro, e o erro pode ficar escondido até a
  fonte do calendário passar a ter aquela data.
- **Todo fato respeita a janela**, inclusive os agregados e os que não têm data no
  visual. Fato sem filtro traz o passado para uma data em branco, que soma nos
  totais.
- **Dimensão derivada de fato** (pedido, por exemplo) herda a janela; confira se isso
  é o desejado.
- **Período gravado em segmentação** não anda com a janela: o relatório abre no ano
  antigo e, um dia, vazio.

## E o Incremental Refresh?

| Comportamento | Consequência |
|---|---|
| Os parâmetros `RangeStart` e `RangeEnd` são substituídos pelo Service só nas partições das tabelas **com política**; nas demais vale o valor do modelo, ou a tabela carrega tudo | Calendário filtrado por eles pode ficar menor que os fatos |
| A janela em **anos** guarda anos civis completos mais o corrente; a partição que sai desse período é removida do modelo | Não expressa ano fiscal: meses de fora da janela fiscal continuam no modelo até o ano civil inteiro sair |
| Partição fora do período de atualização não é relida | Exclusão ou correção feita na origem para um mês antigo não chega ao modelo |

Com poucos anos e uma regra que muda com a data, avalie **não usar** o incremental e
atualizar tudo. Meça antes: se a view relê a origem inteira a cada partição (janela
`ROW_NUMBER` sem o período, `UNION` de várias views), o incremental já não economiza
o que parece.

Fontes:
[Incremental refresh](https://learn.microsoft.com/power-bi/connect-data/incremental-refresh-overview) ·
[Filtrar os dados](https://learn.microsoft.com/power-bi/connect-data/incremental-refresh-configure#filter-data) ·
[Partições](https://learn.microsoft.com/power-bi/connect-data/incremental-refresh-xmla#partitions)

## SQL: a janela em uma view

Exemplo: ano fiscal vigente e anterior, começando em 1º de outubro, no horário de
Brasília. Para outro início, troque `10`; para N anos, troque o `1` subtraído por
`N - 1`.

```sql
CREATE OR ALTER VIEW bi.VwDimJanela
AS
SELECT
    DATEFROMPARTS(a.AnoInicioVigente - 1, 10, 1)   AS [Data Inicial],
    DATEFROMPARTS(a.AnoInicioVigente + 1, 10, 1)   AS [Data Final Exclusiva]
FROM (
    SELECT YEAR(h.Hoje) - CASE WHEN MONTH(h.Hoje) >= 10 THEN 0 ELSE 1 END AS AnoInicioVigente
    FROM (
        SELECT CAST(SYSDATETIMEOFFSET() AT TIME ZONE 'E. South America Standard Time' AS date) AS Hoje
    ) AS h
) AS a;
```

Nos fatos, `CROSS JOIN` com ela (a view devolve **sempre uma linha**):

```sql
FROM dbo.Vendas AS v
CROSS JOIN bi.VwDimJanela AS j
WHERE v.DataVenda >= j.[Data Inicial]
  AND v.DataVenda <  j.[Data Final Exclusiva]
```

- Em view que deduplica com `ROW_NUMBER`, se o período não está na partição da
  janela, filtre **depois** de escolher a linha, para não mudar o resultado.
- Confirme o aceite como em `bi-qa-documentacao`
  (`references/checkup-banco-sql.md`, "Aceite de mudança em view").

## M: a mesma regra para fonte em arquivo

Expressão compartilhada `Janela.Fiscal`, sem carregamento. Ela não lê nenhuma fonte,
o que evita combinar fontes (`Formula.Firewall`).

```m
let
    // Brasília; DateTimeZone.RemoveZone mantém a hora de -3 mesmo no Service (UTC)
    vAgora = DateTimeZone.RemoveZone(DateTimeZone.SwitchZone(DateTimeZone.UtcNow(), -3)),
    vHoje = Date.From(vAgora),
    vAnoInicioVigente = Date.Year(vHoje) - (if Date.Month(vHoje) >= 10 then 0 else 1)
in
    [Inicio = #date(vAnoInicioVigente - 1, 10, 1), FimExclusivo = #date(vAnoInicioVigente + 1, 10, 1)]
```

```m
NaJanela = Table.SelectRows(
    Anterior,
    each [Data] <> null and Date.From([Data]) >= #"Janela.Fiscal"[Inicio] and Date.From([Data]) < #"Janela.Fiscal"[FimExclusivo]
)
```

⚠️ O filtro `<> null` **tira as linhas sem data**. Confira se alguma tabela dependia
delas. `Date.From` aceita coluna de data ou de data e hora; sem ele, comparar data e
hora com `#date` dá erro no M.

O `-3` é um **deslocamento fixo**: onde há horário de verão, a virada pode errar em
uma hora. O SQL usa o nome do fuso, que já considera o horário de verão; no M, ajuste
o deslocamento se a sua região adotar.

## Testar a virada

Rode a fórmula com datas fixas antes de confiar nela:

| Hoje | Início | Fim exclusivo |
|---|---|---|
| 30/09/2027 | 01/10/2025 | 01/10/2027 |
| 01/10/2027 | 01/10/2026 | 01/10/2028 |
| 30/09/2028 | 01/10/2026 | 01/10/2028 |
| 01/10/2028 | 01/10/2027 | 01/10/2029 |
