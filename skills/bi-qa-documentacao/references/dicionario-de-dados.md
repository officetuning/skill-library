# Dicionário de dados em todo projeto

Regra do autor: **todo projeto tem o dicionário de dados atualizado**. Em quatro
projetos, só dois tinham; os outros dois não tinham a tabela nem as descrições
(95 e 66 objetos sem `///`).

## Obrigatório
- **Toda tabela, coluna e medida com descrição (`///`).** O dicionário é gerado
  das descrições; sem elas, a linha sai vazia.
- **Tabela `Dicionário`** (grupo de consultas Internas, oculta) (estática) com 7 colunas: Tabela, Descrição da
  Tabela, Tipo (Campo, Campo Calculado ou Medida), Campo/Medida, Fórmula DAX (em
  uma linha), Descrição, Tipo de Dados (Text, Integer, Number, Currency, Date).
  Sem relacionamentos. Campo Calculado = coluna calculada em DAX; Campo = coluna
  que vem da origem ou do Power Query.
- **Visual Tabela no nicho "Dicionário de Dados" da página Sobre** (fundo do
  Builder: x656, y656, 608×312), com texto alternativo e sem título próprio (o
  nicho já tem nome). Mostra 5 colunas, nesta ordem: **Campo/Medida, Tipo de
  Dados, Tipo, Tabela, Descrição**. Descrição da Tabela e Fórmula DAX ficam na
  tabela (para o `.docx` e para consulta), fora do visual. Ordem de tabulação: menu, atualização, tabela, textos.
- **Regenerar** sempre que tabela, coluna ou medida for criada, renomeada ou
  tiver a descrição alterada. Compare as linhas do dicionário com o modelo antes
  de publicar.

## Como gerar
1. Leia o modelo com o parser TMDL (`scripts/tmdl_parser.py`): descrições,
   expressões, `dataType` e `formatString`.
2. Monte as linhas na ordem: fatos (com suas medidas), calendário e demais dimensões, pontes,
   monolíticas, internas e, por último, o próprio dicionário (ele descreve a si
   mesmo; gere em **duas passadas**: crie o arquivo, releia o modelo, grave as
   linhas).
3. Serialize como JSON, comprima (deflate) e grave em base64 no M:
   `Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("…",
   BinaryEncoding.Base64), Compression.Deflate)), type table [...])`, com
   renomeação para os nomes em português.
4. Registre `ref table Dicionário` no `model.tmdl`, e a tabela em
   `PBI_QueryOrder` (grupo de consulta Internas).

## Armadilhas
- **Descrever sem olhar os dados.** No Vendas supus SKU, CNPJ e tamanhos PP/GG;
  a planilha tinha 179 códigos de produto, CPF e tamanhos EP a EG. Antes de
  escrever a descrição, **conte os valores distintos e leia alguns exemplos da
  fonte** (campanhas Contínua/Sazonal, categorias Padrão/Bronze/Prata/Ouro).
- **Regenerar o dicionário** (script `tmdl_parser.py` → linhas → JSON → deflate →
  base64 no M) **sempre que o modelo muda**, inclusive ao criar medida de
  storytelling. Num modelo de 4 tabelas foram 142, depois 146 linhas.
- **Ordem no visual:** sem coluna de ordem, a tabela do dicionário sai em ordem
  alfabética de Campo/Medida; para a ordem do modelo (fato, calendário, demais)
  acrescente uma coluna de ordem oculta.
- **Tipo de dado de coluna calculada sem `dataType`:** o parser devolve vazio e
  o tipo cai em Text. Infira: nome terminado em "#", Ano, Dia, Dia do Ano e
  Semana do Mês viram Integer; Data Referência vira Date.
- **Descrição de calendário e município:** reaproveite as de um projeto
  maduro (as colunas são as mesmas).
- **Aspas:** o parser TMDL e a DAX Query View escapam aspas de forma diferente;
  a diferença é só de formatação, não de conteúdo.
- **Dados pessoais (LGPD):** descreva a coluna como dado protegido e peça que
  só seja exibida a quem tiver autorização.

## Validação barata
- **Tabular Editor 2** em linha de comando carrega a pasta TMDL e salva um
  `.bim`: serve como validador de sintaxe sem abrir o Desktop
  (`TabularEditor.exe <definition> -B saida.bim`).
- `scripts/check_visual_bindings.py` confirma que a tabela da página Sobre
  referencia colunas que existem.
