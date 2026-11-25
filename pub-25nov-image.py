import json,pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent
deals={d["asin"]:d for d in json.load(open(ROOT/"suivi/deals_chrome.json"))}
idx=json.load(open(ROOT/"docs/recherche.json")); NTXT=f"{len(idx):,}".replace(",", " ")
money=lambda p:(f"{p:,.2f}".replace(",", " ").replace(".", ",") if p%1 else f"{p:,.0f}".replace(",", " "))+" $"
P=[("B0HDVVDGZW","Dyson Airwrap"),("B0DN45YMP6","JBL Vibe Beam 2"),("B0CHBNXJ24","Ninja CREAMi XL"),("B0G2STSGW3","LEGO Star Wars"),("B08DJ8Z3WH","Shark Navigator"),("B0BWWZP49F","Blink Mini 2")]
cards="".join(f'<div class="c"><div class="b">-{deals[a]["pct"]} %</div><img src="{(ROOT/f"docs/img/p/marque-{a}.jpg").resolve().as_uri()}"><div class="n">{n}</div><div class="p">{money(deals[a]["price"])}</div></div>' for a,n in P)
h=f'''<!doctype html><meta charset=utf-8><style>*{{box-sizing:border-box;margin:0;padding:0}}body{{width:1080px;height:1350px;background:#C1121F;font-family:'Liberation Sans Narrow',Arial Narrow,Arial,sans-serif;font-weight:700;text-align:center;position:relative;overflow:hidden}}
.an{{font-family:Anton,Impact,sans-serif;font-weight:400}}
.c{{background:#fff;border-radius:28px;width:320px;height:290px;position:relative;padding:14px 10px;box-shadow:0 8px 0 #8E0B16}}.c img{{width:250px;height:150px;object-fit:contain}}
.b{{position:absolute;top:-16px;right:-12px;background:#FFC21A;color:#8E0B16;font-family:Anton,Impact,sans-serif;font-size:46px;border-radius:18px;padding:2px 16px;transform:rotate(4deg)}}
.n{{font-size:30px;color:#3D0A10}}.p{{font-family:Anton,Impact,sans-serif;font-size:54px;color:#C1121F}}
.g{{display:grid;grid-template-columns:repeat(3,320px);gap:30px 22px;justify-content:center;margin-top:26px}}</style>
<div style="padding-top:26px"><div class="an" style="font-size:50px;color:#FFE4B0;letter-spacing:1px">VENDREDI FOU : TU NE RATERAS RIEN</div><div class="an" style="font-size:196px;color:#FFC21A;line-height:1;text-shadow:6px 6px 0 #8E0B16">6 000+ DEALS</div>
<div class="an" style="font-size:70px;color:#fff;line-height:1.05">RABAIS MOYEN : <span style="color:#FFC21A">34 %</span></div>
<div style="font-size:40px;color:#FFE4B0;margin-top:8px">dont plus de <b style="color:#fff">4 600 à -30 % et plus</b> · 3 900 sous 50 $</div>
<div style="width:900px;margin:16px auto 0;background:#fff;border:6px solid #FFC21A;border-radius:60px;padding:10px 34px;font-size:40px;color:#3D0A10;display:flex;justify-content:space-between;align-items:center"><span>🔎 Tape ton produit ici</span><i style="font-style:normal;background:#FFC21A;border-radius:40px;padding:4px 24px;font-size:36px">Trouve-moi un deal</i></div></div>
<div class=g>{cards}</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:150px;background:#3D0A10;color:#fff;padding-top:14px"><div class="an" style="font-size:64px;color:#FFC21A">rabaisflashqc.ca</div><div style="font-size:28px;margin-top:0">{NTXT} deals triés pour le Québec · les prix peuvent changer</div></div>'''
p=pathlib.Path("/tmp/pub.html");p.write_text(h)
with sync_playwright() as pw:
    b=pw.chromium.launch();pg=b.new_page(viewport={"width":1080,"height":1350});pg.goto(p.as_uri());pg.wait_for_timeout(500);pg.screenshot(path=str(ROOT/"docs/pack-du-jour/pub-25nov-image-v2.png"));b.close()
