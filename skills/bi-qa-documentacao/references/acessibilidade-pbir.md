# Acessibilidade em PBIR

Complementa a regra 7.11 `ENSURE_ALTTEXT` de `powerbi-boas-praticas`
(`references/regras-bpa.md`) com o caminho no PBIR e a ordem de tabulação.

## Texto alternativo
- **Em português, um por visual**, descrevendo o que o visual mostra, não só o
  tipo. Exemplos: "Segmentação por região, em lista suspensa: filtra todos os
  visuais da página."; "Gráfico de colunas: Entradas e saídas por mês."
- Ferramentas automáticas podem gerar em **outro idioma** (a de varredura
  testada gerou em italiano): conferir o idioma antes de aplicar; se não for o
  do relatório, escreva você.
- Caminho: `visual.visualContainerObjects.general[0].properties.altText`
  (literal). Vale também para cascata, área, mapa e árvore. [verificado em
  projetos; anote a versão do Desktop ao registrar novos tipos de visual]
- Nunca sobrescrever um texto que o autor já escreveu.
- Cartão de cabeçalho de detalhe: "exibe o item em análise", sem citar valores
  que mudam.
- Visual decorativo (imagem): `altText` vazio e `tabOrder = -9999000`.
  [doc; texto vazio a confirmar no Desktop]

## Ordem de tabulação
- Por página, de cima para baixo e da esquerda para a direita: menu →
  atualização → botão → indicadores → segmentações → gráficos.
- Múltiplos de 1000. Pela documentação da ferramenta, **o maior valor recebe o
  foco primeiro**. [doc: confirmar em Exibição › Painel de seleção › Ordem de
  tabulação]
- **Nunca alterar `z`** (empilhamento visual).
- Se o Desktop ignorar a ordem gravada, confira o `$schema` do `visual.json`:
  já houve versão (2.147.x) que descartou `tabOrder` com schema incompatível.
  Ver `tmdl-pbir/references/edicao-por-script-e-desktop.md`.

## Títulos e legibilidade
- Título e subtítulo seguem a regra de `powerbi-visuais` (cartões, tabelas,
  matrizes e árvores personalizados; gráficos padrão).
- Texto truncado ("…") em cartão é problema de acessibilidade: reduza a fonte
  a partir do padrão do tema até caber.
