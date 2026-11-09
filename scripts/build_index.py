"""Generate index.html — the visual brand & tools overview for designers.
usage: python3 scripts/build_index.py      (run again whenever assets/templates change)
Opens offline by double-click; every item shows its file path."""
import os, glob, json, html

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)
E = html.escape


def files(pattern):
    return sorted(glob.glob(pattern))


DATA = {}  # path -> embedded data so "copy image" works offline from file://
import base64, re as _re


def reg(path, svg_text=None):
    """Embed a file for clipboard copy. SVG -> text (+size), raster -> data URI."""
    if path in DATA:
        return path
    if svg_text is None and path.endswith(".svg"):
        svg_text = open(path, encoding="utf-8").read()
    if svg_text is not None:
        vb = _re.search(r'viewBox="([^"]+)"', svg_text)
        w, h = (float(x) for x in vb.group(1).split()[2:4]) if vb else (512, 512)
        if 'xmlns="http://www.w3.org/2000/svg"' not in svg_text[:300]:
            svg_text = svg_text.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        DATA[path] = {"t": "svg", "d": svg_text, "w": w, "h": h}
    else:
        mime = "image/jpeg" if path.lower().endswith((".jpg", ".jpeg")) else "image/png"
        raw = open(path, "rb").read()
        if len(raw) > 250_000:  # keep the embedded copy light; the full file stays in the package
            from PIL import Image as _I
            import io as _io
            im = _I.open(_io.BytesIO(raw)); im.thumbnail((1200, 1200))
            buf = _io.BytesIO()
            if mime == "image/png" and im.mode in ("RGBA", "LA", "P"):
                im.save(buf, "PNG", optimize=True)
            else:
                im.convert("RGB").save(buf, "JPEG", quality=82); mime = "image/jpeg"
            raw = buf.getvalue()
        DATA[path] = {"t": "img", "d": f"data:{mime};base64," + base64.b64encode(raw).decode()}
    return path


def bar(path, svg=True, key=None):
    k = E(key or path)
    b = f'<div class="cbar"><button data-png="{k}" title="نسخ كصورة PNG — للصق في PowerPoint وWord وSlides وCanva">نسخ الصورة</button>'
    if svg:
        b += f'<button data-svg="{k}" title="نسخ كود SVG — للصق في Figma وIllustrator كفيكتور">SVG</button>'
    b += f'<button data-txt="{E(path)}" title="نسخ مسار الملف">المسار</button></div>'
    return b


def tile(src, label, bg="#FFFFFF", h=110, cls=""):
    reg(src)
    return (f'<div class="tile {cls}"><a href="{E(src)}" target="_blank" title="فتح الملف">'
            f'<span class="thumb" style="background:{bg}"><img src="{E(src)}" alt="{E(label)}" style="max-height:{h}px" loading="lazy"></span></a>'
            f'<b>{E(label)}</b><code>{E(src)}</code>{bar(src, src.endswith(".svg"))}</div>')


def section(id_, num, title, intro, body):
    return (f'<section id="{id_}"><header class="sh"><span class="num">{num}</span><h2>{E(title)}</h2></header>'
            f'{f"<p class=intro>{intro}</p>" if intro else ""}{body}</section>')


S = []
NAV = []


def add(id_, title, intro, body):
    num = f"{len(S) + 1:02d}"
    NAV.append((id_, num, title)); S.append(section(id_, num, title, intro, body))


# 1 logos -----------------------------------------------------------------
club = [("assets/logos/club/tuwaiq-club-color.svg", "النادي — الأساسي", "#FFFFFF"),
        ("assets/logos/club/tuwaiq-club-white.svg", "النادي — أبيض", "#4F29B7"),
        ("assets/logos/club/tuwaiq-club-color-no-tagline.svg", "النادي — بدون سطر الدعم", "#FFFFFF"),
        ("assets/logos/club/tuwaiq-club-white-no-tagline.svg", "النادي — أبيض بدون سطر الدعم", "#1F0F45"),
        ("assets/logos/club/tuwaiq-club-pixel-mark.svg", "علامة النادي البكسلية", "#FFFFFF")]
acad = []
for v, vn in (("horizontal", "أفقي"), ("vertical", "رأسي")):
    for c, cn, bg in (("color", "ملوّن", "#FFFFFF"), ("white", "أبيض", "#4F29B7"), ("black", "أسود", "#FFFFFF")):
        acad.append((f"assets/logos/academy/tuwaiq-academy-{v}-{c}.svg", f"الأكاديمية — {vn} {cn}", bg))
acad.append(("assets/logos/academy/tuwaiq-academy-mark.svg", "رمز الأكاديمية", "#FFFFFF"))
body = '<h3>نادي طويق</h3><div class="grid g3">' + "".join(tile(s, l, b) for s, l, b in club) + "</div>"
body += '<h3>أكاديمية طويق (ملفات رسمية)</h3><div class="grid g3">' + "".join(tile(s, l, b, 90) for s, l, b in acad) + "</div>"
body += '''<div class="rules"><div class="do"><h4>المعتمد</h4><ul>
<li>الشعار الأفقي هو الأساسي، والرأسي للمساحات الضيقة فقط.</li>
<li>النسخة البيضاء على البنفسجي والداكن، والملوّنة على الأبيض والفاتح.</li>
<li>مساحة فارغة كافية حول الشعار، وحجم يضمن وضوحه.</li>
<li>ملفات PDF الأصلية للطباعة موجودة بجانب ملفات SVG.</li></ul></div>
<div class="dont"><h4>الممنوع</h4><ul>
<li>تدرج لوني، أو تغيير ألوان الشعار، أو إعادة تلوينه.</li>
<li>تغيير تكوين العناصر أو الخط، والمط أو الضغط.</li>
<li>ظلال وتأثيرات، أو خلفية بتباين ضعيف.</li>
<li>تصغير شعار طويق حتى يفقد وضوحه، أو استخدام شعار الجامعة صورة للحساب.</li></ul></div></div>'''
add("logos", "الشعارات", "اضغط أي شعار لفتح ملفه. المسار مكتوب تحت كل عنصر.", body)

