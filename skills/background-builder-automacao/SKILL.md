---
name: background-builder-automacao
description: Preencher o Background Builder e baixar a coleção (PNGs, Tema.json, Script.TMDL, Ficha) sem o usuário abrir o site — o agente estuda o PBIP, propõe H1, H2, tagline, páginas e filtros (5W2H e Encaixe 1/1, 1/2, 1/3), grava a Ficha Técnica em JSON e roda um script Playwright que carrega a ficha e exporta o ZIP para a pasta do projeto. Use quando o usuário pedir para gerar, atualizar ou regenerar os fundos do Background Builder, criar, renomear ou reordenar página ou filtro do Builder, ou "fazer o Builder sozinho". Para montar o relatório com os PNGs depois use dashboard-layout.
---

# Background Builder automático

## Pergunta central

> O que o Builder vai desenhar (identidade, menu, painel de filtros) é o que
> este relatório precisa, e o ZIP novo chegou à pasta do projeto sem nenhum
> clique do usuário?

O Builder roda inteiro no navegador e não tem API. O caminho automático é o
mesmo que o usuário faz à mão, só que por script: **Abrir Ficha Técnica** com um
JSON preparado pelo agente, **Exportar coleção**, salvar o ZIP. O script
`scripts/exportar-colecao.cjs` faz isso com Playwright, sem janela.

## Fluxo

1. **Estudar o projeto.** Ler o PBIP (modelo, relacionamentos, medidas, páginas
   do relatório) antes de propor qualquer coisa. Se o projeto já tem uma Ficha
   (`<H1> - Background Builder.md`, que vem no ZIP), partir dela: ela é o estado
   atual do Builder.
2. **Propor a coleção.** Identidade, páginas e filtros pelas regras abaixo.
   Mostrar ao usuário a proposta em tabela (o que muda e por quê) e **esperar o
   ok**: mudar H1, página ou filtro obriga a regenerar e substituir os fundos de
   todas as páginas.
3. **Gravar a ficha.** Um `.md` com um bloco ` ```json ` no fim (ou um `.json`
   puro) na pasta do projeto, por exemplo `Background Builder/ficha.md`.
   Contrato dos campos em `references/ficha-json.md`. Partindo de uma Ficha
   exportada, editar **só o JSON**; o texto acima dele é ignorado na leitura.
4. **Exportar.** Rodar o script (instalação abaixo):

   ```powershell
   node "<pasta da skill>\scripts\exportar-colecao.cjs" `
     --ficha ".\Background Builder\ficha.md" `
     --saida ".\Background Builder"
   ```

   **Sem marca (white label):** acrescente `--sem-marca` quando o autor pedir o rodapé
   oculto (o script envia `Ctrl+Alt+8`; a Ficha não tem esse campo). Confira num PNG que
   a faixa vertical à direita ficou vazia.

   Saída em uma linha JSON: `{ ok, zip, paginas[], versaoBuilder }` ou
   `{ ok:false, erro }`. O script tira os campos só de saída (`_appVersion`,
   `resolvedPalette`, `filtrosForaDoPainel`), confere se o H1 chegou ao
   formulário e só salva o ZIP se a verificação de pixels do Builder passar.
5. **Conferir o ZIP.** Descompactar (`Expand-Archive`) numa pasta com a data ou
   a versão, e ler a Ficha que veio dentro:
   - `filtrosForaDoPainel` não vazio = filtro que **não coube** no painel e não
     aparece no PNG. Compactar com o Encaixe, tirar filtro ou levar para outra
     página, e exportar de novo.
   - Comparar a lista de PNGs com as páginas do relatório.
   - **Comparar com os fundos atuais** (arquivo a arquivo e por pixel): ao incluir
     um filtro, só a **barra lateral** das páginas de corpo muda; ao regenerar sem
     mudar nada, quase tudo sai idêntico (às vezes só a Sobre muda). As três Dicas
     (`dicaSizes`) precisam sair com 320×240, 400×304 e 600×456 se estavam na Ficha.
     Diferença fora do esperado é sinal de Ficha editada ou de Builder novo.
   - No `Script.TMDL`, toda fórmula DAX com a tabela entre aspas simples
     (`'Atualização'[...]`, `'Calendário'[...]`). Até o Builder 1.033 a medida
     `Data da Última Atualização` sai sem aspas e dá erro: corrigir antes de
     aplicar (ver `dashboard-layout`, `references/background-builder.md`).
6. **Aplicar no relatório.** Substituir os fundos, reposicionar navegador e
   segmentações, aplicar o `Tema.json` e, na primeira vez, o `Script.TMDL`.
   Passo a passo e coordenadas em `dashboard-layout`
   (`references/background-builder-ciclo.md` e `background-builder-regeneracao.md`).

## Regras para propor a coleção

**Identidade**
- **H1** = o assunto do relatório (o que se analisa), não o departamento. Só se
  sustenta se uma página o representar.
- **H2** = frase curta em tom manuscrito, pergunta ou promessa. Opcional; vazio
  ↔ preenchido muda todos os PNGs.
- **Tagline** = o que o relatório entrega. Cada promessa precisa existir no
  conteúdo.
- **Tema** = a família do assunto (lista em `references/ficha-json.md`); ele
  define o accent e as ilustrações.

**Páginas de corpo** (`bodyPages`): nome descreve o conteúdo, nunca é nome de
medida. Início, Sobre, Detalhe e Dica são geradas pelo Builder e não entram na
lista. A ordem da lista é a ordem do menu.

**Filtros** (`filters`) — o painel lateral é **o mesmo em todas as páginas de
corpo**:
- Só os campos que mais recortam os dados e que fazem sentido em **todas** as
  páginas; toda medida precisa responder a todos eles.
- Um filtro de **data ou período** (nome começando por "Data" ou "Período") vira
  segmentação de intervalo: sempre largura inteira e mais alta (296×120). Partes
  de data como Ano e Mês são listas compactas (1/3 sugerido).
- Cada filtro recebe a classificação **5W2H** (`filterCategoryOverrides`) e o
  **Encaixe** (`filterWidthOverrides`: `full` 1/1, `half` 1/2, `third` 1/3).
  Agrupamento 5W2H ligado: o painel ordena por Quando, Onde, Quem, O quê, Como,
  Quanto, Por quê, e a ordem da lista vale dentro de cada grupo.
- Encaixe: 1/1 para nomes longos ou listas grandes; 1/2 para pares naturais
  (Região e UF); 1/3 para listas curtas (Ano, Mês, Trimestre).
- Entregar ao usuário a tabela: filtro · coluna do modelo · 5W2H · Encaixe ·
  motivo.

## Instalação (uma vez por máquina)

O script precisa do pacote `playwright` do npm, instalado **uma vez por
computador** (e por usuário do Windows). Antes da primeira exportação numa
máquina, o agente confere se existe `%USERPROFILE%\.bb-automacao\node_modules\playwright`
e, se não existir, roda ele mesmo:

```powershell
npm install --prefix "$env:USERPROFILE\.bb-automacao" playwright
```

O script procura o Playwright nessa pasta sozinho; não precisa de `NODE_PATH`.
No Windows ele usa o Microsoft Edge que já vem instalado, então não baixa
navegador. Sem Edge: `--navegador chrome`, ou `npx playwright install chromium`
e `--navegador chromium`. `--visivel` abre a janela para acompanhar. `--url`
aponta outro endereço do Builder (o padrão é
`https://backgroundbuilder.officetuning.ai/`).

