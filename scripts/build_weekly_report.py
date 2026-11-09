"""Build the WEEKLY Tuwaiq Clubs report (portrait 9:16 PowerPoint, 11.25 x 20 in) from the official
weekly template + a JSON file.

usage:
  python3 scripts/build_weekly_report.py templates/pptx/weekly-report-template.pptx weekly.json out.pptx

Template slides: 1 cover · 2 event card (photo + description) · 3 numbered list.
Extra slide types are built on the same purple canvas, inspired by the rest of the identity:
kpis (stat cards like the academy posts), upcoming (rows like the clubs weekly-schedule post), closing.

JSON (see templates/pptx/weekly-report-example.json):
{
  "slides": [
    {"type": "cover", "title": "التقرير الأسبوعي", "subtitle": "أندية طويق", "week": "الأسبوع 10 من الدراسة",
     "period": "فترة التقرير من الأحد 8 نوفمبر إلى الخميس 12 نوفمبر"},
    {"type": "kpis", "title": "الأسبوع بالأرقام", "items": [{"value": "12", "label": "فعالية"}, ...max 4]},
    {"type": "event", "title": "فعاليات الأسبوع", "name": "مسابقة ...", "image": "photo.jpg",
     "tag": "جامعة ... - نادي طويق", "subtitle": "مسابقة | 10 نوفمبر", "text": "..."},
    {"type": "list", "title": "أبرز المخرجات", "items": ["...", "...", "...", "..."]},          # max 4 per slide
    {"type": "upcoming", "title": "فعاليات الأسبوع القادم",
     "items": [{"day": "15", "month": "نوفمبر", "org": "جامعة ... – النادي", "name": "...", "time": "4:00 م",
                "mode": "حضوري|عن بعد", "academy": false}, ...max 5]},
    {"type": "closing"}
  ]
}
Never invent numbers or names: keep "[...]" placeholders for anything missing.
"""
import sys, json, copy, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_club_report import clone_slide, by_id, set_text, para, round_picture, FONT
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

LILAC = RGBColor(0x9C, 0x75, 0xFF); WHITE = RGBColor(0xFF, 0xFF, 0xFF); ORANGE = RGBColor(0xF4, 0xA6, 0x64)
TEAL = RGBColor(0x57, 0xE3, 0xD8); MINT = RGBColor(0x9A, 0xED, 0xE6); SOFT = RGBColor(0xEE, 0xEE, 0xEE)
CARD = RGBColor(0x5E, 0x3B, 0xC4); INK = RGBColor(0x1A, 0x15, 0x30); LIGHTLILAC = RGBColor(0xA8, 0x93, 0xFF)


def remove(sl, *ids):
    for i in ids:
        e = by_id(sl, i)._element; e.getparent().remove(e)


def no_style(shape):
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)
    shape.line.fill.background()


def rrect(sl, l, t, w, h, fill, radius=0.18, alpha=None, line=None):
    s = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    s.adjustments[0] = radius; no_style(s)
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if alpha is not None:
        sf = s.fill._xPr.find(qn("a:solidFill"))[0]
        a = sf.makeelement(qn("a:alpha"), {"val": str(int(alpha * 100000))}); sf.append(a)
    if line:
        s.line.color.rgb = line; s.line.width = Pt(2)
    return s


