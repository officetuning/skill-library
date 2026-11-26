<#
.SYNOPSIS
  Converte cada página de um PDF em PNG usando o próprio Windows (Windows.Data.Pdf), sem instalar nada.
.DESCRIPTION
  Serve para conferir o PDF exportado do relatório e para ilustrar o manual do usuário. Exige Windows
  PowerShell 5.1. Páginas ocultas do relatório (Detalhe e Dica) não saem na exportação do Power BI.
.EXAMPLE
  powershell -File renderizar_pdf.ps1 -Pdf "C:\proj\Relatorio.pdf" -Saida "C:\temp\paginas" -Largura 1920
#>
param(
    [Parameter(Mandatory)][string]$Pdf,
    [Parameter(Mandatory)][string]$Saida,
    [int]$Largura = 1920,
    [string]$Prefixo = 'p'
)
$ErrorActionPreference = 'Stop'
$Pdf = (Resolve-Path -LiteralPath $Pdf).Path
New-Item -ItemType Directory -Force -Path $Saida | Out-Null
$Saida = (Resolve-Path -LiteralPath $Saida).Path

Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Data.Pdf.PdfDocument, Windows.Data.Pdf, ContentType = WindowsRuntime]
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$metodos = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 }
$comResultado = $metodos | Where-Object { $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
$semResultado = $metodos | Where-Object { $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncAction' } | Select-Object -First 1
function Wait-Operacao($operacao, $tipo) {
    $tarefa = $comResultado.MakeGenericMethod($tipo).Invoke($null, @($operacao))
    $tarefa.Wait()
    $tarefa.Result
}

$arquivo = Wait-Operacao ([Windows.Storage.StorageFile]::GetFileFromPathAsync($Pdf)) ([Windows.Storage.StorageFile])
$documento = Wait-Operacao ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($arquivo)) ([Windows.Data.Pdf.PdfDocument])
for ($i = 0; $i -lt $documento.PageCount; $i++) {
    $pagina = $documento.GetPage($i)
    $memoria = New-Object Windows.Storage.Streams.InMemoryRandomAccessStream
    $opcoes = New-Object Windows.Data.Pdf.PdfPageRenderOptions
    $opcoes.DestinationWidth = $Largura
    $semResultado.Invoke($null, @($pagina.RenderToStreamAsync($memoria, $opcoes))).Wait()
    $leitura = [System.IO.WindowsRuntimeStreamExtensions]::AsStreamForRead($memoria.GetInputStreamAt(0))
    $destino = Join-Path $Saida ('{0}{1}.png' -f $Prefixo, ($i + 1))
    $gravacao = [System.IO.File]::Create($destino)
    $leitura.CopyTo($gravacao)
    $gravacao.Close()
    $pagina.Dispose()
    $destino
}
