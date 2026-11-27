# Carga de uma pasta com vários arquivos

Lições de um relatório que combina um arquivo Excel por mês de uma pasta do
SharePoint. O que está marcado **[verificado]** foi medido nesse caso.

## Pergunta antes de transformar
> O que cada arquivo promete entregar, e o que acontece quando ele entrega mais?

## Riscos

| Risco | Como aparece | Prevenção |
|---|---|---|
| Cabeçalho promovido vem do **primeiro** arquivo | colunas lidas por posição; um layout novo troca o conteúdo sem erro | validar o cabeçalho de cada arquivo nas posições lidas |
| Arquivo **cumulativo** ao lado dos mensais | meses contados duas vezes | cada arquivo contribui só com o período do próprio nome |
| `Table.Distinct` depois de selecionar colunas | esconde parte da sobreposição e **apaga repetições válidas** cuja diferença estava nas colunas descartadas | medir antes de remover |
| Versões do mesmo mês com campos de cadastro diferentes | o `Distinct` mantém as duas **[verificado]** | tratar pelo arquivo de origem, não pela igualdade da linha |
| Número de colunas varia | identificadores existem em uns arquivos e faltam em outros | não usar coluna instável como chave |

## Medir antes de remover duplicatas
Numa consulta temporária, **mantendo o nome do arquivo**, conte por período:
1. linhas e valor sem nenhuma remoção;
2. repetições **dentro** do mesmo arquivo e **entre** arquivos, separadamente;
3. para as repetidas, quais colunas descartadas diferem;
4. se dois arquivos cobrem o mesmo período, os totais de cada um.

Só então escolha a regra, simule os totais por período e peça aprovação: valores já
publicados podem mudar.

## Filtrar pelo período do nome do arquivo
Padrão de exemplo `Dados AAAA_MM.xlsx`. A coluna `Arquivo` vem do nome do arquivo,
renomeada depois de promover os cabeçalhos (a primeira coluna recebe como título o
valor da primeira linha).

```m
DoPeriodo = Table.SelectRows(
    Tipado,
    each [Arquivo] = "Dados " & Text.From([Ano]) & "_"
        & Text.PadStart(Text.From([Mês]), 2, "0") & ".xlsx"
)
```

⚠️ A comparação exata ignora **em silêncio** o arquivo com nome fora do padrão (e
evita somar cópias como "(1)"). Por isso ela pede a validação da carga
(`bi-qa-documentacao`, `references/validacao-da-carga.md`).

## Fim de período fixo
`RangeEnd = #date(2027, 10, 1)` usado como limite da fato e do calendário faz a
carga **parar** nessa data, sem erro. **Com Incremental Refresh**, mantenha os
parâmetros no formato exigido (a política os sobrescreve). **Sem ele**, o limite
pode ser uma consulta calculada. Exemplo para ano fiscal que começa em outubro:

```m
let
    Hoje = Date.From(DateTime.LocalNow()),
    FimAnoFiscal = #date(Date.Year(Hoje) + (if Date.Month(Hoje) >= 10 then 1 else 0), 9, 30)
in
    FimAnoFiscal
```

No Service, `DateTime.LocalNow()` segue o relógio do servidor (UTC): só importa nas
horas próximas da virada. O calendário passa a terminar no fim do ano fiscal, sem
ano com um único dia.
