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

## Ordem sugerida
Bindings (camada 3) → Tabular Editor 2 carregando a pasta TMDL → checagens 1 a 18
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

## Regra de manutenção
Toda checagem nova nasce de um erro que escapou: registre aqui a causa, o
arquivo e o objeto afetado, para que a próxima auditoria o encontre sozinha.
