# PBIR — referência

Consolidado de Microsoft Learn:
[Formato de relatório aprimorado](https://learn.microsoft.com/pt-br/power-bi/developer/embedded/projects-enhanced-report-format) ·
[Pasta do relatório](https://learn.microsoft.com/pt-br/power-bi/developer/projects/projects-report).
Vigência desta cópia: 29/08/2026, com PBIR em preview. Confirme o status atual.

## O que muda em relação ao PBIR-Legacy

O `report.json` monolítico vira uma pasta `definition\` com um arquivo por
página, visual e bookmark. O formato é documentado publicamente, cada arquivo
tem JSON Schema, e o Desktop valida os arquivos ao abrir. Ganhos: copiar
visuais e páginas entre relatórios, localizar e substituir em massa, mudanças
em lote por script.

## Habilitar

Arquivo → Opções e configurações → Opções → Recursos de visualização →
**Armazenar relatórios usando o formato de metadados aprimorado (PBIR)**. Há
opção equivalente para PBIX.

Durante o preview, Fabric Git Integration e REST APIs exportam em PBIR-Legacy,
salvo se o relatório já estiver em PBIR no Service.

## Converter e restaurar

- Abrir o PBIP com o recurso ativo → Salvar → **Atualizar**. Não se desfaz pela interface.
- Backup automático do Desktop, retido 30 dias:
  - Microsoft Store: `%USERPROFILE%\Microsoft\Power BI Desktop Store App\TempSaves\Backups`
  - Instalador: `%USERPROFILE%\AppData\Local\Microsoft\Power BI Desktop\TempSaves\Backups`
- No Service, relatórios novos já nascem em PBIR e os editados são convertidos.
  Admin pode desativar pela configuração de tenant "Automatically convert and
  store reports in the Power BI enhanced metadata format (PBIR)" durante o preview.
- Backup do Service: 28 dias; Configurações do relatório → **Restaurar como
  PBIR-Legacy**. Só existe para relatórios convertidos no próprio Service.

## Arquivos em `definition\`

| Arquivo | Obrigatório | Conteúdo |
|---|---|---|
| `pages\[pagina]\page.json` | Sim | Filtros e formatação da página |
| `pages\[pagina]\visuals\[visual]\visual.json` | Sim | Posição, formatação, query |
| `pages\[pagina]\visuals\[visual]\mobile.json` | Não | Layout mobile |
| `pages\pages.json` | Não | Ordem e página ativa |
| `bookmarks\*.bookmark.json`, `bookmarks.json` | Não | Bookmarks e grupos |
| `version.json` | Sim | Versão do formato |
| `reportExtensions.json` | Não | Medidas de relatório |
| `report.json` | Sim | Filtros e formatação do relatório |

### Nomes
Padrão: identificador de 20 caracteres. Pode renomear para nome amigável
(letras, dígitos, `_`, `-`), reiniciando o Desktop depois. Pode quebrar
referências internas e externas. Para achar o objeto: Opções → Configurações do
relatório → habilitar "Copiar nomes de objeto" e usar o botão direito → Copiar
nome do objeto.

## `definition.pbir`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byPath": { "path": "../Vendas.SemanticModel" }
  }
}
```

| Tipo | Efeito |
|---|---|
| `byPath` | Caminho relativo; abre o modelo em edição completa |
| `byConnection` | Connection string de modelo no Fabric; live connect |

Via Fabric REST API, `byConnection` é obrigatório e basta `semanticmodelid`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byConnection": { "connectionString": "semanticmodelid=[SemanticModelId]" }
  }
}
```

`version` 1.0 aceita só PBIR-Legacy; 4.0+ aceita os dois. Pode haver vários
`*.pbir` (ex.: `definition-liveConnect.pbir`); o Git Integration processa só
`definition.pbir`.

## Anotações
Pares nome-valor em `report`, `page` e `visual`, ignorados pelo Desktop, úteis
para scripts de deploy.

```json
"annotations": [ { "name": "defaultPage", "value": "c2d9b4b1487b2eb30e98" } ]
```

## Edição externa: erros

| Tipo | Efeito |
|---|---|
| Bloqueante | Desktop não abre; indica o arquivo |
| Não bloqueante | Corrigido automaticamente ao abrir (avisa antes de salvar) |

| Sintoma | Causa e solução |
|---|---|
| Objeto some após renomear pasta | Nome fora da convenção; Desktop ignora |
| Nomes novos com formato diferente dos antigos | Convenção nova só vale para objetos novos |
| Copiar bookmark apaga parte da configuração | Intencional: copie também página e visuais |
| `'pageBinding.name' must be unique` ao copiar página | Dê valor único ao `pageBinding.name` |

## Limitações (preview)

- Nuvens soberanas sem conversão automática antes da GA.
- Mais de 500 arquivos pode deixar a **autoria** lenta.
- Salvar PBIP como PBIX leva o PBIR junto.
- Filtros automáticos do visual só vão para o `visual.json` depois de expandir o painel de filtros uma vez.
- Sem suporte em workspace de Template App.

| Limite no Service | Valor |
|---|---|
| Páginas por relatório | 1.000 |
| Visuais por página | 1.000 |
| Arquivos de recurso | 1.000 |
| Tamanho dos recursos | 300 MB |
| Tamanho total do relatório | 300 MB |

## Fora de `definition\`

| Item | Nota |
|---|---|
| `.pbi\localSettings.json` | Local do usuário; no `.gitignore` |
| `CustomVisuals\` | Só visuais privados (`.pbiviz`) |
| `StaticResources\RegisteredResources\` | Temas, imagens; exige entrada no `report.json` |
| `semanticModelDiagramLayout.json` | Diagrama; sem edição externa |
| `mobileState.json` | Sem edição externa |
| `.platform` | Metadados do item Fabric para Git |
