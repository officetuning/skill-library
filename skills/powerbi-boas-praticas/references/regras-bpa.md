# Catálogo das 90 regras

Formato: **nº — regra** · severidade · por que importa · como aplicar.
Severidade: Alta 🔴 · Média 🟠 · Baixa 🔵.

| Seção | Tema | Regras |
|---|---|---|
| 1 | Performance | 19 |
| 2 | Expressões DAX | 11 |
| 3 | Prevenção de erros | 10 |
| 4 | Manutenção | 8 |
| 5 | Nomenclatura | 2 |
| 6 | Formatação | 13 |
| 7 | Relatórios e visuais | 14 |
| 8 | Storytelling e comunicação (revisão manual) | 13 |

---

## Seção 1 — Performance

**1.1 — Evite tipos de ponto flutuante** · 🟠
Float/Double ocupam mais memória e calculam mais devagar.
Como: troque por Decimal Fixo ou Inteiro (`Table.TransformColumnTypes`).
❌ `Double 3.14159265358979` · ✅ `Decimal 3.14` (se 2 casas bastam)

**1.2 — `IsAvailableInMdx = false` em colunas não usadas em MDX** · 🟠
Colunas disponíveis em MDX geram hierarquia de atributo, que custa processamento.
Como: no Tabular Editor, `IsAvailableInMdx = false` em chaves e colunas técnicas que ninguém usa no Excel.

**1.3 — Evite bidirecional em coluna de alta cardinalidade** · 🟠
O motor avalia muito mais combinações na propagação de filtro.
Como: relacionamento unidirecional; `CROSSFILTER` só na medida que precisa.
```dax
CALCULATE ( [Vendas], CROSSFILTER ( Produtos[ID], Vendas[ProdutoID], BOTH ) )
```

**1.4 — Reduza coluna calculada com `RELATED`** · 🟠
Cada linha faz a busca no refresh; em milhões de linhas, minutos a mais.
Como: traga a coluna no Power Query com `Table.NestedJoin` + `Table.ExpandTableColumn`.

**1.5 — Star schema em vez de snowflake** · 🟠
VertiPaq é otimizado para estrela; cadeias de dimensão pioram compressão e consulta.
Como: achate Categoria → Subcategoria → Produto numa só dimensão no Power Query.
❌ `Fato → Produto → Subcategoria → Categoria` · ✅ `Fato → DimProduto (todas as colunas)`

**1.6 — Tabela de datas dedicada** · 🟠
Sem ela, funções de inteligência temporal falham ou dão resultado inconsistente.
Como: `CALENDAR()`/`CALENDARAUTO()` ou tabela importada, cobrindo todo o período, sem lacunas.
```dax
Calendario = CALENDAR ( DATE ( 2020, 1, 1 ), DATE ( 2026, 12, 31 ) )
```

**1.7 — Marque o calendário como Tabela de Datas** · 🟠
Sem a marcação, `TOTALYTD`, `DATEADD` e afins podem se comportar de forma inconsistente.
Como: botão direito → Marcar como tabela de datas; a coluna de data sem nulos nem duplicados.

**1.8 — Desabilite a data/hora automática** · 🟠
Cada coluna de data ganha uma tabela oculta; 10 colunas = 10 tabelas inúteis.
Como: Arquivo → Opções → Arquivo Atual → Carregamento de Dados → desmarque "Data/hora automática".

**1.9 — Evite excesso de bidirecionais ou M:M** · 🟠
Mais caminhos de filtro = consultas lentas e resultados inesperados.
Como: elimine bidirecionais desnecessários; use tabela ponte; `CROSSFILTER` pontual.

**1.10 — Minimize transformação complexa no Power Query** · 🟠
Parsing de JSON/XML, recursão e merges aninhados rodam a cada refresh.
Como: leve para a fonte (SQL, Data Factory); prefira funções nativas a iterações. Ver skill `power-query-m`.

**1.11 — M:M unidirecional** · 🟠
Bidirecional em M:M gera loops de filtro e resultado duplicado.
Como: relacionamento Single; `CROSSFILTER` só onde precisa.

**1.12 — Reduza tabelas calculadas** · 🟠
São recalculadas depois de todas as outras a cada refresh.
Como: crie no Power Query; reserve DAX para calendário, parâmetros e agrupamentos pequenos.

