# Visuais gerados por medida DAX (SVG e HTML)

Técnica avançada, depois de esgotar o nativo: sparkline dentro de célula, barra
de progresso em cartão, landing page no topo do relatório.

**Regra da casa:** visual nativo primeiro para análise. Se formatação condicional ou KPI
nativo resolvem, use o nativo: é mais leve, mais acessível e sem risco de locale.
**Exceção que é o padrão:** cena de storytelling em que posição, preenchimento ou quantidade
mudam com o filtro é SVG por medida (`data-storytelling`;
exemplo completo em `references/cena-svg-exemplo.md`).

---

## A. Imagem SVG por medida

Medida que retorna um data URI (`data:image/svg+xml;utf8,<svg>...</svg>`),
exibida em tabela, matriz, cartão ou botão com **Categoria de Dados = URL da
Imagem** (Ferramentas de Medida → Categoria de dados).

**Usos:** cena de storytelling, sparkline por linha, barra de progresso, bullet chart,
semáforo com forma que o ícone nativo não tem.

No **cartão**, a seção *Image* aceita a medida como origem, e o estado *Hover* aceita outra
medida (variação ao passar o mouse).
[Visual de cartão](https://learn.microsoft.com/power-bi/visuals/power-bi-visualization-card)

### ⚠️ Armadilha 1 — locale pt-BR

`FORMAT()` e a conversão implícita respeitam a localidade. Em pt-BR sai vírgula
decimal, e atributos de SVG (`width`, `x`, `d`, `points`) **exigem ponto**. Um
`width='62,3'` quebra a imagem em silêncio. Force o ponto sempre. O exemplo de cartão da
Microsoft usa `FORMAT` sem essa troca num modelo `en-US`: copiado para um modelo em pt-BR,
ajuste antes.

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

Pressupõe `[Índice Mês]` (1 a 12 na janela) e `[Receita Máxima (12M)]`.

```dax
Sparkline 12M =
VAR vMaximo = [Receita Máxima (12M)]
VAR vPontos =
    CONCATENATEX (
        VALUES ( 'Calendário'[Mês e Ano] ),
        VAR vX = ( [Índice Mês] - 1 ) * 15
        VAR vY = 40 - DIVIDE ( [Receita], vMaximo, 0 ) * 40
        RETURN
            SUBSTITUTE ( FORMAT ( vX, "0.0" ), ",", "." ) & ","
                & SUBSTITUTE ( FORMAT ( vY, "0.0" ), ",", "." ),
        " ",
        'Calendário'[Mês e Ano], ASC
    )
RETURN
    "data:image/svg+xml;utf8,"
        & "<svg xmlns='http://www.w3.org/2000/svg' width='165' height='40'>"
        & "<polyline points='" & vPontos & "' fill='none' stroke='%232B579A' stroke-width='2'/>"
        & "</svg>"
```

⚠️ Ordene por uma coluna que ordene de fato no tempo. Se `Mês e Ano` for texto
("jan/2026"), use a coluna numérica de ordenação no argumento de ordem.

### Checklist SVG
- [ ] Categoria de Dados = URL da Imagem
- [ ] Todo número em atributo passou por `SUBSTITUTE(..., ",", ".")`
- [ ] `#` escapado como `%23`
- [ ] Testado com o relatório em pt-BR, não só na sua máquina
- [ ] Testado com nulo e zero
- [ ] Custo avaliado: SVG por linha em tabela com mais de ~1.000 linhas visíveis pesa
- [ ] Tamanho conferido (`EVALUATE ROW ( "Tamanho", LEN ( [Medida] ) )`) abaixo de 32.766
- [ ] Texto alternativo e versão legível dos dados na página
- [ ] `checar_svg.py` sem erros (skill `bi-qa-documentacao`)

[Categoria de dados URL da Imagem](https://learn.microsoft.com/pt-br/power-bi/create-reports/desktop-image-title-column) ·
[Especificação SVG (W3C)](https://www.w3.org/TR/SVG2/) ·
[Visual de imagem](https://learn.microsoft.com/power-bi/visuals/power-bi-visualization-image-visual) ·
[Funções DAX do usuário](https://learn.microsoft.com/dax/best-practices/dax-user-defined-functions)

---

### Infográfico inteiro num visual de imagem [verificado]
- Visual `image` com `objects.image` em `sourceType 'imageData'` e `sourceField` =
  medida `dataCategory: ImageUrl`. A imagem reage aos filtros da página; não tem dica.
- No data URI, **`%` vira `%25`** (inclusive em textos como "131% do ritmo"); acento e
  símbolos como ▲ funcionam em `utf8`.
- **Texto alternativo por medida** (`general.altText.expr.Measure`) com os mesmos
  números da imagem.
- Trate os estados: sem realizado, sem meta, acima de 100%, filtro que zera a meta.
- Desenho repetido (personagem, ícone) sai de **um módulo gerador**, usado no esboço e
  na medida. Para conferir sem abrir o Desktop, extraia as cadeias da própria medida e
  renderize no Edge.

### Reuso: funções DAX do usuário
Peça usada em **duas ou mais medidas** vira função (`Svg.Peca`; nível de compatibilidade
1702, disponibilidade geral em jun/2026; skill `dax-udf`). Cena única fica numa medida só, e a
peça repetida dentro dela (roda, árvore) é desenhada uma vez numa `VAR` e posicionada com
`<g transform>`.

A [DaxLib.SVG](https://github.com/EvaluationContext/daxlib.svg) (licença MIT) traz funções
prontas para formas e mini-gráficos; é dependência **opcional**. A versão 2.0.0 tem mudanças
incompatíveis com a 1.x (ordem dos parâmetros): confira antes de atualizar.

### Tamanho do resultado
Mantenha a imagem **abaixo de 32.766 caracteres**. É precaução da casa: o
[limite publicado em 2019](https://blog.crossjoin.co.uk/2019/05/17/maximum-length-text-value-power-bi/)
vale para texto **carregado no modelo**, que é cortado sem aviso; para medida exibida em
visual ele não está confirmado.

### Acessibilidade da cena
Texto alternativo em duas partes
([imagens complexas, W3C](https://www.w3.org/WAI/tutorials/images/complex/)):
1. **curto**, no texto alternativo do visual, por medida: identifica a cena e traz os números;
2. **longo**, os mesmos dados legíveis na própria página (cartão, tabela ou gráfico nativo).

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
- Não dá para oferecer o texto alternativo e a versão legível dos dados: o leitor de tela
  não lê o conteúdo desenhado na imagem.