# 2 colours ---------------------------------------------------------------
groups = [
    ("الرئيسية — البنفسجي 75% من كل تصميم", [("#4F29B7", "البنفسجي الأساسي"), ("#262626", "الأسود"), ("#EDEDED", "الرمادي الفاتح"), ("#FFFFFF", "الأبيض")]),
    ("الثانوية — 20% للفت الانتباه", [("#57E3D8", "التركواز"), ("#A380FF", "البنفسجي الفاتح"), ("#F4A664", "البرتقالي")]),
    ("ثانوية الأكاديمية — لمسات فقط", [("#4D96FF", "أزرق"), ("#80D883", "أخضر"), ("#FFDB5E", "أصفر"), ("#FF8181", "وردي")]),
    ("تدرجات البنفسجي (لوحة مولّد البكسل)", [("#4F29B7", "p1"), ("#6438DD", "p2"), ("#754BEA", "p3"), ("#9C75FF", "p4"), ("#B798FF", "p5"), ("#CDB7FF", "p6"), ("#E3D8FF", "p7")]),
    ("ألوان البوستات والتقارير", [("#A893FF", "نص تمييز على الداكن"), ("#F08A7A", "أرقام كورال"), ("#F4C38A", "أرقام رملي"), ("#9AEDE6", "تاريخ فعاليات الجامعات"), ("#2FD5CB", "حبة المكان"), ("#8B6CF6", "حبة الوقت"), ("#9C75FF", "عناوين التقارير"), ("#0D0A2E", "كحلي داكن"), ("#1F0F45", "بنفسجي داكن"), ("#F5F1FF", "خلفية فاتحة")]),
]
body = ""
for g, cs in groups:
    body += f"<h3>{E(g)}</h3><div class='swatches'>" + "".join(
        f'<div class="sw"><span style="background:{c}" data-txt="{c}" title="نسخ {c}"></span><b>{E(n)}</b><code>{c}</code>'
        f'<div class="cbar"><button data-txt="{c}">HEX</button><button data-txt="rgb({int(c[1:3],16)}, {int(c[3:5],16)}, {int(c[5:7],16)})">RGB</button>'
        f'<button data-txt="{c[1:]}">بدون #</button></div></div>' for c, n in cs) + "</div>"
body += '<div class="ratio"><span style="flex:75;background:#4F29B7">75% بنفسجي</span><span style="flex:20;background:#57E3D8;color:#262626">20% ثانوية</span><span style="flex:5;background:#262626">5%</span></div>'
body += '<p class="note">اضغط مربع اللون لنسخ كوده، أو اختر الصيغة: HEX، أو RGB، أو بدون #. كل الرموز موجودة في <code>brand/tokens.css</code> و<code>brand/tokens.json</code>. شعار الأكاديمية الرسمي لونه #571CBD، ولا يُعاد تلوينه.</p>'
add("colors", "الألوان", "", body)

# 3 type ------------------------------------------------------------------
body = '''<div class="fontcopy"><b>اسم الخط</b> <code style="font-size:15px">IBM Plex Sans Arabic</code>
<div class="cbar"><button data-txt="IBM Plex Sans Arabic">نسخ اسم الخط</button>
<button data-txt="font-family: 'IBM Plex Sans Arabic', sans-serif;">نسخ CSS</button>
<button data-txt="assets/fonts/">نسخ مسار الملفات</button></div></div>
<div class="type">
<div style="font-weight:700;font-size:56px">العنوان الرئيسي <small>Bold 700</small><span class="cbar in"><button data-txt="IBM Plex Sans Arabic Bold">الاسم + الوزن</button><button data-txt="font-family: \'IBM Plex Sans Arabic\', sans-serif; font-weight: 700;">CSS</button></span></div>
<div style="font-weight:500;font-size:36px;color:#57C9C0">العنوان الفرعي <small>Medium 500</small><span class="cbar in"><button data-txt="IBM Plex Sans Arabic Medium">الاسم + الوزن</button><button data-txt="font-family: \'IBM Plex Sans Arabic\', sans-serif; font-weight: 500;">CSS</button></span></div>
<div style="font-weight:400;font-size:22px">النص الأساسي يكتب هنا بخط عادي واضح ومقروء. <small>Regular 400</small><span class="cbar in"><button data-txt="IBM Plex Sans Arabic Regular">الاسم + الوزن</button><button data-txt="font-family: \'IBM Plex Sans Arabic\', sans-serif; font-weight: 400;">CSS</button></span></div>
<div style="font-weight:300;font-size:40px">وش الفكـــرة اللي تستحق أن تبدأها؟ <small>Light 300 — جمل الحملات</small><span class="cbar in"><button data-txt="IBM Plex Sans Arabic Light">الاسم + الوزن</button><button data-txt="font-family: \'IBM Plex Sans Arabic\', sans-serif; font-weight: 300;">CSS</button></span></div>
<div class="kash"><span>بدون تطويل:</span> فعاليات أندية طويق <span>← بالتطويل:</span> <b>فعاليــات أنديــة طويــق</b></div>
<div style="font-size:30px;font-weight:700" dir="ltr">180,000 · 6,000+ · %82</div></div>
<p class="note">الخط IBM Plex Sans Arabic، وملفاته في <code>assets/fonts/</code> بأوزان 300–700 ورخصة OFL. التطويل (ـ) يوازن أطوال أسطر العناوين، والأرقام لاتينية مع فاصل الآلاف.</p>'''
add("type", "الخط", "", body)

