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

## Cartão único com AA e Δ% (`cardVisual`, altura 240) [verificado]
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

## Armadilhas e variações [nov/2026]

- **`Δ` não vale em nome de variável DAX.** `VAR vΔ = ...` dá "Token inválido"
  (o erro aponta a posição do `Δ`), e o Desktop, ao abrir, remove dos visuais as
  formatações que apontavam para a medida inválida (cor do Δ% do cartão). Use
  `vDelta`. O **nome da medida** pode ter `Δ` (`'Faturamento (Δ)'`); só o
  identificador de variável não pode.
- **Medida de fluxo do período** (contratados, demitidos: contam eventos entre duas
  datas) não usa `SAMEPERIODLASTYEAR`. Desloque as duas pontas do período com
  `EDATE` e ignore o filtro do calendário:

  ```dax
  Contratados (AA) =
  VAR vInicio  = MIN ( 'Calendário'[Data Referência] )
  VAR vTermino = MAX ( 'Calendário'[Data Referência] )
  RETURN
      IF ( NOT ISBLANK ( vInicio ) && NOT ISBLANK ( vTermino ),
           CALCULATE ( [Colaboradores],
                       REMOVEFILTERS ( 'Calendário' ),
                       'Colaborador'[Entrada] >= EDATE ( vInicio, -12 ),
                       'Colaborador'[Entrada] <= EDATE ( vTermino, -12 ) ) )
  ```
  O `IF` protege a linha "(Em branco)" que o calendário ganha com datas de saída
  em branco. Medida de **estoque** (headcount no fim do período) usa a data de
  fechamento deslocada, não o intervalo.
- **"Menor é melhor"** (demitidos, prazo de entrega, atraso): o farol e a cor se
  invertem. `(Δi)`: `Δ > 0` vira ❗ e `Δ < 0` vira ✔️; `(Δ Cor)`: positivo vira a
  cor negativa do tema. A descrição `///` diz que a subida é ruim.
- **Contagem simples não leva Δ%** quando a base é zero: `DIVIDE` e `ABS` na
  base já devolvem vazio.
- Teste os dois lados: com a segmentação de data em "Este ano", `(AA)` precisa
  devolver o mesmo período do ano anterior (confira contra um filtro manual).
