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
| **Ranking** | Pódio (com nome e foto dos três primeiros: ver `powerbi-visuais/references/imagens-e-icones.md`) |
| **Território** | Mapa com alfinetes |
| **Conversão** | Funil |
| **Meta** | Termômetro, velocímetro |
| **Conta multiplicativa** (A × B × C = total) | **Carrinho de compras até o caixa**: notas × peças por nota × preço = faturamento |
| **Distribuição** (mínimo, mediana, média, desvio, máximo) | **Corrida de entregas**: o mais rápido, o meio do pelotão, o ponto de equilíbrio, a regularidade, o mais lento |
| **Entra e sai** (estoque e fluxo: ativos, contratados, demitidos) | **Ponto de ônibus** (sobem, descem) ou **porta do escritório** (entram, saem) |

## 2. Regra de ouro: tem de continuar verdadeira com qualquer filtro
A imagem é fixa, mas o relatório é dinâmico: trocando um filtro, o resultado
muda. **Se a analogia congela uma conclusão, ela falha.** Exemplo: a balança
AV × AA penderia sempre para o mesmo lado; de um ano para o outro o peso
inverte. Prefira imagem **neutra**, em que **o dinâmico está nas medidas dos
cartões**, não no desenho.

## 2b. Teste dos 5 segundos: a analogia não pode precisar de explicação
Regra do autor: **se for preciso explicar a piada, ela falhou**, e piada que não é
para todos não serve a um relatório. Antes de gastar tempo em arte, faça a pergunta
que a imagem deve responder **sem legenda** e imagine alguém do negócio vendo a
página por 5 segundos.

- **Caso reprovado:** a *banheira* (a água é o quadro de pessoas, a torneira são as
  contratações, o ralo são as demissões). A identidade é exata, mas o usuário tem
  de traduzir "água = pessoas". Foi trocada.
- **Caso aprovado:** o *ponto de ônibus* ou a *porta do escritório*: todo mundo sabe
  o que é subir, descer, entrar e sair. "O ônibus saiu mais cheio ou mais vazio do
  que chegou?" se responde sem texto.
- Prefira **cenas do cotidiano** (ônibus, caixa de supermercado, corrida, pódio,
  porta) a metáforas de objeto (banheira, termômetro, balança).
- Quando a analogia tem **dois estados** (início e fim), prefira uma cena que mostra
  os dois de forma natural (dois ônibus, o que chega e o que parte) a uma cena de
  objeto único que exige desenhar "antes e depois" artificial.
- Teste de 5 segundos com um usuário de verdade, quando possível; se ele demora ou
  erra, mude a analogia, não o texto.

## 2c. Uma analogia por página; mesma família, cenas diferentes
Cada página do relatório conta a sua história com **uma analogia própria**. A
família visual é a mesma (3D isométrico, mesma paleta, mesmos balões), mas **a cena
muda**: nada de "estrada em toda página". Exemplos de páginas de relatórios
comerciais e de RH:

| Assunto da página | Pergunta | Cena |
|---|---|---|
| Prazo de entrega | O que querem dizer mediana e desvio padrão? | Corrida de entregas |
| Visão geral de vendas | De onde vem o faturamento? | Do carrinho ao caixa |
| Ranking de vendedores | Quem lidera? | Pódio com foto e nome |
| Quadro de pessoas | O que muda no número de ativos? | Ponto de ônibus ou porta do escritório |

Reaproveitar a *mesma estrutura de dados* em outro relatório é permitido; reaproveitar
o *desenho* não (regra do início do documento).

## 2d. Identidade antes do desenho: o que a imagem afirma precisa ser verdade
1. **Escreva a identidade** que a imagem mostra e **prove** a partir das medidas:
   `Faturamento = Notas × Camisetas por Nota × Preço por Camiseta`;
   `Ativos no Fim = Ativos no Início + Contratados − Demitidos`.
   Se os intervalos das medidas de início e fim têm bordas diferentes, a conta pode
   não fechar por um dia ou um evento: leia as definições (>=, >, <).
2. **Teste no Desktop** com uma consulta DAX, que deve devolver 0:
   ```dax
   EVALUATE ROW ( "Diferença", [Ativos no Fim] - ( [Ativos no Início] + [Contratados no Período] - [Demitidos no Período] ) )
   ```
3. **Desenho neutro:** a imagem é fixa e o relatório é dinâmico. Marcadores de
   "início" e "fim" no **mesmo nível**, dois ônibus com **a mesma lotação**, balança
   que não pende: nada que afirme "subiu" ou "caiu". Quem muda são os cartões.
