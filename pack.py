#!/usr/bin/env python3
"""Prépare le pack de publication (post + image + Reel) et la page privée /pack-du-jour/.

Usage : python3 pack.py [matin|midi|soir]
Sans argument, le créneau est choisi selon l'heure du Québec.
Aucun modèle d'IA : tout est généré par ce script, à partir de data.json.
Règles : pas de prix sur les images, mention Partenaire Amazon, aucun long trait (tiret cadratin).
"""
import sys, json, html, datetime, pathlib, subprocess, tempfile, shutil
from zoneinfo import ZoneInfo

import build  # charge data.json et applique les règles d'expiration

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs" / "pack-du-jour"
SITE = build.DOMAIN
DISC = build.DISCLOSURE
FLASH = ("⚡ Rabais Flash : Amazon ou la marque peut modifier ou arrêter une offre à tout moment, "
         "on ne peut pas garantir sa durée. Clique vite!")
e = html.escape
NOW = datetime.datetime.now(ZoneInfo("America/Toronto"))
SEED = NOW.timetuple().tm_yday

SLOTS = {"matin": ("☀️", "Post de 7 h"), "midi": ("🥪", "Bonus du midi"), "soir": ("🌙", "Deal du soir, 20 h")}

OPEN = {
    "matin": ["☀️ Bon matin la gang! Le café est chaud, et les rabais aussi.",
              "☕ Avant de partir pour la journée, jette un œil à ça :",
              "🌅 Nouvelle journée, nouveaux rabais triés pour toi.",
              "😴 Pas le temps de chercher ce matin? On l'a fait pour toi.",
              "🍁 Bon matin, le Québec! Voici ce qui vaut le coup aujourd'hui :",
              "⏰ 7 h pile, comme promis! Les deals du matin sont arrivés.",
              "💛 Une petite douceur pour bien commencer ta journée :"],
    "midi": ["🥪 Pause dîner? Voici un petit rabais à croquer :",
             "⚡ Offre flash du midi! Ça passe vite, comme la pause :",
             "😋 Pendant que ta soupe refroidit, regarde ça :",
             "🕛 Midi, l'heure des bonnes affaires :"],
    "soir": ["🌙 Les enfants sont couchés? C'est le temps de magasiner tranquille.",
             "🛋️ Sur le divan, un café ou une tisane à la main : voici le Top 5 du soir.",
             "✨ Le deal du soir est arrivé! Les meilleurs rabais du jour, triés pour toi.",
             "🍷 Tu l'as bien mérité. Regarde ce qu'on a déniché aujourd'hui :",
             "🎁 Noël approche vite. On trie pour toi les rabais qui valent vraiment la peine :",
             "💫 Fin de journée, début des bonnes affaires :",
             "🔥 Voici le Top 5 de ce soir, choisi un par un :"],
}
REEL_HOOK = ["Tout coûte plus cher? On trie les rabais pour toi. 😮‍💨",
             "Arrête de scroller pendant des heures. On a fait le tri. ⚡",
             "Les meilleurs rabais d'Amazon.ca, sur une seule page. 🔥",
             "Ton portefeuille va nous dire merci. 💛"]


def clean(s):
    return s.replace("—", ",").replace("–", "-")


def pct_txt(d):
    return f"-{d['pct']} %" if d.get("live") and d.get("pct") else ""


def short(name, n=46):
    name = name.split(" (")[0]
    return name if len(name) <= n else name[:n].rsplit(" ", 1)[0] + "…"


def line(d):
    p = pct_txt(d)
    return f"{build.ICON.get(d['cat'], '⭐')} {d['brand']} : {short(d['name'])}" + (f" ({p})" if p else "")


