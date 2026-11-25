# Regenerar o fundo sem quebrar o relatório

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

## Onde ficam as segmentações no fundo novo (medir, não adivinhar)
Ao incluir, tirar ou reordenar um filtro, os retângulos "fantasma" da barra
lateral mudam de lugar (o que vem depois desce 80 px por linha, mais o vão do
cabeçalho 5W2H). Meça no PNG novo:

```
python data-storytelling/scripts/medir_png.py retangulos fundo.png --ref 100,492
```
Saída: `y 272-391 (altura 120)`, `y 472-511 (altura 40)`, ... todas em x 40, largura
296. Compare com o PNG antigo: o filtro incluído aparece como um retângulo novo e os
seguintes ficam deslocados. Atualize, **em todas as páginas de corpo**, o `y` das
segmentações que se moveram e crie a nova (clone uma segmentação de texto, troque o
campo, o `syncGroup.groupName`, o `displayName` e o texto alternativo; `tabOrder` =
maior da página + 1000).
- Só a barra lateral muda (verifique por pixel): menu, cabeçalho e Sobre ficam como
  estão, e **as Dicas não mudam**.
- Medidas e visuais ligados ao novo filtro precisam responder a ele (a medida lê a
  fato, então responde; medida em tabela desconectada, não).

## O tema registrado precisa ser o da Ficha
O Builder gera `Tema.json` junto com os fundos, mas **o relatório só muda quando o
tema é importado**. É comum o relatório continuar com um tema antigo (outra cor
de destaque e outro navy) enquanto os fundos já são os da Ficha: cores de cartão,
tabela e segmentação não batem com os nichos.
Confira: compare `dataColors` do tema registrado em `RegisteredResources` com o
`Tema.json` da pasta do Builder. Para corrigir por arquivo, sobrescreva o conteúdo
do tema registrado (mantendo o nome do recurso, para não mexer em `report.json`)
ou use Design › Importar tema.

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
