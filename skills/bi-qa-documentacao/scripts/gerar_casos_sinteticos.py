"""Gera os arquivos de casos do modelo sintético, com os valores de controle.

Os esperados são calculados aqui, em Python, a partir das linhas de origem, e não
pelo DAX que está sendo testado. As UDFs são lidas do medidas.md publicado.

Uso: python gerar_casos_sinteticos.py   (grava em ../assets)
"""
import json
import re
from datetime import date
from decimal import Decimal
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
MEDIDAS_MD = SKILL.parent / 'calendario-inteligencia-tempo' / 'references' / 'medidas.md'

LINHAS = [  # 'Vendas'[Data], 'Vendas'[Valor da Venda]
    (date(2023, 2, 28), 7),     # 29/02: destino no modo clássico
    (date(2023, 3, 1), 11),     # 29/02: destino no modo calendário
    (date(2024, 2, 29), 29),
    (date(2025, 1, 10), 100),   # Sem valor atual (jan/2026 vazio)
    (date(2025, 3, 5), 50),     # Base zero: 50 - 50
    (date(2025, 3, 20), -50),
    (date(2025, 4, 15), -100),  # Base negativa
    (date(2025, 5, 8), 100),    # Sem variação
    (date(2025, 6, 3), 120),    # Queda
    (date(2025, 6, 18), 80),
    (date(2026, 2, 12), 100),   # Sem ano anterior (fev/2025 vazio)
    (date(2026, 3, 9), 100),
    (date(2026, 4, 14), -50),
    (date(2026, 5, 11), 100),
    (date(2026, 6, 16), 150),
]

PERIODOS = [  # nome, ano, mês (None = ano inteiro)
    ('Sem valor atual', 2026, 1), ('Sem ano anterior', 2026, 2),
    ('Base zero', 2026, 3), ('Base negativa', 2026, 4),
    ('Sem variação', 2026, 5), ('Queda', 2026, 6),
    ('Só ano anterior', 2025, 2), ('Ano inteiro', 2026, None),
]


def soma(ano, mes):
    valores = [v for d, v in LINHAS if d.year == ano and mes in (None, d.month)]
    return sum(valores) if valores else None  # sem linha = em branco


def regra(av, aa):
    """Regra de comparativo-ano-anterior.md, maior é melhor."""
    if av is None or aa is None:
        return None, None, None
    delta = av - aa
    pct = None if aa == 0 else float(Decimal(delta) / Decimal(abs(aa)))
    farol = '✔️' if delta > 0 else '⚠️' if delta == 0 else '❗'
    return delta, pct, farol


def filtro(ano, mes):
    texto = f"'Calendário'[Ano] = {ano}"
    return texto + (f", 'Calendário'[Mês #] = {mes}" if mes else '')


DIA = "'Calendário'[Data] = DATE ( 2024, 2, 29 )"


def verificacao(medida, onde, esperado):
    return {'expressao': f'CALCULATE ( {medida}, {onde} )', 'esperado': esperado}


def udfs():
    bloco = MEDIDAS_MD.read_text(encoding='utf-8')
    bloco = bloco.split('## UDF com CALENDARREF')[1].split('```dax')[1].split('EVALUATE')[0]
    bloco = re.sub(r'(?m)^\s*///.*\n', '', bloco)
    partes = (p.split('=', 1) for p in re.split(r'FUNCTION\s+', bloco)[1:])
    return {nome.strip(): corpo.strip() for nome, corpo in partes}


def gravar(nome, conteudo):
    caminho = SKILL / 'assets' / nome
    texto = json.dumps(conteudo, ensure_ascii=False, indent=2) + '\n'
    caminho.write_text(texto, encoding='utf-8', newline='\n')
    total = sum(len(c['verificar']) for c in conteudo['casos'])
    print(f'{caminho.name}: {total} verificações')


def main():
    modelo, funcao = [], []
    for nome, ano, mes in PERIODOS:
        av, aa = soma(ano, mes), soma(ano - 1, mes)
        delta, pct, farol = regra(av, aa)
        onde = filtro(ano, mes)
        modelo.append({'nome': nome, 'verificar': [
            verificacao(f'[Faturado ({s})]', onde, e)
            for s, e in zip(['AV', 'AA', 'Δ', 'Δ%', 'Δi'], [av, aa, delta, pct, farol])]})
        funcao.append({'nome': nome, 'verificar': [
            verificacao(f"Tempo.{u} ( [Faturado (AV)], 'Gregoriano' )", onde, e)
            for u, e in [('AnoAnterior', aa), ('VariacaoAnoAnterior', pct)]]})

    # 29/02: o clássico volta para 28/02; o calendário, para 01/03 (60º dia)
    modelo.append({'nome': '29/02 no modo clássico', 'verificar': [
        verificacao('[Faturado (AV)]', DIA, 29),
        verificacao('[Faturado (AA)]', DIA, 7)]})
    funcao.append({'nome': '29/02 no modo calendário', 'verificar': [
        verificacao("Tempo.AnoAnterior ( [Faturado (AV)], 'Gregoriano' )", DIA, 11)]})

    gravar('casos-modelo-sintetico.json', {'casos': modelo})
    gravar('casos-udf-ano-anterior.json', {'funcoes': udfs(), 'casos': funcao})


if __name__ == '__main__':
    main()