**1.13 — Reduza texto longo de alta cardinalidade** · 🟠
Descrições e URLs únicas comprimem mal e podem pesar mais que todo o resto.
Como: remova o que não é analisado; se precisar, trunque com `Text.Start`.

**1.14 — Separe data e hora** · 🟠
3 anos de data ≈ 1.095 valores; com hora ao minuto ≈ 1,5 milhão.
Como: `Date.From([DataHora])` e `Time.From([DataHora])`; relacione pela data.

**1.15 — Particione tabelas grandes** · 🟠
Sem partição, todo refresh recarrega a tabela inteira.
Como: configure Incremental Refresh (Pro, PPU, Premium e Embedded). Ver skill `power-query-m`.

**1.16 — Simplifique o RLS** · 🟠
A regra de RLS é avaliada em toda consulta; condições caras multiplicam o custo.
Como: tabela de segurança dedicada com relacionamento simples; atributos de segurança desnormalizados na fato quando der.
```dax
[Regiao] = LOOKUPVALUE ( Usuarios[Regiao], Usuarios[Email], USERPRINCIPALNAME () )
```

**1.17 — Agregações com DirectQuery** · 🔵
Sem agregação, cada interação vai ao banco.
Como: tabela de agregação Import em grão maior (dia/produto) vinculada à fato DirectQuery.

**1.18 — M:M em tabela com RLS dinâmico** · 🔴
A segurança resolvida por vários caminhos pode levar a consulta de milissegundos para minutos.
Como: relacionamento 1:N entre a tabela com RLS e a fato; se M:M for inevitável, aplique RLS na fato.

**1.19 — Despivote colunas** · 🟠
Meses como colunas travam a análise e obrigam uma medida por coluna.
Como: Transformar → Transformar Colunas em Linhas.
❌ `Jan, Fev, Mar (colunas)` · ✅ `Mês (coluna) + Valor (coluna)`

---

## Seção 2 — Expressões DAX

**2.1 — Medidas duplicadas** · 🟠
Manutenção em dois lugares e números que divergem.
Como: consolide numa medida; as outras referenciam ou saem.

**2.2 — Colunas calculadas duplicadas** · 🔵
Fonte: Measure Killer ("No two calculated columns should have the same definition").
Cada cópia ocupa memória.
Como: centralize, de preferência no Power Query.

**2.3 — `TREATAS` em vez de `INTERSECT`** · 🟠
`TREATAS` propaga filtro com índices; `INTERSECT` materializa tabelas.
❌ `CALCULATE ( [Vendas], INTERSECT ( VALUES ( Datas[Ano] ), VALUES ( Anos[Ano] ) ) )`
✅ `CALCULATE ( [Vendas], TREATAS ( VALUES ( Anos[Ano] ), Datas[Ano] ) )`

**2.4 — Use `DIVIDE`** · 🟠
Divisão por zero com `/` quebra o visual.
❌ `[Receita] / [Quantidade]` · ✅ `DIVIDE ( [Receita], [Quantidade] )`

**2.5 — Evite `IFERROR`** · 🟠
Mascara a causa e força avaliação extra.
Como: `DIVIDE` para divisão; `IF`/`COALESCE` explícitos para busca.
❌ `IFERROR ( [A] / [B], 0 )` · ✅ `DIVIDE ( [A], [B], 0 )`

**2.6 — Medida que só referencia outra** · 🟠
`[NovaVendas] = [Vendas]` é indireção sem ganho.
Como: use a original; para nome diferente, use sinônimo ou pasta de exibição.

**2.7 — Sintaxe de filtro por coluna** · 🟠
Predicado direto usa o índice; `FILTER` itera linha a linha.
❌ `CALCULATE ( [Vendas], FILTER ( ALL ( Produtos ), Produtos[Categoria] = "A" ) )`
✅ `CALCULATE ( [Vendas], Produtos[Categoria] = "A" )`
⚠️ Não são idênticas: `ALL ( Produtos )` remove filtros de **todas** as colunas de Produtos. A forma direta remove só o filtro de `Categoria`. Confira se a remoção extra era intencional.

**2.8 — Filtre por coluna, não pela tabela** · 🟠
Filtro de tabela inteira não aproveita índice de coluna.
❌ `CALCULATE ( [Vendas], FILTER ( Clientes, Clientes[Tipo] = "VIP" ) )`
✅ `CALCULATE ( [Vendas], Clientes[Tipo] = "VIP" )`

