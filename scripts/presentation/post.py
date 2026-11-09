import sys
from pptx import Presentation
from pptx.oxml.ns import qn
from lxml import etree
src,dst=sys.argv[1],sys.argv[2]
p=Presentation(src); n=0
for sl in p.slides:
    for sh in sl.shapes:
        if sh.shape_type==13 and sh.name.startswith('photo-'):
            sp=sh._element.spPr; g=sp.find(qn('a:prstGeom'))
            g.set('prst','roundRect'); av=g.find(qn('a:avLst'))
            if av is None: av=etree.SubElement(g,qn('a:avLst'))
            for c in list(av): av.remove(c)
            gd=etree.SubElement(av,qn('a:gd')); gd.set('name','adj'); gd.set('fmla','val 8000'); n+=1
A=qn('a:pPr')
for sl in p.slides:
    for el in sl._element.iter(A):
        if el.get('algn')=='r':
            el.set('rtl','1')
            if el.get('marL') and el.find(qn('a:buChar')) is not None or (el.get('marL') and el.get('indent','0').startswith('-')):
                el.set('marR',el.get('marL')); el.attrib.pop('marL')
p.save(dst); print('rounded',n)
import zipfile,shutil,os
tmp=dst+'.tmp'
with zipfile.ZipFile(dst) as zi, zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        d=zi.read(it.filename)
        if it.filename=='[Content_Types].xml' and b'Extension="jpg"' not in d:
            d=d.replace(b'<Default Extension="xml"',b'<Default Extension="jpg" ContentType="image/jpeg"/><Default Extension="xml"',1)
        zo.writestr(it,d)
os.replace(tmp,dst); print('ct fixed')
