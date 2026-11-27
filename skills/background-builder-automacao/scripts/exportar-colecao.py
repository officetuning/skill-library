#!/usr/bin/env python3
"""Exporta a coleção do Background Builder sem cliques, para máquina sem Node.

Uso:
    python exportar-colecao.py --ficha "<arquivo .md ou .json>" --saida "<pasta>"
        [--url <endereço>] [--navegador msedge|chrome|chromium] [--visivel]
        [--sem-marca] [--bloquear-envios]

Mesmo fluxo do exportar-colecao.cjs: carrega a ficha em "Abrir Ficha Técnica", confere
o H1, clica em "Exportar coleção" e salva o ZIP. Com --bloquear-envios, aborta toda
requisição que não seja GET: a ficha é lida só no navegador (as contagens de uso do site
também deixam de ser enviadas).

Requisito: pacote "playwright" do Python (pip install playwright), de preferência num
ambiente virtual. Por padrão usa o Microsoft Edge instalado; não baixa navegador.
Saída: uma linha JSON com { ok, zip, paginas, versaoBuilder, bloqueados } ou { ok, erro }.
"""
import argparse
import json
import os
import re
import sys
import tempfile

URL = "https://backgroundbuilder.officetuning.ai/"
SO_SAIDA = ("_appVersion", "_origem", "resolvedPalette", "filtrosForaDoPainel")


def ler_colecao(arquivo):
    """Último bloco ```json que interpreta (mesma regra do Builder) ou o arquivo inteiro."""
    with open(arquivo, encoding="utf-8-sig") as f:
        texto = f.read()
    for bloco in reversed(re.findall(r"```json\s*(.*?)```", texto, re.S)):
        try:
            return json.loads(bloco)
        except ValueError:
            pass
    return json.loads(texto)


def montar_ficha(colecao):
    limpo = {k: v for k, v in colecao.items() if k not in SO_SAIDA}
    h1 = limpo.get("h1")
    if not isinstance(h1, str) or not h1.strip():
        raise ValueError("A ficha precisa de h1.")
    corpo = json.dumps(limpo, ensure_ascii=False, indent=2).replace("`", "\\u0060")
    return h1.strip(), f"# Ficha Técnica — {h1}\n\n```json\n{corpo}\n```\n"


def exportar(o):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError("Playwright não instalado. Rode uma vez: python -m pip install playwright")
    h1, md = montar_ficha(ler_colecao(o.ficha))
    os.makedirs(o.saida, exist_ok=True)
    bloqueados = []
    with tempfile.TemporaryDirectory() as pasta, sync_playwright() as p:
        ficha = os.path.join(pasta, "ficha.md")
        with open(ficha, "w", encoding="utf-8") as f:
            f.write(md)
        opcoes = {"headless": not o.visivel}
        if o.navegador != "chromium":
            opcoes["channel"] = o.navegador
        navegador = p.chromium.launch(**opcoes)
        try:
            contexto = navegador.new_context(accept_downloads=True, locale="pt-BR",
                                             viewport={"width": 1600, "height": 1000})
            contexto.add_init_script("try { localStorage.setItem('bgbuilder.welcomeSeen', '1'); } catch (e) {}")
            if o.bloquear_envios:
                def filtrar(rota):
                    if rota.request.method != "GET":
                        bloqueados.append(rota.request.method)
                        return rota.abort()
                    return rota.continue_()
                contexto.route("**/*", filtrar)
            pagina = contexto.new_page()
            alertas = []
            pagina.on("dialog", lambda d: (alertas.append(d.message), d.dismiss()))
            try:
                pagina.goto(o.url, wait_until="networkidle", timeout=30000)
            except Exception:
                pagina.goto(o.url, wait_until="domcontentloaded", timeout=90000)
            campo = pagina.locator('input[type=file][accept=".md,text/markdown"]')
            campo.wait_for(state="attached", timeout=30000)
            campo.set_input_files(ficha)
            try:
                pagina.wait_for_function(
                    "e => [...document.querySelectorAll('input')].some(i => i.value === e)", arg=h1, timeout=15000)
            except Exception:
                raise RuntimeError("O Builder não aplicou a ficha (H1 não apareceu). A interface pode ter mudado.")
            if o.sem_marca:
                pagina.keyboard.press("Control+Alt+8")
                pagina.wait_for_timeout(1500)
            versao = pagina.evaluate("() => document.body.innerText.match(/v\\d+\\.\\d+/)?.[0] ?? null")
            try:
                with pagina.expect_download(timeout=240000) as baixado:
                    pagina.locator("[role=toolbar] button.bg-accent").first.click()
            except Exception:
                regiao = pagina.locator("[role=region]").first
                relatorio = regiao.inner_text() if regiao.count() else ""
                if "✗" in relatorio:
                    raise RuntimeError("ZIP bloqueado pela verificação de pixels:\n" + relatorio)
                if alertas:
                    raise RuntimeError("Falha na exportação: " + " | ".join(alertas))
                raise
            nome = re.sub(r'[\\/:*?"<>|]', "-", h1) + " - Coleção.zip"
            destino = os.path.join(o.saida, nome)
            baixado.value.save_as(destino)
            paginas = pagina.eval_on_selector_all(
                "[role=region] tbody tr",
                "l => l.map(tr => ({ pagina: tr.cells[0]?.innerText.trim(), ok: !tr.innerText.includes('✗') }))")
        finally:
            navegador.close()
    return {"ok": True, "zip": destino, "paginas": paginas, "versaoBuilder": versao,
            "bloqueados": len(bloqueados)}


def main():
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8")
        except Exception:
            pass
    a = argparse.ArgumentParser(description="Exporta a coleção do Background Builder.")
    a.add_argument("--ficha", required=True)
    a.add_argument("--saida", required=True)
    a.add_argument("--url", default=URL)
    a.add_argument("--navegador", default="msedge", choices=["msedge", "chrome", "chromium"])
    a.add_argument("--visivel", action="store_true")
    a.add_argument("--sem-marca", action="store_true")
    a.add_argument("--bloquear-envios", action="store_true")
    try:
        print(json.dumps(exportar(a.parse_args()), ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"ok": False, "erro": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
