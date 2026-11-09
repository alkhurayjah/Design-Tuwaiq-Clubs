"""Build README.pdf — the visual introduction to the package (what it is + everything it can do).
usage: python3 scripts/build_readme_pdf.py        -> README.pdf (16:9 pages)"""
import os, glob, json, html
from playwright.sync_api import sync_playwright

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)
E = html.escape
G = lambda p: sorted(glob.glob(p))
n_files = sum(len(f) for _, _, f in os.walk(".") if True)
px = json.load(open("assets/pixels/pixels.json", encoding="utf-8"))
ic = json.load(open("assets/icons/academy/icons.json", encoding="utf-8"))


def pxsvg(k, color, h=60):
    v = px[k]
    return f'<svg viewBox="0 0 {v["w"]} {v["h"]}" style="height:{h}px"><path fill="{color}" d="{v["d"]}"/></svg>'


DECO = ('<div class="pxd" style="left:56px;top:48px;width:18px;height:18px;background:#57E3D8"></div>'
        '<div class="pxd" style="left:24px;top:110px;width:28px;height:28px;background:#9C75FF"></div>'
        '<div class="pxd" style="left:300px;top:70px;width:14px;height:14px;background:#F4A664"></div>')


def page(body, cls="light", num=None, title=None, kicker=None):
    head = ""
    if title:
        head = (f'<div class="ph"><div><span class="kick">{E(kicker or "")}</span><h2>{E(title)}</h2></div>'
                f'<div class="lg"><img src="assets/logos/club/tuwaiq-club-color-no-tagline.svg"><i></i><img src="assets/logos/academy/tuwaiq-academy-horizontal-color.svg" style="height:26px"></div></div>')
    foot = f'<div class="pf"><span>Tuwaiq_Clubs_Claude_Design</span><span>{num:02d}</span></div>' if num else ""
    return f'<section class="pg {cls}">{head}{body}{foot}</section>'


SITE_URL = 'https://claude.ai/artifact/WfmTw6KSubrHGsbQiGSbcd'
P = []
# 1 cover ------------------------------------------------------------------
P.append(page(f'''{DECO}
<div class="cover">
 <div class="clogos"><img src="assets/logos/club/tuwaiq-club-white-no-tagline.svg" style="height:86px"><i></i><img src="assets/logos/academy/tuwaiq-academy-horizontal-white.svg" style="height:58px"></div>
 <p class="ck">حزمة التصميم الشاملة لأندية طويق وأكاديمية طويق</p>
 <h1>Tuwaiq_Clubs<br>Claude_Design</h1>
 <p class="cs">الهوية، والأصول، والقوالب، والتقارير، ومهارات Claude، كلها في مكان واحد</p>
 <div class="cstats"><div><b>{n_files}</b><span>ملف</span></div><div><b>4</b><span>مهارات لـ Claude</span></div><div><b>14+3</b><span>قوالب بوستات ومطبوعات وعروض وتقارير</span></div><div><b>{len(G("assets/logos/universities/*/*.svg"))+len(G("assets/logos/universities/*/*-color.png"))-len(G("assets/logos/universities/*/*-color.svg"))+len(G("assets/logos/partners/*/"))+14}</b><span>شعار</span></div></div>
 <a class="cbtn" href="{SITE_URL}">افتح دليل الهوية والأدوات <b>←</b></a>
</div>
<img class="corner" src="assets/pixels/svg/club-mark-3color.svg" alt="">''', "cov"))

# 2 what is it -------------------------------------------------------------
P.append(page('''<div class="two">
<div class="lead"><p>هذه الحزمة هي <b>المرجع الكامل</b> لتصميم أي محتوى لأندية طويق: بوستات، وستوريات، وشرائح، وتقارير أسبوعية ودورية.</p>
<p>جمعت فيها كل ما تعلّمته في جلسة التدريب:</p>
<ul><li>أدلة الهوية: الأندية، والأكاديمية، والهوية الرقمية.</li><li>منصة club.tuwaiq.edu.sa.</li><li>مولّد البكسل.</li><li>25 بوستًا رسميًا.</li><li>قوالب العروض والتقارير.</li><li>صور الحرم الجامعي.</li><li>الشعارات الرسمية.</li></ul>
<p>كل شيء مرتّب ومسمّى وجاهز للاستخدام المباشر، سواء للمصمم أو لـ Claude.</p></div>
<div class="ways">
<div class="way"><span>1</span><h4>للمصمم</h4><p>افتح <a class="lnk" href="'''+SITE_URL+'''">دليل الهوية والأدوات</a> (أو <code>index.html</code> من الحزمة): دليل بصري لكل الأصول، وتحت كل عنصر أزرار نسخ للصورة أو الكود أو اللون أو الخط.</p></div>
<div class="way"><span>2</span><h4>لـ Claude</h4><p>ارفع الحزمة والصق <code>prompts/SYSTEM_PROMPT.md</code>. يتبع Claude المهارات والقواعد، ويصمم بنفس الهوية.</p></div>
<div class="way"><span>3</span><h4>للتوليد الآلي</h4><p>أدوات في <code>scripts/</code> تصدّر القوالب إلى PNG، وتبني التقارير PowerPoint من بيانات JSON.</p></div>
</div></div>''', num=2, title="وش هي الحزمة؟", kicker="نظرة عامة"))

