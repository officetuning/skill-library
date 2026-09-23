---
name: tmdl-pbir
description: Formatos de texto do Power BI Project (.pbip) — TMDL para o modelo semântico e PBIR para o relatório. Sintaxe TMDL (indentação, expressões, descrição com ///, ref, createOrReplace), estrutura de pastas, TmdlSerializer, estrutura PBIR (definition, pages, visual.json), definition.pbir byPath/byConnection, JSON Schemas e limitações. Use para escrever script TMDL, criar tabela ou medida via TMDL, editar medida fora do Desktop, versionar relatório em Git, entender ou editar visual.json/page.json, ou converter para PBIR. Para validar esses arquivos em pipeline use bi-qa-documentacao.
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

Status: o PBIR estava em **preview** na data desta base (29/08/2026), com
conversão automática no Service e previsão de virar o único formato na GA.
Status de preview muda: confirme na documentação antes de afirmar.

Habilitar, converter, restaurar, recursos avançados, erros comuns e limites:
`references/pbir.md`.

## Posição dos visuais

O bloco de posição do `visual.json` (x, y, z, width, height, tabOrder, em pixel,
origem no canto superior esquerdo) recebe as coordenadas do grid da skill
`dashboard-layout`. Confirme o formato no schema antes de editar em lote.
