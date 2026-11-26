<#
.SYNOPSIS
    Testa medidas via XMLA comparando cada resultado com o valor esperado.
.DESCRIPTION
    Cada verificação do arquivo de casos vira uma consulta DAX. O teste reprova
    com erro de DAX, resposta em formato inesperado ou valor diferente do esperado.
    "definir" substitui medidas só durante a consulta (DEFINE MEASURE) e
    "funcoes" cria UDFs só da consulta (DEFINE FUNCTION); o modelo não é alterado.

    Saída: 0 = tudo conferiu; 1 = alguma verificação falhou;
    2 = erro de configuração (arquivo de casos ou módulo ausente).
.EXAMPLE
    .\testar_medidas.ps1 -Servidor "powerbi://api.powerbi.com/v1.0/myorg/Staging" -Banco "VendasAurora" -Casos .\casos.json
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)] [string]$Servidor,
    [Parameter(Mandatory = $true)] [string]$Banco,
    [Parameter(Mandatory = $true)] [string]$Casos
)

$ErrorActionPreference = 'Stop'
$invariante = [Globalization.CultureInfo]::InvariantCulture

function Test-Numero($v) {
    ($v -is [int]) -or ($v -is [long]) -or ($v -is [decimal]) -or ($v -is [double])
}

function Get-Lista($v) { @($v | Where-Object { $null -ne $_ }) }

# Valida o arquivo inteiro antes da primeira consulta
function Read-Verificacoes([string]$caminho) {
    $json = Get-Content -LiteralPath $caminho -Raw -Encoding UTF8 | ConvertFrom-Json
    $casos = @(Get-Lista $json.casos)
    if ($casos.Count -eq 0) { throw 'Nenhum caso em "casos".' }
    foreach ($caso in $casos) {
        if (-not $caso.nome) { throw 'Caso sem "nome".' }
        # "funcoes" são UDFs só da consulta, com a mesma troca por nome
        $funcoes = [ordered]@{}
        foreach ($origem in @($json.funcoes, $caso.funcoes)) {
            if (-not $origem) { continue }
            foreach ($p in $origem.PSObject.Properties) {
                if ($p.Name -notmatch '^[A-Za-z_][A-Za-z0-9_.]*$') {
                    throw "$($caso.nome): nome de função inválido em ""funcoes"": $($p.Name)"
                }
                if ([string]::IsNullOrWhiteSpace($p.Value)) { throw "$($caso.nome): $($p.Name) sem corpo." }
                $funcoes[$p.Name] = $p.Value
            }
        }
        # "definir" do topo vale para todos; o do caso troca a medida de mesmo nome
        $medidas = [ordered]@{}
        foreach ($origem in @($json.definir, $caso.definir)) {
            if (-not $origem) { continue }
            foreach ($p in $origem.PSObject.Properties) {
                if ($p.Name -notmatch "^('.+'|\w+)\[.+\]$") {
                    throw "$($caso.nome): em ""definir"", use 'Tabela'[Medida]. Recebido: $($p.Name)"
                }
                if ([string]::IsNullOrWhiteSpace($p.Value)) { throw "$($caso.nome): $($p.Name) sem expressão." }
                $medidas[$p.Name] = $p.Value
            }
        }
        $definicoes = @(
            $funcoes.Keys | ForEach-Object { "    FUNCTION $_ = $($funcoes[$_])" }
            $medidas.Keys | ForEach-Object { "    MEASURE $_ = $($medidas[$_])" }
        )
        $verificar = @(Get-Lista $caso.verificar)
        if ($verificar.Count -eq 0) { throw "$($caso.nome): nada em ""verificar""." }
        foreach ($v in $verificar) {
            if (-not $v.expressao) { throw "$($caso.nome): verificação sem ""expressao""." }
            # null é um valor válido (em branco); chave ausente é erro
            if ($null -eq $v.PSObject.Properties['esperado']) {
                throw "$($caso.nome) $($v.expressao): falta ""esperado"" (use null para em branco)."
            }
            $esperado = $v.esperado
            if (-not ($null -eq $esperado -or $esperado -is [string] -or (Test-Numero $esperado))) {
                throw "$($caso.nome) $($v.expressao): ""esperado"" aceita número, texto ou null."
            }
            $tolerancia = 0.000001
            if ($null -ne $v.PSObject.Properties['tolerancia']) {
                if (-not (Test-Numero $v.tolerancia) -or $v.tolerancia -lt 0) {
                    throw "$($caso.nome) $($v.expressao): ""tolerancia"" deve ser um número >= 0."
                }
                $tolerancia = [double]$v.tolerancia
            }
            $linhas = @()
            if ($definicoes.Count -gt 0) { $linhas += 'DEFINE'; $linhas += $definicoes }
            # A sentinela garante uma linha mesmo quando o valor é em branco
            $linhas += 'EVALUATE'
            $linhas += "ROW ( ""sentinela"", 1, ""valor"", $($v.expressao) )"
            [pscustomobject]@{
                Nome       = "$($caso.nome) | $($v.expressao)"
                Consulta   = $linhas -join "`n"
                Esperado   = $esperado
                Tolerancia = $tolerancia
            }
        }
    }
}

