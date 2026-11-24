---
name: bi-nomenclatura
description: Padrão Corporativo de Nomenclatura para SQL, Power Query e modelo semântico Power BI, alinhado ao padrão oficial da Microsoft — prefixos Tab/Vw/Pr/Fn no SQL, Cns e Lista nas consultas não carregadas, grupos de consultas por papel (Fatos, Dimensões, Pontes, Monolíticas, Internas, Funções, Parâmetros, Listas), tabela do modelo com nome de negócio, coluna com nome amigável completo, medida com nome curto e sem "Total", comparativo (AV)/(AA)/(Δ)/(Δ%)/(Δi), nome encurtado no visual e aspas por linguagem. Use ao nomear ou renomear tabela, view, procedure, consulta, grupo de consultas, coluna, medida ou função, ao criar alias SQL, ao nomear medida que compara com o ano anterior ou ao rotular campo num visual.
---

# Padrão Corporativo de Nomenclatura

Técnico para quem desenvolve, intuitivo para quem consome, previsível para quem
mantém. O nome revela o papel do objeto antes de ele ser aberto.

## Regra de ouro

**SQL é estrutura. Power BI é comunicação.** O prefixo técnico mora no SQL e
nas consultas do Power Query que **não** carregam no modelo. A consulta que
carrega **é** a tabela do modelo e leva nome de negócio, como manda o
[padrão oficial da Microsoft](https://github.com/microsoft/skills-for-fabric/blob/main/skills/semantic-model-authoring/references/naming-conventions.md)
("não use prefixos técnicos como Fact, Dim"). No modelo, o papel da tabela
aparece no **grupo de consultas**, não no nome.

```
SQL (TabFatVenda) → Power Query (Fatos/Preparo: CnsVendaTratado) → Modelo (Vendas) → Visual (rótulo curto)
```

| Camada | Tabela / consulta | Coluna | Acento |
|---|---|---|---|
| SQL físico | `TabFatVenda`, `VwFatVenda` | `ValorVenda` | ❌ |
| Power Query, não carregada | `CnsVendaTratado`, `ListaUFsAtendidas`, `Texto.RemoveAcentos` | — | ❌ no nome de função e parâmetro |
| Modelo (consulta carregada) | `Vendas`, `Cliente`, `Calendário` | `Valor da Venda` | ✔️ |
| Visual | — | `Cliente` (de `Nome do Cliente`) | ✔️ |

## 1. SQL físico

| Prefixo | Objeto | Exemplo |
|---|---|---|
| `Tab` | Tabela | `TabDimCliente`, `TabFatVenda` |
| `Vw` | View | `VwFatVenda` |
| `Pr` | Procedure | `PrAtualizarEstoque` |
| `Fn` | Função SQL | `FnCalcularMargem` |

| Papel | Padrão | Exemplo |
|---|---|---|
| Dimensão | `TabDimObjeto` | `TabDimCliente`, `TabDimCalendario` |
| Fato | `TabFatEvento` | `TabFatVenda`, `TabFatPedido` |
| Ponte N:N | `TabPonAB` | `TabPonClienteProduto` |
| Monolítica | `TabFltObjeto` | `TabFltVendasCamisetas` |

- Singular, PascalCase, **sem acento**, sem espaço e sem caractere especial
  (collation e ferramentas de terceiros).
- Campo por extenso: `CodigoCliente`, `ValorVenda`. ❌ `CodCli`, `DtFat`, `VlrTot`.
- ❌ Nome genérico: `TabFatDados`, `TabFatBase`.
- `TabFlt` é tabela achatada (fato + dimensões) para escopo pequeno ou export
  de terceiros. Quando o volume ou o reuso crescer, migre para estrela.

Na view semântica, já entregue o nome amigável com `AS [Nome Amigável]`:

```sql
CREATE VIEW VwFatVenda AS
SELECT
    v.CodigoCliente AS [Código do Cliente],
    v.DataVenda     AS [Data da Venda],
    v.ValorVenda    AS [Valor da Venda]
FROM TabFatVenda AS v;
```

## 2. Power Query: consultas e grupos

| Grupo | Conteúdo | Nome da consulta |
|---|---|---|
| Fatos | Fatos carregadas | `Vendas`, `Pedidos` (plural) |
| Dimensões | Dimensões carregadas | `Cliente`, `Produto`, `Calendário` (singular) |
| Pontes | Pontes N:N carregadas | `Cliente Produto` |
| Monolíticas | Tabelas achatadas carregadas | `Vendas Camisetas` |
| Internas | Apoio do relatório | `Atualização`, `Dicionário` |
| Funções | Funções M | `Texto.RemoveAcentos`, `Validacao.CPF` |
| Parâmetros | Parâmetros de consulta | `RangeStart`, `RangeEnd`, `Servidor`, `Banco` |
| Listas | Consultas que devolvem **lista** M | `ListaUFsAtendidas` |
| `<Grupo>/Preparo` | Staging e tratamento, sem carregamento | `CnsClienteStaging`, `CnsClienteTratado` |

- Consulta carregada = nome de negócio, com espaço e acento.
- Consulta não carregada = nome formal PascalCase sem espaço: `Cns` para
  preparo, `Lista` + conteúdo no plural para lista. Lista convertida em tabela
  e carregada vai para o grupo do papel dela, com nome de negócio.
- Função M: `Grupo.Acao`, como as nativas (`Table.AddColumn`) e como a UDF DAX;
  sem acento; parâmetros em camelCase sem acento; português por padrão
  (inglês só em função feita para outro idioma). Detalhes: skill `power-query-m`.
- O grupo fica gravado no TMDL (`queryGroup`) e é dele que a documentação
  automática tira o papel da tabela (skill `bi-qa-documentacao`).

## 3. Colunas

- Nome amigável **completo** e **único entre tabelas**: `Código do Cliente`,
  `Nome do Cliente`, `Endereço do Cliente`, `Valor da Venda`. Nome único evita
  ambiguidade para o Copilot e agentes de dados.
- Chaves e FKs também com nome amigável, e **ocultas**.
- Coluna que só alimenta medida (valor de fato) fica oculta e não tem o mesmo
  nome de uma medida.
- Sem abreviação; acrônimo de negócio consagrado (CPF, UF, NPS) pode, e vai
  definido na descrição.
- Sem emoji, tabulação, quebra de linha ou espaço no início ou fim.

## 4. Medidas

- **Nome de negócio mais curto** que diga o que mede: `Faturado`,
  `Ticket Médio`, `Margem Bruta (%)`.
- **Sem "Total"**: toda medida já é um total. ❌ `Total de Vendas` → ✅ `Faturado`.
  Exceção: quando "total" é o conceito calculado (`% do Total`, `Total Acumulado`).
- Nome diferente de tabela e de coluna: medida `Vendas` com tabela `Vendas`
  confunde a DAX e o Copilot.
- Contagem com `#`: `# Pedidos`, `# Clientes`.
- Variação: `[Base] ([Período ou Unidade])`, sigla **maiúscula, sem ponto,
  entre parênteses**: `Faturado (YTD)`, `Margem Bruta (%)`. Parênteses ficam
  reservados para período e unidade.
- Toda medida com descrição `///` que diga exatamente o que soma ("valor bruto
  das notas emitidas, sem devoluções"): o nome curto depende dela.
- A medida mora na tabela a que pertence (`Faturado` em `Vendas`), organizada
  por pasta de exibição; não há tabela única de medidas.
- Variável DAX: camelCase com prefixo `v` (`vTotal`, `vMetaMes`).
- UDF DAX: `Grupo.Acao`, sem acento (skill `dax-udf`).

## 5. Comparativo temporal: (AV)/(AA)/(Δ)/(Δ%)/(Δi)

Toda medida comparada existe nas duas versões, `(AV)` e `(AA)`; não há
medida-base sem sufixo. Use o símbolo literal.

| Sigla | Significado | Medida |
|---|---|---|
| `(AV)` | Ano Vigente (período corrente) | `Faturado (AV)` |
| `(AA)` | Ano Anterior (mesmo período) | `Faturado (AA)` |
| `(Δ)` | Variação absoluta (AV − AA) | `Faturado (Δ)` |
| `(Δ%)` | Variação percentual | `Faturado (Δ%)` |
| `(Δi)` | Farol: ✔️ positivo │ ⚠️ estável │ ❗ negativo | `Faturado (Δi)` |

```dax
Faturado (AV) = SUM ( Vendas[Valor da Venda] )

Faturado (AA) =
CALCULATE ( [Faturado (AV)], SAMEPERIODLASTYEAR ( 'Calendário'[Data] ) )

Faturado (Δ) = [Faturado (AV)] - [Faturado (AA)]

Faturado (Δ%) = DIVIDE ( [Faturado (Δ)], [Faturado (AA)] )

Faturado (Δi) =
VAR vVariacao = [Faturado (Δ%)]
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( vVariacao ), BLANK (),   -- sem ano anterior: sem farol
        vVariacao > 0, "✔️",
        vVariacao = 0, "⚠️",
        "❗"
    )
```

As variações ficam em ordem alfabética logo abaixo da base no painel Dados.
O farol mora no **valor**, não no nome. ⚠️ `SAMEPERIODLASTYEAR` exige o
calendário marcado como Tabela de Datas. Com a inteligência de tempo baseada
em calendário (prévia), a referência passa a ser o calendário:
`SAMEPERIODLASTYEAR ( 'Gregoriano' )`; qual modo usar e os padrões YTD, MTD,
WTD e 12M estão na skill `calendario-inteligencia-tempo`.

## 6. Nome no visual: tire o que o contexto já diz

O modelo guarda o nome completo; o visual mostra o mais curto que o contexto
permite. Renomeie **só no visual** ("Renomear para este visual"; no PBIR,
`displayName` + `nativeQueryRef` na projeção, ver `powerbi-visuais`).

| Cenário | Modelo | Visual |
|---|---|---|
| Nome da entidade em eixo, filtro, tabela ou matriz | `Nome do Cliente` | `Cliente` |
| Atributo num visual sobre a entidade | `Latitude do Município` (mapa) | `Latitude` |
| Página de Detalhe ou Dica da entidade | `Cidade do Cliente` | `Cidade` |
| Níveis do calendário | `Ano do Calendário` | `Ano` |
| Variações agrupadas sob o título da medida | `Faturado (AV)`, `Faturado (AA)` | `AV`, `AA`, `Δ%` |
| Visual de uma medida só, com o nome no título | Série `Faturado` | sem repetir |

**Não encurte** quando duas entidades dividem o visual (`Cidade do Cliente` ao
lado de `Cidade da Loja`) ou quando o nome curto colide com outro campo
(`Código do Cliente` ao lado de `Cliente`).

## 7. Aspas por linguagem

| Linguagem | Quando | Exemplo |
|---|---|---|
| DAX | Nome de tabela com espaço, acento ou caractere especial | `'Calendário'[Data]`, `'Cliente Produto'[Peso]` |
| M | Nome de **consulta** com espaço ou acento | `#"Calendário"`; campo entre colchetes dispensa: `[Data da Venda]` |
| TMDL | Só com espaço, `.`, `=`, `:` ou `'` (acento não exige) | `table Calendário`, `measure 'Faturado (AV)'` |

Sem aspas onde elas são exigidas, a fórmula dá erro.

## 8. Nomes e IA (Copilot)

A Microsoft não pede prefixo nem nome curto para o Copilot; pede nomes
legíveis, sem abreviação críptica, **sem campo de mesmo nome em tabelas
diferentes**, com descrição e sinônimos
([Optimize your semantic model for Copilot](https://learn.microsoft.com/power-bi/create-reports/copilot-evaluate-data),
[Use Copilot with semantic models](https://learn.microsoft.com/power-bi/create-reports/copilot-semantic-models)).
Instruções de IA, esquema de dados para IA e respostas verificadas ficam na
tela **Prep data for AI**.

## Checklist ao criar ou renomear

1. SQL: prefixo de papel, singular, PascalCase, sem acento?
2. Consulta não carregada com `Cns`/`Lista`/`Grupo.Acao`; consulta carregada com nome de negócio?
3. Toda consulta no grupo do seu papel, preparo em `<Grupo>/Preparo`?
4. Coluna com nome amigável completo e único; chaves ocultas?
5. Medida curta, sem "Total", sem colidir com tabela ou coluna, com `///`?
6. Comparativo com `(AV)` e `(AA)` e as variações entre parênteses?
7. Rótulo do visual encurtado pelo contexto, sem mexer no modelo?
8. Aspas certas em DAX, M e TMDL?
