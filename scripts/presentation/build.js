// Tuwaiq Clubs — general presentation template (16:9, RTL Arabic)
// node build.js <img-dir> <out.pptx>
const pptxgen = require("pptxgenjs");
const path = require("path");
const IMG = process.argv[2] || path.join(__dirname, "img");
const OUT = process.argv[3] || "tuwaiq-clubs-presentation-template.pptx";
const I = (f) => path.join(IMG, f);

const THEME = {
  name: "Tuwaiq Clubs",
  headFontFace: "IBM Plex Sans Arabic",
  bodyFontFace: "IBM Plex Sans Arabic",
  colors: {
    dk1: "262626", lt1: "FFFFFF", dk2: "1F0F45", lt2: "EDEDED",
    accent1: "4F29B7", accent2: "57E3D8", accent3: "A380FF", accent4: "F4A664",
    accent5: "9C75FF", accent6: "80D883", hlink: "4F29B7", folHlink: "A380FF",
  },
};
const COL = { purple: "4F29B7", deep: "1F0F45", teal: "57E3D8", lilac: "A380FF", lilac2: "9C75FF", orange: "F4A664", ink: "262626", grey: "EDEDED", mute: "6B6B6B", white: "FFFFFF" };
const FONT = THEME.headFontFace;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
pres.rtlMode = true;
pres.title = "Tuwaiq Clubs — Presentation template";
pres.author = "Tuwaiq Clubs";
pres.company = "Tuwaiq Academy";
const W = 13.333, H = 7.5;

// ---------- helpers ----------
const px = (s, x, y, size, color, name) =>
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: size, h: size, rectRadius: size * 0.15, fill: { color }, line: { type: "none" }, objectName: name || "pixel" });
const logos = (s, dark) => {
  // club | academy lockup, top-left like the official report template
  s.addImage({ path: I(dark ? "club-white.png" : "club-color.png"), x: 0.55, y: 0.38, w: 0.82, h: 0.82 * 300 / 521, objectName: "logo-club" });
  s.addShape(pres.shapes.LINE, { x: 1.52, y: 0.38, w: 0, h: 0.48, line: { color: dark ? "FFFFFF" : "BDBDBD", width: 1 } });
  s.addImage({ path: I(dark ? "academy-white.png" : "academy-color.png"), x: 1.67, y: 0.46, w: 1.6, h: 1.6 * 300 / 1480, objectName: "logo-academy" });
};
const T = (opts) => Object.assign({ fontFace: FONT, rtlMode: true, align: "right", isTextBox: true, margin: 0 }, opts);

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "TC_CONTENT",
  background: { color: COL.grey },
  objects: [
    { rect: { x: 0, y: H - 0.09, w: W, h: 0.09, fill: { color: COL.lilac2 } } },
    { image: { path: I("club-color.png"), x: 0.55, y: 0.38, w: 0.82, h: 0.82 * 300 / 521 } },
    { line: { x: 1.52, y: 0.38, w: 0, h: 0.48, line: { color: "BDBDBD", width: 1 } } },
    { image: { path: I("academy-color.png"), x: 1.67, y: 0.46, w: 1.6, h: 1.6 * 300 / 1480 } },
    { placeholder: { options: { name: "title", type: "title", x: 4.0, y: 0.95, w: 8.78, h: 0.8, fontFace: FONT, fontSize: 34, bold: true, color: COL.purple, align: "right", rtlMode: true, valign: "middle", margin: 0 }, text: "[عنوان الشريحة]" } },
    { placeholder: { options: { name: "kicker", type: "body", x: 6.8, y: 0.42, w: 5.98, h: 0.4, fontFace: FONT, fontSize: 13, color: "D9894A", align: "right", rtlMode: true, margin: 0 }, text: "نادي طويق – [الجامعة] | [اسم العرض]" } },
  ],
  slideNumber: { x: 0.55, y: H - 0.55, w: 0.6, h: 0.3, fontFace: FONT, fontSize: 11, color: "8A8A8A", align: "left" },
});
pres.defineSlideMaster({
  title: "TC_DARK",
  background: { color: COL.deep },
  objects: [
    { image: { path: I("club-white.png"), x: 0.55, y: 0.38, w: 0.82, h: 0.82 * 300 / 521 } },
    { line: { x: 1.52, y: 0.38, w: 0, h: 0.48, line: { color: "FFFFFF", width: 1 } } },
    { image: { path: I("academy-white.png"), x: 1.67, y: 0.46, w: 1.6, h: 1.6 * 300 / 1480 } },
  ],
  slideNumber: { x: 0.55, y: H - 0.55, w: 0.6, h: 0.3, fontFace: FONT, fontSize: 11, color: "B9AEE6", align: "left" },
});
pres.defineSlideMaster({ title: "TC_SECTION", background: { color: COL.purple }, objects: [] });
pres.defineSlideMaster({ title: "TC_BLANK", background: { color: COL.grey }, objects: [] });

