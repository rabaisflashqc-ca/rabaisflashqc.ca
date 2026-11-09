#!/usr/bin/env python3
"""Image du 9 nov. soir (1080x1350), concept « La liste du Père Noël » : 5 cadeaux pour les kids, tous à moins de 25 $.
Cible : mamans du Québec qui remplissent les bas de Noël. Photos officielles (marques ou grands détaillants), prix Keepa du 9 nov. à 8 h 11."""
import pathlib, tempfile, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
P=[("Le jouet viral","Bitzee, l'animal virtuel en boule","marque-B0DSCGXCT4","42,14 $","24,98 $",41),
   ("La collectionneuse","5 Surprise My Mini Baby","marque-B0CD311Q6J","25,34 $","17,99 $",29),
   ("Le tout-petit","Guitare en bois LeapFrog","marque-B0DMF8JZYS","25,19 $","18,22 $",28),
   ("Le fan de Pokémon","Coffret d'art Crayola Pokémon","marque-B0CCPRDH3T","27,48 $","19,98 $",27),
   ("L'ado","Fer plat Conair double céramique","marque-B07ZHZMXMV","31,45 $","20,99 $",33)]
from PIL import Image, ImageChops
_T=pathlib.Path(tempfile.mkdtemp())
def img(s):  # recadre le blanc autour de la photo officielle (copie temporaire, rien n'est copié dans docs/)
    im=Image.open(pathlib.Path("docs/img/p")/(s+".jpg")).convert("RGB")
    bb=ImageChops.difference(im,Image.new("RGB",im.size,"white")).point(lambda v:255 if v>18 else 0).getbbox()
    if bb: im=im.crop((max(bb[0]-8,0),max(bb[1]-8,0),min(bb[2]+8,im.width),min(bb[3]+8,im.height)))
    out=_T/(s+".png"); im.save(out); return out.resolve().as_uri()
CSS="""*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;background:#FFF6E5;font-family:'Barlow Semi Condensed',sans-serif;color:#1E2A22;position:relative;overflow:hidden}
.an{font-family:Anton,Impact,sans-serif;font-weight:400}
.hd{background:#0F5132;color:#fff;padding:26px 50px 24px;position:relative}
.br{display:flex;align-items:center;gap:10px;font-size:30px;font-weight:700;letter-spacing:2px}.br b{color:#FFC72C}
.h1{font-size:84px;line-height:.95;margin-top:10px;color:#fff}.h1 span{color:#FFC72C}
.sub{font-size:34px;font-weight:600;margin-top:10px}
.tag{position:absolute;right:40px;top:30px;width:200px;height:200px;border-radius:50%;background:#C1121F;border:8px dashed #FFC72C;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(10deg);color:#fff;text-align:center}
.tag small{font-size:30px;font-weight:700}.tag strong{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:84px;line-height:.9;color:#FFC72C}
.l{padding:18px 40px 0}
.r{display:flex;align-items:center;gap:22px;background:#fff;border-radius:24px;padding:12px 22px 12px 12px;margin-bottom:12px;border:3px solid #E8D9B5;height:158px}
.r img{width:150px;height:136px;object-fit:contain;border-radius:16px;background:#fff;flex:none}
.ck{width:46px;height:46px;border:4px solid #0F5132;border-radius:10px;flex:none;display:grid;place-items:center;font-size:36px;color:#C1121F;font-weight:900}
.m{flex:1;min-width:0}.w{display:inline-block;background:#0F5132;color:#fff;border-radius:10px;padding:2px 12px;font-size:24px;font-weight:700}
.t{font-size:34px;font-weight:700;line-height:1.05;margin-top:6px}
.p{text-align:right;flex:none}.p .n{font-family:Anton,Impact,sans-serif;font-size:66px;color:#C1121F;line-height:1}.p .o{font-size:24px;color:#555}
.p .x{display:inline-block;background:#FFC72C;color:#7A0A16;border-radius:10px;padding:0 10px;font-family:Anton,Impact,sans-serif;font-size:32px;margin-top:2px}
.ft{position:absolute;left:0;right:0;bottom:0;background:#C1121F;color:#fff;text-align:center;padding:20px 0 18px}
.ft .u{font-family:Anton,Impact,sans-serif;font-size:62px;color:#FFC72C;line-height:1}.ft .s{font-size:24px;font-weight:600;margin-top:6px}"""
rows="".join(f'<div class="r"><div class="ck">✓</div><img src="{img(s)}"><div class="m"><span class="w">{e(w)}</span><div class="t">{e(t)}</div></div>'
             f'<div class="p"><div class="n">{pr}</div><div class="o">avant <s>{av}</s></div><div class="x">-{pc} %</div></div></div>' for (w,t,s,av,pr,pc) in P)
html=(f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body>'
 f'<div class="hd"><div class="br">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>'
 f'<div class="h1 an">LA LISTE<br>DU <span>PÈRE NOËL</span> 🎅</div><div class="sub">5 cadeaux pour les kids, parfaits pour le bas de Noël</div>'
 f'<div class="tag"><small>moins de</small><strong>25 $</strong><small>chacun</small></div></div>'
 f'<div class="l">{rows}</div>'
 f'<div class="ft"><div class="u">👉 rabaisflashqc.ca</div><div class="s">Prix observés le 9 nov. · peuvent changer · vérifie le prix final sur le site</div></div></body></html>')
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    br,ctx,pg=pack.render(pw,html,(1080,1350),tmp,"img09k")
    pg.wait_for_timeout(800); out=pack.OUT/"post-09nov-soir-kids.png"; pg.screenshot(path=str(out)); ctx.close(); br.close()
print(out)
