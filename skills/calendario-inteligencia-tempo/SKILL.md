---
name: calendario-inteligencia-tempo
description: Inteligência de tempo no Power BI a partir do Calendário do Background Builder — detecta se a inteligência de tempo baseada em calendário (prévia "Enhanced DAX Time Intelligence") está disponível; se estiver, define o calendário 'Gregoriano' em TMDL (categorias Ano, Trimestre, Mês, Semana, Data e colunas relacionadas ao tempo) e escreve as medidas com a referência ao calendário; se não, garante "Marcar como tabela de data" pela coluna Data e usa a inteligência de tempo clássica. Medidas (AV)/(AA)/(Δ), YTD/QTD/MTD/WTD, 12 meses móveis, DATEADD com Extension/Truncation e UDF com CALENDARREF. Use ao criar comparativo com ano anterior, acumulado no ano, cálculo por semana, configurar tabela de datas ou calendário, TOTALYTD, SAMEPERIODLASTYEAR, DATEADD, DATESINPERIOD ou "inteligência de tempo".
---

# Calendário e inteligência de tempo

## Pergunta central

> As medidas de tempo deste modelo usam o calendário mais capaz que o
> Power BI do usuário aceita, e a mesma medida dá o mesmo número no
> Desktop e no Service?

Há dois modos. A skill escolhe sozinha, nesta ordem:

| Modo | Quando | Referência nas medidas |
|---|---|---|
| **Calendário** (prévia) | A prévia está disponível (detecção abaixo) | `'Gregoriano'` (o calendário) |
| **Clássico** | Qualquer outro caso | `'Calendário'[Data]` (tabela marcada) |

A Microsoft recomenda o modo calendário: funciona com qualquer calendário,
aceita datas faltando, tem funções semanais (`TOTALWTD`) e é mais rápido em
alguns visuais. O modo clássico continua válido e é o plano B.

## 1. Detectar o modo

Pare no primeiro passo que responder:

1. **O modelo já tem calendário?** Procure `calendar ` nos `.tmdl` do PBIP
   (em `definition/tables/Calendário.tmdl`) ou rode `EVALUATE INFO.CALENDARS()`
   na DAX Query View / MCP. Tem linha → **modo calendário**.
2. **Nível de compatibilidade.** Calendário exige compatibilidade **1701 ou
   maior**. Leia `compatibilityLevel` em `definition/database.tmdl`. Abaixo de
   1701 → **modo clássico** (e diga ao usuário como ligar a prévia, abaixo).
3. **Teste real, com o modelo aberto** (MCP ou TMDL view): aplique o script do
   calendário (`references/tmdl-calendario.md`) dentro de uma transação, ou na
   TMDL view. Aplicou sem erro → **modo calendário**. Erro dizendo que o objeto
   ou a propriedade não é reconhecida → desfaça e use o **modo clássico**.
4. **Edição offline do PBIP sem como testar:** pergunte ao usuário uma vez se
   a prévia está ligada. Sem resposta → **modo clássico**, que nunca quebra.

Ligar a prévia (o usuário faz): **Arquivo › Opções e configurações › Opções ›
Recursos de visualização › Inteligência de tempo DAX aprimorada** e reiniciar
o Desktop. Exige o Desktop de setembro de 2025 (2.147) ou mais novo.

## 2. Modo calendário

1. Confira se o Calendário tem as colunas da tabela abaixo (Builder 1.033 ou
   mais novo). Faltando `Ano/Semana` ou `Mês do Trimestre`, tire do script as
   categorias `week` e `monthOfQuarter`: o resto funciona.
2. Com o PBIP versionado (commit antes), aplique o script de
   `references/tmdl-calendario.md` na TMDL view (ou via MCP, com
   `powerbi-mcp`). Não mexe em nenhuma coluna; só acrescenta o calendário.
3. Em **Opções de calendário › Editar › Validar dados**, rode as validações
   offline e trate os avisos.
4. Escreva as medidas com `'Gregoriano'` (`references/medidas.md`).
5. Mantenha também a tabela **marcada como tabela de data**: os dois modos
   convivem, e medidas antigas com `'Calendário'[Data]` continuam funcionando.

### Mapa do Calendário do Builder

| Categoria | Coluna principal | Associadas |
|---|---|---|
| Ano | `Ano` | — |
| Trimestre | `Ano/Trimestre` | — |
| Trimestre do Ano | `Trimestre #` | `Trimestre` |
| Mês | `Ano/Mês` | `Ano/Mês (Abreviado)` |
| Mês do Ano | `Mês #` | `Mês`, `Mês (Abreviado)` |
| Mês do Trimestre | `Mês do Trimestre` | — |
| Semana | `Ano/Semana` | — |
| Semana do Ano | `Semana #` | `Semana` |
| Semana do Mês | `Semana do Mês` | — |
| Data | `Data` | `Data (AAAAMMDD)`, `Data (ddd dd/mm/aaaa)` |
| Dia do Ano | `Dia do Ano` | — |
| Dia do Mês | `Dia` | — |
| Dia da Semana | `Dia da Semana #` | `Dia da Semana`, `Dia da Semana (Abreviado)` |
| **Relacionadas ao tempo** | `Semestre #`, `Semestre`, `Quinzena #`, `Quinzena`, `Estação #`, `Estação`, `Estação Cor` | |
| **Fora do calendário** | `Fim de Semana`, `Hemisfério`, `Localidade do Projeto` | |

