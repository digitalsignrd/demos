# Probador de juegos · Digital Sign RD

Sitio estático publicado en GitHub Pages en **https://demo.digitalsignrd.com**.

- `index.html` — portada con las demos (se genera, no editar a mano)
- `<slug>/index.html` — visor con marco de tótem para cada cliente (se genera)
- `juegos/<slug>/index.html` — el juego en sí (versión demo, sin envío a Google Sheets)
- `demos.json` — lista de demos (cliente, título, clave de acceso, etc.)
- `_src/` — plantillas del visor y la portada
- `build.py` — genera todo lo anterior

## Agregar un juego nuevo
1. Copiar el HTML del juego (versión demo) en `juegos/<slug>/index.html`
2. Agregar la entrada en `demos.json`
3. `python3 build.py`
4. `git add -A && git commit -m "Nueva demo" && git push`
