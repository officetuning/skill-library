# Checagens baratas adicionais (acrescentar à camada 3 do QA)

Complementam as sete checagens de `tmdl-pbir/references/edicao-por-script-e-desktop.md`.
Todas pegaram problema real em quatro projetos e rodam em segundos contra a
pasta do relatório.

| # | Checagem | O que acusa |
|---|---|---|
| 8 | Cartão numérico sem `labelDisplayUnits 1D` por medida | "mil/mi" no cartão |
| 9 | Eixo de valor, rótulo, rosca (**objeto `value`**), medidor ou árvore sem a unidade Nenhum | "mil/mi" no centro da rosca, no eixo, nos rótulos |
| 10 | Segmentação sem `background.show = false` ou `border.show = false` | Fundo ou borda por herança, principalmente na de data |
| 11 | `pageNavigator` fora das células do PNG do menu (x e largura) | Cliques deslocados em relação aos rótulos |
| 12 | `pageOrder` diferente da ordem do menu da ficha | Menu e páginas em ordem diferente |
| 13 | Objeto do modelo sem `///`; tabela `Dicionário` (grupo Internas) ausente ou com menos linhas que o modelo | Dicionário vazio ou desatualizado |
| 14 | Dica sem cartão único, sem rodapé de drillthrough, ou com `tabOrder` fora de cartão → gráfico → rodapé | Dica fora do padrão |
| 15 | Texto alternativo ausente, em outro idioma, ou citando nome técnico de medida ou campo | Acessibilidade |
| 16 | Referência a campo do modelo antigo no `.Report`: `grep -r '"Entity": "<prefixo antigo>'` (ex.: `"Entity": "Tab` depois de migrar para nomes de negócio na 2.0.0) deve dar **0** | `filterConfig` de visual com campo que não existe mais (fica pendurado, sem erro) e regra de cor condicional apontando para medida inexistente (código morto) |
| 17 | Qualquer `labelDisplayUnits`, `valueDisplayUnits` ou `dataLabelDisplayUnits` com valor diferente de `1D`, **em qualquer visual** | Visual com "mil/mi" que escapou das checagens 8 e 9 |
| 18 | Visual R ou Python: `grep -rlE '"visualType": "(scriptVisual|pythonVisual)"' <pasta>.Report` deve dar **0** | Visual que para de renderizar com a aposentadoria dos visuais R e Python (maio de 2027) |
| 19 | Segmentação de data em `RelativeDatePicker` sem `general.filter` (`DateSpan`) ou sem `dateRangeText` e `relativeText` em 12 | Segmentação que abre sem recorte ou com fonte fora do padrão; costuma estar certa só na primeira página |
| 20 | Segmentação de texto sem `selfFilterEnabled true` (Pesquisar) ou sem `dropdown.accentBarShow false` | Barra de destaque e falta de busca em todas as páginas |
| 21 | Gráfico ou matriz com eixo de tempo (Calendário, **Tempo de Casa**) sem decisão registrada sobre a segmentação de data (`page.json › visualInteractions`) | Coluna por Ano com um ano só, matriz "ano a ano" com um ano, área por Tempo de Casa esvaziada; ver `powerbi-visuais/references/eixo-temporal-e-interacoes.md` |
| 22 | Cartão largo de Grandes Números com altura ≠ 168 (sem etiquetas de referência) ou 240 (com), sem ícones, com ícone fora de ~53 px, sem `paddingUniform 10L`, ou com `spaceAboveDivider` ≠ 4 quando há referência | Rótulo colado ou cortado, ícone batendo na margem, altura heterogênea entre páginas |
| 23 | Qualquer coordenada de visual fora da grade de 8 px (x, y, largura, altura; exceto Dica e cartão sobre balão de arte) | Redistribuição que deixou 1 ou 2 px de sobra |
| 24 | DAX com tabela sem aspas simples, **inclusive sem colchete** (`COUNTROWS(Tab)`, `ALL(Tab)`), e `VAR` com `Δ` ou símbolo no nome | "Token inválido" ao abrir; regra da casa descumprida |
| 25 | `dataColors` do tema **registrado** no relatório ≠ `Tema.json` da Ficha do Builder | Cores de visual e nichos do fundo que não combinam |
| 26 | Gráfico com `title` ou `subTitle` próprio (exceto título por medida em Dica): perguntar ao autor | Títulos escritos por script que o autor teve de redefinir |
| 27 | Dica sem cartão com título por medida, com mais de um cartão, ou de até 320 px com eixo de tempo | Dica só com gráfico, com rolagem lateral |
| 28 | Botão Voltar sem `background.show` e `border.show` em `false` | Moldura sobre o botão desenhado no fundo |
| 29 | Medidas concentradas em tabela só de medidas (`checar_medidas.py`) | Contraria a orientação de distribuir as medidas pelas tabelas |
| 30 | Cena em SVG por medida sem `ImageUrl`, com `#` ou `%` sem escape, vírgula decimal a conferir ou visual sem texto alternativo (`checar_svg.py`) | Imagem que quebra em silêncio, sobretudo em pt-BR, ou que o leitor de tela não descreve |

