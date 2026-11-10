"""شعار النادي لكل جامعة: Tuwaiq CLUB + سطر "Supported by Tuwaiq Academy | <اختصار الجامعة>".
يبني لكل جامعة 3 نسخ (ملون، أبيض، أسود) SVG وPNG في assets/logos/club/universities/<slug>/
المقاسات مأخوذة من شعار نادي الإمام الرسمي (IMSIU): نفس حجم الخط والمسافات ولون الفاصل.

usage: python3 scripts/build_club_lockups.py            # كل الجامعات
       python3 scripts/build_club_lockups.py imam ksu   # جامعات محددة
لتعديل اختصار: عدّل القاموس ABBR تحت وأعد التشغيل."""
import re, subprocess, io, json, sys, os
import numpy as np
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = f'{PKG}/assets/logos/club'
font = TTFont(f'{PKG}/assets/fonts/ttf/IBMPlexSansArabic-Regular.ttf'); gs = font.getGlyphSet(); cmap = font.getBestCmap()
hmtx = font['hmtx']; UPM = 1000
def text_adv(s):
    return sum(hmtx[cmap[ord(c)]][0] for c in s)
def ink_bounds(s):
    x = 0; xmin = xmax = None
    for c in s:
        g = cmap[ord(c)]; bp = BoundsPen(gs); gs[g].draw(bp)
        if bp.bounds:
            a, b = x + bp.bounds[0], x + bp.bounds[2]
            xmin = a if xmin is None else min(xmin, a); xmax = b if xmax is None else max(xmax, b)
        x += hmtx[g][0]
    return xmin, xmax
def text_path(s, x0, base, size):
    sc = size / UPM; pen = SVGPathPen(gs, ntos=lambda v: ('%.2f' % v).rstrip('0').rstrip('.')); x = 0
    for c in s:
        g = cmap[ord(c)]
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x0 + x * sc, base)))
        x += hmtx[g][0]
    return pen.getCommands()
