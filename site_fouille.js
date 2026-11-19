/* Page /recherche/ (19 nov. 2026, demande d'Alex : « la page pour faciliter la recherche » dans tout le volume de rabais du site).
   Lit /recherche.json (tous les deals vérifiés affichables), filtre par mots, catégorie, prix max et verdict, trie, affiche par paquets de 48. */
(function(){
var TAG="coupdecoeurqc-20",PAS=48,D=[],vus=PAS;
var $=function(i){return document.getElementById(i)};
var q=$("fq"),lst=$("fl"),cpt=$("fn"),plus=$("fp"),tri=$("ft");
if(!q)return;
var etat={cat:"",max:0,hot:0};
function n(s){return(s||"").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[’']/g," ")}
function rac(w){return w.length>4?w.replace(/(aux|eaux)$/,"al").replace(/[sx]$/,""):w}
var SYN={casque:["casque","headphone","ecouteur"],ecouteur:["ecouteur","buds","casque"],aspirateur:["aspirateur","vacuum","balai"],friteuse:["friteuse","air fryer","four friteuse"],
cafe:["cafe","espresso","expresso","nespresso","keurig"],montre:["montre","watch"],tele:["tele","televiseur","tv"],parfum:["parfum","eau de"],
"haut-parleur":["haut-parleur","enceinte","speaker","boombox"],brosse:["brosse"],jouet:["jouet","lego","barbie","hot wheels","jeu"],pantoufle:["pantoufle","slipper"],
lego:["lego"],bebe:["bebe","nourrisson","siege d auto","tout-petit"]};
var CATS={"enfants":["enfants","jouets"],"mode":["homme","femme"],"femme":["femme","beaute"]};
var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};
var $$=function(v){return v.toFixed(2).replace(".",",").replace(",00","")+" $"};
function parse(t){var s=n(t),max=0,cat="";if(/\blui\b|\bhomme\b/.test(s)){cat="homme";s=s.replace(/\b(lui|homme)\b/g," ")}else if(/\belle\b|\bfemme\b/.test(s)){cat="femme";s=s.replace(/\b(elle|femme)\b/g," ")}else if(/\benfants?\b/.test(s)){cat="enfants";s=s.replace(/\benfants?\b/g," ")}var m=s.match(/(sous|moins de|max|<)\s*(\d+)/);var m=m;if(m){max=+m[2];s=s.replace(m[0]," ")}
 s=s.replace(/\$/g," ").replace(/\b(pour|de|des|du|la|le|les|un|une|a|et|cadeau|cadeaux)\b/g," ");return{mots:s.split(/\s+/).filter(function(w){return w.length>1}).map(rac),max:max,cat:cat}}
function ok(x,p){if(etat.hot&&!x.h)return false;
 var ct=etat.cat||p.cat;if(ct){var cs=CATS[ct]||[ct];if(cs.indexOf(x.c)<0)return false}
 var mx=p.max||etat.max;if(mx&&x.p>mx)return false;
 var t=" "+n(x.t)+" ";for(var i=0;i<p.mots.length;i++){var w=p.mots[i],al=SYN[w]||[w],bon=false;
  for(var j=0;j<al.length;j++)if(t.indexOf(al[j])>=0){bon=true;break}if(!bon)return false}return true}
var TRI={best:function(a,b){return(b.r+(b.h?15:0)+Math.min(b.e,150)/10)-(a.r+(a.h?15:0)+Math.min(a.e,150)/10)},pct:function(a,b){return b.r-a.r},
eco:function(a,b){return b.e-a.e},bas:function(a,b){return a.p-b.p},haut:function(a,b){return b.p-a.p}};
function carte(x){var u="https://www.amazon.ca/dp/"+x.a+"?tag="+TAG;
 return'<li><a href="'+u+'" target="_blank" rel="sponsored nofollow noopener"><div class="fi">'+(x.i?'<img src="'+esc(x.i)+'" alt="" loading="lazy">':'<span>🛍️</span>')+'<b>-'+x.r+' %</b></div>'
 +'<h3>'+esc(x.t)+'</h3><p class="fpx"><strong>'+$$(x.p)+'</strong>'+(x.w?' <s>'+$$(x.w)+'</s>':'')+'</p>'
 +(x.e>=1?'<p class="fe">Tu économises '+x.e+' $</p>':'')+(x.v?'<p class="fv">'+esc(x.v)+'</p>':'')
 +'<p class="fd">Prix observé le '+esc(x.d)+'</p><span class="fb">Voir le deal 👉</span></a></li>'}
function go(){var p=parse(q.value),L=D.filter(function(x){return ok(x,p)});L.sort(TRI[tri.value]||TRI.best);
 if(window.rfqLog&&q.value.trim())rfqLog(q.value,L.length);
 cpt.textContent=L.length===D.length?D.length+" rabais vérifiés, tous ici":L.length+" rabais trouvés sur "+D.length;
 lst.innerHTML=L.length?L.slice(0,vus).map(carte).join(""):'<li class="fz">Rien pour ça en ce moment. Essaie un mot plus court ou enlève un filtre. Les deals changent chaque jour!</li>';
 plus.hidden=L.length<=vus;plus.textContent="Voir "+Math.min(PAS,L.length-vus)+" rabais de plus ("+(L.length-vus)+" restants)";
 try{var u=new URL(location.href);if(q.value)u.searchParams.set("q",q.value);else u.searchParams.delete("q");history.replaceState(null,"",u)}catch(e){}}
function chips(id,cle){var b=$(id);if(!b)return;b.addEventListener("click",function(ev){var t=ev.target.closest("button");if(!t)return;
 [].forEach.call(b.querySelectorAll("button"),function(x){x.classList.remove("on")});t.classList.add("on");etat[cle]=cle==="cat"?t.dataset.v:+t.dataset.v;vus=PAS;go()})}
chips("fc","cat");chips("fm","max");
$("fh").addEventListener("change",function(){etat.hot=this.checked?1:0;vus=PAS;go()});
q.addEventListener("input",function(){vus=PAS;go()});tri.addEventListener("change",function(){vus=PAS;go()});
plus.addEventListener("click",function(){vus+=PAS;go()});
$("ff").addEventListener("submit",function(ev){ev.preventDefault();q.blur();go()});
try{var v=new URL(location.href).searchParams.get("q");if(v)q.value=v}catch(e){}
fetch("/recherche.json?v="+Date.now().toString().slice(0,7)).then(function(r){return r.json()}).then(function(d){D=d;$("ftot").textContent=d.length;go()})
 .catch(function(){cpt.textContent="Oups, la liste n'a pas chargé. Recharge la page."});
})();
