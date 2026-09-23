---
name: dashboard-canvas
description: Método Dashboard Canvas (OfficeTuning) para planejar um relatório Power BI antes de abrir o Desktop — 12 blocos em 4 fases (Descoberta, Dados, Governança, Execução), taxonomia de tabela e campo, matrizes Tipo de Dado × Segmentação e Tipo de Dado × 5W2H, anatomia de página e revisão de modelo existente contra o Canvas. Use em briefing de BI, workshop com cliente, escopo de dashboard, cronograma de projeto BI, 5W2H ou "planejar dashboard". Para posição em pixel dos visuais use dashboard-layout.
---

# Dashboard Canvas

Método de planejamento usado **antes** do Power BI Desktop. O usuário preenche
o canvas no web app ([dashboardcanvas.officetuning.com.br](https://dashboardcanvas.officetuning.com.br/metodologia)),
que gera uma especificação técnica em Markdown. Essa especificação:

- alimenta o **Background Builder** (sistema visual, skill `dashboard-layout`);
- serve de handoff e documentação para quem constrói e mantém;
- alimenta o **Cronograma Consolidado** do projeto.

O Canvas não gera visual. Ele força decisões de escopo e modelagem antes, para
reduzir retrabalho.

Duas etapas: **Canvas ETL & Modelagem** (blocos 1–9) e **Data Visualization** (blocos 10–12).

## Os 12 blocos

### Fase 1 — Descoberta
1. **Problema** — qual pergunta de negócio o relatório responde? Se não cabe
   numa frase, o escopo está inflado (mesmo teste da Big Idea, skill `data-storytelling`).
2. **Nível de Decisão** — cada página por visão temporal
   (operacional/tático/estratégico) e finalidade; calibra o nível de detalhe.
3. **Contexto de Uso** — apresentação ao vivo ou leitura solitária.

### Fase 2 — Dados
4. **Origem dos Dados** — sistema, planilha, API; taxonomia de tabela e campo (abaixo).
5. **Frequência de Atualização** — diário, semanal, tempo real; define refresh
   completo ou incremental (skill `power-query-m`).
6. **Horários de Atualização** — janela da fonte e fuso horário (ver o bug de
   "última atualização" na skill `dashboard-layout`).

### Fase 3 — Governança
7. **Regras de Usuários / RLS** — quem vê o quê.
8. **Riscos** — qualidade de dado, atraso de fonte, mudança de escopo; mitigação.
9. **Premissas** — o que se assume sem validação (ex.: "vendas já líquidas de devolução").

### Fase 4 — Execução
10. **Cálculos** — medidas e sua lógica, justificadas pela Matriz Tipo de Dado ×
    5W2H e nomeadas no padrão AV/AA/Δ/Δ%/Δi (skill `bi-nomenclatura`).
11. **Cronograma & Esforço** — estimativa por etapa, consolidada no Cronograma Consolidado.
12. **Encerramento** — critério de pronto: números batendo, RLS testada, performance aceitável.

## Taxonomia

| Tabela | Prefixo físico | Papel |
|---|---|---|
| Fato | `TabFat` | Eventos e transações |
| Dimensão | `TabDim` | Entidades para filtrar e agrupar |
| Monolítica | `TabFlt` | Tudo numa estrutura; protótipo, legado ou escopo simples |

| Campo | Papel |
|---|---|
| Chave Primária | Identifica a linha |
| Chave Estrangeira | Aponta para a PK de outra tabela |
| Descritor | Texto ou categoria; não se agrega |
| Georreferenciado | Candidato a Categoria de Dados para mapa |
| Agregável | Numérico com soma/média de negócio |

Prefixos nunca aparecem na camada semântica (skill `bi-nomenclatura`).

## Matrizes de apoio

- **Tipo de Dado × Tipo de Segmentação** — cada filtro recebe um tipo de dado
  que determina as segmentações compatíveis (ex.: Data/Hora aceita data
  relativa; Texto não aceita "Entre", "Antes de", "Depois de").
- **Tipo de Dado × 5W2H** — cruza o tipo de dado com What/Why/Where/When/Who/How/How
  much para justificar cada medida no Bloco 10 antes de criá-la.

## Anatomia de página (Canvas 2)

1. **Mensagem principal** — a Big Idea.
2. **Painel Visual** — por visual: **Intenção**, **Cálculo** (medida) e
   **Posição** (Topo/Meio/Base).
3. **Hierarquia visual** — o elemento dominante e os secundários.
4. **Cronograma** — esforço da página.

A skill `dashboard-layout` transforma a Posição qualitativa em coordenadas.

## De-Para: Canvas → Power BI

| Origem no Canvas | Ação no Power BI |
|---|---|
| Canvas 1 (blocos 1–9) | Tabelas, relacionamentos, RLS, estratégia de refresh |
| Canvas 2 (blocos 10–12) | Layout, visuais, medidas DAX, cronograma |
| Configuração global de filtros | Segmentações com controle compatível |

| Intenção no Canvas | Visual no Power BI |
|---|---|
| Valores | Cartão ou KPI |
| Comparação entre poucos itens | Barras horizontais ordenadas |
| Tendência temporal | Linhas |
| Composição de um total | Barras 100% empilhadas |
| Diagnóstico / causa raiz | Árvore de Decomposição |
| Inteligência Artificial | Principais Influenciadores, Decomposição, Narrativa Inteligente |

## Ponte com o Background Builder

Três campos opcionais do Canvas vão direto para o Background Builder:
**Idealização/Realização** (créditos), **Subtítulo** e **ícone de cabeçalho**.

## Revisar um modelo existente contra o Canvas

Ao inspecionar um modelo (TMDL, MCP do Power BI, print ou PDF), avalie:

1. Cada tabela se comporta como Fato, Dimensão ou Monolítica, e o nome físico
   reflete isso? Sinalize `TabFatDados`, `TabFatBase`.
2. Chaves e colunas técnicas ocultas?
3. Chave substituta inteira nos relacionamentos fato-dimensão?
4. Tabela monolítica usada em várias páginas com fan-out? Recomende estrela.
5. Campos geográficos com Categoria de Dados?
6. Descritores com sumarização numérica? Troque para "Não resumir".
7. Tipo de segmentação compatível com o tipo de dado (Matriz 1)?
8. Prefixo técnico exposto em objeto visível?
9. Medidas com nome amigável, contagem com `#`, comparativo em AV/AA/Δ/Δ%/Δi?
10. Sem especificação? Recomende montar um Canvas retroativo, ao menos para handoff.
