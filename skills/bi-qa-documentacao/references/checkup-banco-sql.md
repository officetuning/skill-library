# Check-up do banco SQL Server que alimenta o modelo

Para quando o modelo lê views ou tabelas de um SQL Server e o pedido é auditar o
projeto inteiro, ou quando o refresh é lento e a causa parece estar na origem.

⚠️ As consultas de leitura abaixo foram executadas em **um** SQL Server 2017
(14.x). Confira em outras versões.

## Antes de consultar

- **Somente leitura.** Metadados primeiro; consulta pesada em tabela grande só com
  motivo, fora da janela de carga da origem.
- Diga ao usuário com que conta está conectado. Conta `sysadmin` ou `db_owner` em
  produção é um achado, e pede ainda mais cuidado.
- `sys.dm_*` pede `VIEW SERVER STATE` (itens 5 e, para tamanhos,
  `VIEW DATABASE STATE`). Sem a permissão, registre como **não verificado**.
- Não leia linhas com dado pessoal: contagens, somas e metadados bastam.

## O que olhar

Troque `bi` pelo esquema que o modelo consome.

| # | Item | O que costuma ser achado |
|---|---|---|
| 1 | Versão e opções do banco | Nível de compatibilidade antigo, sem atualização cumulativa, Query Store desligado |
| 2 | Backup | Sem backup recente |
| 3 | Tamanhos e índices | Tabela grande sem índice agrupado (heap), índices gerados em massa, colunas `char` largas |
| 4 | Dependências das views | View sobre view relendo a mesma tabela grande |
| 5 | Tempos e leituras | View que leva minutos ou lê muitas vezes o tamanho da tabela |
| 6 | Permissões | Nenhum `GRANT` no esquema: quem lê precisa de direito amplo |
| 7 | Scripts de instalação | `DELETE` ou `TRUNCATE` sem trava, carga que apaga o que foi editado à mão, sem transação |

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

O cache zera quando o servidor reinicia. O tempo decorrido inclui a entrega das
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
   repositório: `SELECT OBJECT_DEFINITION(OBJECT_ID('bi.VwFatVenda'));`.
2. **Compare o SQL novo sem instalar:** rode o corpo da view nova como consulta,
   para uma tabela temporária, e compare com a view atual por período: linhas,
   somas e chaves duplicadas.
3. **Meça com todas as colunas.** Selecionar duas ou três deixa o otimizador pular
   trabalho: em um caso, a mesma consulta caiu de 29 s para 6 s só pela projeção
   estreita, e a comparação levou a procurar uma regressão que não existia.
4. **Mesmo script antes e depois**, na mesma carga da origem. Fontes de fotografia
   (saldo, pendência) mudam entre cargas.
5. **Instale em transação** (`SET XACT_ABORT ON` e `BEGIN TRANSACTION`), em um
   script que altera só o necessário: reexecutar a instalação completa pode apagar
   dado mantido à mão.

⚠️ No `sqlcmd`, a variável dentro de `:r` (`:r "$(PASTA)\arquivo.sql"`) pode não
ser substituída (visto com o cliente ODBC 17). Teste a inclusão com um arquivo
inofensivo ou use caminho relativo, rodando de dentro da pasta.
