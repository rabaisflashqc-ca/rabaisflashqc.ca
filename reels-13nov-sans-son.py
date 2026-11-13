#!/usr/bin/env python3
"""Réels SANS SON du 13 nov. (ajouter un son tendance dans chaque app), même vidéo pour TikTok et Facebook. Objectif : visite du site.
Midi : cadeaux tech. 16 h : prêts pour l'hiver. 21 h : jouets sous le sapin. Aucun produit déjà publié.
Prix lus le 13 nov. (Keepa 8 h 34, page Amazon envoyée par Alex 8 h 39 et 8 h 45). Photos officielles (marques ou grands détaillants, jamais Amazon)."""

import pathlib, tempfile, subprocess, html as H
import pack
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+="h1,h2{text-align:center}h1{font-weight:800}.c{background:#fff;color:#1A1A1A;border-radius:40px;margin:30px 56px;padding:50px 44px;text-align:center}.big{font-family:Anton,Impact,sans-serif;font-size:210px;color:#C1121F;line-height:1}.pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:10px 34px;font-family:Anton,Impact,sans-serif;font-size:110px;margin:20px 0}"
OB="13 nov."
MIDI=[("JBL","Écouteurs sans fil Tune 125","B08WM1FXSF","44,98 $","19,97 $",56),("JBL","Écouteurs Vibe Beam 2","B0DN45YMP6","92,09 $","49,98 $",46),("Soundcore","Haut-parleur Bluetooth Soundcore 3","B08BCHKY52","99,99 $","54,98 $",45)]
H16=[("Kamik","Bottes d’hiver Forester pour homme","B07N1K4NK8","168,60 $","89,99 $",47),("Columbia","Manteau softshell Ascender pour homme","B0CLSS58LT","119,66 $","64,79 $",46),("Crocs","Sabots Classic doublés, bien chauds","B01A6LTSA0","64,20 $","34,99 $",45)]
SOIR=[("Barbie","The Movie, la poupée Allan","B0F2594KSN","72,73 $","34,99 $",52),("Hot Wheels","Mario Kart, le château de Bowser","B0DN1NFKQW","94,15 $","49,97 $",47),("NERF","Minecraft Firebrand","B0CJZFB8YQ","29,99 $","17,63 $",41)]
BPM=124; B=60/BPM
def page(inner,foot="Tous les deals avec photos sur le site"):
    return f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body style="width:1080px;height:1920px"><div class="top" style="padding-top:90px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 rabaisflashqc.ca</div><div class="s">{foot}</div></div></body></html>'
def deal(a,t,ic,av,pr,pc,hook=""):
    img=(pathlib.Path('docs/img/p')/('marque-'+ic+'.jpg')).resolve(); assert img.exists(), img
    hk=f'<div style="margin:36px 56px 0;text-align:center"><span style="display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:14px 34px;font-family:Anton,Impact,sans-serif;font-size:70px;line-height:1.1">{hook}</span></div>' if hook else ''
    return page(hk+f'<div style="margin:{34 if hook else 70}px auto 0;width:620px;height:{470 if hook else 520}px;background:#fff;border-radius:40px;display:flex;align-items:center;justify-content:center"><img src="{img.as_uri()}" style="max-width:560px;max-height:{430 if hook else 480}px;object-fit:contain"></div><div class="c"><div style="font-size:34px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:52px;font-weight:700;margin:10px 0 24px">{e(t)}</div><div class="big">{pr}</div><div class="pc">-{pc} %</div><div style="font-size:44px">avant : <s>{av}</s></div><div style="font-size:30px;color:#555;margin-top:18px">prix observé le {OB}</div></div>')
def titre(qui,h1,h2): return page(f'<div style="margin:170px 56px 0;text-align:center"><span style="display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:30px;padding:18px 40px;font-family:Anton,Impact,sans-serif;font-size:84px;line-height:1.1">{qui}</span></div><h1 class="an" style="font-size:112px;line-height:1.05;margin-top:70px">{h1}</h1><h2 style="font-size:58px">{h2}</h2>')
def fin(n,j): return page(f'<h1 class="an" style="font-size:124px;line-height:1.08;margin-top:230px">{n} AUTRES DEALS<br>T’ATTENDENT 👇</h1><div style="margin:50px 56px 0;text-align:center"><span style="display:inline-block;background:#fff;color:#C1121F;border-radius:30px;padding:24px 44px;font-family:Anton,Impact,sans-serif;font-size:104px">rabaisflashqc.ca</span></div><h2 style="font-size:54px;margin-top:50px">Vendredi fou dans {j} jours ⏳<br>Tape l’adresse, c’est gratuit</h2><p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:50px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>',"Prix observés le 13 nov., ils peuvent changer")
# Leçon des stats Facebook du 11 nov. (visionnage moyen d'environ 10 %, 1,2 % jusqu'au bout, 65 % de 45 ans et plus) :
# la 1re image montre tout de suite un produit et son prix, pas d'écran titre, et la vidéo est plus courte.
REELS={
 "reel-13nov-midi-tech-sans-son.mp4":[(deal(*MIDI[0],hook="ÉCOUTEURS JBL À -56 % 🎧"),6)]+[(deal(*p),5) for p in MIDI[1:]]+[(fin(170,14),6)],
 "reel-13nov-16h-hiver-sans-son.mp4":[(deal(*H16[0],hook="PRÊTS POUR L’HIVER? ❄️"),6)]+[(deal(*p),5) for p in H16[1:]]+[(fin(170,14),6)],
 "reel-13nov-21h-jouets-sans-son.mp4":[(deal(*SOIR[0],hook="SOUS LE SAPIN 🎄<br>3 JOUETS EN RABAIS"),6)]+[(deal(*p),5) for p in SOIR[1:]]+[(fin(170,14),6)],
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
