---
name: bi-qa-documentacao
description: Documentar e validar um modelo Power BI antes de publicar — descrição de medida com /// na DAX Query View, QA em três camadas (Best Practice Analyzer pelo Tabular Editor CLI, smoke test de medidas via XMLA, binding visual.json × TMDL), pipeline de CI/CD e geração de documentação .docx a partir do TMDL/PBIR. Use para documentar medida no código, checklist de publicação automatizado, validar PBIP, CI/CD Power BI, testar medidas por script, visual quebrado, dicionário de dados, handoff ou "gerar Word do modelo". Regras de boas práticas em si ficam em powerbi-boas-praticas; sintaxe dos arquivos em tmdl-pbir.
---

# QA e documentação de modelos Power BI

Três frentes, na ordem em que aparecem no ciclo:

| Frente | Quando | Onde |
|---|---|---|
| Descrever a medida com `///` | Ao escrever a medida | Abaixo |
| QA em três camadas | Antes de cada merge ou publicação | `references/qa-pipeline.md` |
| Gerar documentação `.docx` | A cada publicação | `references/documentacao.md` |

## 1. Descrição de medida com `///` na DAX Query View

A descrição vai no próprio código, sem abrir o Model Explorer.

```dax
DEFINE
    /// Soma o valor líquido das vendas.
    /// Exclui pedidos cancelados e devoluções.
    /// Retorna BLANK() quando não há vendas no período filtrado.
    /// Usada nos KPIs comerciais e financeiros.
    MEASURE Vendas[Total de Vendas Líquidas] =
        SUM ( Vendas[Valor Líquido] )

EVALUATE
    ROW ( "Total de Vendas Líquidas", [Total de Vendas Líquidas] )
```

Depois, execute **Atualizar modelo com alterações** (CodeLens acima do
`MEASURE`). A descrição vai para a propriedade Description e aparece no Model
Explorer, no painel Dados, no tooltip do campo e no TMDL.

**Regras**
- `///` imediatamente acima do `MEASURE`; várias linhas viram uma descrição.
- Descreva o quê, a regra de negócio, as exceções, quando retorna `BLANK()` e
  onde é usada. Pense no próximo dev e no Copilot.
- Não repita a fórmula na descrição. Nada de "Calcula vendas" ou "Medida de teste".
- Fórmula mudou → descrição muda junto.
- A tabela no `MEASURE` é a tabela semântica visível (`Vendas`), e as colunas
  usam o nome semântico (`[Valor Líquido]`), nunca o físico (skill `bi-nomenclatura`).

[DAX Query View](https://learn.microsoft.com/pt-br/power-bi/transform-model/dax-query-view)

## 2. QA em três camadas

> Se eu publicar agora, o que quebra — e eu fico sabendo antes do usuário?

| Camada | Valida | Ferramenta |
|---|---|---|
| 3. Binding | Todo campo de `visual.json` existe no TMDL | `scripts/check_visual_bindings.py` |
| 1. BPA | Modelo segue as regras | Tabular Editor 2 CLI (`TabularEditor.exe`) |
| 2. Smoke test | Cada medida calcula sem erro | `Invoke-ASCmd` via XMLA, pós-deploy em staging |

Rode a camada 3 primeiro: é a mais barata e pega o erro mais comum (campo renomeado).

**Obrigatório**
- As três camadas antes de publicar.
- Rodar contra a pasta TMDL/PBIR versionada no Git, nunca contra "o que deveria estar".
- Versionar o arquivo de regras do BPA no repositório.
- Falhar o pipeline em regra de severidade Alta.

**Como o Tabular Editor 2 falha o pipeline:** não existe opção
`--error-on-violation`. O CLI retorna **exit code 1** quando há saída de nível
Error, e o BPA emite Error para regra com **severidade ≥ 3**. Portanto, deixe as
regras Altas com severidade 3 no arquivo de regras. Severidade 2 vira Warning e
1 vira informação.

```powershell
# Camada 1 — BPA sobre a pasta TMDL; -G anota no GitHub Actions (-V no Azure DevOps)
$p = Start-Process -FilePath ".\te2\TabularEditor.exe" -Wait -NoNewWindow -PassThru `
       -ArgumentList "`"VendasAurora.SemanticModel\definition`" -A `"ci\BPARules.json`" -G"
exit $p.ExitCode
```

⚠️ `TabularEditor.exe` é aplicativo WinForms: sem `-Wait` (ou `start /wait` no
cmd), o prompt volta antes de terminar e o exit code se perde. `-B` não é
"modo build": ele **salva** o modelo como `Model.bim`. Confirme a leitura de
pasta TMDL na versão que o time usa.

Comandos completos das três camadas, workflow do GitHub Actions e
proveniência das ferramentas: `references/qa-pipeline.md`.

## 3. Documentação automática

> Alguém que nunca abriu este relatório entende o modelo só lendo o documento?

Gere a partir do repositório, a cada publicação. Nunca digite à mão.

```bash
python scripts/extrair_modelo.py VendasAurora.SemanticModel/definition VendasAurora.Report/definition > modelo.json
node scripts/gerar_docx.js modelo.json documentacao-modelo.docx "Vendas Aurora" 2B579A
```

O documento sai com capa, sumário, tabelas (papel pelo prefixo), colunas,
relacionamentos (inativos marcados), medidas com DAX completo, formato, pasta e
descrição, e páginas com os campos de cada visual. Medida sem formato ou sem
`///` aparece marcada com ❗. Commit de origem no rodapé.

Estrutura, o que extrair de cada arquivo, cuidados (RLS com valores sensíveis,
explicação de DAX complexo) e checklist: `references/documentacao.md`.

## Scripts

| Script | Faz | Requer |
|---|---|---|
| `scripts/tmdl_parser.py` | Lê tabelas, colunas, medidas multilinha e relacionamentos do TMDL | Python 3.9+ |
| `scripts/check_visual_bindings.py` | Camada 3; exit 1 se houver campo quebrado | Python 3.9+ |
| `scripts/extrair_modelo.py` | JSON intermediário para a documentação | Python 3.9+ |
| `scripts/gerar_docx.js` | `.docx` a partir do JSON | Node + `npm install docx` |

O leitor TMDL é mínimo: cobre QA e documentação, não substitui o `TmdlSerializer`.
