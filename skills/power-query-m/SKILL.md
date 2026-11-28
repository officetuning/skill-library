---
name: power-query-m
description: Boas práticas de Power Query M no Power BI — Query Folding, consultas em camadas (Cns) e grupos de consultas por papel, Incremental Refresh com RangeStart/RangeEnd, funções personalizadas M (nome Grupo.Acao, padrão de código, documentação com Value.ReplaceType, uso, desempenho e teste) e tratamento de erro auditável. Use quando o usuário citar refresh lento pelo lado do ETL, "query folding", "exibir consulta nativa", função M, função personalizada, invocar função, grupo de consultas, Table.Buffer, incremental refresh, erro na transformação ou consulta com passos demais. Não use para otimização do modelo semântico ou DAX (use powerbi-boas-praticas).
---

# Power Query M

Camada entre a origem dos dados e o modelo semântico. Metade dos problemas de
refresh lento nasce aqui e ninguém olha primeiro.

## Pergunta central

> Essa transformação pode ser feita na fonte, ou precisa mesmo acontecer aqui?

Power Query é o lugar de **tratar**, não de **processar**. Agregação, junção de
tabelas grandes e filtro sobre milhões de linhas vão para a fonte (SQL, view
semântica). Sobra para o M: tipagem, renomeação para o nome semântico,
tratamento de nulo e erro, e combinação de fontes que a origem não combina
sozinha.

## Regras

**Obrigatório**
- Verificar Query Folding em toda consulta sobre fonte relacional. Perder o
  folding no meio faz a máquina local processar linha a linha, e o refresh sai
  de minutos para horas.
- Consulta **não carregada** com nome formal: `Cns` no preparo, `Lista` na
  consulta que devolve lista, `Grupo.Acao` na função. Consulta **carregada** é a
  tabela do modelo e leva nome de negócio (`Vendas`, `Cliente`). Nomes seguem
  a skill `bi-nomenclatura`.
- Toda consulta num **grupo de consultas** pelo papel: Funções, Parâmetros,
  Internas, Dimensões, Fatos, Monolíticas, Pontes, Listas; o preparo fica no
  subgrupo `<Grupo>/Preparo` (ex.: `Dimensões/Preparo`). O grupo vai para o
  TMDL (`queryGroup`) e a documentação automática lê o papel dele.
- Conferir no catálogo de funções (`references/funcoes-m.md`) antes de escrever
  uma transformação nova. Não invente função.
- Documentar toda função reutilizável com metadados via `Value.ReplaceType`.
  Nunca entregue função "nua". Nome, padrão de código, documentação, uso,
  desempenho e teste de funções: `references/funcoes-personalizadas-m.md`.
- Corrigir erro na causa. Nunca mascare com `try ... otherwise` sem isolar as
  linhas descartadas.

**Preferir**
- Três camadas por tabela: Staging → Tratamento → Final.
- `Table.Buffer` só antes de operação não dobrável reaproveitada por várias
  consultas-filhas. Nunca "por garantia".
- Parâmetros (`RangeStart`, `RangeEnd`, ambiente, caminho) como Parâmetros de
  Consulta nomeados, nunca valor fixo dentro de um passo.
- "Selecionar Colunas" quando se mantêm poucas colunas: a consulta sobrevive a
  colunas novas na fonte sem trazer lixo.

**Evitar**
- Mais de ~40–50 passos numa consulta sem quebrar em consultas intermediárias.
- `Table.Buffer` no início da consulta: trava a árvore em memória e impede o
  folding no resto.
- Filtro de data com valor fixo (`= #date(2024,1,1)`) em vez dos parâmetros de
  Incremental Refresh: funciona no Desktop, mas não particiona no Service.

## Query Folding

Folding é o Power Query traduzir os passos numa única instrução executada na
fonte (ex.: um SELECT), em vez de baixar tudo e filtrar localmente.

**Como achar o passo que quebrou:**
1. Clique com o botão direito no último passo aplicado.
2. Se **Exibir Consulta Nativa** estiver ativo, ainda dobra até ali.
3. Suba passo a passo até o primeiro em que a opção fica cinza. Esse passo
   quebrou o folding.

Os indicadores de folding no painel de passos mostram o mesmo sem clicar.

**O que costuma quebrar** (varia por conector):
- Transformação de texto complexa (ex.: `Text.Combine` sobre várias colunas).
- `Table.AddColumn` com função customizada que o conector não traduz.
- Ordenar antes de filtrar. Inverta a ordem quando der.
- Mesclar consultas de fontes diferentes.
- `Table.Buffer`, sempre.

