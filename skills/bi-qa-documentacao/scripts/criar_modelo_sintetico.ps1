<#
.SYNOPSIS
    Cria o modelo sintético de teste em um Power BI Desktop com relatório em branco.
.DESCRIPTION
    Grava as tabelas 'Vendas' e 'Calendário', o relacionamento, o calendário
    'Gregoriano' e as medidas Faturado. As linhas vêm de
    gerar_casos_sinteticos.py e as medidas, do código de referência de
    comparativo-ano-anterior.md.

    Só grava em localhost e em modelo sem tabelas. Subir o nível de
    compatibilidade não se desfaz, por isso exige -SubirCompatibilidade.
    Não salva o arquivo: feche sem salvar para descartar.

    Saída: 0 = modelo criado; 1 = falha ao gravar; 2 = recusado antes de gravar.
.EXAMPLE
    .\criar_modelo_sintetico.ps1 -Servidor localhost:51402 -SubirCompatibilidade
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)] [string]$Servidor,
    [switch]$SubirCompatibilidade
)

$ErrorActionPreference = 'Stop'
$nivel = 1702

function Stop-Recusado([string]$motivo) { Write-Host "RECUSADO  $motivo"; exit 2 }

# O motor devolve erro como XML, sem exceção: é preciso olhar a resposta
function Invoke-Comando([string]$consulta) {
    $resposta = (Invoke-ASCmd -Server $Servidor -Query $consulta -ErrorAction Stop) -join ''
    $xml = [xml]$resposta
    $erros = @($xml.SelectNodes("//*[local-name()='Error']"))
    if ($erros.Count -gt 0) { throw (($erros | ForEach-Object { $_.Description }) -join ' ') }
}

function Read-Linhas {
    $texto = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'gerar_casos_sinteticos.py') -Raw -Encoding UTF8
    $achados = [regex]::Matches($texto, '\(date\((\d+), (\d+), (\d+)\), (-?\d+)\)')
    if ($achados.Count -eq 0) { throw 'Nenhuma linha encontrada em gerar_casos_sinteticos.py.' }
    foreach ($m in $achados) {
        '        {{ "{0}-{1:00}-{2:00}", {3} }}' -f $m.Groups[1].Value, [int]$m.Groups[2].Value,
            [int]$m.Groups[3].Value, $m.Groups[4].Value
    }
}

function Read-Medidas {
    $md = Join-Path $PSScriptRoot '../../powerbi-visuais/references/comparativo-ano-anterior.md'
    $texto = (Get-Content -LiteralPath $md -Raw -Encoding UTF8) -replace "`r", ''
    $bloco = [regex]::Match($texto, '(?s)## Código de referência.*?```dax\n(.*?)```').Groups[1].Value
    $medidas = [ordered]@{}
    foreach ($m in [regex]::Matches($bloco, '(?ms)^(Faturado \([^)]+\)) =(.*?)(?=^Faturado \(|\z)')) {
        $medidas[$m.Groups[1].Value] = $m.Groups[2].Value.Trim()
    }
    if ($medidas.Count -ne 5) { throw "Esperadas 5 medidas no código de referência, achadas $($medidas.Count)." }
    $medidas
}

# Tudo é conferido antes da primeira gravação
try {
    if ($Servidor -notmatch '^localhost:\d+$') { Stop-Recusado 'só grava em um Desktop local (localhost:<porta>).' }
    $linhas = @(Read-Linhas)
    $medidas = Read-Medidas

    $modulo = Get-Module -ListAvailable SqlServer | Sort-Object Version -Descending | Select-Object -First 1
    if (-not $modulo) { Stop-Recusado 'módulo SqlServer não encontrado.' }
    Import-Module SqlServer
    $pasta = $modulo.ModuleBase
    if ($PSVersionTable.PSEdition -eq 'Core') { $pasta = Join-Path $pasta 'coreclr' }
    Add-Type -Path (Join-Path $pasta 'Microsoft.AnalysisServices.Tabular.dll')

    $servidorTom = New-Object Microsoft.AnalysisServices.Tabular.Server
    $servidorTom.Connect($Servidor)
    if ($servidorTom.Databases.Count -ne 1) { Stop-Recusado "esperado 1 banco no servidor, há $($servidorTom.Databases.Count)." }
    $banco = $servidorTom.Databases[0]
    $modelo = $banco.Model
    if ($modelo.Tables.Count -gt 0) {
        Stop-Recusado "o modelo já tem $($modelo.Tables.Count) tabela(s). Use um relatório em branco."
    }
    if ($banco.CompatibilityLevel -lt $nivel -and -not $SubirCompatibilidade) {
        Stop-Recusado "compatibilidade $($banco.CompatibilityLevel); é preciso $nivel. Isso não se desfaz: repita com -SubirCompatibilidade."
    }
} catch {
    Stop-Recusado $_.Exception.Message
}

