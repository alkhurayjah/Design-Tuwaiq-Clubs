#!/usr/bin/env bash
# Rebuild templates/pptx/presentation-template.pptx from the package assets.
# Needs: node + pptxgenjs (npm i pptxgenjs jszip), python3 + python-pptx + pillow, rsvg-convert.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"; IMG="$HERE/img"; mkdir -p "$IMG"; cd "$IMG"
rsvg-convert -h 300 "$ROOT/assets/logos/club/tuwaiq-club-color-no-tagline.svg" -o club-color.png
rsvg-convert -h 300 "$ROOT/assets/logos/club/tuwaiq-club-white-no-tagline.svg" -o club-white.png
rsvg-convert -h 300 "$ROOT/assets/logos/academy/tuwaiq-academy-horizontal-color.svg" -o academy-color.png
rsvg-convert -h 300 "$ROOT/assets/logos/academy/tuwaiq-academy-horizontal-white.svg" -o academy-white.png
rsvg-convert -h 600 "$ROOT/assets/pixels/svg/club-mark-3color.svg" -o mark.png
for i in bulb calendar clock laptop location person; do
  rsvg-convert -w 256 "$ROOT/assets/icons/academy/white/$i.svg" -o "ic-$i-w.png"
  rsvg-convert -w 256 "$ROOT/assets/icons/academy/purple/$i.svg" -o "ic-$i-p.png"
done
python3 - "$ROOT" <<'PY'
import sys; from PIL import Image
R=sys.argv[1]
for s,d in [('campus/ksu.jpg','photo-cover.jpg'),('campus/qassim.jpg','photo-1.jpg'),('campus/jeddah.jpg','photo-2.jpg'),('campus/upm.jpg','photo-3.jpg'),('campus/kfupm.jpg','photo-4.jpg'),('events/tuwaiq-clubs-awards-ceremony.jpg','photo-event.jpg')]:
    im=Image.open(f'{R}/assets/photos/{s}').convert('RGB'); im.thumbnail((1920,1920)); im.save(d,quality=85)
PY
cd "$HERE"
node build.js "$IMG" raw.pptx
python3 post.py raw.pptx "$ROOT/templates/pptx/presentation-template.pptx"
rm -f raw.pptx; echo "done -> templates/pptx/presentation-template.pptx"
