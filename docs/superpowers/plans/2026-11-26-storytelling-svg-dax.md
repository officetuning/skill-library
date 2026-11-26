# Storytelling com cena em SVG por medida DAX: plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tornar a cena em SVG por medida DAX o padrão de storytelling do plugin, com exemplo testável e checagem automática (versão 2.6.0).

**Architecture:** Um script de checagem (`checar_svg.py`) lê o TMDL com o `tmdl_parser` existente e o PBIR em JSON. Um exemplo em script TMDL, com dados fictícios, serve de referência e de caso limpo para a checagem. As skills passam a apontar para a regra de escolha, o exemplo e a checagem.

**Tech Stack:** Python 3 (só biblioteca padrão), TMDL, PBIR, DAX, SVG, Edge sem janela para conferir o desenho.

**Spec:** `docs/superpowers/specs/2026-11-26-storytelling-svg-dax-design.md`

## Global Constraints

- O repositório é **público**: nenhum dado, nome, valor ou área de projeto real.
- Texto em português, no tom das skills existentes.
- Scripts só com biblioteca padrão, saída em UTF-8.
- Medida de cena: data URI, `dataCategory: ImageUrl`, ponto decimal forçado, `%23` e `%25`.
- Peça desenhada duas vezes ou mais vira função DAX (`Svg.Peca`, compatibilidade 1702); cena única fica numa medida.
- DaxLib.SVG (MIT) é dependência opcional; nenhum código dela é copiado. Nada das skills da Data Goblins.
- Resultado da medida abaixo de 32.766 caracteres, apresentado como precaução da casa.
- Versão **2.6.0** em `plugin.json`, `marketplace.json`, `CHANGELOG.md` e "Novidades" do `README.md`.
- Commit, push e PR **só com autorização do autor**. Nunca fazer merge.
- Arquivos de teste ficam no scratchpad da sessão (`<scratch>`), fora do repositório.

## Review Focus

1. Formato `"#,0"` e nomes como `[# Pedidos]` ou `[Faturado (Δ%)]`: não são cor nem `%` solto.
2. Comentários DAX (`--`, `//`, `/* */`) com `#`, `%` ou aspas: ignorados.
3. Data URI em base64: sem achados de `#`, `%` ou vírgula.
4. Medida auxiliar que devolve só um pedaço de SVG (sem `data:`): não exige `ImageUrl`.
5. Rodar sem a pasta do relatório: avisa que o texto alternativo não foi conferido, sem erro.

---

## Preparação (antes da tarefa 1)

- [ ] Confirmar que o PR #16 está mesclado (`gh pr view 16 --json state` → `MERGED`). Se não estiver, parar e avisar o autor.
- [ ] Com `git status` mostrando só os dois documentos em `docs/superpowers/`, criar a branch a partir da `main` atualizada: `storytelling-svg-2.6.0`.

---

### Task 1: `checar_svg.py`

**Files:**
- Create: `skills/bi-qa-documentacao/scripts/checar_svg.py`
- Modify: `skills/bi-qa-documentacao/SKILL.md` (citar o script junto de `checar_medidas.py`)
- Modify: `skills/bi-qa-documentacao/references/checagens-adicionais.md` (checagem 30)
- Test: `<scratch>/plugin/test_checar_svg.py`

**Interfaces:**
- Consumes: `tmdl_parser.parse_model(dir)` → `tabelas[].medidas[]` com `nome`, `expressao`, `props`; `auditar_visuais.obj(o, k)` e `auditar_visuais.texto_ligado(valor)`.
- Produces:
  - CLI `python checar_svg.py <SemanticModel/definition> [<Report/definition>]`
  - `analisar_medida(expressao: str, props: dict) -> list[tuple[str, str]]`, pares `(nivel, codigo)`
  - `visuais_sem_alt(relatorio: pathlib.Path, nomes: set[str]) -> list[str]`
  - Saída: uma linha `## <nivel> <codigo>: <medida ou visual>` por achado e o resumo `N medida(s) SVG; E erro(s); C a conferir.`
  - Código de saída 1 se houver `erro`; 0 se não houver (itens `conferir` não reprovam).

| código | nível | quando |
|---|---|---|
| `sem-imageurl` | erro | a expressão tem `data:image/svg+xml` e `dataCategory` não é `ImageUrl` |
| `cerquilha` | erro | cadeia DAX com `#` seguido de 3 a 8 hexadecimais, ou `url(#`; isenta se a medida troca `"#"` por `"%23"` |
| `porcento` | erro | cadeia DAX com `%` sem dois hexadecimais depois; isenta se a medida usa `SUBSTITUTE` com `"%25"` |
| `virgula` | conferir | `FORMAT` com casas decimais no formato, fora de `SUBSTITUTE(` direto e sem 3º argumento `"en-US"` |
| `sem-alt` | erro | visual que referencia a medida SVG em qualquer ponto do JSON sem `general.altText` ligado |

