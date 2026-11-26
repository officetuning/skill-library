# Manual do usuário para quem não é de BI

Documento para quem **usa** o relatório. A documentação técnica (modelo, medidas)
é outra peça. Escreva em linguagem de negócio: "orçamento", "passar o mouse",
"botão direito"; sem DAX, sem nome de tabela. Os dados do manual costumam ser
reais: gere um arquivo local, marque "uso interno" e não publique fora.

## Roteiro
1. **Para que serve:** tabela "pergunta → onde olhar" e um passo a passo de cinco minutos.
2. **Palavras do relatório:** cada termo e sinal visual (✔️ ⚠️ ❗, vazio, data de atualização).
3. **De onde vêm os dados:** fontes, o que é lido de cada uma, o tratamento em passos
   numerados, o que o preenchimento atual provoca (campos em branco, nomes diferentes
   entre fontes) e como atualizar. **Pergunte se o público pode ver as pendências da fonte.**
4. **Navegar e filtrar:** menu, cada filtro (e quais não valem para alguma medida),
   como o período é escolhido e quais visuais ignoram um filtro.
5. **Páginas:** para cada uma, a pergunta que responde, a imagem e uma tabela
   "quadro (com o título que aparece na tela) → como ler".
6. **Dica:** onde funciona e o que mostra.
7. **Detalhe:** como abrir, o que contém, como voltar e por que o total pode diferir da linha clicada.
8. **Dúvidas comuns** e ficha do relatório (equipe, versão, data).

## De onde tirar o conteúdo
Leia o projeto, não escreva de memória: passos do Power Query, medidas,
`page.json › visualInteractions` (o que ignora filtro), `visualTooltip` (onde há Dica),
`pageBinding` (por onde se abre o Detalhe).

## Imagens
Peça ao autor o **PDF exportado** do relatório e converta com
`scripts/renderizar_pdf.ps1`; recorte os destaques (cabeçalho, filtros, cartão,
infográfico), que na página inteira ficam pequenos. **Detalhe e Dica não saem no
PDF** (páginas ocultas): peça capturas ou diga que ficaram só em texto.

## Montagem e conferência
- Word com estilos de título nativos, sumário, tabelas com larguras explícitas,
  `altText` nas figuras e cada página do relatório em folha própria.
- Com o Word instalado, atualize o sumário e exporte o PDF por automação
  (`TablesOfContents(1).Update()`, `ExportAsFixedFormat`).
- **Renderize o PDF gerado e olhe as páginas** antes de entregar: título separado da
  figura e figura sozinha na folha são os defeitos mais comuns.
- Liste ao autor o que ele precisa confirmar no ambiente dele (nomes de menu,
  permissões de exportação, Ctrl + clique no Desktop).
