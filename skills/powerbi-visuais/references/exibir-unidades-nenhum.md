# Exibir unidades = Nenhum nos visuais cabíveis

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
| **Rosca: valor central** | ligar em **`centerValue.show`**; a unidade vai no objeto **`value`**, que **não existe até alguém mexer**: sem ele o centro mostra "mil/mi" |
| Árvore de decomposição | `dataLabels.dataLabelDisplayUnits` |
| Tacômetro (visual personalizado) | `labels` e `calloutValue`, `labelDisplayUnits` |

Não gravam a propriedade em nenhum dos quatro projetos: tabela, matriz, mapa,
nuvem de palavras e visuais personalizados sem esse objeto. Não invente o nome.

## Obrigatório
- Em visual novo, gravar `1D` desde a criação.
- Excluir do cartão as medidas **de texto**: seleção (Categoria, UF, Conceito,
  `<Campo> Selecionado(a)`, "Você Está Vendo") e a data de atualização.

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

## Rosca com valor central [verificado, nov/2026]
Em relatório salvo com `visualContainer/2.15.0`, o Desktop grava a chave do valor
central em `objects.centerValue[0].properties.show`. Ligar não basta: o número saiu
como "99,07 mil" até receber `objects.value[0].properties.labelDisplayUnits = 1D`.
Grave as duas coisas (e `labels.labelDisplayUnits`, se houver rótulos) e peça a
conferência na tela: o ajuste de unidade é tarefa de quem edita, não do autor.
