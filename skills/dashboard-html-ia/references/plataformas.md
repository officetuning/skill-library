# Dashboard com IA: o que cada plataforma oferece

> Conferido em 26/10/2026. Recursos de IA mudam rápido; plano, menu e status de
> preview valem para essa data. Os nomes de menu podem aparecer em inglês,
> conforme o idioma da conta. Confira o link oficial de cada seção antes de
> ensinar em aula.

## Resumo

| | Microsoft 365 Copilot | Google Gemini | Claude | ChatGPT |
|---|---|---|---|---|
| Análise com código | Analyst (Python) | Canvas / Colab | Execução de código | Análise de dados (Python) |
| Painel ao vivo na plataforma | Copilot Code (Frontier) | Sheets canvas | Claude Dashboards (beta) | Sites + tarefa agendada |
| HTML para levar para fora | Arquivo gerado pelo Analyst ou pelo Code | Código do Canvas | Artefato / arquivo `.html` | Arquivo gerado na análise |
| Lê Excel no OneDrive / SharePoint | ✔ nativo | ✖ (converta para Google Sheets) | ✔ conector Microsoft 365 | ✔ app SharePoint / OneDrive |
| Lê Google Sheets | ✖ | ✔ nativo | ✔ conector Google Drive | ✔ app Google Drive |

---

## Microsoft 365 Copilot

### Analyst

Agente de análise de dados do Microsoft 365 Copilot. Raciocina em etapas,
escreve e executa Python, mostra o código e entrega relatório com gráficos e
tabelas.

- **Acesso:** Microsoft Copilot → **Agents → Analyst**, com conta de trabalho e
  licença Microsoft 365 Copilot. Se não aparecer, o admin pode não ter
  habilitado. Na atualização de 12/10/2026 (Frontier), Researcher e Analyst
  deixam de ficar fixados por padrão na navegação e seguem disponíveis para
  fixar.
- **Dados:** **+ → Attach content**: arquivo do computador ou do OneDrive.
  Formatos citados: Excel e CSV.
- **Saída:** relatório com gráficos e tabelas; o código Python fica visível para
  conferência. A capacidade de *code interpreter* dos agentes Copilot gera
  arquivos para download, disponíveis **só durante a sessão**.
- **HTML:** a Microsoft não documenta um formato "dashboard HTML" no Analyst.
  Peça "gere um arquivo .html único para download" e, se ele não entregar o
  arquivo, peça o código e salve como `.html`. Teste no seu tenant.

**Use para:** perfilar o arquivo, calcular o total de controle, validar as
fórmulas dos KPIs. É o "analista que confere" antes de alguém montar o visual.

### Copilot Code (Frontier)

Aba **Code** no app Microsoft Copilot, ao lado de Chat e Cowork. Transforma
uma descrição em software funcionando: dashboards, ferramentas internas, sites
estáticos, transformações de dados.

- **Status:** preview do programa **Frontier**; cobrança por uso (licença
  Microsoft 365 Copilot + política de gastos definida pelo admin).
- **Dados:** upload de CSV, planilhas e documentos; texto colado; pasta local;
  e, com sua permissão, o contexto do Microsoft 365 (documentos, e-mails,
  reuniões).
- **Canvas:** prévia ao vivo, visão do código, clique num elemento para pedir
  ajuste, voltar a versões anteriores.
- **Local ou nuvem:** local trabalha numa pasta do seu computador; nuvem permite
  compartilhar o projeto com colegas.
- **Publicar:** apps interativos vão para o **Copilot Managed Runtime**
  (preview) e são compartilhados por link dentro da organização. Compartilhar
  o app **não compartilha o dado**: cada pessoa vê só o que já pode ver na fonte
  conectada. App estático pode virar link restrito à organização (nuvem).
- **Controle:** pede permissão antes de acessar a rede, rodar comando ou sair
  da pasta do projeto. Evite "Always allow".

**Use para:** painel que vai ficar no ar para a equipe, com dado do Microsoft 365
e governança do tenant.

### Copilot no Excel

Para quem quer ficar dentro da planilha: o Copilot no Excel roda Python ao
editar (agosto/2026) e o **canvas interativo** do Excel está no programa
Insiders (outubro/2026). Não gera HTML; útil para preparar a tabela antes.

### Fluxo recomendado

1. Arquivo no OneDrive for Business, numa **Tabela do Excel** (Ctrl+Alt+T) com
   cabeçalho de uma linha.
2. **Analyst:** perfil + total de controle + KPIs em Python.
3. **Copilot Code** (se tiver Frontier): "construa o dashboard com estes números
   seguindo o contrato colado abaixo" → publicar na organização.
