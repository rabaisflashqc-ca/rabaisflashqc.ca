#!/usr/bin/env python3
"""Moteur du pack du jour : image 1080x1350 + réel 9:16 (12-13 s) depuis une liste de deals Keepa.
Usage : python3 outils/pack_du_jour.py AAAA-MM-JJ ASIN1 ASIN2 ASIN3  -> docs/pack-du-jour/matin-JJmois-prix.png et reel-matin-JJmois-musique.mp4
Prix lus dans suivi/deals_chrome.json. Aucune photo Amazon dans nos images."""
import sys, json, pathlib, tempfile, subprocess, html as H
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import pack, music
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
e = H.escape
MOIS = ["jan","fév","mars","avr","mai","juin","juil","août","sept","oct","nov","déc"]
CSS = open(ROOT/'soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS += ".c{background:#fff;color:#1A1A1A;border-radius:40px;margin:20px 56px;padding:44px 40px;text-align:center}.big{font-family:Anton,Impact,sans-serif;font-size:230px;color:#C1121F;line-height:1}.pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:8px 34px;font-family:Anton,Impact,sans-serif;font-size:110px;margin:14px 0}"
def money(p): return f"{p:.2f}".replace(".", ",") + " $"
import re
def cl(t, n=44):
    t = re.sub(r" (à|pour|de|du|des|avec) \S*$", "", t) if len(t) > n else t
    return t if len(t) <= n else re.sub(r" (à|pour|de|du|des|avec|en)$", "", t[:n].rsplit(" ", 1)[0])
def foot(h): return f'<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">{h}</div><div class="s">rabaisflashqc.ca · prix vérifié, peut changer</div></div>'
def page(inner, H_, hook, ft): return f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}body{{height:{H_}px!important}}</style></head><body><div class="top" style="padding-top:{90 if H_>1500 else 46}px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}{foot(ft)}</body></html>'
def slide(d, k, H_=1920):
    return page(f'<h2 style="font-size:60px;padding-top:{60 if H_>1500 else 20}px;text-align:center;color:#FFC72C" class="an">{e(hook(d,k))}</h2><div class="c"><div style="font-size:50px;font-weight:700;margin:0 0 18px">{e(cl(d["title"],34))}</div><div class="big">{money(d["price"])}</div><div class="pc">-{d["pct"]} %</div><div style="font-size:48px">au lieu de <s>{money(d["was"])}</s></div></div>', H_, None, "👉 RABAISFLASHQC.CA")
def hook(d, k): return f'{money(d["price"])} AU LIEU DE {money(d["was"])}' if k == 0 else f'N° {k+1} : -{d["pct"]} %'
def main():
    date, asins = sys.argv[1], sys.argv[2:]
    src = {d["asin"]: d for d in json.load(open(ROOT/"suivi/deals_chrome.json"))}
    deals = [src[a] for a in asins]
    y, m, dd = map(int, date.split('-')); tag = f"{dd}{MOIS[m-1]}"
    pack.OUT.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as pw:
        # image 1080x1350 : Top 3
        rows = "".join(f'<div class="card" style="padding:26px 30px;margin:0 56px 20px"><div class="bd" style="font-size:64px">-{d["pct"]}%</div><div style="font-size:34px;font-weight:700;line-height:1.15">{e(cl(d["title"],34))}<br><span style="font-family:Anton,Impact,sans-serif;font-size:62px;color:#C1121F">{money(d["price"])}</span> <s style="font-size:30px;color:#777">{money(d["was"])}</s></div></div>' for d in deals)
        h = f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div><h1 class="an" style="font-size:84px;padding-bottom:20px">TOP 3 DU JOUR ⚡</h1>{rows}{foot("👉 LIEN DANS LA BIO")}</body></html>'
        br, ctx, pg = pack.render(pw, h, (1080, 1350), tmp, "img"); pg.wait_for_timeout(600)
        img = pack.OUT/f"matin-{tag}-prix.png"; pg.screenshot(path=str(img)); ctx.close(); br.close()
        fr = []
        slides = [slide(d, k) for k, d in enumerate(deals)]
        slides.append(page('<h1 class="an" style="font-size:120px;line-height:1.1;margin-top:330px">LES LIENS<br>SONT SUR LE SITE 👇</h1><h2 style="font-size:64px">rabaisflashqc.ca</h2><p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:60px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>', 1920, None, "👉 LIEN DANS LA BIO"))
        for i, s in enumerate(slides):
            br, ctx, pg = pack.render(pw, s, (1080, 1920), tmp, f"s{i}"); pg.wait_for_timeout(500)
            p = tmp/f"s{i}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
    durs = [4.0, 3.5, 3.5, 1.8]; tot = sum(durs)
    wav = tmp/"m.wav"; music.make(wav, tot+0.3, fadein=0.05)
    out = pack.OUT/f"reel-matin-{tag}-musique.mp4"
    inp, flt = [], []
    for i, p in enumerate(fr):
        inp += ["-loop", "1", "-t", str(durs[i]), "-i", str(p)]
        fi = "" if i == 0 else "fade=t=in:d=0.2,"
        flt.append(f"[{i}:v]scale=1080:1920,fps=30,{fi}fade=t=out:st={durs[i]-0.2}:d=0.2[v{i}]" if i else f"[{i}:v]scale=1080:1920,fps=30,fade=t=out:st={durs[i]-0.2}:d=0.2[v{i}]")
    n = len(fr); flt.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,format=yuv420p[o]")
    flt.append(f"[{n}:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    subprocess.run(["ffmpeg","-y",*inp,"-i",str(wav),"-filter_complex",";".join(flt),"-map","[o]","-map","[a]","-t",str(tot),"-c:a","aac","-b:a","160k","-r","30","-preset","veryfast","-c:v","libx264","-movflags","+faststart",str(out)], check=True, capture_output=True)
    print(img); print(out)
main()