// ---------- 1. cover ----------
pres.addSection({ title: "الغلاف" });
let s = pres.addSlide({ masterName: "TC_BLANK", sectionTitle: "الغلاف" });
s.addImage({ path: I("photo-cover.jpg"), x: 0, y: 0, w: W, h: H, sizing: { type: "cover", w: W, h: H }, objectName: "cover-photo" });
s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: H, fill: { color: COL.purple, transparency: 28 }, line: { type: "none" }, objectName: "cover-overlay" });
s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: W, h: H, fill: { color: COL.deep, transparency: 55 }, line: { type: "none" }, objectName: "cover-shade" });
s.addImage({ path: I("club-white.png"), x: W - 0.55 - 1.3, y: 0.45, w: 1.3, h: 1.3 * 300 / 521, objectName: "logo-club" });
s.addImage({ path: I("academy-white.png"), x: W - 0.55 - 1.3 - 0.25 - 2.3, y: 0.58, w: 2.3, h: 2.3 * 300 / 1480, objectName: "logo-academy" });
s.addShape(pres.shapes.LINE, { x: W - 0.55 - 1.3 - 0.13, y: 0.5, w: 0, h: 0.65, line: { color: "FFFFFF", width: 1 } });
s.addText("[عنوان العرض التقديمي]", T({ x: 3.2, y: 2.65, w: 9.58, h: 1.2, fontSize: 48, bold: true, color: COL.white, valign: "middle", objectName: "cover-title" }));
s.addText("[سطر فرعي يوضح موضوع العرض]", T({ x: 3.2, y: 3.85, w: 9.58, h: 0.6, fontSize: 22, color: COL.orange, objectName: "cover-subtitle" }));
s.addText("نادي طويق في [الجامعة]  |  [00 شهر 2026م]", T({ x: 3.2, y: 4.6, w: 9.58, h: 0.45, fontSize: 16, color: "E6E0FA", objectName: "cover-meta" }));
s.addImage({ path: I("mark.png"), x: -0.35, y: H - 1.9, w: 1.6 * 400 / 600, h: 1.6, objectName: "pixel-mark" });
px(s, 1.2, 0.55, 0.14, COL.teal); px(s, 2.0, 1.15, 0.09, COL.lilac);
s.addNotes("الغلاف: بدّل صورة الحرم (كليك يمين > تغيير الصورة) واحتفظ بالطبقة البنفسجية. العنوان سطر أو سطرين بحد أقصى.");

