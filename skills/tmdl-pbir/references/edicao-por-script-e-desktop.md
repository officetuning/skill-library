# Editar PBIR por script e conviver com o Desktop

Lições de construir um relatório inteiro (páginas, visuais, dicas) por script
em um `.pbip`. **[verificado]** = confirmado em arquivo gravado pelo Desktop.

## O ciclo seguro
1. Backup da pasta `*.Report` e `*.SemanticModel` antes de lote.
2. Script reexecutável (idempotente) que lê o JSON, altera e grava.
3. Validar: **bindings** (todo campo existe no TMDL) e **schema** do `visual.json`.
4. **Fechar o Desktop sem salvar e reabrir o `.pbip`.** O Desktop só lê o
   projeto ao abrir; salvar com a versão antiga em memória sobrescreve a edição
   externa. [verificado]
5. Conferir com captura de tela; **dizer que o render não foi visto**.

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

As checagens 8 a 15 estão em
`../../bi-qa-documentacao/references/checagens-adicionais.md`. Lições de lotes por
script e de Git: `edicao-por-script-adendo.md`.
