# Adendo à edição por script e ao uso do Git (acrescentar a `edicao-por-script-e-desktop.md`)

Lições de aplicar lotes por script em quatro projetos.

## Descobrir a propriedade certa antes de criá-la
- **Procure o nome da propriedade nos arquivos que o Desktop já gravou**, em
  qualquer projeto, antes de inventar. Foi assim que se descobriram
  `dataLabels.dataLabelDisplayUnits` (árvore de decomposição),
  `referenceLabelValue.valueDisplayUnits` (cartão com referência) e o objeto
  `value` da rosca. Um `grep` pelo trecho do nome (`"…Units"`) e o caminho do
  objeto resolve.
- **Quando nenhum projeto tem a propriedade** (ex.: Pesquisar da segmentação),
  peça ao autor que configure **um** visual, salve, e leia o arquivo.

## Texto alternativo por tipo de visual
- Os papéis dos campos variam: `Values`/`Series`/`Category` (tornado),
  `Y` sem categoria (medidor, rosca simples), `Actual` (tacômetro),
  `employeeId`/`managerId` (organograma). Escreva uma regra por tipo e uma
  mensagem de erro para o tipo sem regra, em vez de deixar a exceção parar o
  lote.
- Limpe o nome do campo antes de escrever o texto ("Nome da Região" → "região",
  "Classificação IMC" → "classificação do IMC").
- Visual personalizado: dê o texto alternativo e confirme ao reabrir no Desktop
  que o aceita sem erro.

## Git: separar o trabalho do autor do seu
Quando um arquivo mistura mudanças em andamento do autor com as suas:
1. Monte a versão "só sua" a partir do último commit (`git show HEAD:caminho`)
   aplicando só as suas edições.
2. Coloque-a no índice sem tocar no diretório de trabalho:
   `git hash-object -w arquivo` e `git update-index --cacheinfo 100644,<hash>,<caminho>`.
3. Confira `git diff --cached` (só as suas linhas) e faça o commit.
4. Faça `git add` da versão do diretório de trabalho e commite como "mudanças
   do autor em andamento".
Funcionou em `model.tmdl`, em uma tabela `.tmdl` e em um `visual.json`.

## Antes de commitar vários projetos
- Uma **branch por projeto**, merge com `--no-ff`, push e exclusão da branch,
  um passo de cada vez ou direto até o fim, conforme o autor autorizar.
- Deixe de fora o que o Desktop gravou sozinho (ex.: `DAXQueries`,
  `activePageName`) e o que é de outro trabalho.

## Ambiente
- No Windows, a saída do Python em cp1252 quebra com acentos: defina
  `PYTHONIOENCODING=utf-8`.
- Em scripts que percorrem pastas, normalize as barras do caminho antes de
  `split("/")`.
