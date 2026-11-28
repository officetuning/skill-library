# Janela de histórico, check-up de banco e correções: plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publicar a 2.12.0 com seis correções e as lições de check-up de banco e de janela de histórico.

**Architecture:** Só Markdown, um script Python e os arquivos de versão. Conteúdo longo vai para `references/`, com uma remissão curta no `SKILL.md`.

**Tech Stack:** Markdown, Python 3.9+ (biblioteca padrão), T-SQL e M em exemplos.

**Spec:** `docs/superpowers/specs/2026-11-28-janela-e-checkup-de-banco-design.md`

## Global Constraints

- Repositório **público**: nenhum nome, dado, valor, servidor, esquema ou área de projeto real. Exemplos genéricos.
- Cada item novo diz o que foi testado: banco em um SQL Server 2017; janela SQL instalada e comparada; **parte M não aberta no Desktop**; incremental no Service **não testado**.
- Texto em português, no tom das skills. Preservar o fim de linha de cada arquivo.
- Versão **2.12.0** em `plugin.json`, `marketplace.json`, `CHANGELOG.md` e "Novidades" do `README.md`.
- Commit, push e PR **só com autorização do autor**; nunca merge. Os passos "commit" abaixo esperam essa ordem.
- Arquivos de teste no scratchpad da sessão (`<scratch>`), fora do repositório.

## Review Focus

1. Visual com nível de hierarquia de tabela ou hierarquia renomeada: o script deve acusar.
2. Visual com campo de hierarquia válido ou com variação de data automática (`PropertyVariationSource`): sem falso positivo.
3. Referência por apelido em filtro (`SourceRef.Source`): continua ignorada, sem quebrar.
4. Modelo sem nenhuma hierarquia: resultado igual ao de hoje.
5. Consulta de exemplo de banco rodada por quem só tem leitura: avisar quais exigem `VIEW SERVER STATE`.

---

### Task 1: hierarquias no `check_visual_bindings.py`

**Files:**
- Modify: `skills/bi-qa-documentacao/scripts/tmdl_parser.py`
- Modify: `skills/bi-qa-documentacao/scripts/check_visual_bindings.py`
- Test: `<scratch>/plugin212/test_hierarquia.py`

**Interfaces:**
- Produces: cada tabela de `parse_model` ganha `hierarquias: list[{"nome": str, "niveis": list[str]}]`.
- Produces: `check_visual_bindings.hierarchy_refs(node, found: list[tuple[str, str, str]])` com `(tabela, hierarquia, nivel)`; `model_levels(model) -> set[tuple[str, str, str]]`. `field_refs` mantém a assinatura.

- [ ] **Step 1: teste que falha** (`unittest`, com PBIP temporário: tabela `Calendário`, hierarquia `Fiscal`, níveis `Ano` e `Mês`)

```python
test_nivel_valido:       main(modelo, relatorio_com("Fiscal", "Ano")) == 0
test_nivel_inexistente:  main(modelo, relatorio_com("Fiscal", "Semana")) == 1
test_hierarquia_errada:  main(modelo, relatorio_com("Antiga", "Ano")) == 1
test_sem_hierarquia:     relatório só com colunas válidas == 0
```

- [ ] **Step 2:** `python <scratch>/plugin212/test_hierarquia.py` → falham os dois casos que esperam 1.
- [ ] **Step 3:** implementar. No parser, `level` é filho de `hierarchy` (um nível de indentação a mais); o nível referencia uma coluna. Nó do PBIR: `{"HierarchyLevel": {"Expression": {"Hierarchy": {"Expression": {"SourceRef": {"Entity"}}, "Hierarchy": nome}}, "Level": nivel}}`.
- [ ] **Step 4:** testes passam; `checar_medidas.py`, `checar_svg.py` e `extrair_modelo.py` continuam rodando no mesmo PBIP temporário.
- [ ] **Step 5:** rodar o script em um PBIP real local com hierarquia, só leitura: nenhuma referência quebrada nova sem causa.
- [ ] **Step 6: commit** `bi-qa: conferir níveis de hierarquia nos visuais`.

### Task 2: cinco correções de texto

**Files (Modify):**
- `docs/como-usar-skills.md`: 15 skills nas três ocorrências; acrescentar à tabela `background-builder-automacao` e `calendario-inteligencia-tempo`.
- `skills/bi-qa-documentacao/SKILL.md`: "papel pelo prefixo" → papel pelo grupo de consultas, depois prefixo antigo e relacionamentos.
- `skills/dashboard-layout/references/wireframe.md`: filtros na barra lateral (corpo x 376 a 1904), nas duas passagens.
- `skills/data-storytelling/references/storytelling-com-imagem.md`: seção 3 passa a `scaling 'Fill'`, com a ressalva da proporção 3:1.
- `skills/bi-qa-documentacao/references/checagens-adicionais.md`: item 14 cobra rodapé só em Dica com Detalhe irmão.

