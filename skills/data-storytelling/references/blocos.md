# Os oito blocos, aplicados ao Power BI

| Pedido | Bloco |
|---|---|
| Entender a audiência | 1 |
| Tipo de gráfico | 2 (tabela no SKILL.md) |
| Limpar visual poluído | 3 |
| Destacar o dado certo | 4 |
| Usabilidade e acessibilidade | 5 |
| Mensagem principal | 6 (Big Idea no SKILL.md) |
| Sequência de páginas | 7 |
| Checklist final | 8 (no SKILL.md) |

## Bloco 1 — Contexto

1. **Quem é a audiência?** Nível de decisão (estratégico, tático, operacional),
   familiaridade com os dados, o que ela já acredita ou teme.
2. **O que ela precisa saber ou fazer depois?** Se a resposta é "só ver os
   números", falta uma decisão associada. Volte ao Bloco 1 (Problema) da skill
   `dashboard-canvas`.
3. **Como vai consumir?** Ao vivo, o apresentador guia e o visual pode ser mais
   denso e progressivo. Leitura solitária exige visual que se explica sozinho,
   com título-conclusão e anotação.

## Bloco 3 — Poluição visual e Gestalt

Todo elemento tem custo cognitivo: o cérebro decide se é informação ou decoração.

**Faxina:**
1. Tire bordas quando o espaço em branco já separa os blocos.
2. Reduza a grade a poucas linhas de referência, ou use rótulo direto.
3. Troque a legenda por rótulo na própria série.
4. No máximo 2 pesos de fonte e 1–2 cores de destaque por página.
5. Alinhe tudo a uma grade (skill `dashboard-layout`).

**Gestalt útil em dashboard:**
- **Proximidade:** perto = relacionado. Agrupe KPIs do mesmo tema pelo espaçamento.
- **Similaridade:** mesma cor/forma = mesma categoria. Não varie estilo sem motivo.
- **Fechamento:** o olho completa a forma; o cartão não precisa de borda inteira.
- **Conexão:** linha ou seta vence proximidade e cor. Use pouco.

## Bloco 4 — Atenção e atributos pré-atentivos

Cor, tamanho, posição, orientação, forma e negrito são percebidos antes da
atenção consciente. Use **um** para o dado que sustenta a Big Idea.

Antes de aplicar cor ou formatação condicional, pergunte: qual é o único ponto
que a audiência deve ver primeiro nesta página?

No Power BI:
- Formatação condicional que pinta só a barra ou célula que quebra a regra de
  negócio; o resto em cinza.
- Anotação em caixa de texto apontando o pico ou desvio.
- Ordenar por valor quando o ranking é a mensagem: a posição já comunica.

Implementação técnica: skill `powerbi-visuais`.

## Bloco 5 — Pensar como designer

1. **Affordance:** o que é clicável parece clicável. Estados de botão (hover,
   seleção) distintos; nada interativo com cara de estático.
2. **Acessibilidade:** nunca só cor; contraste WCAG AA; ordem de tabulação e
   texto alternativo coerentes para leitor de tela.
3. **Estética a serviço da função:** consistência de fonte, cor e alinhamento
   entre páginas reduz o reaprendizado a cada tela.

## Bloco 7 — Arco narrativo

1. **Situação** — contexto e o "normal esperado" (visão geral).
2. **Complicação** — o desvio, risco ou oportunidade que motiva o relatório
   (tendência, alerta).
3. **Resolução** — a implicação e, quando fizer sentido, a recomendação
   (causa raiz, próximos passos).

Teste: leia só os títulos das páginas, em ordem. A história fecha sem abrir nenhuma?
