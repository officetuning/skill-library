# Check-up do banco SQL Server que alimenta o modelo

Para quando o modelo lê views ou tabelas de um SQL Server e o pedido é auditar o
projeto inteiro, ou quando o refresh é lento e a causa parece estar na origem.

⚠️ As consultas de leitura abaixo foram executadas em um SQL Server 2017 (14.x) e em
um LocalDB 17.0 (SQL Server 2025). Confira em outras versões.

## Antes de consultar

- **Somente leitura.** Metadados primeiro; consulta pesada em tabela grande só com
  motivo, fora da janela de carga da origem.
- Diga ao usuário com que conta está conectado. Conta `sysadmin` ou `db_owner` em
  produção é um achado, e pede ainda mais cuidado.
- Confira a coluna **Permissão** abaixo. Sem ela, algumas consultas dão erro, mas
  outras devolvem **menos linhas, nenhuma linha ou NULL em silêncio** (tamanhos,
  permissões e `OBJECT_DEFINITION`). Com conta restrita, resultado vazio ou NULL é
  **não verificado, não "ausente"**. Testado no LocalDB com um login que só tinha
  `SELECT` no esquema, concedendo um direito por vez.
- Não leia linhas com dado pessoal: contagens, somas e metadados bastam.

## O que olhar

Troque `bi` pelo esquema que o modelo consome.

| # | Item | Permissão | O que costuma ser achado |
|---|---|---|---|
| 1 | Versão e opções do banco | acesso ao banco | Nível de compatibilidade antigo, sem atualização cumulativa, Query Store desligado |
| 2 | Backup | leitura no `msdb` | Sem backup recente |
| 3 | Tamanhos e índices | `VIEW DATABASE STATE` e `VIEW DEFINITION` | Tabela grande sem índice agrupado (heap), índices gerados em massa, colunas `char` largas |
| 4 | Dependências das views | `VIEW DEFINITION` e `SELECT` em `sys.sql_expression_dependencies` (sem o `SELECT`, erro 229) | View sobre view relendo a mesma tabela grande |
| 5 | Tempos e leituras | `VIEW SERVER STATE` | View que leva minutos ou lê muitas vezes o tamanho da tabela |
| 6 | Permissões | `VIEW DEFINITION` (filtra em silêncio) | Nenhum `GRANT` no esquema: quem lê precisa de direito amplo |
| 7 | Scripts de instalação | só o repositório | `DELETE` ou `TRUNCATE` sem trava, carga que apaga o que foi editado à mão, sem transação |

### 1 e 2. Ambiente

```sql
SELECT SERVERPROPERTY('ProductVersion') AS versao, SERVERPROPERTY('Edition') AS edicao;

SELECT compatibility_level, recovery_model_desc, is_query_store_on,
       is_read_committed_snapshot_on, is_auto_shrink_on, page_verify_option_desc
FROM sys.databases WHERE name = DB_NAME();

SELECT type, MAX(backup_finish_date) AS ultimo
FROM msdb.dbo.backupset WHERE database_name = DB_NAME() GROUP BY type;
```

### 3. Tamanhos e índices

```sql
SELECT s.name AS esquema, t.name AS tabela,
       SUM(CASE WHEN p.index_id IN (0, 1) THEN p.row_count ELSE 0 END) AS linhas,
       SUM(p.reserved_page_count) * 8 / 1024 AS mb,
       MIN(p.index_id) AS menor_indice            -- 0 = heap
FROM sys.dm_db_partition_stats AS p
JOIN sys.tables  AS t ON t.object_id = p.object_id
JOIN sys.schemas AS s ON s.schema_id = t.schema_id
GROUP BY s.name, t.name
ORDER BY mb DESC;
```

### 4. Dependências

```sql
SELECT OBJECT_NAME(d.referencing_id) AS objeto, d.referenced_database_name AS banco,
       d.referenced_schema_name AS esquema, d.referenced_entity_name AS referencia
FROM sys.sql_expression_dependencies AS d
WHERE OBJECT_SCHEMA_NAME(d.referencing_id) = 'bi'
ORDER BY objeto, referencia;
```