- [ ] **Step 1:** editar.
- [ ] **Step 2:** `grep -rnE "13 skills|papel pelo prefixo|modo de cabeçalho|scaling 'Normal'" docs/como-usar-skills.md skills` → sem saída; contar 15 linhas na tabela do guia.
- [ ] **Step 3: commit** `Corrige cinco inconsistências da 2.11.0`.

### Task 3: check-up de banco

**Files:**
- Create: `skills/bi-qa-documentacao/references/checkup-banco-sql.md`
- Modify: `skills/bi-qa-documentacao/SKILL.md` (remissão e termo "check-up do banco" na `description`)

Conteúdo fixo, nesta ordem: regras (somente leitura, fora da janela de carga, aviso de conta com privilégio alto); tabela de itens com consulta e o que significa (versão e nível de compatibilidade; opções do banco e último backup; objetos, tamanhos, heaps e índices; dependências das views; tempos e leituras em `sys.dm_exec_query_stats`; permissões no schema; scripts que apagam dados na instalação); aceite de mudança em view (comparar o SQL novo sem instalar; salvar `OBJECT_DEFINITION`; mesmo script antes e depois na mesma carga; medir com **todas as colunas**, porque projeção estreita engana; instalar em transação); nota: `:r` com variável pode não ser substituído, preferir caminho relativo e testar com arquivo inofensivo.

- [ ] **Step 1:** escrever com nomes genéricos (`bi`, `VwFatVenda`).
- [ ] **Step 2:** executar cada consulta, só leitura, em um SQL Server disponível; todas rodam sem erro. Registrar a versão no texto.
- [ ] **Step 3: commit** `bi-qa: roteiro de check-up de banco`.

### Task 4: janela de histórico e checagens

**Files:**
- Create: `skills/power-query-m/references/janela-de-historico.md`
- Modify: `skills/power-query-m/SKILL.md` (seção Incremental Refresh: remissão)
- Modify: `skills/calendario-inteligencia-tempo/SKILL.md` (seção "Ano fiscal e orçamento": remissão)
- Modify: `skills/bi-qa-documentacao/references/checagens-adicionais.md` (checagens 31 a 33)

Conteúdo fixo da referência: perguntar a intenção antes de apontar limite de histórico como erro; regra em um só lugar (view de uma linha no SQL e, para fonte em arquivo, expressão M); fim exclusivo `<`, com o caso do dia a mais que só aparece quando a fonte passa a ter a data; tabela sem política de atualização usa os parâmetros do modelo ou carrega tudo; incremental em anos conta ano civil, não reprocessa exceção antiga e, em janela que anda, mantém partições antigas; exemplo T-SQL e M para N = 2 com ano fiscal iniciando em outubro, hora local calculada por `DateTimeZone.SwitchZone` e `RemoveZone`. Marcar o M como não aberto no Desktop.

Checagens: 31 script TMDL avulso defasado em relação ao PBIP; 32 planilha, PDF ou exportação com dado sensível versionada; 33 período gravado em segmentação que ficará fora da janela (`grep -rnE "'[0-9]{2}-[0-9]{2}'"` para ano fiscal no formato `AA-AA`).

- [ ] **Step 1:** escrever.
- [ ] **Step 2:** testar a fórmula T-SQL do exemplo com datas fixas (30/09, 01/10 de dois anos) em consulta só de leitura; conferir cada afirmação sobre incremental na documentação da Microsoft e citar o link.
- [ ] **Step 3: commit** `Janela de histórico e checagens 31 a 33`.

### Task 5: versão 2.12.0 e conferência

**Files (Modify):** `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `CHANGELOG.md`, `README.md`

- [ ] **Step 1:** 2.12.0 nos quatro lugares, com o estado de verificação no CHANGELOG.
- [ ] **Step 2:** rodar a comparação de `.github/workflows/versao.yml` → `Versões coincidem: 2.12.0`.
- [ ] **Step 3:** links relativos citados existem; varrer o diff por nomes, servidores, bancos e valores do projeto de origem → nenhum.
- [ ] **Step 4: commit** `Versão 2.12.0`.
- [ ] **Step 5:** com autorização, push e PR com o que foi e o que não foi testado.
