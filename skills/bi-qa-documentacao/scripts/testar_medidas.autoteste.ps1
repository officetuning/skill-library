<#
.SYNOPSIS
    Autoteste de testar_medidas.ps1 com um Invoke-ASCmd simulado.
.DESCRIPTION
    Não conecta em servidor e não exige o módulo SqlServer. Confere se o teste de
    medidas aprova o que deve aprovar e reprova o que deve reprovar. Não prova que
    a resposta simulada é igual à de um servidor real.
.EXAMPLE
    pwsh -File testar_medidas.autoteste.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot 'testar_medidas.ps1'
$casosComparativo = Join-Path $PSScriptRoot '../assets/casos-regra-comparativo.json'
$pasta = Join-Path ([IO.Path]::GetTempPath()) ('autoteste-' + [guid]::NewGuid())
New-Item -ItemType Directory -Path $pasta | Out-Null

# Fila de respostas do simulador e consultas recebidas
$global:Respostas = New-Object System.Collections.Queue
$global:Consultas = New-Object System.Collections.ArrayList

function Invoke-ASCmd {
    [CmdletBinding()]
    param($Server, $Database, $Query)
    [void]$global:Consultas.Add($Query)
    if ($global:Respostas.Count -eq 0) { throw 'Simulador sem resposta na fila' }
    $r = $global:Respostas.Dequeue()
    if ($r -is [System.Exception]) { throw $r }
    return $r
}

# Formato capturado de um motor real (Power BI Desktop, 26/11/2026): o tipo de cada
# coluna vem só no xsd:schema do início; os valores não têm xsi:type, e o <row>
# declara o próprio namespace.
function Envelope([string]$corpo, [string]$tipo = 'long') {
    '<return xmlns="urn:schemas-microsoft-com:xml-analysis">' +
    '<root xmlns="urn:schemas-microsoft-com:xml-analysis:mddataset" ' +
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' +
    'xmlns:xsd="http://www.w3.org/2001/XMLSchema">' +
    '<xsd:schema targetNamespace="urn:schemas-microsoft-com:xml-analysis:rowset" ' +
    'xmlns:sql="urn:schemas-microsoft-com:xml-sql" elementFormDefault="qualified">' +
    '<xsd:complexType name="row"><xsd:sequence>' +
    '<xsd:element sql:field="[sentinela]" name="_x005B_sentinela_x005D_" type="xsd:long" minOccurs="0" />' +
    "<xsd:element sql:field=""[valor]"" name=""_x005B_valor_x005D_"" type=""xsd:$tipo"" minOccurs=""0"" />" +
    '</xsd:sequence></xsd:complexType></xsd:schema>' + $corpo + '</root></return>'
}

# $null = coluna ausente (em branco); '' = texto vazio
function Linha($valor) {
    $xml = '<row xmlns="urn:schemas-microsoft-com:xml-analysis:rowset"><_x005B_sentinela_x005D_>1</_x005B_sentinela_x005D_>'
    if ($null -ne $valor) {
        $texto = [Security.SecurityElement]::Escape([string]$valor)
        $xml += "<_x005B_valor_x005D_>$texto</_x005B_valor_x005D_>"
    }
    $xml + '</row>'
}

# Sem $tipo, deduz como o motor: texto não numérico = string; com ponto = double
function Resposta($valor, [string]$tipo = '') {
    if (-not $tipo) {
        $tipo = if ($null -eq $valor) { 'long' }
                elseif ("$valor" -notmatch '^-?[\d.]+(E-?\d+)?$') { 'string' }
                elseif ("$valor" -match '[.E]') { 'double' }
                else { 'long' }
    }
    Envelope (Linha $valor) $tipo
}

# Erro de DAX: o motor responde XML normal, sem exceção do PowerShell
function RespostaErro([string]$descricao) {
    '<return xmlns="urn:schemas-microsoft-com:xml-analysis"><root xmlns="urn:schemas-microsoft-com:xml-analysis:empty">' +
    '<Exception xmlns="urn:schemas-microsoft-com:xml-analysis:exception" />' +
    '<Messages xmlns="urn:schemas-microsoft-com:xml-analysis:exception">' +
    "<Error ErrorCode=""-1053163476"" Description=""$descricao"" Source=""Microsoft Analysis Services"" />" +
    '</Messages></root></return>'
}

