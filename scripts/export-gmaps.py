#!/usr/bin/env python3
"""export-gmaps.py — gera um CSV de POIs pra importar no Google My Maps.

Lê um data.json de viagem e emite um CSV com TODOS os pontos (atrações + comida +
paradas de walking tour), categorizados e com nota de recompensa (⭐). O Google My
Maps geocodifica a coluna 'Endereço' na importação — então não precisamos de coord
pra cada ponto (onde já temos coord, a coluna 'Endereço' leva a própria lat,lng,
que o Google resolve exata; onde não, leva nome+região).

Uso:
    python3 scripts/export-gmaps.py <viagem>/data.json <saida>.csv

No My Maps: Criar mapa → Importar → escolher este CSV → posicionar por 'Endereço'
→ agrupar/estilizar por 'Categoria' (ou 'Estrelas').
"""
import json, csv, sys, re
from pathlib import Path

CAT = {
    'atracao':   '🎯 Atração',
    'restaurante':'🍽️ Restaurante',
    'cafe':      '☕ Café',
    'padaria':   '🥐 Padaria/Doceria',
    'loja':      '🛍️ Loja/Design',
    'bar':       '🍸 Bar',
    'parque':    '🌳 Parque',
    'mercado':   '🛒 Mercado',
    'food-hall': '🍴 Food Hall',
}
STARS = {3: '⭐⭐⭐ Vale a viagem', 2: '⭐⭐ Vale o desvio', 1: '⭐ Se sobrar', 0: '⏭️ Pula sem culpa'}


def clean_name(nome):
    """Nome geocodável: tira parênteses (mantém conteúdo), corta descrição após '·'."""
    n = re.sub(r'[()]', ' ', nome or '')
    n = n.split('·')[0]
    return re.sub(r'\s+', ' ', n).strip()


def build_rows(data):
    region = data.get('maps_region', '').strip()
    days = data.get('days', [])
    rows, seen = [], set()

    def add(nome, poicat, vale, coord, dia, notas):
        key = clean_name(nome).lower()
        if key in seen:
            return
        seen.add(key)
        if coord and 'lat' in coord and 'lng' in coord:
            endereco = f"{coord['lat']}, {coord['lng']}"   # Google resolve a coord exata
            lat, lng = coord['lat'], coord['lng']
        else:
            endereco = clean_name(nome) + (', ' + region if region else '')
            lat = lng = ''
        rows.append({
            'Nome': nome,
            'Categoria': CAT.get(poicat, poicat or ''),
            'Estrelas': STARS.get(vale, ''),
            'Dia': dia,
            'Endereço': endereco,
            'Latitude': lat,
            'Longitude': lng,
            'Notas': notas or '',
        })

    for day in days:
        dia = day.get('date', '')
        for s in day.get('stops', []):
            if s.get('tipo') == 'transit':
                continue
            if s.get('tipo') == 'card':
                nota = re.sub('<[^>]+>', '', s.get('imperdivel', '') or s.get('cat', ''))
                add(s['nome'], s.get('poiCat'), s.get('valeAPena'), s.get('coord'), dia, nota)
                for tour in s.get('walkingTours', []):
                    for st in tour.get('stops', []):
                        add(st['nome'], 'atracao', None, st.get('coord'), dia, 'Parada do walking tour: ' + tour.get('nome', ''))
            elif s.get('tipo') == 'opcoes':
                for o in s.get('opcoes', []):
                    add(o['nome'], o.get('poiCat'), o.get('valeAPena'), o.get('coord'), dia,
                        re.sub('<[^>]+>', '', o.get('desc', '')))
    for e in data.get('extras', []):
        add(e['nome'], e.get('poiCat'), e.get('valeAPena'), e.get('coord'), '💡 Dica',
            re.sub('<[^>]+>', '', e.get('cat', '')))
    return rows


def main():
    if len(sys.argv) < 3:
        print("Uso: python3 scripts/export-gmaps.py <viagem>/data.json <saida>.csv", file=sys.stderr)
        sys.exit(2)
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    rows = build_rows(data)
    cols = ['Nome', 'Categoria', 'Estrelas', 'Dia', 'Endereço', 'Latitude', 'Longitude', 'Notas']
    with open(sys.argv[2], 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    ncoord = sum(1 for r in rows if r['Latitude'] != '')
    print(f"✓ {len(rows)} POIs → {sys.argv[2]} ({ncoord} com coord exata, {len(rows)-ncoord} p/ geocodar por nome)")


if __name__ == '__main__':
    main()
