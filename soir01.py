#!/usr/bin/env python3
"""Pack du soir 1er nov. : 4 deals sous 45 $ avec vraies photos des produits.
Image 1080x1350 + réel 9:16 (musique originale music.py, -14 LUFS, accroche dès la 1re image)."""
import base64, pathlib, subprocess, tempfile, html as H
import music
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs" / "pack-du-jour"
e = H.escape
FONT = base64.b64encode(pathlib.Path("/tmp/fnt/package/files/anton-latin-400-normal.woff2").read_bytes()).decode()
def img64(stem): return "data:image/jpeg;base64," + base64.b64encode((ROOT / "docs/img/p" / f"{stem}.jpg").read_bytes()).decode()

# (marque, produit, photo, prix, avant, %, date du prix)
PICK = [("UGREEN", "Chargeur Nexode 65 W, 3 ports", "B091BGMKYS-2", "25,99 $", "35,99 $", 28, "28 oct."),
        ("Winix", "Filtre A pour purificateur d'air", "B0GNC8FQS7-2", "42,73 $", "91,00 $", 53, "29 oct."),
        ("Splendor Kids", "Jeu de société pour enfants", "B0FKJT8TFG-2", "22,42 $", "34,44 $", 35, "29 oct."),
        ("Anker soundcore", "Écouteurs ouverts V20i, 36 h", "B0D31C567W-2", "35,99 $", "59,99 $", 40, "26 oct.")]

CSS = f"""@font-face{{font-family:Anton;src:url(data:font/woff2;base64,{FONT})}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:Inter,"DejaVu Sans",sans-serif;color:#fff;
background:radial-gradient(ellipse at 50% 35%,#D7192A 0%,#A50F1E 60%,#5E0812 100%);overflow:hidden}}
.an{{font-family:Anton,Impact,sans-serif;font-weight:400}}.y{{color:#FFC72C}}
.brand{{display:flex;align-items:center;justify-content:center;gap:12px;font-weight:800;letter-spacing:4px;font-size:34px;padding-top:44px}}
.foot{{position:absolute;left:0;right:0;bottom:0;background:#FFC72C;color:#7A0A16;text-align:center;padding:22px 0}}
.foot b{{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:54px;display:block}}.foot span{{font-size:24px;font-weight:700}}"""
BOLT = '<svg width="30" height="48" viewBox="0 0 100 160"><path d="M62 0 L8 92 L44 92 L28 160 L94 58 L58 58 L78 0 Z" fill="#FFC72C"/></svg>'
BRAND = f'<div class="brand">{BOLT}<span>RABAIS <span class="y">FLASH</span> QC</span></div>'

def image():
    rows = "".join(f'''<div style="display:flex;gap:22px;align-items:center;background:#fff;color:#1a1a1a;border-radius:28px;padding:14px 22px;margin:0 50px 14px">
<img src="{img64(ph)}" style="width:170px;height:170px;object-fit:contain;border-radius:16px;background:#fff;flex:none">
<div style="flex:1"><div style="color:#C1121F;font-weight:800;font-size:24px;text-transform:uppercase">{e(b)}</div>
<div style="font-weight:700;font-size:30px;line-height:1.1;margin:2px 0 6px">{e(t)}</div>
<div><span class="an" style="font-size:52px;color:#C1121F">{p}</span> <s style="font-size:26px;color:#777">{o}</s></div>
<div style="font-size:19px;color:#666">prix du {d}</div></div>
<div class="an" style="background:#FFC72C;color:#7A0A16;border-radius:22px;padding:10px 18px;font-size:50px;flex:none">-{pc}%</div></div>''' for b, t, ph, p, o, pc, d in PICK)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="width:1080px;height:1350px;position:relative">
{BRAND}<h1 class="an y" style="text-align:center;font-size:92px;line-height:1;margin:18px 0 6px">4 DEALS SOUS 45 $ 🔥</h1>
<p style="text-align:center;font-size:32px;font-weight:700;margin-bottom:22px">Le Top du soir, choisi pour toi</p>{rows}
<div class="foot"><b>👉 LIEN DANS LA BIO</b><span>Tous les deals sur rabaisflashqc.ca</span></div></body></html>'''

def slide(inner):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="width:1080px;height:1920px;position:relative">
<div style="padding-top:60px">{BRAND}</div>{inner}<div class="foot"><b>👉 LIEN DANS LA BIO</b><span>rabaisflashqc.ca</span></div></body></html>'''

