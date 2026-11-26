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

## Camada 2 — Testes de medidas via XMLA

Pega o que a análise estática não pega: erro de DAX em execução, referência
circular. O Desktop não tem modo de linha de comando para "abrir e testar";
publique num workspace de **staging** e consulte pelo endpoint XMLA.

Pré-requisitos: workspace com XMLA habilitado (Premium, PPU ou Fabric),
`Install-Module -Name SqlServer`, modelo já publicado.

São dois testes. O **smoke test** cobre muitas medidas e só procura erro. O
**teste de valores esperados** cobre poucas e confere o resultado. Medida que
não dá erro ainda pode devolver número errado.

### Smoke test: a medida calcula sem erro

```powershell
$servidor = "powerbi://api.powerbi.com/v1.0/myorg/StagingWorkspace"
$banco    = "VendasAurora"
$medidas  = @("Faturado (AV)", "Ticket Médio", "Margem Bruta (%)", "Faturado (Δ%)")
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
Rode como job **depois** do deploy para staging. Este teste aprova uma medida que
devolve em branco ou um valor errado sem erro.

### Teste de valores esperados: a medida devolve o que deveria

⚠️ **Executado em 26/11/2026** contra um Power BI Desktop local, no PowerShell
7.7.0 com `SqlServer` 22.4.5.1: os 15 testes do arquivo de casos conferiram, e uma
cópia com a fórmula errada de propósito foi reprovada. Os controles do modelo
sintético (abaixo) também: 42 de 42 nas medidas e 17 de 17 nas UDFs, com
reprovação ao quebrar uma medida do modelo e uma UDF. **Ainda não testado:** o
Windows PowerShell 5.1 contra um servidor (o autoteste passa nele, mas sem
servidor), o endpoint XMLA do Service (`powerbi://`, com autenticação) e dados de
um modelo real. Antes de pôr no pipeline, rode uma vez em staging, incluindo um
caso com valor errado de propósito, que precisa reprovar.

```powershell
# Confere o próprio script, sem servidor
pwsh -File scripts/testar_medidas.autoteste.ps1

pwsh -File scripts/testar_medidas.ps1 `
    -Servidor "powerbi://api.powerbi.com/v1.0/myorg/StagingWorkspace" `
    -Banco "VendasAurora" `
    -Casos assets/casos-regra-comparativo.json