function NovoArquivo([string]$conteudo) {
    $caminho = Join-Path $pasta ([guid]::NewGuid().ToString() + '.json')
    [IO.File]::WriteAllText($caminho, $conteudo, (New-Object Text.UTF8Encoding($false)))
    $caminho
}

# Um arquivo com uma única verificação; $esperado é o trecho JSON
function UmCaso([string]$esperado, [string]$extra = '') {
    NovoArquivo ('{"casos":[{"nome":"c","verificar":[{"expressao":"[M]","esperado":' +
        $esperado + $extra + '}]}]}')
}

$global:Falhas = 0
function Conferir([string]$nome, [string]$arquivo, [object[]]$respostas, [int]$saida, [int]$consultas = -1) {
    $global:Respostas.Clear()
    $global:Consultas.Clear()
    foreach ($r in $respostas) { $global:Respostas.Enqueue($r) }
    $global:LASTEXITCODE = $null
    $registro = & $script -Servidor 'simulado' -Banco 'simulado' -Casos $arquivo *>&1 | Out-String
    $problema = @()
    if ($global:LASTEXITCODE -ne $saida) { $problema += "saída $($global:LASTEXITCODE), esperada $saida" }
    if ($consultas -ge 0 -and $global:Consultas.Count -ne $consultas) {
        $problema += "$($global:Consultas.Count) consultas, esperadas $consultas"
    }
    if ($problema.Count -eq 0) {
        Write-Host "OK     $nome"
    } else {
        $global:Falhas++
        Write-Host "FALHA  $nome : $($problema -join '; ')"
        Write-Host $registro
    }
}