# 3 what I can do (one page) ---------------------------------------------
caps = [
    ("templates/previews/club-workshop-1080.png", "بطاقات الورش والجلسات", "بوست مربع للأندية فيه نوع الفعالية، والعنوان، والمقدم، والوصف، وحبوب التاريخ والوقت والمكان."),
    ("templates/previews/club-weekly-schedule-1080x1560.png", "جدول فعاليات الأسبوع", "فعاليات الجامعات والأكاديمية في صفوف ملونة حسب الجهة، مع حضوري أو عن بعد."),
    ("templates/previews/club-launch-story-1080x1920.png", "ستوري إطلاق نادي", "صورة الجامعة بطبقة بنفسجية، والمزايا، والمجالات، وشعار الجامعة."),
    ("templates/previews/club-countdown-1080.png", "حملات العدّ التنازلي", "سلسلة 4، 3، 2، 1 بجمل تشويقية وزر تسجيل، مع الشريك."),
    ("templates/previews/academy-story-results-1080x1920.png", "ستوريات الأكاديمية", "فائزون، وإنجازات، وإطلاقات، وأرقام، بأسلوب بوستات الأكاديمية."),
    ("templates/previews/presentation/presentation-01.png", "عرض تقديمي كامل", "PowerPoint قابل للتعديل: 13 شريحة (غلاف، محاور، أقسام، صور، بطاقات، أرقام، رسم بياني، مراحل، جدول، اقتباس، فعالية، ختام)."),
    ("templates/previews/weekly/weekly-report-example-1.png", "التقرير الأسبوعي", "PowerPoint عمودي 9:16 فيه الأرقام، والفعاليات بالصور، والمخرجات، والأسبوع القادم."),
    ("templates/previews/report/club-report-example-02.png", "التقرير الدوري", "PowerPoint 16:9 فيه ملخص، وجدول، ورسم بياني، ومستهدفات، وإنجازات، وخطة."),
]
cards = "".join(f'<div class="cap"><div class="ci"><img src="{s}"></div><h4>{E(t)}</h4><p>{E(d)}</p></div>' for s, t, d in caps)
extra = '''<div class="capx">
<div><b>توليد أشكال بكسل</b><span>بنفس خوارزمية مولّد طويق: أي شكل جديد بلون الهوية.</span></div>
<div><b>استخراج الأصول</b><span>شعارات وصور من ملفات PowerPoint وPDF والمواقع، وتنظيفها وتسميتها.</span></div>
<div><b>مراجعة التصاميم</b><span>فحص أي تصميم مقابل قواعد الهوية: الشعارات، والألوان، والنبرة، والعناصر الإلزامية.</span></div>
<div><b>كتابة المحتوى</b><span>صياغة بنبرة طويق المعتمدة، بلا مبالغة ولا وعود.</span></div>
<div><b>تصدير جاهز</b><span>PNG للنشر، وPowerPoint قابل للتعديل، وPDF للمشاركة.</span></div>
</div>'''
P.append(page(f'<div class="caps">{cards}</div>{extra}', num=3, title="وش أقدر أسوي — مرة وحدة", kicker="القدرات"))
caps2 = [
    ("templates/previews/club-certificate-a4.png", "شهادة حضور أو شكر", "A4 أفقي للطباعة: اسم المشارك، والفعالية، والتاريخ، والمكان، وتوقيعان."),
    ("templates/previews/club-partnership-1080.png", "إعلان شراكة", "النادي × الشريك مع سطر عن هدف الشراكة. يُنشر بعد اعتمادها فقط."),
    ("templates/previews/club-semester-harvest-1080x1350.png", "حصاد الفصل", "ستة أرقام رئيسية وأبرز المحطات، مع شعار الجامعة."),
    ("templates/previews/club-winners-1080x1350.png", "فائزو مسابقة النادي", "المراكز الثلاثة بأسماء الفرق وأفكار المشاريع."),
    ("templates/previews/banner-linkedin-1584x396.png", "غلاف LinkedIn", "1584×396، والمحتوى يمينًا بعيدًا عن صورة الحساب."),
    ("templates/previews/banner-x-1500x500.png", "غلاف X", "1500×500، والمحتوى في المنطقة الآمنة."),
    ("templates/previews/print-rollup-stand-1000x2000.png", "ستاند ترحيبي", "100×200 سم بمكان لشعار الجامعة، وأسفله منطقة القاعدة."),
    ("templates/previews/print-badge-6x12.png", "بطاقات الفعاليات", "6×12 سم بخمسة أنواع: منظم، ومشارك، وزائر، ومحكم، ومتحدث."),
]
cards2 = "".join(f'<div class="cap"><div class="ci"><img src="{s}"></div><h4>{E(t)}</h4><p>{E(d)}</p></div>' for s, t, d in caps2)
P.append(page(f'<div class="caps">{cards2}</div>', num=4, title="قوالب إضافية: شهادات وشراكات ومطبوعات", kicker="القوالب"))

