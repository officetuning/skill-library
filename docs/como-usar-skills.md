# Como usar as skills do Data Analyst Advisor no Claude, ChatGPT, Gemini e Copilot

> Atualizado em 23/09/2026. Recursos de IA mudam rápido: plano, menu e status de
> preview citados aqui valem para essa data. Na dúvida, confira o link oficial
> no fim de cada seção. Os nomes de menu podem aparecer em inglês, conforme o
> idioma da sua conta.

As skills do **Data Analyst Advisor** ensinam a IA a trabalhar do jeito
OfficeTuning: nomenclatura `TabDim`/`TabFat`, comparativo AV/AA/Δ, Query
Folding, as 76 regras de modelagem, grid de 8 px e QA de PBIP. Elas ficam no
repositório público [officetuning/skill-library](https://github.com/officetuning/skill-library).

## O que é uma skill

Uma skill é uma **pasta** com um arquivo `SKILL.md` e, opcionalmente,
referências e scripts:

```
power-query-m/
├── SKILL.md              ← nome, descrição e instruções
└── references/
    ├── funcoes-m.md
    └── padroes-m.md
```

O `SKILL.md` começa com um cabeçalho:

```markdown
---
name: power-query-m
description: Boas práticas de Power Query M no Power BI — Query Folding, ...
  Use quando o usuário citar refresh lento, "query folding", função M ...
---
```

A IA lê só o `name` e a `description` de todas as skills instaladas. Quando sua
pergunta combina com uma descrição, ela abre aquela skill e segue as instruções.
Por isso você não precisa dizer "use a skill X": basta perguntar.

O formato é um **padrão aberto** ([Agent Skills](https://agentskills.io)). A
mesma pasta funciona no Claude, no ChatGPT, no Gemini e no GitHub Copilot, sem
conversão.

## As 9 skills

| Skill | Dispara quando você pergunta sobre |
|---|---|
| `powerbi-visuais` | Qual visual usar, formatação condicional, tooltip, SVG por DAX |
| `powerbi-boas-praticas` | Modelo lento, revisão de DAX, as 76 regras e a severidade de cada uma |
| `power-query-m` | Query Folding, refresh lento no ETL, função M, Incremental Refresh |
| `bi-nomenclatura` | Nome de tabela, coluna e medida; AV/AA/Δ/Δ%/Δi |
| `data-storytelling` | Mensagem principal, Big Idea, poluição visual |
| `dashboard-canvas` | Briefing, os 12 blocos, 5W2H |
| `dashboard-layout` | Wireframe, grid 8 px, Background Builder |
| `tmdl-pbir` | Script TMDL, `.pbip`, `visual.json` |
| `bi-qa-documentacao` | Descrição com `///`, BPA por linha de comando, documentação `.docx` |

## Primeiro passo (vale para todas as IAs)

Baixe o repositório: em [github.com/officetuning/skill-library](https://github.com/officetuning/skill-library)
clique em **Code → Download ZIP** e descompacte. As skills estão em `skills/`.

Algumas plataformas pedem **um `.zip` por skill**. No Windows, este PowerShell
gera todos de uma vez, na pasta `zips`:

```powershell
# Rode dentro da pasta skill-library descompactada
New-Item -ItemType Directory -Force zips | Out-Null
Get-ChildItem skills -Directory | ForEach-Object {
    # O .zip contém a pasta da skill (ex.: power-query-m\SKILL.md)
    Compress-Archive -Path $_.FullName -DestinationPath "zips\$($_.Name).zip" -Force
}
```

⚠️ Não renomeie a pasta: o nome dela tem que ser igual ao `name` do `SKILL.md`.

---

## Claude

### Claude no navegador, desktop e celular

**Plano:** Free, Pro, Max, Team e Enterprise. Exige **Execução de código e
criação de arquivos** ligada.

1. Ligue a execução de código:
   - Free, Pro e Max: **Configurações → Capacidades**.
   - Team e Enterprise: o admin libera em **Configurações da organização →
     Plugins e skills**.
2. Vá em **Personalizar → Skills**.
3. Clique em **+ → Criar skill → Enviar uma skill** e escolha o `.zip` (ex.:
   `power-query-m.zip`). Repita para cada skill.
4. Confira se a chave da skill está ligada.

**Teste:** "Meu refresh ficou lento depois que adicionei uma coluna
personalizada. Como descubro o passo que quebrou o Query Folding?"

No Team e no Enterprise, a skill enviada fica visível só para você até ser compartilhada.

### Claude Code

Instala as 9 de uma vez, como plugin:

```text
/plugin marketplace add officetuning/skill-library
/plugin install data-analyst-advisor@officetuning
```

Para usar só algumas, copie as pastas para `~/.claude/skills/` (todas as
conversas) ou `.claude/skills/` dentro do projeto.

📎 [Usar skills no Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

---

## ChatGPT

### Com skills (Business, Enterprise, Edu e Healthcare)

Skills estão em **beta** e **desligadas por padrão**. O dono do workspace
precisa ativá-las nas configurações do workspace.

1. Na barra lateral, abra **Plugins → Skills**.
2. Clique em **Criar → Enviar do computador** e escolha a skill.
3. Instale. O ChatGPT passa a usar a skill sozinho quando ela ajuda.
4. Para forçar, mencione a skill com **@** na conversa.

Skill compartilhada por um colega: **Skills → Compartilhadas comigo → ••• → Instalar**.

📎 [Skills no ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)

### Sem skills (Free e Plus): GPT personalizado

Nos planos individuais não há skills. A alternativa é um **GPT personalizado**,
que usa as skills como base de conhecimento:

1. **Explorar GPTs → Criar → Configurar**.
2. Em **Instruções**, cole o texto abaixo do cabeçalho `---` de uma ou duas
   skills que você mais usa. O campo tem limite de tamanho.
3. Em **Conhecimento**, envie os `SKILL.md` das outras skills e os arquivos de `references/`.

⚠️ No GPT personalizado não há disparo automático por descrição. O GPT consulta
os arquivos por busca, então cite o tema na pergunta ("pela regra de
nomenclatura, como nomeio...").

💡 Não quer montar? Use o [Data Analyst Advisor (GPT)](https://functionlibrary.officetuning.com.br/) já publicado.

### Codex

O agente de código da OpenAI também lê skills no mesmo formato. Catálogo e
instruções: [openai/skills](https://github.com/openai/skills).

---

## Gemini

### App Gemini (gemini.google.com)

**Plano:** Google AI Pro ou Ultra, com **conta pessoal** Google (não funciona com
conta de trabalho ou escola), maior de 18 anos e **Atividade** ligada.
Disponível no Brasil; indisponível no Espaço Econômico Europeu, Reino Unido,
Suíça e Nigéria.

1. Abra [gemini.google.com](https://gemini.google.com) → barra lateral →
   **Switch to Spark → Skills**.
2. Escolha **Enviar arquivo** e selecione o `SKILL.md` ou o `.zip` da skill
   (até 100 MB). O `.zip` precisa ter o `SKILL.md` na raiz.
3. Ligue a skill.
4. O Gemini usa a skill sozinho pelo contexto. Para escolher manualmente,
   digite **/** na conversa.

⚠️ O app Gemini **não aceita** PDF, DOCX, XLSX nem imagens dentro da skill. As
skills do Data Analyst Advisor são só texto (`.md`, `.py`, `.js`) e funcionam.

📎 [Criar e gerenciar skills no Gemini](https://support.google.com/gemini/answer/17094296)

### Sem skills (conta de trabalho ou plano sem skills): Gem

1. **Gems → Novo Gem**.
2. Em **Instruções**, cole o corpo do `SKILL.md` principal.
3. Em **Conhecimento**, envie os demais `SKILL.md` e `references/`.

### Gemini CLI (terminal)

```bash
# Instala a partir da pasta local, para todos os projetos
gemini skills install ./skill-library/skills/power-query-m --consent

# Dentro do Gemini CLI
/skills list
```

Ou copie as pastas para `~/.gemini/skills/` (usuário) ou `.gemini/skills/`
(projeto). O Gemini pede sua confirmação antes de ativar cada skill.

📎 [Agent Skills no Gemini CLI](https://geminicli.com/docs/cli/skills/)

---

## Copilot

"Copilot" é o nome de vários produtos. Skills funcionam no **GitHub Copilot** e
no **Copilot Studio**.

### GitHub Copilot (VS Code, Visual Studio, CLI e cloud agent)

Copie as pastas das skills para uma destas pastas:

| Escopo | Pasta |
|---|---|
| Só este projeto | `.github/skills/` ou `.agents/skills/` |
| Todos os projetos | `~/.copilot/skills/` ou `~/.agents/skills/` |

No chat do VS Code, no modo agente, digite **/** para ver as skills e chamar uma
pelo nome:

```text
/power-query-m revise esta consulta e diga onde o folding quebra
```

Pelo GitHub CLI (versão 2.90.0 ou superior, recurso em preview):

```bash
gh skill install officetuning/skill-library power-query-m
```

💡 Quem usa Power BI Projects (`.pbip`) versionado no Git ganha mais: com
`tmdl-pbir` e `bi-qa-documentacao` em `.github/skills/`, o Copilot lê o TMDL do
próprio repositório.

📎 [Agent Skills no VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills) ·
[Skills no GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)

### Copilot Studio

Agentes do Copilot Studio movidos pelo harness do GitHub Copilot aceitam upload
de `SKILL.md` ou `.zip` na configuração do agente. O uso consome Copilot Credits.

📎 [Skills para agentes no Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-overview)

### Microsoft 365 Copilot (chat do Office)

Na data deste guia, a Microsoft não documenta upload de skills no chat do
Microsoft 365 Copilot. A alternativa é criar um **agente** e anexar os
`SKILL.md` como conhecimento, como no GPT personalizado e no Gem.

---

## Uma pasta para várias IAs

Várias ferramentas leem a pasta `.agents/skills/`. Instalando nela, a mesma
cópia serve a mais de uma:

| Ferramenta | Usuário | Projeto |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| GitHub Copilot | `~/.copilot/skills/` · `~/.agents/skills/` | `.github/skills/` · `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` · `~/.agents/skills/` | `.gemini/skills/` · `.agents/skills/` |

O Copilot também lê `.claude/skills/` no projeto.

## Resumo

| IA | Skills nativas | Plano | Como instalar | Plano B |
|---|---|---|---|---|
| Claude | ✔️ | Free em diante | Upload do `.zip` ou plugin no Claude Code | — |
| ChatGPT | ✔️ (beta) | Business, Enterprise, Edu | Plugins → Skills → Enviar | GPT personalizado |
| Gemini | ✔️ | AI Pro ou Ultra, conta pessoal | Spark → Skills → Enviar arquivo | Gem |
| GitHub Copilot | ✔️ | Qualquer plano do Copilot | Copiar para `.github/skills/` ou `gh skill install` | — |
| Microsoft 365 Copilot | Não documentado | — | — | Agente com conhecimento |

## Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| Upload recusado: nome não confere | Pasta renomeada | O nome da pasta deve ser igual ao `name` do `SKILL.md` |
| Upload recusado: falta `SKILL.md` | O `.zip` foi feito com os arquivos soltos ou com pasta a mais | Compacte a pasta da skill (Claude) ou deixe o `SKILL.md` na raiz (Gemini) |
| A skill nunca é usada | Skill desligada ou pergunta vaga | Confira a chave; use termos da tabela "As 9 skills" |
| Menu Skills não aparece | Plano sem o recurso ou recurso desligado pelo admin | Veja o plano de cada IA acima |
| Resposta diferente do padrão OfficeTuning | Skill antiga | Baixe a versão mais recente do repositório e reenvie |

## Manter atualizado

As skills evoluem junto com o Function Library. Para atualizar:

- **Upload manual** (Claude, ChatGPT, Gemini): baixe o repositório de novo e
  reenvie o `.zip` da skill que mudou.
- **Claude Code:** `/plugin marketplace update officetuning`.
- **Pastas locais** (Copilot, Gemini CLI): `git pull` no clone.

⚠️ Skill executa instruções e, às vezes, scripts. Instale só skills de fontes
que você confia e leia o `SKILL.md` antes. Vale para estas também.
