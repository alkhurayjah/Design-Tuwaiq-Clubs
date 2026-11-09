"""Build a periodic Tuwaiq Club report (.pptx) from the official template + a JSON file.

usage:
  python3 scripts/build_club_report.py templates/pptx/club-report-template.pptx report.json out.pptx

The template has 8 master slides; every output slide is a copy of one of them, so fonts,
colours, logos, the purple bottom bar, page numbers and the pixel corners stay exactly as designed.

JSON shape (see templates/pptx/club-report-example.json):
{
  "subtitle": "نادي طويق – جامعة ... | تقرير شهر ...",   # small orange line on every inner slide
  "slides": [
    {"type": "cover",   "title": "...", "subtitle": "..."},
    {"type": "section", "title": "..."},
    {"type": "status",  "title": "...", "items": [{"text": "...", "status": "done|partial|not_done"}, ...max 3]},
    {"type": "table",   "title": "...", "headers": ["..",".."], "rows": [["..",".."], ...]},
    {"type": "bars",    "title": "...", "items": [{"tag": "01", "text": "..."}, ...max 2]},
    {"type": "text",    "title": "...", "text": "..."},
    {"type": "kpis",    "title": "...", "items": [{"value": "12", "label": "فعالية"}, ...max 4]},
    {"type": "chart",   "title": "...", "categories": [".."], "series": [{"name": "..", "values": [..]}]},
    {"type": "image",   "title": "...", "image": "path.jpg", "caption": "...", "backdrop": "lilac|light|teal|orange|purple (optional)", "radius": 0.08},
    {"type": "bullets", "title": "...", "items": ["..", ".."]},
    {"type": "closing"}
  ]
}
Missing facts must stay as "[...]" placeholders — never invent numbers.
"""
import sys, json, copy
from pptx import Presentation
from pptx.util import Emu, Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.oxml.ns import qn

LILAC = RGBColor(0x9C, 0x75, 0xFF); GREY = RGBColor(0x59, 0x59, 0x59); DARK = RGBColor(0x43, 0x43, 0x43)
WHITE = RGBColor(0xFF, 0xFF, 0xFF); LIGHT = RGBColor(0xD9, 0xCE, 0xF5); ORANGE = RGBColor(0xF4, 0xA6, 0x64)
TEAL = RGBColor(0x57, 0xE3, 0xD8); PURPLE = RGBColor(0x4F, 0x29, 0xB7)
FONT = "IBM Plex Sans Arabic"

# template slide index (0-based) and the shape ids used for text
T = {
    "cover":   dict(i=0, title=51, sub=52),
    "section": dict(i=1, title=63, sub=64),
    "status":  dict(i=2, title=94, sub=81),
    "table":   dict(i=3, title=113, sub=109),
    "bars":    dict(i=4, title=134, sub=130),
    "text":    dict(i=5, title=156, sub=152, body=165),
    "blank":   dict(i=6, title=175, sub=171),
    "closing": dict(i=7),
}
BLANK_TYPES = {"kpis", "chart", "image", "bullets"}


BACKDROPS = {"lilac": RGBColor(0x9C, 0x75, 0xFF), "light": RGBColor(0xD9, 0xCE, 0xF5), "teal": TEAL,
             "orange": ORANGE, "purple": PURPLE}


def round_picture(pic, radius=0.08):
    """Clip a picture to a rounded rectangle. radius = corner size as a fraction of the SHORT side."""
    pic.auto_shape_type = MSO_SHAPE.ROUNDED_RECTANGLE
    geom = pic._element.spPr.find(qn("a:prstGeom"))
    av = geom.find(qn("a:avLst"))
    if av is None:
        from lxml import etree
        av = etree.SubElement(geom, qn("a:avLst"))
    for g in list(av):
        av.remove(g)
    from lxml import etree
    gd = etree.SubElement(av, qn("a:gd")); gd.set("name", "adj"); gd.set("fmla", f"val {int(radius * 100000)}")


def by_id(slide, sid):
    for sh in slide.shapes:
        if sh.shape_id == sid:
            return sh
    raise KeyError(sid)


def set_text(shape, text):
    """Replace text but keep the first run's formatting (font, size, colour, RTL)."""
    tf = shape.text_frame
    p0 = tf.paragraphs[0]
    runs = p0.runs
    if runs:
        runs[0].text = text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
    else:
        p0.text = text
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)


