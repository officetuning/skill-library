---
name: data-storytelling
description: Storytelling com dados aplicado a relatórios Power BI, a partir dos frameworks de Cole Nussbaumer Knaflic — contexto e audiência, escolha do gráfico eficaz, limpeza de poluição visual, atributos pré-atentivos, Big Idea, título-conclusão e arco narrativo entre páginas. Use quando o usuário pedir a mensagem principal de uma página, reduzir poluição visual, preparar apresentação para diretoria, decidir qual gráfico comunica melhor, ou citar storytelling, Big Idea, gráfico de espaguete ou "então o quê?". Para a configuração técnica do visual use powerbi-visuais. Também: imagem de storytelling por analogia escolhida para os dados (visual thinking, design-by-analogy), sempre verdadeira com qualquer filtro.
---

# Storytelling com dados no Power BI

## Tese

Gráfico correto não é o mesmo que gráfico eficaz. Eficácia é a velocidade e a
clareza com que a audiência entende a mensagem e sabe o que fazer com ela.

**Fluxo:** contexto (quem, o quê, como) → visual certo → tirar poluição →
focar a atenção → pensar como designer → amarrar em Big Idea e arco → testar
com "então o quê?".

## Regras

**Obrigatório**
- Antes de sugerir visual, saiba (ou infira do briefing): quem é a audiência, o
  que ela precisa saber ou fazer, e como vai consumir (reunião ao vivo ou
  leitura solitária).
- Toda página crítica tem uma **Big Idea** que cabe numa frase.
- Ao revisar, **corte antes de colorir**: poluição sai antes de discutir cor ou estilo.
- **Um** destaque pré-atentivo por página. Cinco cores chamando atenção anulam o efeito.
- Dado pontual (1–2 números) ou leitura exata → texto ou tabela. Padrão ou comparação → gráfico.
- Acessibilidade: contraste WCAG AA e nunca codificar categoria só por cor.

**Preferir**
- Linha para tendência; barras horizontais para ranking com nome longo; colunas
  para categoria curta ou tempo discreto.
- Cinza em 85–90% dos elementos; cor de destaque só no dado da Big Idea.
- **Conclusão visível na página** (nome da página, cartão, infográfico, anotação). Nos gráficos
  do Power BI vale o **título automático**, com os campos renomeados no visual; escreva o título
  como conclusão ("Sul superou a meta; Norte caiu 12%") **só quando o autor pedir**: o texto
  digitado não acompanha o idioma do navegador (`powerbi-visuais`, `cartoes-e-titulos.md`).
- Dado mais importante no canto superior esquerdo (leitura em Z/F).
- Storyboard no papel antes de abrir o Power BI.

**Evitar**
- Pizza ou rosca com mais de 4 fatias (padrão OfficeTuning; o livro é mais rígido, 2–3), 3D, gauge no lugar de KPI, eixo duplo sem necessidade.
- Página com rolagem vertical: tudo cabe na página Full HD (1920 × 1080).
- Legenda longe do dado (prefira rótulo direto).
- Bordas, grades densas, sombras: tinta que não informa.
- Cor que decora em vez de comunicar.
- Dashboard "de tudo": se tudo está em negrito, nada está.

## Big Idea

Três componentes:
1. **O quê** — uma ideia central, não uma lista.
2. **Por que importa** — um ponto de vista defensável com os dados.
3. **O que está em jogo** — a consequência de agir ou não agir.

**Teste:** sujeito + verbo + consequência numa frase. Se não cabe, a página
responde duas perguntas e deve virar duas. Faça também o teste dos **3 segundos**:
o que a audiência conclui olhando 3 segundos, sem explicação? Escreva isso
**antes** de escolher o gráfico.

## Qual gráfico

| A pergunta é... | Prefira |
|---|---|
| Um valor importa agora | Cartão ou texto |
| Comparar poucos itens | Barras horizontais ordenadas |
| Itens ao longo do tempo | Linha (contínuo) ou coluna (discreto) |
| Composição de um total | Barras 100% empilhadas |
| Relação entre duas variáveis | Dispersão |
| Desvio de uma meta | Barra divergente ou bullet chart, não gauge |
| Valor exato | Tabela ou matriz |