4. Medidas novas (`Camisetas por Nota`, `Preço Médio por Camiseta`) ficam em uma
   pasta `Storytelling`, com `///`, e o dicionário é regenerado.

## 2e. Arte vetorial por medida: o nível do próprio relatório
Quando a arte precisa **se mover com o dado** (personagem sobre uma pista), SVG por medida
serve, desde que no estilo plano do fundo (traço fino no azul do tema, cor chapada, aquarela
suave, um destaque). **Boneco de palito é rejeitado.** Antes de aplicar:
1. esboço com o **acabamento final** e os estados difíceis (acima da meta, sem meta, sem dado);
2. duas opções de desenho, em **tamanho real e ampliado**, ao lado do estilo do fundo;
3. aprovação do autor; só então a medida (`powerbi-visuais`, `svg-html-dax.md`).

Para arte 3D ou rica, continua valendo o gerador de imagem.

## 3. Mecânica (já verificada)
- Visual `image` (`sourceFile`, `scaling 'Normal'`) em 1016×344, no canto
  inferior direito da Visão Geral, (888, 720); o corpo continua até x=1904.
- **Cartões de uma medida** sobrepostos às caixas de chamada, sem título, fundo,
  borda nem rótulo, valor centralizado, fonte 14, z acima da imagem.
- **Quem desenha a arte.** Diagrama simples (pista, régua, caixas) pode ser **gerado
  por código** (SVG → PNG em 2×, fundo transparente, Edge ou Chrome sem janela). Mas
  **ilustração 3D com volume, luz e personagens não sai de SVG à mão**: o resultado
  fica com cara de diagrama e perde para o que um gerador de imagem (ChatGPT, por
  exemplo) faz. O fluxo que funciona: o agente escreve o **prompt**
  (`references/prompt-imagem-storytelling.md`), o autor gera e salva o PNG na pasta do
  projeto, e o agente **mede os balões no PNG**
  (`scripts/medir_png.py baloes`) e posiciona os cartões. O que o gerador não
  garante (texto longo exato, geometria precisa) fica por conta dos balões vazios e
  dos cartões do Power BI. Conectores desenhados **depois** da peça
  principal, senão ficam escondidos atrás dela; caixas estreitas para não cobrir
  partes do desenho.
- Texto alternativo descrevendo a imagem e o que os cartões mostram.
- Para abrir espaço, saem gráficos que já existem em outras páginas.

### Posicionar cartões nos balões desenhados pela arte
1. **Medir:** `python medir_png.py baloes arte.png --cor escuro=10,10,14 --cor azul=30,140,240 --cor laranja=255,90,30`.
   Cada balão sai com o trecho reto das bordas; some o raio do canto (≈34 px em arte
   de 2170 px) para ter a caixa real. A imagem pode sair com 1 a 2 px de diferença
   do esperado (2170×725): use a largura e a altura reais do arquivo.
2. **Escala:** `s = largura do visual ÷ largura do PNG`. As posições `X` e `Y` do
   visual saem do layout do **Background Builder** (corpo de (376, 128) a (1904,
   1064); faixa de indicadores no topo; barra lateral em x40). Posição de um cartão:
   `x = X + (x0 + 16) × s`, `largura = (x1 − x0 − 32) × s`, `y = Y + 96 × s`
   (abaixo do rótulo que a arte traz no topo do balão), altura 40.
3. **Texto do cartão:** Segoe UI Semibold, **na cor do contorno do balão** (meça a cor
   no PNG com `medir_png.py cor`). Tamanho pelo **pior caso do valor** e pela
   largura do balão: 20 quando cabe, 18 quando o valor é largo (ex.: `R$ 7.815.206`
   num balão de ~170 px).
4. **Espaço:** a imagem de 3:1 ocupa **1008×336** (ou 1528×509 na faixa inteira);
   avise o que sai da página para abrir espaço (um gráfico redundante, não um
   que alimenta um Detalhe).
5. **Ajuste Preencher** (`scaling 'Fill'`) e texto alternativo descrevendo a cena e
   o que cada cartão mostra.
6. **Ordem de tabulação** e dicionário (as medidas novas) na mesma passada.
7. **Simule antes de entregar:** monte um HTML com a imagem e os cartões nas
   posições gravadas e tire uma captura com o Edge; só depois diga ao usuário que
   não viu o render no Desktop e peça a conferência.

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