# 4 pixels ----------------------------------------------------------------
px = json.load(open("assets/pixels/pixels.json", encoding="utf-8"))
cols = ["#9C75FF", "#57E3D8", "#F4A664", "#B798FF", "#FFFFFF", "#CDB7FF"]
body = '<div class="dark grid g6">'
for i, (k, v) in enumerate(px.items()):
    svgt = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {v["w"]} {v["h"]}"><path fill="{cols[i % 6]}" d="{v["d"]}"/></svg>'
    key = f"pixel:{k}:{cols[i % 6]}"; reg(key, svgt)
    body += (f'<div class="tile"><a href="assets/pixels/svg/{k}.svg" target="_blank"><span class="thumb" style="background:transparent">'
             f'<svg viewBox="-10 -10 {v["w"] + 20} {v["h"] + 20}" style="max-height:80px;max-width:100%"><path fill="{cols[i % 6]}" d="{v["d"]}"/></svg></span></a>'
             f'<b>{k} <small style="color:#CDB7FF">{cols[i % 6]}</small></b><code>assets/pixels/svg/{k}.svg</code>'
             f'{bar(f"assets/pixels/svg/{k}.svg", True, key)}</div>')
body += tile("assets/pixels/svg/club-mark-3color.svg", "علامة النادي الملوّنة", "transparent", 80) + "</div>"
body += '''<div class="rules"><div class="do"><h4>قواعد مولّد طويق</h4><ul>
<li>شبكة مربعات متساوية، وكل مربع زواياه دائرية بنسبة <b>15% من الضلع</b>.</li>
<li>المربعات المتجاورة أفقيًا أو رأسيًا <b>تندمج</b>، فتختفي الزوايا الداخلية.</li>
<li>المربعات المتلامسة قطريًا بينها <b>جسر مقعّر</b> بنصف قطر الزاوية.</li>
<li>كل شكل بلون واحد: تدرجات البنفسجي أو التركواز.</li></ul></div>
<div class="do"><h4>الملفات والأدوات</h4><ul>
<li><code>assets/pixels/svg/</code>: currentColor، يأخذ لون النص.</li>
<li><code>assets/pixels/palette/&lt;لون&gt;/</code>: 7 ألوان جاهزة.</li>
<li><code>scripts/pixels.py</code>: يولّد أي شكل جديد من رسم نصي (<code>#</code> = مربع).</li>
<li>المولّد الأصلي: <a href="https://genebranding.github.io/Tuwaiq/" target="_blank">genebranding.github.io/Tuwaiq</a></li>
<li>في التصميم: 3–6 مربعات فقط، بلا ازدحام.</li></ul></div></div>'''
add("pixels", "أشكال البكسل", "", body)

# 5 icons -----------------------------------------------------------------
ic = json.load(open("assets/icons/academy/icons.json", encoding="utf-8"))
body = '<div class="dark grid g5">' + "".join(tile(f"assets/icons/academy/white/{k}.svg", f'{v["ar"]} · {k}', "transparent", 64) for k, v in ic.items()) + "</div>"
body += '<div class="grid g5" style="margin-top:14px">' + "".join(tile(f"assets/icons/academy/purple/{k}.svg", f'{v["ar"]} · {k}', "#FFFFFF", 64) for k, v in ic.items()) + "</div>"
body += '<div class="grid g5" style="margin-top:14px">' + tile("assets/icons/social/x.svg", "X", "#FFFFFF", 40) + tile("assets/icons/social/linkedin.svg", "LinkedIn", "#FFFFFF", 40) + "</div>"
body += '<p class="note">كل أيقونة بثلاث نسخ: <code>white/</code>، و<code>purple/</code>، و<code>currentColor/</code> (للتلوين بالـCSS). لا emoji في التصاميم.</p>'
add("icons", "الأيقونات", "", body)

# 6 decorations -----------------------------------------------------------
dec = [("assets/decorations/frame-notch-orange.svg", "إطار الورشة البرتقالي بلسان", "#2E1468"),
       ("assets/decorations/card-tab-corner.svg", "لسان البطاقات", "#FFFFFF"),
       ("assets/decorations/deco-two-squares.svg", "مربعان (المنصة)", "#FFFFFF"),
       ("assets/decorations/deco-pixel-step.svg", "درجة بكسل (المنصة)", "#FFFFFF")]
