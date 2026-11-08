#!/usr/bin/env python3
"""Réels du 8 nov., SANS SON (ajouter un son tendance dans chaque app), 3 audiences : Beauté, Maison, Cadeaux.
Photos officielles des marques ou de grands détaillants (jamais Amazon). Prix : passe Keepa du 8 nov. à 11 h 43.
Format qui marche sur TikTok (stats du 8 nov.) : une vraie photo + gros prix + pastille % jaune, un deal par écran."""
import pathlib, tempfile, subprocess, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".c{background:#fff;color:#1A1A1A;border-radius:40px;margin:30px 56px;padding:50px 44px;text-align:center}.big{font-family:Anton,Impact,sans-serif;font-size:210px;color:#C1121F;line-height:1}.pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:10px 34px;font-family:Anton,Impact,sans-serif;font-size:110px;margin:20px 0}"
OB="8 nov."
REELS={
 "beaute":("BEAUTÉ<br>JUSQU’À -41 % 💇‍♀️","3 outils coiffure Conair<br>pour elle 🎁",[
   ("Conair","Fer à friser double céramique 1 po","B07ZL9MXKN","29,43 $","17,49 $",41),
   ("Conair","Curl Secret, fer à boucler automatique","B0GLSXY2JL","99,63 $","62,99 $",37),
   ("Conair","Fer plat double céramique 1 po","B07ZHZMXMV","32,73 $","20,99 $",36)]),
 "maison":("LA CUISINE<br>À PETIT PRIX 🏠","Nespresso, Philips, Ninja<br>jusqu’à -38 %",[
   ("Nespresso","Machine à café Vertuo Pop+ Deluxe","B0D712DKKD","151,81 $","94,00 $",38),
   ("Ninja","Mélangeur Nutri-Blender Pro","B095FSJ7N6","124,79 $","89,99 $",28),
   ("Philips","Friteuse à air série 2000","B0D8QN4C9X","137,70 $","99,99 $",27)]),
 "cadeaux":("CADEAUX DES FÊTES<br>JUSQU’À -50 % 🎄","Pour lui, pour elle,<br>pour les petits 🎁",[
   ("JBL","Écouteurs sport Endurance Race 2","B0DVTGBCBL","80,72 $","39,98 $",50),
   ("Levi's","Jeans 505 pour homme","B08P55W5DW","67,96 $","37,03 $",46),
   ("Little Tikes","Chien berceur Rockin’ Puppy (1 à 3 ans)","B08S3BFJ37","89,90 $","49,99 $",44),
   ("Sony","Écouteurs sans fil WF-C510","B0D9R45FMH","87,22 $","58,00 $",34),
   ("Crayola","Coffret d’art Pokémon","B0CCPRDH3T","29,08 $","19,98 $",31),
   ("GUND","Ourson en peluche Grahm","B07CSL8LR8","52,82 $","42,13 $",20)]),
}
BPM=124; B=60/BPM
def page(inner,foot="Vérifie le prix final sur rabaisflashqc.ca"):
    return f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body style="width:1080px;height:1920px"><div class="top" style="padding-top:90px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">{foot}</div></div></body></html>'
def deal(a,t,ic,av,pr,pc):
    img=(pathlib.Path('docs/img/p')/('marque-'+ic+'.jpg')).resolve()
    assert img.exists(), img
    return page(f'<div style="margin:70px auto 0;width:620px;height:520px;background:#fff;border-radius:40px;display:flex;align-items:center;justify-content:center"><img src="{img.as_uri()}" style="max-width:560px;max-height:480px;object-fit:contain"></div><div class="c"><div style="font-size:34px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:52px;font-weight:700;margin:10px 0 24px">{e(t)}</div><div class="big">{pr}</div><div class="pc">-{pc} %</div><div style="font-size:44px">avant : <s>{av}</s></div><div style="font-size:30px;color:#555;margin-top:18px">prix observé le {OB}</div></div>')
def build(nom,titre,sous,picks,pw):
    # 1re image = le plus gros % (accroche choc dès la 1re seconde), puis les deals
    slides=[(page(f'<h1 class="an" style="font-size:118px;line-height:1.05;margin-top:230px">{titre}</h1><h2 style="font-size:60px">{sous}</h2>'),5)]
    slides+=[(deal(*p),5) for p in picks]
    slides.append((page('<h1 class="an" style="font-size:120px;line-height:1.1;margin-top:300px">BLACK FRIDAY<br>DANS 19 JOURS ⏳</h1><h2 style="font-size:58px">Enregistre et partage<br>à quelqu’un qui magasine 🎄</h2>'),5))
    slides.append((page('<h1 class="an" style="font-size:120px;line-height:1.1;margin-top:330px">PLUS DE DEALS<br>SUR LE SITE 👇</h1><h2 style="font-size:60px">rabaisflashqc.ca</h2><p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:60px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>'),5))
    tmp=pathlib.Path(tempfile.mkdtemp()); fr=[]
    for i,(h,_) in enumerate(slides):
        br,ctx,pg=pack.render(pw,h,(1080,1920),tmp,f"s{i}"); pg.wait_for_timeout(500)
        p=tmp/f"s{i}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
    durs=[n*B for _,n in slides]; total=sum(durs)
    out=pack.OUT/f"reel-08nov-{nom}-sans-son.mp4"
    inp=[];flt=[]
    for i,(p,d) in enumerate(zip(fr,durs)):
        inp+=["-loop","1","-t",f"{d:.4f}","-i",str(p)]
        flt.append(f"[{i}:v]scale=1080:1920,fps=30,setsar=1[v{i}]")
    n=len(fr); flt.append("".join(f"[v{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0,format=yuv420p[o]")
    subprocess.run(["ffmpeg","-y",*inp,"-filter_complex",";".join(flt),"-map","[o]","-t",f"{total:.3f}","-an","-r","30","-preset","veryfast","-c:v","libx264","-movflags","+faststart",str(out)],check=True,capture_output=True)

    print(out, round(total,2))
with sync_playwright() as pw:
    for k,(t,s,p) in REELS.items(): build(k,t,s,p,pw)
