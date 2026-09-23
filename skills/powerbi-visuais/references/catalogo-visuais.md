# Catálogo de visuais

Baseado nos princípios de Stephen Few e na documentação Microsoft Learn.

> "Um dashboard eficaz é o produto não de medidores e semáforos bonitinhos, mas
> sim de um design informado: mais ciência que arte, mais simplicidade do que
> deslumbre." — Stephen Few

---

## 1. Comparação e tendência

### Barras e colunas
- **Quando:** comparar categorias. Colunas quando o eixo X é tempo; barras com
  rótulo longo (> 5 caracteres) ou mais de 5 categorias.
- **Por quê:** comprimento é o atributo mais preciso depois da posição.
- **Configurar:** grade desligada ou cinza a 15%; rótulo de dado na barra;
  sem título de eixo redundante; uma cor só, destaque só com significado;
  ordenar por valor quando a ordem da categoria não importa.
- **Evitar:** empilhar mais de 3 séries; eixo sem zero; cor diferente por barra sem motivo.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-column-charts)

### Linhas
- **Quando:** tempo contínuo com mais de 8 períodos; até 4–5 séries.
- **Por quê:** a inclinação é percebida antes de qualquer número.
- **Configurar:** marcador só nos pontos de atenção; linha de meta/média no
  painel de Análise; rótulo no fim da linha em vez de legenda.
- **Recursos:** *Análise → Encontrar anomalias* e *Análise → Previsão*.
- **Evitar:** mais de 5 séries (espaguete); dado categórico sem relação temporal.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-line-chart)

### Área
- **Quando:** a magnitude da mudança é o insight; 100% empilhada para composição no tempo.
- **Configurar:** transparência de 50–70%.
- **Evitar:** mais de 3 séries empilhadas; valores muito oscilantes.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-basic-area-chart)

### Combinação (combo)
- **Quando:** duas métricas com escalas diferentes e relação clara (Receita em R$ × Margem em %).
- **Configurar:** nomeie os dois eixos; cores contrastantes; rótulo só na série principal; alinhe os zeros.
- **Evitar:** mais de uma linha sobre as colunas; métricas sem relação (sugere correlação falsa).
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-combo-chart)

### Faixa (ribbon)
- **Quando:** a mudança de posição no ranking ao longo do tempo é o insight.
- **Configurar:** 5–7 categorias; cor fixa por categoria.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/desktop-ribbon-charts)

### Cascata (waterfall)
- **Quando:** decompor a variação de um KPI, DRE simplificada, fluxo de caixa.
- **Configurar:** verde positivo, vermelho negativo, cinza/azul nos totais; rótulo em todas as barras.
- **Evitar:** mais de 10–12 etapas; trocar as cores convencionais.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-waterfall-charts)

---

## 2. Partes de um todo

### Pizza e rosca
- **Aceitável:** 2 a 4 categorias com proporção dominante e óbvia.
- **Substituto superior:** barras horizontais ordenadas.
- **Se usar:** máximo 4 fatias, resto em "Outros"; percentual dentro da fatia;
  sem legenda se o rótulo identifica; na rosca, total no centro via caixa de texto.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-pie-donut-chart)

### Treemap
- **Quando:** hierarquia com muitos itens e alguns dominantes.
- **Configurar:** um matiz em gradiente; rótulo só nos retângulos grandes; drill-down.
- **Evitar:** valores próximos; mais de 3 níveis.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-treemaps)

### Funil
- **Quando:** processo sequencial com perda entre etapas.
- **Configurar:** valor e % de conversão sobre a etapa anterior; saturação maior nos gargalos; nunca inverta a ordem.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-funnel-charts)

---

## 3. Distribuição e relação

### Dispersão, bolhas e dot plot
- **Quando:** correlação entre duas variáveis, outliers, clusters. Bolhas para uma terceira dimensão.
- **Configurar:** rótulo só nos outliers; legenda com até 5–6 categorias;
  linhas de média nos dois eixos criam quadrantes; defina tamanho mínimo/máximo da bolha.
- **Recurso:** Eixo de Reprodução para animar no tempo.
- **Evitar:** mais de 200–300 pontos sem agrupamento.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-scatter)

---

## 4. Tabela e matriz

### Tabela
- **Quando:** valor exato, várias unidades, complemento de gráfico.
- **Configurar:** linha alternada cinza claro (#F5F5F5); sem divisor vertical;
  número à direita, texto à esquerda; total em negrito; sparkline e barras de dados.
- **Formatação condicional:** fundo por regra, ícones por regra de negócio, barras de dados.
- **Evitar:** bordas em toda célula; mais de 8–10 colunas.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-tables)

### Matriz
- **Quando:** mais de uma dimensão, hierarquia expansível, subtotais.
- **Configurar:** layout escalonado; expandir/recolher; formatação condicional como heatmap.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-matrix-visual)

---

## 5. Mapas

- **Mapa preenchido:** métrica por região delimitada; gradiente sequencial de um matiz, nunca arco-íris.
- **Mapa de bolhas:** pontos específicos (filiais, clientes) com volume no tamanho.
- **Shape Map:** regiões próprias via TopoJSON.
- **Regra:** só quando a distribuição geográfica é o insight. Senão, barras.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-map-visualizations-overview)

