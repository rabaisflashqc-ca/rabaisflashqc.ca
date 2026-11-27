#!/usr/bin/env python3
"""Post FB 26 nov : 60 produits (jamais publies les 24-25 nov), 1 lien = 1 commentaire. Sortie suivi/posts/2026-11-26-fb-*"""
import json, re, pathlib, os
ROOT = pathlib.Path(__file__).resolve().parent
D = json.load(open(ROOT/"suivi/deals_chrome.json"))
TAG = "coupdecoeurqc-20"
EM = {"maison":"🏠","tech":"💻","beaute":"✨","femme":"👗","homme":"🧔","jouets":"🧸","plein-air":"🏕️","animaux":"🐶","enfants":"👶"}
QUOTA = {"maison":8,"tech":8,"beaute":7,"femme":7,"homme":7,"jouets":7,"plein-air":6,"animaux":5,"enfants":5}
money = lambda p: (f"{p:,.2f}".replace(",", " ").replace(".", ",") if abs(p-round(p))>0.001 else f"{p:,.0f}".replace(",", " ")) + " $"
ex = set()
for f in (ROOT/"suivi/posts").glob("2026-11-2[45]-fb*"):
    ex |= set(re.findall(r"/dp/([A-Z0-9]{10})", f.read_text()))
def clean(t):
    t = re.sub(r"\s+", " ", t).strip(" ,-")
    if len(t) > 55:
        m = [i for i in (t.find(", ", 18), t.find(" - ", 18), t.find(" : ", 18)) if 0 < i <= 60]
        t = t[:min(m)] if m else t[:55].rsplit(" ", 1)[0].rstrip(" ,-(")
    t = re.sub(r"( (de|à|et|pour|avec|en|du|la|le|les|des|d'|au|sur|par|or|and|for|with))+$", "", t, flags=re.I).rstrip(" ,-:(")
    return t
BAD = re.compile(r"replacement|heater core|compatible|pièce|remplacement|\bfor (ford|honda|toyota|chevy|gmc|dodge|jeep|nissan|bmw|mercedes)|brake|filter pack|flange|gasket|fitting|bracket|adapter|adaptateur|connector|valve|screw|bolt|washer|hose|cable tie|sticker|vinyl|decal|cartridge|refill|battery for|batterie pour|fits |blu-ray|dvd|boxset|génétique|genetic|incontinence|welder|cat6|cat5|drill|socket|insert|wire|bit set|wrench|\\bsaw\\b|qualtech|makita|db electrical|dashcam|tableau de bord|ethernet|hdmi|usb cable|pads for", re.I)
RECAT = [(re.compile(r"barbie|schleich|lego|hot wheels|peppa|fisher-price|\bdoll\b|playset|bratz|mattel"), "jouets"), (re.compile(r"aspirateur|vacuum|cuisinart|ice cream|knife|kitchen|measuring|bissell|shades|wallpaper|pillow|blanket|throw|napkin|coussin|christmas|planter|votive|holder|candle|vase|tea\\b"), "maison"), (re.compile(r"\becho\b|blink|jbl|earbuds|surveillance|speaker|haut-parleur|iphone"), "tech"), (re.compile(r"\bdog\b|cat litter|\bpets\b|chien"), "animaux")]
SHOE = re.compile(r"shoe|sneaker|sandal|clog|boot|loafer|flat|slip-on|wedge|chaussure|espadrille|mule|trainer|oxford|vince camuto|aerosoles|rockport|clarks|skechers|sperry|merrell|cole haan|new balance|propet|easy spirit", re.I)

def key(t): return " ".join(re.sub(r"[^\w ]", "", t.lower()).split()[:3])
def fixcat(x):
    t = x["title"].lower()
    if SHOE.search(t) or re.search(r"jean|chino|trouser|pants|vest|swimsuit|hoodie|jacket|shirt|dress|legging", t):
        if re.search(r"pour fille|pour garçon|girl|\\bboy\\b|kids|enfant|toddler|youth|hook and loop|\bfrench toast\b", t): x["cat"] = "enfants"
        elif re.search(r"pour homme|men['’]s|\bmen\b|big and tall|big & tall|dockers|ariat|cole haan|classic turbo|oxford", t): x["cat"] = "homme"
        else: x["cat"] = "femme"
        return x
    for r,c in RECAT:
        if r.search(x["title"].lower()): x["cat"]=c; break
    return x
pool_all = [fixcat(x) for x in D if x["asin"] not in ex and x["seen"][:10] == "2026-11-26" and x.get("img_url") and 19 <= x["price"] <= 900 and not BAD.search(x["title"])]
def score(x):
    s = x["pct"] + (12 if x.get("comm",0) >= 6 else 6 if x.get("comm",0) >= 4 else 0) + (8 if x.get("vf") else 0) + min(x["price"],300)/30
    return -s
picked, seen, brands = {}, set(), {}
for cat in QUOTA:
    lo = 16 if cat == "enfants" else 25
    pool = sorted([x for x in pool_all if x["cat"] == cat and x["pct"] >= lo and (x.get("comm",0) >= 4 or x["pct"] >= 35)], key=score)
    sel = []; shoes = 0
    for x in pool:
        k = key(x["title"]); b = k.split(" ")[0]
        if k in seen or brands.get(b,0) >= 2: continue
        if SHOE.search(x["title"]):
            if shoes >= 3: continue
            shoes += 1
        seen.add(k); brands[b] = brands.get(b,0)+1; sel.append(x)
        if len(sel) == QUOTA[cat]: break
    picked[cat] = sel; print(cat, len(sel), "/", QUOTA[cat], "pool", len(pool))
tot = sum(len(v) for v in picked.values())
if tot < 60:  # complete avec les meilleurs restants, tous themes
    used = {x["asin"] for v in picked.values() for x in v}
    rest = sorted([x for x in pool_all if x["asin"] not in used and x["pct"] >= 25 and (x.get("comm",0) >= 4 or x["pct"] >= 35) and key(x["title"]) not in seen], key=score)
    for x in rest:
        k = key(x["title"]); b = k.split(" ")[0]
        if k in seen or brands.get(b,0) >= 2: continue
        seen.add(k); brands[b] = brands.get(b,0)+1; picked[x["cat"]].append(x); tot += 1
        if tot == 60: break
items = [x for cat in QUOTA for x in picked[cat]]
comments = [f"{EM[x['cat']]} {clean(x['title'])} : {money(x['price'])} (-{x['pct']} %)\n👉 https://www.amazon.ca/dp/{x['asin']}?tag={TAG}" for x in items]
json.dump(comments, open(ROOT/"suivi/posts/2026-11-26-fb-commentaires.json","w"), ensure_ascii=False, indent=1)
json.dump([{k:x[k] for k in ("asin","title","cat","price","was","pct","vf")} for x in items], open(ROOT/"suivi/posts/2026-11-26-fb-items.json","w"), ensure_ascii=False, indent=1)
print(len(items), "produits; overlap avec hier:", len({x['asin'] for x in items} & ex))
print("avec photo locale:", [(x["cat"], x["asin"], x["title"][:30], x["pct"], x["price"]) for x in items if os.path.exists(ROOT/f"docs/img/p/{x['asin']}.jpg") or os.path.exists(ROOT/f"docs/img/p/marque-{x['asin']}.jpg")])
