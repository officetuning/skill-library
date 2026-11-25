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
- **Data:** `data.mode = 'RelativeDatePicker'` com filtro `DateSpan` sobre
  `ScopedEval ( Max ( Calendário[Data] ) )`, `TimeUnit 3` (ano): o rótulo fica
  "Este ano a partir da última data", deslocamento 0. `slider` e
  `calendarButton` na cor 1 do tema (ícone na cor 0), `relativeText.fontSize
  10.8`. **[verificado]**

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
