# Editar PBIR por script e conviver com o Desktop

Lições de construir um relatório inteiro (páginas, visuais, dicas) por script
em um `.pbip`. **[verificado]** = confirmado em arquivo gravado pelo Desktop.
**[relato do autor]** = vem da prática em projetos, ainda sem confirmação em arquivo gravado.

## O ciclo seguro
1. Backup da pasta `*.Report` e `*.SemanticModel` antes de lote.
2. Script reexecutável (idempotente) que lê o JSON, altera e grava.
3. Validar: **bindings** (todo campo existe no TMDL) e **schema** do `visual.json`.
4. **Conferir que o Desktop está fechado, antes e depois de escrever**:
   `Get-Process PBIDesktop -ErrorAction SilentlyContinue` no PowerShell (sem
   saída = fechado); no Git Bash, `tasklist | grep -i PBIDesktop`.
   Se estiver aberto, peça ao autor que feche **sem salvar**. O Desktop só lê o
   projeto ao abrir; salvar com a versão antiga em memória sobrescreve a edição
   externa. [verificado] Já houve perda de trabalho do autor por salvar com a
   sessão antiga aberta. [relato do autor] Depois de gravar, repita a conferência
   e só então reabra o `.pbip`.
   **Trave o script**, não só avise: no começo do script de gravação, aborte se o
   processo existir (`tasklist | grep -qi PBIDesktop && { echo "Desktop aberto"; exit 1; }`
   no Git Bash; `if (Get-Process PBIDesktop -EA 0) { throw 'Desktop aberto' }` no
   PowerShell). Imprimir o aviso e seguir gravando já custou trabalho ao autor.
5. Conferir com captura de tela; **dizer que o render não foi visto**.
6. Antes de commitar: `git diff --cached --stat` para ver só o que entra no
   commit. Se o arquivo mistura trabalho do autor com o seu, siga "Git: separar o
   trabalho do autor do seu" abaixo.

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
| `segmentação.general.selfFilterEnabled` | Pesquisar ligado (texto, suspenso) | `true` | verificado |
| `segmentação.dropdown.accentBarShow` | Barra de destaque desligada | `false` | verificado |
| segmentação de data relativa | "Este ano a partir da última data" | `data.mode 'RelativeDatePicker'` + filtro `DateSpan` sobre `ScopedEval ( Max ( Data ) )`, `TimeUnit 3` | verificado |
| `tableEx`/`pivotTable` `stylePreset` | Estilo: Cabeçalho em negrito | `'BoldHeader'` | verificado |
| `columnHeaders.columnAdjustment` | Aumentar para ajustar | `'growToFit'` | verificado |
| `columnHeaders.backColor` | Cabeçalho na Cor do tema 1 | `ThemeDataColor { ColorId: 2 }` (`ColorId 0` é branco: cabeçalho invisível) | verificado |
| `grid.imageHeight`/`imageWidth` | Tamanho da imagem na coluna | `NL` | verificado |
| `image.sourceType` + `sourceField` | Visual de imagem dinâmico | `'imageData'` + `Aggregation ( Function 3 )` de coluna ImageUrl | verificado |
| `cardVisual.image` (por medida) | Ícone no cartão | `position 'Right'`, `scaling 'Fit'`, `imageAreaSize 20L` | verificado |
| `actionButton` limpar filtros | Botão Limpar filtros | `icon.shapeType 'clearAllSlicers'` + `visualLink.type 'ClearAllSlicers'` | verificado |
| `page.json › type` (dica) | Página de dica | `"Tooltip"`, sem `pageBinding` | verificado |
| `columnHeaders` da `pivotTable` | mesmo estilo da `tableEx` | mesmos objetos | verificado |
| `segmentação de data › dateRangeText.fontSize` e `relativeText.fontSize` | Texto › Intervalo de datas e Resumo | `12D` | verificado |
| `segmentação de data › general.filter` | "Este ano a partir da última data" | `DateSpan` sobre `ScopedEval(Max(data))`, `TimeUnit 3` | verificado |
| `page.json › visualInteractions` | Editar interações: "Nenhum" | `[{ source, target, type: "NoFilter" }]` (nomes completos dos visuais) | verificado |
| `image` (visual) › `sourceFile › scaling` | Ajuste da imagem: Preencher | `'Fill'` | verificado (infográfico) |
| `image` (visual) › `sourceField` | Imagem por campo | `expr › Measure` de uma medida com `dataCategory: ImageUrl` funciona; filtro de visual em medida de ranking **não** separa as linhas | verificado |
| `visualContainerObjects.border.radius` | Cantos arredondados | metade do lado num visual quadrado = círculo | verificado |
| `cardVisual › value.fontFamily`, `fontSize`, `fontColor` | Fonte, tamanho e cor do valor | nomes confirmados no Desktop (`'Segoe UI Semibold'`, `20D`, literal hex) | verificado |
| `cardVisual › layout (selector id default) › paddingIndividual`, `paddingUniform` | Preenchimento interno do bloco | `false` e `10L` | verificado |
| `visualContainerObjects.spacing.spaceAboveDivider` | Espaço acima do divisor | `4D` em cartão com etiquetas de referência | verificado |
| `donutChart › slices.innerRadiusRatio` | Raio interno (%) | existe (0 a 99; padrão 48% do raio); **não usar**: deixe o padrão e ajuste a fonte do valor central (`value.fontSize`) | verificado no código do Desktop |
| `image` (visual) › `cornerRadius` | Cantos | existe, plano B ao raio do contêiner | verificado no código do Desktop |

