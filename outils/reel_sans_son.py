#!/usr/bin/env python3
"""Réel 9:16 sans son (12 à 14 s), 1 deal par écran, prix choc dès la 1re image. Prix = suivi/deals_chrome.json (Keepa). Aucune photo.
Usage : python3 outils/reel_sans_son.py NOM "ACCROCHE (<br> permis)" ASIN1 ASIN2 ASIN3 ASIN4  -> docs/pack-du-jour/reel-NOM.mp4
Dernier écran : « prix lus le JJ nov. à H h MM » (heure seen réelle du premier deal)."""
import sys, json, pathlib, tempfile, subprocess, html as H
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import pack
from playwright.sync_api import sync_playwright
e = H.escape
CSS = open(ROOT/'soir_flash.py').read().split('CSS = """')[1].split('"""')[0]
CSS += (".c{background:#fff;color:#1A1A1A;border-radius:40px;margin:30px 56px;padding:54px 40px;text-align:center}"
        ".big{font-family:Anton,Impact,sans-serif;font-size:230px;color:#C1121F;line-height:1}"
        ".pc{display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:26px;padding:8px 34px;font-family:Anton,Impact,sans-serif;font-size:110px;margin:14px 0}"
        ".hk{font-family:Anton,Impact,sans-serif;font-size:88px;line-height:1.05;text-align:center;color:#FFC72C;margin:50px 50px 0}")
money = lambda p: f"{p:.2f}".replace(".", ",") + " $"
def doc(inner, foot="👉 RABAISFLASHQC.CA"):
    return (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}body{{height:1920px!important}}</style></head><body>'
            f'<div class="top" style="padding-top:90px">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>{inner}'
            f'<div class="foot" style="position:absolute;bottom:0;left:0;right:0"><div class="u an">{foot}</div><div class="s">rabaisflashqc.ca · prix vérifié, peut changer</div></div></body></html>')
def carte(d, k=None, n=None):
    t = d["short"]
    bad = f'<div style="font-size:44px;font-weight:700;color:#8E0B16">{k}/{n}</div>' if k else ""
    return (f'<div class="c">{bad}<div style="font-size:54px;font-weight:700;margin:0 0 18px">{e(t)}</div><div class="big">{money(d["price"])}</div>'
            f'<div class="pc">-{d["pct"]} %</div><div style="font-size:52px">au lieu de <s>{money(d["was"])}</s></div></div>')
def main():
    nom, accroche, asins = sys.argv[1], sys.argv[2], sys.argv[3:]
    src = {d["asin"]: d for d in json.load(open(ROOT/"suivi/deals_chrome.json"))}
    deals = []
    for a in asins:
        d = dict(src[a]); assert d.get("source") == "keepa", a
        d["short"] = d["title"] if len(d["title"]) <= 34 else d["title"][:34].rsplit(" ", 1)[0]
        deals.append(d)
    seen = deals[0]["seen"]; h, mi = int(seen[11:13]), seen[14:16]
    lu = f'Prix lus sur Keepa le {int(seen[8:10])} nov. à {h} h {mi}'
    d0 = deals[0]
    slides = [(doc(f'<div class="hk">{accroche}</div>{carte(d0)}'), 2.4)]
    n = len(deals)
    slides += [(doc(f'<div class="hk" style="font-size:70px">{money(d["price"])} AU LIEU DE {money(d["was"])}</div>{carte(d, k, n)}'), 2.4) for k, d in enumerate(deals[1:], 2)]
    slides.append((doc('<h1 class="an" style="font-size:120px;line-height:1.1;margin-top:330px;text-align:center">LES LIENS<br>SONT SUR LE SITE 👇</h1>'
                       '<h2 style="font-size:70px;text-align:center">rabaisflashqc.ca</h2>'
                       f'<p style="color:#fff;font-size:34px;text-align:center;padding:0 70px;margin-top:50px">{lu}. Les prix peuvent changer.</p>'
                       '<p style="color:#fff;font-size:28px;text-align:center;padding:0 70px;margin-top:30px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>',
                       "👉 LIEN DANS LA BIO"), 2.6))
    tmp = pathlib.Path(tempfile.mkdtemp()); fr = []
    with sync_playwright() as pw:
        for i, (hh, _) in enumerate(slides):
            br, ctx, pg = pack.render(pw, hh, (1080, 1920), tmp, f"s{i}"); pg.wait_for_timeout(500)
            p = tmp/f"s{i}.png"; pg.screenshot(path=str(p)); ctx.close(); br.close(); fr.append(p)
    inp, flt = [], []
    for i, (p, (_, dur)) in enumerate(zip(fr, slides)):
        inp += ["-loop", "1", "-t", str(dur), "-i", str(p)]; flt.append(f"[{i}:v]scale=1080:1920,setsar=1,fps=30[v{i}]")
    tot = sum(d for _, d in slides)
    flt.append("".join(f"[v{i}]" for i in range(len(fr))) + f"concat=n={len(fr)}:v=1:a=0,format=yuv420p[o]")
    out = pack.OUT/f"reel-{nom}.mp4"
    subprocess.run(["ffmpeg","-y",*inp,"-filter_complex",";".join(flt),"-map","[o]","-t",str(tot),"-an","-r","30","-preset","veryfast","-c:v","libx264","-movflags","+faststart",str(out)], check=True, capture_output=True)
    print(out, tot, "s")
main()
