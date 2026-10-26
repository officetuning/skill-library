# Fontes de dados para dashboard HTML

## Regra geral

A IA lê a fonte, perfila, **calcula em código** e embute o resultado agregado no
HTML. Ler a fonte direto do navegador (dado "ao vivo" num arquivo `.html`) só
funciona bem com fonte pública; para dado corporativo, prefira o painel ao vivo
da própria plataforma (`plataformas.md`).

| Fonte | Snapshot (IA embute) | Ao vivo dentro do HTML |
|---|---|---|
| CSV | ✔ | Botão "Trocar dados" lê CSV local (template) |
| Excel local | ✔ (IA converte para JSON) | Possível com SheetJS; desaconselhado |
| Excel no OneDrive for Business / SharePoint | ✔ via Analyst, Copilot Code, conector do Claude ou app do ChatGPT | ✖ no HTML solto; use Copilot Code + Managed Runtime |
| Google Sheets | ✔ via Gemini, conector do Claude ou app do ChatGPT | Só com planilha publicada (pública) |

---

## Contrato dos dados embutidos

```html
<script type="application/json" id="dados">
{
  "meta": {
    "titulo": "Receita por Região",
    "fonte": "Vendas_2026.xlsx › Tabela tbVendas",
    "extraido_em": "2026-10-26",
    "linhas_fonte": 18240,
    "total_controle": 8383618.16,
    "exemplo": false
  },
  "linhas": [
    {"data": "2026-01-01", "regiao": "Sudeste", "receita": 183512.40, "pedidos": 561}
  ]
}
</script>
```

- `linhas` já agregadas (mês × categoria). 18 mil linhas de venda viram dezenas.
- Datas em `AAAA-MM-DD`; números com ponto decimal, sem separador de milhar.
- `total_controle` vem da **fonte bruta**, calculado antes da agregação. Se a
  soma das linhas embutidas não bater, a agregação perdeu ou duplicou algo.

### Volume

| Linhas embutidas | Abordagem |
|---|---|
| Até 1.000 | Embutir direto |
| 1.000 a 10.000 | Embutir; agregar para os gráficos |
| 10.000 a 100.000 | Agregar antes; embutir só o agregado |
| Acima de 100.000 | Não é caso de HTML solto: Power BI ou painel ao vivo |

Gráfico de linha: até ~500 pontos por série. Barras: até ~50 categorias.
Tabela: pagine acima de 100–200 linhas.

---

## CSV brasileiro

Exportações do Excel em português costumam vir com:

- separador **`;`** (porque a vírgula é decimal);
- decimal **`,`** e milhar **`.`** (`1.234,56`);
- codificação **Windows-1252** (acentos quebram como `RegiÃ£o`) ou **UTF-8 com
  BOM** (primeira coluna vira `﻿data`);
- datas `dd/mm/aaaa`.

Peça à IA para tratar isso **explicitamente** no perfil. Em Python:

```python
import csv
import pandas as pd

def ler_csv_br(caminho):
    """Lê CSV exportado no Brasil (; e 1.234,56) ou internacional (, e 1234.56)."""
    for cod in ("utf-8-sig", "cp1252"):
        try:
            with open(caminho, encoding=cod) as f:
                amostra = f.read(20000)
            break
        except UnicodeDecodeError:
            continue
    sep = csv.Sniffer().sniff(amostra, delimiters=";,\t").delimiter
    br = sep == ";"                       # ";" quase sempre indica decimal com vírgula
    df = pd.read_csv(caminho, sep=sep, encoding=cod,
                     decimal="," if br else ".",
                     thousands="." if br else None)
    df.columns = df.columns.str.strip()
    df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")
    return df

df = ler_csv_br("vendas.csv")
print(df.dtypes, len(df), df["data"].min(), df["data"].max())
print("nulos:", df.isna().sum().to_dict())
print("duplicados:", df.duplicated().sum())
print("total de controle:", round(df["receita"].sum(), 2))
```

⚠️ Não aplique `thousands="."` a um CSV separado por vírgula: `1234.5` vira
`12345` sem erro nenhum. Por isso o código decide a convenção pelo separador.
Confira se as colunas numéricas saíram como número (`float64`), não como texto.

