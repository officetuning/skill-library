# Editar PBIR por script e conviver com o Desktop

Lições de construir um relatório inteiro (páginas, visuais, dicas) por script
em um `.pbip`. **[verificado]** = confirmado em arquivo gravado pelo Desktop.
**[relato do autor]** = vem da prática em projetos, ainda sem confirmação em arquivo gravado.

## O ciclo seguro
1. Backup da pasta `*.Report` e `*.SemanticModel` antes de lote.
2. Script reexecutável (idempotente) que lê o JSON, altera e grava.
3. Validar: **bindings** (todo campo existe no TMDL) e **schema** do `visual.json`.
4. **Conferir que o Desktop está fechado, antes e depois de escrever**:
   `Get-Process PBIDesktop -ErrorAction SilentlyContinue` (sem saída = fechado).
   Se estiver aberto, peça ao autor que feche **sem salvar**. O Desktop só lê o
   projeto ao abrir; salvar com a versão antiga em memória sobrescreve a edição
   externa. [verificado] Já houve perda de trabalho do autor por salvar com a
   sessão antiga aberta. [relato do autor] Depois de gravar, repita a conferência
   e só então reabra o `.pbip`.
5. Conferir com captura de tela; **dizer que o render não foi visto**.
6. Antes de commitar: `git diff --cached --stat` (ver "Git: separar o trabalho do
   autor do seu" abaixo).

## Descobrir o valor certo de uma propriedade
Não deduza enums de outro relatório. Faça: o usuário configura **um** visual no
Desktop, salva; você lê o arquivo e replica nos demais.
Exemplo: `cardVisual.layout.orientation`: **Grade = `0D`**; `1D` e `2D` são
outras disposições; propriedade ausente = Horizontal. [verificado]

## Tabela de propriedades já confirmadas

| Propriedade | O que o usuário vê | Valor gravado | Status |
|---|---|---|---|
| `layout.orientation` (card) | Disposição: Grade | `0D` | verificado |
| `layout.maxTiles`, `columnCount`, `rowCount` | Nº de blocos / colunas / linhas | `NL` | verificado |
| `value.labelDisplayUnits` (por `selector.metadata`) | Unidade de exibição "Nenhuma" | `1D` | verificado |
| `visualContainerObjects.visualTooltip` | Tooltip: página do relatório | `{ show, section }` | verificado |
| `page.json › pageBinding` | Página de drillthrough | `{ type:"Drillthrough", parameters }` | verificado |
| `page.json › objects.background.image.scaling` | Ajuste da imagem ("Ajuste = Alongar" na interface) | `'Fit'` | verificado (valor e rótulo, guia do Builder 1.031) |
| `title.text` ligado a medida | Título dinâmico | `{ expr:{ Measure } }` | verificado |
| projeção `displayName` + `nativeQueryRef` | Campo renomeado no visual | strings | verificado |
| `visualContainerObjects.general[0].properties.altText` | Texto alternativo | literal | verificado |
| `position.tabOrder` (ordem de foco) | Ordem de tabulação | maior = primeiro (doc da ferramenta) | **a confirmar no Desktop** |

## O que o Desktop faz sozinho
- **Reescreve o arquivo inteiro ao salvar** e injeta propriedades de tema
  (fundo, borda, sombra, padding, `fontFamily`) nos contêineres. Ao clonar um
  visual, a cópia herda isso; ao criar do zero, **não escreva estilo que o tema
  já aplica**. [verificado]
- **Grava propriedades que o schema público não conhece** (ex.:
  `actionButtonSection` em `visualContainerObjects`). Inofensivas; podem voltar
  a cada salvamento; se o validador acusar, remova. [verificado]
- **Normaliza** valores (`y: 872.0000000000001`). Grave posições **inteiras**.
- **Declara `visualContainer/2.14.0`** enquanto o repositório público de
  schemas pode só ter versões menores: valide reescrevendo o `$schema` apenas
  na validação; o erro de `const` no `$schema` é ruído. [verificado]

## Armadilhas de arquivo
- **CRLF e UTF-8 sem BOM.** Scripts que reescrevem texto trocam CRLF por LF;
  reconverta. BOM quebra a leitura.
- **TMDL multilinha:** `measure X =` e o corpo a **3 tabs** (propriedades a 2).
- **Recursos de imagem:** cada página tem a sua cópia registrada do fundo.
  Para trocar, sobrescreva o arquivo já registrado (não mexe em `report.json`).
  Para um PNG novo, copie para `StaticResources/RegisteredResources` e acrescente
  `{ name, path, type: "Image" }` em `report.json › resourcePackages`.
- **Ordem das páginas:** `pages.json › pageOrder`; ao criar página, inclua o
  nome da pasta; `activePageName` não deve apontar para página oculta.
- Nome de pasta de página/visual: hexadecimal aleatório de 20 caracteres;
  renomear pasta não muda o `displayName`.

## Checagens baratas que pegaram erro real (candidatas ao QA)
1. `title.show = true` sem `text`.
2. `cardVisual` só com colunas de texto.
3. Cartão multi-campo sem `maxTiles` e com colunas automáticas.
4. `visualTooltip.section` apontando para página inexistente.
5. Coluna-chave de drillthrough que não está em nenhum visual de página principal.
6. Segmentação fora da posição reservada pelo fundo.
7. Posições não inteiras.

As checagens 8 a 17 estão em
`../../bi-qa-documentacao/references/checagens-adicionais.md`.

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
2. **Descubra o fim de linha que aquele arquivo tem no HEAD**:
   `git ls-files --eol caminho` (`i/lf` ou `i/crlf`). Com `core.autocrlf=true`,
   os blobs do mesmo repositório ficam em LF em alguns arquivos e em CRLF em
   outros (já houve `.tmdl` em CRLF no HEAD). Grave a versão "só sua" **com o
   mesmo fim de linha do HEAD**. [relato do autor]
3. Coloque-a no índice sem tocar no diretório de trabalho e **sem filtros**,
   para o Git não converter o fim de linha:
   `git hash-object -w --no-filters arquivo` e
   `git update-index --cacheinfo 100644,<hash>,<caminho>`.
4. **Confira `git diff --cached --stat` antes de commitar.** Devem aparecer só
   as suas linhas. Centenas de linhas trocadas num arquivo em que você mexeu em
   três é fim de linha errado (já marcou cerca de 1.500 linhas): desfaça com
   `git restore --staged caminho` e refaça os passos 2 e 3. [relato do autor]
5. Faça o commit.
6. Faça `git add` da versão do diretório de trabalho e commite como "mudanças
   do autor em andamento".
Funcionou em `model.tmdl`, em uma tabela `.tmdl` e em um `visual.json`.

**Erro "dubious ownership"** (pasta de outro usuário, OneDrive ou unidade
externa): use `git -c safe.directory=<pasta do repositório> <comando>` só no
comando, sem alterar a configuração global. [relato do autor]

## Antes de commitar vários projetos
- Uma **branch por projeto**, merge com `--no-ff`, push e exclusão da branch,
  um passo de cada vez ou direto até o fim, conforme o autor autorizar.
- Deixe de fora o que o Desktop gravou sozinho (ex.: `DAXQueries`,
  `activePageName`) e o que é de outro trabalho.

## Ambiente
- No Windows, a saída do Python em cp1252 quebra com acentos: defina
  `PYTHONIOENCODING=utf-8`.
- Ao gravar bytes com acento (`open(..., "wb")`), codifique o literal com
  `.encode("utf-8")`; sem isso o literal pode sair em outra codificação e
  corromper os acentos no arquivo. [relato do autor]
- Arquivos temporários: não use `/tmp`. No Windows, ele não existe fora do Git Bash
  e cada ferramenta o resolve de um jeito; use `%TEMP%` ou a pasta de
  rascunho da sessão. [relato do autor]
- Em scripts que percorrem pastas, normalize as barras do caminho antes de
  `split("/")`.
