#!/usr/bin/env python3
"""Réel 9:16 du soir 28 oct : intro, 5 deals (prix, avant, %), fin. Sans musique."""
import pathlib, tempfile, subprocess, html as H
import pack, build
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".c{background:#fff;color:#1A1A1A;border-radius:40px;margin:30px 56px;padding:50px 44px;text-align:center}.big{font-family:Anton,Impact,sans-serif;font-size:210px;color:#C1121F;line-height:1}.pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:10px 34px;font-family:Anton,Impact,sans-serif;font-size:110px;margin:20px 0}"
pick=[("ThermoMaven","Thermomètre à viande Bluetooth G2","🥩","159,99 $",79.99,50),("Russell Athletic","Chandail pullover pour homme","👕","63,76 $",27.88,56),("Cottonelle","Papier de toilette, 144 rouleaux","🧻","43,96 $",21.98,50),("The North Face","Gants Etip recyclés","🧤","54,99 $",31.98,42),("Skechers","Espadrilles Go Run Consistent 2.0","👟","env. 69 $",49.98,28)]
def money(p): return f"{p:.2f}".replace(".",",")+" $"
def page(inner,foot="rabaisflashqc.ca · Les prix bougent vite, fonce!"):
    return f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body style="width:1080px;height:1920px"><div class="top" style="padding-top:90px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">{foot}</div></div></body></html>'
slides=[page('<h1 class="an" style="font-size:150px;line-height:1.05;margin-top:300px">LES RABAIS<br>DU MATIN ⚡</h1><h2 style="font-size:56px">5 aubaines à ne pas manquer</h2>')]
for a,t,ic,av,pr,pc in pick:
    slides.append(page(f'<div style="font-size:200px;text-align:center;margin-top:120px">{ic}</div><div class="c"><div style="font-size:34px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:52px;font-weight:700;margin:10px 0 24px">{e(t)}</div><div class="big">{money(pr)}</div><div class="pc">-{pc} %</div><div style="font-size:44px">avant : <s>{av}</s></div></div>'))
slides.append(page('<h1 class="an" style="font-size:120px;line-height:1.1;margin-top:330px">PLUS DE DEALS<br>SUR LE SITE 👇</h1><h2 style="font-size:60px">rabaisflashqc.ca</h2><p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:60px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>'))
tmp=pathlib.Path(tempfile.mkdtemp()); fr=[]
with sync_playwright() as pw:
    for i,h in enumerate(slides):
        br,ctx,pg=pack.render(pw,h,(1080,1920),tmp,f"s{i}"); pg.wait_for_timeout(500)
        p=tmp/f"s{i}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
out=pack.OUT/"reel-matin-29oct.mp4"
inp=[];flt=[]
for i,p in enumerate(fr):
    inp+=["-loop","1","-t","3.2","-i",str(p)]
    flt.append(f"[{i}:v]scale=1080:1920,fps=30,fade=t=in:d=0.3,fade=t=out:st=2.9:d=0.3[v{i}]")
n=len(fr); flt.append("".join(f"[v{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0,format=yuv420p[o]")
subprocess.run(["ffmpeg","-y",*inp,"-filter_complex",";".join(flt),"-map","[o]","-r","30","-preset","veryfast","-c:v","libx264","-movflags","+faststart",str(out)],check=True,capture_output=True)
print(out)