```

| Saída | Significado |
|---|---|
| 0 | Todas as verificações conferem |
| 1 | Valor diferente do esperado, erro de DAX ou resposta em formato não reconhecido |
| 2 | Arquivo de casos inválido ou `Invoke-ASCmd` ausente |

Regras da comparação:

- `"esperado": null` quer dizer **em branco**. Em branco, zero e texto vazio são
  três resultados diferentes. Sem a chave `esperado`, o arquivo é recusado.
- Número aceita diferença absoluta de até `0.000001`; mude com `"tolerancia"`.
  Percentual vai como fração (50% = `0.5`).
- Texto precisa ser idêntico, inclusive o símbolo do farol.
- `"definir"` (medidas) e `"funcoes"` (UDFs, `DEFINE FUNCTION`) existem só durante
  a consulta. Os dois podem ficar no topo do arquivo ou em um caso, que troca o
  item de mesmo nome. UDF exige compatibilidade 1702 ou maior.

**Casos de regra.** `assets/casos-regra-comparativo.json` traz os cinco casos de
`powerbi-visuais/references/comparativo-ano-anterior.md`. Ele testa **a regra**, não
as medidas do modelo: `definir` no topo do arquivo copia as fórmulas de `(Δ)`,
`(Δ%)` e `(Δi)`, e cada caso troca `(AV)` e `(AA)`, tudo só durante a consulta
([DEFINE MEASURE](https://learn.microsoft.com/dax/measure-statement-dax)); o
modelo não muda. O `definir` do caso sobrescreve o do topo.

- **A substituição não chega às medidas do modelo.** Medido no motor: com `(AV)`
  = -50 e `(AA)` = -100 definidos na consulta, `[Faturado (AV)]` devolve -50, mas
  o `[Faturado (Δ)]` do modelo continua usando os valores do modelo (devolveu 0,
  não 50). Por isso as fórmulas precisam estar no `definir`.
- A consulta precisa de uma tabela existente (aqui, `Vendas`) para hospedar as
  medidas definidas. Troque `Vendas` e `Faturado` pelos nomes do seu modelo.
- Se alguém alterar a fórmula do modelo, este teste não percebe. Para testar a
  medida do modelo, use os valores de controle abaixo.
- Os casos supõem "maior é melhor". Em "menor é melhor", o farol esperado se
  inverte.
- Não testam o cálculo do ano anterior, porque `(AA)` é substituída.

**Valores de controle.** Para testar `(AV)` e `(AA)`, use um caso sem `definir`,
com filtro fixo e um número conferido **fora do modelo** (consulta na origem ou
relatório já homologado). Escolha um período fechado, que não mude com a carga.

```json
{
  "casos": [
    {
      "nome": "Controle de um ano fechado",
      "verificar": [
        {
          "expressao": "CALCULATE ( [Faturado (AV)], 'Calendário'[Ano] = 2025 )",
          "esperado": 1234567.89,
          "tolerancia": 0.01
        }
      ]
    }
  ]
}
```

O número acima é fictício. Não copie para o esperado o resultado da própria
medida: o teste passaria mesmo com a fórmula errada.

O arquivo de casos vira consulta DAX: versione e revise como código.

**Modelo sintético.** Dois arquivos prontos, com esperados calculados em Python a
partir das linhas de origem por `scripts/gerar_casos_sinteticos.py`:

| Arquivo | Testa |
|---|---|
| `assets/casos-modelo-sintetico.json` | `(AV)`, `(AA)`, `(Δ)`, `(Δ%)` e `(Δi)` **gravadas no modelo**, inclusive 29/02 no modo clássico |
| `assets/casos-udf-ano-anterior.json` | `Tempo.AnoAnterior` e `Tempo.VariacaoAnoAnterior` com `CALENDARREF`, definidas só na consulta |

O modelo precisa ser montado à mão (ainda não há script que o crie):

- compatibilidade 1702 e a prévia de inteligência de tempo com calendário;
- `'Vendas'` com `Data` e `Valor da Venda` (decimal fixo), com as linhas de
  `LINHAS` no gerador;
- `'Calendário'` contínuo de 01/01/2023 a 31/12/2026, com `Data`, `Ano`,
  `Trimestre #`, `Mês #`, `Ano/Mês` e `Dia`, marcado como tabela de datas;
- relacionamento `'Vendas'[Data]` → `'Calendário'[Data]`;
- calendário `'Gregoriano'` com ano, trimestre do ano, mês, mês do ano, dia do mês
  e data;
- as medidas do código de referência de `comparativo-ano-anterior.md`, com `(AA)`
  no modo clássico;
- se criar os objetos por XMLA, recalcule o modelo (refresh `calculate`) antes de
  testar: sem isso o relacionamento dá erro e tudo reprova.

Em 29/02/2024 o ano anterior é 28/02/2023 no modo clássico e 01/03/2023 no modo
calendário. Os números sintéticos conferem fórmulas, não os dados do seu modelo.

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
- [ ] Camada 2: casos de regra e valores de controle conferem em staging
- [ ] Nomenclatura conforme `bi-nomenclatura` (pode virar regra customizada no BPA)
- [ ] `.gitignore` cobre `.pbi/localSettings.json`
- [ ] Resultado do QA anexado ao Pull Request

## Ferramentas

| Ferramenta | Tipo | Papel |
|---|---|---|
| Tabular Editor 2 | Open source, gratuita | BPA por CLI (camada 1) |
| Módulo `SqlServer` (`Invoke-ASCmd`) | Oficial Microsoft, não exclusivo do Power BI | DAX via XMLA (camada 2) |
| `testar_medidas.ps1` | Script desta skill | Valores esperados (camada 2) |
| `check_visual_bindings.py` | Script desta skill | Binding (camada 3) |
| pbi-tools | Comunitária | Extrair PBIX para pasta quando o projeto ainda não é PBIP |
