#!/usr/bin/env node
/**
 * Exporta a coleção do Background Builder sem cliques humanos.
 *
 * Uso:
 *   node exportar-colecao.cjs --ficha "<arquivo .md ou .json>" --saida "<pasta>" [--url <endereço>] [--navegador msedge|chrome|chromium] [--visivel]
 *
 * O que faz:
 *   1. Lê a Ficha Técnica (.md com bloco ```json no fim) ou um .json puro.
 *   2. Remove os campos só de saída (_appVersion, resolvedPalette, filtrosForaDoPainel)
 *      para o Builder não abrir o aviso de "ficha de versão anterior".
 *   3. Abre o Builder num navegador sem janela, carrega a ficha pelo campo
 *      "Abrir Ficha Técnica" e confere se o H1 foi aplicado.
 *   4. Clica em "Exportar coleção", espera a verificação de pixels e salva o ZIP.
 *
 * Requisito: o pacote "playwright" (npm). Por padrão usa o Microsoft Edge já
 * instalado no Windows, então não precisa baixar navegador.
 * Saída: imprime uma linha JSON com { ok, zip, paginas, versaoBuilder } ou { ok:false, erro }.
 */
const fs = require("fs");
const os = require("os");
const path = require("path");

function args() {
  const a = process.argv.slice(2);
  const out = { url: "https://backgroundbuilder.officetuning.ai/", navegador: "msedge", visivel: false };
  for (let i = 0; i < a.length; i++) {
    const k = a[i];
    if (k === "--ficha") out.ficha = a[++i];
    else if (k === "--saida") out.saida = a[++i];
    else if (k === "--url") out.url = a[++i];
    else if (k === "--navegador") out.navegador = a[++i];
    else if (k === "--visivel") out.visivel = true;
  }
  if (!out.ficha || !out.saida) {
    throw new Error('Informe --ficha "<arquivo>" e --saida "<pasta>".');
  }
  return out;
}

/** Último bloco ```json que parseia (mesma regra do Builder) ou o arquivo inteiro, se for JSON. */
function lerColecao(arquivo) {
  const texto = fs.readFileSync(arquivo, "utf8");
  const blocos = [...texto.matchAll(/```json\s*([\s\S]*?)```/g)];
  for (let i = blocos.length - 1; i >= 0; i--) {
    try { return JSON.parse(blocos[i][1]); } catch { /* tenta o anterior */ }
  }
  return JSON.parse(texto);
}

function montarFicha(colecao) {
  const limpo = { ...colecao };
  for (const k of ["_appVersion", "_origem", "resolvedPalette", "filtrosForaDoPainel"]) delete limpo[k];
  if (typeof limpo.h1 !== "string" || !limpo.h1.trim()) throw new Error("A ficha precisa de h1.");
  const json = JSON.stringify(limpo, null, 2).replace(/`/g, "\\u0060");
  return { limpo, md: `# Ficha Técnica — ${limpo.h1}\n\n\`\`\`json\n${json}\n\`\`\`\n` };
}

/** playwright do projeto/NODE_PATH ou, se não houver, da pasta padrão ~/.bb-automacao. */
function carregarPlaywright() {
  try { return require("playwright"); } catch { /* tenta a pasta padrão */ }
  const padrao = path.join(os.homedir(), ".bb-automacao", "node_modules", "playwright");
  try { return require(padrao); } catch {
    throw new Error(`Playwright não instalado. Rode uma vez nesta máquina: npm install --prefix "${path.join(os.homedir(), ".bb-automacao")}" playwright`);
  }
}

async function main() {
  const o = args();
  const { chromium } = carregarPlaywright();
  const { limpo, md } = montarFicha(lerColecao(o.ficha));
  const tmp = path.join(os.tmpdir(), `bb-ficha-${Date.now()}.md`);
  fs.writeFileSync(tmp, md, "utf8");
  fs.mkdirSync(o.saida, { recursive: true });

  const lancar = { headless: !o.visivel };
  if (o.navegador !== "chromium") lancar.channel = o.navegador;
  const browser = await chromium.launch(lancar);
  try {
    const ctx = await browser.newContext({ acceptDownloads: true, locale: "pt-BR", viewport: { width: 1600, height: 1000 } });
    // Sem a janela de boas-vindas.
    await ctx.addInitScript(() => { try { localStorage.setItem("bgbuilder.welcomeSeen", "1"); } catch { /* ignora */ } });
    const page = await ctx.newPage();
    const alertas = [];
    page.on("dialog", (d) => { alertas.push(d.message()); d.dismiss().catch(() => {}); });
    await page.goto(o.url, { waitUntil: "networkidle", timeout: 90000 });

    // Campo exato de "Abrir Ficha Técnica". O outro campo (".json,.md,...") é o
    // importador de projeto de outro endereço e abre uma janela diferente.
    const campo = page.locator('input[type=file][accept=".md,text/markdown"]');
    await campo.waitFor({ state: "attached", timeout: 30000 });
    await campo.setInputFiles(tmp);

    // Confere se o H1 chegou ao formulário.
    const h1 = limpo.h1.trim();
    await page.waitForFunction(
      (esperado) => [...document.querySelectorAll("input")].some((i) => i.value === esperado),
      h1,
      { timeout: 15000 },
    ).catch(() => { throw new Error("O Builder não aplicou a ficha (H1 não apareceu no formulário). A interface pode ter mudado."); });

    const versaoBuilder = await page.evaluate(() => document.body.innerText.match(/v\d+\.\d+/)?.[0] ?? null);
    const botao = page.locator('[role=toolbar] button.bg-accent').first();
    const [download] = await Promise.all([
      page.waitForEvent("download", { timeout: 240000 }),
      botao.click(),
    ]).catch(async (e) => {
      const relatorio = await page.locator("[role=region]").first().innerText().catch(() => "");
      if (relatorio.includes("✗")) throw new Error(`ZIP bloqueado pela verificação de pixels:\n${relatorio}`);
      if (alertas.length) throw new Error(`Falha na exportação: ${alertas.join(" | ")}`);
      throw e;
    });
    // Mesmo nome que o Builder dá ao arquivo; sem caracteres proibidos no Windows.
    const nome = `${h1.replace(/[\\/:*?"<>|]/g, "-")} - Coleção.zip`;
    const zip = path.join(o.saida, nome);
    await download.saveAs(zip);
    const paginas = await page.$$eval("[role=region] tbody tr", (linhas) =>
      linhas.map((tr) => ({ pagina: tr.cells[0]?.innerText.trim(), ok: !tr.innerText.includes("✗") })));
    console.log(JSON.stringify({ ok: true, zip, paginas, versaoBuilder }));
  } finally {
    await browser.close();
    fs.rmSync(tmp, { force: true });
  }
}

main().catch((e) => {
  console.log(JSON.stringify({ ok: false, erro: String(e && e.message ? e.message : e) }));
  process.exit(1);
});
