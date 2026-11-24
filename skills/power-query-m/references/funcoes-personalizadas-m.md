# Funções personalizadas em M

O equivalente em M da skill `dax-udf`. Fontes: [Use custom functions](https://learn.microsoft.com/power-query/custom-function),
[Best practices](https://learn.microsoft.com/power-query/best-practices#create-reusable-functions),
[Add function documentation](https://learn.microsoft.com/power-query/handling-documentation)
e o padrão das funções M da Biblioteca
([officetuning.ai/biblioteca/udf?grupo=m](https://officetuning.ai/biblioteca/udf?grupo=m)).
Conferido em 24/11/2026.

## Quando criar

A mesma transformação em duas ou mais consultas ou colunas (validar CPF, limpar
texto, montar feriados). Antes de escrever, procure na Biblioteca e no
catálogo de funções nativas (`funcoes-m.md`).

## Nome, grupo e parâmetros

A Microsoft não publica convenção de nome para função M personalizada; o
padrão da casa segue o das funções nativas (`Table.AddColumn`) e o da UDF DAX.

| Item | Padrão | Exemplo |
|---|---|---|
| Nome da função | `Grupo.Acao`, PascalCase, sem acento; o ponto faz parte do identificador M | `Texto.SomenteDigitos`, `Validacao.CPF`, `Data.Feriados` |
| Grupo de consultas | **Funções** | — |
| Parâmetro | camelCase, sem acento, como nas nativas (`newColumnName`) | `texto`, `dataInicial`, `cultura` |
| Idioma | Português; inglês só em função feita para outro idioma | `Data.FeriadosFR` |
| Variável interna | Prefixo `v`, como na DAX | `vDigitos` |
| Função auxiliar interna | `fn` + ação, dentro do `let` | `fnDigito` |

⚠️ As funções publicadas na Biblioteca ainda usam o formato antigo
(`fnValidaCPF`); a renomeação para `Grupo.Acao` está planejada.

## Criar

| Caminho | Como | Cuidado |
|---|---|---|
| Do zero | Consulta Nula → Editor Avançado → escrever a função | Documente antes de entregar |
| A partir de uma consulta | Parâmetro com valor de exemplo → consulta que o usa → botão direito → **Criar Função** | A consulta de exemplo fica **ligada** à função: altere a consulta, não a função. Editar a função à mão rompe a ligação (o Power Query avisa) |

## Padrão de código da casa

```m
let
    Texto.SomenteDigitos = (texto as nullable text) as nullable text =>
        let
            // Nulo entra, nulo sai: separa "sem dado" de "dado inválido"
            vResultado = if texto = null then null else Text.Select(texto, {"0".."9"})
        in
            vResultado,

    Documentacao = [
        Documentation.Name = "Texto.SomenteDigitos",
        Documentation.Description = "Mantém só os dígitos de um texto.",
        Documentation.LongDescription = "Remove pontuação, letras e espaços. Entrada null retorna null; texto sem dígitos retorna texto vazio.",
        Documentation.Category = "Texto",
        Documentation.Author = "OfficeTuning",
        Documentation.Version = "1.0",
        Documentation.Examples = {
            [Description = "CPF formatado", Code = "Texto.SomenteDigitos(""123.456.789-09"")", Result = """12345678909"""],
            [Description = "Sem dígitos", Code = "Texto.SomenteDigitos(""abc"")", Result = """"""]
        }
    ]
in
    Value.ReplaceType(Texto.SomenteDigitos, Value.ReplaceMetadata(Value.Type(Texto.SomenteDigitos), Documentacao))
```

Regras do padrão (todas vêm das funções da Biblioteca):

- **Nulo entra, nulo sai.** Use `??` para tratar nulo no meio do cálculo.
- **Cultura fixa** ao converter número em texto (`Text.From(n, "en-US")`): o
  resultado não pode depender da máquina nem do Service.
- **Tabela de retorno tipada e não vazia de colunas**: combine com
  `#table(type table [Data = date, Feriado = text], {})` para garantir as
  colunas mesmo sem linhas.
- **Dependência declarada** na descrição quando uma função chama outra
  (`Data.FeriadosNoPeriodo` → `Data.Feriados`).
- **Histórico de versão** em `Documentation.Version` e, quando uma versão
  corrige um erro, a lição registrada ("até a 2.0, …").

## Documentar

O Power Query Editor exibe **da função**: `Documentation.Name` (título da janela
de invocação), `Documentation.LongDescription` e `Documentation.Examples`; e,
**por parâmetro**: `Documentation.FieldCaption`, `Documentation.FieldDescription`,
`Documentation.SampleValues` (texto de exemplo esmaecido),
`Documentation.AllowedValues` (vira lista suspensa) e
`Formatting.IsMultiLine`/`Formatting.IsCode`. `Documentation.Description` e
`Documentation.Category` aparecem nos metadados das funções nativas; `Author` e
`Version` são registro da casa.

| Forma | Quando | Como |
|---|---|---|
| Padrão (Biblioteca) | Toda função | Record `Documentacao` + `Value.ReplaceMetadata` (acima) |
| Completa | Função que outras pessoas vão invocar pela janela | `type function` com metadados por parâmetro, `SampleValues` e `AllowedValues` (`padroes-m.md`) |

⚠️ Dataflows do Power BI, Dataflow Gen2 do Fabric e dataflows do Power Platform
**não guardam metadados personalizados** ([Metadata](https://learn.microsoft.com/powerquery-m/metadata)):
a documentação some quando a função vai para um dataflow. Mantenha a origem
documentada no repositório.

## Usar

| Forma | Exemplo |
|---|---|
| Interface | Adicionar Coluna → **Invocar Função Personalizada** |
| `each` | `Table.AddColumn(Origem, "CPF Limpo", each Texto.SomenteDigitos([CPF]), type nullable text)` |
| Função com nome do argumento | `Table.AddColumn(Origem, "CPF Limpo", (linha) => Texto.SomenteDigitos(linha[CPF]), type nullable text)` |

Sempre declare o tipo da coluna nova no quarto argumento do `Table.AddColumn`.

## Desempenho

- Função aplicada linha a linha quase sempre **quebra o Query Folding**: chame-a
  **depois** do último passo dobrável (filtros e seleção de colunas antes).
- Função que acessa fonte por linha (`Web.Contents`, `Sql.Database` dentro do
  `each`) multiplica as chamadas; prefira trazer a tabela uma vez e mesclar.
- Misturar fontes com níveis de privacidade diferentes dentro da função gera
  `Formula.Firewall`: isole o acesso a cada fonte na sua própria consulta.
- `Table.Buffer` dentro da função só para lista ou tabela pequena reusada em
  todas as linhas (ex.: tabela de feriados); nunca "por garantia".

## Testar

Toda função tem uma consulta de teste no grupo Funções, sem carregamento, com
casos conhecidos e o resultado esperado:

```m
let
    Casos = #table(
        type table [Entrada = nullable text, Esperado = nullable text],
        {
            {"123.456.789-09", "12345678909"},
            {"abc", ""},
            {null, null}
        }
    ),
    ComObtido = Table.AddColumn(Casos, "Obtido", each Texto.SomenteDigitos([Entrada]), type nullable text),
    ComOk = Table.AddColumn(ComObtido, "Ok", each [Obtido] = [Esperado], type logical)
in
    ComOk
```

Nome da consulta: `TesteTextoSomenteDigitos`. Qualquer `Ok = false` bloqueia a entrega.