"Medida SVG": a expressão contém `data:image/svg+xml` ou `<svg`. Base64 (`;base64,`) isenta `cerquilha`, `porcento` e `virgula`. A leitura das cadeias é por *tokens*: pula comentários, `'Tabela'` e `[Campo]`, e entende `""` dentro da cadeia.

- [ ] **Passo 1: escrever os testes** (`unittest`, importando o script pelo caminho)

```python
URI = '"data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\'>'
IMG = {"dataCategory": "ImageUrl"}
def cod(expr, props=IMG): return sorted(c for _, c in m.analisar_medida(expr, props))

test_limpa:          cod(URI + "<rect fill='%231F4E79' width='100%25'/></svg>\"") == []
test_sem_imageurl:   cod(URI + '</svg>"', {}) == ["sem-imageurl"]
test_cerquilha:      cod(URI + "<rect fill='#1F4E79'/></svg>\"") == ["cerquilha"]
test_url_gradiente:  cod(URI + "<rect fill='url(#g)'/></svg>\"") == ["cerquilha"]
test_porcento:       cod(URI + "<rect width='100%'/></svg>\"") == ["porcento"]
test_format_pct:     cod('VAR a = FORMAT([x], "0%") RETURN ' + URI + '" & a & "</svg>"') == ["porcento"]
test_virgula:        cod('VAR a = FORMAT([x], "0.0") RETURN ' + URI + '" & a & "</svg>"') == ["virgula"]
test_virgula_ok:     o mesmo com SUBSTITUTE(FORMAT([x], "0.0"), ",", ".") == []
test_en_us:          o mesmo com FORMAT([x], "0.0", "en-US") == []
test_nomes:          cod('VAR a = FORMAT([# Pedidos], "#,0") VAR b = [Faturado (Δ%)] RETURN ' + URI + '</svg>"') == []
test_comentarios:    expressão limpa precedida de '-- cor #FFF 100%\n/* "#ABC" */\n' == []
test_base64:         cod('"data:image/svg+xml;base64,PHN2Zz4="') == []
test_fragmento:      cod('"<circle r=\'4\'/>" & "<svg></svg>"', {}) == []
test_alt:            relatório temporário com dois visuais "image" apontando para a medida,
                     um com altText por medida e um sem → visuais_sem_alt devolve só o segundo
test_sem_relatorio:  CLI só com o modelo → saída contém "texto alternativo não conferido", código 0
test_codigo_saida:   CLI num modelo com um defeito "erro" → código 1
```

- [ ] **Passo 2: rodar e ver falhar**: `python <scratch>/plugin/test_checar_svg.py` → falha por script inexistente.
- [ ] **Passo 3: implementar** `checar_svg.py` com as interfaces acima e docstring de uso no padrão de `checar_medidas.py`. A docstring avisa que conversão implícita de número em texto não é detectada.
- [ ] **Passo 4: rodar os testes** → todos passam.
- [ ] **Passo 5: documentar** o script no `SKILL.md` e como checagem 30 em `checagens-adicionais.md` (tabela de códigos acima).
- [ ] **Passo 6: commit**: `bi-qa: checar_svg.py para medidas de cena em SVG`.

---

### Task 2: exemplo completo de cena

**Files:**
- Create: `skills/powerbi-visuais/references/cena-svg-exemplo.md`
- Test: `<scratch>/plugin/test_exemplo.py`

**Interfaces:**
- Consumes: `checar_svg.py` (tarefa 1).
- Produces: script TMDL `createOrReplace` da tabela `Entregas` com as medidas `Caminhão até a Meta` e `Caminhão (Texto Alternativo)`, pasta de exibição `Storytelling`, com `///`.

Cena: caminhão numa estrada até a bandeira da meta; 720×200; estrada de x=40 a x=664; bandeira em x=560 (100%); arte plana com volume simples (cabine, baú, rodas, sombra), cores fixas do exemplo.

Tabela calculada `Entregas` (`Região`, `Pedidos Entregues`, `Meta de Pedidos`), fictícia:

| Região | Entregues | Meta | Estado que exercita |
|---|---|---|---|
| Sul | 82 | 100 | abaixo |
| Norte | 124 | 100 | acima, com teto em 120% |
| Leste | 60 | vazio | sem meta |
| Oeste | vazio | 80 | sem entregas |

Regras: o percentual usa só as entregas das regiões **com meta** no contexto; `vXCaminhao = 40 + MIN ( MAX ( vPercentual, 0 ), 1.2 ) * 520`.

| Contexto | `vXTexto` | Cena | Rótulo |
|---|---|---|---|
| Sul | `466.4` | caminhão e bandeira | `82 de 100 pedidos (82%)` |
| Norte | `664.0` | caminhão além da bandeira | `124 de 100 pedidos (124%)` |
| Leste | ausente | caminhão parado em 40, sem bandeira | `60 pedidos, sem meta` |
| Oeste | `40.0` | caminhão na largada | `0 de 80 pedidos (0%)` |
| Região sem linha | ausente | só a estrada | `Sem entregas no período` |
| sem filtro | `422.6` | caminhão e bandeira | `206 de 280 pedidos (74%)` |

