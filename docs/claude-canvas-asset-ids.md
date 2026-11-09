# معرفات الأصول داخل لوحة Claude Design "نادي طويق — مكتبة العناصر"
> صالحة فقط داخل تلك اللوحة على claude.ai. خارجها استخدم ملفات assets/.

# Tuwaiq brand notes (from user's guides)

Font: IBM Plex Sans Arabic — Bold titles, Medium subtitles, Regular body.
Primary: #4F29B7 purple (75%), #262626, #EDEDED, #57E3D8 teal (titles on purple).
Club secondary: #57E3D8, #A380FF, #F4A664. Academy adds #4D96FF, #80D883, #FFDB5E, #FF8181.
Purple tints: #6438DD #754BEA #9C75FF #B798FF #CDB7FF #E3D8FF. Light bg #F5F1FF.

## Pixel generator (genebranding.github.io/Tuwaiq) algorithm
- Square grid, cols = Details (default 15), cell l = width/cols, rows = floor(h/l), centered vertically.
- Filled cell = rounded square, corner radius = 0.15*l. Grid lines #D5CAFF on bg #F5F1FF.
- Neighbours merge: right neighbour filled -> rect(x+l/2, y, l, l); down -> rect(x, y+l/2, l, l)
  (so adjacent cells fuse into one solid shape; only outer corners rounded).
- Diagonal neighbour (DR/DL) filled -> small concave "bridge" between corners: two arcs of radius r
  joining at the shared corner point (the pinched link seen in the CLUB logo squares).