**2.9 — Relacionamento inativo nunca ativado** · 🟠
Ocupa metadado e confunde.
Como: se nenhuma medida usa `USERELATIONSHIP` nele, exclua.

**2.10 — Evite `1 - (x/y)` em margem** · 🟠
Pouco legível e não trata zero.
❌ `1 - [Custo] / [Receita]`
✅
```dax
Margem (%) =
VAR vMargem = DIVIDE ( [Receita] - [Custo], [Receita] )
RETURN vMargem
```

**2.11 — Remova `EVALUATEANDLOG` em produção** · 🔵
Função de debug: pesa na performance e gera log massivo.

---

## Seção 3 — Prevenção de erros

**3.1 — Coluna de dados com coluna de origem** · 🔴
Coluna órfã funciona no Desktop e falha no refresh do Service.

**3.2 — Objeto com expressão definida** · 🔴
Expressão vazia ou inválida impede publicação ou quebra em execução.
Como: no Tabular Editor, liste medidas e colunas calculadas e corrija as vazias.

**3.3 — `USERELATIONSHIP` e RLS na mesma tabela** · 🔴
O RLS pode não ser aplicado quando o relacionamento é trocado: brecha ou número errado.
Como: separe as responsabilidades ou reestruture para não precisar de `USERELATIONSHIP` ali.

**3.4 — Mesmo tipo nas colunas de relacionamento** · 🔴
Tipos diferentes impedem o relacionamento ou forçam conversão cara.
Como: padronize no Power Query; prefira inteiro.

**3.5 — Caractere inválido em nome** · 🔴
Aspas, colchetes, tabs e quebras de linha quebram expressões e integrações.
Como: só letras, números, espaço e underscore.

**3.6 — Caractere inválido em descrição** · 🔴
Caractere de controle corrompe serialização e documentação.
Como: texto simples; cuidado ao colar de fontes com formatação oculta.

**3.7 — `IsAvailableInMdx = true` em coluna necessária para MDX** · 🔴
Sem isso, a coluna some da tabela dinâmica do Excel (Analisar no Excel).

**3.8 — Partição de provedor (legado)** · 🟠
Pode não dobrar consulta e se comportar diferente no Service.
Como: converta para partição M com conector nativo.

**3.9 — RLS dinâmico é mesmo necessário?** · 🔵
Adiciona complexidade e custo.
Como: avalie RLS estático, relatórios separados ou workspaces diferentes.

**3.10 — Integridade referencial** · 🟠
FK sem correspondente vira "(Em branco)" e distorce totais.
Como: registro "Não informado" na dimensão ou limpeza na fonte.

---

## Seção 4 — Manutenção

**4.1 — Remova colunas não usadas** · 🟠 — memória, refresh e custo de capacidade.
Como: DAX Studio (View Metrics) ou BPA; remova no Power Query.

**4.2 — Remova medidas não usadas** · 🟠 — poluem o modelo.
Como: identifique no Tabular Editor e revise com o time antes de excluir.

**4.3 — Toda tabela com ao menos um relacionamento** · 🔵
Tabela ilha não é filtrada pelas outras. Se for tabela de parâmetro, documente.

**4.4 — Descrição em todo objeto visível** · 🔵
Aparece como tooltip e melhora o Copilot. Ver descrição com `///` na skill `bi-qa-documentacao`.

**4.5 — Grupo de cálculo sem item** · 🟠 — trabalho incompleto; complete ou exclua.

**4.6 — Fonte de dados sem partição** · 🔵 — conexão órfã, pode guardar credencial velha.

**4.7 — Role sem membro** · 🔵 — segurança que não protege ninguém.

**4.8 — Perspectiva vazia** · 🔵 — confunde quem a seleciona.

---

## Seção 5 — Nomenclatura

**5.1 — Caracteres especiais em nomes** · 🟠
Quebram expressões, URLs de API e exportações.
❌ `Vendas ($)` · ✅ `Vendas em Reais`

**5.2 — Espaço no início ou fim do nome** · 🔵
`" Vendas"` não é encontrada ao buscar `Vendas`.
Como: `Text.Trim` no Power Query; localizar e substituir no Tabular Editor.

Padrão completo: skill `bi-nomenclatura`.

---

## Seção 6 — Formatação

