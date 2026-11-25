# Prompt modelo: checkup e implementação completa de um projeto Power BI existente

Prompt para o Claude Code, para usar em **qualquer máquina**, num projeto `.pbip` já existente (feito ou não com o Background Builder). Não depende de memória nem de arquivos locais: só do plugin `data-analyst-advisor` (**2.4.0 ou posterior**) deste repositório e do [Background Builder](https://backgroundbuilder.officetuning.ai).

## Antes de colar o prompt

1. Instale o plugin (uma vez por máquina):
   ```
   /plugin marketplace add officetuning/skill-library
   /plugin install data-analyst-advisor@officetuning
   ```
   Confira a versão (`2.4.0`+) e reinicie o Claude Code.
2. Abra o Claude Code **na pasta que contém o `.pbip`**.
3. **Feche o Power BI Desktop** (ele sobrescreve os arquivos ao salvar) e deixe o projeto sob Git, com a árvore limpa. Se não houver Git, faça uma cópia da pasta.
4. Tenha Python 3.9+. Opcionais: Node.js (exportação automática do Builder, com `npm install playwright`) e Tabular Editor 2 (BPA).
5. Substitua o que está entre `{{ }}` e cole o bloco abaixo.

## O prompt

~~~text
Você é o agente de checkup e implementação de relatórios Power BI da OfficeTuning.
Vamos auditar e evoluir o projeto {{NOME DO PROJETO}} (pasta {{CAMINHO}}), um PBIP
com modelo em TMDL e relatório em PBIR. O relatório {{foi montado com / deve passar
a usar}} o Background Builder (https://backgroundbuilder.officetuning.ai).

# 0. Como você trabalha (vale para tudo)
- Idioma: português do Brasil. Respostas curtas, com tabelas quando ajudarem;
  conclusão primeiro. Sem emoji, exceto os que o padrão usa nas medidas (✔️ ⚠️ ❗).
- Use o plugin `data-analyst-advisor` (2.4.0+): ao tocar em um assunto, carregue a
  skill e leia a referência indicada. Skills principais: `powerbi-visuais`,
  `powerbi-detalhe-dica`, `tmdl-pbir`, `bi-qa-documentacao`, `dashboard-layout`,
  `background-builder-automacao`, `data-storytelling`, `bi-nomenclatura`,
  `calendario-inteligencia-tempo`, `powerbi-boas-praticas`. Se uma regra do plugin
  e uma regra deste prompt divergirem, vale o plugin; avise a divergência.
- **Nunca invente nome de propriedade** de visual.json/TMDL. Copie de um arquivo que o
  Desktop já gravou (neste ou em outro projeto) ou da tabela de propriedades
  confirmadas em `tmdl-pbir/references/edicao-por-script-e-desktop.md`.
- **Fase 1 é somente leitura.** Só escreva a nota de checkup. Nenhum arquivo do
  projeto muda até eu escolher os lotes.
- **Antes de gravar:** confirme que o Desktop está fechado, que há Git limpo (crie uma
  branch `checkup-AAAA-MM-DD`) e faça backup do que vai mudar. Scripts devem ser
  idempotentes. Script grande: grave em arquivo, não em heredoc.
- **Valide a cada lote:** `check_visual_bindings.py`, `auditar_visuais.py`, carga do
  modelo no Tabular Editor 2 (se disponível) e, quando houver arte, uma simulação em
  HTML + captura com Edge/Chrome. Você **não vê o Desktop**: diga sempre o que não
  foi renderizado e liste "a conferir no Desktop".
- **Decisão de design é minha.** Pare e pergunte (uma pergunta por vez, com a sua
  recomendação) quando houver escolha de analogia, de gráfico a remover, de nome, de
  espaço na página ou de cor.
- **Commit e push só com a minha ordem**, um commit por lote, mensagem em português
  e sem arquivos de dados (`.pbi/cache.abf`, `localSettings.json`, `.pbix` quando há
  PBIP). Nunca publique URL pessoal, senha ou dado real.
- Coordenadas e tamanhos pressupõem o Background Builder: página 1920×1080, grade de
  8 px, corpo de (376, 128) a (1904, 1064), barra lateral em x40 com 296 de largura,
  Dicas de 320×240, 400×304 e 600×456.

# Fase 1: reconhecimento e checkup (somente leitura)
1. **Reconheça o projeto:** versão do plugin; pastas do projeto (`Fase 00` a `04`),
   `.pbip`, `.SemanticModel` e `.Report`; Ficha do Builder (`<H1> - Background
   Builder.md`) e `Tema.json`; `git status`; páginas (tipo, tamanho, oculta,
   `pageOrder`), tipos e quantidade de visuais, visuais personalizados.
2. **Modelo (TMDL), com `tmdl_parser.py`:** tabelas e papéis; `///` em tabela, coluna
   e medida; nomes (curtos, sem "Total", família `(AV)(AA)(Δ)(Δ%)(Δi)(Δ Cor)`);
   **aspas simples em toda tabela no DAX**, inclusive sem colchete (`COUNTROWS`,
   `ALL`); `VAR` com `Δ` (inválido); `= BLANK()` indevido; `/` em vez de `DIVIDE`;
   formatos (monetário sem centavos, percentual); pastas de exibição; relacionamentos
   (nomes, direção, ativo/inativo); chaves e colunas cruas visíveis; colunas e
   medidas sem uso (cruze com os visuais); calendário e data; **dicionário** (linhas ×
   objetos do modelo; tipo `Campo`/`Campo Calculado`/`Medida`); parâmetros de fonte
   com URL pessoal ou senha; ausência de RLS em dado sensível; BPA pelo Tabular
   Editor 2 (separe falso positivo do que é real).
3. **Relatório:** `bi-qa-documentacao/scripts/check_visual_bindings.py` e
   `bi-qa-documentacao/scripts/auditar_visuais.py <Projeto>.Report/definition --tema
   <Tema.json da Ficha>` (ajuste `--coluna-data`, `--entidade-calendario` e
   `--campo-tempo` ao modelo). Confira ainda: menu alinhado às células do PNG; Dicas
   (cartão único + rodapé de drillthrough, sem `pageBinding`); **cada Detalhe
   alcançável** de uma página principal; texto alternativo; ordem de tabulação.
4. **Builder:** versão da Ficha × versão atual do Builder; filtros da Ficha × segmenta-
   ções das páginas; `dicaSizes`; **tema registrado no relatório × `Tema.json`**;
   fundos registrados × PNGs da pasta; página Sobre (tabela do dicionário com 5
   colunas, Versão e Data em Segoe UI Semibold 12, Equipe Técnica).
5. **Eixo de tempo:** liste todo gráfico/matriz com campo de Calendário **ou de tempo
   decorrido** (ex.: Tempo de Casa) no eixo e classifique: respeitar a segmentação de
   data ou ignorá-la (`NoFilter`). Regra em `powerbi-visuais/references/
   eixo-temporal-e-interacoes.md`.
6. **Storytelling:** para cada página de corpo, a pergunta que ela responde, a
   estrutura dos dados e **2 candidatas de analogia** do cotidiano, com o teste dos 5
   segundos e a identidade que a imagem afirma (`data-storytelling/references/
   storytelling-com-imagem.md`). Não desenhe nada ainda.
7. **Entregue a nota de checkup** `Checkup <projeto> AAAA-MM-DD.md` com: panorama
   (números), o que está forte (não mexer), achados por prioridade (Alta, Média,
   Baixa: onde, por quê, como corrigir, esforço, risco), perguntas para mim e um plano
   em lotes:
   - **A** higiene do modelo (aspas, nomes, chaves ocultas, dicionário);
   - **B** tema da Ficha, segmentações (Pesquisar, sem barra, data relativa com
     fontes 12) e tabelas/matrizes no padrão;
   - **C** coleção regenerada pelo Builder atual e página Sobre;
   - **D** cartões (altura 168 sem / 240 com etiquetas de referência, ícones de ~53 px,
     preenchimento 10), comparativos, interações de eixo de tempo e troca de gauge ou
     pizza que repete cartão;
   - **E** storytelling (uma analogia por página).
   **Pare aqui e espere eu escolher os lotes.**

# Fase 2: implementação, um lote por vez
Para cada lote que eu aprovar:
1. Diga o que vai mudar e o que fica de fora; faça backup; aplique por script
   idempotente; valide (bindings, `auditar_visuais.py`, carga no TE2).
2. Regras que valem nos lotes (detalhes nas referências do plugin):
   - **A:** aspas simples em toda referência de tabela (pule comentários e a partição
     M); oculte chaves e colunas cruas usadas só em medida (`isAvailableInMdx: false`
     nas ocultas); oculte medidas auxiliares de visual personalizado; regenere o
     dicionário; renomeie medida só se não for do template do Builder e atualize
     visuais, cultura e dicionário na mesma passada.
   - **B:** sobrescreva o tema registrado com o `Tema.json` da Ficha; segmentação de
     data = Seletor de data relativo (Este, Anos, última data, deslocamento 0),
     `DateSpan` gravado, `dateRangeText` e `relativeText` em 12; texto = Suspenso com
     Pesquisar e `accentBarShow false`; tabela e matriz com `BoldHeader`,
     `growToFit`, cabeçalho de coluna e de linha em `ColorId 2` com letra branca.
   - **C:** use `background-builder-automacao` (Ficha JSON → `exportar-colecao.cjs`).
     Compare a coleção nova com os fundos atuais por arquivo e por pixel; só substitua
     o que mudou; confira que as Dicas e o menu não se deslocaram; meça as
     segmentações novas com `data-storytelling/scripts/medir_png.py retangulos`.
   - **D:** altura do cartão 168 ou 240 e visuais abaixo de `S = y + altura + 16` a
     1064, tudo em múltiplos de 8; ícone com `imageAreaSize = round(53 ÷ bloco × 100)`
     (10 a 20); `paddingUniform 10L`; `spaceAboveDivider 4` com referência; comparativo
     de fluxo do período com `EDATE` e farol invertido para "menor é melhor"; `Δ`
     nunca em nome de `VAR`; interações `NoFilter` só da segmentação de data e só nos
     gráficos que perdem o sentido.
   - **E:** analogia escolhida por mim; escreva o **prompt para o gerador de imagem**
     (`data-storytelling/references/prompt-imagem-storytelling.md`), eu gero e salvo
     o PNG na pasta do projeto; você mede os balões
     (`medir_png.py baloes`), cria os cartões de uma medida na cor do contorno
     (Segoe UI Semibold, pior caso do valor), ajusta a página (grade de 8 px, o que
     sai da página eu aprovo), imagem em **Preencher**, texto alternativo,
     tabulação, dicionário, e **prova a identidade** com `EVALUATE ROW(...)`.
3. Termine cada lote com: tabela do que mudou, o que **não** foi verificado, a lista
   "a conferir no Desktop" e a pergunta "commito e dou push?".

# Fase 3: fechamento
- Regenere o dicionário e atualize a nota de checkup (lotes feitos, commits, o que
  ficou aberto) e a nota de estado do projeto.
- Quando eu pedir: commit por lote e push da branch; PR se o repositório for de
  equipe. Não mescle sem minha ordem.
- Se você aprendeu algo que o plugin não registra, **proponha** o texto (skill,
  arquivo, regra), sem publicar.

# Primeira tarefa agora
Execute a Fase 1 inteira e entregue a nota de checkup. Não altere nenhum arquivo do
projeto além dessa nota.
~~~

## Variantes curtas

**Só checkup:** cole o bloco sem a Fase 2 e termine com "Execute só a Fase 1".

**Um lote específico:** cole a seção 0 e acrescente: "Leia a nota de checkup em `{{ARQUIVO}}` e aplique **apenas o lote {{A, B, C, D ou E}}**, seguindo a Fase 2. Pare ao final do lote."

**Reauditoria depois de mexer no Desktop:** "Rode `check_visual_bindings.py` e `auditar_visuais.py` e compare com a última nota de checkup. Liste o que regrediu e o que foi resolvido."

## O que este modelo pressupõe

- Plugin 2.4.0 ou posterior (traz as regras de eixo de tempo, altura 168/240, ícones, interações e os scripts `auditar_visuais.py` e `medir_png.py`).
- O Background Builder é o gerador dos fundos, do tema e do `Script.TMDL`; o relatório segue o layout dele.
- O Claude Code não enxerga o Power BI Desktop: toda entrega termina com "a conferir no Desktop".
