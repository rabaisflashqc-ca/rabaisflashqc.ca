#!/usr/bin/env python3
"""Éclaireur : lit les Hot Deals Amazon.ca de RedFlagDeals (dealer_id=775) et propose les meilleurs.

Ne touche pas à Amazon. Ne publie rien sur le site : il prépare une liste à valider par Alex
(docs/pack-du-jour/eclaireur.html et eclaireur.json). Une requête par page, avec une pause polie.
"""
import json, re, time, html, datetime, pathlib, urllib.parse, urllib.request
ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs" / "pack-du-jour"
BASE = "https://forums.redflagdeals.com"
LIST = BASE + "/hot-deals-f9/?dealer_id=775&sk=pv&rfd_sk=pv&sd=d&st=7"  # meilleurs scores, 7 derniers jours
LIST_NEW = BASE + "/hot-deals-f9/?dealer_id=775"  # plus récents
TAG = "coupdecoeurqc-20"
UA = "RabaisFlashQC-eclaireur/1.0 (+https://rabaisflashqc.ca)"
ASIN = re.compile(r"amazon\.ca/(?:[^\s\"'<>]*?/)?(?:dp|gp/product|gp/aw/d)/([A-Z0-9]{10})")

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr-CA,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace")

def unwrap(s):
    for _ in range(3): s = urllib.parse.unquote(s)
    return html.unescape(s)

def _txt(x): return html.unescape(re.sub(r"<[^>]+>|\s+", " ", x or "")).strip()
def _money(x):
    m = re.search(r"\$\s?(\d[\d,]*(?:\.\d{1,2})?)", x or "")
    return float(m.group(1).replace(",", "")) if m else None

def threads(page):
    """Lit chaque carte de la liste RFD : titre, prix, ancien prix, votes, réponses, heure."""
    out = []
    for c in re.split(r'<li class="topic-card', page)[1:]:
        u = re.search(r'class="topic-card-info[^"]*" href="(/[^"]+-(\d{5,})/)"', c)
        t = re.search(r'<h3 class=thread_title>(.*?)</h3>', c, re.S)
        if not u or not t: continue
        sv = re.search(r'<div class=savings>(.*?)</div>', c, re.S)
        now_p = was = None
        if sv:
            old = re.search(r'<span>(.*?)</span>', sv.group(1), re.S)
            was = _money(old.group(1)) if old else None
            now_p = _money(re.sub(r'<span>.*?</span>', "", sv.group(1), flags=re.S))
        v = re.search(r'class="votes thread_stat">(.*?)</span>', c, re.S)
        p = re.search(r'class="posts thread_stat">(.*?)</span>', c, re.S)
        tm = re.search(r'datetime="([^"]+)"', c)
        num = lambda m: int(re.sub(r"[^\d-]", "", _txt(re.sub(r"<svg.*?</svg>", "", m.group(1), flags=re.S))) or 0) if m else None
        out.append({"url": BASE + u.group(1), "title": _txt(t.group(1)), "price": now_p, "was": was,
                    "votes": num(v), "posts": num(p), "time": tm.group(1) if tm else None})
    return out