# 4 posts showcase ---------------------------------------------------------
show = "".join(f'<img src="{s}">' for s in ["templates/previews/club-workshop-1080.png", "templates/previews/club-countdown-1080.png",
                                             "templates/previews/club-weekly-schedule-1080x1560.png", "templates/previews/club-launch-story-1080x1920.png",
                                             "templates/previews/academy-story-results-1080x1920.png"])
P.append(page(f'<div class="show">{show}</div><p class="cap2">كل القوالب HTML قابلة للتعديل، وتُصدَّر PNG بدقة مضاعفة بأمر واحد: <code>python3 scripts/render.py 2</code></p>',
              "dark", 5, "قوالب البوستات", "عرض"))

# 5 reports ----------------------------------------------------------------
wk = "".join(f'<img class="t" src="{s}">' for s in G("templates/previews/weekly/*.png"))
pr = "".join(f'<img class="w" src="{s}">' for s in G("templates/previews/report/*.png")[:5])
P.append(page(f'''<div class="rep"><div class="rl"><h4>التقرير الأسبوعي (9:16)</h4><div class="strip">{wk}</div></div>
<div class="rl"><h4>التقرير الدوري (16:9)</h4><div class="strip">{pr}</div></div>
<p class="cap2">تعطيني البيانات (أرقام، وفعاليات، وصور)، فيطلع ملف PowerPoint بقالبكم الرسمي نفسه، والصور فيه بزوايا دائرية.</p></div>''',
              num=6, title="التقارير", kicker="PowerPoint"))

# 6 identity at a glance ---------------------------------------------------
sw = "".join(f'<div class="s"><span style="background:{c}"></span><b>{n}</b><code>{c}</code></div>' for c, n in
             [("#4F29B7", "البنفسجي 75%"), ("#57E3D8", "تركواز"), ("#A380FF", "بنفسجي فاتح"), ("#F4A664", "برتقالي"), ("#262626", "أسود"), ("#EDEDED", "رمادي")])