Montagem testável: o `RETURN` é só `"data:image/svg+xml;utf8," & <cadeias> & <VARs>`; as partes condicionais ficam em `vCaminhao`, `vBandeira` e `vRotulo`; no rótulo, `%` sai como `%25`.

O documento traz, nesta ordem: o que a cena responde (teste dos 5 segundos), a regra do percentual (por que é verdadeira com qualquer filtro), o script TMDL, como montar (visual de imagem, texto alternativo por medida, segmentação por `Região`, alternativa na imagem do cartão), a descrição longa (tabela nativa com os três campos na mesma página), os estados esperados e a consulta de tamanho `EVALUATE ROW ( "Tamanho", LEN ( [Caminhão até a Meta] ) )`.

- [ ] **Passo 1: escrever o teste.** Extrai o bloco ```` ```tmdl ```` do `.md`, grava `definition/tables/Entregas.tmdl` temporário (sem a linha `createOrReplace` e um nível de tabulação), roda `checar_svg.py` e exige nenhum achado: `1 medida(s) SVG; 0 erro(s); 0 a conferir.` Depois planta, em cópias, um defeito por código (`sem-imageurl`, `cerquilha`, `porcento`, `virgula`) e exige que cada cópia acuse o seu.
- [ ] **Passo 2: rodar e ver falhar** (arquivo inexistente).
- [ ] **Passo 3: escrever o documento** conforme acima.
- [ ] **Passo 4: rodar o teste** → passa.
- [ ] **Passo 5: conferir o desenho.** O teste monta o SVG de cada linha da tabela de estados a partir das cadeias da própria medida (VARs preenchidas conforme a tabela), valida como XML (`xml.dom.minidom`) e grava um HTML com os seis estados; capturar com o Edge sem janela e **olhar a imagem**: nada cortado, sobreposto ou com cara de boneco de palito. Mostrar a captura ao autor antes do commit.
- [ ] **Passo 6: commit**: `powerbi-visuais: exemplo de cena em SVG por medida`.

---

### Task 3: regra nas skills

**Files (Modify):**
- `skills/data-storytelling/SKILL.md`: trocar o item "Arte 3D vem de gerador de imagem" pela **tabela de regra de escolha** do spec; manter o teste dos 5 segundos e a identidade.
- `skills/data-storytelling/references/storytelling-com-imagem.md`: seção 2e vira o padrão (itens 1 a 4 do "Padrão da cena"); na seção 3, "Quem desenha a arte" passa a seguir a tabela; link para o exemplo.
- `skills/powerbi-visuais/SKILL.md`: em "Visual gerado por DAX", "nativo primeiro" vale para análise; cena que muda com o dado é a exceção padrão.
- `skills/powerbi-visuais/references/svg-html-dax.md`: abertura com a mesma exceção; imagem do cartão com estados padrão e *hover*; funções DAX e DaxLib.SVG 2.0.0 (incompatível com 1.x); nota do exemplo da Microsoft em `en-US`; tamanho (32.766, com a ressalva); acessibilidade em duas partes no lugar do item "Acessibilidade é requisito formal"; fontes do spec.
- `skills/dax-udf/SKILL.md`: parágrafo curto: peça usada 2+ vezes vira `Svg.Peca`; link para o exemplo.

**Interfaces:** consome o caminho do exemplo (tarefa 2) e o nome `checar_svg.py` (tarefa 1).

- [ ] **Passo 1: editar** os cinco arquivos preservando o fim de linha de cada um.
- [ ] **Passo 2: conferir contradições**: buscar em `skills/` por `nativo primeiro`, `Visual nativo`, `gerador de imagem`, `leitor de tela`; cada ocorrência concorda com a regra de escolha.
- [ ] **Passo 3: conferir fontes**: cada URL nova está na lista do spec; nenhuma afirmação além do que a fonte diz.
- [ ] **Passo 4: conferir links relativos**: todo `references/…` e `scripts/…` citado existe.
- [ ] **Passo 5: commit**: `Storytelling: cena em SVG por medida como padrão`.

---

### Task 4: versão 2.6.0 e entrega

**Files (Modify):** `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `CHANGELOG.md`, `README.md`

- [ ] **Passo 1:** versão `2.6.0` nos quatro lugares, com entrada no `CHANGELOG.md` e em "Novidades".
- [ ] **Passo 2:** rodar a comparação de `.github/workflows/versao.yml` localmente → `Versões coincidem: 2.6.0`.
- [ ] **Passo 3:** rodar de novo os dois testes → passam. Varrer o diff por nomes de projeto real → nenhum.
- [ ] **Passo 4: commit**: `Versão 2.6.0`.
- [ ] **Passo 5 (autor):** no Desktop, relatório em branco → TMDL view → aplicar o script do exemplo → visual de imagem + segmentação → conferir os estados e o `LEN`. Salvar.
- [ ] **Passo 6:** com autorização, push e PR; no corpo, o que foi testado e o que depende do passo 5.
