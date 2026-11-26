# Exemplo completo: caminhão até a meta

Cena em SVG por medida, com **dados fictícios**. É referência de estrutura: cada
relatório escolhe a própria analogia (`data-storytelling`), não copia este desenho.

## O que a cena responde
"As entregas chegaram à meta?" Quem olha cinco segundos vê o caminhão antes, em cima
ou depois da bandeira, sem precisar de legenda. Sem meta, a bandeira some; sem linha
no contexto, sobra a estrada.

## Por que continua verdadeira com qualquer filtro
O percentual compara **só as entregas das regiões que têm meta** com a soma das metas.
Somar as entregas de uma região sem meta empurraria o caminhão para a frente sem que a
meta tivesse crescido. A posição para em 120% para o caminhão não sair da imagem; o
rótulo mostra o valor real.

## Script (TMDL view, relatório em branco)

```tmdl
createOrReplace

	table Entregas

		/// Pedidos entregues no contexto.
		measure Entregues = SUM ( 'Entregas'[Pedidos Entregues] )
			formatString: #,0
			displayFolder: Storytelling

		/// Meta de pedidos no contexto.
		measure Meta = SUM ( 'Entregas'[Meta de Pedidos] )
			formatString: #,0
			displayFolder: Storytelling

		/// Pedidos entregues apenas nas regiões que têm meta.
		measure 'Entregues com Meta' =
				SUMX (
				    FILTER ( VALUES ( 'Entregas'[Região] ), NOT ISBLANK ( [Meta] ) ),
				    [Entregues]
				)
			formatString: #,0
			displayFolder: Storytelling

		/// Entregues com meta sobre a meta; vazio quando nada no contexto tem meta.
		measure 'Atingimento (%)' =
				IF ( [Meta] > 0, DIVIDE ( COALESCE ( [Entregues com Meta], 0 ), [Meta] ) )
			formatString: 0%
			displayFolder: Storytelling

		/// Cena: caminhão na estrada até a bandeira da meta (SVG 720 x 200).
		measure 'Caminhão até a Meta' = ```
				VAR vTemDado = NOT ISEMPTY ( 'Entregas' )
				VAR vPercentual = [Atingimento (%)]
				VAR vTemMeta = NOT ISBLANK ( vPercentual )
				-- estrada: 40 = início, 560 = meta (100%), teto em 120%
				VAR vXCaminhao = 40 + MIN ( MAX ( COALESCE ( vPercentual, 0 ), 0 ), 1.2 ) * 520
				VAR vXTexto = SUBSTITUTE ( FORMAT ( vXCaminhao, "0.0" ), ",", "." )
				VAR vBandeira =
				    IF (
				        vTemMeta,
				        "<rect x='558' y='58' width='4' height='90' rx='2' fill='%236B7280'/>"
				            & "<rect x='562' y='60' width='36' height='24' fill='%23FFFFFF' stroke='%23111827'/>"
				            & "<path d='M562 60h9v8h-9z M580 60h9v8h-9z M571 68h9v8h-9z M589 68h9v8h-9z M562 76h9v8h-9z M580 76h9v8h-9z' fill='%23111827'/>"
				            & "<text x='560' y='190' text-anchor='middle' font-family='Segoe UI' font-size='13' fill='%236B7280'>meta</text>",
				        ""
				    )
				VAR vCaminhao =
				    IF (
				        vTemDado,
				        "<g transform='translate(" & vXTexto & " 0)'>"
				            & "<ellipse cx='0' cy='153' rx='40' ry='5' fill='%23000000' fill-opacity='0.18'/>"
				            & "<rect x='-40' y='134' width='82' height='6' rx='2' fill='%23374151'/>"
				            & "<rect x='-40' y='94' width='50' height='42' rx='4' fill='%232563EB'/>"
				            & "<rect x='-40' y='94' width='50' height='9' rx='4' fill='%2360A5FA'/>"
				            & "<rect x='-32' y='114' width='34' height='5' rx='2' fill='%23FFFFFF' fill-opacity='0.85'/>"
				            & "<path d='M13 108h15q4 0 6 3l8 13v12H13z' fill='%231E40AF'/>"
				            & "<path d='M18 112h10l7 11H18z' fill='%23DBEAFE'/>"
				            & "<rect x='39' y='129' width='5' height='7' rx='2' fill='%239CA3AF'/>"
				            & "<circle cx='-24' cy='141' r='10' fill='%23111827'/><circle cx='-24' cy='141' r='4' fill='%23D1D5DB'/>"
				            & "<circle cx='27' cy='141' r='10' fill='%23111827'/><circle cx='27' cy='141' r='4' fill='%23D1D5DB'/>"
				            & "</g>",
				        ""
				    )
				VAR vRotulo =
				    SWITCH (
				        TRUE (),
				        NOT vTemDado, "Sem entregas no período",
				        NOT vTemMeta, FORMAT ( [Entregues], "#,0" ) & " pedidos, sem meta",
				        FORMAT ( COALESCE ( [Entregues com Meta], 0 ), "#,0" ) & " de "
				            & FORMAT ( [Meta], "#,0" ) & " pedidos ("
				            & FORMAT ( vPercentual * 100, "0" ) & "%25)"
				    )
				RETURN
				    "data:image/svg+xml;utf8,"
				        & "<svg xmlns='http://www.w3.org/2000/svg' width='720' height='200' viewBox='0 0 720 200'>"
				        & "<rect x='0' y='147' width='720' height='24' rx='4' fill='%234B5563'/>"
				        & "<line x1='28' y1='162' x2='700' y2='162' stroke='%23FFFFFF' stroke-width='2' stroke-dasharray='14 12'/>"
				        & "<text x='40' y='190' text-anchor='middle' font-family='Segoe UI' font-size='13' fill='%236B7280'>início</text>"
				        & vBandeira
				        & vCaminhao
				        & "<text x='360' y='34' text-anchor='middle' font-family='Segoe UI' font-size='22' font-weight='600' fill='%23111827'>"
				        & vRotulo
				        & "</text></svg>"
				```
			displayFolder: Storytelling
			dataCategory: ImageUrl

		/// Texto alternativo da cena, com os mesmos números da imagem.
		measure 'Caminhão (Texto Alternativo)' = ```
				SWITCH (
				    TRUE (),
				    ISEMPTY ( 'Entregas' ), "Estrada vazia: sem entregas no período.",
				    ISBLANK ( [Atingimento (%)] ),
				        "Caminhão no início da estrada, sem bandeira: "
				            & FORMAT ( [Entregues], "#,0" ) & " pedidos entregues, sem meta.",
				    "Caminhão na estrada até a bandeira da meta: "
				        & FORMAT ( COALESCE ( [Entregues com Meta], 0 ), "#,0" ) & " de "
				        & FORMAT ( [Meta], "#,0" ) & " pedidos, "
				        & FORMAT ( [Atingimento (%)], "0%" ) & " da meta."
				)
				```
			displayFolder: Storytelling

		column 'Região'
			summarizeBy: none
			isNameInferred
			sourceColumn: [Região]

		column 'Pedidos Entregues'
			formatString: #,0
			summarizeBy: sum
			isNameInferred
			sourceColumn: [Pedidos Entregues]

		column 'Meta de Pedidos'
			formatString: #,0
			summarizeBy: sum
			isNameInferred
			sourceColumn: [Meta de Pedidos]

		partition Entregas = calculated
			mode: import
			source = ```
					SELECTCOLUMNS (
					    {
					        ( "Sul", 82, 100 ),
					        ( "Norte", 124, 100 ),
					        ( "Leste", 60, BLANK () ),
					        ( "Oeste", BLANK (), 80 )
					    },
					    "Região", [Value1],
					    "Pedidos Entregues", [Value2],
					    "Meta de Pedidos", [Value3]
					)
					```
```

