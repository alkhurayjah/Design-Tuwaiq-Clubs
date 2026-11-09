"""يجهّز مجلد claude-setup/ للرفع على claude.ai:
  - skills/<name>.zip : المهارات الأربع، كل وحدة ZIP جاهزة لـ Customize > Skills
  - Tuwaiq_Clubs_Lite.zip : نسخة خفيفة من الحزمة (بدون المراجع والمعاينات وPNG المكررة) ترفق في المحادثة
usage: python3 scripts/build_claude_setup.py"""
import os, zipfile, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'claude-setup'); os.makedirs(os.path.join(OUT, 'skills'), exist_ok=True)
for d in sorted(glob.glob(os.path.join(ROOT, 'skills/*/'))):
    name = os.path.basename(d.rstrip('/'))
    with zipfile.ZipFile(os.path.join(OUT, 'skills', name + '.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for f in glob.glob(d + '**/*', recursive=True):
            if os.path.isfile(f): z.write(f, os.path.join(name, os.path.relpath(f, d)))
    print('skill', name)
SKIP_DIRS = ('references', 'docs', 'templates/previews', 'claude-setup', '.git', '.github', 'scripts/presentation/img')
SKIP_FILES = ('README.pdf', 'index.html', '.DS_Store')
lite = os.path.join(OUT, 'Tuwaiq_Clubs_Lite.zip'); n = 0
with zipfile.ZipFile(lite, 'w', zipfile.ZIP_DEFLATED) as z:
    for dp, dn, fn in os.walk(ROOT):
        r = os.path.relpath(dp, ROOT)
        if any(r == s or r.startswith(s + os.sep) for s in SKIP_DIRS) or '__pycache__' in r: continue
        for x in fn:
            p = os.path.join(dp, x)
            if x in SKIP_FILES: continue
            if x.endswith('.png') and dp.startswith(os.path.join(ROOT, 'assets/logos')) and os.path.exists(p[:-4] + '.svg'): continue
            if x.endswith('-example.pptx'): continue
            z.write(p, os.path.join('Tuwaiq_Clubs_Claude_Design', os.path.relpath(p, ROOT))); n += 1
print(f'lite: {n} files, {os.path.getsize(lite)/2**20:.1f} MB')
