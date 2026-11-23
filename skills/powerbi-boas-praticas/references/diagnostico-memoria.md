# Diagnóstico: "Não há memória suficiente" numa tabela de detalhe

**[relato do autor]**, de um projeto real em PBIP. Anote a versão do Desktop ao
reproduzir.

## Sintoma
Uma tabela ou matriz de detalhe falha com **"Não há memória suficiente para
concluir a operação"** (`QuerySystemError`), embora os dados estejam corretos e o
modelo seja pequeno. Os outros visuais da página abrem normalmente.

## Causa encontrada
Uma **relação extra no caminho do visual**: o visual combinava colunas de duas
tabelas que só se ligavam por uma cadeia de relações a mais, e o mecanismo montou
um produto grande demais. Nem a "ponte" entre as tabelas nem os dados eram o
problema.

## Correção que funcionou
1. Trazer a coluna para a **dimensão** com `LOOKUPVALUE` (coluna calculada na
   dimensão, chave única).
2. **Remover** a relação que só existia para esse visual.
3. Refazer o visual com a coluna da dimensão.

Ao escolher onde trazer a coluna, siga a regra do modelo (`powerbi-boas-praticas`):
se a coluna existe na fonte, prefira o **merge no Power Query** a uma coluna
calculada; use `LOOKUPVALUE` quando a origem só existe no modelo.

## Antes de culpar a ponte
Teste variantes numa **página temporária**, uma mudança por vez, e apague a página
depois:
1. O mesmo visual sem o campo suspeito.
2. O mesmo visual com a coluna vinda de outra tabela.
3. Uma tabela mínima só com a chave e a coluna.

Se a variante sem a relação extra abre, a causa é a relação, não a ponte nem o
volume. Registre qual variante resolveu e a versão do Desktop.

Relacionado: `references/medidas-para-visuais.md` (atributo do lado "um" a partir
do lado "muitos" com `LOOKUPVALUE`).
