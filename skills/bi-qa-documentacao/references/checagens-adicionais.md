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
| 13 | Objeto do modelo sem `///`; `TabIntDicionário` ausente ou com menos linhas que o modelo | Dicionário vazio ou desatualizado |
| 14 | Dica sem cartão único, sem rodapé de drillthrough, ou com `tabOrder` fora de cartão → gráfico → rodapé | Dica fora do padrão |
| 15 | Texto alternativo ausente, em outro idioma, ou citando medida técnica (ex.: `VocêEstáVendo`) | Acessibilidade |

## Ordem sugerida
Bindings (camada 3) → Tabular Editor 2 carregando a pasta TMDL → checagens 1 a 15
→ BPA. As checagens 8 a 10 e 15 são idempotentes: o mesmo script que audita
também corrige.

## Regra de manutenção
Toda checagem nova nasce de um erro que escapou: registre aqui a causa, o
arquivo e o objeto afetado, para que a próxima auditoria o encontre sozinha.