def slides():
    s = [(slide('<h1 class="an" style="text-align:center;font-size:150px;line-height:1.02;margin-top:300px">4 DEALS<br><span class="y">SOUS 45 $</span> 🔥</h1>'
                '<p style="text-align:center;font-size:58px;font-weight:800;margin-top:30px">Le Top du soir 👀</p>'), 6)]
    for b, t, ph, p, o, pc, d in PICK:
        s.append((slide(f'''<div style="margin:70px 70px 0;background:#fff;border-radius:44px;padding:40px;text-align:center;color:#1a1a1a">
<img src="{img64(ph)}" style="width:620px;height:620px;object-fit:contain">
<div style="color:#C1121F;font-weight:800;font-size:38px;text-transform:uppercase;margin-top:10px">{e(b)}</div>
<div style="font-weight:700;font-size:46px;line-height:1.1;margin:6px 0 12px">{e(t)}</div>
<div><span class="an" style="font-size:150px;color:#C1121F;line-height:1">{p}</span></div>
<div style="margin-top:10px"><span class="an" style="background:#FFC72C;color:#7A0A16;border-radius:24px;padding:6px 30px;font-size:90px">-{pc}%</span>
<s style="font-size:46px;color:#777;margin-left:18px">{o}</s></div>
<div style="font-size:28px;color:#666;margin-top:16px">prix du {d}</div></div>'''), 5))
    s.append((slide('<h1 class="an" style="text-align:center;font-size:118px;line-height:1.1;margin-top:330px">LEQUEL<br>TU PRENDS?<br><span class="y">1, 2, 3 OU 4</span> 👇</h1>'
                    '<p style="text-align:center;font-size:52px;font-weight:800;margin-top:40px">Dis-le en commentaire!</p>'), 6))
    s.append((slide('<h1 class="an" style="text-align:center;font-size:120px;line-height:1.1;margin-top:330px">TOUS LES DEALS<br><span class="y">SUR LE SITE</span> 👇</h1>'
                    '<p style="text-align:center;font-size:62px;font-weight:800;margin-top:30px">rabaisflashqc.ca</p>'
                    '<p style="text-align:center;font-size:28px;padding:0 90px;margin-top:70px">En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises.</p>'), 6))
    return s

if __name__ == "__main__":
    tmp = pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1350}); pg.set_content(image()); pg.wait_for_timeout(500)
        pg.screenshot(path=str(OUT / "soir-01nov-photos.png")); pg.close()
        fr = []
        for i, (h, _) in enumerate(slides()):
            pg = br.new_page(viewport={"width": 1080, "height": 1920}); pg.set_content(h); pg.wait_for_timeout(400)
            p = tmp / f"s{i}.png"; pg.screenshot(path=str(p)); pg.close(); fr.append(p)
        br.close()
    BPM = 124; B = 60 / BPM
    durs = [n * B for _, n in slides()]; total = sum(durs)
    raw = music.make(tmp / "m.wav", total + 0.2, bpm=BPM, fadein=0); norm = tmp / "mn.wav"
    subprocess.run(["ffmpeg", "-y", "-i", str(raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", str(norm)], check=True, capture_output=True)
    inp, flt = [], []
    for i, (p, d) in enumerate(zip(fr, durs)):
        inp += ["-loop", "1", "-t", f"{d:.4f}", "-i", str(p)]; flt.append(f"[{i}:v]scale=1080:1920,fps=30,setsar=1[v{i}]")
    n = len(fr); flt.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,format=yuv420p[o]")
    out = OUT / "reel-soir-01nov-musique.mp4"
    subprocess.run(["ffmpeg", "-y", *inp, "-i", str(norm), "-filter_complex", ";".join(flt), "-map", "[o]", "-map", f"{n}:a", "-t", f"{total:.3f}",
                    "-c:a", "aac", "-b:a", "192k", "-r", "30", "-preset", "veryfast", "-c:v", "libx264", "-movflags", "+faststart", str(out)], check=True, capture_output=True)
    print(out, round(total, 2))
