# Storytelling com imagem: a analogia dos dados

Regra do autor: **storytelling não é pegar a imagem de um relatório que deu
certo, trocar as etiquetas e usar em outro.** É contar uma história com dados.
Cada relatório precisa de uma imagem que conte a história **dele**, a partir de
uma **analogia escolhida para o assunto**. Nada de reaproveitar ilustração de
outro relatório. As grandezas podem ser outras; o que importa é o contexto.

## 1. Qual analogia? (antes de desenhar)
1. **Liste a estrutura dos dados:** há **fases** (etapas em sequência)? **níveis
   ou status** (Bronze, Prata, Ouro)? **partes de um objeto**? **comparação**
   (ano vigente × anterior)? **território**? **meta**?
2. **Visual thinking (Dan Roam, *The Back of the Napkin*):** que pergunta os
   dados respondem? quem/o quê → retrato; quanto → gráfico; onde → mapa; quando →
   linha do tempo; como → fluxo; por quê → plano de várias variáveis. E o
   **SQVID**: simples × elaborado, qualitativo × quantitativo, visão × execução,
   individual × comparação, mudança × status quo.
3. **Design-by-Analogy (design thinking):** abstraia a relação e procure um
   domínio cuja estrutura seja a mesma. Conexão óbvia demais vira kitsch;
   distante demais não é entendida. Levante **2 ou 3 candidatas** e o autor escolhe.

| Estrutura dos dados | Analogia que serve |
|---|---|
| **Fases** em sequência | Estrada, trilha, linha de montagem. Sem fases, a estrada "fica engraçada" e perde o contexto |
| **Níveis / status** | Degraus, medalhas, escada de fidelidade |
| **Partes de um objeto** | **Anatomia** do produto, com chamadas em cada parte |
| **Comparação de dois lados** | Balança, gangorra (cuidado: veja a regra seguinte) |
| **Ranking** | Pódio |
| **Território** | Mapa com alfinetes |
| **Conversão** | Funil |
| **Meta** | Termômetro, velocímetro |

## 2. Regra de ouro: tem de continuar verdadeira com qualquer filtro
A imagem é fixa, mas o relatório é dinâmico: trocando um filtro, o resultado
muda. **Se a analogia congela uma conclusão, ela falha.** Exemplo: a balança
AV × AA penderia sempre para o mesmo lado; de um ano para o outro o peso
inverte. Prefira imagem **neutra**, em que **o dinâmico está nas medidas dos
cartões**, não no desenho.

## 3. Mecânica (já verificada)
- Visual `image` (`sourceFile`, `scaling 'Normal'`) em 1016×344, no canto
  inferior direito da Visão Geral, (888, 720); o corpo continua até x=1904.
- **Cartões de uma medida** sobrepostos às caixas de chamada, sem título, fundo,
  borda nem rótulo, valor centralizado, fonte 14, z acima da imagem.
- A imagem é **gerada por código** (SVG → PNG em 2×, fundo transparente, Playwright
  com Edge, sem download), com as cores do tema, e a geometria das caixas é
  desenhada para aquele relatório. Conectores desenhados **depois** da peça
  principal, senão ficam escondidos atrás dela; caixas estreitas para não cobrir
  partes do desenho.
- Texto alternativo descrevendo a imagem e o que os cartões mostram.
- Para abrir espaço, saem gráficos que já existem em outras páginas.

## 4. Exemplo: anatomia da camiseta (Vendas)
Relatório de camisetas: uma camiseta no centro (estampa no peito, etiqueta do
tamanho na gola) e quatro chamadas: **estampa, cor, tamanho e modelagem
campeãs**. Cada cartão é uma medida "Líder" que devolve o item de maior
faturado no contexto de filtro:

```dax
Estampa Líder =
VAR vTabela =
    ADDCOLUMNS ( VALUES ( 'Vendas Camisetas'[Nome da Estampa] ), "@Faturado", [Faturado (AV)] )
VAR vLider =
    TOPN ( 1, vTabela, [@Faturado], DESC, 'Vendas Camisetas'[Nome da Estampa], ASC )
RETURN
    MAXX ( vLider, 'Vendas Camisetas'[Nome da Estampa] )
```
Pasta de exibição `Storytelling`, formato `@`, com `///`. Teste feito no Desktop:
sem filtro (Branca, Médio, Feminina, "I've got the Power BI") e filtrando a região
Sul (Preta, Grande, Masculina, "The Power BI Bear"): o desenho é o mesmo e a
história muda com o filtro. Esta imagem só serve a um relatório de camisetas;
é de propósito.