### 5. Tempos no cache de planos

```sql
SELECT TOP (20) qs.execution_count AS execucoes,
       qs.total_elapsed_time  / qs.execution_count / 1000000.0 AS seg_medio,
       qs.total_logical_reads / qs.execution_count * 8 / 1024  AS mb_lidos,
       qs.last_execution_time AS ultima, LEFT(t.text, 150) AS consulta
FROM sys.dm_exec_query_stats AS qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) AS t
WHERE t.text LIKE '%bi%.%Vw%' AND t.text NOT LIKE '%dm_exec%'
ORDER BY seg_medio DESC;
```

O cache zera quando o servidor reinicia e perde entradas por pressão de memória.
Depois de um `ALTER VIEW`, a linha antiga ainda aparece até a consulta rodar de novo;
aí a contagem recomeça (visto no LocalDB). O tempo decorrido inclui a entrega das
linhas ao cliente; leitura lógica é o indicador mais estável.

### 6. Permissões

```sql
SELECT pr.name AS quem, dp.permission_name AS permissao, dp.class_desc AS escopo
FROM sys.database_permissions AS dp
JOIN sys.database_principals AS pr ON pr.principal_id = dp.grantee_principal_id
WHERE (dp.class = 3 AND dp.major_id = SCHEMA_ID('bi'))
   OR (dp.class = 1 AND OBJECT_SCHEMA_NAME(dp.major_id) = 'bi');

SELECT IS_SRVROLEMEMBER('sysadmin') AS sou_sysadmin, IS_MEMBER('db_owner') AS sou_db_owner;
```

## Entrega

Uma tabela com identificador, severidade, achado, **evidência medida**, correção e
esforço. Separe o que é do projeto do que é do dono do banco ou da carga, e liste o
que não foi verificado.

## Aceite de mudança em view

1. **Guarde as definições atuais** antes de alterar e confira que batem com o
   repositório: `SELECT OBJECT_DEFINITION(OBJECT_ID('bi.VwFatVenda'));`. Textos longos
   são cortados sem aviso no `sqlcmd` padrão (256 caracteres) e na grade do SSMS (não
   testado aqui):
   salve com `sqlcmd -y 0 -o definicoes.sql` ou com "Gerar script como". Anote também
   os tempos do item 5 **antes de alterar**.
2. **Compare o SQL novo sem instalar:** rode o corpo da view nova como consulta,
   para uma tabela temporária, e compare com a view atual por período: linhas,
   somas e chaves duplicadas.
3. **Meça com todas as colunas.** Selecionar duas ou três deixa o otimizador pular
   trabalho: em um caso, a mesma consulta caiu de 29 s para 6 s só pela projeção
   estreita, e a comparação levou a procurar uma regressão que não existia.
4. **Mesmo script antes e depois**, na mesma carga da origem. Fontes de fotografia
   (saldo, pendência) mudam entre cargas.
5. **Instale em transação**, em um script que altera só o necessário: reexecutar a
   instalação completa pode apagar dado mantido à mão. Como cada view pede um lote
   próprio (`GO`), a transação **não basta**: sem parar no primeiro erro, o `sqlcmd`
   segue com os lotes seguintes em autocommit, depois de a transação ter sido desfeita, e
   ainda pode terminar com código 0 (reproduzido com tabelas temporárias).
   Comece o script com `:on error exit` (ou rode com `sqlcmd -b`), use
   `SET XACT_ABORT ON` e `BEGIN TRANSACTION`, e confira o que ficou instalado.

⚠️ No `sqlcmd`, a variável dentro de `:r` **entre aspas** (`:r "$(PASTA)\arquivo.sql"`)
não foi substituída; **sem aspas** (`:r $(PASTA)\arquivo.sql`) funcionou com `-v` e com
`:setvar` (cliente 15.0, caminho sem espaços). Com espaços no caminho, use caminho
relativo, rodando de dentro da pasta. Teste antes com um arquivo inofensivo.
