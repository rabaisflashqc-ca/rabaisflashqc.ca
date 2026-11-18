#!/usr/bin/env python3
"""TikTok du 18 nov. : 4 visuels 1080x1920 (mode photo) + une vidéo de 12 s sans son (diaporama), 2 robots Dreame au plus bas prix jamais vu.
Textes : suivi/posts/2026-11-18-dreame.md. Palette B2. Zones sûres TikTok : rien d'important dans les 420 px du bas ni les 140 px de droite.
Usage : python3 tiktok-18nov-dreame.py [dossier des polices woff2]"""
import json, pathlib, sys, subprocess, html as H
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from verdict import eco, eco_txt, SIGNATURE
e = H.escape
ROOT = pathlib.Path(__file__).parent; OUT = ROOT / "docs/pack-du-jour"
SRC = {x["asin"]: x for x in json.load(open(ROOT / "suivi/deals_chrome.json"))}
FD = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
money = lambda v: (f"{v:,.2f}".replace(",", " ").replace(".", ",")).replace(",00", "") + " $"
face = lambda fam, f, w: f"@font-face{{font-family:'{fam}';src:url('{(FD / f).resolve().as_uri()}') format('woff2');font-weight:{w}}}" if FD else ""
CSS = (face("Anton", "anton-latin-400-normal.woff2", 400) + face("Barlow Semi Condensed", "barlow-semi-condensed-latin-600-normal.woff2", 600)
       + face("Barlow Semi Condensed", "barlow-semi-condensed-latin-700-normal.woff2", 700)) + """
*{box-sizing:border-box;margin:0}body{width:1080px;height:1920px;overflow:hidden;font-family:'Barlow Semi Condensed',Arial,sans-serif;background:#C1121F;color:#fff;padding:150px 140px 420px 70px;display:flex;flex-direction:column}
.an{font-family:Anton,Impact,sans-serif;font-weight:400}.top{display:flex;align-items:center;gap:12px;font-size:40px;letter-spacing:3px}.top b{color:#FFD23F;font-weight:400}
.pill{align-self:flex-start;background:#FFD23F;color:#5A0A10;border-radius:999px;padding:10px 28px;font-size:38px;font-weight:700;margin-top:40px}
h1{font-size:170px;line-height:.98;margin-top:30px}h1 span{color:#FFD23F}.sub{font-size:64px;font-weight:700;line-height:1.15;margin-top:30px}
.card{margin-top:40px;background:#FFF7E8;border-radius:36px;color:#1A1A1A;padding:30px;display:flex;flex-direction:column;align-items:center;text-align:center;flex:1}
.ph{width:100%;height:560px;background:#fff;border-radius:26px;display:flex;align-items:center;justify-content:center}.ph img{max-height:520px;max-width:92%;object-fit:contain}
.b{font-size:34px;font-weight:700;color:#C1121F;letter-spacing:3px;margin-top:22px}.n{font-size:76px;line-height:1.02}.rec{margin-top:16px;background:#2A0508;color:#FFD23F;border-radius:14px;padding:8px 20px;font-size:34px;font-weight:700}
.p{font-size:120px;color:#C1121F;line-height:1.05;margin-top:16px}.w{font-size:42px;font-weight:600;color:#6B6560;text-decoration:line-through}
.s{margin-top:auto;background:#146C34;color:#fff;border-radius:20px;padding:10px 30px;font-size:62px}
.u{align-self:flex-start;background:#FFC21A;color:#2A0508;border-radius:999px;padding:16px 46px;font-size:76px;margin-top:50px}.sig{font-size:44px;font-weight:700;margin-top:24px}"""
TOP = '<div class="top an"><svg width="32" height="52" viewBox="0 0 100 160" aria-hidden="true"><path d="M62 0 L8 92 L44 92 L28 160 L94 58 L58 58 L78 0 Z" fill="#FFD23F"/></svg><span>RABAIS <b>FLASH</b> QC</span></div>'
def card(a, n):
    x = SRC[a]
    return (f'{TOP}<div class="card"><div class="ph"><img src="{(ROOT / "docs/img/p" / f"{a}.jpg").resolve().as_uri()}"></div><div class="b">DREAME</div><div class="n an">{e(n)}</div>'
            f'<div class="rec">📉 PLUS BAS PRIX JAMAIS VU</div><div class="p an">{money(x["price"])}</div><div class="w">{money(x["was"])}</div>'
            f'<div class="s an">TU SAUVES {eco_txt(eco(x)).replace(" ", chr(160))}</div></div>')
SLIDES = [
    ("1-accroche", f'{TOP}<div style="margin:auto 0;display:flex;flex-direction:column"><span class="pill">🔥 PRIX PRÉ-VENDREDI FOU</span><h1 class="an">JAMAIS VU<br><span>AUSSI BAS</span></h1>'
                   f'<div class="sub">2 robots Dreame qui aspirent ET lavent.<br>Jusqu\'à 200 $ de moins.</div><div class="sub" style="color:#FFD23F">Lequel tu prends? 👉</div></div>'),
    ("2-l40", card("B0FSJPFDPV", "L40 Ultra Gen 2")),
    ("3-d20", card("B0G5Y3LN8M", "D20 Air Plus")),
    ("4-site", f'{TOP}<div style="margin:auto 0;display:flex;flex-direction:column"><h1 class="an" style="font-size:130px">1 OU 2?<br><span>DIS-LE EN COMMENTAIRE</span></h1>'
               f'<div class="sub">Les liens sont sur le site :</div><span class="u an">rabaisflashqc.ca</span><div class="sig">⚡ {e(SIGNATURE)}</div></div>'),
]
def main():
    files = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(**({"executable_path": "/usr/bin/google-chrome"} if pathlib.Path("/usr/bin/google-chrome").exists() else {}))
        pg = br.new_page(viewport={"width": 1080, "height": 1920})
        for name, body in SLIDES:
            tmp = ROOT / "suivi" / f".tt-{name}.html"; tmp.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
            pg.goto(tmp.resolve().as_uri()); pg.wait_for_timeout(700)
            out = OUT / f"tiktok-18nov-dreame-{name}.png"; pg.screenshot(path=str(out)); tmp.unlink(); files.append(out)
        br.close()
    # Vidéo : 2,5 s + 3,5 s + 3,5 s + 2,5 s, fondus de 0,4 s, sans son (ajouter un son tendance dans TikTok)
    d = [2.9, 3.9, 3.9, 2.9]; inp = sum((["-loop", "1", "-t", str(t), "-i", str(f)] for f, t in zip(files, d)), [])
    off, chain, prev = 0, [], "0:v"
    for i in range(1, 4):
        off += d[i - 1] - 0.4
        chain.append(f"[{prev}][{i}:v]xfade=transition=slideleft:duration=0.4:offset={off:.2f}[v{i}]"); prev = f"v{i}"
    vid = OUT / "tiktok-18nov-dreame-sans-son.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-filter_complex", ";".join(chain) + f";[{prev}]format=yuv420p,fps=30[out]", "-map", "[out]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-movflags", "+faststart", str(vid)], check=True)
    print(*files, vid, sep="\n")
main()
