# Background Builder: ciclo de trabalho, menu e filtros

Complementa `background-builder.md`. As posições em pixel abaixo foram medidas
nos PNGs do Builder 1.031 (nov/2026); se o Builder mudar, vale o guia de
montagem exportado do projeto. Estrutura e slots: `background-builder.md`.

## Ciclo de trabalho
Mudou H1, H2, tagline, páginas de corpo, filtros ou fontes de dados?
1. Atualize o projeto: **Abrir Ficha Técnica** no Builder (o `.md` traz o JSON
   completo), altere no formulário e exporte de novo. Editar o `.md` à mão
   exige mudar texto **e** JSON.
2. **Gere os PNGs de novo** no Builder.
3. **Sobrescreva os fundos registrados** (cada página tem a sua cópia); ajuste
   de imagem **Alongar** (`Fit` no `page.json`), transparência 0%.
4. **Reposicione** o navegador e as segmentações conforme o PNG novo.
5. Reabra o projeto sem salvar e confira com captura de tela.

O próprio Builder ajuda a conferir antes de exportar: **Comparar** mostra lado a
lado a prévia e o PNG real, e **Conferir medidas** audita a geometria (grade de
8 px, painel lateral, assinatura) e exibe "Tudo cabe no Power BI" quando passa.

O H2 e a tagline reaparecem no hero da página Início: mudar identidade exige
regenerar o fundo.

## Identidade (H1, H2, tagline, fontes)
- **H1** = o assunto do relatório, não o departamento. Só se sustenta se
  existir uma página que o represente.
- **H2** = frase manuscrita curta, com ritmo (pergunta ou promessa). Sem
  espaço inicial: o Builder grava como veio. É **opcional**: em branco, o PNG
  não desenha texto nem sublinhado no cabeçalho de nenhuma página nem no hero
  do Início, e a tagline sobe 96 px. Vazio ↔ preenchido muda todos os PNGs:
  regenere tudo.
- **Tagline** = o que o relatório **entrega**. Confronte cada promessa com o
  conteúdo real antes de aceitar.
- **Fontes de dados** em linguagem de leitor, uma por linha; sem endereços nem
  e-mails; "dados fictícios" em projeto de portfólio.

## Menu e navegador
O menu do PNG tem uma célula por item (Início + páginas de corpo + Sobre). O
`pageNavigator` é invisível e precisa ficar **sobre as células**:

| Itens no menu | Célula | `x` | Largura | `y` / altura |
|---|---|---|---|---|
| 4 | 200 px | 616 | 800 | 16 / 96 |
| 5 | 200 px | 512 | 976 | 16 / 96 |
| 8 | 160 px | 368 | 1280 | 16 / 96 |

A tabela é um exemplo medido com o título padrão, não uma fórmula fixa. O
Builder calcula o menu assim (1.029 em diante):

- **Passo único** entre os itens, em múltiplos de 8 px: os separadores "·"
  ficam sempre equidistantes. Em coleções normais o passo vai de 80 a 200 px.
- **Limites:** o menu começa depois do título (o maior entre H1 e H2) com 24 px
  de folga e termina no máximo em x=1680, 24 px antes do ícone de atualização.
  Fica **centralizado** nesse espaço. Título longo e muitos itens diminuem o
  passo.
- **Rótulo que não cabe:** o Builder reduz a fonte por degraus (15, 14, 13 e
  12 px, com padding menor) e só em último caso usa reticências. Passo abaixo
  de 80 px só aparece quando o menu transbordaria, e continua múltiplo de 8.
- **Coleção que já cabia fica idêntica**: nada muda até que um rótulo seja
  cortado ou o menu passe de 1680.

Por isso, a regra prática: largura = itens × passo; **ler a posição dos
rótulos no PNG**, nunca calcular de cabeça.

Cada página nova muda o menu, o PNG e a ficha. Nome de página descreve conteúdo;
nunca é nome de medida.

## Painel de filtros (global)
- Sidebar 344×936 em x=16, y=128, a partir de 1 filtro; segmentações em
  x=40, largura 296 (1/1), 144 (1/2) ou 96/96/88 (1/3), 8 px entre itens;
  data completa 296×120. Tabela do Encaixe em `background-builder.md`.
- **É o mesmo em todas as páginas de corpo**; a ordem vem da ficha. Mudou a
  ordem → mover as segmentações em todas as páginas.
- Por isso, **toda medida precisa funcionar com todos os filtros** (ex.:
  entradas/saídas com `KEEPFILTERS` se Transação for segmentação).
- Período: modo relativo ("este ano", a partir da última data) como padrão;
  sem ele a página abre em todo o histórico.

### Classificação 5W2H dos filtros
| 5W2H | Filtros típicos |
|---|---|
| Quando | Período |
| Onde | Região, UF, município |
| Quem | Atributos da pessoa: tipo, atividade, categoria (do geral ao específico) |
| O quê | Tipo de movimento (ex.: recebimento/pagamento), produto |

## Layout (complemento a `dashboard-layout`)
- **Margem e vão de 16 px** entre visuais e bordas, cabeçalho e painel; grade de 8 px.
- Com painel: conteúdo em x=376→1904 e y=128→1064. Sem painel (detalhe): x=16→1904.
- Duas colunas iguais sem painel: x=16 e x=968, largura 936. Posições **inteiras**.
- Zonas a evitar: cabeçalho até y=112; faixa de marca de x=1904 a 1920; arcos
  decorativos dos cantos nos detalhes. O rodapé é livre até x=1904.
- Dicas do Builder: 320×240 (visual único), 400×304 (vários visuais) e
  600×456 (mini relatório); margem interna de 8 px. Escolha em
  `powerbi-detalhe-dica`. Com uma dica, o PNG sai como
  `<Projeto> - Dica de Ferramenta.png`; com duas ou três, como
  `<Projeto> - Dica de Ferramenta - <Uso> (<L>x<A>).png`.

## Filtro exclusivo de uma página
O painel do Builder é igual em todas as páginas de corpo. Para um filtro que só uma
página tem (ex.: seletores de linha, coluna e valor):
1. copie a Ficha e acrescente os filtros no fim (classificação **Como** os deixa
   abaixo dos demais, sem deslocar os outros);
2. exporte e confira que `filtrosForaDoPainel` veio vazio;
3. aproveite **somente a faixa da barra lateral** (x 0 a 376, a partir de y 128) do
   PNG daquela página e cole sobre o fundo registrado dela;
4. meça os nichos novos no PNG e posicione as segmentações, sem sincronização.

Guarde a segunda Ficha ao lado da principal. A mesma técnica de colar só a faixa
alterada (cabeçalho, y 0 a 128) acrescenta um item de menu sem refazer o corpo dos
fundos; compare por pixel antes de substituir.
