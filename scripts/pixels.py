# Recreates the Tuwaiq Pixels Generator geometry (genebranding.github.io/Tuwaiq) as SVG paths.
import sys, json
L, C = 100, 15  # cell size, corner = 0.15*L
def n(v): return f"{v:g}"
def cell_path(cells):
    S = set(cells); out = []
    for (x, y) in cells:
        X, Y = x*L, y*L
        out.append(f"M{n(X)} {n(Y+C)}A{C} {C} 0 0 1 {n(X+C)} {n(Y)}H{n(X+L-C)}A{C} {C} 0 0 1 {n(X+L)} {n(Y+C)}V{n(Y+L-C)}A{C} {C} 0 0 1 {n(X+L-C)} {n(Y+L)}H{n(X+C)}A{C} {C} 0 0 1 {n(X)} {n(Y+L-C)}Z")
        if (x+1, y) in S: out.append(f"M{n(X+L/2)} {n(Y)}h{L}v{L}h{-L}Z")
        if (x, y+1) in S: out.append(f"M{n(X)} {n(Y+L/2)}h{L}v{L}h{-L}Z")
        if (x+1, y+1) in S:
            # same geometry as the generator's drawLink('DR'), traced CLOCKWISE like every other sub-path
            # (opposite winding would punch holes where sub-paths overlap under the non-zero fill rule)
            out.append(f"M{n(X+L-C)} {n(Y+L)}L{n(X+L)} {n(Y+L-C)}A{C} {C} 0 0 0 {n(X+L+C)} {n(Y+L)}L{n(X+L)} {n(Y+L+C)}A{C} {C} 0 0 0 {n(X+L-C)} {n(Y+L)}Z")
        if (x-1, y+1) in S:
            out.append(f"M{n(X+C)} {n(Y+L)}A{C} {C} 0 0 0 {n(X)} {n(Y+L+C)}L{n(X-C)} {n(Y+L)}A{C} {C} 0 0 0 {n(X)} {n(Y+L-C)}Z")
    return "".join(out)
def from_art(art):
    rows = [r for r in art.strip("\n").split("\n")]
    return [(x, y) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch == "#"]
SHAPES = {
 "zigzag":  "#.#.\n.#.#",
 "v":       "#.#\n.#.",
 "diag2":   "#.\n.#",
 "diag3":   "#..\n.#.\n..#",
 "step":    ".##\n#..",
 "hook":    ".#\n.#\n.#\n#.",
 "plus":    ".#.\n###\n.#.",
 "x":       "#.#\n.#.\n#.#",
 "checker": "#.#.#\n.#.#.\n#.#.#",
 "chevron": "#..\n.#.\n..#\n.#.\n#..",
 "lt":      "..#\n.#.\n#..\n.#.\n..#",
 "code":    "..#.....#.#..\n.#.....#...#.\n#.....#.....#\n.#...#.....#.\n..#.#.....#..",
 "stairs":  "#...\n##..\n.##.\n..##",
 "club":    "#.\n.#\n#.",
 "corner":  "####\n#...\n#...",
 "cluster": "##..#\n.#.##\n#....",
 "bar":     "####",
 "dot":     "#",
}

# 20 extra shapes (v2) — exported to assets/pixels with:  python3 scripts/pixels.py --export-extra
EXTRA = {
 "arrow-right":    "..#..\n...#.\n#####\n...#.\n..#..",
 "arrow-up":       "..#..\n.###.\n#.#.#\n..#..\n..#..",
 "arrow-diagonal": "..###\n...##\n..#.#\n.#...\n#....",
 "bracket-left":   "##\n#.\n#.\n#.\n##",
 "bracket-right":  "##\n.#\n.#\n.#\n##",
 "slash":          "..#\n.#.\n#..",
 "terminal":       "#....\n.#...\n#.###",
 "bar-vertical":   "#\n#\n#\n#",
 "ring":           "###\n#.#\n###",
 "l-shape":        "#..\n#..\n###",
 "t-shape":        "###\n.#.\n.#.",
 "z-shape":        "##.\n.##",
 "block":          "##\n##",
 "diamond":        ".#.\n#.#\n.#.",
 "star":           "..#..\n.###.\n#####\n.###.\n..#..",
 "wave":           "#...#...\n.#.#.#.#\n..#...#.",
 "ellipsis":       "#.#.#",
 "dots-grid":      "#.#\n...\n#.#",
 "chart":          "....#\n..#.#\n..#.#\n#.#.#",
 "hash":           ".#.#.\n#####\n.#.#.\n#####\n.#.#.",
}
PALETTE = {"lavender": "#CDB7FF", "lilac": "#9C75FF", "orange": "#F4A664", "purple": "#4F29B7",
           "teal": "#57E3D8", "violet": "#6438DD", "white": "#FFFFFF"}
def export(shapes, root):
    """Write currentColor SVG + 7 palette SVGs per shape and merge into pixels.json."""
    import os
    jp = f"{root}/assets/pixels/pixels.json"; lib = json.load(open(jp, encoding="utf-8"))
    for k, art in shapes.items():
        cells = from_art(art); rows = art.strip("\n").split("\n")
        w, h = max(len(r) for r in rows)*L, len(rows)*L; d = cell_path(cells)
        open(f"{root}/assets/pixels/svg/{k}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><path fill="currentColor" d="{d}"/></svg>')
        for c, hx in PALETTE.items():
            open(f"{root}/assets/pixels/palette/{c}/{k}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><path fill="{hx}" d="{d}"/></svg>')
        lib[k] = {"art": art, "w": w, "h": h, "d": d}
    json.dump(lib, open(jp, "w", encoding="utf-8"), ensure_ascii=False)
    return len(lib)

if __name__ == "__main__":
    if sys.argv[1:] == ["--export-extra"]:
        import os
        print(export(EXTRA, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "shapes in pixels.json"); sys.exit()
    K = sys.argv[1]; lib = {}
    for k, art in SHAPES.items():
        cells = from_art(art); rows = art.strip().split("\n")
        w, h = max(len(r) for r in rows)*L, len(rows)*L
        d = cell_path(cells); lib[k] = {"w": w, "h": h, "d": d, "art": art}
        open(f"{K}/pixels/{k}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><path fill="#4F29B7" d="{d}"/></svg>')
    json.dump(lib, open(f"{K}/pixels/pixels.json", "w"))
    print(len(lib), "shapes")
