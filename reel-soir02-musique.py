#!/usr/bin/env python3
"""Réel 9:16 du soir 2 nov : 5 plus gros rabais de la passe Keepa de 19 h 16.
Coupes franches calées sur le beat (124 bpm), musique originale music.py sans fondu d'entrée, audio normalisé à -14 LUFS."""
import pathlib, tempfile, subprocess, html as H
import pack, music
from playwright.sync_api import sync_playwright
e=H.escape
CSS=open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS+=".c{background:#fff;color:#1A1A1A;border-radius:40px;margin:30px 56px;padding:50px 44px;text-align:center}.big{font-family:Anton,Impact,sans-serif;font-size:210px;color:#C1121F;line-height:1}.pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:10px 34px;font-family:Anton,Impact,sans-serif;font-size:110px;margin:20px 0}"
OB="2 nov. à 19 h 16"
PICK=[("Sony","Casque sans fil WH-CH520","🎧","93,96 $","48,00 $",49,OB),("CMF by Nothing","Écouteurs sans fil Buds 2","🎵","70,70 $","37,99 $",46,OB),("Sony","Haut-parleur ULT Field 1, étanche","🔊","174,27 $","98,00 $",44,OB),("DEWALT","Perceuse sans balais 20V MAX, ensemble","🛠️","199,94 $","118,00 $",41,OB),("EXIT","Jeu d’évasion La maison des énigmes","🧩","30,62 $","17,95 $",41,OB)]
BPM=128; B=60/BPM
def page(inner,foot="Vérifie le prix final sur rabaisflashqc.ca"):
    return f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body style="width:1080px;height:1920px"><div class="top" style="padding-top:90px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 LIEN DANS LA BIO</div><div class="s">{foot}</div></div></body></html>'
slides=[(page('<h1 class="an" style="font-size:135px;line-height:1.05;margin-top:230px">JUSQU’À -49 %<br>CE SOIR ⚡</h1><h2 style="font-size:60px">Son, outils et jeux<br>prix vus à 19 h 16 👀</h2>'),6)]
for a,t,ic,av,pr,pc,ob in PICK:
    slides.append((page(f'<div style="font-size:200px;text-align:center;margin-top:120px">{ic}</div><div class="c"><div style="font-size:34px;font-weight:700;color:#C1121F;text-transform:uppercase">{e(a)}</div><div style="font-size:52px;font-weight:700;margin:10px 0 24px">{e(t)}</div><div class="big">{pr}</div><div class="pc">-{pc} %</div><div style="font-size:44px">avant : <s>{av}</s></div><div style="font-size:30px;color:#555;margin-top:18px">prix observé le {ob}</div></div>'),5))
slides.append((page('<h1 class="an" style="font-size:130px;line-height:1.1;margin-top:300px">BLACK FRIDAY<br>DANS 25 JOURS ⏳</h1><h2 style="font-size:58px">Abonne-toi pour pas<br>manquer les vrais deals</h2>'),6))
slides.append((page('<h1 class="an" style="font-size:120px;line-height:1.1;margin-top:330px">PLUS DE DEALS<br>SUR LE SITE 👇</h1><h2 style="font-size:60px">rabaisflashqc.ca</h2><p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:60px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>'),6))
tmp=pathlib.Path(tempfile.mkdtemp()); fr=[]
with sync_playwright() as pw:
    for i,(h,_) in enumerate(slides):
        br,ctx,pg=pack.render(pw,h,(1080,1920),tmp,f"s{i}"); pg.wait_for_timeout(500)
        p=tmp/f"s{i}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
durs=[n*B for _,n in slides]; total=sum(durs)
raw=music.make(tmp/"m.wav",total+0.2,bpm=BPM,fadein=0)
norm=tmp/"mn.wav"
subprocess.run(["ffmpeg","-y","-i",str(raw),"-af","loudnorm=I=-14:TP=-1.5:LRA=11","-ar","44100",str(norm)],check=True,capture_output=True)
out=pack.OUT/"reel-soir-02nov-musique.mp4"
inp=[];flt=[]
for i,(p,d) in enumerate(zip(fr,durs)):
    inp+=["-loop","1","-t",f"{d:.4f}","-i",str(p)]
    flt.append(f"[{i}:v]scale=1080:1920,fps=30,setsar=1[v{i}]")
n=len(fr); flt.append("".join(f"[v{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0,format=yuv420p[o]")
subprocess.run(["ffmpeg","-y",*inp,"-i",str(norm),"-filter_complex",";".join(flt),"-map","[o]","-map",f"{n}:a","-t",f"{total:.3f}","-c:a","aac","-b:a","192k","-r","30","-preset","veryfast","-c:v","libx264","-movflags","+faststart",str(out)],check=True,capture_output=True)
print(out, round(total,2))
