# Ficha Técnica: contrato do JSON

Conferido no código do Background Builder 1.032 (nov/2026). O Builder lê o
**último** bloco ` ```json ` do `.md` que for JSON válido. Campo inválido é
descartado; texto longo demais é cortado. Crase dentro do JSON vai como
```.

## Exemplo mínimo

```json
{
  "h1": "Análise de Vendas",
  "h2": "onde crescer em 2027",
  "tagline": "Receita, margem e clientes em uma leitura",
  "theme": "vendas",
  "bodyPages": ["Visão Geral", "Clientes", "Produtos"],
  "filters": ["Data", "Região", "UF", "Vendedor", "Categoria", "Canal"],
  "filterCategoryOverrides": {
    "Data": "when", "Região": "where", "UF": "where",
    "Vendedor": "who", "Categoria": "what", "Canal": "how"
  },
  "filterWidthOverrides": { "Região": "half", "UF": "half", "Vendedor": "full", "Categoria": "full", "Canal": "full" },
  "use5W2HGrouping": true,
  "filterAutoApply": true,
  "dataSources": "ERP de vendas\nCadastro de clientes",
  "idealizacao": "Diretoria Comercial",
  "especificacaoNegocio": "Gerência de Vendas; Controladoria",
  "realizacao": "Time de Dados & BI"
}
```

Este exemplo foi carregado e exportado no Builder publicado: 7 páginas, todas
aprovadas na verificação de pixels.

## Campos

| Campo | Tipo | Limite / valores | Observação |
|---|---|---|---|
| `h1` | texto | 200 | Obrigatório para o script |
| `h2` | texto | 200 | `""` = sem H2 |
| `tagline` | texto | 300 | Hero da página Início |
| `theme` | chave | lista abaixo | Define accent e ilustrações |
| `bodyPages` | lista de textos | 24 itens × 120 | Ordem = menu |
| `filters` | lista de textos | 40 itens × 120 | Painel lateral |
| `filterCategoryOverrides` | `{ filtro: categoria }` | `when` `where` `who` `what` `how` `howMuch` `why` | Quando, Onde, Quem, O quê, Como, Quanto, Por quê |
| `filterWidthOverrides` | `{ filtro: encaixe }` | `full` `half` `third` | Ignorado em filtro de data/período (sempre `full`) |
| `use5W2HGrouping` | booleano | padrão `true` | Agrupa o painel por 5W2H |
| `filterAutoApply` | booleano | padrão `true` | `false` = botões Aplicar + Limpar |
| `dicaSizes` | lista | `single` `multi` `mini` (até 3) | Ausente = `multi` (400×304) |
| `dataSources` | texto | 4000 | Uma fonte por linha (`\n`) |
| `idealizacao`, `especificacaoNegocio`, `realizacao` | texto | 300 | Página Sobre, cartão Equipe Técnica: **nomes** dos idealizadores, dos especificadores de negócio e dos realizadores. Até o Builder 1.033, `especificacaoNegocio` aceitava 4000 caracteres de descrição; a partir da 1.034, nomes, cortados em 300 |
| `pageBackground` | chave | `paper` `white` `ice` `lightgray` `tint` `charcoal` `slate` `navy` `darktint` | Ausente = `paper` |
| `customAccent`, `customNavy` | `#RRGGBB` | | Marca do cliente |
| `customDataColors` | lista de 8 | `""` ou `#RRGGBB` | Posições 0 e 2 sempre `""` |
| `customGood`, `customNeutral`, `customBad`, `customMaximum`, `customCenter`, `customMinimum` | `#RRGGBB` | | Sentimento e escala divergente |
| `customSlot` | `#RRGGBB` | | Cor dos nichos, só nos PNGs |
| `headerIcon` | `data:image/...` | | Ícone quadrado do cabeçalho |

**Só de saída** (o Builder ignora ao abrir; o script remove): `_appVersion`,
`resolvedPalette`, `filtrosForaDoPainel`.

## Regras de lista

- Itens vazios e repetidos (sem diferenciar maiúsculas e acentos) são removidos.
- Nomes reservados não entram em `bodyPages` nem em `filters`: Início, Sobre,
  Detalhe, Dica (em qualquer idioma).
- As chaves de `filterCategoryOverrides` e `filterWidthOverrides` precisam ter o
  mesmo nome do filtro; overrides de filtro que não está na lista são
  descartados.
- Filtro de **data/período** = nome igual a "Data", "Datas", "Período" ou
  "Períodos" ou começando por um deles seguido de espaço, `-`, `/`, `:` ou `_`
  (também em inglês e espanhol). Sempre largura inteira e mais alto.
- Sem override, o Builder sugere a categoria por um dicionário (Ano e Mês →
  Quando; Região e UF → Onde; Cliente e Vendedor → Quem; Produto e Categoria →
  O quê; Canal → Como; Valor e Idade → Quanto; Campanha → Por quê) e o Encaixe
  (partes de data → 1/3; o resto → 1/1). Filtro fora do dicionário fica sem
  classificação: **sempre** informe a categoria.

## Temas (`theme`)

| Família (accent) | Chaves |
|---|---|
| Comercial (#FF8C42) | `vendas`, `crm`, `rfm` |
| Finanças (#E8A13D) | `financeiro`, `controladoria`, `credito_cobranca`, `investimentos`, `contabil` |
| Pessoas (#3FA34D) | `rs`, `dp`, `td`, `endomarketing` |
| Cadeia & Operações (#7B4FC9) | `operacoes`, `compras`, `logistica`, `comex` |
| Marketing & Mercado (#D64541) | `marketing_digital`, `nps`, `churn`, `customer-journey` |
| Projetos (#E2B93B) | `pmo`, `kpis` |
| Qualidade (#1B9E8F) | `qa_garantia`, `qa_controle`, `esg`, `governanca`, `compliance` |
| TI (#5B7A99) | `bi` (Governança de Dados), `tco`, `finops`, `service-desk`, `infra-ti`, `ciberseguranca` |
| SSMA (#A6447A) | `hse`, `seguranca-trabalho`, `saude-ocupacional`, `meio-ambiente` |

## O que vem no ZIP

`<H1> - Coleção.zip` traz um PNG por página (`<H1> - <Página>.png`),
`<H1> - Tema.json`, `<H1> - Script.TMDL`, `<H1> - Background Builder.md` (a
Ficha, com `filtrosForaDoPainel`), o LEIAME e a pasta `Icones-Estatisticos`
(SVG e PNG).
