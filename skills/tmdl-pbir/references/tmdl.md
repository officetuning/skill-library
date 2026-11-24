# TMDL — referência

Consolidado da documentação Microsoft Learn:
[Visão geral](https://learn.microsoft.com/pt-br/analysis-services/tmdl/tmdl-overview) ·
[Introdução e API](https://learn.microsoft.com/pt-br/analysis-services/tmdl/tmdl-how-to) ·
[Scripts](https://learn.microsoft.com/pt-br/analysis-services/tmdl/tmdl-scripts).

TMDL (Tabular Model Definition Language) define objetos de modelos tabulares
com nível de compatibilidade 1200+. Vale para SSAS 2016+, Azure Analysis
Services e Power BI/Fabric. Expõe as mesmas propriedades do TOM, com sintaxe
parecida com YAML.

## Estrutura de pastas

```
definition/
├── cultures/        (1 arquivo por cultura)
├── perspectives/    (1 por perspectiva)
├── roles/           (1 por role)
├── tables/          (1 por tabela: colunas, medidas, hierarquias, partições)
├── relationships.tmdl   (todos os relacionamentos)
├── functions.tmdl       (todas as funções DAX definidas pelo usuário)
├── expressions.tmdl     (todas as expressões compartilhadas e parâmetros)
├── dataSources.tmdl     (todas as fontes)
├── model.tmdl
└── database.tmdl
```

## Linguagem

### Declaração e propriedades
- `<tipo TOM> <nome>`; aspas simples se o nome tiver `.`, `=`, `:`, `'` ou
  espaço. Acento não exige aspas (`table Calendário`). Isso vale só para a
  declaração: dentro da expressão de uma medida, a fórmula é DAX e a tabela vai
  sempre entre aspas simples (`'Atualização'[Momento da Última Atualização]`;
  sem aspas, a medida dá erro).
- `propriedade: valor`. Aspas duplas em texto são opcionais, obrigatórias com
  espaço no início ou fim; aspas duplas internas duplicadas `""`.
- Booleano: `isHidden` sozinho equivale a `isHidden: true`.

```tmdl
table Vendas
    measure 'Faturado (AV)' =
            VAR vResultado = SUMX ( 'Vendas', 'Vendas'[Quantidade] * 'Vendas'[Preço Líquido] )
            RETURN vResultado
        formatString: R$ #,##0
        displayFolder: " Medidas ""Principais"""
```

### Objetos filhos
Coleções não são declaradas: todo filho no escopo do pai entra na coleção.
Colunas e medidas podem vir intercaladas.

### Delimitadores
| Delimitador | Uso |
|---|---|
| `=` | Propriedade padrão e toda propriedade do tipo expressão |
| `:` | Qualquer outro valor, incluindo referência a objeto |

### Expressões
Lidas literalmente. Multilinha: um nível mais fundo que as propriedades.
Espaço fora da indentação e linhas em branco finais são removidos. Para
preservar exatamente, use ` ``` ` após o `=`.

| Objeto | Propriedade de expressão | Linguagem |
|---|---|---|
| Measure, CalculatedColumn, CalculationItem | Expression | DAX |
| Function (UDF) | Expression | DAX |
| MPartitionSource | Expression | M |
| CalculatedPartitionSource | Expression | DAX |
| QueryPartitionSource | Query | Nativa |
| BasicRefreshPolicy | SourceExpression, PollingExpression | M |
| KPI | Status/Target/TrendExpression | DAX |
| TablePermission | FilterExpression | DAX |
| FormatStringDefinition, DetailRowsDefinition | Expression | DAX |
| NamedExpression | Expression | M ou DAX |

### Descrições
`///` imediatamente acima do tipo do objeto, sem linha em branco. Multilinha
permitido; o serializador quebra em 80 caracteres.

### Declaração parcial
Um objeto pode ser definido em mais de um arquivo; a mesma propriedade não pode
aparecer duas vezes.

### `ref`
Referencia objeto definido em outro arquivo. No `model.tmdl`, a lista de `ref`
fixa a ordem das coleções e evita diff desnecessário.
- `ref` sem arquivo correspondente → ignorado.
- Arquivo sem `ref` → anexado ao fim da coleção.

### Indentação
Três níveis: declaração → propriedades → expressão multilinha. Filhos diretos de
`model`/`database` (tabelas, roles, culturas, relacionamentos...) não precisam
de indentação. Erro de indentação é erro de parsing.

### Maiúsculas
Serialização em camelCase; leitura sem diferenciar maiúsculas e minúsculas.

## Scripts TMDL

```tmdl
createOrReplace

    ref table Vendas
        measure '# Produtos Vendidos' = DISTINCTCOUNT ( 'Vendas'[Código do Produto] )
            formatString: #,##0

    table Produto

        measure '# Produtos' = COUNTROWS ( Produto )
            formatString: #,##0

        column 'Nome do Produto'
            dataType: string
            isDefaultLabel
            summarizeBy: none
            sourceColumn: Nome do Produto

        partition Produto = m
            mode: import
            queryGroup: Dimensões
            source =
                let
                    Origem = CnsProdutoTratado,
                    Renomeado = Table.RenameColumns(Origem, {{"NomeProduto", "Nome do Produto"}})
                in
                    Renomeado
```

- Um verbo por script.
- `createOrReplace` recria o objeto e todos os descendentes.
- A ordem dos objetos no script não importa.

## API .NET — `TmdlSerializer`

Namespace `Microsoft.AnalysisServices.Tabular`.

```csharp
// Extrair um modelo publicado para pasta TMDL
using (var server = new Microsoft.AnalysisServices.Tabular.Server())
{
    server.Connect("<endereço XMLA do workspace>");
    var database = server.Databases.GetByName("<nome do modelo>");
    TmdlSerializer.SerializeDatabaseToFolder(database, $@"C:\saida\{database.Name}-tmdl");
}

// Reimplantar a pasta editada
var model = TmdlSerializer.DeserializeModelFromFolder(@"C:\saida\Contoso-tmdl");
using (var server = new Microsoft.AnalysisServices.Tabular.Server())
{
    server.Connect("<endereço XMLA do workspace>");
    using (var remoteDatabase = server.Databases[model.Database.ID])
    {
        model.CopyTo(remoteDatabase.Model);
        remoteDatabase.Model.SaveChanges();
    }
}

// Serializar um objeto só
var texto = TmdlSerializer.SerializeObject(model.Tables["Produto"].Columns["Código do Produto"], qualifyObject: true);
```

`MetadataSerializationContext` (namespace
`Microsoft.AnalysisServices.Tabular.Serialization`) lê e grava por stream e
permite escolher quais documentos ler (ex.: ignorar `roles/`).

### Erros

| Exceção | Quando |
|---|---|
| `TmdlFormatException` | Sintaxe inválida (palavra-chave, indentação) |
| `TmdlSerializationException` | Sintaxe válida, mas viola a lógica do TOM |

Ambas trazem documento, número e texto da linha.

## Onde se usa

- `.pbip`: a pasta `.SemanticModel` é TMDL.
- VS Code com a extensão [TMDL](https://marketplace.visualstudio.com/items?itemName=analysis-services.TMDL).
- CI/CD com `TmdlSerializer`.
- Scripts `createOrReplace` na TMDL View do Desktop ou no Tabular Editor.
