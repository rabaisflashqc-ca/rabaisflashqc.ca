#!/usr/bin/env python3
"""Réels SANS SON (ajouter un son tendance dans chaque app), même vidéo pour TikTok et Facebook. Objectif : visite du site.
Soir du 11 nov. : cadeaux tech pour ados. Matin du 12 nov. (publier AVANT 9 h 45) : pour les mamans. Aucun produit en commun.
Audience nommée dès la 1re image. Prix lus le 11 nov. (Keepa 21 h 47, page Offres du jour d'Amazon 21 h 52). Photos officielles des marques."""
import pathlib, tempfile, subprocess, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+="h1,h2{text-align:center}h1{font-weight:800}.c{background:#fff;color:#1A1A1A;border-radius:40px;margin:30px 56px;padding:50px 44px;text-align:center}.big{font-family:Anton,Impact,sans-serif;font-size:210px;color:#C1121F;line-height:1}.pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:10px 34px;font-family:Anton,Impact,sans-serif;font-size:110px;margin:20px 0}"
OB="11 nov."
SOIR=[("Sony","Casque antibruit WH-CH720N","B0BS1QCFHX","248,00 $","118,00 $",52),("JBL","Écouteurs sans fil Vibe Beam","B0BQPNMXQV","99,98 $","44,98 $",55),("Sony","Casque sans fil WH-CH520","B0BS1RT9S2","98,00 $","48,00 $",51),("JBL","Haut-parleur Bluetooth Clip 5","B0CTP56C5R","99,98 $","69,98 $",30)]
MATIN=[("Braun","Mélangeur à main MQ505","B01EA5ZI2U","77,99 $","44,99 $",42),("Crest","3D Whitestrips Vivid White","B01MRX9US8","34,99 $","24,66 $",30),("Conair","Fer à friser double céramique","B07ZL9MXKN","24,09 $","17,49 $",27),("Conair","Fer à boucler Curl Secret","B0GLSXY2JL","83,81 $","62,99 $",25)]
BPM=124; B=60/BPM
def page(inner,foot="Tous les deals avec photos sur le site"):
    return f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body style="width:1080px;height:1920px"><div class="top" style="padding-top:90px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 rabaisflashqc.ca</div><div class="s">{foot}</div></div></body></html>'
def deal(a,t,ic,av,pr,pc):
    img=(pathlib.Path('docs/img/p')/('marque-'+ic+'.jpg')).resolve(); assert img.exists(), img
    return page(f'<div style="margin:70px auto 0;width:620px;height:520px;background:#fff;border-radius:40px;display:flex;align-items:center;justify-content:center"><img src="{img.as_uri()}" style="max-width:560px;max-height:480px;object-fit:contain"></div><div class="c"><div style="font-size:34px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:52px;font-weight:700;margin:10px 0 24px">{e(t)}</div><div class="big">{pr}</div><div class="pc">-{pc} %</div><div style="font-size:44px">avant : <s>{av}</s></div><div style="font-size:30px;color:#555;margin-top:18px">prix observé le {OB}</div></div>')
def titre(qui,h1,h2): return page(f'<div style="margin:170px 56px 0;text-align:center"><span style="display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:30px;padding:18px 40px;font-family:Anton,Impact,sans-serif;font-size:84px;line-height:1.1">{qui}</span></div><h1 class="an" style="font-size:112px;line-height:1.05;margin-top:70px">{h1}</h1><h2 style="font-size:58px">{h2}</h2>')
def fin(n,j): return page(f'<h1 class="an" style="font-size:124px;line-height:1.08;margin-top:230px">{n} AUTRES DEALS<br>T’ATTENDENT 👇</h1><div style="margin:50px 56px 0;text-align:center"><span style="display:inline-block;background:#fff;color:#C1121F;border-radius:30px;padding:24px 44px;font-family:Anton,Impact,sans-serif;font-size:104px">rabaisflashqc.ca</span></div><h2 style="font-size:54px;margin-top:50px">Vendredi fou dans {j} jours ⏳<br>Tape l’adresse, c’est gratuit</h2><p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:50px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>',"Prix observés le 11 nov., ils peuvent changer")
REELS={
 "reel-11nov-soir-ados-sans-son.mp4":[(titre("PARENTS D’ADOS 👀","SON CADEAU<br>DE NOËL<br>À MOITIÉ PRIX 🎧","4 deals Sony et JBL<br>jusqu’à -55 %"),6)]+[(deal(*p),5) for p in SOIR]+[(fin(70,16),7)],
 "reel-12nov-matin-mamans-sans-son.mp4":[(titre("MAMANS DU QUÉBEC ☕","4 PETITS PRIX<br>POUR TE<br>GÂTER 💛","Jusqu’à -42 %<br>dès 17,49 $"),6)]+[(deal(*p),5) for p in MATIN]+[(fin(70,15),7)],
}
with sync_playwright() as pw:
    for nom,slides in REELS.items():
        tmp=pathlib.Path(tempfile.mkdtemp()); fr=[]
        for i,(h,_) in enumerate(slides):
            br,ctx,pg=pack.render(pw,h,(1080,1920),tmp,f"s{i}"); pg.wait_for_timeout(500)
            p=tmp/f"s{i}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
            if i in (0,1,len(slides)-1): (pathlib.Path('/tmp')/f"{nom}-{i}.png").write_bytes(p.read_bytes())
        durs=[n*B for _,n in slides]; total=sum(durs)
        out=pack.OUT/nom; inp=[]; flt=[]
        for i,(p,d) in enumerate(zip(fr,durs)):
            inp+=["-loop","1","-t",f"{d:.4f}","-i",str(p)]
            flt.append(f"[{i}:v]scale=1080:1920,fps=30,setsar=1[v{i}]")
        n=len(fr); flt.append("".join(f"[v{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0,format=yuv420p[o]")
        subprocess.run(["ffmpeg","-y",*inp,"-filter_complex",";".join(flt),"-map","[o]","-t",f"{total:.3f}","-an","-r","30","-preset","veryfast","-c:v","libx264","-movflags","+faststart",str(out)],check=True,capture_output=True)
        print(out, round(total,2))