CATS = [
 ("animaux", r"\b(dog|cat|pet|chien|chat|litter|kibble|aquarium|leash)\b"),
 ("beaute", r"\b(beauty|skin|serum|cream|moisturi[sz]er|retinol|makeup|mascara|lipstick|perfume|parfum|cologne|fragrance|shampoo|conditioner|hair|dryer|straightener|curling|razor|shaver|trimmer|toothbrush|sonicare|oral-b|waterpik|nail|cerave|olay|l'or[ée]al|maybelline|neutrogena|vitamin|supplement|protein)\b"),
 ("enfants", r"\b(lego|toy|toys|kids?|baby|bébé|diaper|pampers|huggies|stroller|puzzle|playmobil|barbie|hot wheels|nerf|nintendo|switch|board game|jeu)\b"),
 ("tech", r"\b(tv|monitor|laptop|tablet|ipad|iphone|samsung|galaxy|pixel|earbuds|headphones?|speaker|soundbar|charger|cable|usb|power bank|ssd|hdd|nas|router|wi-?fi|mouse|keyboard|camera|drone|gpu|cpu|ram|anker|ugreen|iniu|logitech|echo|kindle|fire tv|roku|smart|bluetooth|gaming|xbox|playstation|ps5)\b"),
 ("plein-air", r"\b(tool|tools|drill|driver|wrench|socket|saw|dewalt|milwaukee|makita|ryobi|craftsman|klein|tape measure|garden|camping|tent|bike|bicycle|kayak|fishing|outdoor|ladder|car|tire|jump starter)\b"),
 ("mode", r"\b(shoe|shoes|sneaker|boots?|jacket|coat|parka|hoodie|shirt|t-shirt|jeans|pants|socks|underwear|dress|bag|backpack|wallet|watch|sunglasses|levi'?s|columbia|north face|skechers|adidas|nike|under armour|crocs)\b"),
 ("epicerie", r"\b(coffee beans|snack|chocolate|chips|bar|bars|cereal|tea|k-cup|kcup|candy|nuts|grocery|drink|water|sauce|food|clif|kirkland)\b"),
 ("maison", r"\b(vacuum|robot|mop|air fryer|kettle|blender|coffee maker|espresso|nespresso|keurig|ninja|instant pot|pan|pot|knife|cookware|mattress|pillow|blanket|sheets|towel|detergent|laundry|cleaner|paper towel|toilet|fan|heater|humidifier|purifier|lamp|light|bulb|furniture|chair|desk|storage|organizer|kitchen|home)\b"),
]
def categorie(title):
    t = title.lower()
    for cat, pat in CATS:
        if re.search(pat, t): return cat
    return "maison"

def votes(page):
    for pat in (r'class="[^"]*total_count[^"]*"[^>]*>\s*([+-]?\d+)', r'data-votes="([+-]?\d+)"', r'"votes"\s*:\s*([+-]?\d+)'):
        m = re.search(pat, page)
        if m: return int(m.group(1))
    return None