**6.1 — Format string em toda medida** · 🔴
Sem formato, decimais excessivos e sem separador de milhar.
Como: defina a **propriedade** Formato (Ferramentas de Medida → Formato, ou `formatString` no TMDL). Não use `FORMAT()` dentro da medida: ele devolve texto, quebra ordenação, soma e eixo.
```tmdl
measure 'Total de Vendas' = SUM ( Vendas[Valor da Venda] )
    formatString: R$ #,##0.00
```

**6.2 — Desabilite sumarização automática em numérico que não é métrica** · 🔴
Somar ID ou ano gera "totais" absurdos.
Como: `Summarization = None` (`summarizeBy: none` no TMDL).

**6.3 — Percentual com uma casa** · 🟠 — `0.0%`. O Power BI multiplica por 100.

**6.4 — Inteiro com milhar e sem decimal** · 🟠 — `#,##0`. Ajuste a localidade do modelo.

**6.5 — Inteiro em coluna de relacionamento** · 🔵 — chave texto é maior e compara mais devagar. Crie chave substituta.

**6.6 — Oculte FK** · 🟠 — `isHidden`; continua funcionando no relacionamento.

**6.7 — Marque chave primária** · 🔵 — `isKey`; documenta e ajuda o motor.

**6.8 — Maiúscula no início do nome** · 🔵
❌ `total vendas mensal` · ✅ `Total Vendas Mensal`

**6.9 — Flag como "Sim/Não"** · 🔵
0/1 confunde em segmentação. Trate no Power Query ou:
```dax
Ativo (Sim/Não) = IF ( [Ativo] = 1, "Sim", "Não" )
```

**6.10 — Formato de data** · 🔵 — `dd/MM/yyyy` no Brasil; configure a localidade do modelo.

**6.11 — Formato de mês** · 🔵 — padronize (Janeiro, Jan ou 01).

**6.12 — Oculte colunas da fato** · 🟠
Arrastar coluna de fato gera agregação errada (soma de média).
Como: oculte e exponha medidas explícitas.

**6.13 — Ordenação do mês em texto** · 🟠
Ordem alfabética põe Abril antes de Janeiro.
Como: coluna numérica 1–12 e "Classificar por coluna".

---

## Seção 7 — Relatórios e visuais

Fonte: regras base do PBI-Inspector (7.1 a 7.11) e extensões do Measure
Killer (7.12 a 7.14). Entre colchetes, o nome da regra na ferramenta.

**7.1 [Relatório] — Limite o total de páginas** · 🟠 · `REDUCE_PAGES`
Máximo 10 páginas. Consolide com indicadores, detalhamento ou navegação por
botões; relatórios separados por audiência.

**7.2 [Página] — Limite visuais por página** · 🔴 · `REDUCE_VISUALS_ON_PAGE`
Cada visual dispara consultas. Máximo 20 visuais visíveis: é teto de
desempenho; para leitura, menos costuma ser melhor (Seção 8). Detalhe em
drill-through ou tooltip.

**7.3 [Página] — Reduza filtros TopN** · 🔵 · `REDUCE_TOPN_FILTERS`
Máximo 4 visuais com TopN por página; ordenam tudo antes de filtrar.

**7.4 [Página] — Reduza filtros avançados** · 🔵 · `REDUCE_ADVANCED_FILTERS`
Máximo 4 visuais com filtro avançado por página; avaliados a cada interação.

**7.5 [Página] — Oculte páginas de tooltip e drill-through** · 🔵 · `HIDE_TOOLTIP_DRILLTROUGH_PAGES`
Botão direito na aba → Ocultar página. Continuam funcionando.

**7.6 [Página] — Sem rolagem vertical** · 🔴 · `ENSURE_PAGES_DO_NOT_SCROLL_VERTICALLY`
O que fica abaixo da dobra é ignorado. Página padrão Full HD (1920 × 1080):
tudo cabe em 1080 px. O PBI-Inspector e o Measure Killer verificam 720 px
(HD); em relatório Full HD, ajuste `paramMaxAllowedPageHeight` para 1080 ou
desconsidere o alerta. Use navegação, detalhamento ou mais páginas.

**7.7 [Visuais] — Remova visuais personalizados não usados** · 🔵 · `REMOVE_UNUSED_CUSTOM_VISUALS`
Visualizações → ⋯ → Gerenciar visuais.

**7.8 [Visuais] — Limite os campos em cada visual** · 🔴 · `REDUCE_OBJECTS_WITHIN_VISUALS`
"Objeto" é cada campo colocado no visual (eixo, legenda, valores, dicas).
Máximo 6. Divida o visual, mova contexto para tooltip page e use drill-down.