# Devolve o valor da consulta. Só é "em branco" se a resposta tiver o formato
# esperado: uma linha, com a sentinela, e a coluna "valor" ausente ou nula.
function Read-Valor([string]$resposta) {
    if ([string]::IsNullOrWhiteSpace($resposta)) { throw 'Resposta vazia.' }
    $xml = New-Object System.Xml.XmlDocument
    $xml.PreserveWhitespace = $true
    $xml.LoadXml($resposta)

    $erros = $xml.SelectNodes("//*[local-name()='Error' or local-name()='Exception']")
    if ($erros.Count -gt 0) { throw "Erro retornado pelo servidor: $(($erros | ForEach-Object { $_.OuterXml }) -join ' ')" }

    $linhas = @($xml.SelectNodes("//*[local-name()='row' and namespace-uri()='urn:schemas-microsoft-com:xml-analysis:rowset']"))
    if ($linhas.Count -ne 1) { throw "Esperada 1 linha, recebidas $($linhas.Count)." }

    $colunas = @{}
    foreach ($no in $linhas[0].ChildNodes) {
        if ($no.NodeType -ne [Xml.XmlNodeType]::Element) { continue }
        $nome = [Xml.XmlConvert]::DecodeName($no.LocalName)
        if (@('[sentinela]', '[valor]') -notcontains $nome -or $colunas.ContainsKey($nome)) {
            throw "Coluna inesperada na resposta: $nome"
        }
        $colunas[$nome] = $no
    }
    if (-not $colunas.ContainsKey('[sentinela]') -or $colunas['[sentinela]'].InnerText -ne '1') {
        throw 'Resposta sem a coluna sentinela; formato não reconhecido.'
    }

    $esquema = 'http://www.w3.org/2001/XMLSchema-instance'
    $no = $colunas['[valor]']
    if ($null -eq $no -or $no.GetAttribute('nil', $esquema) -eq 'true') {
        return [pscustomobject]@{ EmBranco = $true; Texto = $null; Tipo = '' }
    }
    # O motor não põe xsi:type nos valores; o tipo da coluna vem no xsd:schema
    $declaracao = $xml.SelectSingleNode("//*[local-name()='element' and @name='_x005B_valor_x005D_']")
    $tipo = if ($declaracao) { $declaracao.GetAttribute('type') -replace '^.*:', '' } else { '' }
    [pscustomobject]@{
        EmBranco = $false
        Texto    = $no.InnerText
        Tipo     = $tipo
    }
}

function Format-Valor($v) {
    if ($null -eq $v) { return '(em branco)' }
    if ($v -is [string]) { return """$v""" }
    [Convert]::ToString($v, $invariante)
}

# Devolve $null quando confere, ou a descrição da diferença
function Compare-Valor($obtido, $esperado, [double]$tolerancia) {
    $texto = if ($obtido.EmBranco) { '(em branco)' } else { """$($obtido.Texto)""" }
    $diferenca = "esperado $(Format-Valor $esperado), obtido $texto"

    if ($null -eq $esperado) {
        if ($obtido.EmBranco) { return $null }
        return $diferenca
    }
    if ($obtido.EmBranco) { return $diferenca }

    if ($esperado -is [string]) {
        if ($obtido.Tipo -and $obtido.Tipo -ne 'string') { return "$diferenca (tipo $($obtido.Tipo))" }
        if ([string]::Equals($obtido.Texto, $esperado, [StringComparison]::Ordinal)) { return $null }
        return $diferenca
    }

    if ($obtido.Tipo -eq 'string') { return "$diferenca (texto, não número)" }
    $numero = 0.0
    if (-not [double]::TryParse($obtido.Texto, [Globalization.NumberStyles]::Float, $invariante, [ref]$numero)) {
        return "$diferenca (não é número)"
    }
    if ([double]::IsNaN($numero) -or [double]::IsInfinity($numero)) { return $diferenca }
    if ([math]::Abs($numero - [double]$esperado) -le $tolerancia) { return $null }
    $diferenca
}

try {
    $verificacoes = @(Read-Verificacoes $Casos)
    if (-not (Get-Command Invoke-ASCmd -ErrorAction SilentlyContinue)) {
        throw 'Invoke-ASCmd não encontrado. Instale com: Install-Module -Name SqlServer'
    }
} catch {
    Write-Host "CONFIGURAÇÃO  $($_.Exception.Message)"
    exit 2
}

$falhas = 0
foreach ($v in $verificacoes) {
    try {
        $resposta = Invoke-ASCmd -Server $Servidor -Database $Banco -Query $v.Consulta -ErrorAction Stop
        $problema = Compare-Valor (Read-Valor ($resposta -join '')) $v.Esperado $v.Tolerancia
    } catch {
        $problema = $_.Exception.Message
    }
    if ($null -eq $problema) {
        Write-Host "OK     $($v.Nome)"
    } else {
        $falhas++
        Write-Host "FALHA  $($v.Nome) : $problema"
        Write-Host $v.Consulta
    }
}

Write-Host "$($verificacoes.Count - $falhas) de $($verificacoes.Count) verificações conferem."
if ($falhas -gt 0) { exit 1 }
exit 0