// ---------- 2. agenda ----------
pres.addSection({ title: "المحتوى" });
s = pres.addSlide({ masterName: "TC_CONTENT", sectionTitle: "المحتوى" });
s.addText("محـاور العرض", { placeholder: "title" });
s.addText("نادي طويق – [الجامعة] | [اسم العرض]", { placeholder: "kicker" });
const agenda = ["[المحور الأول]", "[المحور الثاني]", "[المحور الثالث]", "[المحور الرابع]"];
agenda.forEach((t, i) => {
  const y = 2.05 + i * 1.12;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 4.6, y, w: 8.18, h: 0.9, rectRadius: 0.16, fill: { color: COL.white }, line: { type: "none" }, objectName: `agenda-card-${i + 1}` });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 11.98, y: y + 0.15, w: 0.6, h: 0.6, rectRadius: 0.09, fill: { color: i === 0 ? COL.purple : COL.lilac }, line: { type: "none" }, objectName: `agenda-num-bg-${i + 1}` });
  s.addText(String(i + 1).padStart(2, "0"), T({ x: 11.98, y: y + 0.15, w: 0.6, h: 0.6, fontSize: 18, bold: true, color: COL.white, align: "center", valign: "middle", rtlMode: false, objectName: `agenda-num-${i + 1}` }));
  s.addText(t, T({ x: 5.0, y, w: 6.7, h: 0.9, fontSize: 20, bold: i === 0, color: COL.ink, valign: "middle", objectName: `agenda-text-${i + 1}` }));
});
s.addImage({ path: I("photo-1.jpg"), x: 0.55, y: 2.05, w: 3.55, h: 4.26, sizing: { type: "cover", w: 3.55, h: 4.26 }, objectName: "photo-agenda" });
s.addNotes("المحاور: 3 إلى 5 بنود قصيرة. المحور الحالي بلون بنفسجي غامق.");

// ---------- 3. section divider ----------
s = pres.addSlide({ masterName: "TC_SECTION", sectionTitle: "المحتوى" });
s.addText("01", T({ x: 6.5, y: 1.7, w: 6.28, h: 1.6, fontSize: 96, bold: true, color: COL.teal, rtlMode: false, objectName: "section-number" }));
s.addText("[عنوان القسم]", T({ x: 3.0, y: 3.35, w: 9.78, h: 1.0, fontSize: 44, bold: true, color: COL.white, objectName: "section-title" }));
s.addText("[سطر يشرح ما يغطيه هذا القسم]", T({ x: 3.0, y: 4.35, w: 9.78, h: 0.6, fontSize: 20, color: "D9CEF5", objectName: "section-sub" }));
s.addImage({ path: I("club-white.png"), x: 0.55, y: 0.45, w: 1.0, h: 1.0 * 300 / 521, objectName: "logo-club" });
s.addImage({ path: I("mark.png"), x: -0.3, y: H - 2.2, w: 1.9 * 400 / 600, h: 1.9, objectName: "pixel-mark" });
px(s, 12.2, 0.6, 0.14, COL.orange); px(s, 11.6, 6.6, 0.1, COL.teal);

// ---------- 4. text + image ----------
s = pres.addSlide({ masterName: "TC_CONTENT", sectionTitle: "المحتوى" });
s.addText("[عنوان: فكرة واحدة]", { placeholder: "title" });
s.addText("نادي طويق – [الجامعة] | [اسم العرض]", { placeholder: "kicker" });
s.addText([
  { text: "[النقطة الأولى: جملة قصيرة وواضحة]", options: { bullet: { indent: 18 }, breakLine: true } },
  { text: "[النقطة الثانية: رقم أو نتيجة حقيقية]", options: { bullet: { indent: 18 }, breakLine: true } },
  { text: "[النقطة الثالثة: ما الخطوة التالية]", options: { bullet: { indent: 18 } } },
], T({ x: 6.75, y: 2.15, w: 6.03, h: 3.6, fontSize: 20, color: COL.ink, paraSpaceAfter: 14, valign: "top", objectName: "body-points" }));
// rounded image + rounded backdrop square (offset down-left), identity rule
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.75, y: 2.35, w: 5.4, h: 3.6, rectRadius: 0.29, fill: { color: COL.lilac2 }, line: { type: "none" }, objectName: "photo-backdrop" });
s.addImage({ path: I("photo-2.jpg"), x: 0.95, y: 2.15, w: 5.4, h: 3.6, sizing: { type: "cover", w: 5.4, h: 3.6 }, objectName: "photo-main" });
s.addText("[وصف الصورة]", T({ x: 0.95, y: 5.98, w: 5.4, h: 0.35, fontSize: 12, color: COL.mute, align: "center", objectName: "photo-caption" }));
s.addNotes("قاعدة الهوية: الصور بزوايا دائرية (8% من الضلع الأقصر)، والمربع الخلفي بنفس الحجم مزاح للأسفل واليسار بلا ظل.");

