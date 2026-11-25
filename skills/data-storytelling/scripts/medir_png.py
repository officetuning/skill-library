#!/usr/bin/env python3
"""Mede elementos em um PNG sem instalar nada (só biblioteca padrão).

Dois usos, ambos para posicionar visuais do Power BI sobre uma arte pronta:

1. balões de chamada de um infográfico (contorno colorido, interior vazio):

   python medir_png.py baloes arte.png --cor escuro=10,10,14 --cor azul=30,140,240 \
       --cor laranja=255,90,30

   Para cada cor, acha os trechos horizontais longos (as bordas de cima e de baixo
   dos balões) e imprime o retângulo. O trecho reto não inclui os cantos
   arredondados: o balão real tem `--canto` px a mais de cada lado (padrão 34 em
   imagem de ~2170 px de largura).

2. retângulos "fantasma" (nichos) do plano de fundo do Background Builder, que é
   onde entram as segmentações:

   python medir_png.py retangulos fundo.png --ref 100,492

   `--ref x,y` é um ponto dentro de qualquer retângulo fantasma; o script varre a
   coluna x e imprime cada retângulo (y, altura, x, largura).

Também: `cor arte.png --caixa x0,x1,y` devolve a cor mais forte do contorno.

Exemplos medidos (nov/2026): balões de um infográfico 2172×724 com cantos de ~34 px;
segmentações do Builder em x40, largura 296, altura 40 (Período 120).
"""
import argparse
import struct
import sys
import zlib


# Saída em UTF-8 mesmo em console cp1252 (Windows) ou com `python -I`.
for _fluxo in (sys.stdout, sys.stderr):
    try:
        _fluxo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def ler_png(caminho):
    d = open(caminho, "rb").read()
    assert d[:8] == b"\x89PNG\r\n\x1a\n", "não é PNG"
    pos, idat = 8, b""
    while pos < len(d):
        n, = struct.unpack(">I", d[pos:pos + 4])
        tipo, corpo = d[pos + 4:pos + 8], d[pos + 8:pos + 8 + n]
        if tipo == b"IHDR":
            w, h, prof, ct, _, _, entrelaçado = struct.unpack(">IIBBBBB", corpo)
        elif tipo == b"IDAT":
            idat += corpo
        pos += 12 + n
    assert prof == 8 and entrelaçado == 0, "só PNG de 8 bits sem entrelaçamento"
    canais = {0: 1, 2: 3, 4: 2, 6: 4}[ct]
    bruto = zlib.decompress(idat)
    passo, linhas, ant, p = w * canais, [], bytearray(w * canais), 0
    for _ in range(h):
        f = bruto[p]
        lin = bytearray(bruto[p + 1:p + 1 + passo])
        p += 1 + passo
        for i in range(passo):
            a = lin[i - canais] if i >= canais else 0
            b = ant[i]
            c = ant[i - canais] if i >= canais else 0
            if f == 1:
                lin[i] = (lin[i] + a) & 255
            elif f == 2:
                lin[i] = (lin[i] + b) & 255
            elif f == 3:
                lin[i] = (lin[i] + ((a + b) >> 1)) & 255
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                lin[i] = (lin[i] + pr) & 255
        linhas.append(lin)
        ant = lin
    return w, h, canais, linhas


def perto(p, c, tol):
    return abs(p[0] - c[0]) + abs(p[1] - c[1]) + abs(p[2] - c[2]) < tol


def baloes(args):
    w, h, ch, linhas = ler_png(args.arquivo)
    print(f"imagem {w}x{h}")
    for par in args.cor:
        nome, rgb = par.split("=")
        cor = tuple(int(x) for x in rgb.split(","))
        trechos = []
        for y in range(int(h * args.topo)):
            lin, x = linhas[y], 0
            while x < w:
                if perto(lin[x * ch:x * ch + 3], cor, args.tol):
                    x0 = x
                    while x < w and perto(lin[x * ch:x * ch + 3], cor, args.tol):
                        x += 1
                    if x - x0 >= args.min:
                        trechos.append((y, x0, x - 1))
                else:
                    x += 1
        grupos = []
        for y, a, b in trechos:
            for g in grupos:
                if abs(g["a"] - a) < 40 and abs(g["b"] - b) < 40:
                    g["ys"].append(y)
                    break
            else:
                grupos.append({"a": a, "b": b, "ys": [y]})
        for g in sorted(grupos, key=lambda g: g["a"]):
            if max(g["ys"]) - min(g["ys"]) > 60:  # tem borda de cima e de baixo
                print(f"{nome:10s} reto x {g['a']}-{g['b']}  y {min(g['ys'])}-{max(g['ys'])}  "
                      f"=> balão x {g['a'] - args.canto}-{g['b'] + args.canto}")


def retangulos(args):
    w, h, ch, linhas = ler_png(args.arquivo)
    rx, ry = (int(v) for v in args.ref.split(","))
    ref = tuple(linhas[ry][rx * ch:rx * ch + 3])
    print(f"cor fantasma {ref}")
    y = 0
    while y < h:
        if perto(linhas[y][rx * ch:rx * ch + 3], ref, 6):
            y0 = y
            while y < h and perto(linhas[y][rx * ch:rx * ch + 3], ref, 6):
                y += 1
            if y - y0 >= 20:
                ym = (y0 + y) // 2
                xa = rx
                while xa > 0 and perto(linhas[ym][(xa - 1) * ch:(xa - 1) * ch + 3], ref, 6):
                    xa -= 1
                xb = rx
                while xb < w - 1 and perto(linhas[ym][(xb + 1) * ch:(xb + 1) * ch + 3], ref, 6):
                    xb += 1
                print(f"y {y0}-{y - 1} (altura {y - y0})  x {xa}-{xb} (largura {xb - xa + 1})")
        else:
            y += 1


def cor(args):
    w, h, ch, linhas = ler_png(args.arquivo)
    x0, x1, y = (int(v) for v in args.caixa.split(","))
    melhor = None
    for yy in range(y - 3, y + 8):
        for x in range(x0, x1, 3):
            r, g, b = linhas[yy][x * ch:x * ch + 3]
            chave = (max(r, g, b) - min(r, g, b), -(r + g + b))
            if melhor is None or chave > melhor[0]:
                melhor = (chave, (r, g, b))
    print("#%02X%02X%02X" % melhor[1])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("baloes")
    b.add_argument("arquivo")
    b.add_argument("--cor", action="append", required=True, help="nome=R,G,B (repita)")
    b.add_argument("--tol", type=int, default=90)
    b.add_argument("--min", type=int, default=100, help="comprimento mínimo do trecho reto")
    b.add_argument("--canto", type=int, default=34)
    b.add_argument("--topo", type=float, default=0.4, help="fração do topo da imagem a varrer")
    b.set_defaults(f=baloes)
    r = sub.add_parser("retangulos")
    r.add_argument("arquivo")
    r.add_argument("--ref", required=True, help="x,y de um ponto dentro de um retângulo fantasma")
    r.set_defaults(f=retangulos)
    c = sub.add_parser("cor")
    c.add_argument("arquivo")
    c.add_argument("--caixa", required=True, help="x0,x1,y: trecho da borda de cima do balão")
    c.set_defaults(f=cor)
    a = ap.parse_args()
    sys.exit(a.f(a))