# --- base logo (no tagline) : ink bbox in its user units
src = open(f'{LOGO}/tuwaiq-club-color-no-tagline.svg').read()
vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', src).group(1).split()]
K = 10
arr = np.array(Image.open(io.BytesIO(subprocess.run(['rsvg-convert', '-w', str(int(vb[2]*K)), f'{LOGO}/tuwaiq-club-color-no-tagline.svg'], capture_output=True, check=True).stdout)))
rgb = arr[..., :3].astype(int)
colored = (arr[..., 3] > 20) & ((rgb.max(-1) - rgb.min(-1)) > 40)   # brand colours only, not the grey tagline
ys, xs = np.where(colored)
lx0, lx1, ly0, ly1 = vb[0] + xs.min()/K, vb[0] + (xs.max()+1)/K, vb[1] + ys.min()/K, vb[1] + (ys.max()+1)/K
W = lx1 - lx0
# --- reference measurements (from the IMSIU lockup, px): logo width 2544
R = W / 2544
lead = 'Supported by Tuwaiq Academy'
a0, a1 = ink_bounds(lead)
size = (2590 - 536) * R / ((a1 - a0) / UPM)          # calibrate from lead width
cap_top = ly1 + (2114 - 1898) * R
capH = 712 * size / UPM                                # S with overshoot
base = cap_top + capH
gap1, gap2 = (2638 - 2590) * R, (2694 - 2643) * R
divw = 6 * R; div_y0, div_y1 = cap_top - 2*R, cap_top + (2245 - 2114) * R
def lockup(abbr, mode):
    col = {'color': ('#606060', '#4F29B7'), 'white': ('#FFFFFF', '#FFFFFF'), 'black': ('#000000', '#000000')}[mode]
    base_svg = {'color': 'tuwaiq-club-color-no-tagline.svg', 'white': 'tuwaiq-club-white-no-tagline.svg', 'black': 'tuwaiq-club-color-no-tagline.svg'}[mode]
    body = open(f'{LOGO}/{base_svg}').read()
    body = re.sub(r'^\s*<\?xml[^>]*\?>', '', body).strip()
    if mode == 'black':
        body = re.sub(r'fill="rgb\([^"]*\)"', 'fill="#000000"', body)
    inner = re.sub(r'<svg\b[^>]*>', '', body, count=1).rsplit('</svg>', 1)[0]
    # drop the old centred tagline (glyph defs + uses + grey rules) and shorten numbers
    inner = re.sub(r'<defs>.*?</defs>', '', inner, flags=re.S)
    inner = re.sub(r'<use\b[^>]*/>|<use\b.*?</use>', '', inner, flags=re.S)
    inner = re.sub(r'<path\b[^>]*rgb\(47\.79[^>]*/>', '', inner)
    inner = re.sub(r'<g\b[^>]*>\s*</g>', '', inner)
    inner = re.sub(r'(\d+\.\d{2})\d+', r'\1', inner)
    inner = (f'<clipPath id="tc-clip-{abbr}"><rect x="{lx0-5:.2f}" y="{ly0-5:.2f}" width="{W+10:.2f}" height="{ly1-ly0+5.5:.2f}"/></clipPath>'
             f'<g clip-path="url(#tc-clip-{abbr})">{inner}</g>')
    # line metrics; shrink to logo width if needed
    s = size; x = lx0 - (a0 / UPM) * s
    lead_end = x + (a1 / UPM) * s
    b0, b1 = ink_bounds(abbr)
    def total(s):
        sc = s / size
        return (a1 - a0) / UPM * s + (gap1 + divw + gap2) * sc + (b1 - b0) / UPM * s
    maxw = W * 1.0075
    if total(s) > maxw:
        s = s * maxw / total(s)
    sc = s / size
    x = lx0 - (a0 / UPM) * s; lead_end = x + (a1 / UPM) * s
    dx = lead_end + gap1 * sc
    ax = dx + divw * sc + gap2 * sc - (b0 / UPM) * s
    bl = cap_top + 712 * s / UPM
    d1 = text_path(lead, x, bl, s); d2 = text_path(abbr, ax, bl, s)
    dy0, dy1 = cap_top - 2*R*sc, cap_top + (2245 - 2114) * R * sc
    right = max(lx1, ax + (b1 / UPM) * s)
    pad = 0
    bottom = max(dy1, bl + 230 * s / UPM)
    nvb = f'{lx0:.2f} {ly0:.2f} {right-lx0:.2f} {bottom-ly0:.2f}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="{nvb}">'
            f'<title>Tuwaiq Club | {abbr}</title>{inner}'
            f'<path fill="{col[0]}" d="{d1}"/><rect fill="{col[1]}" x="{dx:.2f}" y="{dy0:.2f}" width="{divw*sc:.2f}" height="{dy1-dy0:.2f}"/>'
            f'<path fill="{col[0]}" d="{d2}"/></svg>\n')
# اختصار كل جامعة كما يظهر في سطر الشعار (اعتمد الاختصار الرسمي للنادي إن وجد)
ABBR = {
    'baha': 'BU', 'hail': 'UOH', 'iau': 'IAU', 'imam': 'IMSIU', 'jazan': 'JU', 'jeddah': 'UJ',
    'kau': 'KAU', 'kfu': 'KFU', 'kfupm': 'KFUPM', 'kku': 'KKU', 'ksu': 'KSU', 'najran': 'NU',
    'nbu': 'NBU', 'pnu': 'PNU', 'psau': 'PSAU', 'qassim': 'QU', 'taibah': 'TaibahU', 'taif': 'TU',
    'upm': 'UPM', 'uqu': 'UQU', 'tabuk': 'UT',
}
if __name__ == '__main__':
    only = sys.argv[1:]
    base = f'{PKG}/assets/logos/club/universities'; meta = []
    for slug, abbr in ABBR.items():
        meta.append({'slug': slug, 'abbr': abbr, 'files': [f'{slug}/tuwaiq-club-{slug}-{m}.{e}' for m in ('color', 'white', 'black') for e in ('svg', 'png')]})
        if only and slug not in only: continue
        d = f'{base}/{slug}'; os.makedirs(d, exist_ok=True)
        for m in ('color', 'white', 'black'):
            f = f'{d}/tuwaiq-club-{slug}-{m}.svg'
            open(f, 'w').write(lockup(abbr, m))
            subprocess.run(['rsvg-convert', '-w', '2000', '-o', f[:-4] + '.png', f], check=True)
        print('club lockup', slug, abbr)
    json.dump(meta, open(f'{base}/club-lockups.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