## Qual exportador usar (decida pelo ambiente)

Há dois scripts com o **mesmo fluxo e os mesmos parâmetros**. A redundância é
proposital: muitas máquinas corporativas não têm Node, ou não permitem instalá-lo, e
já têm Python. Confira o que existe e o que é permitido **antes** de instalar algo, e
escolha pela primeira linha que se aplicar:

| Situação da máquina | Use |
|---|---|
| Node disponível (`node --version`) e Playwright instalado ou instalável | `exportar-colecao.cjs` (principal) |
| Sem Node, com Python (`python --version`) e permissão para ambiente virtual | `exportar-colecao.py` |
| Sem nenhum dos dois, ou instalação não permitida | caminho manual (abaixo) |

- Para o Python: crie um ambiente virtual numa pasta temporária ou do usuário e rode
  nele `python -m pip install playwright`. Usa o Edge instalado, sem baixar navegador.
- `--bloquear-envios` (só no `.py`) aborta tudo que não for GET, para a ficha não sair
  do navegador. Use quando a ficha tiver nomes ou outro conteúdo que não deva ser
  enviado; as contagens de uso do site também deixam de ir.
- Restrição de política (instalação bloqueada, modo de linguagem restrito, proxy):
  **não contorne**. Informe o bloqueio e siga pelo caminho manual.
- Diga ao usuário qual script usou, o que instalou e onde.
- Mudança na interface do Builder pede o ajuste **nos dois** scripts.

## Quando o script falha

| Erro | Causa provável | O que fazer |
|---|---|---|
| Playwright não instalado | Primeira vez nesta máquina | Rodar a instalação acima e repetir |
| H1 não apareceu no formulário | A interface do Builder mudou ou o JSON é inválido | Validar o JSON; se estiver certo, abrir a ficha à mão em **Projeto › Abrir Ficha Técnica** e avisar que o script precisa de ajuste |
| ZIP bloqueado pela verificação de pixels | Uma página saiu chapada | Exportar de novo; se repetir, é problema no Builder: informar a página |
| Medida `Data da Última Atualização` com erro depois do script | Builder 1.033 ou anterior gerou `Atualização[...]` sem aspas | Trocar por `'Atualização'[Momento da Última Atualização]` |
| Tempo esgotado no download | Muitas páginas ou máquina lenta | Rodar de novo com `--visivel` para ver onde para |
| `page.goto: Timeout 90000ms` esperando `networkidle` | O site mantém conexões abertas (métricas) e a rede nunca fica ociosa | O script já tenta `networkidle` por 30 s e cai para `domcontentloaded`. Em versão antiga do script, troque `waitUntil` por `"domcontentloaded"`; o site responde (HTTP 200) |

O caminho manual continua valendo sempre: o usuário abre a mesma ficha no
Builder, clica em **Exportar coleção** e põe o ZIP na pasta do projeto.

## Limites

- O script usa dois pontos da interface: o campo de arquivo de **Abrir Ficha
  Técnica** e o botão **Exportar coleção**. Se o Builder mudar esses elementos,
  o script quebra até ser ajustado; a ficha em si não muda.
- Ícone do cabeçalho (`headerIcon`) só entra como `data:image/...` dentro do
  JSON. Ilustrações enviadas à mão no Builder não passam pela ficha.
- A exportação manda ao site só contagens de uso (tema, número de páginas e de
  filtros), não o conteúdo da ficha.
