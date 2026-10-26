#!/usr/bin/env python3
"""Reel : les marques chouchous. Pas de pourcentage (intemporel)."""
import pathlib, tempfile, subprocess, html as H
import pack
e=H.escape
B=[("💄","L'Oréal"),("💋","Maybelline"),("🌹","Lancôme"),("🤍","Clarins"),("🌿","Garnier"),("✨","e.l.f."),("🍳","Ninja"),("🌀","Dyson"),("☕","Nespresso"),("🏔️","North Face"),("🧥","Columbia"),("👟","Skechers")]
tiles="".join(f'<div class="t" style="--d:{3.0+i*0.28:.2f}s"><i>{ic}</i><b>{e(n)}</b></div>' for i,(ic,n) in enumerate(B))
CSS="""*{box-sizing:border-box;margin:0}html,body{width:720px;height:1280px;overflow:hidden}
body{background:linear-gradient(160deg,#C1121F,#8E0B16);color:#fff;position:relative;font-family:"Barlow Semi Condensed",Arial,sans-serif}
.logo{position:absolute;top:44px;left:48px;display:flex;gap:10px;align-items:center;font-size:30px;font-weight:700;letter-spacing:2px}.logo b{color:#FFC72C}
.s{position:absolute;left:0;right:0;padding:0 44px;opacity:0;text-align:center}
@keyframes sc{0%{opacity:0;transform:scale(.8)}12%,86%{opacity:1;transform:none}100%{opacity:0;transform:translateY(-40px)}}
.h1{top:300px;font-size:92px;line-height:1.05;animation:sc 3s 0s ease both}.h1 i{font-style:normal;color:#FFC72C}
.hd{top:150px;font-size:44px;font-weight:700;color:#FFC72C;animation:sc 6.6s 3s ease both}
.g{position:absolute;top:330px;left:34px;right:34px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.t{background:#fff;color:#1A1A1A;border-radius:22px;padding:18px 6px;text-align:center;opacity:0;position:relative;animation:pop .45s var(--d) ease forwards,out .4s 9.4s ease forwards}
.t i{display:block;font-style:normal;font-size:52px;line-height:1.1}.t b{display:block;font-size:27px;margin-top:4px}
.t::after{content:'OFFRES';position:absolute;top:-10px;right:4px;background:#FFC72C;color:#8E0B16;font-size:15px;font-weight:800;padding:2px 8px;border-radius:999px;transform:rotate(8deg)}
@keyframes pop{0%{opacity:0;transform:scale(.4) rotate(-8deg)}70%{transform:scale(1.08)}100%{opacity:1;transform:none}}@keyframes out{to{opacity:0}}
.m{top:330px;font-size:80px;line-height:1.08;animation:sc 3.6s 9.8s ease both}.m i{font-style:normal;color:#FFC72C}
.m .k{display:inline-block;margin-top:30px;font-size:120px;animation:tap 1s 10.6s 3}
@keyframes tap{50%{transform:scale(.8)}}
.end{top:300px;animation:end 3.6s 13.4s ease forwards}@keyframes end{0%{opacity:0;transform:scale(.85)}25%,100%{opacity:1;transform:none}}
.end .t2{font-size:84px;line-height:1.02;color:#FFC72C}.end .u{margin-top:34px;display:inline-block;background:#FFC72C;color:#8E0B16;border-radius:999px;padding:18px 34px;font-size:46px}
.end .x{margin-top:28px;font-size:42px;font-weight:700}
.tiny{position:absolute;left:30px;right:30px;bottom:34px;text-align:center;font-size:20px;opacity:.92;font-weight:600}"""
html=f'''<!doctype html><html><head><meta charset="utf-8">{pack.FONTS}<style>{CSS}</style></head><body>
<div class="logo">{pack.BOLT.replace('width="38" height="60"','width="26" height="42"')}<span>RABAIS <b>FLASH</b> QC</span></div>
<div class="s h1 an">TA MARQUE<br>PRÉFÉRÉE EST<br><i>PEUT-ÊTRE EN<br>RABAIS 👀</i></div>
<div class="s hd an">LES CHOUCHOUS<br>DES QUÉBÉCOISES 💖</div>
<div class="g">{tiles}</div>
<div class="s m an">UN CLIC<br>=<br><i>TOUTES SES<br>OFFRES</i><br><span class="k">👆</span></div>
<div class="s end"><div class="t2 an">C'EST QUOI<br>TA MARQUE? 💬</div><div class="u an">RABAISFLASHQC.CA</div><div class="x">🔗 Lien dans la bio</div></div>
<div class="tiny">⚡ Offres fixées par Amazon, sujettes à changement · {e(pack.DISC)}</div></body></html>'''
tmp=pathlib.Path(tempfile.mkdtemp())
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    br,ctx,pg=pack.render(pw,html,(720,1280),tmp,"marques",video=True)
    pg.wait_for_timeout(18500); ctx.close(); br.close()
webm=sorted(tmp.glob("*.webm"))[-1]
out=pack.OUT/"reel-marques.mp4"
subprocess.run(["ffmpeg","-y","-loglevel","error","-ss","0.4","-i",str(webm),"-c:v","libx264","-pix_fmt","yuv420p","-crf","24","-preset","veryfast","-an","-movflags","+faststart","-t","17.5",str(out)],check=True)
ts=(1.5,6.5,8.5,11.5,16.5)
for t in ts: subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(t),"-i",str(out),"-frames:v","1",str(tmp/f"f{t}.png")],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error"]+sum([["-i",str(tmp/f"f{t}.png")] for t in ts],[])+["-filter_complex","hstack=5,scale=1800:-1","/tmp/claude-0/strip.png"],check=True)
print(out)
