# Eixo temporal: respeitar o filtro de tempo ou editar as interações

Regra do autor, confirmada em dois relatórios (um comercial e um de RH, nov/2026),
ambos montados com o Background Builder, cuja barra lateral traz a segmentação de
data relativa em todas as páginas de corpo. **[verificado]** = visto em arquivo
gravado pelo Desktop.

## O problema
A segmentação de data padrão do relatório é relativa: **"Este ano a partir da
última data"**. Um gráfico cujo **eixo é tempo** pode **perder o sentido** sob esse
filtro:

- colunas por **Ano** viram uma coluna só;
- matriz "ano a ano" mostra um ano;
- área 100% por Ano mostra uma fatia de ano;
- gráfico por **Tempo de Casa**: a data chega à fato pela **data de Entrada**, então
  "Este ano" deixa só quem entrou neste ano e a curva de tempo de casa some.

**"Eixo de tempo" inclui o Calendário e também o Tempo de Casa** (e qualquer campo
que meça tempo decorrido a partir da mesma data que o filtro usa). Tempo de Casa
como coluna de tabela ou como valor de cartão não conta: só quando é o **eixo**.

## Decisão: respeitar ou ignorar?
Decida **gráfico a gráfico**, com a pergunta: *o recorte do período é o assunto
deste gráfico?*

| Granularidade do eixo | Decisão | Exemplo |
|---|---|---|
| **Mês (ou dia) dentro do período** | **Respeitar** o filtro | Linha AV × AA por mês; vendas e entregas por mês |
| **Ano**, ou comparação entre anos | **Ignorar** a segmentação de data | Colunas por Ano; matriz "ano a ano"; participação por ano |
| **Tempo de Casa** como eixo | **Ignorar** a segmentação de data | Ativos por Tempo de Casa |

Ignorar significa que **só a segmentação de data** deixa de filtrar o visual. As
outras (Região, Unidade, Canal...) continuam valendo.

## Como gravar (editar interações)
No `page.json` da página, em `visualInteractions`, uma entrada por par origem →
destino com `type: "NoFilter"`:

```json
"visualInteractions": [
  { "source": "<name da segmentação de data>", "target": "<name do gráfico>", "type": "NoFilter" }
]
```

- `source` e `target` são o campo `name` do `visual.json` (o nome completo, 20
  caracteres, não o prefixo da pasta). **[verificado]**
- O comportamento padrão (`DataFilter`) não precisa de entrada. Se a página já tem
  entradas, acrescente a nova sem apagar as outras.
- Na interface: selecionar a segmentação › **Formato › Editar interações** › no
  gráfico, ícone "Nenhum".

## Medida de período continua certa?
Medida que usa `MIN`/`MAX` do calendário no contexto de filtro (por exemplo,
`Contratados no Período`) continua correta por Ano quando o **eixo é o próprio Ano**:
cada coluna cria o seu contexto. Com a segmentação de data ignorada, cada ano
aparece inteiro.

## Revisão de um projeto
1. Liste os visuais com campo do Calendário (ou de tempo) em **Categoria/Eixo/Linhas**.
2. Classifique cada um pela tabela acima.
3. Grave as interações dos que ignoram a data e anote os que respeitam, com o motivo.
4. Teste no Desktop com "Este ano" ligado: o gráfico ainda diz alguma coisa?
