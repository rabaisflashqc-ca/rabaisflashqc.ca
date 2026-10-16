#!/usr/bin/env python3
"""Reel viral 16 oct : accroche -64 %, astuce Historique des prix, 3 deals, CTA enregistrer. % seulement."""
import pathlib, tempfile, subprocess, html as H
import pack, build
from playwright.sync_api import sync_playwright
e=H.escape
D={d["asin"]:d for d in build.data["deals"] if d.get("asin")}
pick=[("B0CT9SBWC9","Casque Tune 670NC","🎧"),("B0BQPNMXQV","Écouteurs Vibe Beam","🎵"),("B0711FGWN9","Trousse solaire","☀️")]
cards="".join(f'<div class="card" style="--d:{8.9+i*0.7:.1f}s"><div class="ic">{ic}</div><div class="tx"><div class="br">{e(D[a]["brand"])}</div><div class="nm">{e(t)}</div></div><div class="bd">-{D[a]["pct"]} %</div></div>' for i,(a,t,ic) in enumerate(pick))
CSS="""*{box-sizing:border-box;margin:0}html,body{width:720px;height:1280px;overflow:hidden}
body{background:#C1121F;color:#fff;position:relative;font-family:"Barlow Semi Condensed",Arial,sans-serif}
.logo{position:absolute;top:44px;left:48px;display:flex;gap:10px;align-items:center;font-size:30px;font-weight:700;letter-spacing:2px}.logo b{color:#FFC72C}
.s{position:absolute;left:0;right:0;padding:0 48px;opacity:0;text-align:center}
.h1{top:330px;font-size:96px;line-height:1.02;animation:sc 2.4s 0s ease both}.h1 b{display:block;font-size:220px;color:#FFC72C;animation:shake .5s .5s 3}
@keyframes shake{0%,100%{transform:rotate(0)}25%{transform:rotate(-4deg) scale(1.06)}75%{transform:rotate(4deg) scale(1.06)}}
.h2{top:380px;font-size:92px;line-height:1.05;animation:sc 2.6s 2.4s ease both}.h2 i{font-style:normal;color:#FFC72C}
@keyframes sc{0%{opacity:0;transform:scale(.8)}12%,86%{opacity:1;transform:none}100%{opacity:0;transform:translateY(-40px)}}
.tip{top:250px;animation:sc 3.8s 5s ease both}
.amz{margin:0 auto;width:600px;background:#fff;color:#111;border-radius:24px;padding:30px;text-align:left;font-family:Arial,sans-serif}
.amz .p{font-size:30px;color:#CC0C39}.amz .p b{font-size:56px;color:#111}.amz .o{font-size:24px;color:#555;margin-top:8px}
.amz .hp{display:inline-block;margin-top:16px;margin-left:-12px;font-size:32px;color:#0066C0;padding:6px 12px;border-radius:10px;animation:hl 1s 6.4s 2 both}
@keyframes hl{50%{background:#FFF3B0;outline:4px solid #FFC72C}}
.finger{position:absolute;font-size:80px;left:330px;top:120px;opacity:0;animation:tap 1.6s 6s ease both}
@keyframes tap{0%{opacity:0;transform:translate(80px,80px)}40%{opacity:1;transform:none}55%{transform:scale(.85)}70%,100%{opacity:1;transform:none}}
.tip .t{margin-top:40px;font-size:52px;font-weight:700;line-height:1.15}.tip .t i{font-style:normal;color:#FFC72C}
.hd{top:150px;font-size:56px;font-weight:700;color:#FFC72C;animation:sc 4s 8.6s ease both}
.list{position:absolute;top:360px;left:36px;right:36px;display:flex;flex-direction:column;gap:24px}
.card{background:#fff;color:#1A1A1A;border-radius:28px;padding:28px 24px;display:flex;align-items:center;gap:18px;opacity:0;animation:pop .5s var(--d) ease forwards,out .4s 12.4s ease forwards}
@keyframes pop{0%{opacity:0;transform:translateX(140px) rotate(4deg)}100%{opacity:1;transform:none}}@keyframes out{to{opacity:0}}
.ic{font-size:60px}.tx{flex:1}.br{font-size:26px;font-weight:700;color:#C1121F;text-transform:uppercase}.nm{font-size:36px;font-weight:700;line-height:1.1}
.bd{background:#FFC72C;color:#8E0B16;border-radius:16px;padding:8px 16px;font-family:Anton,Impact,sans-serif;font-size:50px}
.end{top:280px;animation:end 3.2s 12.7s ease forwards}@keyframes end{0%{opacity:0;transform:scale(.85)}25%,100%{opacity:1;transform:none}}
.end .t{font-size:96px;line-height:1.02;color:#FFC72C}.end .x{margin-top:26px;font-size:46px;font-weight:700}
.end .u{margin-top:36px;display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:999px;padding:18px 34px;font-size:46px}
.tiny{position:absolute;left:30px;right:30px;bottom:34px;text-align:center;font-size:20px;opacity:.92;font-weight:600}"""
html=f'''<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body>
<div class="logo">{pack.BOLT.replace('width="38" height="60"','width="26" height="42"')}<span>RABAIS <b>FLASH</b> QC</span></div>
<div class="s h1 an">UN CASQUE JBL À<b>-64 %</b></div>
<div class="s h2 an">AVANT DE<br>CRAQUER,<br><i>VÉRIFIE ÇA 👇</i></div>
<div class="s tip"><div class="amz"><div class="p">-64 % <b>49,98 $</b></div><div class="o">Prix conseillé : 139,98 $</div><div class="hp">Historique des prix</div></div><div class="finger">👆</div>
<div class="t">Même prix le mois passé?<br><i>Ce n'est pas une aubaine.</i></div></div>
<div class="s hd an">LES GROS RABAIS DU JOUR ⚡</div>
<div class="list">{cards}</div>
<div class="s end"><div class="t an">📌 ENREGISTRE<br>CE REEL</div><div class="x">pour ton prochain achat Amazon</div><div class="u an">RABAISFLASHQC.CA</div></div>
<div class="tiny">⚡ Prix sujets à changement · {e(pack.DISC)}</div></body></html>'''
tmp=pathlib.Path(tempfile.mkdtemp())
with sync_playwright() as pw:
    br,ctx,pg=pack.render(pw,html,(720,1280),tmp,"viral",video=True)
    pg.wait_for_timeout(19000); ctx.close(); br.close()
webm=sorted(tmp.glob("*.webm"))[-1]
out=pack.OUT/"reel-viral-16oct.mp4"
subprocess.run(["ffmpeg","-y","-loglevel","error","-ss","0.4","-i",str(webm),"-c:v","libx264","-pix_fmt","yuv420p","-crf","24","-preset","veryfast","-an","-movflags","+faststart","-t","17.5",str(out)],check=True)
for t in (1.5,4.5,7.5,11.5,16.5):
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(t),"-i",str(out),"-frames:v","1",str(tmp/f"f{t}.png")],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error"]+sum([["-i",str(tmp/f"f{t}.png")] for t in (1.5,4.5,7.5,11.5,16.5)],[])+["-filter_complex","hstack=5,scale=1800:-1","/tmp/claude-0/strip.png"],check=True)
print(out)
