# Exemplo completo: caminhão até a meta

Cena em SVG por medida, com **dados fictícios**. É referência de estrutura: cada
relatório escolhe a própria analogia (`data-storytelling`), não copia este desenho.

## O que a cena responde
"As entregas chegaram à meta?" Quem olha cinco segundos vê o caminhão antes ou depois do
pórtico "META", sem precisar de legenda. A **frente** do caminhão marca o percentual, igual à
barra: só toca o pórtico quando a meta é alcançada. O balão dá o percentual e a situação por escrito, e a
barra de marcos mostra o avanço (25%, 50%, 75%, meta). Sem meta, somem o pórtico, a loja e a
barra; sem linha no contexto, sai também o caminhão.

A cena é completa de propósito: cenário com profundidade, veículo detalhado e indicador em
destaque, não só o objeto que se move. As peças repetidas (roda e árvore) são desenhadas uma
vez, numa `VAR`.

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

		/// Cena: caminhão na pista a caminho do pórtico da meta, com barra de marcos (SVG 960 x 320).
		measure 'Caminhão até a Meta' = ```
				VAR vTemDado = NOT ISEMPTY ( 'Entregas' )
				VAR vPercentual = [Atingimento (%)]
				VAR vTemMeta = NOT ISBLANK ( vPercentual )
				VAR vEntregues = COALESCE ( [Entregues com Meta], 0 )
				VAR vDiferenca = vEntregues - [Meta]
				-- abaixo de 100% o arredondamento para em 99, para não anunciar meta que falta
				VAR vInteiro =
				    IF ( vPercentual < 1, MIN ( ROUND ( vPercentual * 100, 0 ), 99 ), ROUND ( vPercentual * 100, 0 ) )
				VAR vSituacao =
				    SWITCH ( TRUE (), NOT vTemMeta, "neutro", vPercentual >= 1, "ok", "abaixo" )
				VAR vCorBorda = SWITCH ( vSituacao, "ok", "%2316A34A", "abaixo", "%23F59E0B", "%2394A3B8" )
				VAR vCorFundo = SWITCH ( vSituacao, "ok", "%23DCFCE7", "abaixo", "%23FEF3C7", "%23F1F5F9" )
				VAR vCorTexto = SWITCH ( vSituacao, "ok", "%23166534", "abaixo", "%2392400E", "%2364748B" )
				VAR vCorBarra = IF ( vSituacao = "ok", "%2322C55E", "%23FBBF24" )
				VAR vGrande =
				    SWITCH (
				        TRUE (),
				        NOT vTemDado, "—",
				        NOT vTemMeta, FORMAT ( [Entregues], "#,0" ),
				        FORMAT ( vInteiro, "0" ) & "%25"
				    )
				VAR vDetalhe =
				    SWITCH (
				        TRUE (),
				        NOT vTemDado, "Sem entregas no período",
				        NOT vTemMeta, "pedidos entregues",
				        FORMAT ( vEntregues, "#,0" ) & " de " & FORMAT ( [Meta], "#,0" ) & " pedidos"
				    )
				VAR vSelo =
				    SWITCH (
				        TRUE (),
				        NOT vTemDado, "nada a mostrar",
				        NOT vTemMeta, "sem meta definida",
				        vDiferenca = 0, "✔ meta atingida",
				        vDiferenca > 0, "✔ meta superada em " & FORMAT ( vDiferenca, "#,0" ),
				        vDiferenca = -1, "falta 1 pedido",
				        "faltam " & FORMAT ( - vDiferenca, "#,0" ) & " pedidos"
				    )
				-- pista: a FRENTE do caminhão marca o percentual: 230 = início, 720 = meta, teto em 120%
				VAR vXFrente = 230 + MIN ( MAX ( COALESCE ( vPercentual, 0 ), 0 ), 1.2 ) * 490
				-- o desenho avança 100 à frente do seu ponto de origem
				VAR vXCaminhao = vXFrente - 100
				VAR vXTexto = SUBSTITUTE ( FORMAT ( vXCaminhao, "0.0" ), ",", "." )
				VAR vLarguraTexto = SUBSTITUTE ( FORMAT ( vXFrente - 230, "0.0" ), ",", "." )
				-- peças repetidas, desenhadas na origem
				VAR vRoda =
				    "<circle cx='7' cy='-4' r='15' fill='%23020617' /><rect x='0' y='-15' width='7' height='4' rx='0' fill='%23020617' />"
				        & "<circle cx='0' cy='0' r='15' fill='%23111827' /><circle cx='0' cy='0' r='9.3' fill='url(%23aro)' /><circle cx='0' cy='0' r='3' fill='%23475569' />"
				        & "<circle cx='6' cy='0' r='1.6' fill='%23475569' /><circle cx='-6' cy='0' r='1.6' fill='%23475569' /><circle cx='0' cy='6' r='1.6' fill='%23475569' />"
				        & "<circle cx='0' cy='-6' r='1.6' fill='%23475569' />"
				VAR vArvore =
				    "<ellipse cx='7' cy='1' rx='20' ry='5' fill='%230F172A' opacity='0.14'/><rect x='-3' y='-16' width='6' height='17' rx='2' fill='%2392400E' />"
				        & "<circle cx='0' cy='-32' r='19' fill='url(%23copa)' /><circle cx='10' cy='-22' r='11' fill='url(%23copa)' />"
				-- camadas, na ordem de desenho
				VAR vDefs =
				    "<defs><linearGradient id='fundo' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='%23F8FAFC'/><stop offset='1' stop-color='%23E2E8F0'/>"
				        & "</linearGradient><linearGradient id='bF' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='%233B82F6'/>"
				        & "<stop offset='1' stop-color='%231D4ED8'/></linearGradient><linearGradient id='cF' x1='0' y1='0' x2='0' y2='1'>"
				        & "<stop offset='0' stop-color='%232563EB'/><stop offset='1' stop-color='%231E3A8A'/></linearGradient>"
				        & "<linearGradient id='vidroB' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='%23F0F9FF'/><stop offset='1' stop-color='%2338BDF8'/>"
				        & "</linearGradient><linearGradient id='grama' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='%23A7F3D0'/>"
				        & "<stop offset='1' stop-color='%236EE7B7'/></linearGradient><linearGradient id='aro' x1='0' y1='0' x2='0' y2='1'>"
				        & "<stop offset='0' stop-color='%23F8FAFC'/><stop offset='1' stop-color='%2394A3B8'/></linearGradient>"
				        & "<radialGradient id='copa' cx='0.35' cy='0.3' r='0.75'><stop offset='0' stop-color='%234ADE80'/><stop offset='1' stop-color='%23166534'/>"
				        & "</radialGradient></defs>"
				VAR vCenario =
				    "<rect x='0' y='0' width='960' height='320' rx='14' fill='url(%23fundo)' /><ellipse cx='486' cy='310' rx='466' ry='9' fill='%230F172A' opacity='0.10'/>"
				        & "<path d='M14 272l96-88h836l-70 88z' fill='url(%23grama)' /><path d='M14 272h862v30H14z' fill='%23334155' />"
				        & "<path d='M876 272l70-88v30l-70 88z' fill='%231E293B' /><path d='M98 202l50 -27.5h100l-50 27.5z' fill='%230F172A' opacity='0.10'/>"
				        & "<path d='M104 140l36 -19.8h100l-36 19.8z' fill='%23475569' /><path d='M204 140l36 -19.8v62l-36 19.8z' fill='%2394A3B8' />"
				        & "<rect x='104' y='140' width='100' height='62' rx='0' fill='%23E2E8F0' /><rect x='114' y='152' width='15' height='13' rx='2' fill='url(%23vidroB)' />"
				        & "<rect x='138' y='152' width='15' height='13' rx='2' fill='url(%23vidroB)' />"
				        & "<rect x='162' y='152' width='15' height='13' rx='2' fill='url(%23vidroB)' /><path d='M120 170l3 -1.65h32l-3 1.65z' fill='%2394A3B8' />"
				        & "<path d='M152 170l3 -1.65v32l-3 1.65z' fill='%23475569' /><rect x='120' y='170' width='32' height='32' rx='0' fill='%2364748B' />"
				        & "<rect x='120' y='178' width='32' height='2' rx='0' fill='%23334155' /><rect x='120' y='186' width='32' height='2' rx='0' fill='%23334155' />"
				        & "<rect x='120' y='194' width='32' height='2' rx='0' fill='%23334155' /><path d='M164 186l9 -4.95h18l-9 4.95z' fill='%23FBBF24' />"
				        & "<path d='M182 186l9 -4.95v16l-9 4.95z' fill='%2392400E' /><rect x='164' y='186' width='18' height='16' rx='0' fill='%23D97706' />"
				        & "<path d='M186 186l9 -4.95h18l-9 4.95z' fill='%23FBBF24' /><path d='M204 186l9 -4.95v16l-9 4.95z' fill='%2392400E' />"
				        & "<rect x='186' y='186' width='18' height='16' rx='0' fill='%23D97706' /><path d='M176 170l9 -4.95h18l-9 4.95z' fill='%23FCD34D' />"
				        & "<path d='M194 170l9 -4.95v16l-9 4.95z' fill='%23B45309' /><rect x='176' y='170' width='18' height='16' rx='0' fill='%23F59E0B' />"
				        & "<g transform='translate(262 204) scale(0.85)'>"
				        & vArvore
				        & "</g><g transform='translate(296 198) scale(0.65)'>"
				        & vArvore
				        & "</g><g transform='translate(640 202) scale(0.8)'>"
				        & vArvore
				        & "</g><g transform='translate(922 206) scale(0.8)'>"
				        & vArvore
				        & "</g><g transform='translate(40 246) scale(0.75)'>"
				        & vArvore
				        & "</g>"
				VAR vLoja =
				    IF (
				        vTemMeta,
				        "<path d='M780 202l46 -25.3h88l-46 25.3z' fill='%230F172A' opacity='0.10'/><path d='M786 142l32 -17.6h88l-32 17.6z' fill='%23B45309' />"
				            & "<path d='M874 142l32 -17.6v60l-32 17.6z' fill='%23D97706' /><rect x='786' y='142' width='88' height='60' rx='0' fill='%23FEF3C7' />"
				            & "<path d='M786 156h12.6v9a6.3 6.3 0 0 1-12.6 0z' fill='%23DC2626' /><path d='M798.6 156h12.6v9a6.3 6.3 0 0 1-12.6 0z' fill='%23FFFFFF' />"
				            & "<path d='M811.2 156h12.6v9a6.3 6.3 0 0 1-12.6 0z' fill='%23DC2626' /><path d='M823.8 156h12.6v9a6.3 6.3 0 0 1-12.6 0z' fill='%23FFFFFF' />"
				            & "<path d='M836.4 156h12.6v9a6.3 6.3 0 0 1-12.6 0z' fill='%23DC2626' /><path d='M849 156h12.6v9a6.3 6.3 0 0 1-12.6 0z' fill='%23FFFFFF' />"
				            & "<path d='M861.6 156h12.6v9a6.3 6.3 0 0 1-12.6 0z' fill='%23DC2626' /><rect x='794' y='176' width='34' height='20' rx='2' fill='url(%23vidroB)' />"
				            & "<rect x='842' y='174' width='22' height='28' rx='2' fill='%2392400E' />",
				        ""
				    )
				VAR vPista =
				    "<path d='M22 264l38-35h862l-30 35z' fill='%23475569' /><path d='M22 264h870v4H22z' fill='%231E293B' />"
				        & "<path d='M50 247h860' fill='none' stroke='%23FDE047' stroke-width='2.5' stroke-dasharray='22 16'/>"
				VAR vPortico =
				    IF (
				        vTemMeta,
				        "<path d='M720 264h8l7.6 -7h-8z' fill='%230F172A' /><path d='M727.6 257h8l7.6 -7h-8z' fill='%23FFFFFF' />"
				            & "<path d='M735.2 250h8l7.6 -7h-8z' fill='%230F172A' /><path d='M742.8 243h8l7.6 -7h-8z' fill='%23FFFFFF' />"
				            & "<path d='M750.4 236h8l7.6 -7h-8z' fill='%230F172A' /><path d='M728 264h8l7.6 -7h-8z' fill='%23FFFFFF' />"
				            & "<path d='M735.6 257h8l7.6 -7h-8z' fill='%230F172A' /><path d='M743.2 250h8l7.6 -7h-8z' fill='%23FFFFFF' />"
				            & "<path d='M750.8 243h8l7.6 -7h-8z' fill='%230F172A' /><path d='M758.4 236h8l7.6 -7h-8z' fill='%23FFFFFF' />"
				            & "<path d='M762 108l6 -3.3h7l-6 3.3z' fill='%2394A3B8' /><path d='M769 108l6 -3.3v122l-6 3.3z' fill='%23334155' />"
				            & "<rect x='762' y='108' width='7' height='122' rx='0' fill='%2364748B' /><path d='M714 112l6 -3.3h7l-6 3.3z' fill='%23CBD5E1' />"
				            & "<path d='M721 112l6 -3.3v152l-6 3.3z' fill='%23475569' /><rect x='714' y='112' width='7' height='152' rx='0' fill='%2394A3B8' />"
				            & "<path d='M712 112l60-6v26l-60 6z' fill='%230F172A' />"
				            & "<text x='742' y='128' text-anchor='middle' font-family='Segoe UI' font-size='13' font-weight='700' fill='%23FFFFFF' transform='rotate(-5.7 742 128)'>META</text>",
				        ""
				    )
				VAR vBarra =
				    IF (
				        vTemMeta,
				        "<rect x='230' y='277' width='588' height='7' rx='3.5' fill='%2364748B' /><rect x='230' y='277' width='"
				            & vLarguraTexto
				            & "' height='7' rx='3.5' fill='"
				            & vCorBarra
				            & "'/><rect x='229' y='275' width='2' height='11' rx='0' fill='%23FFFFFF' />"
				            & "<text x='230' y='298' text-anchor='middle' font-family='Segoe UI' font-size='11' font-weight='600' fill='%23FFFFFF' >início</text>"
				            & "<rect x='351.5' y='275' width='2' height='11' rx='0' fill='%23FFFFFF' />"
				            & "<text x='352.5' y='298' text-anchor='middle' font-family='Segoe UI' font-size='11' font-weight='600' fill='%23FFFFFF' >25%25</text>"
				            & "<rect x='474' y='275' width='2' height='11' rx='0' fill='%23FFFFFF' />"
				            & "<text x='475' y='298' text-anchor='middle' font-family='Segoe UI' font-size='11' font-weight='600' fill='%23FFFFFF' >50%25</text>"
				            & "<rect x='596.5' y='275' width='2' height='11' rx='0' fill='%23FFFFFF' />"
				            & "<text x='597.5' y='298' text-anchor='middle' font-family='Segoe UI' font-size='11' font-weight='600' fill='%23FFFFFF' >75%25</text>"
				            & "<rect x='719' y='275' width='2' height='11' rx='0' fill='%23FFFFFF' />"
				            & "<text x='720' y='298' text-anchor='middle' font-family='Segoe UI' font-size='11' font-weight='600' fill='%23FFFFFF' >meta</text>",
				        ""
				    )
				VAR vCaminhao =
				    IF (
				        vTemDado,
				        "<g transform='translate("
				            & vXTexto
				            & " 0)'><path d='M-88 258l26-16h140l-30 18z' fill='%230F172A' opacity='0.20'/><path d='M-76 228l26 -14.3h150l-26 14.3z' fill='%23334155' />"
				            & "<path d='M74 228l26 -14.3v12l-26 14.3z' fill='%230F172A' /><rect x='-76' y='228' width='150' height='12' rx='0' fill='%231E293B' />"
				            & "<path d='M-80 158l30 -16.5h104l-30 16.5z' fill='%2393C5FD' /><path d='M24 158l30 -16.5v70l-30 16.5z' fill='%231E40AF' />"
				            & "<rect x='-80' y='158' width='104' height='70' rx='0' fill='url(%23bF)' />"
				            & "<rect x='-64' y='164' width='2' height='58' rx='1' fill='%231E3A8A' opacity='0.35'/>"
				            & "<rect x='-48' y='164' width='2' height='58' rx='1' fill='%231E3A8A' opacity='0.35'/>"
				            & "<rect x='-32' y='164' width='2' height='58' rx='1' fill='%231E3A8A' opacity='0.35'/>"
				            & "<rect x='6' y='164' width='2' height='58' rx='1' fill='%231E3A8A' opacity='0.35'/>"
				            & "<rect x='-80' y='214' width='104' height='6' rx='0' fill='%23FBBF24' /><circle cx='-27' cy='190' r='16' fill='%23FFFFFF' />"
				            & "<path d='M-37 185l10-5 10 5v11l-10 5-10-5z' fill='%23D97706' /><path d='M-37 185l10 5 10-5-10-5z' fill='%23FCD34D' />"
				            & "<path d='M-27 190v11l10-5v-11z' fill='%2392400E' /><path d='M34 178l24-13h24l-24 13z' fill='%2360A5FA' />"
				            & "<path d='M58 178l24-13 16 27-24 13z' fill='url(%23vidroB)' /><path d='M74 205l24-13v23l-24 13z' fill='%231E40AF' />"
				            & "<path d='M74 228l24-13v13l-24 13z' fill='%23172554' /><path d='M34 178h24l16 27v35H34z' fill='url(%23cF)' />"
				            & "<path d='M40 184h16l11 19H40z' fill='url(%23vidroB)' /><path d='M45 186h7l-9 15h-3v-7z' fill='%23FFFFFF' opacity='0.6'/>"
				            & "<rect x='44' y='212' width='10' height='3' rx='1.5' fill='%23DBEAFE' /><path d='M80 218l11-6v8l-11 6z' fill='%23FDE68A' />"
				            & "<path d='M72 236l30-16v8l-30 16z' fill='%2394A3B8' /><g transform='translate(-56 241)'>"
				            & vRoda
				            & "</g><g transform='translate(-28 241)'>"
				            & vRoda
				            & "</g><g transform='translate(52 241)'>"
				            & vRoda
				            & "</g></g>",
				        ""
				    )
				VAR vBalao =
				    "<rect x='354' y='18' width='272' height='100' rx='18' fill='%230F172A' opacity='0.10'/><path d='M478 116l12 14 12-14z' fill='%23FFFFFF' stroke='"
				        & vCorBorda
				        & "' stroke-width='2.5'/><rect x='350' y='12' width='272' height='104' rx='18' fill='%23FFFFFF' stroke='"
				        & vCorBorda
				        & "' stroke-width='2.5'/><rect x='481' y='113' width='18' height='5' rx='0' fill='%23FFFFFF' />"
				        & "<text x='486' y='56' text-anchor='middle' font-family='Segoe UI' font-size='40' font-weight='700' fill='%230F172A' >"
				        & vGrande
				        & "</text><text x='486' y='78' text-anchor='middle' font-family='Segoe UI' font-size='14' font-weight='400' fill='%23475569' >"
				        & vDetalhe
				        & "</text><rect x='386' y='87' width='200' height='21' rx='10' fill='"
				        & vCorFundo
				        & "' /><text x='486' y='102' text-anchor='middle' font-family='Segoe UI' font-size='13' font-weight='600' fill='"
				        & vCorTexto
				        & "' >"
				        & vSelo
				        & "</text>"
				RETURN
				    "data:image/svg+xml;utf8,"
				        & "<svg xmlns='http://www.w3.org/2000/svg' width='960' height='320' viewBox='0 0 960 320'>"
				        & vDefs
				        & vCenario
				        & vLoja
				        & vPista
				        & vPortico
				        & vBarra
				        & vCaminhao
				        & vBalao
				        & "</svg>"
				```
			displayFolder: Storytelling
			dataCategory: ImageUrl

		/// Texto alternativo da cena, com os mesmos números da imagem.
		measure 'Caminhão (Texto Alternativo)' = ```
				VAR vPercentual = [Atingimento (%)]
				VAR vEntregues = COALESCE ( [Entregues com Meta], 0 )
				VAR vDiferenca = vEntregues - [Meta]
				VAR vInteiro =
				    IF ( vPercentual < 1, MIN ( ROUND ( vPercentual * 100, 0 ), 99 ), ROUND ( vPercentual * 100, 0 ) )
				RETURN
				    SWITCH (
				        TRUE (),
				        ISEMPTY ( 'Entregas' ), "Pista vazia: sem entregas no período.",
				        ISBLANK ( vPercentual ),
				            "Caminhão no início da pista, sem pórtico de meta: "
				                & FORMAT ( [Entregues], "#,0" ) & " pedidos entregues, sem meta definida.",
				        "Caminhão na pista a caminho do pórtico da meta: "
				            & FORMAT ( vEntregues, "#,0" ) & " de " & FORMAT ( [Meta], "#,0" ) & " pedidos, "
				            & FORMAT ( vInteiro, "0" ) & "% da meta, "
				            & SWITCH (
				                TRUE (),
				                vDiferenca = 0, "meta atingida",
				                vDiferenca > 0, "meta superada em " & FORMAT ( vDiferenca, "#,0" ),
				                vDiferenca = -1, "falta 1 pedido",
				                "faltam " & FORMAT ( - vDiferenca, "#,0" ) & " pedidos"
				            ) & "."
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
   ajuste *Ajustar*; proporção 3:1 (ex.: 1008 × 336).
2. **Texto alternativo** do visual: botão *fx* → `Caminhão (Texto Alternativo)`.
3. **Segmentação** por `Região`.
4. **Descrição longa:** tabela nativa na mesma página com `Região`, `Pedidos Entregues`,
   `Meta de Pedidos`, `Entregues com Meta` e `Atingimento (%)`. É a versão legível dos dados
   da cena: o total de `Entregues com Meta` é o número da imagem (sem filtro, 206, e não as
   266 entregas de todas as regiões).
5. Cena pequena: no **visual de cartão**, seção *Image* com *Image source* = dados; o
   estado *Hover* aceita outra medida.

## Estados esperados
| Contexto | Cena | Balão |
|---|---|---|
| Sul | caminhão antes do pórtico | 82% · 82 de 100 pedidos · faltam 18 pedidos |
| Norte | caminhão além do pórtico, parado em 120% | 124% · 124 de 100 pedidos · meta superada em 24 |
| Leste | caminhão no início, sem pórtico, loja e barra | 60 · pedidos entregues · sem meta definida |
| Oeste | caminhão no início, com pórtico | 0% · 0 de 80 pedidos · faltam 80 pedidos |
| Nenhuma linha (filtro de visual que não casa) | só o cenário e a pista | Sem entregas no período |
| Sem filtro | caminhão antes do pórtico | 74% · 206 de 280 pedidos · faltam 74 pedidos |

## Conferir
```dax
EVALUATE ROW ( "Tamanho", LEN ( [Caminhão até a Meta] ) )
```
E `checar_svg.py` (skill `bi-qa-documentacao`) no modelo e no relatório.
