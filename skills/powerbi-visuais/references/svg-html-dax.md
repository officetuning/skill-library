# Visuais gerados por medida DAX (SVG e HTML)

Técnica avançada, depois de esgotar o nativo: sparkline dentro de célula, barra
de progresso em cartão, landing page no topo do relatório.

**Regra da casa:** visual nativo primeiro. Se formatação condicional ou KPI
nativo resolvem, use o nativo: é mais leve, mais acessível e sem risco de locale.

---

## A. Imagem SVG por medida

Medida que retorna um data URI (`data:image/svg+xml;utf8,<svg>...</svg>`),
exibida em tabela, matriz, cartão ou botão com **Categoria de Dados = URL da
Imagem** (Ferramentas de Medida → Categoria de dados).

**Usos:** sparkline por linha, barra de progresso, bullet chart, semáforo com
forma que o ícone nativo não tem.

### ⚠️ Armadilha 1 — locale pt-BR

`FORMAT()` e a conversão implícita respeitam a localidade. Em pt-BR sai vírgula
decimal, e atributos de SVG (`width`, `x`, `d`, `points`) **exigem ponto**. Um
`width='62,3'` quebra a imagem em silêncio. Force o ponto sempre:

```dax
-- ❌ Risco em pt-BR: pode gerar width='62,3'
Barra Progresso (RISCO) =
VAR vPercentual = DIVIDE ( [Receita Realizada], [Meta Receita] )
VAR vLargura = vPercentual * 200
RETURN
    "data:image/svg+xml;utf8,"
        & "<svg xmlns='http://www.w3.org/2000/svg' width='200' height='20'>"
        & "<rect width='200' height='20' fill='%23E5E7EB'/>"
        & "<rect width='" & vLargura & "' height='20' fill='%232B579A'/>"
        & "</svg>"

-- ✔️ Correto: ponto forçado e largura limitada a 0–200
Barra Progresso =
VAR vPercentual = DIVIDE ( [Receita Realizada], [Meta Receita], 0 )
VAR vLargura = MIN ( MAX ( vPercentual, 0 ), 1 ) * 200
VAR vLarguraTexto = SUBSTITUTE ( FORMAT ( vLargura, "0.00" ), ",", "." )
RETURN
    "data:image/svg+xml;utf8,"
        & "<svg xmlns='http://www.w3.org/2000/svg' width='200' height='20'>"
        & "<rect width='200' height='20' rx='3' fill='%23E5E7EB'/>"
        & "<rect width='" & vLarguraTexto & "' height='20' rx='3' fill='%232B579A'/>"
        & "</svg>"
```

### ⚠️ Armadilha 2 — caracteres reservados de URL

`#`, `%`, `<`, `>` e `"` quebram o data URI. Use aspas simples nos atributos e
`%23` no lugar de `#` nas cores (como acima). Alternativa mais robusta e mais
trabalhosa em DAX: `data:image/svg+xml;base64,`.

### Sparkline 12 meses

Pressupõe `[Índice Mês]` (1 a 12 na janela) e `[Receita Máxima 12M]`.

```dax
Sparkline 12M =
VAR vMaximo = [Receita Máxima 12M]
VAR vPontos =
    CONCATENATEX (
        VALUES ( 'Calendário'[MêsAno] ),
        VAR vX = ( [Índice Mês] - 1 ) * 15
        VAR vY = 40 - DIVIDE ( [Receita Total], vMaximo, 0 ) * 40
        RETURN
            SUBSTITUTE ( FORMAT ( vX, "0.0" ), ",", "." ) & ","
                & SUBSTITUTE ( FORMAT ( vY, "0.0" ), ",", "." ),
        " ",
        'Calendário'[MêsAno], ASC
    )
RETURN
    "data:image/svg+xml;utf8,"
        & "<svg xmlns='http://www.w3.org/2000/svg' width='165' height='40'>"
        & "<polyline points='" & vPontos & "' fill='none' stroke='%232B579A' stroke-width='2'/>"
        & "</svg>"
```

⚠️ Ordene por uma coluna que ordene de fato no tempo. Se `MêsAno` for texto
("jan/2026"), use a coluna numérica de ordenação no argumento de ordem.

### Checklist SVG
- [ ] Categoria de Dados = URL da Imagem
- [ ] Todo número em atributo passou por `SUBSTITUTE(..., ",", ".")`
- [ ] `#` escapado como `%23`
- [ ] Testado com o relatório em pt-BR, não só na sua máquina
- [ ] Testado com nulo e zero
- [ ] Custo avaliado: SVG por linha em tabela com mais de ~1.000 linhas visíveis pesa

[Categoria de dados URL da Imagem](https://learn.microsoft.com/pt-br/power-bi/create-reports/desktop-image-title-column) ·
[Especificação SVG (W3C)](https://www.w3.org/TR/SVG2/)

---

## B. HTML por medida (visual de terceiros)

Um visual do AppSource (ex.: "HTML Content") renderiza a string HTML/CSS da
medida. **Não executa JavaScript**: só HTML e CSS inline. Não há página oficial
Microsoft para esse visual; consulte a documentação do visual escolhido no
[AppSource](https://appsource.microsoft.com/pt-br/marketplace/apps?product=power-bi-visuals).

**Usos:** hero card no topo, grid "bento" de KPIs, calendário de calor,
narrativa condicional determinística.

### ⚠️ HTML aparece como texto cru
1. O visual é o de HTML, não um Cartão comum?
2. A medida está no campo certo do visual?
3. Há aspas duplas quebrando a string DAX?

### Narrativa condicional

```dax
Narrativa Meta HTML =
VAR vPercentual = DIVIDE ( [Receita Realizada], [Meta Receita] )
VAR vCor =
    SWITCH ( TRUE (), vPercentual >= 1, "#27AE60", vPercentual >= 0.9, "#F4A321", "#C0392B" )
VAR vTexto =
    SWITCH ( TRUE (), vPercentual >= 1, "Meta batida", vPercentual >= 0.9, "Perto da meta", "Abaixo da meta" )
RETURN
    "<div style='font-family:Segoe UI;padding:12px;'>"
        & "<span style='color:" & vCor & ";font-size:24px;font-weight:600;'>"
        & FORMAT ( vPercentual, "0%" )
        & "</span><br/>"
        & "<span style='color:#6B7280;font-size:13px;'>" & vTexto & "</span>"
        & "</div>"
```

Regra de design: se o layout pede mais de ~15 linhas de CSS inline, uma página
com visuais nativos em grade provavelmente resolve melhor.

---

## Quando NÃO usar SVG/HTML
- KPI, cartão ou formatação condicional nativos já resolvem.
- Tabela ou matriz com muitas linhas visíveis.
- O time que mantém não lê DAX concatenado com string.
- Acessibilidade é requisito formal: leitor de tela interpreta mal SVG/HTML embutido.
