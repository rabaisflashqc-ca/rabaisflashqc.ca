#!/usr/bin/env python3
"""Réel du matin 3 nov., SANS SON (ajouter un son tendance dans chaque app).
9:16 : 5 deals de la passe Keepa du 3 nov. à 8 h 15, accroche dès la 1re image, compte à rebours Black Friday.
Coupes franches toutes les ~2,4 s, aucune piste audio."""
import pathlib, tempfile, subprocess, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".c{background:#fff;color:#1A1A1A;border-radius:40px;margin:30px 56px;padding:50px 44px;text-align:center}.big{font-family:Anton,Impact,sans-serif;font-size:210px;color:#C1121F;line-height:1}.pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:10px 34px;font-family:Anton,Impact,sans-serif;font-size:110px;margin:20px 0}"
OB="3 nov. à 8 h 15"
PICK=[("Contigo","Tasse de voyage Streeterville","☕","31,16 $","19,06 $",39,OB),("DREO","Humidificateur intelligent pour la chambre","💧","100,01 $","62,99 $",37,OB),("Dremel","Outil rotatif 4300 avec 40 accessoires","🛠️","157,65 $","99,98 $",37,OB),("Conair","Fer à boucler automatique Curl Secret","💇‍♀️","97,99 $","69,94 $",29,OB),("Fisher-Price","Tapis-piano d’éveil Glow and Grow","🎹","76,12 $","54,97 $",28,OB)]
BPM=124; B=60/BPM
def page(inner,foot="Vérifie le prix final sur rabaisflashqc.ca"):
    return f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body style="width:1080px;height:1920px"><div class="top" style="padding-top:90px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">{foot}</div></div></body></html>'
slides=[(page('<h1 class="an" style="font-size:118px;line-height:1.05;margin-top:230px">CADEAUX DES FÊTES<br>JUSQU’À -39 % 🎁</h1><h2 style="font-size:60px">5 deals vus ce matin<br>à 8 h 15 👀</h2>'),6)]
for a,t,ic,av,pr,pc,ob in PICK:
    slides.append((page(f'<div style="font-size:200px;text-align:center;margin-top:120px">{ic}</div><div class="c"><div style="font-size:34px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:52px;font-weight:700;margin:10px 0 24px">{e(t)}</div><div class="big">{pr}</div><div class="pc">-{pc} %</div><div style="font-size:44px">avant : <s>{av}</s></div><div style="font-size:30px;color:#555;margin-top:18px">prix observé le {ob}</div></div>'),5))
slides.append((page('<h1 class="an" style="font-size:130px;line-height:1.1;margin-top:300px">BLACK FRIDAY<br>DANS 24 JOURS ⏳</h1><h2 style="font-size:58px">Enregistre et partage<br>à quelqu’un qui magasine 🎄</h2>'),6))
slides.append((page('<h1 class="an" style="font-size:120px;line-height:1.1;margin-top:330px">PLUS DE DEALS<br>SUR LE SITE 👇</h1><h2 style="font-size:60px">rabaisflashqc.ca</h2><p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:60px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>'),6))
tmp=pathlib.Path(tempfile.mkdtemp()); fr=[]
with sync_playwright() as pw:
    for i,(h,_) in enumerate(slides):
        br,ctx,pg=pack.render(pw,h,(1080,1920),tmp,f"s{i}"); pg.wait_for_timeout(500)
        p=tmp/f"s{i}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
durs=[n*B for _,n in slides]; total=sum(durs)
out=pack.OUT/"reel-matin-03nov-sans-son.mp4"
inp=[];flt=[]
for i,(p,d) in enumerate(zip(fr,durs)):
    inp+=["-loop","1","-t",f"{d:.4f}","-i",str(p)]
    flt.append(f"[{i}:v]scale=1080:1920,fps=30,setsar=1[v{i}]")
n=len(fr); flt.append("".join(f"[v{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0,format=yuv420p[o]")
subprocess.run(["ffmpeg","-y",*inp,"-filter_complex",";".join(flt),"-map","[o]","-t",f"{total:.3f}","-an","-r","30","-preset","veryfast","-c:v","libx264","-movflags","+faststart",str(out)],check=True,capture_output=True)
print(out, round(total,2))