No navegador, o template usa PapaParse com `delimiter: ""` (autodetecção) e a
mesma regra: arquivo com `;` lê `1.234,56` e `1.234` como milhar; arquivo com
`,` lê `1234.56`.

---

## Excel

- Use uma **Tabela do Excel** (Inserir → Tabela) com cabeçalho de uma linha.
  Sem células mescladas, sem subtotais no meio, sem linhas em branco.
- Diga à IA **qual aba ou tabela** usar. Várias abas parecidas confundem.
- Fórmulas: a IA lê o **valor salvo** da última vez que o arquivo foi
  calculado. Abra e salve no Excel antes de anexar.
- Prefira que a IA converta para JSON em Python (`pd.read_excel(arquivo,
  sheet_name="Vendas")`) a carregar uma biblioteca de Excel no navegador. Se
  precisar ler `.xlsx` no navegador, a SheetJS distribui as versões atuais pela
  própria CDN (cdn.sheetjs.com); o pacote `xlsx` do npm parou na 0.18.5.

---

## OneDrive for Business e SharePoint

O HTML aberto no navegador **não consegue** baixar o Excel de um link do
OneDrive corporativo: o arquivo exige login do Microsoft Entra e o navegador
bloqueia a leitura entre domínios. Caminhos que funcionam:

1. **Snapshot pela IA** (mais simples): Analyst, Copilot Code, conector
   Microsoft 365 do Claude ou app SharePoint/OneDrive do ChatGPT leem o arquivo
   com suas permissões e a IA embute o agregado.
2. **Ao vivo no Microsoft 365:** Copilot Code publica o app no Copilot Managed
   Runtime; cada pessoa vê o que já pode ver na fonte (Frontier, preview).
3. **Projeto de desenvolvimento:** app registrado no Entra + MSAL + Microsoft
   Graph para ler a planilha. Exige TI; fora do escopo de "dashboard com IA".

Evite gerar link "qualquer pessoa" para contornar o login: o arquivo inteiro
fica público.

---

## Google Sheets

### Snapshot

Anexe a planilha ao Gemini (Drive), ao Claude (conector Google Drive) ou ao
ChatGPT (app Google Drive). Peça a aba exata.

### Ao vivo no HTML (só para dado público)

Duas URLs comuns, ambas exigem acesso sem login:

| Forma | URL | Compartilhamento exigido |
|---|---|---|
| Publicar na Web | `Arquivo → Compartilhar → Publicar na Web → aba → CSV` → `.../pub?gid=<GID>&single=true&output=csv` | Publicada (pública e indexável) |
| Consulta gviz | `https://docs.google.com/spreadsheets/d/<ID>/gviz/tq?tqx=out:csv&gid=<GID>` | "Qualquer pessoa com o link" pode ver |

```js
// Lê a planilha publicada; se falhar, usa os dados embutidos.
const URL_CSV = "https://docs.google.com/spreadsheets/d/e/<CHAVE>/pub?gid=0&single=true&output=csv";
Papa.parse(URL_CSV, {
  download: true, header: true, skipEmptyLines: true,
  complete: (r) => { base.linhas = r.data; base.meta.fonte = "Google Sheets (publicada)"; normalizar(); },
  error: () => mostrarErro("Planilha indisponível; exibindo a última cópia embutida.")
});
```

- Teste no navegador: o Google pode demorar alguns minutos para refletir a
  mudança na versão publicada, e a leitura entre domínios pode falhar em alguns
  ambientes.
- Mantenha os dados embutidos como reserva.
- O `gid` é o número da aba que aparece na URL (`#gid=123456`).
- **Nunca** use isso para dado interno. Para equipe, Sheets canvas.

---

## Checklist da fonte

- [ ] Cabeçalho único na linha 1; uma linha por registro
- [ ] Sem células mescladas, subtotais ou linhas em branco no meio
- [ ] Separador, decimal e codificação conferidos (CSV)
- [ ] Aba ou tabela nomeada no pedido
- [ ] Total de controle calculado na fonte bruta
- [ ] Nenhuma coluna pessoal ou sigilosa que o painel não precise