def pick(slot):
    picks, _ = build.top5()
    if slot == "soir":
        return picks[:5]
    if slot == "matin":
        return picks[:3]
    # midi : un deal par catégorie, les plus gros rabais d'abord, en évitant le Top 3
    used = {id(x) for x in picks[:3]}
    pool = sorted([d for d in build.DEALS if id(d) not in used and d.get("live") and d.get("pct") and build.rate(d) > 0], key=lambda d: (-d["pct"], -build.gain(d)))
    out, cats = [], set()
    for d in pool:
        if d["cat"] not in cats:
            out.append(d); cats.add(d["cat"])
        if len(out) == 3:
            break
    return out or picks[:3]


def hashtags():
    t = ["#RabaisFlashQC", "#AubainesQuébec", "#DealsQC", "#Québec"]
    if NOW.month == 10: t.append("#Halloween")
    if NOW.month in (11, 12): t += ["#Noël", "#CadeauxDeNoël"]
    if (NOW.month == 11 and NOW.day >= 20) or (NOW.month == 12 and NOW.day <= 2): t.append("#VendrediFou")
    return " ".join(t)


def post_text(slot, items):
    opener = OPEN[slot][SEED % len(OPEN[slot])]
    hook = ""
    if slot != "midi" and items and items[0].get("story"):
        hook = ("Coup de cœur n° 1 : " if slot == "soir" else "") + items[0]["story"] + "\n\n"
    body = "\n".join(line(d) for d in items) if items else "Les meilleurs rabais d'Amazon.ca, triés pour toi."
    txt = (f"{opener}\n\n{hook}{body}\n\n👉 Tous les deals triés, sans chercher : {SITE}\n\n{FLASH}\n\n"
           f"👍 Aime la page pour ne rien manquer. Et partage à quelqu'un qui aime les aubaines! 💛\n\n{DISC}\n\n{hashtags()}")
    return clean(txt)


def first_comment():
    return clean(f"🔗 Tous les deals triés : {SITE}\n🎁 Guides cadeaux de Noël : {SITE}/idees-cadeaux/\n\n{DISC}")


def reel_caption():
    return clean(f"{REEL_HOOK[SEED % len(REEL_HOOK)]}\n\nTous les deals triés : lien dans le premier commentaire 👇\n\n"
                 f"⚡ Rabais Flash : durée non garantie.\n\n{DISC}\n\n{hashtags()}")


BOLT = '<svg width="38" height="60" viewBox="0 0 100 160"><path d="M62 0 L8 92 L44 92 L28 160 L94 58 L58 58 L78 0 Z" fill="#FFC72C"/></svg>'
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Semi+Condensed:wght@600;700&display=swap" rel="stylesheet">'
         '<style>body{font-family:"Barlow Semi Condensed","Arial Narrow",Arial,sans-serif}.an{font-family:Anton,Impact,"Arial Narrow Bold",sans-serif;font-weight:400}</style>')

HEAD = {"matin": ("BON MATIN LA GANG ☀️", "LES DEALS DU MATIN"),
        "midi": ("PAUSE DÎNER ⚡", "OFFRE FLASH DU MIDI"),
        "soir": ("LE DEAL DU SOIR 🌙", "LE TOP 5 DU JOUR")}


def badge(d):
    p = pct_txt(d)
    return f'<div class="bd">{e(p)}</div>' if p else '<div class="bd cc">COUP DE CŒUR</div>'


