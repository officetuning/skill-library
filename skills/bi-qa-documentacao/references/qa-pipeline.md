# QA via linha de comando

⚠️ Não existe um CLI oficial único da Microsoft que valide um PBIP de ponta a
ponta. O padrão de mercado combina ferramentas comunitárias (Tabular Editor) e
módulos oficiais não exclusivos do Power BI (`SqlServer` / `Invoke-ASCmd`).
Confirme a versão que o time usa antes de colar em pipeline de produção.

## Camada 1 — Best Practice Analyzer (Tabular Editor 2 CLI)

Valida as regras da skill `powerbi-boas-praticas` contra a pasta TMDL, sem abrir
o Desktop. O CLI do Tabular Editor 2 não exige licença do Tabular Editor 3.

```powershell
# PowerShell: -Wait é obrigatório (WinForms) e o exit code é repassado ao pipeline
$p = Start-Process -FilePath "TabularEditor.exe" -Wait -NoNewWindow -PassThru `
       -ArgumentList "`"C:\repo\VendasAurora.SemanticModel\definition`" -A `"C:\repo\ci\BPARules.json`" -V -T `"C:\repo\artifacts\bpa.trx`""
exit $p.ExitCode
```

```cmd
:: cmd
start /wait TabularEditor.exe "C:\repo\VendasAurora.SemanticModel\definition" -A "C:\repo\ci\BPARules.json" -V
```

| Opção | Efeito |
|---|---|
| 1º argumento | Pasta do modelo (ou `Model.bim`) |
| `-A <regras>` | Roda o BPA com o arquivo de regras informado (caminho ou URL) |
| `-AX <regras>` | Idem, ignorando regras anotadas no próprio modelo |
| `-V` / `-G` | Comandos de log do Azure DevOps / anotações do GitHub Actions |
| `-T <arquivo>` | Gera resultado VSTEST (`.trx`) para anexar ao pipeline |

**Severidade → nível → exit code** (documentação do Tabular Editor):

| Severidade da regra | Nível | Efeito |
|---|---|---|
| 1 | Informação | Não falha |
| 2 | Warning | Não falha |
| ≥ 3 | Error | **Exit code 1** |

Para barrar o merge nas regras Altas 🔴, deixe-as com severidade 3 no
`BPARules.json` versionado. As regras oficiais estão em
[microsoft/Analysis-Services/BestPracticeRules](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules).

Altas que devem barrar:
- `USERELATIONSHIP` + RLS na mesma tabela
- Caractere inválido em nome ou descrição
- `IsAvailableInMdx = false` em coluna necessária para MDX
- M:M em tabela com RLS dinâmico
- Tipos diferentes nas colunas de um relacionamento
- Coluna sem origem ou objeto com expressão vazia
- Medida sem format string
- Sumarização automática em coluna numérica que não é métrica

Existe também o Tabular Editor CLI multiplataforma (`te`), com
`te bpa run --fail-on error`; estava em preview limitado (até 2026-10-31) na data
desta base. Para produção, a documentação recomenda o `TabularEditor.exe`.

[Tabular Editor 2 — linha de comando](https://docs.tabulareditor.com/en/features/Command-line-Options.html)

## Camada 2 — Smoke test de medidas via XMLA

Pega o que a análise estática não pega: erro de DAX em execução, referência
circular. O Desktop não tem modo de linha de comando para "abrir e testar";
publique num workspace de **staging** e consulte pelo endpoint XMLA.

Pré-requisitos: workspace com XMLA habilitado (Premium, PPU ou Fabric),
`Install-Module -Name SqlServer`, modelo já publicado.

```powershell
$servidor = "powerbi://api.powerbi.com/v1.0/myorg/StagingWorkspace"
$banco    = "VendasAurora"
$medidas  = @("Total de Vendas AV", "Ticket Médio", "Margem Bruta (%)", "Δ% Total de Vendas")
$falhas   = @()