def build(template, data, out):
    prs = Presentation(template)
    tpl = list(prs.slides)
    for s in data["slides"]:
        k = s["type"]
        if k == "cover":
            sl = clone_slide(prs, tpl[0])
            set_text(by_id(sl, 59), s.get("title", "التقرير الأسبوعي"))
            set_text(by_id(sl, 60), s.get("subtitle", "أندية طويق"))
            set_text(by_id(sl, 64), s.get("week", "الأسبوع [0] من الدراسة"))
            set_text(by_id(sl, 63), s.get("period", "فترة التقرير من الأحد [0] إلى الخميس [0]"))

        elif k == "closing":
            sl = clone_slide(prs, tpl[0])
            remove(sl, 59, 60, 63, 64)
            g = by_id(sl, 55)  # logo group: centre and enlarge
            ratio = Inches(7.6) / g.width
            g.width = Inches(7.6); g.height = int(g.height * ratio)
            g.left = int((prs.slide_width - g.width) / 2); g.top = Inches(8.6)

        elif k == "event":
            sl = clone_slide(prs, tpl[1])
            set_text(by_id(sl, 70), s.get("title", "فعاليات الأسبوع"))
            set_text(by_id(sl, 69), s.get("name", "[اسم الفعالية]"))
            set_text(by_id(sl, 71), s.get("tag", "[الجامعة] - نادي طويق"))
            set_text(by_id(sl, 73), s.get("subtitle", "[نوع الفعالية | التاريخ]"))
            set_text(by_id(sl, 72), s.get("text", "[وصف مختصر للفعالية ونتائجها]"))
            card = by_id(sl, 69); tag = by_id(sl, 71)
            if s.get("image"):
                # photo inside the white card: rounded corners always (identity rule)
                l, t = card.left + Inches(0.3), card.top + Inches(1.0)
                w, h = card.width - Inches(0.6), tag.top - card.top - Inches(1.3)
                pic = sl.shapes.add_picture(s["image"], l, t)
                # cover-crop to the box
                iw, ih = pic.image.size; box = w / h; img = iw / ih
                if img > box:
                    c = (1 - box / img) / 2; pic.crop_left = c; pic.crop_right = c
                else:
                    c = (1 - img / box) / 2; pic.crop_top = c; pic.crop_bottom = c
                pic.left, pic.top, pic.width, pic.height = l, t, w, h
                round_picture(pic, 0.05)
                tree = sl.shapes._spTree; tree.remove(tag._element); tree.append(tag._element)  # tag above photo

        elif k == "list":
            sl = clone_slide(prs, tpl[2])
            set_text(by_id(sl, 87), s.get("title", "[عنوان]"))
            rows = [(78, 79), (80, 81), (82, 83), (84, 85)]
            for n, (txt, num) in enumerate(rows):
                if n < len(s["items"]):
                    it = s["items"][n]
                    set_text(by_id(sl, txt), it if isinstance(it, str) else it["text"])
                    set_text(by_id(sl, num), f"{n + 1:02d}" if isinstance(it, str) else it.get("num", f"{n + 1:02d}"))
                else:
                    remove(sl, txt, num)

        elif k in ("kpis", "upcoming"):
            sl = clone_slide(prs, tpl[2])
            set_text(by_id(sl, 87), s.get("title", "[عنوان]"))
            remove(sl, 78, 79, 80, 81, 82, 83, 84, 85)
            if k == "kpis":
                items = s["items"][:4]; accents = [LILAC, TEAL, ORANGE, LIGHTLILAC]
                cw, ch, gap = Inches(4.3), Inches(4.1), Inches(0.45)
                x0 = prs.slide_width - Inches(0.95)  # RTL: start from the right
                for n, it in enumerate(items):
                    col, row = n % 2, n // 2
                    l = x0 - (col + 1) * cw - col * gap; t = Inches(4.0) + row * (ch + gap)
                    c = rrect(sl, l, t, cw, ch, WHITE, 0.12, alpha=0.08)
                    tf = c.text_frame; tf.clear(); tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
                    para(tf, it["value"], 66, accents[n % 4], bold=True, align=PP_ALIGN.CENTER, first=True)
                    para(tf, it["label"], 26, WHITE, align=PP_ALIGN.CENTER)
            else:
                items = s["items"][:5]; t = Inches(3.6); rh = Inches(2.0); gap = Inches(0.5)
                right = prs.slide_width - Inches(0.8); width = Inches(9.6); left = right - width
                for it in items:
                    acad = it.get("academy", False); acc = LIGHTLILAC if acad else MINT
                    body = rrect(sl, left, t, width, rh, CARD, 0.08, line=acc)
                    date = rrect(sl, right - Inches(1.75), t, Inches(1.75), rh, acc, 0.08)
                    tf = date.text_frame; tf.clear(); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                    para(tf, it.get("day", "[00]"), 44, INK, bold=True, align=PP_ALIGN.CENTER, first=True)
                    para(tf, it.get("month", "[الشهر]"), 20, INK, align=PP_ALIGN.CENTER)
                    tb = sl.shapes.add_textbox(left + Inches(2.3), t + Inches(0.2), Inches(5.4), rh - Inches(0.4))
                    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                    para(tf, it.get("org", "[الجهة]"), 18, SOFT, first=True)
                    para(tf, it.get("name", "[اسم الفعالية]"), 24, WHITE, bold=True)
                    tm = rrect(sl, left + Inches(0.3), t + Inches(0.42), Inches(1.75), Inches(0.5), CARD, 0.2, line=SOFT)
                    tf = tm.text_frame; tf.clear(); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                    para(tf, it.get("time", "[0:00 م]"), 16, WHITE, bold=True, align=PP_ALIGN.CENTER, first=True)
                    md = rrect(sl, left + Inches(0.3), t + Inches(1.08), Inches(1.75), Inches(0.5), MINT if it.get("mode") == "عن بعد" else LIGHTLILAC, 0.2)
                    tf = md.text_frame; tf.clear(); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                    para(tf, it.get("mode", "حضوري"), 16, INK, bold=True, align=PP_ALIGN.CENTER, first=True)
                    t += rh + gap
        else:
            raise ValueError("unknown slide type: " + k)

    sldIdLst = prs.slides._sldIdLst
    for sid in list(sldIdLst)[:len(tpl)]:
        prs.part.drop_rel(sid.rId); sldIdLst.remove(sid)
    prs.save(out)
    print("saved", out, "slides:", len(prs.slides))


if __name__ == "__main__":
    build(sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3])