def image_html(slot, items):
    a, b = HEAD[slot]
    rows = "".join(
        f'<div class="row"><div class="n an">{i}</div><div class="ic">{build.ICON.get(d["cat"], "⭐")}</div>'
        f'<div class="tx"><div class="br">{e(d["brand"])}</div><div class="nm">{e(short(d["name"], 40))}</div></div>{badge(d)}</div>'
        for i, d in enumerate(items, 1))
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{box-sizing:border-box;margin:0}}body{{width:1080px;height:1350px;background:#C1121F;color:#fff;position:relative;overflow:hidden}}
.top{{display:flex;align-items:center;gap:14px;padding:46px 56px 0;font-size:40px;letter-spacing:2px;font-weight:700}}.top b{{color:#FFC72C}}
h1{{padding:26px 56px 0;font-size:96px;line-height:.98;color:#FFC72C}}h2{{padding:10px 56px 0;font-size:40px;font-weight:700}}
.list{{padding:34px 56px 0;display:flex;flex-direction:column;gap:16px}}
.big{{gap:28px;padding-top:56px}}.big .row{{padding:36px 28px}}.big .nm{{font-size:40px}}.big .br{{font-size:30px}}.big .ic{{font-size:64px}}.big .bd{{font-size:50px}}.row{{background:#fff;color:#1A1A1A;border-radius:26px;padding:20px 24px;display:flex;align-items:center;gap:20px}}
.n{{width:54px;height:54px;border-radius:50%;background:#C1121F;color:#fff;display:flex;align-items:center;justify-content:center;font-size:30px;flex:none}}
.ic{{font-size:50px;flex:none}}.tx{{flex:1;min-width:0}}.br{{font-size:26px;font-weight:700;color:#C1121F;text-transform:uppercase}}
.nm{{font-size:33px;font-weight:700;line-height:1.1}}.bd{{background:#FFC72C;color:#8E0B16;border-radius:18px;padding:10px 16px;font-family:Anton,Impact,sans-serif;font-size:42px;flex:none}}
.bd.cc{{font-size:22px;font-family:"Barlow Semi Condensed",Arial,sans-serif;font-weight:700;text-align:center}}
.foot{{position:absolute;left:0;right:0;bottom:0;background:#FFC72C;color:#8E0B16;padding:26px 56px 30px;text-align:center}}
.foot .u{{font-size:54px}}.foot .s{{font-size:23px;font-weight:700;margin-top:6px}}
</style></head><body>
<div class="top">{BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>
<h1 class="an">{e(a)}</h1><h2>{e(b)}</h2>
<div class="list{" big" if len(items) <= 3 else ""}">{rows}</div>
<div class="foot"><div class="u an">👉 RABAISFLASHQC.CA</div><div class="s">⚡ Rabais Flash : peut changer à tout moment, durée non garantie</div></div>
</body></html>"""


def reel_html(items, ha="TOUT COÛTE<br>PLUS CHER 😮‍💨", hb="ON FAIT<br>LE TRI<br><i>POUR TOI ⚡</i>", hd="Nos coups de cœur du moment"):
    cards = "".join(
        f'<div class="card" style="--d:{5.0 + i * 1.9:.1f}s"><div class="ic">{build.ICON.get(d["cat"], "⭐")}</div>'
        f'<div class="tx"><div class="br">{e(d["brand"])}</div><div class="nm">{e(short(d["name"], 34))}</div></div>{badge(d)}</div>'
        for i, d in enumerate(items[:3]))
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{box-sizing:border-box;margin:0}}html,body{{width:720px;height:1280px;overflow:hidden}}
body{{background:#C1121F;color:#fff;position:relative}}
.s{{position:absolute;left:0;right:0;padding:0 48px;opacity:0}}
.logo{{position:absolute;top:44px;left:48px;display:flex;gap:10px;align-items:center;font-size:30px;font-weight:700;letter-spacing:2px}}.logo b{{color:#FFC72C}}
.a{{top:330px;font-size:92px;line-height:1;color:#FFC72C;animation:io 2.8s ease both}}
.b{{top:330px;font-size:84px;line-height:1;animation:io 2.4s 2.8s ease both}}.b i{{color:#FFC72C;font-style:normal}}
@keyframes io{{0%{{opacity:0;transform:translateY(40px) scale(.96)}}15%,85%{{opacity:1;transform:none}}100%{{opacity:0;transform:translateY(-30px)}}}}
.list{{position:absolute;top:300px;left:36px;right:36px;display:flex;flex-direction:column;gap:22px}}
.card{{background:#fff;color:#1A1A1A;border-radius:28px;padding:26px 24px;display:flex;align-items:center;gap:18px;opacity:0;animation:pop .6s var(--d) ease forwards,out .5s 12.4s ease forwards}}
@keyframes pop{{0%{{opacity:0;transform:translateX(120px) rotate(3deg)}}100%{{opacity:1;transform:none}}}}
@keyframes out{{to{{opacity:0}}}}
.ic{{font-size:56px}}.tx{{flex:1;min-width:0}}.br{{font-size:24px;font-weight:700;color:#C1121F;text-transform:uppercase}}.nm{{font-size:32px;font-weight:700;line-height:1.1}}
.bd{{background:#FFC72C;color:#8E0B16;border-radius:16px;padding:8px 14px;font-family:Anton,Impact,sans-serif;font-size:40px}}.bd.cc{{font-size:20px;font-family:"Barlow Semi Condensed",Arial,sans-serif;font-weight:700}}
.hd{{top:190px;font-size:44px;font-weight:700;color:#FFC72C;animation:hd 8s 4.6s ease both}}
@keyframes hd{{0%{{opacity:0}}8%,90%{{opacity:1}}100%{{opacity:0}}}}
.end{{top:300px;text-align:center;animation:end 3.2s 12.4s ease forwards}}
@keyframes end{{0%{{opacity:0;transform:scale(.9)}}25%,100%{{opacity:1;transform:none}}}}
.end .t{{font-size:78px;line-height:1.02;color:#FFC72C}}.end .u{{margin-top:34px;display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:999px;padding:18px 34px;font-size:46px}}
.end .l{{margin-top:30px;font-size:36px;font-weight:700}}
.tiny{{position:absolute;left:30px;right:30px;bottom:34px;text-align:center;font-size:20px;opacity:.9;font-weight:600}}
</style></head><body>
<div class="logo">{BOLT.replace('width="38" height="60"', 'width="26" height="42"')}<span>RABAIS <b>FLASH</b> QC</span></div>
<div class="s a an">{ha}</div>
<div class="s b an">{hb}</div>
<div class="s hd">{hd}</div>
<div class="list">{cards}</div>
<div class="s end"><div class="t an">TOUS LES DEALS<br>SUR UNE PAGE</div><div class="u an">RABAISFLASHQC.CA</div><div class="l">👍 Aime la page pour ne rien manquer</div></div>
<div class="tiny">⚡ Rabais Flash : durée non garantie · {e(DISC)}</div>
</body></html>"""


HW_IMG = """body{background:linear-gradient(180deg,#C1121F 0%,#B30F22 42%,#5B1A8C 100%)!important}
h1{color:#FF9A3D!important}.top b{color:#FF9A3D}.row{border:5px solid #2A0F45}.n{background:#5B1A8C!important}.br{color:#5B1A8C!important}
.bd{background:#FF7518!important;color:#2A0F45!important}
.foot{background:#2A0F45!important;color:#FF9A3D!important;border-top:6px solid #FF7518}
.deco{position:absolute;font-size:90px;opacity:.9}.web{position:absolute;top:0;right:0;font-size:150px;line-height:1;opacity:.55}"""
HW_REEL = """body{background:linear-gradient(180deg,#C1121F 0%,#B30F22 45%,#4A1170 100%)!important}
.a,.hd{color:#FF9A3D!important}.b i{color:#FF9A3D!important}.logo b{color:#FF9A3D!important}
.bd{background:#FF7518!important;color:#2A0F45!important}.card{border:4px solid #2A0F45}.br{color:#5B1A8C!important}
.end .t{color:#FF9A3D!important}.end .u{background:#FF7518!important;color:#2A0F45!important}
.bat{position:absolute;font-size:64px;animation:fly 9s linear infinite;opacity:.9}
@keyframes fly{0%{transform:translate(-80px,0) rotate(-10deg)}50%{transform:translate(380px,40px) rotate(10deg)}100%{transform:translate(820px,0) rotate(-10deg)}}"""


def hw_image(html):
    deco = '<div class="web">🕸️</div><div class="deco" style="right:70px;top:150px">🦇</div><div class="deco" style="right:200px;top:60px;font-size:60px">🦇</div><div class="deco" style="left:60px;bottom:215px;font-size:64px">👻</div>'
    return html.replace("</style>", HW_IMG + "</style>", 1).replace("</body>", deco + "</body>")


def hw_reel(html):
    deco = '<div class="bat" style="top:120px">🦇</div><div class="bat" style="top:1010px;animation-delay:-4s">🦇</div><div class="bat" style="top:1100px;animation-delay:-7s;font-size:48px">🎃</div>'
    return html.replace("</style>", HW_REEL + "</style>", 1).replace("</body>", deco + "</body>")


def render(pw, html_str, size, tmp, name, video=False):
    path = tmp / f"{name}.html"
    path.write_text(html_str)
    br = pw.chromium.launch()
    kw = {"viewport": {"width": size[0], "height": size[1]}}
    if video:
        kw.update(record_video_dir=str(tmp), record_video_size={"width": size[0], "height": size[1]})
    ctx = br.new_context(**kw)
    page = ctx.new_page()
    page.goto(path.as_uri())
    try:
        page.evaluate("document.fonts.ready")
    except Exception:
        pass
    return br, ctx, page


def make_image(pw, slot, items, tmp, theme=None):
    html = image_html(slot, items)
    html = hw_image(html) if theme == "hw" else html
    br, ctx, page = render(pw, html, (1080, 1350), tmp, "img")
    page.wait_for_timeout(700)
    page.screenshot(path=str(OUT / f"{slot}.png"))
    ctx.close(); br.close()


def make_reel(pw, items, tmp, out="soir.mp4", theme=None, **kw):
    html = reel_html(items, **kw)
    html = hw_reel(html) if theme == "hw" else html
    br, ctx, page = render(pw, html, (720, 1280), tmp, "reel", video=True)
    page.wait_for_timeout(16000)
    ctx.close(); br.close()
    webm = sorted(tmp.glob("*.webm"))[-1]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(webm), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "28", "-preset", "veryfast", "-an", "-movflags", "+faststart", "-t", "15.5", str(OUT / out)], check=True)


def page_html(meta):
    cards = ""
    for slot in ("matin", "midi", "soir"):
        m = meta.get(slot)
        ico, ttl = SLOTS[slot]
        if not m:
            cards += f'<section class="c"><h2>{ico} {ttl}</h2><p class="m">Pas encore préparé.</p></section>'
            continue
        v = e(m["at"][:16].replace("T", " "))
        reel = ""
        if m.get("reel"):
            reel = (f'<h3>🎬 Reel animé</h3><video controls playsinline preload="metadata" src="{m["reel"]}?v={e(m["v"])}"></video>'
                    f'<p><a class="btn" href="{m["reel"]}?v={e(m["v"])}" download>⬇️ Télécharger le Reel</a></p>'
                    f'<h3>Légende du Reel</h3><pre id="{slot}-rc">{e(m["reel_caption"])}</pre><button data-c="{slot}-rc">📋 Copier la légende</button>'
                    f'<p class="w">{e(m["reel_note"])}</p>')
        cards += (f'<section class="c"><h2>{ico} {ttl}</h2><p class="m">Préparé le {v} (heure du Québec)</p>'
                  f'<img src="{m["image"]}?v={e(m["v"])}" alt="Image du post"><p><a class="btn" href="{m["image"]}?v={e(m["v"])}" download>⬇️ Télécharger l\'image</a></p>'
                  f'<h3>Texte du post</h3><pre id="{slot}-t">{e(m["text"])}</pre><button data-c="{slot}-t">📋 Copier le texte</button>'
                  f'<h3>Premier commentaire à épingler</h3><pre id="{slot}-c">{e(m["comment"])}</pre><button data-c="{slot}-c">📋 Copier le commentaire</button>{reel}</section>')
    return f"""<!doctype html><html lang="fr-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Pack du jour</title><style>
:root{{--red:#C1121F;--deep:#8E0B16;--yel:#FFC72C;color-scheme:light}}*{{box-sizing:border-box}}
body{{margin:0;font:17px/1.45 'Helvetica Neue',Arial,sans-serif;background:#F6F1EC;color:#1A1A1A}}header{{background:var(--red);color:#fff;padding:18px 16px}}
header h1{{margin:0;font-size:26px;color:var(--yel)}}header p{{margin:6px 0 0;font-size:15px}}main{{max-width:640px;margin:0 auto;padding:12px 14px 40px}}
.c{{background:#fff;border-radius:18px;padding:16px;margin:14px 0;box-shadow:0 2px 0 rgba(0,0,0,.06)}}.c h2{{margin:0;color:var(--deep);font-size:24px}}.c h3{{margin:18px 0 6px;font-size:17px;color:var(--red)}}
.m{{margin:4px 0 12px;color:#666;font-size:14px}}img,video{{width:100%;border-radius:12px;display:block;background:#000}}video{{max-height:560px}}
pre{{white-space:pre-wrap;word-wrap:break-word;background:#FFF8E1;border:1px solid #F0DFA6;border-radius:12px;padding:12px;margin:0 0 8px;font:15px/1.45 inherit}}
button,.btn{{display:inline-block;font:700 16px inherit;background:var(--red);color:#fff;border:none;border-radius:999px;padding:11px 18px;text-decoration:none;cursor:pointer;margin:6px 6px 0 0}}
.w{{background:#FFF1C7;border-radius:10px;padding:10px 12px;font-size:15px}}.steps{{background:#fff;border-radius:18px;padding:14px 16px;margin:14px 0}}.steps ol{{margin:6px 0 0 18px;padding:0}}
</style></head><body><header><h1>⚡ Pack du jour</h1><p>Page privée de Rabais Flash QC. Copie, télécharge, publie.</p></header><main>
<div class="steps"><b>Comment publier (2 minutes)</b><ol><li>Télécharge l'image (ou le Reel) et copie le texte.</li><li>Publie sur ta page Facebook.</li><li>Colle le premier commentaire et épingle-le.</li></ol></div>
{cards}</main><script>document.querySelectorAll('button[data-c]').forEach(function(b){{b.addEventListener('click',function(){{var t=document.getElementById(b.dataset.c).innerText;
(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){{b.textContent='✅ Copié!'}}).catch(function(){{var r=document.createRange();r.selectNode(document.getElementById(b.dataset.c));getSelection().removeAllRanges();getSelection().addRange(r);b.textContent='Sélectionné, fais Copier'}});}});}});</script></body></html>"""


def main():
    slot = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in SLOTS else ("matin" if NOW.hour < 10 else "midi" if NOW.hour < 15 else "soir")
    OUT.mkdir(parents=True, exist_ok=True)
    items = pick(slot)
    metaf = OUT / "meta.json"
    meta = json.loads(metaf.read_text()) if metaf.exists() else {}
    stamp = NOW.strftime("%Y%m%d%H%M")
    entry = {"at": NOW.isoformat(timespec="minutes"), "v": stamp, "image": f"{slot}.png", "text": post_text(slot, items), "comment": first_comment(), "reel": None}
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        tmp = pathlib.Path(tempfile.mkdtemp())
        try:
            make_image(pw, slot, items, tmp)
            if slot == "soir":
                make_reel(pw, items, tmp)
                entry["reel"] = "soir.mp4"
                entry["reel_caption"] = reel_caption()
                shows = any(pct_txt(d) for d in items[:3])
                entry["reel_note"] = ("Ce Reel montre des rabais précis : publie-le en organique, ne le commandite pas (le rabais peut changer)."
                                      if shows else "Ce Reel ne montre aucun rabais précis : tu peux le commanditer.")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    meta[slot] = entry
    metaf.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    (OUT / "index.html").write_text(page_html(meta))
    print(f"Pack « {slot} » prêt : {len(items)} produits.")


if __name__ == "__main__":
    main()