foreach ($m in $medidas) {
    # Colchetes no nome da medida são escapados com ]]
    $dax = "EVALUATE ROW(""Teste"", [$($m -replace '\]', ']]')])"
    try {
        $r = Invoke-ASCmd -Server $servidor -Database $banco -Query $dax -ErrorAction Stop
        # Invoke-ASCmd devolve XML; erro de DAX vem como <Error> no corpo
        if ($r -match "<Error") { throw ($r -replace '\s+', ' ') }
        Write-Host "✔️ $m"
    } catch {
        $falhas += $m
        Write-Host "❗ $m : $($_.Exception.Message)"
    }
}

if ($falhas.Count -gt 0) { Write-Error "Medidas com erro: $($falhas -join ', ')"; exit 1 }
```

É a versão em lote do `DEFINE MEASURE` + `EVALUATE ROW(...)` da DAX Query View.
Rode como job **depois** do deploy para staging.

[Invoke-ASCmd](https://learn.microsoft.com/pt-br/powershell/module/sqlserver/invoke-ascmd) ·
[Endpoint XMLA](https://learn.microsoft.com/pt-br/power-bi/enterprise/service-premium-connect-tools)

## Camada 3 — Binding visual × modelo

O BPA audita só o `.SemanticModel`; não lê `visual.json`. Campo renomeado ou
excluído no modelo deixa visuais quebrados em silêncio.

```bash
python scripts/check_visual_bindings.py \
    VendasAurora.SemanticModel/definition \
    VendasAurora.Report/definition
```

Percorre o JSON inteiro de cada `visual.json` (coluna, medida, agregação,
hierarquia) e compara `(tabela, campo)` com o TMDL. Exit 1 se houver quebra.

## Pipeline de exemplo (GitHub Actions)

```yaml
name: qa-power-bi

on:
  pull_request:
    paths:
      - '**/*.SemanticModel/**'
      - '**/*.Report/**'

jobs:
  qa:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Camada 3 — binding visual × modelo
        run: python ci/check_visual_bindings.py VendasAurora.SemanticModel/definition VendasAurora.Report/definition

      - name: Instalar Tabular Editor 2 (portátil)
        shell: pwsh
        run: |
          Invoke-WebRequest -Uri "https://github.com/TabularEditor/TabularEditor/releases/latest/download/TabularEditor.Portable.zip" -OutFile te2.zip
          Expand-Archive te2.zip -DestinationPath .\te2

      - name: Camada 1 — Best Practice Analyzer
        shell: pwsh
        run: |
          New-Item -ItemType Directory -Force artifacts | Out-Null
          $p = Start-Process -FilePath ".\te2\TabularEditor.exe" -Wait -NoNewWindow -PassThru `
                 -ArgumentList "`"VendasAurora.SemanticModel\definition`" -A `"ci\BPARules.json`" -G -T `"artifacts\bpa.trx`""
          exit $p.ExitCode

      - name: Publicar artefatos
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: qa-report
          path: artifacts/
```

Copie `check_visual_bindings.py` e `tmdl_parser.py` para `ci/` no repositório do
projeto. A camada 2 entra num segundo job, depois do deploy para staging.

## Checklist antes de publicar

- [ ] Camada 3: nenhum `visual.json` com campo inexistente
- [ ] Camada 1: `TabularEditor.exe` retornou exit code 0 (nenhuma regra severidade ≥ 3 violada)
- [ ] Camada 2: todas as medidas avaliaram sem erro em staging
- [ ] Nomenclatura conforme `bi-nomenclatura` (pode virar regra customizada no BPA)
- [ ] `.gitignore` cobre `.pbi/localSettings.json`
- [ ] Resultado do QA anexado ao Pull Request

## Ferramentas

| Ferramenta | Tipo | Papel |
|---|---|---|
| Tabular Editor 2 | Open source, gratuita | BPA por CLI (camada 1) |
| Módulo `SqlServer` (`Invoke-ASCmd`) | Oficial Microsoft, não exclusivo do Power BI | DAX via XMLA (camada 2) |
| `check_visual_bindings.py` | Script desta skill | Binding (camada 3) |
| pbi-tools | Comunitária | Extrair PBIX para pasta quando o projeto ainda não é PBIP |