body = '<div class="grid g4">' + "".join(tile(s, l, b, 100) for s, l, b in dec) + "</div>"
body += '''<h3>الصور داخل العروض والتقارير</h3><div class="imgrule">
<figure class="r"><img src="assets/photos/events/tuwaiq-clubs-awards-ceremony.jpg"><figcaption>زوايا دائرية دائمًا (حوالي 8% من الضلع الأقصر)</figcaption></figure>
<figure class="bd"><span></span><img src="assets/photos/campus/ksu.jpg"><figcaption>عند الحاجة: مربع خلفي دائري الزوايا، مزاح للأسفل واليسار، بلون من الهوية، وبلا ظل</figcaption></figure>
<figure class="no"><img src="assets/photos/campus/najran.jpg"><figcaption>ممنوع: زوايا حادة</figcaption></figure></div>'''
add("decor", "العناصر الزخرفية والصور في العروض", "", body)

# 7 universities ----------------------------------------------------------
import json as _json
_unis = _json.load(open("assets/logos/universities/universities.json", encoding="utf-8"))
def _uni_tiles(kind, bg):
    out = []
    for u in _unis:
        f = f"assets/logos/universities/{u['slug']}/{u['slug']}-{kind}.svg"
        if not os.path.exists(f): f = f[:-4] + ".png"
        out.append(tile(f, u["name_ar"].replace("جامعة ", ""), bg, 80))
    return "".join(out)
body = '<h3>ملونة (للخلفيات الفاتحة)</h3><div class="grid g5">' + _uni_tiles("color", "#FFFFFF") + "</div>"
body += '<h3>بيضاء (للخلفيات الداكنة والبنفسجي)</h3><div class="grid g5">' + _uni_tiles("white", "#4F29B7") + "</div>"
body += '<h3>سوداء (للطباعة الأحادية)</h3><div class="grid g5">' + _uni_tiles("black", "#EDEDED") + "</div>"
body += '<p class="note">20 جامعة، شعارات رسمية حديثة من مواقع الجامعات وأدلة هويتها. لكل جامعة SVG وPNG (2000px) بخلفية شفافة في <code>assets/logos/universities/&lt;slug&gt;/</code>. لا تُعيد تلوين الشعار، استخدم النسخة المناسبة للخلفية.</p>'
add("unis", "شعارات الجامعات", "", body)

# 7b club lockups -------------------------------------------------------------
_locks = _json.load(open("assets/logos/club/universities/club-lockups.json", encoding="utf-8"))
_names = {u["slug"]: u["name_ar"] for u in _unis}
body = '<h3>ملونة</h3><div class="grid g5">' + "".join(tile(f"assets/logos/club/universities/{l['slug']}/tuwaiq-club-{l['slug']}-color.svg", f"{_names.get(l['slug'], l['slug'])} · {l['abbr']}", "#FFFFFF", 90) for l in _locks) + "</div>"
body += '<h3>بيضاء</h3><div class="grid g5">' + "".join(tile(f"assets/logos/club/universities/{l['slug']}/tuwaiq-club-{l['slug']}-white.svg", f"{_names.get(l['slug'], l['slug'])} · {l['abbr']}", "#4F29B7", 90) for l in _locks) + "</div>"
body += '<p class="note">أي تصميم لنادي جامعة محددة: هذا الشعار + شعار الجامعة. التصاميم العامة: الشعار العام. النسخة السوداء في نفس المجلد.</p>'
add("clublocks", "شعار النادي لكل جامعة", "", body)

# 8 partners --------------------------------------------------------------
_parts = _json.load(open("assets/logos/partners/partners.json", encoding="utf-8"))
def _part_tiles(kind, bg):
    return "".join(tile(f"assets/logos/partners/{p['slug']}/{p['slug']}-{kind}.svg", p["name"], bg, 60) for p in _parts)
body = '<h3>ملونة (للخلفيات الفاتحة)</h3><div class="grid g6">' + _part_tiles("color", "#FFFFFF") + "</div>"
body += '<h3>بيضاء (للخلفيات الداكنة والبنفسجي)</h3><div class="grid g6">' + _part_tiles("white", "#4F29B7") + "</div>"
body += '<h3>سوداء (للطباعة الأحادية)</h3><div class="grid g6">' + _part_tiles("black", "#EDEDED") + "</div>"
body += '<p class="note">12 شريكًا، شعارات رسمية من مواقع الشركاء أو Wikimedia Commons، في <code>assets/logos/partners/&lt;slug&gt;/</code> (SVG وPNG). DCL الملون ليموني فاستخدمه على الداكن فقط. Exabeam هو الاسم الحالي لـ LogRhythm بعد الاندماج. تُستخدم فقط في سياق شراكة فعلية ومعتمدة.</p>'
add("partners", "الشركاء", "", body)

# 9 photos ----------------------------------------------------------------
low = {"iau", "jazan"}
ph = ""
for f in files("assets/photos/campus/*.jpg") + files("assets/photos/events/*"):
    n = os.path.basename(f).rsplit(".", 1)[0]
    flag = " · دقة منخفضة" if n in low else (" · فيها علامة مائية، قصّها" if n == "baha" else "")
    reg(f)
    ph += f'<div class="photo"><a href="{f}" target="_blank"><img src="{f}" loading="lazy"></a><b>{E(n)}{flag}</b><code>{E(f)}</code>{bar(f, False)}</div>'
add("photos", "صور الحرم والفعاليات", f"{len(files('assets/photos/campus/*.jpg'))} صورة حرم جامعي، كل صورة باسم الجامعة المختصر (slug) مثل شعارها، وصورة حفل تكريم الأندية. المصادر والرخص في assets/photos/campus/SOURCES.md.", f'<div class="photos">{ph}</div>')

