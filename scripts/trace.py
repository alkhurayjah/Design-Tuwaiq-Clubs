import sys, numpy as np, potrace
from PIL import Image
def mask_from(path, mode, color=None, tol=60):
    im = np.array(Image.open(path).convert('RGBA')).astype(int)
    a = im[...,3] > 128
    if mode == 'alpha': return a
    d = np.abs(im[...,:3] - np.array(color)).sum(-1)
    return a & (d < tol)
def trace(mask, alphamax=0.6):
    bm = potrace.Bitmap(~mask)
    pl = bm.trace(turdsize=8, alphamax=alphamax, opticurve=True, opttolerance=0.3)
    out = []
    f = lambda p: f"{p.x:.1f} {p.y:.1f}" if hasattr(p,'x') else f"{p[0]:.1f} {p[1]:.1f}"
    for c in pl:
        out.append("M" + f(c.start_point))
        for s in c.segments:
            if s.is_corner: out.append("L" + f(s.c) + "L" + f(s.end_point))
            else: out.append("C" + f(s.c1) + " " + f(s.c2) + " " + f(s.end_point))
        out.append("Z")
    return "".join(out)
def bbox(mask):
    ys, xs = np.where(mask); return xs.min(), ys.min(), xs.max()+1, ys.max()+1
