# Ano fiscal: calendário, ano em foco e orçamento

Para ano fiscal que não coincide com o civil (exemplo: setembro a agosto, nomeado
pelo ano em que termina). Padrões usados num relatório de Real × Orçamento; os
nomes abaixo são de exemplo.

## Colunas do calendário
Ordene cada texto pela coluna numérica correspondente.

| Coluna | Início em setembro |
|---|---|
| `Ano Fiscal #` | `Ano + IF ( Mês >= 9, 1, 0 )` |
| `Ano Fiscal` | `"FY" & ` últimos dois dígitos |
| `Mês Fiscal #` | `MOD ( Mês + 3, 12 ) + 1` (setembro = 1) |
| `Trimestre Fiscal` | `ROUNDUP ( Mês Fiscal # / 3, 0 )` |

Orçamento em colunas `P01`…`P12`: P01 é o primeiro mês **fiscal**; converta para
data no Power Query para relacionar ao calendário.

## Ano em foco (o relatório não abre vazio)
Sem seleção, use o último ano com realizado, não o último do calendário (o ano novo
costuma estar sem dados).

```dax
Ano Fiscal em Foco =
VAR vVisiveis = COUNTROWS ( VALUES ( 'Calendário'[Ano Fiscal #] ) )
VAR vTodos = COUNTROWS ( ALL ( 'Calendário'[Ano Fiscal #] ) )
VAR vUltimaData =
    CALCULATE ( MAX ( 'Vendas'[Data] ), REMOVEFILTERS (), 'Vendas'[Valor] <> 0 )
VAR vAnoComDados = YEAR ( vUltimaData ) + IF ( MONTH ( vUltimaData ) >= 9, 1, 0 )
RETURN
    IF ( vVisiveis = vTodos, vAnoComDados, MAX ( 'Calendário'[Ano Fiscal #] ) )
```

## Ano anterior nos mesmos meses
Limite o ano anterior aos meses que já têm realizado no ano em foco. Se o ano em
foco não tem nada, mostre o anterior inteiro como base e deixe a variação vazia.

## Orçamento
- **Atingimento e desvio** usam o orçamento **só dos meses com realizado**; o
  orçamento do ano inteiro é a meta (chegada), outra medida.
- Atributo que só existe no realizado (nome do item, classificação): com filtro
  nele, o orçamento deve ficar **vazio** (`ISFILTERED`), senão compara um recorte do
  realizado com o orçamento inteiro.
- Sem um dos lados, atingimento e desvio ficam vazios (não zero, não 100%).

## Medidas com ano fixo
Cartões "FY25, FY26, FY27" precisam de ano gravado na medida: registre que cada ano
novo exige medidas novas, ou use medidas relativas ao ano em foco.

## Teste
Calcule os valores esperados **fora do Power BI** (direto da fonte) e entregue uma
consulta `EVALUATE` com o esperado ao lado de cada resultado, incluindo o ano sem
dados e um mês no meio do ano.