pxs = "".join(pxsvg(k, c, 46) for k, c in [("zigzag", "#9C75FF"), ("v-shape", "#57E3D8"), ("terminal", "#F4A664"), ("plus", "#B798FF"), ("code-brackets", "#9C75FF"), ("arrow-diagonal", "#57E3D8"), ("hash", "#F4A664"), ("chart", "#CDB7FF")])
ics = "".join(f'<img src="assets/icons/academy/purple/{k}.svg">' for k in ic)
P.append(page(f'''<div class="idg">
<div class="box"><h4>الشعارات</h4><div class="lgs"><img src="assets/logos/club/tuwaiq-club-color.svg"><img src="assets/logos/academy/tuwaiq-academy-horizontal-color.svg" style="height:46px"><img src="assets/logos/academy/tuwaiq-academy-vertical-color.svg"></div>
<div class="lgs dk"><img src="assets/logos/club/tuwaiq-club-white.svg"><img src="assets/logos/academy/tuwaiq-academy-horizontal-white.svg" style="height:46px"></div><p>رسمية بصيغ SVG وPDF: ملوّن وأبيض وأسود، أفقي ورأسي.</p></div>
<div class="box"><h4>الألوان</h4><div class="sws">{sw}</div><p>البنفسجي 75%، والثانوية 20% للفت الانتباه، والنص أبيض أو أسود.</p></div>
<div class="box"><h4>الخط — IBM Plex Sans Arabic</h4><p class="ty"><b style="font-weight:700">فعاليــات أنديــة طويــق</b><br><span style="font-weight:500;color:#57C9C0">العنوان الفرعي</span> · <span style="font-weight:300">جملة حملة خفيفة</span></p><p>ملفات الخط مضمّنة، والتطويل (ـ) توقيع أساسي في العناوين.</p></div>
<div class="box"><h4>البكسل والأيقونات</h4><div class="pxs">{pxs}</div><div class="ics">{ics}</div><p>المربعات زواياها 15%، والمتجاور يندمج، والقطري بجسر مقعّر. والأيقونات هي أيقونات الأكاديمية الرسمية.</p></div>
</div>''', num=7, title="الهوية في نظرة", kicker="المرجع"))

# 7 asset library ----------------------------------------------------------
unis = "".join(f'<img src="{s}">' for s in sorted(G("assets/logos/universities/*/*-color.svg")+[x for x in G("assets/logos/universities/*/*-color.png") if not os.path.exists(x[:-4]+".svg")]))
parts = "".join(f'<img src="{s}">' for s in G("assets/logos/partners/*/*-color.svg") if "dcl-" not in s) + '<img src="assets/logos/partners/dcl/dcl-black.svg">'
camp = "".join(f'<img src="{s}">' for s in G("assets/photos/campus/*.jpg")[:10])
P.append(page(f'''<div class="lib">
<div><h4>{len(G("assets/logos/universities/*/"))} جامعة × ملون وأبيض وأسود</h4><div class="lg6">{unis}</div></div>
<div><h4>{len(G("assets/logos/partners/*/"))} شريك</h4><div class="lg6 p">{parts}</div></div>
<div class="full"><h4>{len(G("assets/photos/campus/*"))} صورة حرم جامعي + صورة حفل التكريم</h4><div class="camp">{camp}</div></div>
<p class="cap2">إضافة إلى {len(px)} شكل بكسل بسبع ألوان، و{len(ic)} أيقونات بثلاث نسخ، وزخارف المنصة، وإطار الورشة، والخط بخمسة أوزان.</p></div>''',
              num=8, title="مكتبة الأصول", kicker="assets/"))

# 8 structure --------------------------------------------------------------
rows = [("index.html", "الدليل البصري للمصمم، مع أزرار نسخ (يحتاج docs/index-data.js)"),
        ("README.pdf", "هذا الملف"),
        ("prompts/SYSTEM_PROMPT.md", "البرومت الرئيسي لـ Claude، وبرومتات جاهزة لكل نوع"),
        ("brand/", "BRAND_GUIDE.md (الدليل الكامل)، وtokens.css، وtokens.json"),
        ("skills/", "4 مهارات: tuwaiq-clubs-brand · tuwaiq-social-posts · tuwaiq-club-posts · tuwaiq-club-reports"),
        ("templates/html/", "6 قوالب بوستات وشرائح، وملف _base.css"),
        ("templates/pptx/", "قالبا التقرير الأسبوعي والدوري، وأمثلة JSON ومخرجاتها"),
        ("templates/previews/", "معاينات PNG لكل قالب وتقرير"),
        ("assets/logos/", "club · academy · universities · partners"),
        ("assets/icons · pixels · decorations", "الأيقونات، وأشكال البكسل، والزخارف"),
        ("assets/photos · fonts", "صور الحرم والفعاليات، وIBM Plex Sans Arabic"),
        ("scripts/", "render · build_weekly_report · build_club_report · pixels · trace · build_index · build_readme_pdf"),
        ("references/", "الأدلة والقوالب الأصلية، و25 بوستًا مرجعيًا، ولوحات Claude Design"),
        ("docs/", "صور فهرسية، وبيانات index.html، ومعرّفات الأصول في Claude")]