def clone_slide(prs, src):
    new = prs.slides.add_slide(src.slide_layout)
    for shp in list(new.shapes):
        shp._element.getparent().remove(shp._element)
    rid_map = {}
    for rel in src.part.rels.values():
        if "notesSlide" in rel.reltype or "slideLayout" in rel.reltype:
            continue
        rid_map[rel.rId] = new.part.relate_to(rel._target, rel.reltype)
    bg = src._element.cSld.find(qn("p:bg"))
    if bg is not None:
        new._element.cSld.insert(0, copy.deepcopy(bg))
    tree = new.shapes._spTree
    for el in src.shapes._spTree.iterchildren():
        if el.tag.split("}")[1] in ("sp", "pic", "grpSp", "cxnSp", "graphicFrame"):
            e = copy.deepcopy(el)
            for node in e.iter():
                for attr in (qn("r:embed"), qn("r:link"), qn("r:id")):
                    if node.get(attr) in rid_map:
                        node.set(attr, rid_map[node.get(attr)])
            tree.append(e)
    return new


def para(tf, text, size, color, bold=False, align=PP_ALIGN.RIGHT, first=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    r = p.add_run(); r.text = text
    f = r.font; f.size = Pt(size); f.color.rgb = color; f.bold = bold; f.name = FONT
    p._p.get_or_add_pPr().set("rtl", "1")
    return p


def build(template, data, out):
    prs = Presentation(template)
    tpl = list(prs.slides)
    sub = data.get("subtitle", "")
    for s in data["slides"]:
        kind = s["type"]
        key = "blank" if kind in BLANK_TYPES else kind
        t = T[key]
        sl = clone_slide(prs, tpl[t["i"]])
        if "title" in t and "title" in s:
            set_text(by_id(sl, t["title"]), s["title"])
        if "sub" in t:
            set_text(by_id(sl, t["sub"]), s.get("subtitle", sub) if kind == "cover" else sub)

        if kind == "text":
            set_text(by_id(sl, t["body"]), s["text"])

        elif kind == "bars":
            rows = [(128, 143), (127, 144)]
            for n, (bar, tag) in enumerate(rows):
                if n < len(s["items"]):
                    it = s["items"][n]
                    set_text(by_id(sl, tag), it.get("tag", f"{n+1:02d}"))
                    b = by_id(sl, bar); tf = b.text_frame; tf.clear(); tf.word_wrap = True
                    tf.margin_right = Inches(1.15); tf.margin_left = Inches(0.3); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                    para(tf, it["text"], 16, DARK, first=True)
                else:
                    for sid in (bar, tag):
                        e = by_id(sl, sid)._element; e.getparent().remove(e)

        elif kind == "status":
            cards = [82, 86, 88]
            ind = {"done": (82, [83]), "partial": (86, [87, 93]), "not_done": (88, [89, 95])}
            tops = {c: by_id(sl, c).top for c in cards}
            originals = {k: [copy.deepcopy(by_id(sl, i)._element) for i in v[1]] for k, v in ind.items()}
            old = {k: [by_id(sl, i).top for i in v[1]] for k, v in ind.items()}
            for v in ind.values():
                for i in v[1]:
                    e = by_id(sl, i)._element; e.getparent().remove(e)
            for n, c in enumerate(cards):
                if n < len(s["items"]):
                    it = s["items"][n]; st = it.get("status", "done")
                    set_text(by_id(sl, c), it["text"])
                    for e, ot in zip(originals[st], old[st]):
                        e2 = copy.deepcopy(e); sl.shapes._spTree.append(e2)
                        shp = sl.shapes[-1]; shp.top = tops[c] + (ot - tops[ind[st][0]])
                else:
                    e = by_id(sl, c)._element; e.getparent().remove(e)

        elif kind == "table":
            gf = [sh for sh in sl.shapes if sh.has_table][0]; tbl = gf.table
            hdr, rows = s["headers"], s["rows"]
            ncols = len(tbl.columns)
            # drop extra columns (from the left of an RTL table = last ones in XML order)
            while ncols > len(hdr):
                tbl._tbl.tblGrid.remove(tbl._tbl.tblGrid.gridCol_lst[-1])
                for tr in tbl._tbl.tr_lst:
                    tr.remove(tr.tc_lst[-1])
                ncols -= 1
            trs = tbl._tbl.tr_lst
            body_tpl = [copy.deepcopy(trs[1]), copy.deepcopy(trs[2])]  # plain + zebra
            for tr in trs[1:]:
                tbl._tbl.remove(tr)
            for k in range(len(rows)):
                tbl._tbl.append(copy.deepcopy(body_tpl[k % 2]))
            # RTL: the first JSON column goes to the right-most table column
            for c, h in enumerate(hdr):
                set_text(tbl.cell(0, ncols - 1 - c), h)
            for r, row in enumerate(rows, start=1):
                for c, v in enumerate(row[:ncols]):
                    set_text(tbl.cell(r, ncols - 1 - c), str(v))
            # stretch table to the content width
            gf.left = Inches(0.6); gf.width = Inches(8.8)
            w = int(Inches(8.8) / ncols)
            for col in tbl.columns:
                col.width = w

        elif kind == "kpis":
            items = s["items"][:4]; n = len(items); gap = Inches(0.3)
            w = int((Inches(8.6) - gap * (n - 1)) / n); top = Inches(1.9); h = Inches(2.1)
            for k, it in enumerate(items):
                left = Inches(9.4) - (k + 1) * w - k * gap  # RTL: first item on the right
                card = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
                card.adjustments[0] = 0.12; card.fill.solid(); card.fill.fore_color.rgb = WHITE; card.line.fill.background()
                tf = card.text_frame; tf.clear(); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                para(tf, it["value"], 40, LILAC, bold=True, align=PP_ALIGN.CENTER, first=True)
                para(tf, it["label"], 14, GREY, align=PP_ALIGN.CENTER)

        elif kind == "chart":
            cd = CategoryChartData(); cd.categories = s["categories"]
            for se in s["series"]:
                cd.add_series(se["name"], se["values"])
            gf = sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.8), Inches(1.6), Inches(8.4), Inches(3.4), cd)
            ch = gf.chart; ch.font.name = FONT; ch.font.size = Pt(12); ch.font.color.rgb = GREY
            palette = [LILAC, ORANGE, TEAL, PURPLE]
            for k, ser in enumerate(ch.plots[0].series):
                ser.format.fill.solid(); ser.format.fill.fore_color.rgb = palette[k % 4]
            ch.plots[0].gap_width = 80
            ch.has_legend = len(s["series"]) > 1
            if ch.has_legend:
                ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False
            ch.value_axis.has_major_gridlines = True
            ch.value_axis.major_gridlines.format.line.color.rgb = RGBColor(0xD9, 0xD9, 0xD9)

        elif kind == "image":
            # Images in presentations ALWAYS get rounded corners (never sharp).
            # Optional "backdrop": a rounded square in a brand colour, offset behind the photo.
            box_w, box_h, top = Inches(7.6), Inches(3.0), Inches(1.65)
            pic = sl.shapes.add_picture(s["image"], 0, top, height=box_h)
            if pic.width > box_w:
                ratio = box_w / pic.width; pic.width = box_w; pic.height = int(pic.height * ratio)
            pic.left = int((prs.slide_width - pic.width) / 2)
            round_picture(pic, s.get("radius", 0.08))
            bd = s.get("backdrop")
            if bd:
                col = BACKDROPS.get(bd if isinstance(bd, str) else "lilac", BACKDROPS["lilac"])
                off = Inches(0.18)
                back = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, pic.left - off, pic.top + off, pic.width, pic.height)
                back.adjustments[0] = s.get("radius", 0.08)
                back.fill.solid(); back.fill.fore_color.rgb = col; back.line.fill.background()
                st = back._element.find(qn("p:style"))
                if st is not None: back._element.remove(st)
                tree = sl.shapes._spTree; tree.remove(back._element); tree.insert(tree.index(pic._element), back._element)
            if s.get("caption"):
                tb = sl.shapes.add_textbox(Inches(0.8), Inches(4.8), Inches(8.4), Inches(0.35))
                para(tb.text_frame, s["caption"], 11, GREY, align=PP_ALIGN.CENTER, first=True)

        elif kind == "bullets":
            tb = sl.shapes.add_textbox(Inches(0.9), Inches(1.6), Inches(8.4), Inches(3.4)); tf = tb.text_frame; tf.word_wrap = True
            for k, txt in enumerate(s["items"]):
                p = para(tf, "▪  " + txt, 16, DARK, first=(k == 0)); p.space_after = Pt(10)

    # drop the 8 template slides
    sldIdLst = prs.slides._sldIdLst
    for sid in list(sldIdLst)[:len(tpl)]:
        prs.part.drop_rel(sid.rId); sldIdLst.remove(sid)
    prs.save(out)
    print("saved", out, "slides:", len(prs.slides))


if __name__ == "__main__":
    build(sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3])
