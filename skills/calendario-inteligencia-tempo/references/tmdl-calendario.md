# Script TMDL do calendário 'Gregoriano'

Para o Calendário do Background Builder 1.033 ou mais novo. Cole na **TMDL
view** (nova guia, colar, **Aplicar**) com a prévia ligada. O script só
acrescenta o calendário à tabela existente (`ref table`); não altera colunas,
medidas nem a partição.

Os nomes das categorias (`year`, `quarterOfYear`…) são os do enum `TimeUnit`
do TOM em camelCase, como no exemplo oficial (`year`, `month`, `date`). Um
bloco `calendarColumnGroup` sem categoria marca as colunas como
**relacionadas ao tempo**.

```tmdl
createOrReplace

	ref table Calendário

		/// Calendário gregoriano do Background Builder, para a inteligência de tempo baseada em calendário.
		/// Semestre, Quinzena e Estação são relacionadas ao tempo; Fim de Semana fica fora do calendário de propósito.
		calendar Gregoriano

			calendarColumnGroup = year
				primaryColumn: Ano

			calendarColumnGroup = quarter
				primaryColumn: 'Ano/Trimestre'

			calendarColumnGroup = quarterOfYear
				primaryColumn: 'Trimestre #'
				associatedColumn: Trimestre

			calendarColumnGroup = month
				primaryColumn: 'Ano/Mês'
				associatedColumn: 'Ano/Mês (Abreviado)'

			calendarColumnGroup = monthOfYear
				primaryColumn: 'Mês #'
				associatedColumn: Mês
				associatedColumn: 'Mês (Abreviado)'

			calendarColumnGroup = monthOfQuarter
				primaryColumn: 'Mês do Trimestre'

			calendarColumnGroup = week
				primaryColumn: 'Ano/Semana'

			calendarColumnGroup = weekOfYear
				primaryColumn: 'Semana #'
				associatedColumn: Semana

			calendarColumnGroup = weekOfMonth
				primaryColumn: 'Semana do Mês'

			calendarColumnGroup = date
				primaryColumn: Data
				associatedColumn: 'Data (AAAAMMDD)'
				associatedColumn: 'Data (ddd dd/mm/aaaa)'

			calendarColumnGroup = dayOfYear
				primaryColumn: 'Dia do Ano'

			calendarColumnGroup = dayOfMonth
				primaryColumn: Dia

			calendarColumnGroup = dayOfWeek
				primaryColumn: 'Dia da Semana #'
				associatedColumn: 'Dia da Semana'
				associatedColumn: 'Dia da Semana (Abreviado)'

			calendarColumnGroup
				column: 'Semestre #'
				column: Semestre
				column: 'Quinzena #'
				column: Quinzena
				column: 'Estação #'
				column: Estação
				column: 'Estação Cor'
```

## Calendário de versão anterior do Builder

Sem `Ano/Semana` e `Mês do Trimestre` (Builder até 1.032), apague os blocos
`week` e `monthOfQuarter`. As funções semanais continuam possíveis pelo par
`weekOfYear` + `year` (validação de unicidade do período), mas a coluna completa
`Ano/Semana` é mais robusta.

Até o 1.032, `Ano/Mês (Abreviado)` também não ordena por `Ano/Mês`. Ajuste
antes de aplicar, na interface: selecione a coluna › Ferramentas de coluna ›
Classificar por coluna › `Ano/Mês`. Não use `createOrReplace` numa coluna só
para mudar a ordenação: ele substitui a definição inteira da coluna.

## Semestre como categoria

O TOM tem `semester` e `semesterOfYear`, mas a tela de categorias e a
documentação do Power BI ainda não listam semestre. Por isso o Semestre vai
como relacionado ao tempo. Se uma versão nova do Desktop mostrar Semestre nas
categorias, troque por:

```tmdl
			calendarColumnGroup = semesterOfYear
				primaryColumn: 'Semestre #'
				associatedColumn: Semestre
```

## Conferência depois de aplicar

```dax
EVALUATE INFO.CALENDARS ()
```

Deve devolver uma linha `Gregoriano`. Depois, em **Opções de calendário ›
Editar › Validar dados**, as validações offline conferem: nada em branco,
Ano → Mês um-para-muitos, `Ano/Mês` um-para-um com (`Mês #`, `Ano`) e cada
associada um-para-um com a principal.
