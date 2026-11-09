"""فحص الحزمة قبل أي تحديث أو رفع.
Package health check: run before every update / commit.

usage:  python3 scripts/check.py            # كل الفحوصات
        python3 scripts/check.py --fast     # بدون فتح المتصفح (المسارات والملفات فقط)

Checks
  1. القوالب HTML: كل مسار src/href/url() موجود (فحص ثابت).
  2. القوالب HTML في المتصفح: لا طلبات فاشلة (404)، ولا أخطاء JS، والعنصر .post موجود
     بمقاسه المتوقع (من اسم الملف)، وخط IBM Plex Sans Arabic محمّل فعلًا، ولا صور مكسورة.
  3. الشعارات: كل جامعة وكل شريك في الـ json لها -color و-white و-black (SVG أو PNG)،
     وكل ملف SVG صالح وفيه viewBox.
  4. الوثائق: المسارات والروابط في README.md وBRAND_GUIDE.md والمهارات والبرومت موجودة.
  5. قوالب PowerPoint تفتح بدون أخطاء.
  6. الحزمة: لا ملفات .DS_Store، ولا ملف أكبر من 50MB، ولا ملف فارغ.

Exit code 0 = كل شيء سليم، 1 = فيه أخطاء (تُطبع في النهاية).
"""
import sys, os, re, glob, json, threading, functools, http.server, socketserver
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAST = '--fast' in sys.argv
errors, warns = [], []
def err(sec, msg): errors.append(f'[{sec}] {msg}')
def warn(sec, msg): warns.append(f'[{sec}] {msg}')
def rel(p): return os.path.relpath(p, ROOT)
def ok(sec, n, what): print(f'  ✓ {sec}: {n} {what}')

TEMPLATES = sorted(glob.glob(os.path.join(ROOT, 'templates/html/*.html')))

# 1. static paths in templates -------------------------------------------------
REF = re.compile(r'''(?:src|href)\s*=\s*["']([^"'#?]+)|url\(\s*["']?([^"')#?]+)''')
def local_refs(text):
    text = re.sub(r'/\*.*?\*/|<!--.*?-->', '', text, flags=re.S)   # ignore comments
    for a, b in REF.findall(text):
        u = (a or b).strip()
        if not u or re.match(r'^(https?:|data:|mailto:|javascript:|//|\{)', u): continue
        yield u
print('1) مسارات القوالب')
n = 0
for f in TEMPLATES + [os.path.join(ROOT, 'templates/html/_base.css'), os.path.join(ROOT, 'brand/tokens.css')]:
    if not os.path.exists(f): err('paths', f'missing {rel(f)}'); continue
    for u in local_refs(open(f, encoding='utf-8').read()):
        n += 1
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), u))):
            err('paths', f'{rel(f)} → {u} غير موجود')
ok('paths', n, 'مسار في القوالب')

# 3. logos ----------------------------------------------------------------------
print('3) الشعارات')
def check_set(base, items, label):
    for it in items:
        s = it['slug']
        for kind in ('color', 'white', 'black'):
            stem = os.path.join(ROOT, base, s, f'{s}-{kind}')
            if not (os.path.exists(stem + '.svg') or os.path.exists(stem + '.png')):
                err('logos', f'{label} {s}: نسخة {kind} ناقصة')
    ok('logos', len(items), label)
for base, js, label in [('assets/logos/universities', 'universities.json', 'جامعة'),
                        ('assets/logos/partners', 'partners.json', 'شريك')]:
    p = os.path.join(ROOT, base, js)
    try: check_set(base, json.load(open(p, encoding='utf-8')), label)
    except Exception as e: err('logos', f'{rel(p)}: {e}')
p = os.path.join(ROOT, 'assets/logos/club/universities/club-lockups.json')
try:
    L = json.load(open(p, encoding='utf-8'))
    for it in L:
        for f in it['files']:
            if not os.path.exists(os.path.join(ROOT, 'assets/logos/club/universities', f)): err('logos', f'شعار النادي {it["slug"]}: {f} ناقص')
    ok('logos', len(L), 'شعار نادي لكل جامعة')
except Exception as e: err('logos', f'{rel(p)}: {e}')
svgs = glob.glob(os.path.join(ROOT, 'assets/**/*.svg'), recursive=True)
for f in svgs:
    try:
        r = ET.parse(f).getroot()
        if 'viewBox' not in r.attrib and not ('width' in r.attrib and 'height' in r.attrib):
            err('svg', f'{rel(f)}: بدون viewBox ولا width/height')
        elif 'viewBox' not in r.attrib:
            warn('svg', f'{rel(f)}: بدون viewBox (قد لا يتمدد صح)')
    except ET.ParseError as e:
        err('svg', f'{rel(f)}: SVG غير صالح ({e})')
ok('svg', len(svgs), 'ملف SVG')

# 4. docs -----------------------------------------------------------------------
print('4) الوثائق')
DOCS = [os.path.join(ROOT, x) for x in ['README.md', 'brand/BRAND_GUIDE.md', 'prompts/SYSTEM_PROMPT.md']] \
     + glob.glob(os.path.join(ROOT, 'skills/*/SKILL.md'))