## Montar a página
1. **Visual de imagem** → Origem da imagem: *Selecionar nos dados* → `Caminhão até a Meta`;
   ajuste *Ajustar*; proporção 720 × 200 (ex.: 1440 × 400).
2. **Texto alternativo** do visual: botão *fx* → `Caminhão (Texto Alternativo)`.
3. **Segmentação** por `Região`.
4. **Descrição longa:** tabela nativa na mesma página com `Região`, `Pedidos Entregues`,
   `Meta de Pedidos`, `Entregues com Meta` e `Atingimento (%)`. É a versão legível dos dados
   da cena: o total de `Entregues com Meta` é o número da imagem (sem filtro, 206, e não as
   266 entregas de todas as regiões).
5. Cena pequena: no **visual de cartão**, seção *Image* com *Image source* = dados; o
   estado *Hover* aceita outra medida.

## Estados esperados
| Contexto | Cena | Rótulo |
|---|---|---|
| Sul | caminhão antes da bandeira | 82 de 100 pedidos (82%) |
| Norte | caminhão além da bandeira, parado em 120% | 124 de 100 pedidos (124%) |
| Leste | caminhão no início, sem bandeira | 60 pedidos, sem meta |
| Oeste | caminhão no início, com bandeira | 0 de 80 pedidos (0%) |
| Nenhuma linha (filtro de visual que não casa) | só a estrada | Sem entregas no período |
| Sem filtro | caminhão antes da bandeira | 206 de 280 pedidos (74%) |

## Conferir
```dax
EVALUATE ROW ( "Tamanho", LEN ( [Caminhão até a Meta] ) )
```
E `checar_svg.py` (skill `bi-qa-documentacao`) no modelo e no relatório.
