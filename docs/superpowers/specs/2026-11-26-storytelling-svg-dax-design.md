# Storytelling com cena em SVG por medida DAX (desenho curto)

## Intenção
A cena que **se move com o dado** passa a ser feita em SVG montado por medida DAX, e
isso vira o padrão de storytelling do plugin.

## Caminhos considerados
| Caminho | Troca | Decisão |
|---|---|---|
| A. SVG+DAX só para cena que muda com o dado; gráfico analítico nativo; arte 3D estática no gerador de imagem | Mantém o que cada técnica faz melhor; exige uma regra de escolha | **Escolhido pelo autor** |
| B. Todo infográfico em SVG+DAX, traço plano | Consistente, mas perde o 3D | Descartado |
| C. Fundo 3D gerado com camada móvel em SVG | Mais rico, pesado e não testado | Descartado |

## Regra de escolha
| A página pede | Técnica |
|---|---|
| Comparar, ver tendência, ler valor | Visual nativo |
| Cena em que posição, preenchimento ou quantidade mudam com o filtro | **SVG por medida (padrão)** |
| Ilustração rica que não muda; só os números mudam | Gerador de imagem + cartões |

A cena continua obrigada ao teste dos 5 segundos e a ser verdadeira com qualquer filtro.

## Padrão da cena
1. **Onde aparece:** visual de imagem (cena grande); imagem do cartão, com variação ao
   passar o mouse (cena pequena); tabela ou matriz (por linha).
2. **Medida:** data URI, `dataCategory: ImageUrl`, ponto decimal forçado, `%23` e `%25`.
   O exemplo oficial da Microsoft usa `FORMAT` sem troca de vírgula em modelo `en-US`;
   em pt-BR a troca continua obrigatória.
3. **Estados:** sem dado, sem meta, acima de 100%, filtro que zera a meta.
4. **Arte:** acabamento do próprio relatório; esboço com os estados difíceis e duas opções
   em tamanho real antes de aplicar. Boneco de palito é rejeitado.
5. **Reuso:** peça usada em duas ou mais medidas vira função DAX do usuário (`Svg.Peca`,
   nível de compatibilidade 1702; GA em jun/2026). Cena única fica numa medida só e repete a
   peça por `VAR` (esclarecido em 26/11, com o exemplo em volume).
6. **Biblioteca:** DaxLib.SVG (MIT, 2.0.0 tem mudanças incompatíveis com a 1.x) é
   dependência opcional para formas e mini-gráficos; o plugin não copia o código.
7. **Acessibilidade:** texto alternativo por medida (identifica a cena e traz os números)
   e os mesmos dados legíveis na página em cartão, tabela ou gráfico nativo (descrição
   longa, segundo o tutorial de imagens complexas do W3C). Substitui a regra atual que
   proíbe SVG quando a acessibilidade é formal.
8. **Tamanho:** manter o resultado da medida abaixo de 32.766 caracteres e conferir com
   `LEN`. É precaução da casa: o limite publicado (Chris Webb, 2019) vale para texto
   carregado no modelo; para medida em visual não está confirmado.

## Arquivos
| Arquivo (em `skills/`) | Mudança |
|---|---|
| `data-storytelling/SKILL.md` e `references/storytelling-com-imagem.md` | regra de escolha; troca o item "arte 3D vem de gerador" pela tabela |
| `powerbi-visuais/SKILL.md` e `references/svg-html-dax.md` | exceção ao "nativo primeiro", cartão com imagem, funções, acessibilidade, tamanho, fontes |
| `powerbi-visuais/references/cena-svg-exemplo.md` (novo) | cena completa com dados fictícios, medida e texto alternativo |
| `bi-qa-documentacao/scripts/checar_svg.py` (novo) | acusa em medida SVG: sem `ImageUrl`, `#` ou `%` sem escape, `FORMAT` decimal sem troca de vírgula, visual sem texto alternativo |
| `dax-udf` | remissão ao exemplo |
| versão e `CHANGELOG.md` | 2.6.0 |

## Fora do escopo
Trocar gráfico analítico por SVG; remover o fluxo do gerador de imagem; usar dados ou nomes
de projetos reais; usar as skills da Data Goblins (licença); alterar relatórios existentes.

## Conferência
- `checar_svg.py` roda no exemplo sem achados e acusa uma cópia com cada defeito plantado.
- Exemplo renderizado no Edge a partir das cadeias da própria medida, nos quatro estados.
- Autor abre o exemplo no Desktop antes do merge.

## Entrega
Branch e PR próprios, depois do merge do PR #16.

## Fontes
- <https://learn.microsoft.com/power-bi/visuals/power-bi-visualization-card>
- <https://learn.microsoft.com/power-bi/visuals/power-bi-visualization-image-visual>
- <https://learn.microsoft.com/dax/best-practices/dax-user-defined-functions>
- <https://github.com/EvaluationContext/daxlib.svg>
- <https://www.w3.org/WAI/tutorials/images/complex/>
- <https://blog.crossjoin.co.uk/2019/05/17/maximum-length-text-value-power-bi/>
