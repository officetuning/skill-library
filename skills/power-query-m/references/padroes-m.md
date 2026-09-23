# Padrões de código M

## Função documentada com `Value.ReplaceType`

Funções documentadas assim aparecem no Power Query Editor com nome, descrição
e exemplo para qualquer pessoa que as reutilize.

```m
let
    // Implementação
    FnCalcularMargem = (receita as number, custo as number) as nullable number =>
        if receita = 0 then null else (receita - custo) / receita,

    // Metadados de documentação
    FnCalcularMargemTipo = type function (
        receita as (type number meta [
            Documentation.FieldCaption = "Receita",
            Documentation.FieldDescription = "Valor total da receita, antes de deduzir o custo"
        ]),
        custo as (type number meta [
            Documentation.FieldCaption = "Custo",
            Documentation.FieldDescription = "Valor total do custo associado à receita"
        ])
    ) as nullable number meta [
        Documentation.Name = "FnCalcularMargem",
        Documentation.Description = "Calcula a margem percentual a partir de receita e custo.",
        Documentation.LongDescription = "Retorna (receita - custo) / receita. Retorna null quando a receita é zero.",
        Documentation.Category = "Financeiro",
        Documentation.Author = "OfficeTuning",
        Documentation.Version = "1.0.0",
        Documentation.Examples = {
            [
                Description = "Receita 1000, custo 600 → margem de 40%",
                Code = "FnCalcularMargem(1000, 600)",
                Result = "0.4"
            ]
        }
    ]
in
    Value.ReplaceType(FnCalcularMargem, FnCalcularMargemTipo)
```

Nome da consulta: `FnCalcularMargem` (prefixo `Fn`, ver skill `bi-nomenclatura`).

## Tratamento de erro auditável

Converta com `try`, mas isole as linhas que falharam em vez de descartá-las.

**Consulta `CnsVendaConvertida`** (sem carregamento):

```m
let
    Origem = CnsVendaStaging,
    ComValor = Table.AddColumn(
        Origem,
        "ValorConvertido",
        // Cultura explícita: a fonte usa vírgula decimal
        each try Number.FromText([ValorTexto], "pt-BR") otherwise null,
        type nullable number
    )
in
    ComValor
```

**Consulta `CnsVendaErroConversao`** (auditoria; carregue numa tabela de
qualidade de dado ou só inspecione):

```m
let
    Origem = CnsVendaConvertida,
    // Linha com texto preenchido que não virou número = falha de conversão
    LinhasComErro = Table.SelectRows(
        Origem,
        each [ValorConvertido] = null and [ValorTexto] <> null and [ValorTexto] <> ""
    )
in
    LinhasComErro
```

Assim o time vê quantas linhas estão sendo puladas, em vez de descobrir quando
os totais não batem.

**Evite:**

```m
// Esconde a causa: se a fonte mudar de formato, tudo vira "0" em silêncio
= Table.AddColumn(Origem, "Valor", each try [ValorTexto] otherwise "0")
```