**Regra prática:** toda transformação pesada acontece **antes** do primeiro
passo que quebra o folding. Depois dele, só tipagem final e renomeação.

Docs: [Query folding](https://learn.microsoft.com/pt-br/power-query/power-query-folding) ·
[Indicadores](https://learn.microsoft.com/pt-br/power-query/query-folding-indicators)

## Padrão de camadas

| Camada | Exemplo de nome | Grupo | Carrega no modelo? | Faz |
|---|---|---|---|---|
| Staging | `CnsClienteStaging` | `Dimensões/Preparo` | Não | Extração crua, 100% dobrável |
| Tratamento | `CnsClienteTratado` | `Dimensões/Preparo` | Não | Tipagem, renomeação para o nome amigável, nulo, duplicata |
| Final | `Cliente` | `Dimensões` | Sim | Referencia o Tratamento |

Desmarque **Habilitar carregamento** em Staging e Tratamento. Vantagens: debug
por camada, reuso do mesmo Staging por várias tabelas finais e isolamento da
quebra de folding na camada de Tratamento.

## Incremental Refresh

Particiona a tabela por faixas de data e atualiza só as recentes. Suportado em
Pro, PPU, Premium e Embedded. As partições reais só existem depois de publicar
no Service; no Desktop os parâmetros apenas filtram uma janela pequena.

Parâmetros com nomes **exatos**, tipo Data/Hora:

```m
// Valores iniciais quaisquer: a política sobrescreve ao publicar
RangeStart = #datetime(2024, 1, 1, 0, 0, 0) meta [IsParameterQuery = true, Type = "DateTime", IsParameterQueryRequired = true]
RangeEnd   = #datetime(2024, 1, 2, 0, 0, 0) meta [IsParameterQuery = true, Type = "DateTime", IsParameterQueryRequired = true]
```

Filtro na consulta, logo após a origem para dobrar:

```m
= Table.SelectRows(
    CnsVendaTratado,
    // >= em um lado e < no outro: evita linha duplicada entre partições
    each [Data da Venda] >= RangeStart and [Data da Venda] < RangeEnd
)
```

| Campo da política | Define |
|---|---|
| Arquivar dados a partir de | Histórico retido sem reprocessar |
| Atualizar incrementalmente a partir de | Janela "quente" refeita a cada refresh |
| Detectar alterações de dados (opcional) | Coluna de última modificação na fonte |
| Atualizar só períodos completos | Não reprocessa o dia corrente aberto |

Docs: [Incremental refresh](https://learn.microsoft.com/pt-br/power-bi/connect-data/incremental-refresh-overview)

## Janela de histórico (últimos N anos)

Antes de limitar datas, ou de apontar um limite como erro, leia
`references/janela-de-historico.md`: regra em um só lugar, fim exclusivo, o que o
Incremental Refresh não resolve e a virada automática.

## Pasta com vários arquivos

Antes de combinar arquivos de uma pasta, remover duplicatas ou fixar o fim do
período, leia `references/pasta-com-varios-arquivos.md`: cabeçalho do primeiro
arquivo, sobreposição entre arquivos, medição antes do `Table.Distinct` e data
final que expira.

## Aspas no M

Consulta com espaço ou acento no nome se referencia com `#"..."`:
`#"Calendário"`. Campo entre colchetes aceita espaço e acento sem aspas:
`[Data da Venda]`. Renomear colunas não quebra o folding.

## Função documentada e tratamento de erro

Modelos prontos em `references/padroes-m.md`:
- função com `Value.ReplaceType` completo (nome, descrição, categoria, exemplo);
- padrão de auditoria de erro que isola as linhas que falharam, em vez de
  descartá-las em silêncio.

## Checklist final

- [ ] Consulta relacional com "Exibir Consulta Nativa" ativo até o passo mais tardio possível
- [ ] Nenhum `Table.Buffer` no início de consulta
- [ ] Camadas Staging → Tratamento → Final, com as duas primeiras sem carregamento
- [ ] Preparo com `Cns`, listas com `Lista`, funções em `Grupo.Acao`; consulta carregada com nome de negócio
- [ ] Toda consulta no grupo do seu papel, preparo em `<Grupo>/Preparo`
- [ ] Toda função com consulta de teste (`references/funcoes-personalizadas-m.md`)
- [ ] `RangeStart`/`RangeEnd` em toda fato de volume relevante
- [ ] Funções reutilizáveis documentadas com `Value.ReplaceType`
- [ ] Nenhum `try ... otherwise` sem isolar as linhas afetadas
- [ ] Nenhuma função inventada (confira `references/funcoes-m.md`)
- [ ] Consultas com mais de ~40–50 passos avaliadas para quebra
