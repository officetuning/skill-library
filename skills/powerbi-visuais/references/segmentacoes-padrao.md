# Padrão das segmentações (acrescentar a `powerbi-visuais`)

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
- **Pesquisar: ligado** quando possível. **[a confirmar]** A propriedade não
  está gravada em nenhum dos ~190 segmentadores dos quatro projetos. Não
  deduza o nome: peça ao autor que ligue Pesquisar em **um** segmentador de
  texto, salve, e leia o arquivo para replicar.

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
