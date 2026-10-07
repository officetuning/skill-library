---
name: powerbi-boas-praticas
description: Auditoria e boas práticas de modelo semântico e relatório Power BI — 90 regras de performance, DAX, prevenção de erros, manutenção, nomenclatura, formatação, relatório e storytelling, com a severidade do Best Practice Analyzer e do Measure Killer. Use quando o usuário disser modelo lento, modelo pesado, otimizar Power BI, revisar DAX, auditar modelo, relacionamento bidirecional, M:M, RLS lento, checklist antes de publicar ou severidade de regra, pontuação do Measure Killer, PBI-Inspector ou revisão de página de relatório. Para rodar o BPA por linha de comando use bi-qa-documentacao.
---

# Boas práticas de modelo semântico e relatório Power BI

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
| Mesma lógica repetida em várias medidas | Skill `dax-udf` (transformar em UDF) |
| Alterar o modelo direto via MCP | Skill `powerbi-mcp` antes de aplicar |
| Checklist pré-publicação | Seções 3 e 4 |
| Padronizar nomes | Seção 5 + skill `bi-nomenclatura` |
| Formato de medida ou coluna | Seção 6 |
| Revisar relatório ou página | Seção 7 + skill `powerbi-visuais` |
| Revisar a comunicação do relatório | Seção 8 (revisão manual) + skill `data-storytelling` |
| Explicar a pontuação do Measure Killer | "Pontuação do Measure Killer", abaixo |

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
- Relatório: 7.2 visuais por página, 7.6 rolagem vertical, 7.8 campos por visual, 7.13 medidas implícitas
- Comunicação: 8.1 ideia central da página, 8.2 título como conclusão

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
- Mais de 20 visuais por página ou mais de 6 campos num visual.
- Página com rolagem vertical. A página padrão é Full HD (1920 × 1080).

## Fonte e atribuição

- Seções 1 a 6 (62 regras): repositório oficial
  [microsoft/Analysis-Services/BestPracticeRules](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules)
  (licença MIT), só modelo semântico. A severidade segue o valor oficial; uma
  auditoria de ago/2026 corrigiu 29 divergências.
- Seção 7, regras 7.1 a 7.11 (11 regras): regras base do
  [PBI-Inspector](https://github.com/NatVanG/PBI-Inspector), de Nat Van Gulck
  (licença MIT), projeto da comunidade sem suporte da Microsoft. O suporte a
  PBIR está no repositório PBI-Inspector V2.
- Regras 7.12, 7.13, 7.14 e 2.2: extensões do Best Practices Analyser do
  **Measure Killer** (Gregor Brunner), que adota as regras do PBI-Inspector.
  Ao citar, atribua a cada fonte, não à Microsoft.
- Seção 8 (13 regras): checklist de revisão manual baseado em *Storytelling
  with Data*, de Cole Nussbaumer Knaflic (Wiley, 2015); a 8.9 vem de
  *Information Dashboard Design*, de Stephen Few. Nenhuma ferramenta pontua
  essas regras.
- A severidade de relatório segue a do Measure Killer.

## Limites padrão das regras de relatório

| Regra | Limite | Parâmetro no PBI-Inspector |
|---|---|---|
| 7.1 Páginas por relatório | 10 | `paramMaxNumberOfPagesPerReport` |
| 7.2 Visuais por página | 20 | `paramMaxVisualsPerPage` |
| 7.3 Visuais com filtro TopN por página | 4 | `paramMaxTopNFilteringPerPage` |
| 7.4 Visuais com filtro avançado por página | 4 | `paramMaxAdvancedFilteringVisualsPerPage` |
| 7.6 Altura da página | 1080 px (Full HD) | `paramMaxAllowedPageHeight` (padrão 720) |
| 7.8 Campos por visual | 6 | fixo na regra |
| 7.12 Fatias de pizza ou rosca | até 4 | regra do Measure Killer |
| 7.14 Indicadores por relatório | 10 | regra do Measure Killer |

**Rolagem vertical não é recomendada.** O que mudou foi o tamanho padrão da
página, de HD (1280 × 720) para Full HD (1920 × 1080). O PBI-Inspector e o
Measure Killer ainda verificam 720 px: em relatórios Full HD, ajuste o
parâmetro para 1080 ou desconsidere esse alerta. Não trate como violação uma
página Full HD sem rolagem.

## Pontuação do Measure Killer

Quanto menor, melhor. Severidade: 1 (baixa), 2 (média), 3 (alta).

- **Modelo:** severidade × violações × log10(artefatos do modelo).
- **Relatório:** severidade × violações. Em regra com limite, cada violação
  vale severidade × (1 + valor encontrado − limite).

| Veredito | Modelo | Relatório |
|---|---|---|
| Power BI Pro | abaixo de 75 | abaixo de 50 |
| Good | 75 a 300 | 50 a 100 |
| Ok | 301 a 600 | 100 a 150 |
| Poor | 601 a 900 | 150 a 250 |
| Awful | 901 a 1.200 | 250 a 300 |
| Power BI Criminal | acima de 1.200 | 300 ou mais |

Exemplo: modelo com 300 artefatos (log10 ≈ 2,48) e 10 violações de uma regra
de severidade 2 → 2 × 10 × 2,48 ≈ 50 pontos. Página com 25 visuais contra o
limite de 20, severidade 3 → 3 × (1 + 25 − 20) = 18 pontos.

Catálogo completo das 90 regras: `references/regras-bpa.md`.
Ideias de conteúdo a partir das regras: `references/ideias-de-pauta.md`.
