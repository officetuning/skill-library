# Janela de histórico, check-up de banco e correções (2.12.0, desenho curto)

## Intenção
Levar ao pacote as lições neutras de um check-up e de uma correção em um projeto real e fechar
seis inconsistências achadas na leitura da 2.11.0.

## Objetivo, fora de escopo e anti-objetivo
- **Objetivo:** 2.12.0 com as correções e as lições, cada uma dizendo o que foi testado.
- **Fora:** skill nova; mudança de convenção da casa; alterar os scripts de `tmdl/` de projetos.
- **Anti-objetivo:** publicar nome, dado, valor, servidor ou área de projeto real (repositório
  público); apresentar como testado o que só foi lido no código ou na documentação.

## Caminhos considerados
| Caminho | Troca | Decisão |
|---|---|---|
| A. Tudo na 2.12.0, marcando o que não foi testado | Fecha agora; leitor vê o limite de cada item | **Escolhido pelo autor** |
| B. Só o testado | Mais seguro; a janela automática esperaria os testes no Desktop | Descartado |
| C. Skill nova de check-up de banco | Descrição própria de disparo; mais uma skill para manter | Descartado: cabe nas existentes |

## Partes
1. **Correções:** contagem de skills no guia; papel da tabela pelo grupo de consultas; modo de
   filtros no cabeçalho no wireframe; `scaling` da imagem de storytelling; rodapé da checagem 14;
   `check_visual_bindings.py` com campos de hierarquia (teste que falha antes da correção).
2. **Check-up de banco** (referência nova em `bi-qa-documentacao`): ambiente, índices, tempos,
   permissões, scripts destrutivos; aceite de mudança em view (comparar o SQL novo sem instalar,
   guardar as definições atuais, medir com todas as colunas, antes e depois).
3. **Checagens adicionais:** scripts TMDL avulsos defasados; dado sensível versionado; seleção de
   período gravada em segmentação.
4. **Janela de histórico** (referência nova em `power-query-m`, com remissão no calendário): perguntar
   a intenção; um só lugar para a regra; fim exclusivo; fato sem política carrega tudo; incremental
   em anos conta ano civil, não reprocessa período antigo e não serve a janela que anda.

## Estado de verificação a registrar
| Item | Estado |
|---|---|
| Check-up de banco e aceite de view | Executado em um SQL Server 2017 |
| Janela automática: parte SQL | Instalada e comparada mês a mês em um banco |
| Janela automática: parte M | **Não aberta no Desktop** |
| Comportamento do incremental no Service | **Não testado**: código e documentação da Microsoft |

## A cargo de quem implementa
Redação, nomes dos arquivos de referência, posição das remissões. Exemplos genéricos.

## Entrega
Branch e PR. Commit, push e PR só com autorização do autor; merge nunca.