// ---------- 5. three cards ----------
s = pres.addSlide({ masterName: "TC_CONTENT", sectionTitle: "المحتوى" });
s.addText("[ثلاث نقاط رئيسية]", { placeholder: "title" });
s.addText("نادي طويق – [الجامعة] | [اسم العرض]", { placeholder: "kicker" });
[["bulb", "[العنوان الأول]", "[سطران يشرحان الفكرة بلغة بسيطة وواقعية.]"],
 ["laptop", "[العنوان الثاني]", "[سطران يشرحان الفكرة بلغة بسيطة وواقعية.]"],
 ["person", "[العنوان الثالث]", "[سطران يشرحان الفكرة بلغة بسيطة وواقعية.]"]].forEach(([ic, h, b], i) => {
  const x = 12.78 - (i + 1) * 3.95 + 0.25;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.15, w: 3.7, h: 3.4, rectRadius: 0.2, fill: { color: COL.white }, line: { type: "none" }, objectName: `card-${i + 1}` });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x + 3.7 - 0.35 - 0.85, y: 2.5, w: 0.85, h: 0.85, rectRadius: 0.13, fill: { color: i === 0 ? COL.purple : COL.lilac }, line: { type: "none" }, objectName: `card-icon-bg-${i + 1}` });
  s.addImage({ path: I(`ic-${ic}-w.png`), x: x + 3.7 - 0.35 - 0.85 + 0.19, y: 2.69, w: 0.47, h: 0.47, objectName: `card-icon-${i + 1}` });
  s.addText(h, T({ x: x + 0.35, y: 3.6, w: 3.0, h: 0.55, fontSize: 21, bold: true, color: COL.ink, objectName: `card-title-${i + 1}` }));
  s.addText(b, T({ x: x + 0.35, y: 4.2, w: 3.0, h: 1.5, fontSize: 15, color: "4A4A4A", valign: "top", objectName: `card-body-${i + 1}` }));
});

// ---------- 6. stats ----------
s = pres.addSlide({ masterName: "TC_CONTENT", sectionTitle: "المحتوى" });
s.addText("[الأرقام بإيجاز]", { placeholder: "title" });
s.addText("نادي طويق – [الجامعة] | [اسم العرض]", { placeholder: "kicker" });
[["[0]", "فعالية منفذة"], ["[0]", "مستفيد"], ["[0]", "ساعة تدريبية"], ["[0]", "شراكة"]].forEach(([n, l], i) => {
  const x = 12.78 - (i + 1) * 2.98 + 0.18;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.4, w: 2.8, h: 2.7, rectRadius: 0.22, fill: { color: i === 0 ? COL.purple : COL.white }, line: { type: "none" }, objectName: `stat-card-${i + 1}` });
  s.addText(n, T({ x, y: 2.85, w: 2.8, h: 1.2, fontSize: 60, bold: true, color: i === 0 ? COL.white : COL.purple, align: "center", rtlMode: false, objectName: `stat-number-${i + 1}` }));
  s.addText(l, T({ x, y: 4.1, w: 2.8, h: 0.5, fontSize: 18, color: i === 0 ? "E6E0FA" : "4A4A4A", align: "center", objectName: `stat-label-${i + 1}` }));
});
s.addText("[سطر يفسّر الأرقام أو يقارنها بالفترة السابقة]", T({ x: 0.55, y: 5.55, w: 12.23, h: 0.5, fontSize: 16, color: COL.mute, align: "center", objectName: "stat-note" }));
px(s, 0.55, 2.0, 0.12, COL.teal);

