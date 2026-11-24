---
name: powerbi-mcp
description: Como um agente de IA deve alterar um modelo semântico Power BI pelo Power BI Authoring MCP server (antigo Power BI Modeling MCP) com segurança e no padrão OfficeTuning — local × hospedado, backup e PBIP + Git antes de mexer, inventário somente leitura, plano aprovado, transações, validação com DAX, e convivência com as skills oficiais da Microsoft (skills-for-fabric / powerbi-authoring). Use quando o usuário pedir para o agente criar ou alterar medidas, tabelas, relacionamentos, UDFs ou descrições via MCP, renomear em lote, aplicar boas práticas direto no modelo, ou instalar e combinar skills da Microsoft com as da OfficeTuning.
---

# Power BI via MCP, com segurança

O MCP dá ao agente as **ferramentas**; as skills dão o **método**. Sozinho, o
servidor obedece ao pedido literal. Com as skills OfficeTuning, o agente
nomeia, documenta e valida como a casa faz.

## Qual servidor

| | Local (GA) | Hospedado (preview) |
|---|---|---|
| Modelo aberto no Power BI Desktop | ✅ | ❌ |
| Arquivos PBIP/TMDL no disco | ✅ | ❌ |
| Modelo em workspace do Fabric | ✅ | ✅ |
| Transações e traces | ✅ | ❌ |
| Instalação | Extensão do VS Code, pacote npm `@microsoft/powerbi-modeling-mcp` ou executável | Nenhuma |

A Microsoft recomenda o **hospedado** quando o ambiente permite (nada a
instalar). Para quem desenvolve no Desktop ou em PBIP: **local** (Windows; não
roda no macOS). ⚠️ Não registre os dois ao mesmo tempo: o agente vê
ferramentas duplicadas e gasta tokens à toa.

| Pré-requisito | Detalhe |
|---|---|
| Permissão | *Write* para alterar; só com *Build*, o agente consulta com DAX mas não altera |
| Modo do servidor local | `--readwrite` (padrão) pede confirmação uma vez por modelo antes de gravar; `--readonly` impede qualquer escrita |
| Modelo em workspace pelo local | Endpoint XMLA em **Leitura e Gravação** na capacidade |
| Servidor hospedado | Configuração de tenant *Users can use the Power BI Model Context Protocol server endpoint* |
| Pipeline de CI | Servidor local com `--authmode serviceprincipal` (ver `bi-qa-documentacao`) |
| Rastro de auditoria | Hospedado: `ModifiedByPowerBIMCP`/`ReadByPowerBIMCP` no log de auditoria do Fabric. Local: log em disco com `--audit-log-path`; recomendado em projeto de cliente |

Para **responder perguntas de negócio** a partir do modelo, o servidor certo é
o Fabric IQ, não o de authoring.

## Antes de alterar qualquer coisa

1. **Backup.** Salve uma cópia do `.pbix` ou trabalhe num `.pbip` versionado.
2. **PBIP + Git.** Commit limpo antes da sessão: tudo que o agente mudar vira
   diff revisável e reversível (ver `tmdl-pbir`, seção Git).
3. **Dados sensíveis.** Metadados e resultados de consulta vão para o provedor
   de IA. Sem autorização, não use em modelo com dado pessoal ou sigiloso;
   prefira o modo somente leitura (`--readonly`) para explorar.

## Qual ferramenta edita o modelo

Segue a ordem da skill oficial `semantic-model-authoring`:

1. **MCP conectado** → ele é a fonte da verdade. O agente lê e grava pelo MCP e
   **não** abre nem escreve `.tmdl` à mão durante a sessão (o disco fica
   desatualizado). Conectado a uma pasta PBIP, grava o modelo de volta em
   `definition` no fim da sessão.
2. **Sem MCP, com PBIP** → edita o TMDL (ciclo seguro de `tmdl-pbir`).
3. **`.pbix` sem MCP** → **para** e pede para salvar como PBIP.

O MCP não altera páginas do relatório nem o diagrama: depois de renomear no
modelo, os vínculos dos visuais (`visual.json`) se corrigem à parte, e a
checagem de bindings da `bi-qa-documentacao` confirma.

## Fluxo de trabalho do agente

1. **Conectar e inventariar (só leitura).** Liste tabelas, colunas, medidas,
   relacionamentos e UDFs. Não altere nada nesta etapa.
2. **Diagnosticar com as skills da casa.** Nomes contra `bi-nomenclatura`
   (tabela com nome de negócio e papel no grupo de consultas; renomear vale
   para tabela com prefixo técnico no modelo e para coluna ou medida sem nome
   amigável);
   modelo contra as regras de modelo (seções 1 a 6) de `powerbi-boas-praticas`
   (cite número e severidade); UDFs contra `dax-udf`.
3. **Propor um plano** em tabela: objeto, ação, antes → depois, motivo.
   Agrupe por risco. **Espere o "pode aplicar" do usuário.**
4. **Aplicar em transação** (servidor local), na ordem partição → colunas →
   relacionamentos → medidas, conferindo antes que as colunas usadas existem.
   Erro no meio → desfaça a transação inteira.