## Armadilhas de fluxo (sessão com o Vendas) [verificado]
- **Nunca edite `.pbix` como zip:** corrompe o arquivo ("arquivo corrompido").
  Trabalhe em PBIP; salvar o `.pbix` como PBIP resolve.
- **Desktop fechado ao gravar.** Com ele aberto, o Desktop sobrescreve no
  próximo salvamento e mostra o estado antigo. Feche e, se não fechar, encerre o
  processo sem salvar, e só então grave os arquivos.
- **Reabrir após editar o modelo:** apague `.pbi\cache.abf`; o Desktop pede
  "Atualizar agora" (às vezes duas vezes) e "Aplicar alterações". A abertura leva
  ~90 a 100 s. Cuidado com `open_application`: abre uma segunda instância vazia.
- **Script que reinsere blocos TMDL** precisa remover **todas** as variações do
  bloco antigo (o Desktop reformata para linha única) e as `annotation` órfãs;
  senão surgem medidas duplicadas ("TMDL objects cannot be merged") ou anotações
  repetidas que impedem abrir o projeto.
- **Renomear tabela e medidas em lote:** troque também o relatório (`Entity`,
  `Property`, `queryRef`, `selector.metadata`) em todos os `visual.json` e confira
  com `bi-qa-documentacao/scripts/check_visual_bindings.py`; o `Item` do Excel no
  M não muda.
- `json.dumps` com `ensure_ascii=True` não casa com nomes acentuados ao testar
  presença; grave com `ensure_ascii=False`.
- **`python -I` ignora `PYTHONIOENCODING`.** No Windows, `print` de `Δ`, `Ç` ou
  emoji dá `UnicodeEncodeError` (console cp1252). Rode sem `-I` e com
  `PYTHONIOENCODING=utf-8`, ou grave o resultado em arquivo.
- **Script grande com muito texto entre aspas e crases**: não passe por heredoc do
  shell (as aspas confundem). Grave o script em arquivo e execute.
- **Ocultar medida auxiliar** (de um visual personalizado, por exemplo) faz o BPA
  acusar "Remove unnecessary measures": ele não vê o uso nos visuais. Falso
  positivo; registre na nota de auditoria. Ocultar chave estrangeira e coluna crua
  de fato reduz "Hide foreign keys" e "Hide fact table columns"; nas ocultas, o BPA
  pede `isAvailableInMdx: false`.
- **Referência a tabela em DAX sem colchete** (`COUNTROWS(Tab)`, `ALL(Tab)`,
  `REMOVEFILTERS(Tab)`) também vai entre aspas simples; a troca em lote deve
  cobrir os dois formatos (`Tab[col]` e `Tab`) e pular comentários e a partição M.
- Gerar visual novo **a partir de um visual salvo pelo Desktop** (cartão com
  AA/Δ%, ícones, botão) funciona melhor que escrever o JSON do zero.
- **OneDrive pode negar `rmdir`** em pasta de visual recém-esvaziada; pasta
  vazia é inofensiva. Prefira apagar `visual.json` e tentar o `rmdir` depois.
- Em edição, `ctrl+clique` no navegador de páginas muda de página; o clique de
  mouse simples seleciona o visual.

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

## O que o salvamento muda e o que ele recusa [verificado]
- Ao salvar, o Desktop pode **subir o `$schema`** dos visuais (2.14 para 2.15),
  **renumerar `position.z` e `tabOrder`** e **reescrever medidas sem as crases**.
- **Script gerador não se reaplica às cegas** sobre um relatório já salvo: compare a
  saída com o disco, preserve `$schema`, `z`, `tabOrder` e o que outro script
  acrescentou (ícone, dica, fundo) e rode em ensaio até dar zero alterações. O que o
  autor ajustou à mão manda.
- **Depois de pedir ao autor que abra o relatório**, antes de editar de novo, confira
  se ele **salvou** (data de `.pbi\cache.abf` e dos arquivos) e se o Desktop **fechou**;
  diga o resultado.
- **Trocar uma tabela existente de calculada para M** (mantendo o nome) é recusado ao
  abrir, embora o Tabular Editor carregue o modelo: crie a tabela com outro nome e
  repasse relacionamentos e referências.
- **Data em registro:** use a data local; a hora UTC vira o dia mais cedo e já pôs data
  errada na página Sobre.

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

As checagens 8 a 18 estão em
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
   mesmo fim de linha do HEAD**. Se o arquivo é novo e não tem HEAD, siga o dos
   arquivos vizinhos do mesmo tipo. [relato do autor]
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
  e cada ferramenta o resolve de um jeito; use `$env:TEMP` (PowerShell; no Git
  Bash, `$TEMP`) ou a pasta de rascunho da sessão. [relato do autor]
- Em scripts que percorrem pastas, normalize as barras do caminho antes de
  `split("/")`.