try {
    $T = 'Microsoft.AnalysisServices.Tabular'
    if ($banco.CompatibilityLevel -lt $nivel) {
        $banco.CompatibilityLevel = $nivel
        $banco.Update()
    }

    $dax = [ordered]@{
        'Vendas'     = "DATATABLE (`n    ""Data"", DATETIME,`n    ""Valor da Venda"", CURRENCY,`n    {`n" +
                       ($linhas -join ",`n") + "`n    }`n)"
        'Calendário' = @'
ADDCOLUMNS (
    SELECTCOLUMNS ( CALENDAR ( DATE ( 2023, 1, 1 ), DATE ( 2026, 12, 31 ) ), "Data", [Date] ),
    "Ano", YEAR ( [Data] ),
    "Trimestre #", QUARTER ( [Data] ),
    "Mês #", MONTH ( [Data] ),
    "Ano/Mês", FORMAT ( [Data], "yyyy/MM" ),
    "Dia", DAY ( [Data] )
)
'@
    }
    foreach ($nome in $dax.Keys) {
        $origem = New-Object "$T.CalculatedPartitionSource"
        $origem.Expression = $dax[$nome]
        $particao = New-Object "$T.Partition"
        $particao.Name = $nome
        $particao.Source = $origem
        $tabela = New-Object "$T.Table"
        $tabela.Name = $nome
        $tabela.Description = 'Dados sintéticos de teste.'
        $tabela.Partitions.Add($particao)
        $modelo.Tables.Add($tabela)
    }
    $modelo.RequestRefresh([Microsoft.AnalysisServices.Tabular.RefreshType]::Calculate)
    [void]$modelo.SaveChanges()
    # As colunas das tabelas calculadas são criadas pelo motor
    $modelo.Sync()

    $vendas = $modelo.Tables['Vendas']
    $calendario = $modelo.Tables['Calendário']
    $calendario.DataCategory = 'Time'
    $calendario.Columns['Data'].IsKey = $true

    $relacao = New-Object "$T.SingleColumnRelationship"
    $relacao.Name = 'Vendas_Data_Calendario_Data'
    $relacao.FromColumn = $vendas.Columns['Data']
    $relacao.ToColumn = $calendario.Columns['Data']
    $modelo.Relationships.Add($relacao)

    foreach ($nome in $medidas.Keys) {
        $medida = New-Object "$T.Measure"
        $medida.Name = $nome
        $medida.Expression = $medidas[$nome]
        if ($nome -like '*%)') { $medida.FormatString = '#,0.00%;(#,0.00%);#,0.00%' }
        elseif ($nome -notlike '*i)') { $medida.FormatString = '#,0' }
        $medida.Description = 'Medida de teste, copiada de comparativo-ano-anterior.md.'
        $vendas.Measures.Add($medida)
    }
    [void]$modelo.SaveChanges()

    # O calendário vai por TMSL: a TOM do módulo SqlServer (19.96) o recusa no modo
    # Power BI. É a última alteração, porque essa TOM não grava mais depois dele.
    $definicao = [Microsoft.AnalysisServices.Tabular.JsonSerializer]::SerializeObject($calendario) | ConvertFrom-Json
    $categorias = [ordered]@{
        year = 'Ano'; quarterOfYear = 'Trimestre #'; month = 'Ano/Mês'
        monthOfYear = 'Mês #'; dayOfMonth = 'Dia'; date = 'Data'
    }
    $grupos = @($categorias.Keys | ForEach-Object { @{ timeUnit = $_; primaryColumn = $categorias[$_] } })
    $definicao | Add-Member -NotePropertyName calendars -NotePropertyValue @(
        @{ name = 'Gregoriano'; calendarColumnGroups = $grupos })
    Invoke-Comando (@{ createOrReplace = @{
        object = @{ database = $banco.ID; table = 'Calendário' }
        table  = $definicao
    } } | ConvertTo-Json -Depth 12)

    # Sem este recálculo o relacionamento novo dá erro em qualquer consulta
    Invoke-Comando (@{ refresh = @{ type = 'calculate'; objects = @(@{ database = $banco.ID }) } } |
        ConvertTo-Json -Depth 5)
} catch {
    Write-Host "FALHA  $($_.Exception.Message)"
    Write-Host 'O modelo pode ter ficado incompleto: feche o relatório sem salvar.'
    exit 1
} finally {
    $servidorTom.Disconnect()
}

Write-Host "Modelo criado em $Servidor, banco $($banco.ID), compatibilidade $nivel."
Write-Host "Linhas em 'Vendas': $($linhas.Count). Medidas: $($medidas.Keys -join ', ')."
exit 0
