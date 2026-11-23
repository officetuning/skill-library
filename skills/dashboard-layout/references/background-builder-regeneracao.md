# Regenerar o fundo sem quebrar o relatório (acrescentar a `background-builder-ciclo.md`)

Lições de regenerar os PNGs depois de mudar identidade, ordem de páginas ou
nome. **[verificado]** = visto em arquivo gravado pelo Desktop ou na saída do
Builder.

## Obrigatório
- **Refazer a posição do navegador de páginas depois de toda regeneração.** O
  menu do PNG é alinhado à esquerda a partir do bloco da marca (H1 + H2): H1
  mais curto ou mais longo desloca todas as células. No projeto 02 o menu foi
  para x440 e, com o novo H1, para x424; no projeto 03 foi de x496 para x528.
  [verificado]
- **Conferir a ordem das páginas.** Ao regenerar, o Builder pode reordenar o
  menu conforme a lista de páginas da ficha. Compare com `pages.json ›
  pageOrder` e ajuste: o `pageNavigator` segue a ordem das páginas visíveis.
  [verificado]
- **Conferir a ficha depois de gerar.** A ficha regenerada pode descartar
  edições feitas só no `.md` (classificação 5W2H de um filtro, correção de
  texto). Edite no Builder ou reaplique e confira o diff.

## Como alinhar o menu (procedimento)
1. Abra um PNG de corpo e anote o centro de cada rótulo do menu.
2. **Passo** = distância entre centros (deve ser múltiplo de 8, entre 80 e 200).
3. `x = primeiro centro − passo / 2` e `largura = itens × passo`.
4. Aplique em todas as páginas com menu (`y16`, altura 96).
Exemplo: 9 itens, passo 136, primeiro centro 492 → `x424`, largura `1224`.

## Preferir
- **Cada página de Detalhe tem a sua cópia registrada do mesmo PNG.**
  Sobrescreva todas ao trocar o fundo (no projeto 03, três cópias de
  "Detalhe"). Para achá-las, liste `RegisteredResources` e procure o mesmo
  tamanho de arquivo. [verificado]
- **Depois de renomear a página**, o fundo registrado continua com o nome
  antigo no `page.json`: está certo. Troque o conteúdo do arquivo, não o nome
  registrado, e não mexa em `report.json`.
- O H1 mais curto libera espaço: o título do hero pode caber em uma linha.
  Reveja a quebra no PNG de Início.

## Evitar
- Mudar H1, H2 ou tagline só no texto da ficha e esquecer o JSON embutido.
- Presumir que o menu continua alinhado depois de mudar o nome de uma página:
  a largura do rótulo pode estourar a célula (ex.: "Decomposição" em 136 px).
