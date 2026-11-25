# Dica com imagem e moldes de Detalhe e Dica

Complementa `dica-cartao-unico.md`. **[verificado]** = confirmado no Desktop.

## Fiação da Dica que funciona [verificado]
- `page.json`: `"type": "Tooltip"`, `visibility: HiddenInViewMode`, **sem
  `pageBinding`**. Com `pageBinding { type: Tooltip, parameters: [] }` e
  `visualTooltip.type = 'ReportPage'` o Desktop reconhece a página na lista, mas
  o hover mostra o **tooltip padrão**.
- Visual de origem: `visualTooltip [{ show: true, section: '<id da página>' }]`,
  **sem `type`**.
- A Dica aberta direto na página mostra "-" no título (sem seleção); o teste
  real é passar o mouse num visual.

## Dica de entidade com imagem
Use o visual `image` dinâmico (`powerbi-visuais/references/imagens-e-icones.md`).
- **600×456 (mini relatório):** cartão 584×136 em (8, 8), imagem 232×296 em
  (8, 152) e gráfico de colunas por Ano 344×296 em (248, 152). Margem e vão de 8;
  o gráfico termina em x=592, y=448 (simetria com a borda).
- **400×304 (vários visuais):** imagem 88×88 ao lado do cartão 288×88 e gráfico
  de 152 de altura. A Dica de entidade com imagem cabe em 400×304; 600×456 não é
  obrigatório (o Performance Comercial usa 400×304 nas seis).
- Cartão da Dica **sem ícones** (trunca o valor).
- Texto longo (nome de estampa de 48 caracteres) em tile de 170 px trunca:
  teste com o maior valor possível.

## Molde de Detalhe (um só para várias entidades) [do Performance Comercial]
Cartão de indicadores (altura 152, 7 medidas), **tabela de ranking 784×768** à
esquerda, **rosca + funil** (536×376) e **linha AV × AA por Semana #**
(1088×376). Detalhe de Vendedor e de Estampa levam **imagem 152×152** ao lado do
cartão (cartão de 1720 de largura). Seis Detalhes no mesmo molde: UF, Categoria,
Vendedor, Campanha, Estampa, Canal. No cabeçalho: Voltar em (1744, 40) 144×48
(`icon 'back'`, `visualLink 'Back'`) e cartão de seleção em (1232, 48) 496×32.