## Ordem sugerida
Bindings (camada 3) → Tabular Editor 2 carregando a pasta TMDL → checagens 1 a 25
→ BPA. As checagens 8 a 10 e 15 são idempotentes: o mesmo script que audita
também corrige.

## Como rodar as checagens 16, 17 e 18
- **16:** `grep -rn '"Entity": "Tab' <pasta>.Report` (troque `Tab` pelo prefixo das
  tabelas do modelo antigo). Qualquer linha é pendência. Confira também
  `filterConfig` e as regras de formatação condicional dos visuais.
- **17:** o Desktop grava o valor algumas linhas abaixo da chave; use
  `grep -rn -A6 'DisplayUnits' --include=visual.json <pasta>.Report` e procure o
  `Literal.Value` diferente de `'1D'`, ou percorra o JSON por script. Se o autor
  quis uma unidade de propósito (ex.: milhões num KPI), registre a exceção em vez
  de corrigir. Foi o que teria evitado o erro nos 6 visuais de uma página de
  Custos. [relato do autor]
- **18:** cada arquivo listado é um visual a refazer com visual nativo, visual
  por medida DAX (SVG) ou visual personalizado certificado (skill `powerbi-visuais`).

## Rodar as checagens de visuais de uma vez
`scripts/auditar_visuais.py "<Projeto>.Report/definition" --tema "<Builder>/<H1> - Tema.json"`
cobre as checagens 8, 9, 10, 15 (texto alternativo ausente), 17, 18, 19 a 23, 25 a 28, e
lista as perguntas de design ("[decidir]": eixo de tempo, gauge, pizza, tabela sem
título). Saída 1 se houver pendência fixa. A 24 (DAX) e as demais seguem pelo
`tmdl_parser.py`.

## Medidas fora de lugar (checagem 29)
`scripts/checar_medidas.py "<Projeto>.SemanticModel/definition"` acusa a tabela só de medidas.
Para migrar, escreva um mapa `{ "medidas": {...}, "pastas": {...} }` e rode
`scripts/mover_medidas.py <modelo> <relatório> mapa.json` (ensaio) e depois com `--aplicar`:
move o bloco TMDL com o mesmo `lineageTag`, troca `Entity`, `queryRef`, seletores e filtros no
relatório e **exclui a tabela que ficar vazia** (arquivo, `ref table` e `PBI_QueryOrder`): sem
coluna e sem medida, o Desktop avisa "Esta consulta não tem nenhuma coluna com os tipos de dados
com suporte" e desabilita o carregamento. Backup antes; confira os bindings, abra, atualize e salve.
Testado numa cópia de projeto: modelo carregado no Tabular Editor 2, bindings conferidos e, no
Power BI Desktop, o projeto abriu, atualizou, mostrou os mesmos valores, foi salvo e reabriu sem
erro. Descrições (`///`) que citem a tabela excluída não são reescritas: revise depois.
Migrar projeto existente só com aprovação do autor.

## Cena em SVG por medida (checagem 30)
`scripts/checar_svg.py "<Projeto>.SemanticModel/definition" "<Projeto>.Report/definition"`

| Código | Nível | Quando |
|---|---|---|
| `sem-imageurl` | erro | a medida devolve `data:image/svg+xml` e não tem `dataCategory: ImageUrl` |
| `cerquilha` | erro | `#` de cor ou `url(#` sem virar `%23` |
| `porcento` | erro | `%` sem virar `%25`, inclusive o que vem de `FORMAT(x, "0%")` |
| `virgula` | conferir | `FORMAT` com casas decimais sem `SUBSTITUTE(..., ",", ".")` nem `"en-US"` |
| `sem-alt` | erro | visual que usa a medida sem texto alternativo |

Entram também as medidas que chamam função DAX que desenha SVG (`functions.tmdl`) ou a
`DaxLib.SVG.*`; o corpo das funções próprias é conferido, o das bibliotecas `DaxLib.*` não.
HTML com `<svg>` embutido, sem data URI, fica de fora. Um `SUBSTITUTE` só isenta o texto que
passa por ele.

Sem a pasta do relatório, o texto alternativo não é conferido. Número convertido em texto
sem `FORMAT` não é detectado: abra o relatório em pt-BR.

## Regra de manutenção
Toda checagem nova nasce de um erro que escapou: registre aqui a causa, o
arquivo e o objeto afetado, para que a próxima auditoria o encontre sozinha.

## Cores de série repetidas no tema
Causa que escapou: destaque (accent) igual ao navy no Builder deixa
`dataColors[0] == dataColors[2]`, e duas séries saem com a **mesma cor** sem
nenhum erro. Confira no tema registrado se há cores iguais entre as primeiras
posições usadas e, nos gráficos com legenda, na captura de tela. Correção sem mexer
no tema: `dataPoint` por valor, com `selector.data[0].scopeId` comparando a coluna
da série ao valor e `fill` em `ThemeDataColor`.

## O que a auditoria por arquivo não vê
Corte de texto, rolagem dentro do visual, nível escondido de uma árvore estreita e
sobreposição de cor passam com **0 pendências**. Peça PDF ou captura antes de dar a
página por pronta. O PDF **não inclui páginas ocultas**: Dica e Detalhe pedem
captura ou teste do autor.
