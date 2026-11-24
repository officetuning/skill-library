# Background Builder

Web app ([backgroundbuilder.officetuning.ai](https://backgroundbuilder.officetuning.ai/))
que gera o sistema visual de um relatório: fundos PNG 1920×1080 por página,
PNG da Dica de Ferramenta, tema `.json`, script TMDL, ícones estatísticos, guia
de montagem (`Leiame.md`) e Ficha Técnica. O usuário preenche título,
subtítulo, tagline, tema/cor de acento, fundo da página, páginas de corpo,
filtros, fontes de dados e equipe.

**O fundo não é decoração.** Ele reserva, em pixel exato, onde cada segmentação,
cartão e botão real deve ficar. O guia de montagem traz as coordenadas.

Esta referência descreve a versão **1.031** do Builder (campo `_appVersion` da
Ficha Técnica). Se a versão do projeto for outra, vale o guia de montagem
exportado com ele.

A Ficha guarda a versão do app que a gerou (`_appVersion`). O Builder só avisa
"alguns campos podem não ter sido recuperados" quando a Ficha é mais antiga que
a **versão do contrato** (1.028): Fichas da 1.028 em diante abrem sem aviso,
mesmo que o app já esteja numa versão maior. Campo novo opcional não muda o
contrato.

## O que vem na coleção (`<Projeto> - Coleção.zip`)

| Arquivo | Uso |
|---|---|
| `<Projeto> - Início.png`, `- <Página de corpo>.png`, `- Sobre.png`, `- Detalhe.png` | Tela de fundo de cada página, 1920×1080 |
| `<Projeto> - Dica de Ferramenta.png` | Uma dica escolhida: nome simples |
| `<Projeto> - Dica de Ferramenta - <Uso> (<L>x<A>).png` | Duas ou três dicas: nome completo, ex.: `Visual único (320x240)`, `Vários visuais (400x304)`, `Mini relatório (600x456)` |
| `<Projeto> - Tema.json` | Tema do relatório (paleta, sentimento, divergentes, fundo da página) |
| `<Projeto> - Script.TMDL` | Tabelas de atualização e calendário e as medidas do cabeçalho (nomes: seção "Script TMDL") |
| `<Projeto> - Background Builder.md` | Ficha Técnica com o JSON completo do projeto |
| `Leiame.md` | Guia de montagem em 13 passos + aviso de direitos |
| `Icones-Estatisticos/svg` e `/png` | Soma, Média, Mediana, Mínimo, Máximo, Desvio Padrão, Variância |

## Estrutura das páginas

- **Cabeçalho flutuante branco**, cantos arredondados, igual em todas as
  páginas (exceto Dica). Zona do cabeçalho até y=112.
  - Esquerda: ícone de cabeçalho 40×40 + H1 (Poppins bold) + H2 (manuscrita,
    sublinhada na cor de acento; o H2 é opcional, ver
    `background-builder-ciclo.md`). O ícone padrão é o símbolo transparente do
    Builder nas cores do relatório, com contraste mínimo de 3:1; um ícone
    enviado pelo usuário o substitui.
  - Centro: menu (Início, páginas de corpo, Sobre). Células de **largura
    idêntica**, requisito do visual **Navegador**. O passo e a fonte se ajustam
    à quantidade de itens e ao tamanho do título (ver
    `background-builder-ciclo.md`).
  - Direita: card de **última atualização** (Início, corpo e Sobre) ou
    "Você está vendo" + Voltar (Detalhe).
- **Sem rodapé reservado.** O rodapé fica livre em toda a largura até x=1904.
- **Faixa de marca** vertical de x=1904 a x=1920: sempre livre. A assinatura é
  centralizada na altura útil y=128–1064 (centro em y=596). O texto é
  "© {ano} officetuning.ai · Feito com Background Builder" (versão curta:
  "© {ano} officetuning.ai"). No modo **sem marca** (white label, `Ctrl+Alt+8`
  no Builder) a assinatura some do PNG; o texto não é trocado.

| Página | Corpo | Direita do cabeçalho |
|---|---|---|
| Início | Hero (H2 manuscrito + tagline) + pilares + ilustração | Última atualização |
| Corpo | Barra lateral de filtros + área livre + cantos de ilustração | Última atualização |
| Sobre | 6 cartões: Aviso Legal, Nota, Fonte de Dados, Equipe Técnica, Dicionário de Dados, Versão | Última atualização |
| Detalhe (drill-through) | Área livre, sem barra lateral | Ícone de olho + card da seleção + "← Voltar" |
| Dica de Ferramenta | 320×240, 400×304 ou 600×456, borda de 2 px na cor de acento rente às 4 bordas | — |

### Slots do cabeçalho (coordenadas do guia de montagem)

| Slot | Posição e tamanho | Conteúdo |
|---|---|---|
| Ícone de relógio | (1696, 48) 24×32 | Só ícone, sem rótulo escrito |
| Última atualização | (1728, 48) 160×32 | Card transparente com a medida `[Última Atualização]`; só o valor visível |
| Ícone de olho (Detalhe) | (1200, 48) 24×32 | Só ícone, sem rótulo "Você está vendo:" escrito |
| Seleção (Detalhe) | (1232, 48) 496×32 | Card com a medida de seleção (`Você Está Vendo` especializada) |
| Voltar (Detalhe) | (1744, 40) 144×48 | Botão Voltar |

A página Detalhe **não** leva o card de última atualização.

## Fundo das páginas

Nove opções (5 claras e 4 escuras, ex.: Papel `#FAFAF7`). O fundo escolhido já
está no PNG e no `background` do tema: as áreas reservadas são calculadas sobre
ele. Trocar o fundo exige regenerar PNG e tema juntos.

## Cor dos nichos

"Nichos" são os retângulos reservados para segmentações, cards (última
atualização, seleção do Detalhe) e as caixas de Versão e Data da página Sobre.
Por padrão o tom é derivado do accent (accent a 12% sobre o fundo; nos fundos
escuros, um tom próprio). Desde a 1.031 o formulário tem o seletor **Cor dos
nichos**, no bloco de Filtros, e a cor escolhida vale para todos os nichos do
PNG.

- **O tema não muda.** O `Tema.json` não leva a cor dos nichos: ela existe só
  no fundo. Os visuais herdam a paleta do tema, e a cor do nicho serve de
  referência para o encaixe, não de cor de dado.
- **Contraste.** Se a cor escolhida não tiver contraste suficiente sobre o
  fundo (4,5:1 nos fundos claros), o Builder avisa e usa uma versão ajustada
  no PNG. A Ficha guarda a cor escolhida (`customSlot`), não a ajustada.
- **Troca de tema.** Sem cor escolhida, o nicho acompanha o tema. Com cor
  escolhida, o Builder pergunta se mantém a sua cor ou usa a proporcional ao
  novo tema.
- **Na montagem:** a cor do nicho não é mais necessariamente um tom do accent.
  Confira o encaixe pelo PNG, não pela paleta.

## Barra lateral de filtros

A barra lateral aparece **a partir de 1 filtro** (não há mais modo de filtro no
cabeçalho). Mede **344×936**, em **x=16, y=128**, e termina em **y=1064**.

- Título **Filtros** com botões nativos alinhados à direita: 32 px de altura,
  largura arredondada para múltiplo de 8, raio 8 px, borda 1,5 px, ícone 16 px,
  texto Poppins 600 14 px, padding horizontal 8 px, 8 px entre botões. Os
  rótulos seguem o fundo: **Aplicar todos os filtros** e **Limpar todas as
  segmentações**; com aplicação automática (`filterAutoApply: true`) só
  aparece o de limpar.
- Filtros agrupados sob cabeçalhos **5W2H** (Quando, Onde, Quem, O quê...),
  com ícone. Um filtro classificado no Canvas já chega com o 5W2H.
- **Encaixe** de cada filtro:

  | Tipo | Tamanho |
  |---|---|
  | Data completa | Sempre 1/1, **296×120** |
  | 1/1 | 296×40 |
  | 1/2 | 144×40 + 144×40 |
  | 1/3 | 96×40 + 96×40 + 88×40 |

  8 px entre itens. O agrupamento é guloso e **não atravessa cabeçalhos 5W2H**;
  1/3 que sobra sozinho ou em dupla expande para a largura da linha.
- Se algum filtro não couber (o corte é por linha inteira), o formulário mostra
  a linha **"Fim do painel"** e um alerta em cada filtro de fora, a prévia
  mostra **"+N filtros não cabem"** e a Ficha Técnica lista esses filtros
  (`filtrosForaDoPainel`). Compacte com 1/2 ou 1/3, reduza filtros ou mova-os
  para outra página.
- Segmentação: estilo **Suspenso**, cabeçalho da segmentação desligado,
  posicionada sobre o retângulo "fantasma" (tom derivado do accent).

**Diagnóstico:** segmentação fora dos retângulos da barra, ou retângulo vazio,
indica que os filtros do relatório divergem da Ficha Técnica. Regere o fundo.

## Tema, família e paleta

Cada tema = família temática (Financeiro, Vendas, RH, TI, SSMA...) + uma cor de
acento + ilustrações line-art. Paleta de 8 cores derivada de dois insumos,
**Accent** (cor 3) e **Navy** (cor 1): Navy, Azul Padrão, Accent, Neutro
Escuro, Neutro Claro, Nuance do Accent, Análogo e Complementar.
- **Sentimento:** Positivo, Neutro, Negativo (`good`, `neutral`, `bad`).
- **Divergentes:** Máximo, Centro, Mínimo (escala de cores em tabela, matriz e cartão).

Cada cor é "definida" (alterada no painel de Branding) ou "calculada". Visuais
com paleta diferente parecem dessincronizados: importe o tema em vez de colorir
visual a visual.

## Templates

Galeria por área (Marketing Digital, Financeiro, RH...) com navegação, filtros
típicos e fontes sugeridas. "Montar meu dashboard com este Template" pré-preenche
o formulário. Para "um dashboard de [área]" do zero, sugira olhar a galeria antes.

## Ficha Técnica e ponte com o Canvas

`<Projeto> - Background Builder.md` traz identidade, paleta, páginas, filtros
(com 5W2H e Encaixe), fontes e equipe, e um bloco JSON com todos os dados. O
JSON reabre o projeto no Builder (**Abrir Ficha Técnica**) e entra no Dashboard
Canvas (**Importar do Background Builder**). Ao mudar identidade, páginas ou
filtros, edite pelo Builder e regenere; ver `background-builder-ciclo.md`.

Campos do JSON que ajudam a diagnosticar um projeto:

| Campo | Significado |
|---|---|
| `_appVersion` | Versão do Builder que gerou a Ficha |
| `pageBackground` | Chave do fundo escolhido (ex.: `paper`) |
| `dicaSizes` | Dicas geradas: `single` (320×240), `multi` (400×304), `mini` (600×456); ausente = só `multi` |
| `filterAutoApply` | `true` (padrão): só o botão de limpar; `false`: aplicar + limpar |
| `use5W2HGrouping` | Agrupamento dos filtros por 5W2H (padrão `true`) |
| `customSlot` | Cor dos nichos, só quando o usuário escolheu |
| `resolvedPalette` e `filtrosForaDoPainel` | Só saída: o Builder ignora os dois ao reabrir a Ficha |

## Guia de montagem (13 passos)

1. Descompactar a coleção.
2. Importar o tema: **Design → Importar tema** (antes de set/2026:
   Exibir → Temas → Procurar temas).
3. Criar as páginas na ordem do menu (Início, corpo, Sobre, Detalhe), 1920×1080,
   PNG como tela de fundo, **Ajuste = Alongar**, **Transparência = 0%**.
4. Usar as cores de sentimento e a escala divergente na formatação condicional.
5. Criar a página de dica (tamanho do PNG), mesmo ajuste, e ativar
   **Permitir uso como dica de ferramenta**.
6. Início como página de aterrissagem; ocultar Detalhe e Dica.
7. **Exibir → Ajustar à grade** e zoom de 100% ou mais.
8. **Navegador de página** sobre as células do menu: Texto, Preencher e Borda
   desligados; em Opções, desligar **Mostrar páginas escondidas** e **Mostrar
   páginas de dica de ferramenta**; manter **Mostrar tudo por padrão**.
9. Filtros na barra lateral (seção acima).
10. Cards nativos do cabeçalho (slots acima).
11. Versão e Data da Versão como caixa de texto manual no cartão Versão da Sobre.
12. Script TMDL e medida `[Última Atualização]` (bug de fuso, abaixo).
13. Especializar `[Você Está Vendo]` como `<Campo> Selecionado(a)` e colocá-la no card da Detalhe.

## Script TMDL e bug de fuso horário

`TODAY()`/`NOW()` usam o fuso local no Desktop e **UTC no Service**: perto da
virada do dia em Brasília o relatório acusa "desatualizado" com o refresh em dia.

### Padrão de nomes e de estrutura (2.0.0)

O padrão segue a orientação oficial de modelagem da Microsoft: tabela com nome
de negócio, papel no grupo de consultas, medidas distribuídas pelas tabelas (sem
tabela única de medidas) e calendário em Power Query.

| Objeto | Grupo de consultas | Conteúdo |
|---|---|---|
| **`Atualização`** (oculta) | Internas | Uma linha com o momento do refresh, capturado no **Power Query** já em hora local (`DateTimeZone.SwitchZone(DateTimeZone.UtcNow(), -3, 0)`), não em DAX. Medidas `Data da Última Atualização` e `Última Atualização` (status ✔️ hoje, ⚠️ ontem, ❗ mais antigo, comparando com `UTCNOW() - TIME(3,0,0)`, + data no formato do idioma), pasta `Cabeçalho` |
| **`Calendário`** | Dimensões | Tabela em **Power Query** (não calculada em DAX): ano, semestre, trimestre, mês, semana, quinzena, dia da semana, fim de semana, estação (com cor) e hemisfério, com nomes traduzidos pela localidade; período fixo (5 anos até o fim do ano atual) ou flexível pelas datas das fatos. `dataCategory: Time`, marcada como Tabela de Datas, meses com `sortByColumn`. Medidas `Idioma do Projeto`, `Idioma Detectado do Usuário` (`USERCULTURE()`, só para exibir; só personaliza de verdade em Premium/PPU/Embedded), `Hemisfério do Projeto`, `Primeiro Dia da Semana do Projeto`, `Formato de Data` |
| **`Você Está Vendo`** | — | **Medida-modelo transitória** (devolve `BLANK()`), pasta `Seleção`. Ao definir o campo do Detalhe, renomeie para `<Campo> Selecionado(a)`, mova para a tabela do campo e escreva `SELECTEDVALUE ( coluna, "-" )`. Ver `powerbi-detalhe-dica` |

`Idioma do Projeto` (código de localidade, `"pt-BR"`, `"en-US"`...) é a **fonte
única** de idioma, hemisfério, primeiro dia da semana e formato de data. Manual
de propósito.

### Builder 1.031 e anteriores: nomes antigos

O script atual do Builder ainda gera o padrão anterior. Ao montar um projeto,
renomeie (e confira os visuais com a checagem 16 da `bi-qa-documentacao`):

| Gerado pelo Builder 1.031 | Padrão 2.0.0 |
|---|---|
| `TabIntAtualização` | `Atualização` |
| `TabDimCalendário` (tabela calculada em DAX; exige refresh manual depois do script, senão fica com 0 linhas) | `Calendário` (Power Query) |
| `TabIntMedida` (tabela única de medidas) | medidas movidas para `Atualização` e `Calendário`; a tabela deixa de existir |
| `[Atualização]` / `Data Última Atualização` | `[Última Atualização]` / `Data da Última Atualização` |
| `Idioma do Usuário (Detectado)` | `Idioma Detectado do Usuário` |
| `VocêEstáVendo` com `"vários itens"` | `Você Está Vendo`, especializada com `"-"` |

Fora do Brasil, ajuste o offset -3 nos dois pontos marcados; com horário de
verão, troque o deslocamento fixo por um fuso nomeado. Os nomes das colunas do
calendário ficam em português em qualquer localidade.

Medida de "última atualização" usando `TODAY()`/`NOW()` direto é sinal de que
o valor vai divergir no Service.

## Revisar um relatório feito com o Background Builder

Assinaturas: cabeçalho branco flutuante, menu de células iguais, relógio +
card de atualização no cabeçalho, barra lateral de filtros com cabeçalhos
5W2H, Detalhe com olho + card + Voltar, dica com borda rente.

1. Visuais exatamente sobre as áreas reservadas (use o guia de montagem).
2. Tema `.json` importado, sem cor avulsa; fundo da página igual ao do PNG.
3. Segmentações coerentes com a barra lateral (quantidade, ordem e Encaixe).
4. Páginas de corpo iguais às do Builder (nome e ordem) para o Navegador.
5. Detalhe com o card da seleção personalizado (não `BLANK()`) e Voltar.
6. Nenhum visual sobre os cantos de ilustração nem na faixa de marca.
7. Card de última atualização ligado a `[Última Atualização]`, ausente na Detalhe.
8. `Calendário` com linhas e `Idioma do Projeto` correto; nenhum nome antigo do Builder 1.031 (`TabInt…`, `TabDim…`, `VocêEstáVendo`) sobrando.