try {
    # Tabela de "Casos de teste" de comparativo-ano-anterior.md, na mesma ordem:
    # Δ, Δ%, Δi de cada caso
    $certo = @(
        $null, $null, $null,
        $null, $null, $null,
        100,   $null, '✔️',
        50,    '5.E-1', '✔️',
        0,     0,     '⚠️'
    )
    $respostasCertas = @($certo | ForEach-Object { Resposta $_ })
    Conferir 'cinco casos corretos passam' $casosComparativo $respostasCertas 0 15

    $consulta = [string]$global:Consultas[0]
    if ($consulta -match "MEASURE 'Vendas'\[Faturado \(AV\)\] = BLANK \(\)" -and
        $consulta -match "MEASURE 'Vendas'\[Faturado \(AA\)\] = 100" -and
        $consulta -match "MEASURE 'Vendas'\[Faturado \(Δ\)\] =") {
        Write-Host 'OK     a consulta substitui AV e AA'
    } else {
        $global:Falhas++
        Write-Host "FALHA  a consulta substitui AV e AA :`n$consulta"
    }

    # "definir" no topo vale para todos os casos; o caso pode trocar uma medida
    $comum = NovoArquivo @'
{"definir":{"'T'[A]":"1","'T'[B]":"[A] + 1"},"casos":[{"nome":"c","definir":{"'T'[A]":"9"},"verificar":[{"expressao":"[B]","esperado":10}]}]}
'@
    Conferir 'definir comum, com troca no caso' $comum @(Resposta 10) 0 1
    $consulta = [string]$global:Consultas[0]
    if ($consulta -match "MEASURE 'T'\[A\] = 9" -and $consulta -match "MEASURE 'T'\[B\] = \[A\] \+ 1" -and
        $consulta -notmatch "\[A\] = 1") {
        Write-Host 'OK     o caso troca a medida comum e herda as outras'
    } else {
        $global:Falhas++
        Write-Host "FALHA  o caso troca a medida comum e herda as outras :`n$consulta"
    }

    # Fórmula antiga: sem valor atual, Δ% devolvia -1 sem nenhum erro de DAX
    $antiga = @($respostasCertas)
    $antiga[1] = Resposta '-1'
    Conferir 'valor errado sem erro de DAX reprova' $casosComparativo $antiga 1 15

    Conferir 'em branco onde se esperava 0 reprova' (UmCaso '0') @(Resposta $null) 1
    Conferir '0 onde se esperava em branco reprova' (UmCaso 'null') @(Resposta 0) 1
    Conferir 'texto vazio não é em branco'          (UmCaso 'null') @(Resposta '') 1
    Conferir 'xsi:nil conta como em branco' (UmCaso 'null') @(
        Envelope '<row xmlns="urn:schemas-microsoft-com:xml-analysis:rowset"><_x005B_sentinela_x005D_>1</_x005B_sentinela_x005D_><_x005B_valor_x005D_ xsi:nil="true"/></row>') 0
    Conferir 'farol trocado reprova'                (UmCaso '"✔️"') @(Resposta '❗') 1
    Conferir 'texto onde se esperava número reprova' (UmCaso '50') @(Resposta '50' 'string') 1
    Conferir 'número onde se esperava texto reprova' (UmCaso '"50"') @(Resposta '50' 'long') 1
    Conferir 'diferença dentro da tolerância passa' (UmCaso '0.5') @(Resposta '0.5000001') 0
    Conferir 'diferença fora da tolerância reprova' (UmCaso '0.5') @(Resposta '0.51') 1
    Conferir 'tolerância própria do caso'           (UmCaso '100' ',"tolerancia":1') @(Resposta '100.9') 0
    Conferir 'notação científica'                   (UmCaso '1500000') @(Resposta '1.5E6' 'double') 0
    Conferir 'infinito reprova'                     (UmCaso '0') @(Resposta 'INF' 'double') 1

    $anterior = [Threading.Thread]::CurrentThread.CurrentCulture
    try {
        [Threading.Thread]::CurrentThread.CurrentCulture = [Globalization.CultureInfo]'pt-BR'
        Conferir 'decimal do motor (5.E-1) em Windows pt-BR' (UmCaso '0.5') @(Resposta '5.E-1') 0
    } finally {
        [Threading.Thread]::CurrentThread.CurrentCulture = $anterior
    }

    # Respostas que não podem ser confundidas com "em branco"
    $vazio = UmCaso 'null'
    Conferir 'erro XMLA no corpo reprova' $vazio @(RespostaErro 'A coluna não existe') 1
    Conferir 'exceção do Invoke-ASCmd reprova' $vazio @(New-Object System.Exception 'sem conexão') 1
    Conferir 'resposta sem linha reprova' $vazio @(Envelope '') 1
    Conferir 'duas linhas reprovam' $vazio @(Envelope ((Linha $null) + (Linha $null))) 1
    Conferir 'linha sem sentinela reprova' $vazio @(Envelope '<row/>') 1
    Conferir 'coluna inesperada reprova' $vazio @(
        Envelope '<row><_x005B_sentinela_x005D_>1</_x005B_sentinela_x005D_><outra>1</outra></row>') 1
    Conferir 'resposta que não é XML reprova' $vazio @('falhou') 1
    Conferir 'resposta vazia reprova' $vazio @('') 1

    # Erro no arquivo de casos: saída 2 antes de qualquer consulta
    Conferir 'sem a chave "esperado"' (NovoArquivo '{"casos":[{"nome":"c","verificar":[{"expressao":"[M]"}]}]}') @() 2 0
    Conferir 'lista de casos vazia' (NovoArquivo '{"casos":[]}') @() 2 0
    Conferir 'arquivo sem "casos"' (NovoArquivo '{}') @() 2 0
    Conferir 'caso sem verificação' (NovoArquivo '{"casos":[{"nome":"c","verificar":[]}]}') @() 2 0
    Conferir 'JSON inválido' (NovoArquivo '{') @() 2 0
    Conferir 'arquivo inexistente' (Join-Path $pasta 'nao-existe.json') @() 2 0
    Conferir 'nome de medida sem tabela em "definir"' (NovoArquivo '{"casos":[{"nome":"c","definir":{"[M]":"1"},"verificar":[{"expressao":"[M]","esperado":1}]}]}') @() 2 0
    Conferir 'tolerância negativa' (UmCaso '1' ',"tolerancia":-1') @() 2 0
    Conferir 'tipo de "esperado" não aceito' (UmCaso '[1,2]') @() 2 0
} finally {
    Remove-Item -Recurse -Force $pasta
}

if ($global:Falhas -gt 0) { Write-Host "$($global:Falhas) falha(s) no autoteste"; exit 1 }
Write-Host 'Autoteste aprovado'
exit 0