Barra/coluna agrupada, linha, cartão, tabela/matriz e barra 100% empilhada
cobrem cerca de 80% dos relatórios corporativos.

## Arco narrativo

- **Lógica vertical:** dentro da página, cada elemento sustenta a Big Idea. O
  que não sustenta sai ou vai para drill-through.
- **Lógica horizontal:** lendo só os nomes das páginas (e a conclusão de cada uma) em
  sequência, a história fecha: **situação → complicação → resolução**.

Detalhe dos oito blocos (contexto, gráfico, poluição e Gestalt, atenção,
design, Big Idea, arco, checklist): `references/blocos.md`.

## Identidade do relatório

- **H1 = o assunto** do relatório, não o departamento. Só se sustenta se
  existir uma página que o represente.
- **H2 em forma de pergunta** (ou promessa) curta, com ritmo.
- **Tagline = o que o relatório entrega.** Confira cada promessa com o
  conteúdo real antes de aceitar.
- **Nome de página descreve o conteúdo**, nunca o tipo de visual nem o nome de
  uma medida.
- O arco narrativo é uma **sequência de perguntas**: cada página responde uma,
  e a ordem das páginas segue a ordem das perguntas.

No Background Builder, H1, H2 e tagline vão para o fundo: mudar identidade
exige regenerar os PNGs (`dashboard-layout/references/background-builder-ciclo.md`).

Teste do H1, três combinações de H2 e tagline para o autor escolher, Período
como "Quando" e fontes de dados em linguagem de leitor:
`references/identidade-do-relatorio.md`.

## Storytelling com imagem

Imagem que conta a história dos dados (visual `image` + cartões de uma medida
sobre as chamadas). **Cada relatório tem a sua analogia**, escolhida a partir da
estrutura dos dados (fases, níveis, partes, comparação, território, meta) e
**verdadeira com qualquer filtro**; nunca se reaproveita a ilustração de outro
relatório trocando etiquetas. Método (visual thinking e design-by-analogy),
tabela de analogias e exemplo: `references/storytelling-com-imagem.md`.

- **Teste dos 5 segundos:** se a analogia precisa de explicação, ela falhou
  (a banheira foi trocada pelo ponto de ônibus). Prefira cena do cotidiano.
- **Uma analogia por página**, mesma família visual, cenas diferentes (nunca a
  estrada em toda página).
- **A imagem afirma uma identidade**: prove-a com as medidas e teste com
  `EVALUATE ROW(...)`; desenhe neutro (marcadores no mesmo nível).
- **Arte 3D vem de gerador de imagem**, não de SVG à mão: o agente escreve o prompt
  (`references/prompt-imagem-storytelling.md`), o autor gera, e o agente mede os
  balões com `scripts/medir_png.py` e posiciona os cartões.

## Checklist antes de publicar

- [ ] Big Idea em uma frase com sujeito + verbo + consequência
- [ ] Gráfico de menor esforço para a comparação que importa
- [ ] Bordas, grades e legendas desnecessárias removidas
- [ ] Um único destaque pré-atentivo por página
- [ ] Cor comunica estado de negócio, nunca decora
- [ ] A conclusão de cada página está visível (título-conclusão em gráfico só se o autor pediu)
- [ ] Campos renomeados no visual para o título automático ler bem
- [ ] Páginas em sequência contam a história
- [ ] Contraste AA e informação não depende só de cor

Com número de regra e severidade, este checklist está na Seção 8 de
`powerbi-boas-praticas` (8.1 a 8.13), para citar numa revisão.

## Fonte

Síntese interpretativa de KNAFLIC, C. N. *Storytelling com Dados*. Rio de
Janeiro: Alta Books, 2019 (trad. de *Storytelling with Data*, Wiley, 2015). Cite
a obra e resuma o conceito; não transcreva trechos do livro.
