# Exibir unidades = Nenhum nos visuais cabíveis (acrescentar a `powerbi-visuais`)

Regra do autor: **todo visual onde cabe deve ter "Exibir unidades: Nenhum"**
(sem "mil", "mi" ou "bi" abreviando valores). O valor gravado é
`labelDisplayUnits = 1D` (enum **[verificado]** em cartão; as demais posições
foram **[verificadas]** em arquivos que o Desktop gravou em quatro projetos).

## Onde a propriedade fica
| Visual | Objeto e propriedade |
|---|---|
| Cartão | uma entrada `value` **por medida numérica**, com `selector.metadata = "Tabela.Medida"`, `labelDisplayUnits 1D` |
| Cartão com valor de referência | `referenceLabelValue.valueDisplayUnits` |
| Barras, colunas, linhas, área, cascata, área 100% | `valueAxis.labelDisplayUnits` (e `labels.labelDisplayUnits` se houver rótulos de dados); eixo `categoryAxis` só quando é numérico (escalar) |
| Rosca, pizza, funil, medidor | `labels.labelDisplayUnits` |
| **Rosca: valor central** | objeto **`value`**, que **não existe até alguém mexer**: sem ele o centro mostra "mil/mi" |
| Árvore de decomposição | `dataLabels.dataLabelDisplayUnits` |
| Tacômetro (visual personalizado) | `labels` e `calloutValue`, `labelDisplayUnits` |

Não gravam a propriedade em nenhum dos quatro projetos: tabela, matriz, mapa,
nuvem de palavras e visuais personalizados sem esse objeto. Não invente o nome.

## Obrigatório
- Em visual novo, gravar `1D` desde a criação.
- Excluir do cartão as medidas **de texto**: seleção (Categoria, UF, Conceito,
  VocêEstáVendo, "… Selecionado") e a data de atualização.

## Como auditar e corrigir (idempotente)
1. Percorra todos os `visual.json` do relatório, por tipo.
2. Para cada tipo, garanta o objeto da tabela acima; se o objeto existe, faça
   merge da propriedade; se não existe, crie-o só com `labelDisplayUnits`.
3. Grave em UTF-8 sem BOM e CRLF; reabra no Desktop **sem salvar antes**.
4. Reexecute a auditoria: deve acusar 0 pendências.
Dica: o erro mais fácil de deixar passar é a **rosca** (o `value` central).

## Evitar
- Presumir que o cartão cobre "todas as medidas": cada medida nova precisa da
  sua entrada `value`.
- Reduzir a fonte do cartão antes de ver o número por extenso: sem a unidade, o
  valor fica mais largo e pode truncar ("…").
