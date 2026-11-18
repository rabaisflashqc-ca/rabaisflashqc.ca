#!/usr/bin/env python3
"""Image Facebook et Instagram du 18 nov. (1080x1350) : 2 robots Dreame au plus bas prix jamais vu (Keepa, 18 nov. 16 h 25).
Textes : suivi/posts/2026-11-18-dreame.md. Photos : docs/img/p/ (vérifiées à l'oeil). Palette B2 (rouge franc, crème, jaune = action, vert = économie).
Polices : passer le dossier des fichiers woff2 Anton et Barlow Semi Condensed en argument si Google Fonts n'est pas joignable."""
import json, pathlib, sys, html as H
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from verdict import eco, eco_txt, SIGNATURE
e = H.escape
ROOT = pathlib.Path(__file__).parent
SRC = {x["asin"]: x for x in json.load(open(ROOT / "suivi/deals_chrome.json"))}
DEALS = [("B0FSJPFDPV", "L40 Ultra Gen 2", "Station tout-en-un, 25 000 Pa"), ("B0G5Y3LN8M", "D20 Air Plus", "Auto-vidage 120 jours, 20 000 Pa")]
FD = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
money = lambda v: (f"{v:,.2f}".replace(",", " ").replace(".", ",")).replace(",00", "") + " $"
def face(fam, f, w):
    return f"@font-face{{font-family:'{fam}';src:url('{(FD / f).resolve().as_uri()}') format('woff2');font-weight:{w}}}" if FD else ""
FONTS = (face("Anton", "anton-latin-400-normal.woff2", 400) + face("Barlow Semi Condensed", "barlow-semi-condensed-latin-600-normal.woff2", 600)
         + face("Barlow Semi Condensed", "barlow-semi-condensed-latin-700-normal.woff2", 700))
CSS = FONTS + """*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;overflow:hidden;font-family:'Barlow Semi Condensed',Arial,sans-serif;background:#C1121F;color:#fff}
.an{font-family:Anton,Impact,sans-serif;font-weight:400}
.top{display:flex;align-items:center;justify-content:center;gap:12px;padding-top:36px;font-size:38px;letter-spacing:3px}.top b{color:#FFD23F;font-weight:400}
.rec{display:block;width:max-content;margin:22px auto 0;background:#FFD23F;color:#5A0A10;border-radius:999px;padding:8px 26px;font-size:34px;font-weight:700}
h1{text-align:center;font-size:104px;line-height:1;margin-top:14px}h1 span{color:#FFD23F}
.sub{text-align:center;font-size:42px;font-weight:700;margin-top:8px}
.g{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin:34px 40px 0}
.c{background:#FFF7E8;border-radius:30px;color:#1A1A1A;text-align:center;padding:22px 18px 22px;height:690px;display:flex;flex-direction:column;align-items:center;box-shadow:0 14px 30px rgba(80,0,8,.35)}
.ph{width:100%;height:330px;background:#fff;border-radius:22px;display:flex;align-items:center;justify-content:center}.ph img{max-height:300px;max-width:90%;object-fit:contain}
.b{font-size:28px;font-weight:700;color:#C1121F;letter-spacing:2px;margin-top:16px}.n{font-size:50px;line-height:1.05;margin-top:2px}.d{font-size:26px;font-weight:600;color:#5A534D;margin-top:4px}
.p{font-size:74px;color:#C1121F;line-height:1.05;margin-top:10px}.w{margin-top:2px;font-size:30px;font-weight:600;color:#6B6560;text-decoration:line-through}
.s{margin-top:auto;background:#146C34;color:#fff;border-radius:16px;padding:8px 22px;font-size:40px;white-space:nowrap}
.f{text-align:center;margin-top:40px}.f .u{display:inline-block;background:#FFC21A;color:#2A0508;border-radius:999px;padding:12px 40px;font-size:52px}.f small{display:block;font-size:30px;font-weight:700;margin-top:14px}"""
BOLT = '<svg width="30" height="48" viewBox="0 0 100 160" aria-hidden="true"><path d="M62 0 L8 92 L44 92 L28 160 L94 58 L58 58 L78 0 Z" fill="#FFD23F"/></svg>'
def main():
    tiles = "".join(f'<div class="c"><div class="ph"><img src="{(ROOT / "docs/img/p" / f"{a}.jpg").resolve().as_uri()}"></div><div class="b">DREAME</div>'
                    f'<div class="n an">{e(n)}</div><div class="d">{e(d)}</div><div class="p an">{money(SRC[a]["price"])}</div><div class="w">{money(SRC[a]["was"])}</div>'
                    f'<div class="s an">TU SAUVES {eco_txt(eco(SRC[a])).replace(" ", chr(160))}</div></div>' for a, n, d in DEALS)
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="top an">{BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>'
            f'<span class="rec">🔥 PRIX PRÉ-VENDREDI FOU</span><h1 class="an">JAMAIS VU <span>AUSSI BAS</span></h1><div class="sub">2 robots Dreame qui aspirent ET lavent</div>'
            f'<div class="g">{tiles}</div><div class="f"><span class="u an">rabaisflashqc.ca</span><small>⚡ {SIGNATURE}</small></div></body></html>')
    out = ROOT / "docs/pack-du-jour/post-18nov-dreame.png"
    with sync_playwright() as pw:
        br = pw.chromium.launch(**({"executable_path": "/usr/bin/google-chrome"} if pathlib.Path("/usr/bin/google-chrome").exists() else {}))
        pg = br.new_page(viewport={"width": 1080, "height": 1350})
        tmp = ROOT / "suivi" / ".post-18nov-dreame.html"; tmp.write_text(html)
        pg.goto(tmp.resolve().as_uri()); pg.wait_for_timeout(800); pg.screenshot(path=str(out)); br.close(); tmp.unlink()
    print(out)
main()
