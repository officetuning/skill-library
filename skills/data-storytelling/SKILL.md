---
name: data-storytelling
description: Storytelling com dados aplicado a relatórios Power BI, a partir dos frameworks de Cole Nussbaumer Knaflic — contexto e audiência, escolha do gráfico eficaz, limpeza de poluição visual, atributos pré-atentivos, Big Idea, título-conclusão e arco narrativo entre páginas. Use quando o usuário pedir a mensagem principal de uma página, reduzir poluição visual, preparar apresentação para diretoria, decidir qual gráfico comunica melhor, ou citar storytelling, Big Idea, gráfico de espaguete ou "então o quê?". Para a configuração técnica do visual use powerbi-visuais.
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
- **Título como conclusão:** "Sul superou a meta; Norte caiu 12%", não "Vendas por Região".
- Dado mais importante no canto superior esquerdo (leitura em Z/F).
- Storyboard no papel antes de abrir o Power BI.

**Evitar**
- Pizza com mais de 2–3 fatias, 3D, gauge no lugar de KPI, eixo duplo sem necessidade.
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
- **Lógica horizontal:** lendo só os títulos das páginas em sequência, a
  história fecha: **situação → complicação → resolução**.

Detalhe dos oito blocos (contexto, gráfico, poluição e Gestalt, atenção,
design, Big Idea, arco, checklist): `references/blocos.md`.

## Checklist antes de publicar

- [ ] Big Idea em uma frase com sujeito + verbo + consequência
- [ ] Gráfico de menor esforço para a comparação que importa
- [ ] Bordas, grades e legendas desnecessárias removidas
- [ ] Um único destaque pré-atentivo por página
- [ ] Cor comunica estado de negócio, nunca decora
- [ ] Título é conclusão, não rótulo
- [ ] Títulos em sequência contam a história
- [ ] Contraste AA e informação não depende só de cor

## Fonte

Síntese interpretativa de KNAFLIC, C. N. *Storytelling com Dados*. Rio de
Janeiro: Alta Books, 2019 (trad. de *Storytelling with Data*, Wiley, 2015). Cite
a obra e resuma o conceito; não transcreva trechos do livro.
