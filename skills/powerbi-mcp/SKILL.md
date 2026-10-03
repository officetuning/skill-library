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
roda no macOS). Só com permissão *Build* no modelo, o agente consulta com DAX
mas não altera. ⚠️ Não registre os dois ao mesmo
tempo: o agente vê ferramentas duplicadas e gasta tokens à toa.

Para **responder perguntas de negócio** a partir do modelo, o servidor certo é
o Fabric IQ, não o de authoring.

## Antes de alterar qualquer coisa

1. **Backup.** Salve uma cópia do `.pbix` ou trabalhe num `.pbip` versionado.
2. **PBIP + Git.** Commit limpo antes da sessão: tudo que o agente mudar vira
   diff revisável e reversível (ver `tmdl-pbir`, seção Git).
3. **Dados sensíveis.** Metadados e resultados de consulta vão para o provedor
   de IA. Sem autorização, não use em modelo com dado pessoal ou sigiloso;
   prefira o modo somente leitura (`--readonly`) para explorar.

## Fluxo de trabalho do agente

1. **Conectar e inventariar (só leitura).** Liste tabelas, colunas, medidas,
   relacionamentos e UDFs. Não altere nada nesta etapa.
2. **Diagnosticar com as skills da casa.** Nomes contra `bi-nomenclatura`;
   modelo contra as 76 regras de `powerbi-boas-praticas` (cite número e
   severidade); UDFs contra `dax-udf`.
3. **Propor um plano** em tabela: objeto, ação, antes → depois, motivo.
   Agrupe por risco. **Espere o "pode aplicar" do usuário.**
4. **Aplicar em transação** (servidor local): abra, aplique o lote, valide,
   confirme. Erro no meio → desfaça a transação inteira.
5. **Validar com DAX.** Rode `EVALUATE` das medidas alteradas antes e depois
   e compare os números. Mudança de nome não pode mudar valor.
6. **Documentar.** Descrição `///` em toda medida e UDF nova (ver
   `bi-qa-documentacao`).
7. **Fechar.** Mostre o diff do Git e sugira a mensagem de commit. Quem faz o
   commit é o usuário.

## Regras que o agente não quebra

- Nunca apagar tabela, coluna ou medida sem confirmação explícita, item a item.
- Renomear em lote: listar **todas** as dependências (medidas, RLS, visuais em
  PBIR) antes; renome que quebra visual não entra no lote.
- Não mexer em RLS/OLS, partições ou fonte de dados sem pedido explícito.
- Uma mudança por objetivo: não "aproveitar" para corrigir outras coisas fora
  do plano aprovado.

## Convivência com as skills oficiais da Microsoft

A Microsoft publica skills de Power BI no repositório
[`microsoft/skills-for-fabric`](https://github.com/microsoft/skills-for-fabric)
(MIT). O plugin `powerbi-authoring` traz as skills de modelo semântico
(`semantic-model-authoring`) e de relatório (PBIR) e registra o MCP local.

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
| Nome de tabela, coluna, medida e UDF; AV/AA/Δ | `bi-nomenclatura`, `dax-udf` |
| Regras de modelagem e severidade | `powerbi-boas-praticas` |
| Visual, layout, storytelling | `powerbi-visuais`, `dashboard-layout`, `data-storytelling` |

Quando as duas orientações conflitarem num ponto de padrão (ex.: nome em
inglês × português), siga a OfficeTuning e avise o usuário do conflito.

## Pedidos que funcionam bem

| Objetivo | Pedido |
|---|---|
| Auditoria | "Conecte ao modelo aberto, só leitura, e audite contra as 76 regras. Entregue por severidade." |
| Padronizar nomes | "Proponha os novos nomes segundo bi-nomenclatura, com dependências. Não aplique ainda." |
| Documentar | "Escreva descrição /// para todas as medidas sem descrição, em português de negócio." |
| Refatorar em UDF | "Ache lógica repetida em 3+ medidas e proponha uma UDF no padrão dax-udf, com teste EVALUATE." |

## Fontes

- [Power BI Authoring MCP server](https://learn.microsoft.com/power-bi/developer/mcp/power-bi-authoring-mcp)
- [Power BI MCP servers overview](https://learn.microsoft.com/power-bi/developer/mcp/mcp-servers-overview)
- [Power BI Agentic overview](https://learn.microsoft.com/power-bi/developer/agentic/power-bi-agentic-overview)
- [microsoft/skills-for-fabric](https://github.com/microsoft/skills-for-fabric)
- Guia passo a passo em português: functionlibrary.officetuning.com.br/dax/mcp