**7.9 [Visuais] — Evite "Mostrar itens sem dados"** · 🟠 · `AVOID_SHOW_ITEMS_WITH_NO_DATA`
Gera combinações vazias em massa.

**7.10 [Visuais] — Cores do tema, não HEX avulso** · 🔵 · `ENSURE_THEME_COLOURS`
Cor avulsa não acompanha troca de tema. Única regra que o PBI-Inspector marca
como erro, e não como aviso.

**7.11 [Visuais] — Texto alternativo** · 🟠 · `ENSURE_ALTTEXT`
Formatar → Geral → Texto alternativo; descreva o insight, não o tipo de
gráfico. Vem desligada por padrão no PBI-Inspector.

**7.12 [Visuais] — Pizza e rosca com moderação** · 🔵 · Measure Killer
Limite recomendado: até 4 fatias; acima disso, barras horizontais ordenadas.

**7.13 [Visuais] — Evite medidas implícitas** · 🔴 · Measure Killer
Não têm formato nem descrição.
Como: ative a propriedade **Desestimular medidas implícitas** do modelo (Model Explorer → modelo → Propriedades; no Tabular Editor, `DiscourageImplicitMeasures = true`) e crie medidas explícitas.
❌ arrastar `Fato[Valor]` · ✅ `Total de Vendas = SUM ( Fato[Valor] )`

**7.14 [Relatório] — Limite os indicadores** · 🔵 · Measure Killer
Máximo 10 indicadores (bookmarks). Prefira navegador de páginas, parâmetros de
campo e seletores de visual; apague indicadores sem uso.
❌ um indicador por combinação de filtro · ✅ parâmetro de campo que troca a métrica

---

## Seção 8 — Storytelling e comunicação (revisão manual)

Fonte: *Storytelling with Data*, de Cole Nussbaumer Knaflic (Wiley, 2015); a
8.9 vem de Stephen Few. Nenhuma ferramenta verifica nem pontua estas regras.
Detalhe e método na skill `data-storytelling`.

**8.1 — Defina a ideia central da página antes dos visuais** · 🔴
Uma frase com a conclusão. Teste dos 3 segundos: a conclusão aparece sem explicação?
❌ "Visão Geral" com 15 visuais soltos · ✅ "Margem caiu por causa do frete no Nordeste", com 4 visuais que sustentam a frase

**8.2 — Título diz a conclusão, não só o assunto** · 🔴
Use título dinâmico com medida DAX quando o dado muda com o filtro.
❌ "Vendas por Região" · ✅ "Sul superou a meta; Norte caiu 12%"

**8.3 — Escolha o visual pela comparação que importa** · 🟠
Valor exato: tabela ou cartão. Tendência: linha. Comparação: barras ordenadas.
Composição: barra 100% empilhada. Relação: dispersão.

**8.4 — Elimine a saturação visual** · 🟠
Sem bordas, sombras e grades que não informam. Rótulo de dado ligado → eixo de valores desligado.

**8.5 — Rótulo direto em vez de legenda** · 🔵
Nome da série na ponta da linha ou na barra.

**8.6 — Cinza como base, cor só para destacar** · 🟠
Complementa a 7.10: o tema dá consistência, esta regra dá foco. Uma ou duas cores de destaque por página.

**8.7 — Um destaque por vez** · 🟠
Cor, tamanho, negrito ou posição apontam para um único ponto.

**8.8 — Evite eixo duplo sem necessidade** · 🔵
Dois visuais alinhados com o mesmo eixo de tempo, ou índice base 100.

**8.9 — KPI ou barra no lugar de medidor** · 🔵 · Stephen Few
Visual KPI (valor, meta, tendência) ou bullet chart.

**8.10 — Leitura em Z** · 🔵
Dado principal no canto superior esquerdo; elementos alinhados a uma grade e agrupados por tema.

**8.11 — A sequência de páginas conta uma história** · 🟠
Lidos em ordem, só os títulos das páginas formam uma narrativa.

**8.12 — Densidade conforme o modo de uso** · 🔵
Leitura autônoma: títulos-conclusão e anotações. Apresentação: revelar aos poucos.

**8.13 — Rascunhe antes de abrir o Power BI** · 🔵
Storyboard com uma caixa por página, título-conclusão e ordem; valide com o público.
