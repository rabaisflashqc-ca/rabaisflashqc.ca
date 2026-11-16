#!/usr/bin/env python3
"""Image du 16 nov. (1080x1350 fil + 1080x1920 story) : « Le Vendredi fou commence cette semaine ».
6 deals : 4 avec photo officielle de la marque (docs/img/p/marque-*.jpg), 2 sans photo (gros % à la place).
Prix lus le 16 nov. 2026 (Keepa 11 h 55, page d'offres Amazon envoyée par Alex 11 h 59)."""
import pathlib, tempfile, html as H
import pack
from playwright.sync_api import sync_playwright
e = H.escape
# (étiquette, titre, photo officielle ou None, avant, maintenant, %)
P = [("Pour la maison", "Caméra intérieure Blink Mini 2K+", None, "59,99 $", "23,99 $", 60),
     ("Pour maman", "Gobelet Stanley Quencher FlowState", None, "32,99 $", "16,50 $", 50),
     ("Pour la maison", "Aspirateur balai sans fil BISSELL", "marque-B0GN4L93SM", "179,99 $", "107,99 $", 40),
     ("Pour papa", "Bottes doublées Kamik Forester", "marque-B07N1K4NK8", "135,88 $", "89,99 $", 34),
     ("Pour les kids", "Piste Hot Wheels Mario Kart Bowser", "marque-B0DN1NFKQW", "74,52 $", "49,97 $", 33),
     ("Pour l'ado", "Écouteurs sans fil JBL Vibe Beam 2", "marque-B0DN45YMP6", "72,46 $", "49,98 $", 31)]
EMO = {"Caméra intérieure Blink Mini 2K+": "📷", "Gobelet Stanley Quencher FlowState": "🥤"}
CSS = """*{box-sizing:border-box;margin:0}body{background:#141414;font-family:'Barlow Semi Condensed',sans-serif;color:#fff;position:relative;overflow:hidden}
.an{font-family:Anton,Impact,sans-serif;font-weight:400}
.hd{padding:30px 46px 18px;background:linear-gradient(120deg,#1A1A1A,#8E0B16 70%,#C1121F);border-bottom:6px solid #FFC72C;position:relative}
.br{display:flex;align-items:center;gap:10px;font-size:30px;font-weight:700;letter-spacing:2px}.br b{color:#FFC72C}
.h1{font-size:72px;line-height:.98;margin-top:12px}.h1 span{color:#FFC72C}
.sub{font-size:32px;font-weight:700;margin-top:12px}
.tag{position:absolute;right:40px;top:34px;width:180px;height:180px;border-radius:50%;background:#FFC72C;color:#7A0A16;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(10deg);text-align:center;border:6px solid #fff}
.tag small{font-size:30px;font-weight:700}.tag strong{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:58px;line-height:.9}
.l{padding:20px 36px 0}
.r{display:flex;align-items:center;gap:20px;background:#fff;color:#1A1A1A;border-radius:24px;padding:10px 22px 10px 10px;margin-bottom:10px;height:H px}
.ph{width:150px;height:100%;flex:none;border-radius:16px;background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden}
.ph img{max-width:100%;max-height:100%;object-fit:contain}
.ph.big{background:#C1121F;color:#FFC72C;flex-direction:column;font-family:Anton,Impact,sans-serif;font-size:52px;line-height:1}.ph.big i{font-style:normal;font-size:46px}
.m{flex:1;min-width:0}.w{display:inline-block;background:#8E0B16;color:#fff;border-radius:10px;padding:2px 12px;font-size:24px;font-weight:700}
.t{font-size:32px;font-weight:700;line-height:1.05;margin-top:6px}
.p{text-align:right;flex:none}.p .n{font-family:Anton,Impact,sans-serif;font-size:54px;color:#C1121F;line-height:1}.p .o{font-size:24px;color:#555}
.p .x{display:inline-block;background:#FFC72C;color:#7A0A16;border-radius:10px;padding:0 10px;font-family:Anton,Impact,sans-serif;font-size:34px;margin-top:2px}
.ft{position:absolute;left:0;right:0;bottom:0;background:#FFC72C;color:#7A0A16;text-align:center;padding:18px 0 16px}
.ft .u{font-family:Anton,Impact,sans-serif;font-size:64px;line-height:1}.ft .s{font-size:24px;font-weight:700;margin-top:6px;color:#3A1A00}"""


def row(w, t, s, av, pr, pc):
    if s:
        ph = f'<div class="ph"><img src="{(pathlib.Path("docs/img/p") / (s + ".jpg")).resolve().as_uri()}"></div>'
    else:
        ph = f'<div class="ph big"><i>{EMO.get(t, "🔥")}</i>-{pc}%</div>'
    return (f'<div class="r">{ph}<div class="m"><span class="w">{e(w)}</span><div class="t">{e(t)}</div></div>'
            f'<div class="p"><div class="n">{pr}</div><div class="o">avant <s>{av}</s></div><div class="x">-{pc} %</div></div></div>')


def page(w, h, rh, top):
    css = CSS.replace("height:H px", f"height:{rh}px")
    rows = "".join(row(*p) for p in P)
    return (f'<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{css}</style></head>'
            f'<body style="width:{w}px;height:{h}px"><div class="hd" style="padding-top:{top}px"><div class="br">{pack.BOLT}<span>RABAIS <b>FLASH</b> QC</span></div>'
            f'<div class="h1 an">VENDREDI FOU 🔥<br><span>C’EST CETTE SEMAINE</span></div>'
            f'<div class="sub">Les pré-deals sont déjà là. Les prix bougent vite!</div>'
            f'<div class="tag" style="top:{top + 4}px"><small>jusqu’à</small><strong>-60 %</strong></div></div>'
            f'<div class="l">{rows}</div>'
            f'<div class="ft"><div class="u">👉 RABAISFLASHQC.CA</div>'
            f'<div class="s">Prix observés le 16 nov. · peuvent changer à tout moment · vérifie le prix final</div></div></body></html>')


tmp = pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    for n, (w, h, rh, top) in {"post-16nov-vendredi-fou": (1080, 1350, 122, 24),
                                "story-16nov-vendredi-fou": (1080, 1920, 190, 150)}.items():
        br, ctx, pg = pack.render(pw, page(w, h, rh, top), (w, h), tmp, n)
        pg.wait_for_timeout(900)
        pg.screenshot(path=str(pack.OUT / f"{n}.png")); ctx.close(); br.close(); print(n)