tb = "".join(f'<tr><td><code>{E(a)}</code></td><td>{E(b)}</td></tr>' for a, b in rows)
P.append(page(f'<table class="tree"><tr><th>المسار</th><th>المحتوى</th></tr>{tb}</table>', num=9, title="محتوى الملف", kicker="الهيكل"))

# 9 how to use -------------------------------------------------------------
P.append(page('''<div class="steps">
<div class="st"><span>01</span><h4>مع Claude</h4><p>ارفع الملف المضغوط في محادثة جديدة، والصق محتوى <code>prompts/SYSTEM_PROMPT.md</code>، ثم اطلب مباشرة.</p>
<div class="ex">"صمّم بطاقة ورشة لنادي طويق: العنوان …، المقدم …، 18 نوفمبر، 4–5 مساءً، عن بعد، الشريك الكراج"</div>
<div class="ex">"جهّز التقرير الأسبوعي للأسبوع 10: الأرقام …، الفعاليات …، الأسبوع القادم …"</div></div>
<div class="st"><span>02</span><h4>للمصمم</h4><p>افتح <a class="lnk" href="'''+SITE_URL+'''">دليل الهوية والأدوات</a>، وانسخ الشعار أو الأيقونة أو الشكل كصورة PNG أو كود SVG، وانسخ أكواد الألوان والخط، وابدأ من القالب المناسب.</p></div>
<div class="st"><span>03</span><h4>التوليد بالأوامر</h4><p>تحتاج Python وPlaywright وpython-pptx:</p>
<pre>python3 scripts/render.py 2
python3 scripts/build_weekly_report.py templates/pptx/weekly-report-template.pptx weekly.json out.pptx
python3 scripts/build_club_report.py templates/pptx/club-report-template.pptx report.json out.pptx
python3 scripts/build_index.py</pre></div>
</div>''', num=10, title="طريقة الاستخدام", kicker="البدء"))

# 10 rules + notes ---------------------------------------------------------
P.append(page('''<div class="rules2">
<div><h4>قواعد لا تُكسر</h4><ul>
<li>شعارات رسمية فقط، بلا إعادة تلوين ولا تأثيرات، والنسخة البيضاء على الداكن.</li>
<li><b>الأكاديمية:</b> الشعار أعلى اليمين. <b>الأندية:</b> النادي أعلى اليمين، والأكاديمية أسفل اليمين، و@TuwaiqClubs أسفل اليسار.</li>
<li>إعلان الفعالية فيه: العنوان، والتاريخ، والوقت، والمكان، والرابط، وشعار النادي، وشعار الجامعة.</li>
<li>الصور في العروض زواياها دائرية دائمًا، ومعها مربع خلفي عند الحاجة.</li>
<li>لا أرقام ولا أسماء مخترعة، والناقص يبقى [بين قوسين].</li>
<li>النبرة ودودة وواقعية: لا "نضمن"، ولا "أقوى"، ولا "باقي 3 كراسي".</li>
<li>لا بيانات شخصية للطلاب، ولا صور فردية بلا موافقة.</li></ul></div>
<div><h4>ملاحظات الجودة</h4><ul>
<li>شعارات النادي والأكاديمية والأيقونات والبكسل: ملفات متجهية بجودة كاملة.</li>
<li>شعارات الجامعات والشركاء: PNG بعرض 400–750px، تكفي للرقمي، وللطباعة الكبيرة اطلبوا SVG.</li>
<li>شعار جامعة الحدود الشمالية غير موجود.</li>
<li>صور منخفضة الدقة: imam، وiau، وjazan. وصورة الباحة فيها علامة مائية. وصور kfupm وkau وtaif من Wikimedia وتحتاج ذكر المصوّر (SOURCES.md).</li>
<li>عند إضافة أصول جديدة: <code>build_index.py</code> يحدّث الدليل البصري، و<code>build_readme_pdf.py</code> يحدّث هذا الملف.</li></ul></div></div>''',
              num=11, title="القواعد والملاحظات", kicker="مهم"))

# 11 closing — logos only, no text ------------------------------------------
P.append(page(f'''{DECO}<div class="cover end" style="top:290px"><div class="clogos"><img src="assets/logos/club/tuwaiq-club-white-no-tagline.svg" style="height:110px"><i></i><img src="assets/logos/academy/tuwaiq-academy-horizontal-white.svg" style="height:72px"></div></div>''', "cov"))

