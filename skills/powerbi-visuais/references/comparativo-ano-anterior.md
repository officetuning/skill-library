# Comparativo com o ano anterior: medidas e cartão

Padrão do Finanças e do Vendas, confirmado no Desktop. **[verificado]** =
renderizou e foi gravado pelo Desktop. Nomes seguem `bi-nomenclatura`, seção 5
(`(AV)`, `(AA)`, `(Δ)`, `(Δ%)`, `(Δi)`).

## Família de medidas (por medida-base `X`)
| Medida | DAX | Observação |
|---|---|---|
| `X (AV)` | a própria medida-base, explícita | pasta de exibição `X Δ` |
| `X (AA)` | `CALCULATE ( [X (AV)], SAMEPERIODLASTYEAR ( 'Calendário'[Data] ) )` | exige a tabela de datas marcada |
| `X (Δ)` | `IF ( NOT ISBLANK ( vAV ) && NOT ISBLANK ( vAA ), vAV - vAA )` | **guarda**: sem os dois períodos não há variação (evita −100% nas pontas da série) |
| `X (Δ%)` | `DIVIDE ( [X (Δ)], ABS ( [X (AA)] ) )` | `ABS` mantém o sinal coerente com base negativa |
| `X (Δi)` | `SWITCH ( TRUE (), ISBLANK ( vΔ ), BLANK (), vΔ > 0, "✔️", vΔ = 0, "⚠️", "❗" )` | farol pelo sinal do **Δ absoluto**, não do Δ%, que pode inverter com base negativa |
| `X (Δ Cor)` | mesmo `SWITCH`, devolvendo o hex do sentimento do tema (positivo, neutro, negativo) | formatação condicional por medida; `BLANK()` mantém a cor padrão |

- Formatos: moeda `"R$"\ #,0;("R$"\ #,0);"R$"\ #,0` com
  `annotation PBI_FormatHint = {"currencyCulture":"pt-BR"}`; Δ%
  `#,0.00%;(#,0.00%);#,0.00%` (negativo entre parênteses).
- O Performance Comercial usa 🟩 🟥 🟨 ⬜ e `Δ%` sem `ABS`; a convenção da casa é a
  acima (✔️ ⚠️ ❗ e `ABS`).

## Cartão único com AA e Δ% (`cardVisual`, altura 216) [verificado]
Uma faixa de "Grandes Números" com várias medidas, cada uma com o comparativo
embaixo (valor do ano anterior e variação com farol).
- Em cada medida: `referenceLabel` com `(AA)` (order 0) e `(Δ%)` (order 1);
  `referenceLabelTitle` com texto "AA" e "Δ%"; `referenceLabelDetail` com
  `detailValue = (Δi)` e `detailFontColor =` medida `(Δ Cor)`;
  `cardCalloutArea.show = false` na medida principal; `label.position =
  'aboveValue'`; `accentBar` na cor 3 do tema; `divider`.
- Título "Indicadores do período" no contêiner, preenchimento 14/16/16/16 e
  `cellPadding 16` (ver `cartoes-e-titulos.md`).
- **Copie o objeto de um cartão que o Desktop já salvou**: escrever do zero
  erra enums e posições.
- Visual de apoio, mesma família: matriz Ano > Mês com `(AV)`, `(AA)`, `(Δ)`,
  `(Δ%)` e `(Δi)` (largura 592) e a sazonal Ano × Mês (920).

## Ícones no cartão
Ver `imagens-e-icones.md`.
