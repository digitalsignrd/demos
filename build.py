#!/usr/bin/env python3
"""
Genera el sitio del Probador de juegos a partir de demos.json.

CÓMO AGREGAR UN JUEGO NUEVO:
  1. Copia el HTML del juego (versión demo, sin URL de Google Sheets) en  juegos/<slug>/index.html
  2. Agrega una entrada en demos.json (slug, cliente, titulo, evento, descripcion, clave opcional, color)
  3. Ejecuta:  python3 build.py
  4. git add -A && git commit -m "Nueva demo <cliente>" && git push
  GitHub Pages publica los cambios en 1-2 minutos.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
demos = json.load(open(os.path.join(ROOT, 'demos.json'), encoding='utf-8'))
viewer_tpl = open(os.path.join(ROOT, '_src/viewer.html'), encoding='utf-8').read()
index_tpl = open(os.path.join(ROOT, '_src/index.html'), encoding='utf-8').read()

GUARD = """<script>(function(){try{var c=%s;if(c&&localStorage.getItem('demo_%s')!=='1'&&location.search.indexOf('kiosk')<0){location.replace('../../%s/');}}catch(e){}})();</script>"""

cards = []
for d in demos:
    slug = d['slug']
    assert re.fullmatch(r'[a-z0-9-]+', slug), 'slug inválido: ' + slug
    game_path = os.path.join(ROOT, 'juegos', slug, 'index.html')
    assert os.path.exists(game_path), 'falta ' + game_path
    vals = {
        'SLUG': slug, 'CLIENTE': d['cliente'], 'TITULO': d['titulo'], 'EVENTO': d.get('evento', ''),
        'DESCRIPCION': d.get('descripcion', ''), 'CLAVE': d.get('clave', ''), 'COLOR': d.get('color', '#85BB66'),
    }
    page = viewer_tpl
    for k, v in vals.items():
        page = page.replace('{{' + k + '}}', html.escape(v, quote=True) if k != 'CLAVE' else json.dumps(v)[1:-1])
    os.makedirs(os.path.join(ROOT, slug), exist_ok=True)
    open(os.path.join(ROOT, slug, 'index.html'), 'w', encoding='utf-8').write(page)

    # Guard en el juego: si la demo tiene clave, exige haber entrado por el visor
    g = open(game_path, encoding='utf-8').read()
    g = re.sub(r'<script>\(function\(\)\{try\{var c=.*?\}\)\(\);</script>\n?', '', g, count=1, flags=re.S)
    guard = GUARD % (json.dumps(d.get('clave', '')), slug, slug)
    g = g.replace('<head>', '<head>\n' + guard, 1)
    open(game_path, 'w', encoding='utf-8').write(g)

    cards.append(f"""  <a class="item" href="{slug}/" style="--c:{html.escape(vals['COLOR'])}">
    <div>
      <div class="c"><i></i>{html.escape(d['cliente'])}{' · 🔒' if d.get('clave') else ''}</div>
      <h2>{html.escape(d['titulo'])}</h2>
      <div class="ev">{html.escape(d.get('evento',''))}</div>
    </div>
    <span class="go">Ver demo</span>
  </a>""")

if not cards:
    cards.append('<div class="vacio">Aún no hay demos publicadas.</div>')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(index_tpl.replace('{{CARDS}}', '\n'.join(cards)))
open(os.path.join(ROOT, '.nojekyll'), 'w').close()
print('OK:', len(demos), 'demo(s) generadas')
