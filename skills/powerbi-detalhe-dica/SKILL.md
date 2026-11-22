---
name: powerbi-detalhe-dica
description: Páginas de Detalhe (drillthrough) e Dica de Ferramenta (tooltip page) no Power BI, e o par Detalhe + Dica de um mesmo campo — escolha do campo, chave do drillthrough, ponto de entrada, medida de seleção (SELECTEDVALUE e LOOKUPVALUE), cartão único da dica, rodapé padrão, tamanhos de Dica do Background Builder e fiação em PBIR (pageBinding, visualTooltip). Use ao criar ou revisar página de detalhe, drillthrough, tooltip page, "Dica de Ferramenta", medida "você está vendo" ou ao decidir quais campos merecem detalhe e dica. Para o visual em si use powerbi-visuais; para a sintaxe dos arquivos use tmdl-pbir.
---

# Detalhe e Dica de Ferramenta

## Pergunta central

> De onde o leitor chega a esta página, e o que ele precisa ver sobre aquele único item?

Detalhe e Dica respondem a mesma pergunta em duas profundidades: a Dica é o
relance ao passar o mouse; o Detalhe é a página inteira ao clicar. Se não há
um visual numa página principal com o campo-chave, **nenhum dos dois é
alcançável**.

## Regras

**Obrigatório**
- **Escolha o campo pelo uso, não pela intuição.** Conte os campos que já são
  eixo de visuais e segmentações das páginas principais; o par nasce do mais
  frequente. Campo que nenhum visual usa não tem ponto de entrada.
- **Todo Detalhe tem entrada numa página principal.** Se a entidade só aparece
  como linha dentro de outro detalhe, não vale criar. Se o campo não é eixo de
  nada, crie a página principal que o exiba (ex.: ranking) antes do detalhe.
- **Chave única no drillthrough.** Use o código, não o nome (nomes repetem). A
  coluna-chave precisa estar no visual de origem (pode ser uma coluna estreita).
- **Medida de seleção por campo**: nome igual ao do campo (padrão de nome de
  medida em `bi-nomenclatura`; ver "Armadilha de nomes" em
  `powerbi-boas-praticas/references/medidas-para-visuais.md`), pasta `Seleção`,
  `SELECTEDVALUE ( coluna, "-" )`. Para colunas de tabelas do lado "um" da
  relação, que o filtro da tabela "muitos" não alcança, use `LOOKUPVALUE` pela
  chave. Descreva com `///`.
- **Um visual aponta para uma única dica.** Em matriz com duas dimensões,
  escolha a dimensão que ainda não tem dica.
- **Dica = um cartão + um gráfico (+ rodapé).** O cartão é **um só**; o título
  do cartão é a medida de seleção e os indicadores ficam dentro dele.
- **Rodapé padrão, só na dica que tem detalhe irmão**:
  "🔍 *Para explorar o detalhe*: clique com o **botão direito** sobre o dado de
  interesse, selecione **Drillthrough/Detalhamento** e escolha a página de
  destino no menu." (itálico em "Para explorar o detalhe"; negrito em
  "botão direito" e "Drillthrough/Detalhamento").
- Detalhe e Dica ficam **ocultos** (`HiddenInViewMode`); a Dica tem `type: Tooltip`.

**Preferir**
- Tamanho da Dica pelo conteúdo, nos três tamanhos do Background Builder
  (todos múltiplos de 8):

  | Tamanho | Uso | Exemplo |
  |---|---|---|
  | **320×240** | Visual único | Campo de poucos valores (Categoria, Tipo de pessoa, Transação): só o cartão, sem rodapé |
  | **400×304** | Vários visuais | Cartão + um gráfico pequeno |
  | **600×456** | Mini relatório | Cartão + gráfico com eixo legível + rodapé |
- Detalhe com: indicadores em faixa, evolução no tempo, composição e uma
  tabela de linhas. O cabeçalho é o do Background Builder: "Você está vendo:"
  seguido da medida de seleção, e botão "← Voltar" a 16 px da borda
  (`dashboard-layout/references/background-builder.md`).
- Campos de poucos valores recebem **só Dica**; campos de muitos valores
  (pessoa, UF, natureza) recebem **Dica + Detalhe**.
- Margem de 8 px dentro da dica; cartão e gráfico com a mesma largura.

**Evitar**
- Detalhe exclusivo de outro detalhe.
- Dois cartões na dica (um de título, outro de indicadores): o título do
  cartão único cumpre os dois papéis.
- Cartão da dica com rolagem. Veja `powerbi-visuais` (cartões).
- Mensagem de ajuda ("clique com o botão direito") em dica sem detalhe.

## Armadilhas verificadas
- No **modo de edição** da página de Dica não há filtro: a medida de seleção
  mostra "-". O título só se confirma passando o mouse no relatório.
- Medida que **sobrescreve** filtro de uma coluna que também é segmentação
  produz números incoerentes; ver `powerbi-boas-praticas` (KEEPFILTERS).
- Filtro da tabela "muitos" não propaga para a "um": `SELECTEDVALUE` direto na
  dimensão "um" devolve "-" no detalhe de uma pessoa.

## Fiação em PBIR (resumo; detalhes em `tmdl-pbir`)

| O quê | Onde |
|---|---|
| Página de detalhe | `page.json`: `filterConfig.filters[]` (`howCreated: "Drillthrough"`) + `pageBinding { type: "Drillthrough", parameters: [{ name, boundFilter, fieldExpr }] }` |
| Página de dica | `page.json`: `type: "Tooltip"`, largura/altura da dica |
| Visual que usa a dica | `visualContainerObjects.visualTooltip[0].properties = { show: true, section: '<nome da página de dica>' }` |
| Título do cartão = medida | `visualContainerObjects.title[0].properties.text = { expr: { Measure: … } }` |
| Fundo da dica | PNG do Builder registrado em `report.json › RegisteredResources` |

## Checklist
1. Contei os eixos e escolhi o campo? Existe visual principal com a chave?
2. Medida de seleção criada, descrita e testada com o mouse?
3. Dica com um cartão, título = medida, rodapé só se houver detalhe?
4. Cada visual de origem aponta para a dica correta (e só uma)?
5. Detalhe oculto, com "Você está vendo:" + medida de seleção e botão "← Voltar"?
6. Tamanho da Dica (320×240, 400×304 ou 600×456) coerente com o conteúdo?
