#!/usr/bin/env python3
"""Éclaireur : lit les Hot Deals Amazon.ca de RedFlagDeals (dealer_id=775) et propose les meilleurs.

Ne touche pas à Amazon. Ne publie rien sur le site : il prépare une liste à valider par Alex
(docs/pack-du-jour/eclaireur.html et eclaireur.json). Une requête par page, avec une pause polie.
"""
import json, re, time, html, datetime, pathlib, urllib.parse, urllib.request
ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs" / "pack-du-jour"
BASE = "https://forums.redflagdeals.com"
LIST = BASE + "/hot-deals-f9/?dealer_id=775"
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

def threads(page):
    seen, out = set(), []
    for m in re.finditer(r'href="(/[a-z0-9][a-z0-9-]+-(\d{5,})/)"[^>]*>(.*?)</a>', page, re.S):
        url, tid, txt = m.groups()
        title = re.sub(r"<[^>]+>|\s+", " ", txt).strip()
        if tid in seen or len(title) < 8: continue
        seen.add(tid); out.append((BASE + url, html.unescape(title)))
    return out

def votes(page):
    for pat in (r'class="[^"]*total_count[^"]*"[^>]*>\s*([+-]?\d+)', r'data-votes="([+-]?\d+)"', r'"votes"\s*:\s*([+-]?\d+)'):
        m = re.search(pat, page)
        if m: return int(m.group(1))
    return None

def main():
    known = {d.get("asin") for d in json.loads((ROOT / "data.json").read_text())["deals"]}
    log, items = [], []
    try:
        lst = get(LIST)
    except Exception as ex:
        print("Liste RFD inaccessible :", ex); return
    th = threads(lst)
    print("Fils trouvés :", len(th))
    for url, title in th[:30]:
        time.sleep(1.5)
        try: page = get(url)
        except Exception as ex:
            log.append(f"{url} : {ex}"); continue
        a = ASIN.search(unwrap(page))
        if not a: continue
        asin = a.group(1)
        items.append({"title": title, "rfd": url, "asin": asin, "votes": votes(page),
                      "link": f"https://www.amazon.ca/dp/{asin}?tag={TAG}", "deja": asin in known})
    items.sort(key=lambda x: -(x["votes"] if x["votes"] is not None else -999))
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4)))
    (OUT / "eclaireur.json").write_text(json.dumps({"date": now.isoformat(timespec="minutes"), "items": items}, ensure_ascii=False, indent=1))
    rows = "".join(
        f'<li class="{"d" if x["deja"] else ""}"><b class="v">{x["votes"] if x["votes"] is not None else "?"}</b>'
        f'<div><p class="t">{html.escape(x["title"])}</p><p class="m">ASIN {x["asin"]}{" · déjà sur le site" if x["deja"] else ""}</p>'
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
    print(f"{len(items)} deals Amazon trouvés, {sum(not x['deja'] for x in items)} nouveaux.")
    for l in log[:5]: print("  ", l)

if __name__ == "__main__":
    main()
