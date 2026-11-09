"""يولّد صورة docs/pixels-and-icons.png (كل أشكال البكسل + الأيقونات) لصفحة README.
usage: python3 scripts/build_docs_images.py"""
import os, json
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
px = json.load(open(f"{ROOT}/assets/pixels/pixels.json", encoding="utf-8"))
ic = json.load(open(f"{ROOT}/assets/icons/academy/icons.json", encoding="utf-8"))
cols = ["#9C75FF", "#57E3D8", "#F4A664", "#CDB7FF", "#FFFFFF"]
cells = "".join(
    f'<figure><svg viewBox="-8 -8 {v["w"]+16} {v["h"]+16}" style="height:{min(62, 15.5*v["h"]/100+16)}px"><path fill="{cols[i % 5]}" d="{v["d"]}"/></svg><figcaption>{k}</figcaption></figure>'
    for i, (k, v) in enumerate(px.items()))
icons = "".join(f'<figure><img src="file://{ROOT}/assets/icons/academy/white/{k}.svg"><figcaption>{k}</figcaption></figure>' for k in ic)
html = f'''<html><body style="margin:0"><div id="c" style="width:1200px;background:#4F29B7;padding:26px 24px 20px;box-sizing:border-box;font:13px system-ui,sans-serif;color:#E6DEFF">
<style>.g{{display:flex;flex-wrap:wrap;gap:16px 22px;align-items:flex-end}} figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:6px}}
figcaption{{font-size:12px;color:#E6DEFF}} img{{height:58px}} h3{{margin:0 0 14px;font-size:14px;color:#CDB7FF;font-weight:600}}</style>
<h3 dir="rtl" style="text-align:left">أشكال البكسل ({len(px)})</h3><div class="g">{cells}</div>
<h3 style="margin-top:26px">الأيقونات ({len(ic)})</h3><div class="g">{icons}</div></div></body></html>'''
tmp = f"{ROOT}/docs/_px.html"; open(tmp, "w").write(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 800}, device_scale_factor=1)
    pg.goto("file://" + tmp); pg.query_selector("#c").screenshot(path=f"{ROOT}/docs/pixels-and-icons.png"); b.close()
os.remove(tmp); print("docs/pixels-and-icons.png", len(px), "shapes +", len(ic), "icons")
