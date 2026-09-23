# Wireframe antes de construir

## Do Canvas ao wireframe

| Campo do Canvas | Vira no wireframe |
|---|---|
| Intenção | Rótulo do bloco ("Tendência de Receita 12M") |
| Cálculo | Medida vinculada, herdada sem alteração |
| Posição (Topo/Meio/Base) | Faixa de linhas |
| Hierarquia (dominante/secundário) | Largura em colunas |

## Exemplo: página "Performance Comercial" (sem Background Builder)

| Bloco | Intenção | Grid (col × linha) | Tamanho (px) | x, y |
|---|---|---|---|---|
| Faixa de filtros | Período e região | 1–12 × 1 | 1920×120 | 0, 0 |
| KPI Receita Total | Valor + Δ% AA | 1–3 × 2–3 | 480×240 | 0, 120 |
| KPI Ticket Médio | Valor + Δ% AA | 4–6 × 2–3 | 480×240 | 480, 120 |
| KPI Margem Bruta % | Valor + meta | 7–9 × 2–3 | 480×240 | 960, 120 |
| KPI Atingimento | Farol Δi | 10–12 × 2–3 | 480×240 | 1440, 120 |
| Tendência de Receita (dominante) | Linha 12M | 1–8 × 4–9 | 1280×720 | 0, 360 |
| Ranking por Vendedor | Barras top 10 | 9–12 × 4–9 | 640×720 | 1280, 360 |

Com Background Builder, a faixa de filtros sai (vai para o cabeçalho) e todo `y`
recebe a altura do cabeçalho.

A tabela é a fonte; a imagem do wireframe é só a representação humana dela. A
mesma tabela pode alimentar um script que posiciona os visuais de uma página
nova ou aplica o grid a um relatório antigo.

## Fluxo completo

```
Canvas (Painel Visual: Intenção / Cálculo / Posição qualitativa)
   ↓
Wireframe (tabela grid 12×9: coluna/linha → rótulo/medida)
   ↓
Conversão grid → pixel (x, y, width, height, tabOrder)
   ↓
Construção no Desktop OU escrita direta no visual.json (PBIR)
   ↓
QA camada 3 (skill bi-qa-documentacao): o campo no visual.json bate com o Cálculo previsto?
```

## Checklist

- [ ] Wireframe em 1920×1080 antes do Desktop
- [ ] Coluna e linha múltiplas de 8 (reconfira ao mudar o número de colunas/linhas)
- [ ] Com Background Builder: filtros no modo de cabeçalho; altura útil recalculada
- [ ] Todo bloco com Intenção e Cálculo herdados do Canvas
- [ ] Filtros e KPIs na mesma linha em todas as páginas
- [ ] Dominante ocupa mais colunas
- [ ] `tabOrder` anotado nos fluxos de leitura importantes
- [ ] Wireframe aprovado antes do primeiro visual
- [ ] Tabela grid → pixel guardada para as próximas páginas
