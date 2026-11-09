#!/usr/bin/env python3
"""Réels SANS SON pour le soir du 8 nov. et le matin du 9 nov. (ajouter un son tendance dans chaque app).
Prix : passe Keepa du 8 nov. à 21 h 13 (suivi/deals_chrome.json). Photos officielles des marques (docs/img/p/marque-*), jamais Amazon.
Réel 1 (ce soir) : Cadeaux des Fêtes, 6 deals. Réel 2 (demain matin) : Pour maman, 3 deals. Réel 3 (avant midi) : 1 deal, format TikTok 10 s."""
import pathlib, tempfile, subprocess, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".c{background:#fff;color:#1A1A1A;border-radius:40px;margin:30px 56px;padding:50px 44px;text-align:center}.big{font-family:Anton,Impact,sans-serif;font-size:210px;color:#C1121F;line-height:1}.pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:10px 34px;font-family:Anton,Impact,sans-serif;font-size:110px;margin:20px 0}"
OB="8 nov."
# (marque, produit, fichier photo officielle, avant, prix, %)
RACE=("JBL","Écouteurs sport Endurance Race 2","B0DVTGBCBL","77,38 $","39,90 $",48)
TIKES=("Little Tikes","Chien berceur Rockin’ Puppy","B08S3BFJ37","87,00 $","49,99 $",43)
JBL770=("JBL","Casque à réduction de bruit Tune 770NC","B0CTB8GKM2","138,45 $","79,98 $",42)
LEVIS=("Levi's","Jeans 505 pour homme","B08P55W5DW","61,84 $","37,65 $",39)
SONY=("Sony","Écouteurs sans fil WF-C510","B0D9R45FMH","85,23 $","58,00 $",32)
CRAYOLA=("Crayola","Coffret d’art Pokémon","B0CCPRDH3T","28,34 $","19,98 $",29)
NESP=("Nespresso","Machine Vertuo Pop+ Deluxe","B0D712DKKD","147,09 $","94,00 $",36)
FERPLAT=("Conair","Fer plat double céramique","B07ZHZMXMV","32,13 $","20,99 $",35)
NINJA=("Ninja","Mélangeur Nutri-Blender Pro","B095FSJ7N6","121,81 $","89,99 $",26)
BPM=124; B=60/BPM
def page(inner,foot="Vérifie le prix final sur rabaisflashqc.ca"):
    return f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body style="width:1080px;height:1920px"><div class="top" style="padding-top:90px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 rabaisflashqc.ca</div><div class="s">{foot}</div></div></body></html>'
def deal(a,t,ic,av,pr,pc):
    img=(pathlib.Path('docs/img/p')/('marque-'+ic+'.jpg')).resolve(); assert img.exists(), img
    return page(f'<div style="margin:70px auto 0;width:620px;height:520px;background:#fff;border-radius:40px;display:flex;align-items:center;justify-content:center"><img src="{img.as_uri()}" style="max-width:560px;max-height:480px;object-fit:contain"></div><div class="c"><div style="font-size:34px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:52px;font-weight:700;margin:10px 0 24px">{e(t)}</div><div class="big">{pr}</div><div class="pc">-{pc} %</div><div style="font-size:44px">avant : <s>{av}</s></div><div style="font-size:30px;color:#555;margin-top:18px">prix observé le {OB}</div></div>')
def titre(h1,h2): return page(f'<h1 class="an" style="font-size:118px;line-height:1.05;margin-top:230px">{h1}</h1><h2 style="font-size:60px">{h2}</h2>')
FIN=page('<h1 class="an" style="font-size:120px;line-height:1.1;margin-top:330px">PLUS DE DEALS<br>SUR LE SITE 👇</h1><h2 style="font-size:60px">rabaisflashqc.ca</h2><p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:60px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>')
def bf(j): return page(f'<h1 class="an" style="font-size:120px;line-height:1.1;margin-top:300px">BLACK FRIDAY<br>DANS {j} JOURS ⏳</h1><h2 style="font-size:58px">Enregistre et partage<br>à quelqu’un qui magasine 🎄</h2>')
REELS={
 "reel-08nov-soir-cadeaux-sans-son.mp4":[(titre("CADEAUX DES FÊTES<br>JUSQU’À -48 % 🎁","Pour lui, pour elle,<br>pour les petits"),5)]+[(deal(*p),5) for p in (RACE,TIKES,JBL770,LEVIS,SONY,CRAYOLA)]+[(bf(19),5),(FIN,5)],
 "reel-09nov-matin-maman-sans-son.mp4":[(titre("CADEAUX POUR MAMAN<br>JUSQU’À -36 % 💝","Café, cheveux, cuisine"),5)]+[(deal(*p),5) for p in (NESP,FERPLAT,NINJA)]+[(bf(18),5),(FIN,5)],
 "reel-09nov-midi-deal-sans-son.mp4":[(page('<h1 class="an" style="font-size:150px;line-height:1.05;margin-top:300px">DES JBL<br>À 39,90 $?! 🤯</h1><h2 style="font-size:70px">-48 %</h2>'),3),(deal(*RACE),8),(FIN,4)],
}
with sync_playwright() as pw:
    for nom,slides in REELS.items():
        tmp=pathlib.Path(tempfile.mkdtemp()); fr=[]
        for i,(h,_) in enumerate(slides):
            br,ctx,pg=pack.render(pw,h,(1080,1920),tmp,f"s{i}"); pg.wait_for_timeout(500)
            p=tmp/f"s{i}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
        durs=[n*B for _,n in slides]; total=sum(durs)
        out=pack.OUT/nom; inp=[]; flt=[]
        for i,(p,d) in enumerate(zip(fr,durs)):
            inp+=["-loop","1","-t",f"{d:.4f}","-i",str(p)]
            flt.append(f"[{i}:v]scale=1080:1920,fps=30,setsar=1[v{i}]")
        n=len(fr); flt.append("".join(f"[v{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0,format=yuv420p[o]")
        subprocess.run(["ffmpeg","-y",*inp,"-filter_complex",";".join(flt),"-map","[o]","-t",f"{total:.3f}","-an","-r","30","-preset","veryfast","-c:v","libx264","-movflags","+faststart",str(out)],check=True,capture_output=True)
        print(out, round(total,2))