---

## 6. KPI, cartão e progresso

### Cartão
- **Quando:** o KPI principal, no canto superior esquerdo.
- **Configurar:** título específico ("Receita MTD", não "Receita"); fonte grande;
  subtítulo com variação; sem borda nem fundo colorido.

```dax
Subtítulo Receita =
VAR vVariacao = [Δ% Total de Vendas]
RETURN
    IF (
        ISBLANK ( vVariacao ),
        BLANK (),
        IF ( vVariacao >= 0, "▲ ", "▼ " )
            & FORMAT ( ABS ( vVariacao ), "0.0%" )
            & " vs ano anterior"
    )
```

⚠️ A string de formato do `FORMAT` usa sempre `.` como marcador decimal; a
saída sai com o separador da localidade (vírgula em pt-BR). Teste no Service.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-card)

### Visual KPI
- **Quando:** existe meta; mostra valor, meta e tendência no espaço de um cartão.
- **Configurar:** campos Valor, Metas e Eixo de tendência; defina qual direção é "boa".
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-kpi)

### Medidor (gauge)
- **Aceitável:** monitoramento em tempo real, TV de operação, audiência leiga.
- **Se usar:** Valor, Mínimo, Máximo e Meta; cores semânticas.
- **Substitutos:** KPI, bullet chart (AppSource), cartão com formatação condicional.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-radial-gauge-charts)

### Metas (scorecards)
- **Quando:** vários KPIs com metas formalizadas, no Service.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/create-reports/service-goals-create)

---

## 7. Visuais com IA

- **Árvore de Decomposição:** causa raiz ("por que SP caiu 15%?"). Métrica em
  *Analisar*, dimensões em *Explicar por*, ative a divisão por IA.
  [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-decomposition-tree)
- **Principais Influenciadores:** o que aumenta ou reduz um resultado. Alterne
  entre *Principais influenciadores* e *Segmentos principais*.
  [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-influencers)
- **Narrativa Inteligente:** resumo automático; personalize com medidas DAX.
  [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-smart-narrative)
- **Detecção de anomalias:** recurso do gráfico de linhas (*Análise → Encontrar anomalias*).
  [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-anomaly-detection)

---

## 8. Segmentação

| Formato | Quando |
|---|---|
| Lista | Até 7–8 itens visíveis de uma vez |
| Suspenso (dropdown) | Mais de 8 itens ou pouco espaço |
| Botões | Poucas opções (Ano: 2024 · 2025 · 2026) |
| Controle deslizante de data | Intervalo contínuo |

- Agrupe as segmentações numa área (cabeçalho ou painel lateral).
- *Exibir → Sincronizar segmentações* para valer entre páginas.
- Defina seleção única ou múltipla pela regra de negócio.
- Executivos raramente abrem o painel de filtros: o que importa fica no canvas.
- [Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-slicers)

---

## 9. Estrutura e navegação

- **Caixa de texto e formas:** título, nota metodológica, agrupamento. Um
  retângulo cinza atrás de um grupo de KPIs substitui bordas individuais.
- **Botões e navegadores:** Navegador de Páginas e de Indicadores; estados de
  botão (padrão, hover, pressionado); oculte as abas e use navegação própria.
- **Imagem:** logo; imagem dinâmica com coluna em Categoria de Dados = URL da Imagem.
- **Relatório paginado:** layout pixel-perfect para impressão e PDF.
- **Visuais R e Python:** estatística avançada; interatividade limitada.

---

## Recursos transversais

### Formatação condicional
Fundo, fonte, barras de dados, ícones e URL. Regra de design: comunica status
de negócio, não enfeita.
[Docs](https://learn.microsoft.com/pt-br/power-bi/create-reports/desktop-conditional-table-formatting)

### Tooltip page
1. Nova página → Configurações de Página → Tipo de Página → Dica de Ferramenta.
2. Tamanho personalizado **400 × 304 px** (padrão do ecossistema; ver skill `dashboard-layout`).
3. Visuais de contexto (histórico, comparação).
4. No visual principal: Formatar → Dica de ferramenta → Tipo → Página do relatório.
[Docs](https://learn.microsoft.com/pt-br/power-bi/create-reports/desktop-tooltips)

### Cálculos visuais
DAX no próprio visual, sem contexto de filtro do modelo.

```dax
Total Acumulado = RUNNINGSUM ( [Receita Total] )
% do Total = DIVIDE ( [Receita Total], COLLAPSE ( [Receita Total], ROWS ) )
```
[Docs](https://learn.microsoft.com/pt-br/power-bi/transform-model/desktop-visual-calculations-overview)

### Small multiples
Uma grade de mini-versões do mesmo visual. Melhor que 8 linhas coloridas quando
a pergunta é se o padrão se repete.
[Docs](https://learn.microsoft.com/pt-br/power-bi/visuals/power-bi-visualization-small-multiples)

### Painel de Análise
Linha constante, média, mediana, mínimo, máximo, percentil, previsão, anomalias
e barras de erro. Uma linha de meta mostra quem está acima e abaixo sem esforço.
[Docs](https://learn.microsoft.com/pt-br/power-bi/transform-model/desktop-analytics-pane)