// ---------- 7. chart ----------
s = pres.addSlide({ masterName: "TC_CONTENT", sectionTitle: "المحتوى" });
s.addText("[عنوان الرسم: النتيجة في جملة]", { placeholder: "title" });
s.addText("نادي طويق – [الجامعة] | [اسم العرض]", { placeholder: "kicker" });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.55, y: 2.05, w: 7.6, h: 4.5, rectRadius: 0.2, fill: { color: COL.white }, line: { type: "none" }, objectName: "chart-card" });
s.addChart(pres.charts.BAR, [{ name: "[المؤشر]", labels: ["شهر 1", "شهر 2", "شهر 3", "شهر 4", "شهر 5"], values: [12, 18, 15, 24, 30] }], {
  x: 0.8, y: 2.25, w: 7.1, h: 4.1, barDir: "col", catAxisOrientation: "maxMin", chartColors: [COL.purple], showValue: true, dataLabelPosition: "outEnd", dataLabelColor: COL.ink, dataLabelFontSize: 12, dataLabelFontFace: "+mn-lt",
  catAxisLabelColor: "6B6B6B", catAxisLabelFontSize: 12, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
  showLegend: false, showTitle: false, barGapWidthPct: 60, objectName: "chart-main",
});
[["[استنتاج أول من الرسم]", COL.purple], ["[استنتاج ثانٍ]", COL.lilac], ["[ما الذي سنفعله بناءً عليه]", COL.orange]].forEach(([t, c], i) => {
  const y = 2.25 + i * 1.4;
  px(s, 12.43, y + 0.12, 0.3, c, `takeaway-dot-${i + 1}`);
  s.addText(t, T({ x: 8.6, y, w: 3.65, h: 1.1, fontSize: 17, color: COL.ink, valign: "top", objectName: `takeaway-${i + 1}` }));
});
s.addNotes("الرسم أصلي في PowerPoint: كليك يمين > تعديل البيانات. الأرقام هنا مثال فقط، استبدلها بأرقام حقيقية.");

// ---------- 8. timeline ----------
s = pres.addSlide({ masterName: "TC_CONTENT", sectionTitle: "المحتوى" });
s.addText("[المراحل أو الخطة الزمنية]", { placeholder: "title" });
s.addText("نادي طويق – [الجامعة] | [اسم العرض]", { placeholder: "kicker" });
s.addShape(pres.shapes.LINE, { x: 1.925, y: 3.35, w: 9.48, h: 0, line: { color: "C9BDF0", width: 2, dashType: "dash" } });
const steps = [["[المرحلة 1]", "[الشهر]", "[ماذا يحدث]"], ["[المرحلة 2]", "[الشهر]", "[ماذا يحدث]"], ["[المرحلة 3]", "[الشهر]", "[ماذا يحدث]"], ["[المرحلة 4]", "[الشهر]", "[ماذا يحدث]"]];
steps.forEach(([h, d, b], i) => {
  const cx = 11.405 - i * 3.16;
  const c = [COL.purple, COL.lilac, COL.teal, COL.orange][i];
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx - 0.32, y: 3.03, w: 0.64, h: 0.64, rectRadius: 0.1, fill: { color: c }, line: { type: "none" }, objectName: `step-marker-${i + 1}` });
  s.addText(String(i + 1), T({ x: cx - 0.32, y: 3.03, w: 0.64, h: 0.64, fontSize: 18, bold: true, color: i >= 2 ? COL.deep : COL.white, align: "center", valign: "middle", rtlMode: false, objectName: `step-num-${i + 1}` }));
  s.addText(d, T({ x: cx - 1.375, y: 2.25, w: 2.75, h: 0.5, fontSize: 14, color: "D9894A", align: "center", objectName: `step-date-${i + 1}` }));
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx - 1.375, y: 4.0, w: 2.75, h: 2.1, rectRadius: 0.18, fill: { color: COL.white }, line: { type: "none" }, objectName: `step-card-${i + 1}` });
  s.addText(h, T({ x: cx - 1.2, y: 4.2, w: 2.4, h: 0.5, fontSize: 18, bold: true, color: COL.ink, align: "center", objectName: `step-title-${i + 1}` }));
  s.addText(b, T({ x: cx - 1.2, y: 4.75, w: 2.4, h: 1.1, fontSize: 14, color: "4A4A4A", align: "center", valign: "top", objectName: `step-body-${i + 1}` }));
});