# 10 templates ------------------------------------------------------------
tpl_ar = {"club-workshop-1080": "ورشة / جلسة / لقاء — أندية", "club-weekly-schedule-1080x1560": "جدول فعاليات الأسبوع — أندية",
          "club-launch-story-1080x1920": "إطلاق نادي في جامعة — ستوري", "club-countdown-1080": "حملة عدّ تنازلي — أندية",
          "academy-story-results-1080x1920": "فائزون وأرقام — ستوري أكاديمية", "slide-start-1920x1080": "شريحة البداية بصورة الجامعة"}
body = '<div class="tpls">'
for f in files("templates/previews/*.png"):
    n = os.path.basename(f)[:-4]
    reg(f)
    body += (f'<div class="tpl"><a href="{f}" target="_blank"><img src="{f}" loading="lazy"></a><b>{E(tpl_ar.get(n, n))}</b>'
             f'<code>templates/html/{n}.html</code>{bar(f, False)}</div>')
body += '</div><p class="note">للتعديل: شغّل <code>python3 -m http.server 8000</code> داخل الحزمة، ثم افتح القالب في المتصفح. للتصدير: <code>python3 scripts/render.py 2 &lt;اسم القالب&gt;</code>.</p>'
add("templates", "قوالب البوستات والشرائح", "", body)

# 11 reports --------------------------------------------------------------
def strip(folder, title, cmd, tall=False):
    imgs = "".join(f'<a href="{f}" target="_blank"><img src="{f}" loading="lazy" class="{"tall" if tall else "wide"}"></a>' for f in files(folder + "/*.png"))
    return f'<h3>{E(title)}</h3><div class="strip">{imgs}</div><p class="note"><code>{E(cmd)}</code></p>'
body = strip("templates/previews/presentation", "العرض التقديمي — 16:9، 13 شريحة قابلة للتعديل (templates/pptx/presentation-template.pptx)",
             "افتحه في PowerPoint بعد تثبيت خطوط assets/fonts/ttf — وللتعديل الجذري: bash scripts/presentation/build.sh")
body += strip("templates/previews/weekly", "التقرير الأسبوعي — عمودي 9:16 (غلاف · أرقام · فعالية · مخرجات · الأسبوع القادم · ختام)",
             "python3 scripts/build_weekly_report.py templates/pptx/weekly-report-template.pptx weekly.json out.pptx", True)
body += strip("templates/previews/report", "التقرير الدوري — 16:9 (غلاف · ملخص · جدول · رسم بياني · مستهدفات · إنجازات · تحديات · خطة · صورة · ختام)",
              "python3 scripts/build_club_report.py templates/pptx/club-report-template.pptx report.json out.pptx")
body += '<p class="note">أمثلة JSON في <code>templates/pptx/*-example.json</code>، والتعليمات في <code>skills/tuwaiq-club-reports/SKILL.md</code>.</p>'
add("reports", "العروض والتقارير (PowerPoint)", "", body)

# 12 quick rules ----------------------------------------------------------
body = '''<div class="cards">
<div><h4>أماكن الشعارات — بوستات الأكاديمية</h4><p>الأكاديمية أعلى اليمين، والشريك أعلى اليسار. وفي الأسفل يسارًا: Tuwaiq.edu.sa + TuwaiqAcademy.</p></div>
<div><h4>أماكن الشعارات — بوستات الأندية</h4><p>النادي أعلى اليمين، والأكاديمية أسفل اليمين (والشريك بجانبها)، و@TuwaiqClubs أسفل اليسار، وشعار الجامعة في بوستات الجامعة.</p></div>
<div><h4>إعلان الفعالية — إلزامي</h4><p>العنوان، والتاريخ، والوقت، والمكان، ورابط التسجيل، وشعار نادي طويق، وشعار الجامعة.</p></div>
<div><h4>ألوان حبوب المعلومات (الأندية)</h4><p><span class="chip" style="border-color:#F4A664;color:#C47A35">التاريخ برتقالي</span> <span class="chip" style="border-color:#8B6CF6;color:#6B4BE0">الوقت بنفسجي</span> <span class="chip" style="border-color:#2FD5CB;color:#14968E">المكان تركواز</span></p></div>
<div><h4>النبرة</h4><p><b>معتمد:</b> "سجّل الآن وابدأ رحلتك التقنية معنا"، "يسرّنا دعوتكم…"، "المقاعد محدودة لضمان جودة التجربة".<br><b>ممنوع:</b> "نضمن لك وظيفة"، "أقوى دورة في التاريخ"، "باقي 3 كراسي بسرعة".</p></div>
<div><h4>يُمنع نشر</h4><p>بيانات شخصية للطلاب، ووعود غير رسمية، وشراكات قبل اعتمادها، وصور فردية واضحة بلا موافقة.</p></div>
<div><h4>جدول النشر</h4><p>قبل الفعالية بأسبوع: الإعلان. قبلها بـ48 ساعة: تذكير. بعدها: شكر وتغطية.</p></div>
<div><h4>المحتوى</h4><p>لا أرقام ولا أسماء ولا تواريخ مخترعة، والناقص يبقى [بين قوسين].</p></div></div>'''
add("rules", "قواعد سريعة", "", body)

