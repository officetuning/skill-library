# Background Builder

Web app ([backgroundbuilder.officetuning.com.br](https://backgroundbuilder.officetuning.com.br/))
que gera o sistema visual de um relatório: fundos PNG 1920×1080 por página,
tema `.json` e guia de montagem. O usuário preenche título, subtítulo,
tema/cor de acento, páginas de corpo, filtros, fontes de dados e equipe.

**O fundo não é decoração.** Ele reserva, em pixel exato, onde cada slicer,
cartão e botão real deve ficar. O guia de montagem traz as coordenadas.

## Estrutura fixa (exceto Dica de Ferramenta)

- **Cabeçalho flutuante branco**, cantos arredondados, igual em todas as páginas.
  - Esquerda: logo + H1 (Poppins bold) + H2 (manuscrita, sublinhada na cor de acento).
  - Centro: menu (Início, páginas de corpo, Sobre). Células de **largura
    idêntica**, requisito do visual **Navegador**.
  - Direita: área reservada, conforme o tipo de página.
- **Rodapé "Última atualização:"** — relógio, rótulo e slot fixo no canto inferior
  direito. Presente em Início, corpo e Detalhe; ausente em Sobre e Dica de Ferramenta.

## Tipos de página

| Página | Conteúdo | Área reservada do cabeçalho |
|---|---|---|
| Início | Hero + 3 pilares + ilustração | Vazia |
| Corpo | Em branco + 1–2 cantos de ilustração | Filtros (conforme o modo) |
| Sobre | 6 cartões: Aviso Legal, Nota, Fonte de Dados, Equipe Técnica, Dicionário de Dados, Versão | Vazia |
| Detalhe (drill-through) | Corpo para o detalhe | "Você está vendo:" + botão "← Voltar", a 16 px da borda |
| Dica de Ferramenta | 400×304 px, borda de 2 px na cor de acento rente às 4 bordas | — |

## Modos de filtro

| Filtros cadastrados | Modo | Efeito |
|---|---|---|
| 1 | `header-1` | 1 slot no cabeçalho |
| 2 | `header-2` | 2 slots lado a lado |
| 3+ | `sidebar` | Painel lateral no corpo; menu pode ir até 16 px da borda direita |

**Diagnóstico:** 3+ slicers com o cabeçalho reservando espaço, ou 1–2 slicers
com painel lateral vazio → o número de filtros do `.pbix` diverge do usado no
fundo. Regere o fundo.

## Tema, família e paleta

Cada tema = família temática (Financeiro, Vendas, RH, TI, SSMA) + uma cor de
acento + ilustrações line-art nessa cor. A cor de acento é a primária do `.json`.

Paleta de 8 cores derivada de dois insumos, **Accent** e **Navy**, mais cores fixas:
- **Sentimento:** Positivo, Neutro, Negativo (formatação condicional de KPI).
- **Divergentes:** Máximo, Centro, Mínimo (escalas em tabela, matriz e mapa).

Cada cor é "definida" (escolhida) ou "calculada" (derivada de Accent/Navy).

Visuais com paleta diferente da cor de acento parecem dessincronizados:
importe o `.json` (Exibir → Temas → Procurar temas) em vez de colorir visual a visual.

## Templates

Galeria por área (Marketing Digital, Financeiro, RH) com navegação, filtros
típicos e fontes sugeridas. "Montar meu dashboard com este Template" pré-preenche
o formulário. Para "um dashboard de [área]" do zero, sugira olhar a galeria antes.

## Ponte 5W2H

Os filtros da Ficha Técnica chegam classificados em 5W2H, o mesmo vocabulário da
Matriz 2 do Canvas. Um filtro definido no Canvas já decide o modo do cabeçalho.

## Guia de montagem (12 passos)

1. Aplicar o tema `.json` (Exibir → Temas → Procurar temas).
2. Importar os PNG como plano de fundo de cada página.
3. Criar a página de tooltip de 400×304 px.
4. Montar a página Início como landing page.
5. Ocultar Detalhe e Dica de Ferramenta da navegação.
6. Ativar o alinhamento à grade no Desktop.
7. Configurar o **Navegador** com uma célula por página de corpo, nomes e ordem idênticos.
8. Segmentações no estilo **Suspenso**.
9. Campo **Versão** como caixa de texto manual no rodapé.
10. Vincular o slot "Última atualização" a uma medida real (ver bug abaixo).
11. Testar RLS, drill-through e tooltip com um usuário de cada papel.
12. Publicar e validar no Service.

## Bug de fuso horário em "Última atualização"

`TODAY()`/`NOW()` usam o fuso local no Desktop e **UTC no Service**.

Estrutura da solução (script TMDL via Tabular Editor):
1. **`TabIntAtualização`** — tabela de interface com uma linha: a data/hora do
   último refresh, capturada no Power Query (não em DAX, para não recalcular a
   cada abertura).
2. **`TabDimCalendário`** multi-idioma — nomes de mês e dia por idioma.
3. **`TabIntMedida`** com as medidas:
   - `Idioma do Projeto` e `Hemisfério` (parâmetros);
   - `Formato de Data` (string por idioma);
   - `Atualização` — aplica o deslocamento de fuso sobre o UTC capturado e
     formata no idioma;
   - `VocêEstáVendo` — mesma lógica para o bloco das páginas de Detalhe;
   - status com ✔️ atualizado, ⚠️ atrasado, ❗ falhou.

Medida de "última atualização" usando `TODAY()`/`NOW()` direto é sinal de que
o valor vai divergir no Service.

## Revisar um relatório feito com o Background Builder

Assinaturas: cabeçalho branco flutuante, menu de células iguais, slot "Última
atualização", "Você está vendo" + Voltar, tooltip com borda rente.

1. Visuais exatamente sobre as áreas reservadas (use o guia de montagem).
2. Tema `.json` importado, sem cor avulsa.
3. Número de slicers coerente com o modo.
4. Páginas de corpo no `.pbix` iguais às do Builder (nome e ordem) para o Navegador.
5. Páginas de detalhe com "Você está vendo:" + "← Voltar".
6. Nenhum visual sobre os cantos de ilustração.
7. Slot "Última atualização" vinculado a medida real.