// ---------- 9. table ----------
s = pres.addSlide({ masterName: "TC_CONTENT", sectionTitle: "المحتوى" });
s.addText("[جدول: الفعاليات أو المقارنة]", { placeholder: "title" });
s.addText("نادي طويق – [الجامعة] | [اسم العرض]", { placeholder: "kicker" });
const hdr = (t) => ({ text: t, options: { bold: true, color: COL.white, fill: { color: COL.purple }, fontSize: 15, align: "center", valign: "middle", rtlMode: true, fontFace: FONT } });
const cell = (t, alt) => ({ text: t, options: { color: COL.ink, fill: { color: alt ? "F6F3FE" : COL.white }, fontSize: 14, align: "center", valign: "middle", rtlMode: true, fontFace: FONT } });
const rows = [[hdr("الحضور"), hdr("النوع"), hdr("التاريخ"), hdr("الفعالية")]];
for (let r = 0; r < 5; r++) rows.push([cell("[0]", r % 2), cell("[ورشة / لقاء]", r % 2), cell("[00/00]", r % 2), cell(`[اسم الفعالية ${r + 1}]`, r % 2)]);
s.addTable(rows, { x: 0.55, y: 2.1, w: 12.23, colW: [2.2, 2.6, 2.4, 5.03], rowH: 0.62, border: { type: "solid", color: "E3DDF5", pt: 1 }, objectName: "table-main" });
s.addNotes("الجدول بترتيب من اليمين لليسار: العمود الأول (الفعالية) على اليمين.");

// ---------- 10. key message ----------
s = pres.addSlide({ masterName: "TC_DARK", sectionTitle: "المحتوى" });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 11.85, y: 1.85, w: 0.9, h: 0.9, rectRadius: 0.135, fill: { color: COL.teal }, line: { type: "none" }, objectName: "quote-mark-bg" });
s.addText("”", T({ x: 11.85, y: 1.85, w: 0.9, h: 0.9, fontSize: 54, bold: true, color: COL.deep, align: "center", valign: "middle", rtlMode: false, objectName: "quote-mark" }));
s.addText("[رسالة رئيسية أو اقتباس قصير يلخّص العرض في سطرين]", T({ x: 2.2, y: 2.9, w: 10.55, h: 1.9, fontSize: 38, bold: true, color: COL.white, valign: "top", objectName: "quote-text" }));
s.addText("— [صاحب الاقتباس، صفته]", T({ x: 2.2, y: 4.95, w: 10.55, h: 0.5, fontSize: 18, color: COL.lilac, objectName: "quote-author" }));
s.addImage({ path: I("mark.png"), x: -0.3, y: H - 1.9, w: 1.6 * 400 / 600, h: 1.6, objectName: "pixel-mark" });

// ---------- 11. image grid ----------
s = pres.addSlide({ masterName: "TC_CONTENT", sectionTitle: "المحتوى" });
s.addText("[من فعالياتنا]", { placeholder: "title" });
s.addText("نادي طويق – [الجامعة] | [اسم العرض]", { placeholder: "kicker" });
[["photo-event.jpg", "[وصف الصورة الأولى]"], ["photo-3.jpg", "[وصف الصورة الثانية]"], ["photo-4.jpg", "[وصف الصورة الثالثة]"]].forEach(([f, c], i) => {
  const x = 12.78 - (i + 1) * 4.0 + 0.2;
  s.addImage({ path: I(f), x, y: 2.15, w: 3.8, h: 3.4, sizing: { type: "cover", w: 3.8, h: 3.4 }, objectName: `photo-grid-${i + 1}` });
  s.addText(c, T({ x, y: 5.68, w: 3.8, h: 0.4, fontSize: 14, color: COL.mute, align: "center", objectName: `photo-grid-caption-${i + 1}` }));
});
s.addNotes("صور جماعية عامة فقط، ولا صور فردية واضحة بلا موافقة.");

