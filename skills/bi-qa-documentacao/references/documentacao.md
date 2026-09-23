# Documentação automática do modelo

Do TMDL/PBIR versionado ao `.docx`, sem abrir o Desktop.

## Regras

**Obrigatório**
- Extrair dos arquivos `.tmdl` e `.json` do Git. Nunca digitar o que "deveria existir".
- Toda medida: nome, DAX completo, `formatString`, `displayFolder`, tabela.
- Toda tabela: papel (prefixo `TabFat`/`TabDim`), grão, modo de armazenamento, se oculta.
- Todo relacionamento: cardinalidade, direção do filtro, ativo ou inativo.
- Regerar a cada publicação.

**Preferir**
- Gerar pelos scripts da skill em vez de editar um template Word à mão.
- Capa com a cor do tema do relatório (4º argumento do `gerar_docx.js`, ex.:
  a cor de acento do tema do Background Builder).
- Seção por página do relatório, fechando o rastro medida → visual → página.
- Anexar o `.docx` como artefato do pipeline, junto com o QA.

**Evitar**
- Parser de linha única: medida multilinha com comentário `--` é cortada. O
  `tmdl_parser.py` lê o bloco inteiro pela indentação.
- Publicar RLS com valores literais sensíveis (ex.: `[Gerente] = "Fulano"`)
  sem revisão. O mesmo vale para valores de filtro guardados em `visual.json`.
- Prometer que a explicação em linguagem natural de DAX complexo (variáveis
  aninhadas, `TREATAS`, relacionamento virtual) está correta sem revisão humana.

## Fonte 1 — TMDL

| Seção | Arquivo | Captura |
|---|---|---|
| Visão geral | `model.tmdl`, `database.tmdl` | Nome, `compatibilityLevel`, `culture` |
| Tabelas | `tables/*.tmdl` | Nome, papel, `partition ... mode:`, oculta |
| Colunas | bloco `column` | `dataType`, `sourceColumn`, `summarizeBy`, `isHidden` |
| Medidas | bloco `measure` | DAX, `formatString`, `displayFolder`, descrição `///` |
| Relacionamentos | `relationships.tmdl` | `fromColumn`/`toColumn`, `crossFilteringBehavior`, `isActive` |
| RLS | `roles/*.tmdl` | Role, `modelPermission`, `tablePermission` |
| Grupos de cálculo | tabela com `calculationGroup` | Itens e expressões |

O `tmdl_parser.py` cobre tabelas, colunas, medidas e relacionamentos. RLS e
grupos de cálculo ficam para extensão quando o projeto precisar.

## Fonte 2 — PBIR

| Elemento | Arquivo | Captura |
|---|---|---|
| Ordem das páginas | `pages/pages.json` | `pageOrder` |
| Página | `pages/[p]/page.json` | `displayName` |
| Visual | `pages/[p]/visuals/[v]/visual.json` | `visualType` e campos usados |
| Bookmarks | `bookmarks/*.bookmark.json` | Nome, página e visuais afetados |

O cruzamento de campos é o mesmo da camada 3 do QA, usado para gerar texto.

## Estrutura do documento

1. **Capa** — nome, cor do tema, commit e data de origem
2. **Sumário** — campo TOC real (atualiza ao abrir no Word)
3. **Visão geral** — propósito, fonte, armazenamento, frequência (preencha à mão
   ou a partir do Canvas, skill `dashboard-canvas`)
4. **Tabelas** — papel, armazenamento, colunas
5. **Relacionamentos** — De → Para, filtro, ativo
6. **Medidas** — pasta, formato, descrição, DAX em bloco monoespaçado
7. **Segurança (RLS)** — se houver; revise valores sensíveis
8. **Páginas** — visuais e campos consumidos
9. **Rodapé** — commit

## Execução

```bash
python scripts/extrair_modelo.py VendasAurora.SemanticModel/definition VendasAurora.Report/definition > modelo.json
npm install docx
node scripts/gerar_docx.js modelo.json documentacao-modelo.docx "Vendas Aurora" 2B579A
```

Antes de entregar, converta para PDF e confira o layout página a página.

## Checklist

- [ ] Gerado da pasta atual do repositório
- [ ] Nenhuma medida visível com ❗ sem formato (regra Alta do BPA)
- [ ] Medidas relevantes com descrição `///`
- [ ] Toda tabela com papel e grão
- [ ] Relacionamentos inativos marcados
- [ ] RLS revisado se tiver valor sensível
- [ ] Sumário funcionando
- [ ] Commit no rodapé
