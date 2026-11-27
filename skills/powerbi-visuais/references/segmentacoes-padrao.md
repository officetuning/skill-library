# Padrão das segmentações

Regra do autor para segmentações.

## Obrigatório
- **Cabeçalho da segmentação: desligado.**
- **Tela de fundo: desligada** e **fronteira visual: desligada** (no contêiner,
  `visualContainerObjects.background.show = false` e `border.show = false`).
  Na auditoria de três projetos, as segmentações de **data** eram as que
  faltavam.
- **Estilo:** texto em **Suspenso** (`data.mode = 'Dropdown'`); data em
  **Seletor de data** (nos projetos, `data.mode = 'RelativeDatePicker'`).
  [verificado]
- **Pesquisar: ligado** em segmentação de texto: `general.selfFilterEnabled =
  true`. **[verificado]** Mais `dropdown.accentBarShow = false` (sem barra de
  destaque).
- **Data:** `data.mode = 'RelativeDatePicker'` (Seletor de data) com filtro
  `DateSpan` sobre `ScopedEval ( Max ( Calendário[Data] ) )`, `TimeUnit 3` (ano):
  a data está no **Este**, unidade **Anos**, ancorada na **última data**,
  deslocamento 0; o rótulo fica "Este ano a partir da última data". **[verificado]**
  - O filtro fica em `objects.general[0].properties.filter` (`Version 2`, `From`
    com a tabela de datas, `Where › Comparison ComparisonKind 0 › Right › DateSpan`).
    **Copie de uma segmentação que o Desktop já gravou.** Sem esse bloco o
    `RelativeDatePicker` abre sem recorte nenhum.
  - **Fontes: 12 em `dateRangeText` (Intervalo de datas) e em `relativeText`
    (Resumo)**, as duas. (A regra antiga, `relativeText.fontSize 10.8`, foi
    substituída.) Confirmado no Desktop: `dateRangeText` e `relativeText` são os
    dois grupos de "Texto" da segmentação de data. **[verificado]**
  - `slider` e `calendarButton` seguem o tema (ícone na cor 0) e podem variar por
    projeto; o que não varia é o filtro e as fontes.
  - **Confira todas as páginas.** Em auditorias, a segmentação da primeira página
    costuma estar certa e as das outras sem o filtro ou sem as fontes.

## Preferir
- Segmentações do painel lateral em x40, largura 296; Período altura 120, as
  demais 40; mesma ordem em todas as páginas de corpo (a ordem vem da
  classificação 5W2H da ficha).
- Texto alternativo: "Segmentação por região, em lista suspensa: filtra todos
  os visuais da página." e, para data, "Segmentação de período: seleciona o
  intervalo de datas que filtra todos os visuais da página."
- Rótulo do campo limpo no visual (`displayName`): "Região", não "Nome da
  Região".

## Evitar
- Cabeçalho, fundo ou borda ligados por herança do tema: confira o contêiner de
  cada segmentação, não só a primeira.
- Segmentação de data em `RelativeDatePicker` sem o `filter` gravado.
- Barra de destaque ligada em segmentação suspensa (`dropdown.accentBarShow`
  precisa ser `false`; mudar só a cor da barra não desliga).
- Deixar um gráfico de **eixo temporal** obedecer à segmentação de data sem pensar:
  com "Este ano" ele pode perder o sentido. Ver `references/eixo-temporal-e-interacoes.md`.

## Depois de "Redefinir para o padrão" [verificado, nov/2026]
Aplicado a várias segmentações selecionadas no Desktop, o comando **apagou** a
pesquisa (`general.selfFilterEnabled`), a barra de destaque
(`dropdown.accentBarShow`) e o **texto alternativo**. A sincronização (`syncGroup`)
e as seleções gravadas se mantiveram. Se o autor redefinir:
1. compare os `visual.json` com a versão anterior;
2. religue a pesquisa e restaure o texto alternativo (não mudam a aparência);
3. **desligue de novo a barra de destaque** (`dropdown.accentBarShow = false`): é uma
   estética das versões recentes, que volta ligada ao padrão, e a regra do autor é
   desligada em todos os projetos;
4. nas demais escolhas, replique o que ele decidiu manter e pergunte quando divergir
   deste padrão.
