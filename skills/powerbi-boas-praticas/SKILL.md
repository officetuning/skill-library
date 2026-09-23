---
name: powerbi-boas-praticas
description: Auditoria e boas práticas de modelo semântico Power BI — 76 regras de performance, DAX, prevenção de erros, manutenção, nomenclatura, formatação e relatório, com a severidade oficial do Best Practice Analyzer. Use quando o usuário disser modelo lento, modelo pesado, otimizar Power BI, revisar DAX, auditar modelo, relacionamento bidirecional, M:M, RLS lento, checklist antes de publicar ou severidade de regra. Para rodar o BPA por linha de comando use bi-qa-documentacao.
---

# Boas práticas de modelo semântico Power BI

## Como auditar

1. Peça o modelo (TMDL, print do diagrama ou lista de medidas) antes de opinar.
2. Classifique cada achado pela regra em `references/regras-bpa.md` e cite o
   número e a severidade.
3. Ordene por severidade: Alta 🔴 → Média 🟠 → Baixa 🔵. Agrupe por seção.
4. Entregue cada achado no formato:
   **regra (nº + severidade) → impacto → correção com código pronto → onde
   aplicar (Power Query, Tabular Editor ou DAX)**.

| Pedido | Comece por |
|---|---|
| Modelo lento | Seção 1, regras 1.3, 1.5, 1.9, 1.18 |
| Revisar ou escrever DAX | Seção 2 |
| Checklist pré-publicação | Seções 3 e 4 |
| Padronizar nomes | Seção 5 + skill `bi-nomenclatura` |
| Formato de medida ou coluna | Seção 6 |
| Revisar relatório ou página | Seção 7 + skill `powerbi-visuais` |

## Severidade Alta 🔴 (sempre primeiro)

- 1.18 M:M em tabela com RLS dinâmico
- 3.1 Coluna de dados sem coluna de origem
- 3.2 Objeto com expressão vazia
- 3.3 `USERELATIONSHIP` e RLS na mesma tabela
- 3.4 Tipos diferentes nas colunas de um relacionamento
- 3.5 / 3.6 Caractere inválido em nome ou descrição
- 3.7 `IsAvailableInMdx = false` em coluna necessária para MDX (Excel)
- 6.1 Medida sem format string
- 6.2 Sumarização automática em coluna numérica que não é métrica

## Regras que valem sempre

**Obrigatório**
- Star schema. Desnormalize snowflake no Power Query.
- Tabela de datas dedicada, contígua, marcada como Tabela de Datas, com
  data/hora automática desabilitada.
- `DIVIDE` em vez de `/`. `TREATAS` em vez de `INTERSECT`. Filtro por coluna em
  vez de `FILTER` sobre a tabela inteira.
- Medida explícita para toda métrica. Colunas de fato e FKs ocultas.
  `SummarizeBy = None` em IDs, anos e códigos. Format string em toda medida visível.
- Prefixo técnico na camada física, nome de negócio na semântica (skill
  `bi-nomenclatura`).

**Preferir**
- Transformação pesada na fonte. `RELATED` em coluna calculada vira merge no
  Power Query.
- `Int64` para chave, `Decimal` para valor. Nunca `Double`.
- Data e hora em colunas separadas. Meses em coluna despivotados. Texto longo truncado.
- Relacionamento unidirecional; `CROSSFILTER` pontual na medida que precisa.
- Auditar com Tabular Editor (Best Practice Analyzer) e DAX Studio (View Metrics).

**Evitar**
- `IFERROR` para esconder causa. Medida duplicada ou medida que só repete outra.
- Relacionamento inativo que nenhuma medida ativa.
- Mais de 8–10 visuais por página. Página com rolagem vertical.

## Fonte e atribuição

- Seções 1 a 6 (62 regras): repositório oficial
  [microsoft/Analysis-Services/BestPracticeRules](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules)
  (licença MIT), só modelo semântico. A severidade segue o valor oficial; uma
  auditoria de ago/2026 corrigiu 29 divergências.
- Seção 7 (13 regras) e a regra 2.2: Best Practices Analyser do **Measure
  Killer** (Gregor Brunner). Ao citar, atribua ao Measure Killer, não à Microsoft.
- A regra 2.2 não tem fonte oficial confirmada; foi mantida por analogia com a 2.1.

Catálogo completo das 76 regras: `references/regras-bpa.md`.
Ideias de conteúdo a partir das regras: `references/ideias-de-pauta.md`.