# 13 tools ----------------------------------------------------------------
rows = [("README.pdf", "التعريف المصوّر بالحزمة وكل ما تقدر تسويه"), ("prompts/SYSTEM_PROMPT.md", "البرومت الرئيسي + برومتات جاهزة لكل نوع"),
        ("brand/BRAND_GUIDE.md", "دليل الهوية الكامل نصيًا"),
        ("skills/tuwaiq-clubs-brand/SKILL.md", "المهارة الأم: سير العمل والقواعد"),
        ("skills/tuwaiq-social-posts/SKILL.md", "بوستات الأكاديمية"),
        ("skills/tuwaiq-club-posts/SKILL.md", "بوستات الأندية"),
        ("skills/tuwaiq-club-reports/SKILL.md", "التقرير الأسبوعي والدوري"),
        ("scripts/render.py", "تصدير قوالب HTML إلى PNG"),
        ("scripts/build_weekly_report.py", "توليد التقرير الأسبوعي (.pptx)"),
        ("scripts/build_club_report.py", "توليد التقرير الدوري (.pptx)"),
        ("scripts/pixels.py", "مولّد أشكال البكسل"),
        ("scripts/trace.py", "تحويل PNG إلى SVG"),
        ("scripts/build_index.py", "إعادة توليد هذه الصفحة"),
        ("scripts/build_readme_pdf.py", "إعادة توليد README.pdf"),
        ("references/", "الملفات الأصلية: الأدلة، والقوالب، و25 بوستًا مرجعيًا")]
body = '<table class="tools"><tr><th>الملف</th><th>الاستخدام</th></tr>' + "".join(
    f'<tr><td><a href="{p}" target="_blank"><code>{p}</code></a></td><td>{E(d)}</td></tr>' for p, d in rows) + "</table>"
add("tools", "الأدوات والمهارات", "", body)

# references gallery
refs = "".join(f'<a href="{f}" target="_blank"><img src="{f}" loading="lazy"></a>' for f in files("references/posts-academy/*.jpg") + files("references/posts-clubs/*.jpg"))
add("refs", "البوستات المرجعية", "25 بوستًا رسميًا للأكاديمية والأندية: المرجع البصري لأي تصميم جديد.", f'<div class="refs">{refs}</div>')

