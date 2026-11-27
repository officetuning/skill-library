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
- **Medida de seleção por campo**: `<Campo> Selecionado(a)` (`Estado
  Selecionado`, `Categoria Selecionada`), na tabela do campo, pasta `Seleção`,
  `SELECTEDVALUE ( coluna, "-" )`. O hífen é o texto padrão de "nada ou vários
  selecionados". Nome diferente da coluna (`bi-nomenclatura`; ver "Armadilha
  de nomes" em `powerbi-boas-praticas/references/medidas-para-visuais.md`).
  Para colunas de tabelas do lado "um" da relação, que o filtro da tabela
  "muitos" não alcança, use `LOOKUPVALUE` pela chave. Descreva com `///`.
- **Um visual aponta para uma única dica.** Em matriz com duas dimensões,
  escolha a dimensão que ainda não tem dica.
- **Dica = um cartão + um gráfico (+ rodapé).** O cartão é **um só**; o título
  do cartão é a medida de seleção e os indicadores ficam dentro dele.
- **Rodapé padrão de drillthrough só nas Dicas que têm Detalhe irmão**,
  ocupando o espaço de rodapé da Dica (Dica sem Detalhe não leva o texto):
  "🔍 *Para explorar o detalhe*: clique com o **botão direito** sobre o dado de
  interesse, selecione **Drillthrough/Detalhamento** e escolha a página de
  destino no menu." (itálico em "Para explorar o detalhe"; negrito em
  "botão direito" e "Drillthrough/Detalhamento"; 8 pt).
- **Ordem de tabulação da Dica:** cartão → gráfico → rodapé. Layout em Grade,
  geometria, texto alternativo sem o nome técnico da medida de seleção:
  `references/dica-cartao-unico.md`.
- Detalhe e Dica ficam **ocultos** (`HiddenInViewMode`); a Dica tem `type: Tooltip`.

**Preferir**
- Detalhe no tamanho padrão de página (1920×1080). Dica num dos três
  tamanhos do Background Builder (todos múltiplos de 8), escolhido pelo
  **conteúdo** a exibir, não pelo tipo de campo:

  | Tamanho | Uso | Conteúdo |
  |---|---|---|
  | **320×240** | Visual único | Só o cartão (+ rodapé, se houver Detalhe irmão; essa geometria ainda não foi medida) |
  | **400×304** | Vários visuais | Cartão + um gráfico pequeno (+ rodapé) |
  | **600×456** | Mini relatório | Cartão + gráfico com eixo legível (+ rodapé) |
- Detalhe com: indicadores em faixa, evolução no tempo, composição e uma
  tabela de linhas. No cabeçalho do Background Builder, a medida de seleção
  vai no card de (1232, 48) 496×32, depois do ícone de olho (o fundo não
  escreve "Você está vendo:"), e o botão Voltar fica em (1744, 40) 144×48
  (`dashboard-layout/references/background-builder.md`).
- O script TMDL do Builder cria `[Você Está Vendo]` como **medida-modelo
  transitória** (devolve `BLANK()`). Quando o campo do Detalhe estiver
  definido, **renomeie** a própria medida para `<Campo> Selecionado(a)`, mova-a
  para a tabela do campo e escreva o `SELECTEDVALUE ( coluna, "-" )`: o card do
  cabeçalho continua ligado e não sobra medida órfã.
- Campos de poucos valores recebem **só Dica**; campos de muitos valores
  (pessoa, UF, natureza) recebem **Dica + Detalhe**.
- Margem de 8 px dentro da dica; cartão e gráfico com a mesma largura.

**Evitar**
- Detalhe exclusivo de outro detalhe.
- Dois cartões na dica (um de título, outro de indicadores): o título do
  cartão único cumpre os dois papéis.
- Cartão da dica com rolagem. Veja `powerbi-visuais` (cartões).
- Rodapé de drillthrough numa Dica sem Detalhe irmão: promete um caminho que não existe.
- Medida de seleção com o mesmo nome da coluna, ou `Você Está Vendo` esquecida
  no relatório publicado.

## Armadilhas verificadas
- **320×240 não comporta 12 meses** com eixo de valores: o gráfico rola de lado. Cartão +
  gráfico mensal ficou legível em 600×456 (cartão 584×128 em y8; gráfico 584×304 em y144,
  sem rodapé quando não há Detalhe irmão).
- Fundo do Builder em outro tamanho: troque `dicaSizes` na Ficha, exporte e atualize
  largura e altura da página.
- Botão **Voltar** com fundo e borda desligados (`show false`): o desenho está no PNG.
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
| Página de dica | `page.json`: `type: "Tooltip"`, **sem `pageBinding`**, largura/altura da dica (com `pageBinding` o hover mostra o tooltip padrão) |
| Visual que usa a dica | `visualContainerObjects.visualTooltip[0].properties = { show: true, section: '<id da página de dica>' }`, **sem `type`** |
| Título do cartão = medida | `visualContainerObjects.title[0].properties.text = { expr: { Measure: … } }` |
| Fundo da dica | PNG do Builder registrado em `report.json › RegisteredResources` |

## Dica com imagem e molde de Detalhe
Entidade com foto ou desenho (estampa, vendedor, canal): visual `image`
dinâmico na Dica (600×456: imagem 232×296, gráfico 344×296, cartão 584×136; ou
400×304 com imagem 88×88) e **sem ícones no cartão da Dica**. Molde único de
Detalhe para várias entidades: `references/dica-com-imagem-e-moldes.md`.

## Checklist
1. Contei os eixos e escolhi o campo? Existe visual principal com a chave?
2. Medida de seleção criada, descrita e testada com o mouse?
3. Dica com um cartão e título = medida; rodapé só se houver Detalhe irmão?
4. Cada visual de origem aponta para a dica correta (e só uma)?
5. Detalhe oculto, com o card ligado a `<Campo> Selecionado(a)` (não `Você Está Vendo` com `BLANK()`) ao lado do ícone de olho e o botão Voltar?
6. Tamanho da Dica (320×240, 400×304 ou 600×456) coerente com o conteúdo?

## Antes de dizer que está pronto
Siga a sequência de `powerbi-visuais` ("Antes de dizer que um visual está pronto"):
abrir a referência, partir de um visual salvo pelo Desktop, auditar e pedir PDF ou
captura.
