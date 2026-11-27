# Validação da carga de arquivos

Para modelo alimentado por arquivos que pessoas colocam numa pasta. Complementa os
validadores de relacionamento (itens sem correspondência).

## Regras mínimas

| Regra | Nível |
|---|---|
| Nome fora do padrão (o arquivo não é carregado) | Erro |
| Período em mais de um arquivo | Erro |
| Período sem arquivo entre o primeiro e o último | Erro |
| Mais de uma planilha quando o esperado é uma | Erro |
| Arquivo sem linhas do próprio período | Erro |
| Cabeçalho inesperado nas posições lidas | Erro |
| Moeda ou unidade diferente da esperada | Erro |
| Valor que deveria ser numérico e não é | Erro |
| Último arquivo atrasado | Aviso |
| Variação entre períodos acima do limite combinado | Aviso |
| Linhas de outro período ignoradas | Informação |

Gere também uma linha **OK** por regra sem ocorrência e a coluna **Verificado Em**:
tabela vazia não distingue "tudo certo" de "não rodou".

## Onde fica
- Tabela carregada no grupo **Validadores**, com medidas de erros, avisos e última
  verificação.
- **Fora da atualização geral** (`excludeFromModelRefresh`; no Power Query,
  desmarcar **Incluir na atualização do relatório**), porque relê todos os
  arquivos. Confirme no Desktop do autor como ele atualiza só essa tabela
  (botão direito na tabela › **Atualizar dados**) **[a confirmar no Desktop]**.
- Página própria. Pergunte ao autor se ela fica oculta ou no menu. Nunca dentro da
  página Sobre sem ele pedir.
- Não liste dados pessoais nas ocorrências: arquivo, período, regra e quantidade bastam.

## Testar com erros de propósito
Dados reais bons não provam que a regra detecta algo. Escreva a análise como função
que recebe `[Nome = ..., Planilhas = {tabelas}]` e, numa consulta temporária,
alimente-a com `#table` fictícias, uma por regra:

```m
Entrada = {
    [Nome = "Dados 2030_01.xlsx",     Planilhas = {Boa(2030, 1)}],
    [Nome = "Dados 2030_02 (1).xlsx", Planilhas = {Boa(2030, 2)}],          // nome fora do padrão
    [Nome = "Dados 2030_03.xlsx",     Planilhas = {Boa(2030, 3), Boa(2030, 3)}] // duas planilhas
}
```

Só aprove quando **cada regra** aparecer no resultado. Exclua a consulta temporária.
