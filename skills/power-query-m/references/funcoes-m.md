# Funções M: confusões comuns

Conferido na [referência oficial de funções M](https://learn.microsoft.com/pt-br/powerquery-m/power-query-m-function-reference)
em 2026-09-23. A referência tem mais de 700 funções: busque lá antes de
escrever uma função customizada.

## Funções que não existem

| Escrita errada | Correto |
|---|---|
| `Number.Max(v1, v2)` | `List.Max({v1, v2})` |
| `Text.Join(lista, ";")` | `Text.Combine(lista, ";")` |
| `Sum(tabela[Coluna])` | `List.Sum(tabela[Coluna])` |
| `If ... Then ... Else` | `if ... then ... else` (M diferencia maiúsculas e minúsculas) |

## Funções que existem, mas fazem outra coisa

| Função | O que faz de verdade | Para o que se costuma querer |
|---|---|---|
| `Table.Max(tabela, "Col")` | Retorna a **linha** (record) com o maior valor em `Col` | Para o **valor** máximo: `List.Max(tabela[Col])` |
| `Table.Min(tabela, "Col")` | Retorna a **linha** com o menor valor | Para o valor mínimo: `List.Min(tabela[Col])` |
| `Number.ToText(n, formato, cultura)` | Converte número em texto **com formato** (ex.: `"N2"`, `"P1"`) | Sem formato, `Text.From(n)` resolve |

⚠️ Versões anteriores desta base listavam `Number.ToText` e `Table.Max` como
inexistentes. As duas existem; a correção acima vale.

## Cultura e locale

`Number.ToText`, `Text.From` e `Number.FromText` aceitam cultura opcional
(ex.: `"pt-BR"`, `"en-US"`). Informe a cultura quando o texto vai para outro
sistema ou quando a fonte usa vírgula decimal: sem ela, o resultado depende da
configuração da máquina que roda o refresh.
