---
name: bi-nomenclatura
description: Padrão Corporativo de Nomenclatura para SQL, ETL e modelo semântico Power BI — prefixos Tab/Vw/Pr/Fn/Cns, TabDim/TabFat/TabPon/TabFlt, fronteira entre camada física e semântica, nomes de medida e a convenção de comparativo temporal AV/AA/Δ/Δ%/Δi. Use ao nomear ou renomear tabela, view, procedure, consulta, coluna ou medida, ao escolher prefixo, ao criar alias SQL ou ao nomear medida que compara com o ano anterior.
---

# Padrão Corporativo de Nomenclatura

Técnico para quem desenvolve, intuitivo para quem consome, previsível para quem
mantém. O nome revela o papel do objeto antes de ele ser aberto.

## Regra de ouro

**SQL é estrutura. Power BI é comunicação.** Prefixo técnico só existe na
camada física. Todo objeto **visível** no modelo usa nome de negócio. Colunas
técnicas que sobram (chaves, FKs) ficam ocultas.

Motivo além da leitura humana: Copilot e agentes de IA leem nomes ao pé da
letra. `TabFatVenda` piora respostas em linguagem natural; `Vendas` ajuda.

```
SQL Físico → Views Semânticas → Power Query → Modelo Semântico → Relatórios
```

## 1. Prefixos da camada física

| Prefixo | Objeto | Exemplo |
|---|---|---|
| `Tab` | Tabela | `TabDimCliente`, `TabFatVenda` |
| `Vw` | View | `VwFatVenda` |
| `Pr` | Procedure | `PrAtualizarEstoque` |
| `Fn` | Função (SQL ou M) | `FnCalcularMargem` |
| `Cns` | Consulta de ETL (Power Query) | `CnsClienteTratado` |

## 2. Papel dimensional

| Papel | Padrão | Exemplo |
|---|---|---|
| Dimensão | `TabDimObjeto` | `TabDimCliente`, `TabDimCalendario` |
| Fato | `TabFatEvento` | `TabFatVenda`, `TabFatPedido` |
| Ponte N:N | `TabPonAB` | `TabPonClienteProduto` |
| Monolítica | `TabFltObjeto` | `TabFltVendasCamisetas` |

`TabFlt` é uma tabela achatada que junta fato e dimensões. Serve para escopo
pequeno ou export de terceiros. Quando o volume ou o reuso crescer, migre para
`TabDim`/`TabFat`.

❌ Proibido nome genérico: `TabFatDados`, `TabFatBase`.

## 3. Convenções gerais (camada física)

- Singular: `TabDimCliente` ✔️ │ `TabDimClientes` ❌
- PascalCase: `TabFatVendaMensal` ✔️ │ `tab_fat_venda` ❌
- Sem caractere especial, espaço no início ou fim, ou emoji.

## 4. Campos

| Camada | Padrão | Exemplo |
|---|---|---|
| Física (SQL) | PascalCase por extenso | `CodigoCliente`, `ValorVenda` |
| Semântica (Power BI) | Nome amigável com espaços | `Código do Cliente`, `Valor da Venda` |

❌ Abreviação proibida: `CodCli`, `DtFat`, `VlrTot`.

Em SQL, use sempre `AS [Nome Amigável]` na view semântica: reduz renomeação no
Power Query e antecipa a camada semântica.

```sql
-- View semântica: estrutura física por dentro, nome de negócio por fora
CREATE VIEW VwFatVenda AS
SELECT
    v.CodigoCliente AS [Código do Cliente],
    v.DataVenda     AS [Data da Venda],
    v.ValorVenda    AS [Valor da Venda]
FROM TabFatVenda AS v;
```

## 5. Fronteira física × semântica

| Objeto | Física (SQL/ETL/PQ) | Semântica (visível) |
|---|---|---|
| Dimensão | `TabDimCliente` | `Cliente` (singular) |
| Fato | `TabFatVenda` | `Vendas` (plural aceito em fato) |
| Coluna | `ValorVenda` | `Valor da Venda` |
| Medida | — | `Total de Vendas`, `% vs Meta` |

## 6. Medidas e variáveis DAX

- Medida: nome amigável com espaços — `Total de Vendas`, `Ticket Médio`.
- Variação: `[Base] [Período] ([Unidade])` — `Total de Vendas (ytd)`, `Margem Bruta (%)`.
- Contagem: prefixo `#` — `# Pedidos`, `# Clientes`.
- Variável DAX: camelCase com prefixo `v` — `vTotalVendas`, `vMetaMes`.

## 7. Comparativo temporal: AV/AA/Δ/Δ%/Δi

Padrão oficial para qualquer medida que compara o período corrente com o mesmo
período do ano anterior. Use o símbolo literal, nunca por extenso.

| Sigla | Significado | Medida |
|---|---|---|
| `AV` | Ano Vigente (período corrente) | `Total de Vendas AV` |
| `AA` | Ano Anterior (mesmo período) | `Total de Vendas AA` |
| `Δ` | Variação absoluta (AV − AA) | `Δ Total de Vendas` |
| `Δ%` | Variação percentual | `Δ% Total de Vendas` |
| `Δi` | Farol sobre a variação: ✔️ positivo │ ⚠️ estável │ ❗ negativo | `Δi Total de Vendas` |

```dax
Total de Vendas AV = SUM ( TabFatVenda[ValorVenda] )

Total de Vendas AA =
CALCULATE ( [Total de Vendas AV], SAMEPERIODLASTYEAR ( TabDimCalendario[Data] ) )

Δ Total de Vendas = [Total de Vendas AV] - [Total de Vendas AA]

Δ% Total de Vendas = DIVIDE ( [Δ Total de Vendas], [Total de Vendas AA] )

Δi Total de Vendas =
VAR vVariacao = [Δ% Total de Vendas]
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( vVariacao ), BLANK (),   -- sem ano anterior: sem farol
        vVariacao > 0, "✔️",
        vVariacao = 0, "⚠️",
        "❗"
    )
```

⚠️ `SAMEPERIODLASTYEAR` exige a tabela de calendário marcada como Tabela de Datas.

Os nomes físicos no exemplo (`TabFatVenda`, `TabDimCalendario`) aparecem porque
a referência DAX usa o nome da tabela no modelo. Se as tabelas já foram
renomeadas para a camada semântica, troque por `Vendas[Valor da Venda]` e
`Calendário[Data]`.

## Checklist ao criar ou renomear

1. O prefixo revela o papel? (física)
2. Singular e PascalCase? (física)
3. Objeto visível usa nome de negócio, sem prefixo técnico?
4. Campos semânticos com nome amigável via alias ou renomeação?
5. Nenhuma abreviação críptica sobrou?
6. Comparativos temporais seguem AV/AA/Δ/Δ%/Δi?