css = '''@import url("brand/tokens.css");
@page{size:1280px 720px;margin:0}
*{box-sizing:border-box} body{margin:0;font-family:var(--font);color:#262626;-webkit-print-color-adjust:exact;print-color-adjust:exact}
code,pre{font-family:ui-monospace,Menlo,monospace;direction:ltr;unicode-bidi:isolate}
.pg{width:1280px;height:720px;position:relative;overflow:hidden;page-break-after:always;padding:56px 72px 64px;direction:rtl}
.light{background:#F5F1FF} .dark{background:linear-gradient(180deg,#1F0F45,#4A20AE);color:#fff}
.cov{background:linear-gradient(160deg,#1F0F45 0%,#4F29B7 70%,#6438DD 100%);color:#fff}
.pxd{position:absolute;border-radius:15%}
.ph{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:22px}
.ph h2{margin:2px 0 0;font-size:40px;color:#4F29B7;font-weight:700} .dark .ph h2{color:#57E3D8}
.kick{font-size:15px;font-weight:600;color:#F4A664}
.lg{display:flex;align-items:center;gap:14px} .lg img{height:34px} .lg i{width:1.5px;height:30px;background:#CDB7FF}
.dark .lg img{filter:brightness(0) invert(1)}
.pf{position:absolute;left:72px;right:72px;bottom:22px;display:flex;justify-content:space-between;font-size:12px;color:#9C75FF}
.dark .pf{color:#CDB7FF}
.cover{position:absolute;right:96px;top:90px;width:760px} .cover.end{right:0;left:0;width:auto;top:200px;text-align:center}
.cover.end .clogos{justify-content:center}
.cbtn{display:inline-flex;align-items:center;gap:12px;margin-top:30px;padding:14px 26px;border-radius:14px;background:#57E3D8;color:#1F0F45;font-weight:700;font-size:22px;text-decoration:none}.cbtn b{font-size:22px}
.lnk{color:#4F29B7;font-weight:700;text-decoration:underline}
.clogos{display:flex;align-items:center;gap:26px} .clogos i{width:2px;height:70px;background:rgba(255,255,255,.5)}
.ck{margin:46px 0 6px;font-size:22px;color:#F4A664;font-weight:500}
.cover h1{margin:0;font-size:78px;line-height:1.05;color:#57E3D8;direction:ltr;text-align:right;font-weight:700}
.cover.end h1{text-align:center;direction:rtl}
.cs{font-size:22px;color:#E3D8FF;margin:16px 0 0}
.cstats{display:flex;gap:34px;margin-top:44px} .cstats div{display:flex;flex-direction:column} .cstats b{font-size:40px;color:#fff;line-height:1} .cstats span{font-size:15px;color:#CDB7FF;margin-top:6px}
.corner{position:absolute;left:-30px;bottom:-16px;height:216px}  /* official club mark, small, cropped by the page edge — like the report/guide covers */
.two{display:grid;grid-template-columns:1.1fr 1fr;gap:40px}
.lead p{font-size:21px;line-height:1.75;margin:0 0 14px} .lead ul{margin:0 0 14px;padding-right:22px;font-size:19px;line-height:1.75} .lead b{color:#4F29B7}
.ways{display:flex;flex-direction:column;gap:14px}
.way{background:#fff;border-radius:18px;padding:18px 22px;position:relative;padding-right:74px}
.way span{position:absolute;right:20px;top:18px;width:38px;height:38px;border-radius:8px;background:#9C75FF;color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center;font-size:20px}
.way h4{margin:0 0 4px;font-size:20px;color:#4F29B7} .way p{margin:0;font-size:16px;line-height:1.6} .way code{font-size:14px;color:#6B4BE0}
.caps{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.cap{background:#fff;border-radius:16px;padding:10px 12px 12px}
.ci{height:120px;border-radius:10px;background:#1F0F45;display:flex;align-items:center;justify-content:center;overflow:hidden}
.ci img{max-height:120px;max-width:100%} .cap h4{margin:8px 0 3px;font-size:16px;color:#4F29B7} .cap p{margin:0;font-size:12.5px;line-height:1.5;color:#444}
.capx{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:14px}
.capx div{background:#4F29B7;color:#fff;border-radius:14px;padding:10px 12px} .capx b{display:block;font-size:14.5px;color:#57E3D8;margin-bottom:3px} .capx span{font-size:12px;line-height:1.5;color:#E3D8FF}
.show{display:flex;gap:12px;align-items:center;justify-content:center;height:470px}
.show img{height:440px;width:auto;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.35)}
.show img:nth-child(1),.show img:nth-child(2){height:200px} .show img:nth-child(3){height:400px} .show img:nth-child(4),.show img:nth-child(5){height:420px}
.cap2{font-size:15px;color:#585858;margin:14px 0 0;text-align:center} .dark .cap2{color:#E3D8FF} .cap2 code{color:#9C75FF}
.rep h4{margin:0 0 8px;font-size:18px;color:#4F29B7}
.rl{margin-bottom:14px} .strip{display:flex;gap:10px} .strip img{border-radius:8px;box-shadow:0 4px 14px rgba(79,41,183,.18)}
.strip img.t{height:250px} .strip img.w{height:122px}
.idg{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.box{background:#fff;border-radius:18px;padding:16px 20px} .box h4{margin:0 0 10px;font-size:18px;color:#4F29B7} .box p{margin:8px 0 0;font-size:13.5px;color:#585858;line-height:1.55}
.lgs{display:flex;gap:18px;align-items:center} .lgs img{height:66px} .lgs.dk{background:#4F29B7;border-radius:10px;padding:8px 12px;margin-top:8px} .lgs.dk img{height:48px}
.sws{display:grid;grid-template-columns:repeat(6,1fr);gap:8px} .s span{display:block;height:58px;border-radius:10px;border:1px solid rgba(0,0,0,.06)} .s b{display:block;font-size:12px;margin-top:4px} .s code{font-size:11px;color:#6B5B9A}
.ty{font-size:28px;line-height:1.5;margin:0 !important;color:#262626 !important}
.pxs{display:flex;gap:14px;align-items:center;background:#4F29B7;border-radius:10px;padding:8px 12px} .ics{display:flex;gap:12px;margin-top:10px} .ics img{height:30px}
.lib{display:grid;grid-template-columns:1fr 1fr;gap:12px 24px} .lib h4{margin:0 0 8px;color:#4F29B7;font-size:18px} .lib .full{grid-column:1/-1}
.lg6{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;background:#fff;border-radius:14px;padding:10px}
.lg6 img{width:100%;height:46px;object-fit:contain} .lg6.p img{height:30px}
.camp{display:grid;grid-template-columns:repeat(10,1fr);gap:8px} .camp img{width:100%;height:96px;object-fit:cover;border-radius:10px}
.tree{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden;font-size:14.5px}
.tree th{background:#9C75FF;color:#fff;text-align:right;padding:7px 14px} .tree td{padding:4.5px 14px;border-bottom:1px solid #EEE9FA;font-size:13.5px} .tree code{color:#4F29B7;font-size:12.5px}
.steps{display:grid;grid-template-columns:1.15fr .85fr 1.15fr;gap:16px}
.st{background:#fff;border-radius:18px;padding:18px 20px} .st span{font-size:30px;font-weight:700;color:#9C75FF} .st h4{margin:2px 0 6px;font-size:20px;color:#4F29B7} .st p{margin:0 0 10px;font-size:15px;line-height:1.65}
.st code{color:#6B4BE0;font-size:13px} .ex{background:#F5F1FF;border-radius:10px;padding:8px 12px;font-size:13.5px;line-height:1.6;margin-top:8px;color:#4F29B7}
pre{background:#1F0F45;color:#CDB7FF;border-radius:10px;padding:12px;font-size:11px;line-height:1.7;white-space:pre-wrap;margin:0;text-align:left}
.rules2{display:grid;grid-template-columns:1fr 1fr;gap:18px} .rules2>div{background:#fff;border-radius:18px;padding:18px 22px}
.rules2 h4{margin:0 0 8px;font-size:20px;color:#4F29B7} .rules2 ul{margin:0;padding-right:20px;font-size:15px;line-height:1.75} .rules2 code{font-size:13px;color:#6B4BE0}
'''
html_doc = f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(P)}</body></html>'
tmp = os.path.join(root, "_readme_build.html")
open(tmp, "w", encoding="utf-8").write(html_doc)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto("file://" + tmp); pg.wait_for_timeout(1500); pg.evaluate("document.fonts.ready")
    pg.pdf(path="README.pdf", width="1280px", height="720px", print_background=True, prefer_css_page_size=True)
os.remove(tmp)
print("README.pdf written,", len(P), "pages,", os.path.getsize("README.pdf") // 1024, "KB")