Por que assim:
- **Relacionadas ao tempo** perdem o filtro nas funções que mudam de nível
  (`TOTALYTD`, `PARALLELPERIOD`…). Sem isso, um acumulado no ano com Semestre
  na linha sairia cortado só no semestre.
- **Fora do calendário** mantém o filtro: "fins de semana do ano anterior"
  continua só fim de semana. `Hemisfério` e `Localidade` são constantes.
- Coluna principal precisa ordenar certo. `Ano/Mês` ("2026/03") e
  `Ano/Semana` ("2026/S05") ordenam como texto; os nomes ordenam pela
  coluna `#`.
- A semana do Builder é a do Power Query (`Date.WeekOfYear`): a semana 1 é a
  que contém 1º de janeiro, então a virada do ano parte a semana em duas. Não é
  semana ISO. Para varejo ou ISO, crie outro calendário com colunas próprias.

## 3. Modo clássico (plano B)

1. **Marcar como tabela de data** pela coluna `Data`. No TMDL é a tabela com
   `dataCategory: Time` e a coluna `Data` com `isKey` (o script do Builder já
   faz). Na interface: Ferramentas de tabela › Marcar como tabela de data ›
   `Data`.
2. `Data` sem lacunas entre a primeira e a última data (o Calendário do Builder
   é contínuo).
3. Medidas com `'Calendário'[Data]` (`references/medidas.md`, coluna clássica).
4. Sem `TOTALWTD`, `PREVIOUSWEEK` etc.; para semana, use filtro por
   `Ano/Semana` com `CALCULATE`.
5. Desligue **Data/hora automática** (Opções › Arquivo atual › Carregamento de
   dados) nos dois modos.

## 4. Medidas

Nome e sufixo seguem `bi-nomenclatura`: `(AV)`, `(AA)`, `(Δ)`, `(Δ%)`,
`(Δi)`; a medida mora na tabela de fatos. Padrões completos, nos dois modos,
em `references/medidas.md`:

```dax
-- modo calendário
Faturado (AA) = CALCULATE ( [Faturado (AV)], SAMEPERIODLASTYEAR ( 'Gregoriano' ) )
Faturado (YTD) = TOTALYTD ( [Faturado (AV)], 'Gregoriano' )

-- modo clássico
Faturado (AA) = CALCULATE ( [Faturado (AV)], SAMEPERIODLASTYEAR ( 'Calendário'[Data] ) )
Faturado (YTD) = TOTALYTD ( [Faturado (AV)], 'Calendário'[Data] )
```

Trocar de modo depois é só trocar a referência; a skill `powerbi-mcp` faz em
lote com segurança.

## 5. Limites da prévia (conferir a data no Microsoft Learn)

- Não aninhe funções de tempo com calendário:
  `PREVIOUSDAY ( PREVIOUSMONTH ( 'Gregoriano' ) )` falha; use
  `CALCULATETABLE ( PREVIOUSDAY ( 'Gregoriano' ), PREVIOUSMONTH ( 'Gregoriano' ) )`.
- Calendário em tabela de fatos com RLS pode dar resultado inesperado.
- Não funciona com conexão dinâmica nem modelo composto; ainda não se cria
  calendário no Service.
- Não use com Data/hora automática.
- Tabela com menos de 200 colunas; acima de 20 mil linhas não há validação
  offline (o Calendário do Builder tem cerca de 2,2 mil linhas).
- Cada coluna pertence a uma só categoria, e à mesma categoria em todos os
  calendários do modelo.
- `SAMEPERIODLASTYEAR` e `DATEADD` com calendário levam 29/02/2008 para
  01/03/2007 (60º dia do ano); o clássico leva para 28/02/2007. Para o
  comportamento clássico, desloque por mês: `DATEADD ( 'Gregoriano', -12, MONTH )`.
- O IntelliSense ainda não reconhece os parâmetros novos do `DATEADD`
  (`EXTENDING`, `PRECISE`, `ENDALIGNED`, `BLANKS`, `ANCHORED`); a medida
  funciona mesmo sublinhada.

## Ano fiscal e orçamento
Calendário que começa em outro mês, "ano em foco", ano anterior nos mesmos meses e orçamento
sob filtro que só existe no realizado: `references/ano-fiscal.md`.

## Checklist

1. Modo escolhido e registrado na descrição da tabela `Calendário` (`///`).
2. Data/hora automática desligada; tabela marcada como tabela de data.
3. No modo calendário: validações offline sem aviso.
4. Toda medida de tempo usa uma única referência (`'Gregoriano'` ou
   `'Calendário'[Data]`), sem misturar.
5. Teste com `EVALUATE` comparando AV e AA de um mês conhecido.

Fontes: [Implementar cálculos baseados em tempo](https://learn.microsoft.com/pt-br/power-bi/transform-model/desktop-time-intelligence) ·
[DATEADD](https://learn.microsoft.com/dax/dateadd-function-dax) ·
[DATESINPERIOD](https://learn.microsoft.com/dax/datesinperiod-function-dax) ·
[INFO.CALENDARS](https://learn.microsoft.com/dax/info-calendars-function-dax) ·
[TimeUnit (TOM)](https://learn.microsoft.com/dotnet/api/microsoft.analysisservices.tabular.timeunit)