PATH_RE = re.compile(r'`((?:assets|templates|scripts|brand|skills|prompts|references|docs)/[^`\s*<>{}…]+)`'
                     r'|\]\(((?!https?:)[^)\s#]+)\)|<img src="((?!https?:)[^"]+)"')
n = 0
for d in DOCS:
    if not os.path.exists(d): err('docs', f'missing {rel(d)}'); continue
    for m in PATH_RE.finditer(open(d, encoding='utf-8').read()):
        u = next(x for x in m.groups() if x).rstrip('.,،:)')
        if '[' in u or '<' in u: continue          # placeholders
        n += 1
        cands = [os.path.join(ROOT, u), os.path.join(os.path.dirname(d), u),
                 os.path.join(ROOT, 'templates/html', u)]
        if not any(os.path.exists(c) or glob.glob(c) for c in cands):
            err('docs', f'{rel(d)} → {u} غير موجود')
ok('docs', n, 'مسار في الوثائق')

# 5. pptx -----------------------------------------------------------------------
print('5) قوالب PowerPoint')
try:
    from pptx import Presentation
    pp = glob.glob(os.path.join(ROOT, 'templates/pptx/*.pptx'))
    for f in pp:
        try:
            if len(Presentation(f).slides) == 0: err('pptx', f'{rel(f)}: بدون شرائح')
        except Exception as e: err('pptx', f'{rel(f)}: {e}')
    ok('pptx', len(pp), 'ملف')
except ImportError:
    warn('pptx', 'python-pptx غير مثبّت، تم التخطي')

# 6. package hygiene ------------------------------------------------------------
print('6) نظافة الحزمة')
n = 0
for dp, dn, fn in os.walk(ROOT):
    if '.git' in dp.split(os.sep): continue
    for x in fn:
        p = os.path.join(dp, x); n += 1
        if x == '.DS_Store': err('pkg', f'{rel(p)}: ملف ماك، احذفه')
        sz = os.path.getsize(p)
        if sz == 0 and x not in ('.gitkeep', '.nojekyll'): warn('pkg', f'{rel(p)}: ملف فارغ')
        if sz > 50 * 2**20: err('pkg', f'{rel(p)}: أكبر من 50MB (يحتاج Git LFS)')
        elif sz > 25 * 2**20: warn('pkg', f'{rel(p)}: أكبر من 25MB (ارفعه بـ Git لا بالمتصفح)')
ok('pkg', n, 'ملف')

# 2. browser render -------------------------------------------------------------
if not FAST:
    print('2) فتح القوالب في المتصفح')
    from playwright.sync_api import sync_playwright
    class Q(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=ROOT))
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with sync_playwright() as p:
        b = p.chromium.launch()
        for f in TEMPLATES:
            name = os.path.basename(f)[:-5]; sec = f'render {name}'
            pg = b.new_page(viewport={'width': 2400, 'height': 2600})
            bad = []
            pg.on('response', lambda r: r.status >= 400 and bad.append(f'{r.status} {r.url.split(str(port))[-1]}'))
            pg.on('requestfailed', lambda r: bad.append(f'failed {r.url.split(str(port))[-1]}'))
            pg.on('pageerror', lambda e: bad.append(f'JS: {e}'))
            pg.goto(f'http://127.0.0.1:{port}/templates/html/{name}.html'); pg.wait_for_load_state('networkidle')
            pg.evaluate('document.fonts.ready')
            r = pg.evaluate('''(()=>{const p=document.querySelector(".post");if(!p)return null;
              const b=p.getBoundingClientRect();
              const broken=[...document.images].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.getAttribute("src"));
              const font=document.fonts.check('700 40px "IBM Plex Sans Arabic"', "طويق")&&
                [...document.fonts].some(f=>/IBM Plex Sans Arabic/i.test(f.family)&&f.status==="loaded");
              const over=[...p.querySelectorAll("h1,h2,h3,p,.title")].filter(e=>e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflow!=="visible").length;
              return {w:Math.round(b.width),h:Math.round(b.height),broken,font,over}})()''')
            for x in bad: err(sec, x)
            if r is None: err(sec, 'لا يوجد عنصر .post'); pg.close(); continue
            for s in r['broken']: err(sec, f'صورة مكسورة: {s}')
            if not r['font']: err(sec, 'خط IBM Plex Sans Arabic لم يُحمّل')
            m = re.search(r'(\d{3,4})x(\d{3,4})$', name)
            if m and (abs(r['w'] - int(m[1])) > 2 or abs(r['h'] - int(m[2])) > 2):
                err(sec, f'المقاس {r["w"]}×{r["h"]} والمتوقع {m[1]}×{m[2]}')
            elif not m and (r['w'] < 300 or r['h'] < 300):
                err(sec, f'مقاس غير منطقي {r["w"]}×{r["h"]}')
            print(f'  {"✗" if any(e.startswith(f"[{sec}]") for e in errors) else "✓"} {name} ({r["w"]}×{r["h"]})')
            pg.close()
        b.close()
    srv.shutdown()

# report ------------------------------------------------------------------------
print()
for w in warns: print('  ! ' + w)
if errors:
    print(f'\n✗ {len(errors)} خطأ:')
    for e in errors: print('  ✗ ' + e)
    sys.exit(1)
print(f'✓ الحزمة سليمة ({len(warns)} تنبيه)')
