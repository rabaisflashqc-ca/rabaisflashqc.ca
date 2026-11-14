#!/usr/bin/env python3
"""Pack à UN deal Keepa : image 1080x1350 + réel 9:16 sans son (8 s). Sans photo (aucune photo Amazon dans nos images).
Usage : python3 outils/pack_un_deal.py AAAA-MM-JJ ASIN "ACCROCHE<br>LIGNE 2" -> docs/pack-du-jour/post-JJmois-matin.png et reel-JJmois-matin-sans-son.mp4
Prix lus dans suivi/deals_chrome.json."""
import sys, json, pathlib, tempfile, subprocess, html as H, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); import os; os.chdir(ROOT)
import pack
from playwright.sync_api import sync_playwright
e = H.escape
MOIS = ["jan","fév","mars","avr","mai","juin","juil","août","sept","oct","nov","déc"]
CSS = open('soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS += (".c{background:#fff;color:#1A1A1A;border-radius:40px;margin:40px 56px;padding:44px;text-align:center}"
        ".big{font-family:Anton,Impact,sans-serif;color:#C1121F;line-height:1}"
        ".pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:8px 30px;font-family:Anton,Impact,sans-serif;margin:16px 0}"
        ".hk{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:28px;padding:16px 36px;font-family:Anton,Impact,sans-serif;line-height:1.08}")
money = lambda p: f"{p:.2f}".replace(".", ",") + " $"
def doc(inner, h, foot):
    return (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body style="width:1080px;height:{h}px;position:relative">'
            f'<div class="top" style="padding-top:{70 if h>1500 else 30}px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}'
            f'<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">👉 rabaisflashqc.ca</div><div class="s">{foot}</div></div></body></html>')
def carte(d, hk, jour, big, hks):
    return (f'<div style="margin:30px 56px 0;text-align:center"><span class="hk" style="font-size:{hks}px">{hk}</span></div>'
            f'<div class="c"><div style="font-size:48px;font-weight:700;margin-bottom:20px">{e(d["title"])}</div>'
            f'<div class="big" style="font-size:{big}px">{money(d["price"])}</div><div class="pc" style="font-size:{big//2}px">-{d["pct"]} %</div>'
            f'<div style="font-size:44px">avant : <s>{money(d["was"])}</s></div><div style="font-size:28px;color:#555;margin-top:14px">prix observé le {jour}</div></div>')
def shot(pw, html, size, tmp, nom):
    br, ctx, pg = pack.render(pw, html, size, tmp, nom); pg.wait_for_timeout(700)
    p = tmp/f"{nom}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); return p
def main():
    date, asin, hk = sys.argv[1:4]
    d = {x["asin"]: x for x in json.load(open("suivi/deals_chrome.json"))}[asin]
    y, m, dd = map(int, date.split("-")); jour = f"{dd} {MOIS[m-1]}."; tag = f"{dd}{MOIS[m-1]}"
    tmp = pathlib.Path(tempfile.mkdtemp()); pack.OUT.mkdir(parents=True, exist_ok=True)
    fin = doc('<h1 class="an" style="font-size:120px;line-height:1.08;margin-top:260px;text-align:center">LE LIEN EST<br>SUR LE SITE 👇</h1><div style="margin:50px 56px 0;text-align:center"><span style="display:inline-block;background:#fff;color:#C1121F;border-radius:30px;padding:24px 44px;font-family:Anton,Impact,sans-serif;font-size:104px">rabaisflashqc.ca</span></div><p style="color:#fff;font-size:30px;text-align:center;padding:0 70px;margin-top:60px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>', 1920, f"Prix observé le {jour}, il peut changer")
    with sync_playwright() as pw:
        im = shot(pw, doc(carte(d, hk, jour, 170, 64), 1350, "Prix observé, il peut changer · prix final sur le site"), (1080,1350), tmp, "im")
        (pack.OUT/f"post-{tag}-matin.png").write_bytes(im.read_bytes())
        r = shot(pw, doc(carte(d, hk, jour, 210, 90), 1920, "Tous les deals avec photos sur le site"), (1080,1920), tmp, "r")
        f = shot(pw, fin, (1080,1920), tmp, "f")
    out = pack.OUT/f"reel-{tag}-matin-sans-son.mp4"
    subprocess.run(["ffmpeg","-y","-loop","1","-t","5","-i",str(r),"-loop","1","-t","3","-i",str(f),"-filter_complex",
        "[0:v]scale=1080:1920,fps=30,setsar=1[a];[1:v]scale=1080:1920,fps=30,setsar=1[b];[a][b]concat=n=2:v=1:a=0,format=yuv420p[o]",
        "-map","[o]","-an","-r","30","-preset","veryfast","-c:v","libx264","-movflags","+faststart",str(out)],check=True,capture_output=True)
    print(pack.OUT/f"post-{tag}-matin.png"); print(out)
main()