nav = "".join(f'<a href="#{i}"><span>{n}</span>{E(t)}</a>' for i, n, t in NAV)
page = f'''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tuwaiq Clubs — دليل الهوية والأدوات</title>
<meta name="description" content="دليل الهوية والأدوات لأندية طويق وأكاديمية طويق: الشعارات، والألوان، والخط، والبكسل، والأيقونات، والقوالب، مع أزرار نسخ.">
<meta property="og:title" content="Tuwaiq Clubs — دليل الهوية والأدوات"><meta property="og:image" content="docs/index-preview.png"><meta name="theme-color" content="#4F29B7">
<link rel="icon" href="assets/pixels/svg/club-mark-3color.svg" type="image/svg+xml">
<link rel="stylesheet" href="brand/tokens.css">
<style>
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
body{{margin:0;font-family:var(--font);background:#F5F1FF;color:#262626}}
a{{color:inherit}} code{{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#6B5B9A;direction:ltr;unicode-bidi:isolate;word-break:break-all}}
.hero{{background:linear-gradient(180deg,#1F0F45,#4F29B7);color:#fff;padding:48px 56px 40px;position:relative;overflow:hidden}}
.hero .logos{{display:flex;align-items:center;gap:24px}} .hero .logos img{{height:64px}} .hero .logos i{{width:1.5px;height:56px;background:rgba(255,255,255,.5)}}
.hero h1{{font-size:56px;margin:28px 0 8px;color:#57E3D8}} .hero p{{margin:0;font-size:19px;color:#E3D8FF;max-width:820px;line-height:1.7}}
.hero .px{{position:absolute;border-radius:15%}}
.layout{{display:flex;align-items:flex-start;gap:0}}
nav{{position:sticky;top:0;width:250px;flex:none;max-height:100vh;overflow:auto;padding:24px 16px;background:#fff;border-left:1px solid #E3D8FF}}
nav a{{display:flex;gap:10px;align-items:center;padding:8px 10px;border-radius:10px;text-decoration:none;font-size:15px;font-weight:500}}
nav a:hover{{background:#F5F1FF}} nav a span{{font-size:12px;font-weight:700;color:#fff;background:#9C75FF;border-radius:6px;padding:1px 6px}}
main{{flex:1;min-width:0;padding:32px 48px 80px}}
section{{background:#fff;border-radius:20px;padding:32px;margin:0 0 28px;border:1px solid rgba(0,0,0,.05)}}
.sh{{display:flex;align-items:center;gap:14px;margin-bottom:8px}} .sh h2{{margin:0;font-size:32px;color:#4F29B7}}
.num{{background:#4F29B7;color:#fff;font-weight:700;border-radius:8px;padding:2px 10px}}
h3{{font-size:20px;margin:26px 0 12px}} .intro{{color:#585858;margin:0 0 10px}} .note{{color:#585858;font-size:14px;line-height:1.8;margin:16px 0 0}}
.grid{{display:grid;gap:14px}} .g3{{grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}} .g4{{grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}}
.g5{{grid-template-columns:repeat(auto-fill,minmax(170px,1fr))}} .g6{{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}}
.tile{{display:flex;flex-direction:column;gap:6px;text-decoration:none;border:1px solid #EEE9FA;border-radius:14px;padding:10px;background:#fff}}
.tile:hover{{border-color:#9C75FF}}
.thumb{{display:flex;align-items:center;justify-content:center;min-height:130px;border-radius:10px;padding:14px}}
.thumb img{{max-width:100%}} .tile b{{font-size:14px;font-weight:600}}
.dark{{background:#4F29B7;border-radius:16px;padding:16px}} .dark .tile{{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.12);color:#fff}} .dark code{{color:#CDB7FF}}
.rules{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}} .rules>div{{border-radius:14px;padding:16px 20px}}
.do{{background:#F5F1FF}} .dont{{background:#FFF0F0}} .rules h4{{margin:0 0 6px}} .rules ul{{margin:0;padding-right:18px;line-height:1.9;font-size:15px}}
.swatches{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}
.sw{{font:inherit;text-align:right;border:1px solid #EEE9FA;background:#fff;border-radius:14px;padding:8px;cursor:pointer;display:flex;flex-direction:column;gap:4px}}
.sw span{{height:70px;border-radius:10px;border:1px solid rgba(0,0,0,.06)}} .sw b{{font-size:13px}} .sw.ok{{border-color:#39B54A}}
.ratio{{display:flex;height:48px;border-radius:12px;overflow:hidden;margin-top:20px;color:#fff;font-weight:600}} .ratio span{{display:flex;align-items:center;justify-content:center;font-size:13px}}
.type>div{{padding:10px 0;border-bottom:1px solid #F0ECFA}} .type small{{font-size:13px;color:#9C75FF;font-weight:400;margin-right:10px}}
.kash{{font-size:26px}} .kash span{{font-size:14px;color:#888}}
.imgrule{{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;padding:10px 20px 10px 30px}}
.imgrule figure{{margin:0;position:relative}} .imgrule img{{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;position:relative}}
.imgrule .r img,.imgrule .bd img{{border-radius:20px}} .imgrule .bd span{{position:absolute;inset:0;aspect-ratio:4/3;height:auto;border-radius:20px;background:#9C75FF;transform:translate(-14px,14px)}}
.imgrule .no img{{border-radius:0;outline:3px solid #FD8080}} .imgrule figcaption{{font-size:13px;color:#585858;margin-top:22px;line-height:1.6}}
.photos{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}}
.photo{{text-decoration:none;display:flex;flex-direction:column;gap:4px}} .photo img{{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:14px}} .photo b{{font-size:13px}}
.tpls{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px}} .tpl{{display:flex;flex-direction:column;gap:6px}}
.tpl img{{width:100%;height:300px;object-fit:contain;background:#1F0F45;border-radius:14px}} .tpl b{{font-size:14px}}
.strip{{display:flex;gap:12px;overflow-x:auto;padding-bottom:8px}} .strip img{{border-radius:10px;border:1px solid #E3D8FF}} .strip img.tall{{height:420px}} .strip img.wide{{height:220px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}} .cards>div{{background:#F5F1FF;border-radius:14px;padding:16px 20px}}
.cards h4{{margin:0 0 6px;color:#4F29B7}} .cards p{{margin:0;line-height:1.8;font-size:15px}}
.chip{{display:inline-block;border:1.5px solid;border-radius:999px;padding:1px 10px;font-size:13px;margin:2px 0}}
.tools{{width:100%;border-collapse:collapse}} .tools th{{background:#9C75FF;color:#fff;text-align:right;padding:10px}} .tools td{{padding:10px;border-bottom:1px solid #F0ECFA}} .tools code{{font-size:13px}}
.refs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}} .refs img{{width:100%;border-radius:10px;display:block}}
.cbar{{display:flex;flex-wrap:wrap;gap:4px;margin-top:4px}} .cbar.in{{display:inline-flex;margin:0 10px;vertical-align:middle}}
.cbar button{{font:inherit;font-size:11px;font-weight:600;border:1px solid #D9CEF5;background:#F5F1FF;color:#4F29B7;border-radius:999px;padding:3px 10px;cursor:pointer}}
.cbar button:hover{{background:#4F29B7;color:#fff;border-color:#4F29B7}} .cbar button.ok{{background:#39B54A;color:#fff;border-color:#39B54A}}
.dark .cbar button{{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.25);color:#fff}}
.sw{{cursor:default}} .sw span{{cursor:pointer}}
.fontcopy{{display:flex;flex-wrap:wrap;align-items:center;gap:10px;background:#F5F1FF;border-radius:12px;padding:12px 16px;margin-bottom:8px}}
.copyhelp{{background:#F5F1FF;border-radius:12px;padding:10px 16px;font-size:14px;line-height:1.8;margin:0 0 22px}}
.toast{{position:fixed;bottom:20px;left:20px;background:#262626;color:#fff;padding:10px 16px;border-radius:10px;opacity:0;transition:.2s}} .toast.on{{opacity:1}}
@media (max-width:900px){{.layout{{display:block}} nav{{position:static;width:auto;max-height:none;display:flex;flex-wrap:wrap;border:0}}
 main{{padding:16px}} section{{padding:20px}} .hero{{padding:32px 20px}} .hero h1{{font-size:38px}} .rules,.imgrule{{grid-template-columns:1fr}}}}
</style></head><body>
<div class="hero">
 <div class="px" style="left:12%;top:30px;width:22px;height:22px;background:#57E3D8"></div>
 <div class="px" style="left:6%;top:150px;width:34px;height:34px;background:#9C75FF"></div>
 <div class="px" style="left:20%;bottom:30px;width:16px;height:16px;background:#F4A664"></div>
 <div class="logos"><img src="assets/logos/club/tuwaiq-club-white-no-tagline.svg" alt="Tuwaiq Club"><i></i><img src="assets/logos/academy/tuwaiq-academy-horizontal-white.svg" alt="Tuwaiq Academy" style="height:48px"></div>
 <h1>دليل الهوية والأدوات</h1>
 <p>كل ما يحتاجه المصمم لأندية طويق وأكاديمية طويق: الشعارات، والألوان، والخط، والبكسل، والأيقونات، والصور، والقوالب، والتقارير، والقواعد. اضغط أي عنصر لفتح ملفه، ومساره مكتوب تحته.</p>
</div>
<div class="layout"><nav>{nav}</nav><main><p class="copyhelp"><b>النسخ:</b> تحت كل عنصر أزرار. <b>نسخ الصورة</b> ينسخ PNG بخلفية شفافة، الصقه في PowerPoint أو Word أو Google Slides أو Canva. <b>SVG</b> ينسخ الكود كفيكتور، الصقه في Figma أو Illustrator. <b>المسار</b> ينسخ مكان الملف داخل الحزمة. وفي الألوان: HEX وRGB، وفي الخط: الاسم وCSS.</p>{"".join(S)}</main></div>
<div class="toast" id="t">تم النسخ</div>
<script src="docs/index-data.js"></script>
<script>
const D=window.TWQ_DATA||{{}}, T=document.getElementById('t');
function toast(m,ok=true){{T.textContent=m;T.style.background=ok?'#262626':'#C0392B';T.classList.add('on');clearTimeout(T._h);T._h=setTimeout(()=>T.classList.remove('on'),1600)}}
function flash(b){{if(!b)return;b.classList.add('ok');setTimeout(()=>b.classList.remove('ok'),1000)}}
function fallbackText(s){{const a=document.createElement('textarea');a.value=s;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();let r=false;try{{r=document.execCommand('copy')}}catch(e){{}}a.remove();return r}}
async function copyText(s,b){{try{{await navigator.clipboard.writeText(s)}}catch(e){{if(!fallbackText(s)){{toast('تعذّر النسخ',false);return}}}}flash(b);toast('تم النسخ: '+(s.length>40?s.slice(0,40)+'…':s))}}
async function toPNG(key){{
  const e=D[key]; if(!e) throw new Error('no data');
  let src=e.d, url=null;
  if(e.t==='svg'){{url=URL.createObjectURL(new Blob([e.d],{{type:'image/svg+xml'}}));src=url}}
  const img=new Image(); img.src=src; await img.decode();
  let w=e.t==='svg'?e.w:img.naturalWidth, h=e.t==='svg'?e.h:img.naturalHeight;
  const k=e.t==='svg'?Math.min(4,1600/Math.max(w,h))*1:Math.min(1,2400/Math.max(w,h));
  const c=document.createElement('canvas'); c.width=Math.round(w*k); c.height=Math.round(h*k);
  c.getContext('2d').drawImage(img,0,0,c.width,c.height); if(url)URL.revokeObjectURL(url);
  return await new Promise(r=>c.toBlob(r,'image/png'));
}}
async function copyPNG(key,b){{
  try{{
    const blob=toPNG(key);
    await navigator.clipboard.write([new ClipboardItem({{'image/png':blob}})]);
    flash(b);toast('تم نسخ الصورة — الصقها مباشرة');
  }}catch(err){{
    try{{const bl=await toPNG(key);const a=document.createElement('a');a.href=URL.createObjectURL(bl);a.download=(key.includes(':')?key.split(':')[1]:key.split('/').pop().split('.')[0])+'.png';a.click();
      toast('المتصفح منع النسخ — تم تنزيل الصورة PNG بدلًا من ذلك',false)}}catch(e2){{toast('تعذّر نسخ الصورة',false)}}
  }}
}}
// GitHub Pages: open source files (.md/.py/...) and folders on github.com instead of as raw text / 404
(function(){{const h=location.hostname;if(!h.endsWith('github.io'))return;
  const user=h.split('.')[0], seg=location.pathname.split('/').filter(Boolean), repo=(seg[0]&&!seg[0].includes('.'))?seg[0]:user+'.github.io';
  const base='https://github.com/'+user+'/'+repo+'/', br=document.documentElement.dataset.branch||'main';
  document.querySelectorAll('a[href]').forEach(a=>{{const u=a.getAttribute('href');
    if(/^(https?:|#|data:|mailto:|blob:)/.test(u))return;
    if(/\\.(md|py|sh|json|js|css|txt|pptx|pdf\\.json)$/i.test(u)&&!/^docs\\/index-data/.test(u))a.href=base+'blob/'+br+'/'+u;
    else if(u.endsWith('/'))a.href=base+'tree/'+br+'/'+u;}});
}})();
document.addEventListener('click',ev=>{{
  const b=ev.target.closest('[data-png],[data-svg],[data-txt]'); if(!b) return; ev.preventDefault();
  if(b.dataset.png) copyPNG(b.dataset.png,b);
  else if(b.dataset.svg) {{const e=D[b.dataset.svg]; e?copyText(e.d,b):toast('غير متاح',false)}}
  else copyText(b.dataset.txt,b);
}});
</script></body></html>'''
open("index.html", "w", encoding="utf-8").write(page)
os.makedirs("docs", exist_ok=True)
open("docs/index-data.js", "w", encoding="utf-8").write("window.TWQ_DATA=" + json.dumps(DATA, ensure_ascii=False) + ";")
print("docs/index-data.js:", os.path.getsize("docs/index-data.js") // 1024, "KB,", len(DATA), "items")
print("index.html written:", len(page) // 1024, "KB,", len(NAV), "sections")