4. Sem Frontier: Analyst gera o HTML para download, ou leve os números para o
   Claude/ChatGPT gerar o HTML pelo template.

Fontes:
[Use Analyst](https://support.microsoft.com/en-US/Microsoft-365-Copilot/use-analyst-for-deep-data-analysis) ·
[Get started with Analyst](https://support.microsoft.com/Microsoft-365-Copilot/get-started-with-analyst-in-microsoft-365-copilot) ·
[Code interpreter em agentes](https://learn.microsoft.com/microsoft-365/copilot/extensibility/code-interpreter) ·
[Copilot Code overview](https://learn.microsoft.com/copilot/code/overview) ·
[Use Copilot Code](https://learn.microsoft.com/copilot/code/use-code) ·
[Release notes do Microsoft 365 Copilot](https://learn.microsoft.com/microsoft-365/copilot/release-notes)

---

## Google Gemini

### Sheets canvas (dentro do Google Sheets)

Camada visual interativa, de **leitura e escrita**, criada pelo Gemini sobre os
dados de uma aba: kanban, galeria, calendário, dashboard.

- **Abrir:** Sheets no computador → **Inserir → Criar um canvas** (ou
  Ferramentas → Criar canvas) → descrever o painel.
- **Ao vivo:** mudança no canvas grava na planilha e mudança na planilha aparece
  no canvas. Quem só tem acesso de leitura não altera.
- **Compartilhar:** "Copiar link"; o acesso segue o da planilha.
- **Limites:** uma aba de origem; até 1 milhão de células nas abas de origem;
  só arquivos no Google Drive (Excel precisa ser salvo como Google Sheets); não
  funciona no app de celular nem offline; bloqueado se download/cópia estiver
  desativado.
- **Idioma:** **só contas com idioma em inglês** (out/2026). Em conta em
  português, troque o idioma da conta para testar ou use o Canvas do app.
- **Planos:** Workspace Business e Enterprise Standard/Plus, Google AI Pro e
  Ultra, complementos de educação. Rollout a partir de agosto/2026.

**Use para:** painel do dia a dia de uma equipe que já edita a planilha.

### Canvas no app Gemini (gemini.google.com)

Gera código de app com prévia: dashboards, rastreadores, funis.

- **Abrir:** abaixo da caixa de prompt → **Canvas**; anexe a planilha (upload ou
  Google Drive).
- **Editar:** pedir no chat, editar na visão **Code**, **Select & ask** num
  trecho, **Show console** para ver erros.
- **Compartilhar:** **Share & export → Share** gera link público
  `g.co/gemini/share`. Atenção: para apps, quem tem o link pode **ver e editar os
  dados associados ao app**. Há também **Export to Colab** para código Python.
- **Snapshot:** o app gerado não acompanha a planilha; mudou o dado, gere de
  novo.
- **Conta de trabalho:** o admin precisa liberar o app Gemini e anexos do Drive.

**Use para:** HTML portátil a partir de dado do Google, protótipo rápido.

### Outros

- **Gemini Spark** (agente 24/7): beta só nos EUA, plano AI Ultra (maio/2026).
  Fora do alcance da maioria dos usuários brasileiros nesta data.
- **Data Science Agent no Colab:** notebook Python gerado a partir do objetivo;
  bom para perfilar dados grandes antes do painel.

### Fluxo recomendado

1. Dados numa aba limpa: cabeçalho na linha 1, uma linha por registro, sem
   células mescladas.
2. Peça ao Gemini o perfil e o total de controle antes do painel.
3. Equipe interna → **Sheets canvas**. Painel para levar para fora →
   **Canvas** do app ou Claude/ChatGPT com o template.

Fontes:
[Create a Sheets canvas](https://support.google.com/docs/answer/17035851) ·
[Sheets canvas — Workspace Updates](https://workspaceupdates.googleblog.com/2026/08/use-google-sheets-canvas-to-visualize-data.html) ·
[Canvas no Gemini](https://support.google.com/gemini/answer/16047321) ·
[Visão geral do Canvas](https://gemini.google/overview/canvas/) ·
[Data Science Agent no Colab](https://developers.googleblog.com/en/data-science-agent-in-colab-with-gemini/)

---

## Claude

### Artefato HTML

O Claude escreve o HTML, publica como artefato com link próprio (privado até
você compartilhar) ou entrega o `.html` como arquivo.

- **Dados:** upload de CSV e Excel; **conector Google Drive** (lê Google Sheets,
  Office e PDF; disponível em todos os planos, admin habilita em Team e
  Enterprise); **conector Microsoft 365** (lê Excel e CSV no OneDrive e no
  SharePoint com as permissões do usuário; exige conta corporativa Entra e
  consentimento do admin do tenant; disponível em todos os planos).
- **Análise:** executa Python para perfilar e calcular antes de gerar o painel.
- **Skills:** instale esta skill (`dashboard-html-ia`) e as de storytelling e
  visuais: o Claude passa a seguir o contrato e o template sem você colar o
  prompt inteiro.

### Claude Dashboards (beta)

Lançado em 08/10/2026. Painel que consulta a fonte direto: o Claude escreve
**uma consulta SQL por gráfico**, executa na fonte e mostra a consulta e a data
da última atualização em cada gráfico.

- **Planos:** Pro, Max, Team e Enterprise (no Enterprise, um Owner ativa em
  *Organization settings → Artifacts*). Não está no Free.
- **Fontes:** warehouses (Amazon Redshift, BigQuery, ClickHouse, Databricks,
  Snowflake) e outros apps conectados (ex.: Salesforce). A ajuda oficial **não
  cita** CSV, Excel ou Google Sheets como fonte; para eles, use o artefato HTML.
- **Criar:** peça um dashboard no chat ou escolha **Output → Dashboards**.
- **Compartilhar:** começa privado. Cada visitante consulta com as próprias
  conexões e vê só o que já pode ver.
- **Limite declarado:** feito para perguntas rápidas e exploratórias; não há
  camada semântica, então cada número vale pelo SQL daquele gráfico.

### Fluxo recomendado

1. Anexe o arquivo ou cite o caminho no Drive/OneDrive.
2. "Perfile e me mostre o total de controle" → confira.
3. "Gere o dashboard seguindo a skill dashboard-html-ia" → artefato.
4. Dado em warehouse → Claude Dashboards e confira o SQL de cada gráfico.

Fontes:
[Get started with Claude Dashboards](https://support.claude.com/en/articles/17454700-get-started-with-claude-dashboards) ·
[Conector Microsoft 365](https://support.claude.com/en/articles/12542951-enabling-and-using-the-microsoft-365-connector) ·
[Conectores Google Workspace](https://support.claude.com/en/articles/10166901) ·
[Usar skills no Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

---

## ChatGPT

### Análise de dados

Python em ambiente isolado sobre arquivos enviados.

- **Formatos:** `.xls`, `.xlsx`, `.csv`, PDF, JSON, XML, texto.
- **Fontes conectadas:** com os apps habilitados, anexa arquivos do Google
  Drive, OneDrive e SharePoint usando suas permissões.
- **Gráficos interativos:** barras, linhas, pizza e dispersão; os demais saem
  como imagem.
- **Limite importante:** o Python **não acessa a internet**; o dado precisa ser
  enviado ou anexado antes.

### Sites

Cria, publica e compartilha sites interativos e apps leves, inclusive
dashboards.

- **Planos:** Plus, Pro, Business e Enterprise (não Free nem Go). No
  Enterprise, publicação pública depende do admin.
- **Privado por padrão.** Compartilhe com pessoas, grupos, o workspace ou, se
  liberado, a internet.
- **Dados:** banco do site até 10 GB; apps conectados usam a conta de cada
  visitante.
- **Uso:** construir e editar consome uso do Codex; hospedagem tem uso
  separado.
- **Dashboard que se atualiza:** a OpenAI descreve o fluxo planilha aprovada no
  Google Drive → Sites → **tarefa agendada** que confere a fonte em dias úteis e
  atualiza o painel. O site não roda o agendamento sozinho.

### Fluxo recomendado

1. Anexe o arquivo ou o link exato da planilha no Drive/OneDrive.
2. Análise de dados: perfil + total de controle.
3. Snapshot: peça o `.html` único pelo contrato. Recorrente: **Sites** + tarefa
   agendada, com alerta só quando algo relevante mudar.

Fontes:
[Creating and using ChatGPT Sites](https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites) ·
[Build a dashboard that stays up to date](https://learn.chatgpt.com/use-cases/analyze-data-export) ·
[Data analysis with ChatGPT](https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt)

---

## Leitura complementar

- [Skill build-dashboard da Anthropic](https://github.com/anthropics/knowledge-work-plugins):
  inspirou a estrutura de dados embutidos e os limites de volume.
- [Copilot Adoption Dashboard (Microsoft CAT)](https://microsoft.github.io/cat-agent-skills/skills/create-copilot-adoption-dashboard):
  bom exemplo de regra "nada estimado, painel pendente quando falta dado".
