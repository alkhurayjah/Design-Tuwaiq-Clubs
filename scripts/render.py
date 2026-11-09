"""Render templates in templates/html to PNG through a local http server
(CSS masks used for recolourable icons do not load over file://).
usage: python3 scripts/render.py [scale] [name ...]
       scale 1 = preview (default), 2 = export.   Output: templates/previews/<name>.png
To edit a template live:  cd <package root> && python3 -m http.server 8000  ->  http://localhost:8000/templates/html/<name>.html"""
import sys, glob, os, threading, functools, http.server, socketserver
from playwright.sync_api import sync_playwright
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scale = float(sys.argv[1]) if len(sys.argv) > 1 else 1
only = sys.argv[2:]
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
H = functools.partial(Q, directory=root)
srv = socketserver.TCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in sorted(glob.glob(os.path.join(root, 'templates/html/*.html'))):
        name = os.path.basename(f)[:-5]
        if only and name not in only: continue
        pg = b.new_page(viewport={'width': 2000, 'height': 2000}, device_scale_factor=scale)
        pg.goto(f'http://127.0.0.1:{port}/templates/html/{name}.html'); pg.wait_for_load_state('networkidle')
        pg.evaluate('document.fonts.ready')
        w, h = pg.evaluate('(()=>{const r=document.querySelector(".post").getBoundingClientRect();return [Math.ceil(r.right)+10, Math.ceil(r.bottom)+10]})()')
        pg.set_viewport_size({'width': max(w, 400), 'height': max(h, 400)}); pg.wait_for_timeout(300)
        pg.query_selector('.post').screenshot(path=os.path.join(root, 'templates/previews', name + '.png'))
        print('rendered', name)
srv.shutdown()
