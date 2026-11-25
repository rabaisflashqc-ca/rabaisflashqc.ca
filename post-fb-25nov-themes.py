#!/usr/bin/env python3
"""Post FB 25 nov : image forte + commentaires (50 a 60 produits par theme, liens affilies). Sortie suivi/posts/2026-11-25-fb-themes.json"""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
D = json.load(open(ROOT/"suivi/deals_chrome.json"))
TAG = "coupdecoeurqc-20"
THEMES = [("maison","🏠 MAISON ET CUISINE"),("tech","💻 TECH ET AUDIO"),("beaute","✨ BEAUTÉ ET SOINS"),("femme","👗 POUR ELLE"),
          ("homme","🧔 POUR LUI"),("jouets","🧸 JOUETS ET JEUX"),("plein-air","🏕️ SPORT ET PLEIN AIR"),("animaux","🐶 ANIMAUX"),("enfants","👶 BÉBÉ ET ENFANTS")]
money = lambda p: (f"{p:,.2f}".replace(",", " ").replace(".", ",") if abs(p-round(p))>0.001 else f"{p:,.0f}".replace(",", " ")) + " $"
def clean(t):
    t = re.sub(r"\s+", " ", t).strip(" ,-")
    if len(t) > 55:
        m = [i for i in (t.find(", ", 18), t.find(" - ", 18), t.find(" : ", 18)) if 0 < i <= 60]
        t = t[:min(m)] if m else t[:55].rsplit(" ", 1)[0].rstrip(" ,-(")
    t = re.sub(r"( (de|à|et|pour|avec|en|du|la|le|les|des|d'|au|sur|par|or|and|for|with))+$", "", t, flags=re.I).rstrip(" ,-:(")
    return t
BAD = re.compile(r"replacement|heater core|compatible|pièce|remplacement|\bfor (ford|honda|toyota|chevy)|brake|filter pack", re.I)
def key(t): return " ".join(re.sub(r"[^\w ]", "", t.lower()).split()[:3])
QUOTA = {"maison":7,"tech":7,"beaute":7,"femme":7,"homme":7,"jouets":7,"plein-air":6,"animaux":6,"enfants":6}
out = {}
for cat, label in THEMES:
    lo = 16 if cat == "enfants" else 20
    pool = [x for x in D if x["cat"] == cat and x["pct"] >= lo and x["price"] >= (10 if cat == "enfants" else 15) and x["price"] <= 900 and x.get("img_url") and not BAD.search(x["title"]) and (x.get("comm",0) >= 4 or x["pct"] >= 35) and x["price"] >= 19]
    def score(x):
        s = x["pct"] + (12 if x.get("comm", 0) >= 6 else 6 if x.get("comm", 0) >= 4 else 0)
        s += 8 if x.get("vf") else 0
        s += min(x["price"], 300) / 30
        return -s
    pool.sort(key=score)
    seen, pick, brands = set(), [], {}
    for x in pool:
        k = key(x["title"]); b = k.split(" ")[0]
        if k in seen or brands.get(b, 0) >= 3: continue
        seen.add(k); brands[b] = brands.get(b, 0) + 1; pick.append(x)
        if len(pick) == QUOTA[cat]: break
    # tri final : prix croissant dans le theme pour que tous les budgets s'y retrouvent par blocs
    blocks = []
    for i in range(0, len(pick), 20):
        ch = pick[i:i+20]; n = len(blocks) + 1; tot = (len(pick)+19)//20
        txt = f"{label}\n\n" + "\n\n".join(
            f"{clean(x['title'])} : {money(x['price'])} (-{x['pct']} %)\n👉 https://www.amazon.ca/dp/{x['asin']}?tag={TAG}" for x in ch)
        if n == tot: txt += "\n\n🔎 Pas trouvé ton bonheur? Tape ton produit dans la barre de recherche de rabaisflashqc.ca"
        blocks.append(txt)
    out[cat] = {"label": label, "n": len(pick), "comments": blocks, "asins": [x["asin"] for x in pick]}
    print(cat, len(pick), [len(b) for b in blocks])
intro = ("🔎 TOUS LES DEALS, TRIÉS ET AVEC PHOTOS : https://rabaisflashqc.ca\n"
         "Barre de recherche, filtres par thème, prix et rabais. Garde-le en favori pour le Vendredi fou!\n\n"
         "👇 Plus bas : les liens directs de chaque produit, par thème (maison, tech, beauté, elle, lui, jouets, sport, animaux, enfants).")
json.dump({"intro": intro, "themes": out}, open(ROOT/"suivi/posts/2026-11-25-fb-themes.json", "w"), ensure_ascii=False, indent=1)
print(sum(v["n"] for v in out.values()), "produits")
