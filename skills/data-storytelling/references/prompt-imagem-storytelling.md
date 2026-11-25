# Prompt para o gerador de imagem (infográfico de storytelling)

Modelo usado para gerar a arte dos infográficos (ChatGPT, nov/2026). O agente
preenche as lacunas e entrega o texto ao autor, que gera e salva o PNG na pasta do
projeto. Depois: `scripts/medir_png.py` e o método de `storytelling-com-imagem.md`.

## Modelo

> Ilustração 3D isométrica, estilo "infográfico de produto", no mesmo estilo visual
> dos infográficos anteriores (personagens simpáticos e arredondados, laje elevada de
> cantos suaves, luz suave), mas **uma cena diferente: {CENA}**, sem {O QUE NÃO
> REPETIR, ex.: estrada}. Fundo liso {COR DO FUNDO DA PÁGINA, ex.: creme #FFFAF7}.
> Proporção {3:1 (2172 × 724 px)}. Todo o texto em português, grafia exata, sem nenhum
> outro texto{, exceto: ...}.
>
> **Cena:** {descrição, de um lado ao outro, com os elementos que cada balão aponta}.
> {Sinais 3D discretos de "+", "−", "×", "=" onde a conta pede.} Poucos elementos de
> apoio, discretos.
>
> **{N} balões de chamada brancos, vazios, de cantos bem arredondados e contorno
> colorido de 3 px**, alinhados lado a lado no alto, cada um com cerca de {17 a 22}% da
> largura, com pequeno espaço entre eles. O rótulo em negrito, azul-marinho, fica
> centralizado no topo de cada balão; o resto fica **vazio**. Cada balão tem um
> conector fino terminando num ponto sobre o elemento:
> 1. "{Rótulo 1}": contorno {cor}, ligado a {elemento}.
> 2. ...
>
> **Paleta:** {cores do tema, em hexadecimal}. Sem sombras duras.

## Regras que evitam retrabalho
- **Balões vazios, rótulo no topo**: é onde entram os cartões do Power BI. O texto
  que importa (o valor) nunca fica na arte.
- **Ordem dos balões** é a da leitura (esquerda para a direita); peça para manter
  exatamente essa sequência.
- **Uma cor de contorno por significado** (dois azuis para componentes, laranja para
  destaque, escuro para pontas), porque o cartão herda essa cor.
- **Formato 3:1** é o que o corpo da página comporta (1008×336); 2:1 para pódio ou
  cena mais alta (768×384). Se o gerador entregar mais quadrado, o fundo liso permite
  estender as laterais.
- **Neutralidade:** diga o que **não** pode sugerir ("sem indicar mais ou menos
  gente", "as duas bandeirinhas na mesma altura").
- **Sem rosto nem desenho dentro de molduras** que receberão foto (pódio).
- Se a arte vier com **texto errado** num rótulo, peça de novo; não corrija o PNG
  à mão.

## Exemplos de cena já aprovados
| Assunto | Cena | Balões |
|---|---|---|
| Distribuição do prazo de entrega | Corrida de entregas: entregadores correndo com caixa, venda na largada, entrega na chegada | Mais lenta, Regularidade, Meio do pelotão, Ponto de equilíbrio, Mais rápida |
| Faturamento = notas × peças × preço | Balcão de caixa de loja de camisetas: fila de carrinhos, carrinho cheio, etiqueta de preço, caixa registradora, sinais × × = | Vendas, Camisetas por nota, Preço por camiseta, Ticket Médio (colchete laranja), Faturamento |
| Ranking | Pódio de três degraus com molduras redondas vazias para a foto | 1º, 2º e 3º lugar (nome e valor no balão) |
| Quadro de pessoas | Porta do escritório (entram "+", saem "−", equipe "antes" e "depois") ou ponto de ônibus (chega, sobem, descem, parte) | Ativos no Início, Contratados, Demitidos, Ativos no Fim |
