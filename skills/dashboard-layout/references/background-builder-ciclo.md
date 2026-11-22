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

O H2 e a tagline reaparecem no hero da página Início: mudar identidade exige
regenerar o fundo.

## Identidade (H1, H2, tagline, fontes)
- **H1** = o assunto do relatório, não o departamento. Só se sustenta se
  existir uma página que o represente.
- **H2** = frase manuscrita curta, com ritmo (pergunta ou promessa). Sem
  espaço inicial: o Builder grava como veio.
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

Regra geral: largura = itens × célula; ler a posição dos rótulos no PNG. Cada
página nova muda o menu, o PNG e a ficha. Nome de página descreve conteúdo;
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
  `<Projeto> - Dica de Ferramenta - <Uso> <L>x<A>.png`.