- One colour per drawing (elColor from palette: tints + #57E3D8). Export SVG.

## Kit (local: scratchpad/kit — logos/, icons/icons.json, pixels/pixels.json, scripts/pixels.py)
Canvas url for publishes: https://claude.ai/artifact/6mzUgRdvqJfvFEHq34uJp7 (view: claude.ai/code/artifact/2ec5d73d-bb51-4dd8-9182-a689855d0da0)
Logos: club-color /_blob/45f0ce9e90bce559b5e204fb3163028a · club-white /_blob/327bdaffe0d96f4662f2e604b80a8a9e
 academy-h-color /_blob/464387110fec6d87bbd71185b57d0950 · academy-h-white /_blob/2a416125de67ef5b7b3d5ab73ed070f8
 academy-v-color /_blob/924f2c13e9dd33ab4da51e89f3521925 · academy-v-white /_blob/2c8409806859a2b855e53e3df8e47043
Icons (-p purple / -w white): bulb ca1c6650324b64bb8f671ee28aae8318/9e44071266154d84615d26172ad0059c, calendar 40bbb883a559b344aa9df7f32b0d53fe/a0fb279c772df89cfe208938b3d38422,
 certificate 75bcae3f906ad4e8ea6af62ad1f9afd6/b106a2b946b63bc0c4c5054ad0d05b4d, clock f8ecae6b495118b1489eab3b48580bc3/a07e67d0ad8a9630beee5d0426b0f5a7,
 code 89cd001ec37dbc7387beaf73ae1cd418/198354e3439f1cf1decf0403c4c30a16, cursor 8f2c337f9f4098811ce42324da66757c/ba8e878e3bd8393d9c8722584f07eab4,
 laptop 7675c8b7e9a1bcb3e26bbd7b6564f236/e5b2c454bdf0cb08e7f6dced887b4075, location 184aecf74fd113a7fd15dab6c2861558/f153745c6dcb35eaedc7fdb55cb9b444,
 person 775b5d0c920feb23efa406666a3aef7f/702e272b240f52b02b44bc98129aaf5a, remote e61ae3411379f3dc231c51dced183f90/90da5d8027591d2fbf91ff2aa1117ff0
Pixels (one colour each): bar 860527ea492ad37c1690460c0bf02e7b, checker 19817e352b1278071005fddbfd38d46e, chevron 4af076c94f30d7628c6e63928f6f248e,
 clubmark bdbb9427068965d9f6e919ac02486814, cluster baece7bb7a6fe78ef28cbd241dc3c958, code ecf64817529de19ef2321c3eeda6e64b, corner a5f952e668605b62a923767a747ea4f1,
 diag2 ff9f4db35fcbf43b2b826a52148a6b59, diag3 924b61c2edc6034d107d1c2d80e8c6d3, dot 38c782fd8899e908a02e8792e46d171c, hook 3d6b641d0b81625773e246234812ed05,
 lt 0f0f2f3b72dfb78e9ba1fc6f7983d1d6, plus 4c0230fb70756c6862162eca8b893432, stairs 35f7963e845f3c74eb868dd4cc670401, step 92652e95fe505fc28225851b1e47095e,
 v b57c2fe34f756bc77ccfc28200251fe1, x 850bb2fd29801309f9939a2d68123942, zigzag 2a2609f8d6d51c9230399246b9a30fa0
For recolouring pixels/icons in designs: inline <svg> with path d from the json files.

## From club.tuwaiq.edu.sa (Site.dc.html artboard)
Assets: club-color-notag f0b6597a891cd0c0cdd7fac0faa464f3 · club-white-notag d45c19455d2ddcd8067f759614a9c7e6 · academy-mark 2e448f224289ec4e0b91e49b7e9ac500
 club-pixel-mark(3 colour, official) 38b1ff8b60527979aac8c55b7660a0eb · deco-pixel-step 8828625b7080132c72837234c017913a · deco-two-squares ce1f0906de94810dd5d98dd10df72ebc
 guide-card ed3239a1737b13ea2f67e7fd1577b0ea · hero-photo (800x312, awards stage) c230dadbcfe593a8daffd9299c0cb272
Unis (black ink transparent PNG): baha 87a4e95a01a5d104f3fc305030227f73 hail 180bcd32c5dd9f7c22a63cc245afff54 iau 53464ce6b8884f64490b216d9c8958e2 imam 5c0eaef9f179d8f2f0ac302e1c4c8140
 jazan 8ad5a41a254407329b58d1a058ab1e56 jeddah 7525b45b82c50a1ee782e4c66035ce01 kau 32c28db12281707222c5951cab6ad177 kfu c48ecc825cd1dcd66d013d532616436a kfupm 59f784241c5ecf4af99844007ea305e4
 kku 097d42ed1627b3e5b67ae3934160e323 ksu af6773e038bafe74b1eb3112270c3325 najran 8b812f08c053394b6763b9fc5a0d4a9c pnu 614f275d4b9a3a09677f82790526b411 psau 471c9ac3c89dbdacbe52c74285840d1d
 qassim c060ef78a76125488b331d8c99141cbd taibah 2480b00c1660cac8c5c45a5a94fc8a35 taif c2646995160c21d8a1f9d70bf0ac490d uqu ba398178c8141fdb4a32eb1acf3fdcd5
Partners: alibaba 562acd6622586fb42dd65e5107226c0e bizzdesign bb434d77b84735685d1a90be2c745c24 cisco 612515f68bd80a493ef728ee394aed62 comptia ddea5bc7ad3ebc5ad3ae7ec8eda41f44
 dcl 99890c96a390c9ca46b3d95bd1374621 garage beb1fb1d2dd386bb1335debc294d5d66 google e80e4317258865b2cf59cc460caec46e logrhythm a6c276e536912a13d3a2436a41810438
 nvidia 3f212e1ada9de3279461bfa792ed1021 offsec 8dd036b4fd40c099bd6f5f48ff1c8a25 replit d07c9c30cec034ded1717ab0b90fd20e saip 43abb0bdeab05255b21205322efcc1e8
Site UI language: white page #FAFAFB→#FFF, primary #4931AF/#4F29B7, near-black text #0A0A0F; H1 62/700 white on photo; section H2 48/700;
 pill buttons radius 24/999 (filled purple white text 16/500 pad 13x16; outline 1px purple 14/600 pad 14x24; white pill on photo);
 cards white radius 16, border 1px rgba(0,0,0,.06), no shadow; hero card radius 24 with photo + gradient to top rgba(73,49,175,.85)->0;
 banner (ads) radius 24 bg #F4EFFF; stats "+45 نادي طلابي / 18 جامعة شريكة / +12 مدينة"; small 40px icon tiles with tinted bg;
 section titles get a small lilac pixel square accent behind/above first letter; FAQ rows light #F7F5FB radius 12.

## Academy social posts (9:16, 1080x1920) — full rules in proposed skill "tuwaiq-social-posts"
Dark purple/navy vertical gradient (#0D0A2E -> #5B39AB), event photo top 35-50% fading in, white academy logo top-right, partner top-left w/ thin divider,
kashida-stretched bold white headline + lilac (#A893FF) second line, lilac section pill with side rules, translucent/outlined rounded stat cards,
coral/sand/green number accents, footer Tuwaiq.edu.sa bottom-left, partners row bottom. Club posts: club logo + university logo mandatory.

## Club posts (@TuwaiqClubs) — full rules in proposed skill "tuwaiq-club-posts"
Club logo white top-right, academy logo bottom-right (+partner w/ divider), @TuwaiqClubs bottom-left.
4 templates: workshop square (gradient #1F0F45->#4A20AE, teal outline type pill, white bold title right, 3D icon in orange notched frame left,
 presenter line lilac, 3 outline info pills date=orange time=purple place=teal); weekly schedule (#262626, huge "فعاليات أندية طويق",
 dark zigzag pixel, rows with mint #9AEDE6 / lilac date blocks, notch tab); club launch story (campus photo purple overlay, big club logo,
 4 filled colored benefit cards w/ tabs, 9 outline field pills); countdown campaign (dark navy, giant glass numeral, blurred pixels,
 orange gradient count line, light white sentence, glass "سجّل الآن").

## Campus photos (from Start slide.pptx; Campus.dc.html artboard) — local kit/campus/campus-<slug>.jpg
baha 48fd0fe49c882ab2b22475b6b4a96361 · iau 30dd43be85cab3c302ca5c3d80b74e21 · imam-club(gate) 28ac91ae6525b96c8524ea0787fbd3d5 · imam 265d1157224df864dfeca6a63be04b61
jazan dc9176733e96b78e0e6bebff54f6590c · kfu de0d53b8baf83b0865822154d0307697 · kfupm acd78c88a979631218155771c3765ad6 (665px, low-res) · kku 43efeb43a0a6ffebfd49e8fc004bd204
ksu 00c6c41c8256e2f69f8c3638b1164181 · najran 1aa175af88c7231623731bc49a8ed74c · nbu e956d27256d9bf49e74c8c46eb2290ea · pnu e609c5e6f29ad74bac855e9b5ba07c90
psau (panorama) 2ef0a380e8071902e757cbb872f85e26 · awards ceremony 1920px 6c0654ba6952e93702f3cc2f0ab9c313 (better than hero-photo)
Start-slide style (16:9): photo full-bleed + purple overlay (#5B3FC0-ish, strong) + gradient to #1E123D toward right; logos top-right (CLUB | Academy white);
 university name white bold right-aligned mid; subtitle small orange under it.

## OFFICIAL academy logos (vector, from user PDFs) — REPLACE the old traced ones
academy-h-color 1ba109c6184f1150649a1f84c217d5bc · academy-v-color eb19c51801a6cbb364870b9c52b6d011
academy-h-white 75a228a187719d7cb188a6d778e0858f · academy-v-white 9f1340c2e2a3c5190241bb817362eeac
academy-h-black 8290dacc8177ee3e16bf6042899f6ec4 · academy-v-black 1e54a3d7363440bea70e4eb43b7ddfdd
(official mark colour #571CBD, text #262626). Old ids 464387…, 2a4161…, 924f2c…, 2c8409… are deprecated.
