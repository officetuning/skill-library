# Prompts para dashboard HTML com IA

Copie, troque o que está entre colchetes e envie **em etapas**. Pedir perfil,
números e painel numa mensagem só é o jeito mais rápido de receber um painel
bonito com número errado.

## 1. Perfil (todas as IAs)

```text
Leia o arquivo [nome] (aba/tabela [nome]). Não faça gráfico ainda.
Rodando código, me devolva:
- colunas, tipo de cada uma e 3 exemplos de valor;
- período coberto (data mínima e máxima) e número de linhas;
- nulos e duplicados por coluna;
- categorias com grafia diferente (ex.: "SP" e "São Paulo");
- separador, decimal e codificação, se for CSV;
- total de controle: soma de [coluna de valor] na fonte bruta, com 2 casas.
Se algo estiver ambíguo, pergunte antes de seguir.
```

Confira o total de controle na planilha. Só siga com o "ok".

## 2. Números (todas as IAs)

```text
Ok, o total confere. Agora, rodando código:
- KPIs: [Receita AV = soma de receita no ano selecionado;
         Receita AA = mesma soma nos mesmos meses do ano anterior;
         Δ% = (AV − AA) ÷ AA; Ticket médio = Receita ÷ Pedidos].
- Agregue por [mês] × [região] e me mostre a tabela agregada.
- Confirme que a soma da tabela agregada = total de controle.
```

## 3. Painel (prompt mestre)

```text
Gere um dashboard em HTML de arquivo único com os dados agregados acima.

Público: [quem] · Pergunta: [qual] · Filtros: [ano, região]

Contrato:
- Dados em <script type="application/json" id="dados"> com meta (titulo,
  fonte, extraido_em AAAA-MM-DD, linhas_fonte, total_controle) e linhas.
- Rodapé: fonte, "Dados de dd/mm/aaaa", linhas e conferência do total
  ("✔ confere" / "⚠ diverge"), calculada no navegador.
- Tudo calculado em JavaScript a partir dos dados; nenhum número digitado.
- pt-BR com Intl.NumberFormat (R$, 1.234,56, %); datas sem fuso (ler
  AAAA-MM-DD como texto, não com new Date()).
- Topo: 3 a 5 KPIs com ▲/▼ e sinal, não só cor. Um gráfico de linha AV × AA
  por mês, barras horizontais ordenadas por região, tabela ordenável com total.
- Subtítulo como conclusão, gerado pelo código a partir dos números.
- Texto vindo dos dados inserido com textContent, nunca innerHTML.
- Acessível (contraste AA, aria-label nos gráficos, foco visível), responsivo
  sem rolagem horizontal no celular, modo escuro, estilo de impressão,
  espaçamento em múltiplos de 8 px.
- Chart.js 4.6.1 por cdn.jsdelivr.net com versão fixa; se não carregar,
  KPIs e tabela continuam e aparece um aviso.
- Não invente dados. Sem dado pessoal linha a linha.
```

Com a skill `dashboard-html-ia` instalada, basta: *"Gere o dashboard seguindo a
skill dashboard-html-ia, a partir do template."*

## 4. Conferência (cole o HTML gerado ou abra o artefato)

```text
Revise este dashboard como auditor, sem reescrever ainda:
1. A soma das linhas embutidas bate com meta.total_controle?
2. Sorteie 3 combinações (mês × região) e compare com a fonte.
3. Algum número está escrito à mão no HTML em vez de calculado?
4. Há innerHTML com texto vindo dos dados?
5. Datas usam new Date("AAAA-MM-DD")? (erro de fuso)
6. AA compara os mesmos meses do AV?
7. Há dado pessoal, e-mail, CPF, token ou URL privada no arquivo?
Liste o que falhou e só depois proponha a correção.
```

---

## Ajustes por plataforma

### Microsoft 365 Copilot — Analyst

```text
[Anexe o arquivo do OneDrive pelo + → Attach content]
Use o prompt 1 e depois o 2. Mostre o código Python de cada cálculo.
No final: gere um arquivo .html único para download com o contrato abaixo.
Se não puder gerar o arquivo, mostre o código HTML completo num bloco.
[cole o prompt 3]
```

### Microsoft 365 Copilot — Copilot Code (Frontier)

```text
Construa um dashboard para [equipe] a partir de [arquivo do OneDrive/SharePoint].
Antes de construir, me mostre colunas, período e total de [coluna].
Siga este contrato: [cole o prompt 3].
Quando eu aprovar a prévia, publique e compartilhe só com [grupo].
```

Peça "publish it" só depois de conferir. Compartilhar o app não compartilha o
dado: cada pessoa vê o que já pode ver na fonte.

### Google Sheets — Sheets canvas

Conta com idioma em inglês. Prompt curto, em inglês, na própria planilha:

```text
Create an interactive dashboard from the "[tab]" tab: KPI cards for total
revenue, revenue vs same months last year (%), orders and average ticket;
a monthly line chart this year vs last year; a horizontal bar chart of revenue
by region sorted descending; filters for year and region. Format currency as
BRL (R$ 1.234,56) and dates as dd/mm/yyyy. Do not invent data.
```

### Gemini — Canvas no app

```text
[Selecione Canvas e anexe a planilha do Drive]
Primeiro, resuma cada aba e me dê o total de [coluna]. Não crie o app ainda.
```

Depois do "ok", cole o prompt 3. Antes de compartilhar o link público, lembre
que ele dá acesso para ver e editar os dados do app.

### Claude

```text
[Anexe o arquivo ou cite o caminho no Google Drive / OneDrive]
Perfile e me mostre o total de controle. Depois gere o dashboard como artefato
seguindo a skill dashboard-html-ia, a partir do template.
```

Dado em warehouse (BigQuery, Snowflake, Databricks...): *"Crie um Claude
Dashboard que responda [pergunta]"* e abra a consulta de cada gráfico para
conferir.

### ChatGPT

```text
[Anexe o arquivo ou o link exato da planilha do Drive/OneDrive]
Use análise de dados: prompt 1, depois prompt 2.
Snapshot: gere o .html único com o contrato [prompt 3] para eu baixar.
Recorrente: publique como Site privado e crie uma tarefa agendada que confira
a planilha em dias úteis, atualize o painel e me avise só se [condição].
```
