#!/usr/bin/env python3
"""Posts Facebook par marque (Vendredi fou) : image 1080x1350, texte, commentaires (1 lien par commentaire)."""
import json, re, pathlib, tempfile, html as H
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
D = json.load(open(ROOT/"suivi/posts/2026-11-27-marques-items.json"))
IMG = json.load(open("/mnt/user-data/uploads/Downloads/IMG-marques.json"))
OUT = ROOT/"suivi/posts/marques-27nov"; OUT.mkdir(parents=True, exist_ok=True)
e = H.escape
money = lambda p: (f"{p:,.2f}".replace(",", " ").replace(".", ",") if p % 1 else f"{p:,.0f}".replace(",", " ")) + " $"
META = {
 "LEGO":("🧱","LEGO","Speed Champions, Minecraft, Classic, Pokémon : de quoi gâter les petits (et les grands).","#E3000B"),
 "Ninja":("🍳","NINJA","Friteuses à air, mélangeurs, autocuiseurs : la cuisine des fêtes à prix doux.","#1B1B1B"),
 "JBL":("🎧","JBL","Écouteurs, casques et enceintes jusqu'à -64 %. Le son qui fait plaisir à tout le monde.","#F26B1D"),
 "Columbia":("🧥","COLUMBIA","Du plein air pour affronter l'hiver québécois sans se ruiner.","#00508F"),
 "adidas":("👟","ADIDAS","Souliers, sandales et pantalons à des prix qu'on ne voit pas souvent.","#111111"),
 "Philips":("🪥","PHILIPS","Brosses à dents Sonicare, soins, bébé : les essentiels en rabais.","#0B5ED7"),
 "Samsung":("📱","SAMSUNG","Écouteurs, écrans, barre de son : la techno Samsung à prix réduit.","#1428A0"),
 "Amazon":("📦","AMAZON","Fire TV, Echo, Kindle, Blink : les appareils Amazon jusqu'à -67 %.","#146EB4"),
 "L'Oréal":("💄","L'ORÉAL","Mascaras, soins du visage, cheveux : la beauté L'Oréal en rabais.","#B8860B"),
 "Maybelline":("💋","MAYBELLINE","Les mascaras et le maquillage que tout le monde achète, en rabais.","#D6006E"),
 "CeraVe":("🧴","CERAVE","Hydratants et nettoyants pour la peau : les incontournables du moment.","#1565C0"),
 "Garnier":("🌿","GARNIER","Sérums, eau micellaire, soins cheveux : les rabais Garnier à saisir.","#2E8B3A"),
}
ORDER = ["JBL","LEGO","Ninja","L'Oréal","Amazon","Philips","Maybelline","Samsung","CeraVe","Columbia","Garnier","adidas"]
def clean(t, n=58):
    t = re.sub(r"\s+", " ", t.replace("olumbia olumbia","Columbia")).strip()
    t = re.sub(r"[®™]", "", t)
    t = re.split(r" [–-] | : ", t)[0] if len(t) > n else t
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",.:;") + "…"
CSS = """*{box-sizing:border-box;margin:0;padding:0}body{width:1080px;height:1350px;overflow:hidden;font-family:'Liberation Sans Narrow','Arial Narrow',Arial,sans-serif;font-weight:700;background:#FFF7E8;color:#1A1A1A;position:relative}
.an{font-family:Anton,Impact,'Arial Narrow Bold',sans-serif;font-weight:400}"""
def page(b, items):
    emo, name, _, col = META[b]
    tiles = ""
    for x in items[:6]:
        tiles += (f'<div style="background:#fff;border-radius:26px;position:relative;height:276px;box-shadow:0 5px 0 #E8D9BC;text-align:center;padding-top:12px">'
                  f'<img src="{IMG[x["asin"]]}" style="height:160px;max-width:260px;object-fit:contain">'
                  f'<div class="an" style="position:absolute;top:-12px;left:-8px;background:#FFC21A;color:#8E0B16;border-radius:16px;padding:2px 14px;font-size:38px;transform:rotate(-4deg)">-{x["pct"]} %</div>'
                  f'<div class="an" style="font-size:48px;color:#C1121F;margin-top:4px">{money(x["p"])}</div>'
                  f'<div style="font-size:23px;color:#666;text-decoration:line-through;margin-top:-2px">{money(x["w"])}</div></div>')
    n = len(items)
    mx = max(x["pct"] for x in items)
    sz = 190 if len(name) <= 7 else 150 if len(name) <= 9 else 120
    return f"""<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>
<div style="position:absolute;top:0;left:0;right:0;height:250px;background:#C1121F;border-bottom:8px solid #FFC21A;text-align:center;padding-top:26px">
<div class="an" style="font-size:78px;color:#FFC21A;letter-spacing:2px;line-height:1">RABAISFLASHQC.CA</div>
<div style="margin:16px auto 0;width:820px;background:#fff;border:5px solid #FFC21A;border-radius:50px;padding:10px 30px;font-size:38px;color:#3D0A10;display:flex;justify-content:space-between;align-items:center;white-space:nowrap"><span>🔎 Tape ton produit ici</span><i style="font-style:normal;background:#FFC21A;border-radius:30px;padding:4px 22px;font-size:32px">Trouve-moi un deal</i></div>
<div style="color:#fff;font-size:30px;margin-top:10px">La barre de recherche qui nous différencie</div></div>
<div style="position:absolute;top:262px;left:0;right:0;height:352px;background:{col};text-align:center;padding-top:16px">
<div style="font-size:40px;color:#FFE4B0;letter-spacing:3px">VENDREDI FOU · À SAISIR</div>
<div class="an" style="font-size:{sz}px;color:#fff;line-height:1.05;text-shadow:0 6px 0 rgba(0,0,0,.25)">{emo} {e(name)}</div>
<div style="display:inline-block;background:#FFC21A;color:#8E0B16;border-radius:30px;padding:4px 30px;font-size:46px;margin-top:10px" class="an">JUSQU'À -{mx} %</div></div>
<div style="position:absolute;top:636px;left:34px;right:34px;display:grid;grid-template-columns:repeat(3,1fr);gap:20px 20px">{tiles}</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:130px;background:#3D0A10;text-align:center;padding-top:16px;color:#fff">
<div class="an" style="font-size:54px;color:#FFC21A">{n} LIENS EN COMMENTAIRE 👇</div><div style="font-size:30px;margin-top:2px">Le site québécois de référence en aubaines · 27 au 30 nov.</div></div></body></html>"""
def texte(b, items):
    emo, name, hook, _ = META[b]; mx = max(x["pct"] for x in items); n = len(items)
    nm = {"adidas":"adidas","L'Oréal":"L'Oréal"}.get(b, b)
    return (f"{emo} {name} EN RABAIS : VENDREDI FOU À SAISIR!\n\n{hook}\nJusqu'à -{mx} % sur {n} produits choisis pour toi. 👀\n\n"
            f"🔎 Tu veux plus de {nm}? Tape-le dans la BARRE DE RECHERCHE sur rabaisflashqc point ca et vois le rabais en 5 secondes. Fini de fouiller 40 pages!\n\n"
            f"👇 Les {n} liens directs sont dans les commentaires, un produit par commentaire.\n\n"
            "❤️ Aime ce post pour le retrouver\n💬 Dis-moi ce que tu cherches en commentaire\n🔁 Partage à quelqu'un qui magasine ce week-end\n\n"
            "⚡ Le site québécois de référence en aubaines. Viens économiser!\n\n"
            "En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises. Les prix peuvent changer.\n\n"
            f"#VendrediFou #BlackFriday #{re.sub(r'[^A-Za-z0-9]','',b)} #Aubaines #Québec")
def comments(b, items):
    emo = META[b][0]
    return [f"{emo} {clean(x['t'])} : {money(x['p'])} (-{x['pct']} %)\n👉 https://www.amazon.ca/dp/{x['asin']}?tag=coupdecoeurqc-20" for x in items]
tmp = pathlib.Path(tempfile.mkdtemp()); meta = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for i, b in enumerate(ORDER):
        items = D[b]
        slug = re.sub(r"[^a-z0-9]", "", b.lower().replace("é","e"))
        p = tmp/f"{slug}.html"; p.write_text(page(b, items))
        pg = br.new_page(viewport={"width":1080,"height":1350}); pg.goto(p.as_uri()); pg.wait_for_timeout(300)
        pg.screenshot(path=str(OUT/f"{i+1:02d}-{slug}.png")); pg.close()
        (OUT/f"{i+1:02d}-{slug}-texte.txt").write_text(texte(b, items))
        json.dump(comments(b, items), open(OUT/f"{i+1:02d}-{slug}-commentaires.json","w"), ensure_ascii=False, indent=1)
        meta.append(dict(n=i+1, brand=b, slug=slug, count=len(items)))
    br.close()
json.dump(meta, open(OUT/"index.json","w"), indent=1); print(meta)
