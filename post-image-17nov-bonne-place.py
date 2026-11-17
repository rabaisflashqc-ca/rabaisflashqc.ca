#!/usr/bin/env python3
"""Image Facebook du 17 nov. (1080x1350) « T'es à la bonne place » : total des économies sur 10 deals, 5 photos officielles (Best Buy, Stanley),
les 10 deals un par un en commentaire (textes : suivi/posts/2026-11-17-fb-10-deals.md). Prix : suivi/deals_chrome.json (lus le 17 nov. vers 7 h 35)."""
import json, pathlib, tempfile, sys, html as H
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import pack
from verdict import eco, eco_txt, SIGNATURE
from playwright.sync_api import sync_playwright
e = H.escape
ROOT = pathlib.Path(__file__).parent
SRC = {x["asin"]: x for x in json.load(open(ROOT / "suivi/deals_chrome.json"))}
DIX = ["B0FGYDGJ3H", "B0CWVX1GNX", "B0DCCJZC9F", "B00BTKAPUU", "B0FKVK89N5", "B0G156GM21", "B0D3JF9C6B", "B000JJIERS", "B08XTG3QSF", "B0CP9Y3152"]
PHOTOS = [("B0FGYDGJ3H", "Bose", "Casque QuietComfort"), ("B0CWVX1GNX", "Sony", "Casque ULT WEAR"), ("B0DCCJZC9F", "Oral-B", "iO Series 7"),
          ("B00BTKAPUU", "Coway", "Purificateur d'air"), ("B0CP9Y3152", "Stanley", "Quencher 40 oz")]
money = lambda v: (f"{v:,.2f}".replace(",", " ").replace(".", ",")).replace(",00", "") + " $"
CSS = """*{box-sizing:border-box;margin:0}body{width:1080px;height:1350px;overflow:hidden;font-family:'Barlow Semi Condensed',Arial,sans-serif;
background:radial-gradient(120% 80% at 50% 0,#E01E2F 0,#C1121F 45%,#7A0A16 100%);color:#fff}
.top{display:flex;align-items:center;justify-content:center;gap:12px;padding-top:34px;font-family:Anton,Impact,sans-serif;font-size:36px;letter-spacing:3px}.top b{color:#FFC72C;font-weight:400}
h1{font-family:Anton,Impact,sans-serif;font-weight:400;text-align:center;font-size:84px;line-height:1;margin-top:14px;white-space:nowrap}
.sub{text-align:center;font-family:Anton,Impact,sans-serif;font-size:44px;color:#FFC72C;margin-top:10px}
.tot{text-align:center;margin-top:20px}.tot span{display:inline-block;background:#0F7A3D;border-radius:26px;padding:12px 34px;font-family:Anton,Impact,sans-serif;font-size:66px;line-height:1.05;box-shadow:0 8px 0 rgba(0,0,0,.2)}
.g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:30px 34px 0}
.c{background:#fff;border-radius:26px;color:#1A1A1A;text-align:center;padding:14px 10px 12px;height:372px;display:flex;flex-direction:column;align-items:center}
.c img{height:175px;max-width:270px;object-fit:contain}.b{font-size:26px;font-weight:700;color:#C1121F;letter-spacing:1px;text-transform:uppercase;margin-top:6px}
.n{font-size:28px;font-weight:700;line-height:1.05}.p{font-family:Anton,Impact,sans-serif;font-size:50px;color:#C1121F;line-height:1.1;margin-top:4px}.p s{font-family:'Barlow Semi Condensed',Arial,sans-serif;font-size:24px;color:#888;margin-right:8px}
.s{margin-top:auto;background:#0F7A3D;color:#fff;border-radius:14px;padding:4px 14px;font-family:Anton,Impact,sans-serif;font-size:30px;white-space:nowrap}
.more{background:#FFC72C;color:#8E0B16;justify-content:center;font-family:Anton,Impact,sans-serif;font-size:42px;line-height:1.1;padding:12px}
.f{text-align:center;margin-top:26px;font-family:Anton,Impact,sans-serif;font-size:48px}.f small{display:block;font-family:'Barlow Semi Condensed',Arial,sans-serif;font-size:30px;color:#FFC72C;font-weight:700;margin-top:4px}
.leg{text-align:center;font-size:21px;opacity:.85;margin-top:10px}"""
def main():
    total = eco_txt(sum(int(eco(SRC[a])) for a in DIX))
    tiles = "".join(f'<div class="c"><img src="{(ROOT/"docs/img/p"/f"marque-{a}.jpg").resolve().as_uri()}"><div class="b">{e(m)}</div><div class="n">{e(n)}</div>'
                    f'<div class="p"><s>{money(SRC[a]["was"])}</s>{money(SRC[a]["price"])}</div><div class="s">TU SAUVES {eco_txt(eco(SRC[a])).replace(" ", chr(160))}</div></div>' for a, m, n in PHOTOS)
    tiles += '<div class="c more">+ 5 AUTRES<br>DEALS<br>EN<br>COMMENTAIRE<br>👇</div>'
    html = (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body><div class="top">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>'
            f'<h1>T\'ES À LA BONNE PLACE.</h1><div class="sub">10 DEALS AMAZON QUI VALENT LE CLIC</div><div class="tot"><span>{total.replace(" ", chr(160))} D\'ÉCONOMIES</span></div>'
            f'<div class="g">{tiles}</div><div class="f">rabaisflashqc.ca<small>⚡ {SIGNATURE}</small></div><div class="leg">Prix observés le 17 nov., ils peuvent changer.</div></body></html>')
    tmp = pathlib.Path(tempfile.mkdtemp()); out = pack.OUT / "post-17nov-bonne-place-10-deals.png"
    with sync_playwright() as pw:
        br, ctx, pg = pack.render(pw, html, (1080, 1350), tmp, "img"); pg.wait_for_timeout(600); pg.screenshot(path=str(out)); ctx.close(); br.close()
    print(out, total)
main()
