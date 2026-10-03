---
name: tmdl-pbir
description: Formatos de texto do Power BI Project (.pbip) — TMDL para o modelo semântico e PBIR para o relatório. Sintaxe TMDL (indentação, expressões, descrição com ///, ref, createOrReplace), estrutura de pastas, TmdlSerializer, estrutura PBIR (definition, pages, visual.json), definition.pbir byPath/byConnection, JSON Schemas e limitações. Use para escrever script TMDL, criar tabela ou medida via TMDL, editar medida fora do Desktop, versionar em Git (commit, diff, restaurar, .gitignore), editar em lote na TMDL view, objeto function (UDF) no TMDL, entender ou editar visual.json/page.json, ou converter para PBIR. Para validar esses arquivos em pipeline use bi-qa-documentacao.
---

# TMDL e PBIR

Um Power BI Project (`.pbip`) salva em pastas separadas, em texto amigável ao Git:

| Parte | Formato | Pasta |
|---|---|---|
| Modelo semântico | **TMDL** | `*.SemanticModel\definition\` |
| Relatório | **PBIR** | `*.Report\definition\` |

Os dois trocam um JSON monolítico por **um arquivo por objeto**: alterar uma
medida gera diff em um único arquivo de tabela.

## TMDL essencial

```tmdl
table Vendas

    /// Soma o valor líquido das vendas. Exclui cancelados e devoluções.
    measure 'Total de Vendas' = SUM ( Vendas[Valor da Venda] )
        formatString: R$ #,##0.00
        displayFolder: Vendas

    column 'Código do Cliente'
        dataType: int64
        isHidden
        summarizeBy: none
        sourceColumn: CodigoCliente

    partition Vendas = m
        mode: import
        source =
            let
                Origem = Sql.Database(Servidor, Banco),
                Dados = Origem{[Schema = "dbo", Item = "VwFatVenda"]}[Data]
            in
                Dados
```

| Regra | Sintaxe |
|---|---|
| Declarar objeto | `<tipo> <nome>` |
| Nome com espaço, `.`, `=`, `:` ou `'` | `'Nome do Objeto'` (aspas simples internas duplicadas `''`) |
| Propriedade comum | `propriedade: valor` |
| Booleano verdadeiro | só o nome: `isHidden` |
| Propriedade padrão / expressão | `measure Nome = <expressão>` |
| Expressão multilinha | um nível de indentação **a mais** que as propriedades |
| Preservar formatação exata | delimitar com ` ``` ` logo após o `=` |
| Descrição | `///` na linha imediatamente acima, sem linha em branco |
| Referenciar sem redeclarar | `ref table Vendas` |
| Nome qualificado | `'Tabela'.'Coluna'` |
| Indentação | 1 tab por nível; erro de indentação = erro de parsing |

**Script de alteração** — um só verbo por script:

```tmdl
createOrReplace

    ref table Vendas
        measure '# Pedidos' = DISTINCTCOUNT ( Vendas[Código do Pedido] )
            formatString: #,##0
```

`createOrReplace` substitui o objeto **e todos os descendentes**: ao usar
`table Produto` sem `ref`, colunas e medidas omitidas somem. Para acrescentar
uma medida, use `ref table`.

UDFs são objetos `function` e ficam em `definition/functions.tmdl`:

```tmdl
createOrReplace

    /// Aplica imposto sobre um valor.
    function 'Fiscal.ComImposto' = (valor : NUMERIC) => valor * 1.1
```

Sintaxe, tipos de parâmetro e padrões de UDF: skill `dax-udf`.

### TMDL view: editar em lote

A TMDL view (GA no Desktop, qualquer licença) mostra fórmula, formato e pasta
de exibição juntos. Receitas:

| Tarefa | Como |
|---|---|
| Mover várias medidas para uma pasta | Arraste as medidas para o editor, troque `displayFolder:` de todas com Ctrl + H, *Apply* |
| Corrigir formato em lote | Localize `formatString: 0.00` e substitua pelo padrão (ex.: `#,0.00`) |
| Renomear com padrão | Ctrl + F com expressão regular; confira dependências antes |
| Copiar tabela para outro modelo | Arraste a tabela, copie o script, cole na TMDL view do outro modelo |
| Backup antes de mudança grande | Arraste o modelo inteiro e salve o script (fica em `TMDLScripts\` no `.pbip`) |

A TMDL view aplica na hora. Editar arquivos `.tmdl` fora do Desktop exige
reiniciar o Desktop, a menos que o recurso em preview **Detect and reload
external PBIP changes** (Desktop agosto/2026) esteja ligado: aí aparece o
aviso *Apply external changes*. Ele não recarrega o `cache.abf`.

Estrutura de pastas, tabela de propriedades que são expressão, API .NET
(`TmdlSerializer`), exceções e fontes: `references/tmdl.md`.

## PBIR essencial

```
definition\
├── pages\
│   ├── pages.json                 (ordem das páginas)
│   └── [pagina]\
│       ├── page.json              (obrigatório)
│       └── visuals\[visual]\visual.json   (obrigatório: posição, formatação, query)
├── bookmarks\
├── version.json                   (obrigatório)
└── report.json                    (obrigatório)
```

- Cada arquivo declara um JSON Schema público; o VS Code valida e dá IntelliSense.
  Schemas: [microsoft/json-schemas](https://github.com/microsoft/json-schemas/tree/main/fabric/item/report/definition).
- `definition.pbir` aponta o modelo: `byPath` (caminho relativo, edição completa)
  ou `byConnection` (live connect; **obrigatório via Fabric REST API**).
- Nome de pasta/arquivo: letras, dígitos, `_` ou `-`. Renomear exige reiniciar o
  Desktop e pode quebrar referências.
- ⚠️ `visual.json` e bookmarks podem guardar **valores de dados** (filtro
  `'Company' = 'Contoso'`, seleção de slicer). Cuidado ao versionar em repositório público.
- ⚠️ Converter PBIR-Legacy → PBIR **não se desfaz pela interface**. Salve uma cópia antes.

Status (02/10/2026): PBIP e PBIR estão em **disponibilidade geral (GA)** e o
PBIR é o formato padrão de relatório. Ao editar e salvar um relatório
PBIR-Legacy, o Power BI converte para PBIR. Status muda: confirme na
documentação antes de afirmar.

Habilitar, converter, restaurar, recursos avançados, erros comuns e limites:
`references/pbir.md`.

## PBIP + Git: a rotina mínima

**Antes:** instale Git e VS Code; salve como **Power BI Project (.pbip)**.

**`.gitignore`:** o Desktop cria sozinho (se ainda não existir) com:

```
**/.pbi/localSettings.json
**/.pbi/cache.abf
```

`cache.abf` é o cache **com dados**: nunca versionar. Sem ele, o Desktop abre
o modelo completo, só sem dados (basta atualizar).

**Começar:** VS Code → abrir a pasta do projeto → Source Control →
*Initialize Repository* → primeiro commit.

| Ação | Como | Dica |
|---|---|---|
| Gravar versão | Commit depois de cada mudança que funciona | Mensagem diz o porquê: "Margem % passa a excluir devoluções" |
| Revisar | Veja o diff antes do commit | Uma medida alterada aparece só no `.tmdl` da tabela |
| Desfazer o que não foi gravado | `git restore <arquivo>` | — |
| Voltar um arquivo a um commit anterior | `git checkout <commit> -- <arquivo>` | — |

⚠️ **Feche o Power BI Desktop** antes de restaurar, trocar de branch ou fazer
`git pull`: sem o recurso em preview de recarga externa, o Desktop só relê os
arquivos ao abrir e pode sobrescrever a versão restaurada ao salvar.

⚠️ `unappliedChanges.json` guarda alterações do Power Query ainda não
aplicadas; ao aplicar, elas sobrescrevem consultas editadas fora do Desktop.

Agente de IA alterando o modelo (MCP): comece de um commit limpo e revise o
diff no fim. Ver skill `powerbi-mcp`. Pipeline (BPA, binding, CI/CD): skill
`bi-qa-documentacao`.

## Posição dos visuais

O bloco de posição do `visual.json` (x, y, z, width, height, tabOrder, em pixel,
origem no canto superior esquerdo) recebe as coordenadas do grid da skill
`dashboard-layout`. Confirme o formato no schema antes de editar em lote.