// ---------- 12. event / call to action ----------
s = pres.addSlide({ masterName: "TC_CONTENT", sectionTitle: "المحتوى" });
s.addText("[الفعالية القادمة]", { placeholder: "title" });
s.addText("نادي طويق – [الجامعة] | [اسم العرض]", { placeholder: "kicker" });
s.addText("[اسم الفعالية في سطر واحد]", T({ x: 3.6, y: 2.2, w: 9.18, h: 0.8, fontSize: 32, bold: true, color: COL.ink, objectName: "event-title" }));
s.addText("[سطران عن الفعالية: لمن هي، وماذا سيتعلم الحاضر.]", T({ x: 3.6, y: 3.05, w: 9.18, h: 0.9, fontSize: 18, color: "4A4A4A", valign: "top", objectName: "event-desc" }));
const pill = (x, w, icon, text, color, name) => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.35, w, h: 0.62, rectRadius: 0.31, fill: { color: COL.white }, line: { color, width: 1.5 }, objectName: name });
  s.addImage({ path: I(icon), x: x + w - 0.5, y: 4.5, w: 0.32, h: 0.32 });
  s.addText(text, T({ x: x + 0.2, y: 4.35, w: w - 0.8, h: 0.62, fontSize: 15, color, valign: "middle", objectName: name + "-text" }));
};
pill(9.98, 2.8, "ic-calendar-p.png", "[00 شهر 2026م]", "D9894A", "pill-date");
pill(7.0, 2.8, "ic-clock-p.png", "[4:00 – 5:00 م]", COL.purple, "pill-time");
pill(4.02, 2.8, "ic-location-p.png", "[المكان أو عن بُعد]", "1FB5AB", "pill-place");
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.75, y: 2.2, w: 2.5, h: 2.5, rectRadius: 0.2, fill: { color: COL.white }, line: { color: "C9BDF0", width: 1.5, dashType: "dash" }, objectName: "qr-slot" });
s.addText("[رمز QR للتسجيل]", T({ x: 0.75, y: 2.2, w: 2.5, h: 2.5, fontSize: 14, color: COL.mute, align: "center", valign: "middle", objectName: "qr-label" }));
s.addText("سجّل عبر: [الرابط]", T({ x: 0.75, y: 4.85, w: 2.5, h: 0.4, fontSize: 13, color: COL.purple, align: "center", objectName: "qr-link" }));
s.addText("@TuwaiqClubs", T({ x: 3.6, y: 5.6, w: 9.18, h: 0.4, fontSize: 15, color: COL.mute, rtlMode: false, objectName: "handle" }));
px(s, 0.55, 6.3, 0.12, COL.teal);

// ---------- 13. closing (logos only, no text) ----------
pres.addSection({ title: "الختام" });
s = pres.addSlide({ masterName: "TC_BLANK", sectionTitle: "الختام" });
s.addImage({ path: I("club-color.png"), x: W / 2 + 0.35, y: 3.05, w: 2.3, h: 2.3 * 300 / 521, objectName: "logo-club" });
s.addShape(pres.shapes.LINE, { x: W / 2, y: 2.85, w: 0, h: 1.75, line: { color: "BDBDBD", width: 1 } });
s.addImage({ path: I("academy-color.png"), x: W / 2 - 0.35 - 3.6, y: 3.37, w: 3.6, h: 3.6 * 300 / 1480, objectName: "logo-academy" });
s.addImage({ path: I("mark.png"), x: W - 1.15, y: -0.6, w: 2.4 * 400 / 600, h: 2.4, objectName: "pixel-mark" });
s.addImage({ path: I("mark.png"), x: -0.45, y: H - 1.8, w: 2.4 * 400 / 600, h: 2.4, objectName: "pixel-mark-2" });
s.addNotes("الختام: شعارات فقط، بلا أي عبارة (قاعدة الهوية).");

(async () => {
  await pres.writeFile({ fileName: OUT });
  const { applyTheme } = require(process.env.APPLY_THEME || path.join(__dirname, "apply_theme.js"));
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