def main():
    known = {d.get("asin") for d in json.loads((ROOT / "data.json").read_text())["deals"]}
    log, items = [], []
    pages = [LIST] + [LIST.replace("/hot-deals-f9/", f"/hot-deals-f9/{n}/") for n in (2, 3, 4)] \
            + [LIST_NEW] + [LIST_NEW.replace("/hot-deals-f9/", f"/hot-deals-f9/{n}/") for n in (2, 3)]
    th, seen = [], set()
    for i, u in enumerate(pages):
        try:
            pg = get(u)
            if i == 0: (ROOT / "rfd_debug.html").write_text(pg[:400000])
            for t in threads(pg):
                if t["url"] not in seen and (t["votes"] or 0) >= 0:
                    seen.add(t["url"]); th.append(t)
        except Exception as ex:
            print("Page RFD inaccessible :", u, ex)
        time.sleep(1.5)
    if not th: print("Aucun fil lu."); return
    cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).isoformat()
    th = [t for t in th if not t["time"] or t["time"] >= cutoff]
    th.sort(key=lambda t: -(t["votes"] or 0))
    print("Fils trouvés :", len(th))
    first = True
    for t in th[:90]:
        time.sleep(1.2)
        try: page = get(t["url"])
        except Exception as ex:
            log.append(f'{t["url"]} : {ex}'); continue
        a = ASIN.search(unwrap(page))
        if not a: continue
        asin = a.group(1)
        pct = round((1 - t["price"] / t["was"]) * 100) if t["price"] and t["was"] and t["was"] > t["price"] else None
        items.append({**t, "rfd": t["url"], "asin": asin, "pct": pct, "cat": categorie(t["title"]),
                      "link": f"https://www.amazon.ca/dp/{asin}?tag={TAG}", "deja": asin in known})
    items.sort(key=lambda x: -(x["votes"] if x["votes"] is not None else -999))
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4)))
    (OUT / "eclaireur.json").write_text(json.dumps({"date": now.isoformat(timespec="minutes"), "items": items}, ensure_ascii=False, indent=1))
    rows = "".join(
        f'<li class="{"d" if x["deja"] else ""}"><b class="v">{x["votes"] if x["votes"] is not None else "?"}</b>'
        f'<div><p class="t">{html.escape(x["title"])}</p><p class="m">{(str(x["price"]) + " $ (avant " + str(x["was"]) + " $, -" + str(x["pct"]) + " %) · ") if x.get("pct") else ""}ASIN {x["asin"]}{" · déjà sur le site" if x["deja"] else ""}</p>'
        f'<a href="{html.escape(x["link"])}" target="_blank" rel="sponsored nofollow noopener">Ouvrir sur Amazon (ton lien)</a> · '
        f'<a href="{html.escape(x["rfd"])}" target="_blank" rel="noopener">Fil RedFlagDeals</a></div></li>' for x in items) or "<li>Rien de neuf ce matin.</li>"
    (OUT / "eclaireur.html").write_text(f"""<!doctype html><html lang="fr-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Éclaireur RedFlagDeals</title><style>
body{{font-family:system-ui,sans-serif;max-width:760px;margin:0 auto;padding:16px;background:#FFF8E1;color:#1a1a1a}}h1{{color:#C1121F;margin:0 0 4px}}
ul{{list-style:none;padding:0}}li{{display:flex;gap:14px;background:#fff;border-radius:14px;padding:12px 14px;margin:10px 0;box-shadow:0 2px 0 rgba(0,0,0,.08)}}
li.d{{opacity:.55}}.v{{min-width:44px;height:44px;border-radius:50%;background:#C1121F;color:#fff;display:grid;place-items:center;font-size:18px}}
.t{{margin:0;font-weight:700}}.m{{margin:4px 0;color:#666;font-size:14px}}a{{color:#0067d6;font-weight:600}}</style></head><body>
<h1>🔎 Éclaireur du matin</h1><p>Deals Amazon.ca les plus votés sur RedFlagDeals, {now:%d/%m à %H h %M}. Le chiffre rouge = votes de la communauté.<br>
<b>À faire :</b> ouvre ceux qui t'intéressent, fais une capture et envoie-la pour confirmer le rabais avant qu'il aille sur le site.</p>
<ul>{rows}</ul><p style="color:#888;font-size:13px">{len(items)} deals avec lien Amazon sur {len(th)} fils lus.</p></body></html>""")
    # Publication autonome : les plus votés, prix et rabais signalés (datés et attribués), valables 24 h
    def clean(t):
        t = re.sub(r"\s+-?\s*\d+\s?[mhdw] ago.*$", "", t)
        t = re.sub(r"\[?\(?\bamazon(\.ca)?\b\)?\]?\s*[-:|]?", "", t, flags=re.I)
        t = re.sub(r"\$\s?\d[\d,.]*|\d[\d,.]*\s?\$|\d+\s?%\s*(off|de rabais)?|\(.*?\)|\[.*?\]", "", t, flags=re.I)
        t = re.sub(r"\b(save|saves|lowest ever|historical low|price drop on|price drop|ymmv|deal|just|only|now|min \d+|amazon)\b", "", t, flags=re.I)
        return re.sub(r"\s*[-–:|,…]+\s*$", "", re.sub(r"\s{2,}", " ", t)).strip(" -–:|,")
    PAR_CAT, TOTAL = 5, 40
    cnt, pub = {}, []
    for x in sorted(items, key=lambda x: (-(x["votes"] or 0), -(x.get("pct") or 0))):
        if x["deja"] or re.search(r"hallowe", x["title"], re.I) or not x.get("price"): continue
        if cnt.get(x["cat"], 0) >= PAR_CAT: continue
        cnt[x["cat"]] = cnt.get(x["cat"], 0) + 1
        pub.append({"asin": x["asin"], "title": clean(x["title"]), "cat": x["cat"], "votes": x["votes"], "posts": x.get("posts"),
                    "rfd": x["rfd"], "price": x.get("price"), "was": x.get("was"), "pct": x.get("pct"), "posted": x.get("time"),
                    "seen": now.isoformat(timespec="minutes"), "until": (now + datetime.timedelta(hours=24)).isoformat(timespec="minutes")})
        if len(pub) >= TOTAL: break
    print("Par catégorie :", cnt)
    old = []
    try: old = json.loads((ROOT / "rfd.json").read_text())
    except Exception: pass
    keep = {p["asin"]: p for p in pub}  # chaque passage remplace la vitrine par les données les plus fraîches
    (ROOT / "rfd.json").write_text(json.dumps(list(keep.values()), ensure_ascii=False, indent=1))
    print(f"{len(pub)} publiés automatiquement, {len(keep)} en vitrine.")
    print(f"{len(items)} deals Amazon trouvés, {sum(not x['deja'] for x in items)} nouveaux.")
    for l in log[:5]: print("  ", l)

if __name__ == "__main__":
    main()