5. **Validar com DAX.** `EVALUATE { [Medida] }` em cada medida nova;
   `EVALUATE INFO.MEASURES()` sem `ErrorMessage`; totais agregados das medidas
   alteradas antes e depois (a consulta devolve no máximo **100 mil linhas**:
   compare totais, não a tabela inteira). Tabela nova → atualizar e conferir
   linhas. Mudança de nome não pode mudar valor.
6. **Documentar.** Descrição `///` em toda medida e UDF nova (ver
   `bi-qa-documentacao`).
7. **Fechar.** Mostre o diff do Git e sugira a mensagem de commit. Quem faz o
   commit é o usuário.

## Regras que o agente não quebra

- Nunca apagar tabela, coluna ou medida sem confirmação explícita, item a item.
- Renomear em lote: listar **todas** as dependências (medidas, RLS, visuais em
  PBIR) antes; renome que quebra visual não entra no lote.
- Não mexer em RLS/OLS, partições ou fonte de dados sem pedido explícito.
  Quem pertence a uma função de RLS se administra no portal, nunca pelo agente.
- Instruções de IA, esquema de dados para IA e respostas verificadas
  ("Prep data for AI") são configurados pelo usuário na interface; o agente só
  sugere.
- Uma mudança por objetivo: não "aproveitar" para corrigir outras coisas fora
  do plano aprovado.

## Convivência com as skills oficiais da Microsoft

A Microsoft publica skills de Power BI no repositório
[`microsoft/skills-for-fabric`](https://github.com/microsoft/skills-for-fabric)
(MIT). O plugin `powerbi-authoring` traz as skills de modelo semântico
(`semantic-model-authoring`) e de relatório (`powerbi-report-cli`: planejar,
desenhar, criar e validar PBIR, com captura de tela) e registra o MCP local.
A validação do relatório usa o **Power BI Desktop Bridge** (preview), servidor
local dentro do Desktop aberto que recarrega o projeto e captura cada página
sem fechar o Desktop (ver `tmdl-pbir`, "Editar por script").

```
/plugin marketplace add microsoft/skills-for-fabric
/plugin install powerbi-authoring@fabric-collection
```

O repositório é otimizado para o GitHub Copilot CLI e traz compatibilidade
para Claude Code, VS Code, Cursor e outros. Confira o comando na página do
repositório antes de instalar.

| Assunto | Quem manda |
|---|---|
| Sintaxe, comportamento da ferramenta, APIs, sequência técnica da operação | Skills Microsoft e Microsoft Learn |
| Nome de tabela, coluna, medida e UDF; (AV)/(AA)/(Δ) | `bi-nomenclatura`, `dax-udf` (alinhadas ao padrão oficial; a casa acrescenta português, medida sem "Total" e o comparativo entre parênteses) |
| Regras de modelagem e severidade | `powerbi-boas-praticas` |
| Visual, layout, storytelling | `powerbi-visuais`, `dashboard-layout`, `data-storytelling` |

Quando as duas orientações conflitarem num ponto de padrão (ex.: nome em
inglês × português), siga a OfficeTuning e avise o usuário do conflito.
Em modelo existente, a skill oficial manda manter o padrão já usado, a menos
que o usuário peça para padronizar: ao padronizar, use `bi-nomenclatura` e
siga a checagem 16 da `bi-qa-documentacao` para achar visuais quebrados.

## Pedidos que funcionam bem

| Objetivo | Pedido |
|---|---|
| Auditoria | "Conecte ao modelo aberto, só leitura, e audite contra as regras de modelo de powerbi-boas-praticas. Entregue por severidade." |
| Padronizar nomes | "Proponha os novos nomes segundo bi-nomenclatura, com dependências. Não aplique ainda." |
| Documentar | "Escreva descrição /// para todas as medidas sem descrição, em português de negócio." |
| Refatorar em UDF | "Ache lógica repetida em 3+ medidas e proponha uma UDF no padrão dax-udf, com teste EVALUATE." |

## Fontes

- [Power BI Authoring MCP server](https://learn.microsoft.com/power-bi/developer/mcp/power-bi-authoring-mcp)
- [Power BI MCP servers overview](https://learn.microsoft.com/power-bi/developer/mcp/mcp-servers-overview)
- [Power BI Agentic overview](https://learn.microsoft.com/power-bi/developer/agentic/power-bi-agentic-overview)
- [microsoft/skills-for-fabric](https://github.com/microsoft/skills-for-fabric)
- [Power BI Desktop Bridge](https://learn.microsoft.com/power-bi/developer/agentic/power-bi-desktop-bridge-overview)
- [Power BI Report skill](https://learn.microsoft.com/power-bi/developer/agentic/power-bi-report-skill-overview)
- [powerbi-modeling-mcp (opções de linha de comando)](https://github.com/microsoft/powerbi-modeling-mcp)
- Guia passo a passo em português: [officetuning.ai/biblioteca/guias/dax-mcp-setup](https://officetuning.ai/biblioteca/guias/dax-mcp-setup)
