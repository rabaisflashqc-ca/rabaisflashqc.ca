/* Chercheur de rabais intelligent (19 nov. 2026, demande d'Alex) : cherche dans TOUS les deals vérifiés du site (/recherche.json),
   résultats pendant qu'on tape, sans accents ni pluriels, synonymes FR/EN, « sous 50 $ », « pour lui / elle / enfants », grandes marques en un clic. */
(function(){
var TAG="coupdecoeurqc-20",MIN=15,D=null,LOAD=null,TOUT=[];
var $=function(i){return document.getElementById(i)};
var f=$("rq-f"),q=$("rq-q"),r=$("rq-r"),m=$("rq-m"),l=$("rq-l"),b=$("rq-b"),t=$("rq-t"),mo=$("rq-more"),mk=$("rq-mk");
if(!f)return;
function n(s){return(s||"").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[’']/g," ")}
function racine(w){return w.length>4?w.replace(/(aux|eaux)$/,"al").replace(/[sx]$/,""):w}
var SYN={casque:["casque","headphone","ecouteur"],ecouteur:["ecouteur","buds","earbud","casque"],aspirateur:["aspirateur","vacuum","nettoyeur","balai"],
friteuse:["friteuse","air fryer","airfryer"],cafe:["cafe","expresso","espresso","nespresso","keurig","cafetiere"],expresso:["expresso","espresso","cafe"],
montre:["montre","watch"],tele:["televiseur","tv","tele"],televiseur:["televiseur","tv"],tv:["televiseur","tv"],tablette:["tablette","tab ","ipad"],
parfum:["parfum","eau de toilette","eau de parfum"],enceinte:["enceinte","haut-parleur","speaker"],"haut-parleur":["haut-parleur","enceinte","speaker"],
melangeur:["melangeur","mixeur","blender"],mixeur:["mixeur","melangeur","blender"],brosse:["brosse"],rasoir:["rasoir","oneblade","tondeuse"],
seche:["seche","sechoir"],sechoir:["sechoir","seche-cheveux","seche"],robot:["robot"],jouet:["lego","magna-tiles","jouet","playmobil","melissa","vtech","crayola","pets alive","bitzee","gabby"],
boxer:["boxer"],jean:["jean"],sapin:["sapin"],camera:["camera","sonnette"],sonnette:["sonnette","ring","doorbell"],chandail:["chandail","hoodie","capuchon"]};
var MARQUES=["Dyson","LEGO","Sony","Bose","Samsung","Apple","JBL","Levi's","Ninja","Shark","Oral-B","Philips","Garmin","De'Longhi","Nespresso","Vitamix","Cuisinart","BISSELL","Hoover","Magna-Tiles","DEWALT","Hugo Boss","Calvin Klein","Stanley","Melissa & Doug","Ring","Blink","Anker","Soundcore","SAXX","Crest","Conair","BaBylissPRO","Remington","roborock","Eufy","Keurig","KitchenAid","Henckels","Lagostina","Playmobil","VTech","Crayola","Coway","Canon","Fujifilm","Google","Fitbit","Tile","Thermos","Eddie Bauer","Shapermint","Amazon Kids","Black+Decker","FoodSaver","Chefman","Shokz","Sennheiser","Tefal","Braun","nutribullet"];
function charge(){if(D)return Promise.resolve(D);if(!LOAD)LOAD=fetch("/recherche.json",{cache:"no-cache"}).then(function(x){return x.json()}).then(function(j){D=j.map(function(x){x.n=n(x.t+" "+x.c);return x});marques();return D}).catch(function(){D=[];return D});return LOAD}
var VOC=null;
function lev(a,b,m){if(Math.abs(a.length-b.length)>m)return m+1;var p=[],i,j;for(j=0;j<=b.length;j++)p[j]=j;for(i=1;i<=a.length;i++){var c=[i],mn=i;for(j=1;j<=b.length;j++){c[j]=Math.min(p[j]+1,c[j-1]+1,p[j-1]+(a[i-1]===b[j-1]?0:1));if(c[j]<mn)mn=c[j]}if(mn>m)return m+1;p=c}return p[b.length]}
function vocab(){if(VOC)return VOC;var u={};D.forEach(function(x){x.n.split(/[^a-z0-9]+/).forEach(function(w){if(w.length>3)u[w]=(u[w]||0)+1})});Object.keys(SYN).forEach(function(k){u[k]=(u[k]||0)+5});return VOC=u}
function corrige(o){var V=vocab(),ch=false,mots=o.mots.map(function(w){if(w.length<4||V[w]||V[racine(w)]||SYN[w])return w;var best=null,bd=9,m=w.length>6?2:1;Object.keys(V).forEach(function(k){var d=lev(w,k,m);if(d<=m&&(d<bd||(d===bd&&V[k]>V[best]))){bd=d;best=k}});if(best){ch=true;return best}return w});return ch?mots:null}
function money(v){return v.toFixed(2).replace(".",",").replace(/\B(?=(\d{3})+(?!\d))/g," ")+" $"}
function az(v,p){return"https://www.amazon.ca/s?k="+encodeURIComponent(v)+"&pct-off="+(p||MIN)+"-&tag="+TAG}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function marques(){if(!mk)return;var c=MARQUES.map(function(b){var k=n(b),re=new RegExp("(^|[^a-z])"+k.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+"([^a-z]|$)");return[b,D.filter(function(x){return re.test(x.n)}).length]}).filter(function(x){return x[1]>0}).slice(0,18);
if(!c.length){mk.parentNode.hidden=true;return}mk.innerHTML=c.map(function(x){return'<button type="button" data-q="'+esc(x[0])+'">'+esc(x[0])+' <small>'+x[1]+'</small></button>'}).join("");
[].forEach.call(mk.querySelectorAll("button"),function(x){x.addEventListener("click",function(){q.value=x.getAttribute("data-q");go(true)})})}
function analyse(v){var s=n(v),o={max:null,min:null,cats:null,hot:false,mots:[]},x;
if(x=s.match(/(?:sous|moins de|max(?:imum)?|<|en bas de|pas plus de)\s*(\d+)/)){o.max=+x[1];s=s.replace(x[0]," ")}
if(x=s.match(/(\d+)\s*\$?\s*(?:et moins|ou moins|max)/)){o.max=+x[1];s=s.replace(x[0]," ")}
if(x=s.match(/(?:plus de|au-dessus de|>)\s*(\d+)/)){o.min=+x[1];s=s.replace(x[0]," ")}
s=s.replace(/\$/g," ");
if(/ca vaut le clic|gros rabais|meilleur|top/.test(s)){o.hot=true;s=s.replace(/ca vaut le clic|gros rabais|meilleurs?|top/g," ")}
var A=[[/\b(pour )?(lui|homme|hommes|papa|chum|mari|gars|grand-pere)\b/,["homme","tech","plein-air"],"homme"],[/\b(pour )?(elle|femme|femmes|maman|blonde|epouse|fille|grand-mere)\b/,["femme","beaute"],"femme"],
[/\b(pour )?(enfants?|kids?|bebe|ado|ados|garcon|fillette|petits?-enfants?|jouets?)\b/,["enfants","jouets"],null],[/\b(chien|chat|animal|animaux)\b/,["animaux"],null],[/\b(cuisine|maison)\b/,["maison"],null],[/\b(beaute|soins?)\b/,["beaute"],null],[/\b(techno|tech|electronique|gadget)\b/,["tech"],null]];
A.forEach(function(a){var z=s.match(a[0]);if(z){o.cats=(o.cats||[]).concat(a[1]);if(a[2])o.genre=a[2];s=s.replace(z[0]," ")}});
s=s.replace(/\b(cadeau|cadeaux|idee|idees|pour|un|une|des|de|du|la|le|les|a|en|et|qui|vaut|deal|deals|rabais|aubaine|aubaines|pas cher|cher)\b/g," ");
o.mots=s.split(/\s+/).filter(function(w){return w.length>1});return o}
function score(x,o){var s=x.r+(x.h?40:0)+(x.i?10:0);if(o.genre&&x.n.indexOf(o.genre)>-1)s+=25;return s}
function cherche(o){var vu={};return D.filter(function(x){if(o.max!=null&&x.p>o.max)return false;if(o.min!=null&&x.p<o.min)return false;if(o.hot&&!x.h)return false;
if(o.cats&&!o.mots.length&&o.cats.indexOf(x.c)<0&&!(o.genre&&x.n.indexOf(o.genre)>-1))return false;
return o.mots.every(function(w){var r=racine(w),alts=SYN[w]||SYN[r]||[r];return alts.some(function(a){return x.n.indexOf(a)>-1})})}).sort(function(a,b){return score(b,o)-score(a,o)}).filter(function(x){var k=n(x.t);if(vu[k])return false;vu[k]=1;return true})}
function carte(x){var pic=x.i?'<div class="pic"><img src="'+esc(x.i)+'" alt="'+esc(x.t.slice(0,80))+'" loading="lazy" width="84" height="84"><b>-'+x.r+'%</b></div>':'<div class="tag">-'+x.r+'%<small>rabais</small></div>';
var badge=x.v?'<span class="v'+(x.h?" hot":"")+'">'+esc(x.v)+'</span>':'<span>🔥 Deal du moment</span>';
return'<li class="deal" data-asin="'+x.a+'">'+pic+'<div><p class="badges">'+badge+'</p><h3>'+esc(x.t)+'</h3><p class="px">'+(x.w?'<s>'+money(x.w)+'</s> ':'')+'<b>'+money(x.p)+'</b><span>-'+x.r+' %</span>'+(x.e>=1?'<em>Tu économises '+x.e+' $</em>':'')+'<small>prix vérifié le '+esc(x.d)+'</small></p><a class="go" href="https://www.amazon.ca/dp/'+x.a+'?tag='+TAG+'" target="_blank" rel="sponsored nofollow noopener">Voir le deal 👉</a></div></li>'}
function montre(k){l.innerHTML=TOUT.slice(0,k).map(carte).join("");mo.hidden=TOUT.length<=k;mo.textContent="Voir les "+(TOUT.length-k)+" autres deals 👇"}
function go(scroll){var v=q.value.trim();if(v.length<2){r.hidden=true;l.innerHTML="";return}
charge().then(function(){var o=analyse(v);TOUT=cherche(o);
var corr=null;
if(!TOUT.length&&o.mots.length){var cm=corrige(o);if(cm){var oc=JSON.parse(JSON.stringify(o));oc.mots=cm;var rc=cherche(oc);if(rc.length){TOUT=rc;o=oc;corr=cm.join(" ")}}}
if(!TOUT.length&&o.mots.length>1){for(var ii=0;ii<o.mots.length&&!TOUT.length;ii++){var o2=JSON.parse(JSON.stringify(o));o2.mots=[o.mots[ii]];TOUT=cherche(o2);if(TOUT.length)corr=o.mots[ii]}}
r.hidden=false;var k=TOUT.length;
if(k){var h=TOUT.filter(function(x){return x.h}).length;m.innerHTML="🎉 <b>"+k+(k>1?" deals vérifiés":" deal vérifié")+"</b> pour « "+esc(corr||v)+" »"+(h?" · dont "+h+" 🔥 Ça vaut le clic":"");b.textContent="Encore plus de rabais sur « "+v+" » 👉"}
else{m.textContent="Pas encore dans notre tri. Pas grave : on t'amène direct sur les rabais de 15 % et plus 👇";b.textContent="Voir les rabais sur « "+v+" » 👉"}
montre(12);var az_q=(o.mots.join(" ")||v);b.href=az(az_q,MIN);t.textContent="🔥 Seulement les gros rabais (30 % et plus)";t.href=az(az_q,30);var t5=$("rq-t50");if(!t5){t5=document.createElement("a");t5.id="rq-t50";t5.className=t.className;t5.target=t.target;t5.rel=t.rel;t.parentNode.insertBefore(t5,t.nextSibling)}t5.textContent="💥 Les méga rabais (50 % et plus) sur « "+az_q+" »";t5.href=az(az_q,50);
if(scroll&&window.innerWidth<700)setTimeout(function(){m.scrollIntoView({behavior:"smooth",block:"start"})},60)})}
var tm;q.addEventListener("input",function(){clearTimeout(tm);tm=setTimeout(function(){go(false)},180)});
q.addEventListener("focus",charge,{once:true});
f.addEventListener("submit",function(e){e.preventDefault();q.blur();go(true)});
mo.addEventListener("click",function(){montre(TOUT.length)});
[].forEach.call(document.querySelectorAll(".rq-ch button[data-q]"),function(x){x.addEventListener("click",function(){q.value=x.getAttribute("data-q");go(true)})});
charge().then(function(){var c=$("rq-n");if(c&&D.length>=10)c.textContent=D.length+" deals vérifiés à fouiller, en un clic 👇";
var u=new URLSearchParams(location.search).get("q");if(u){q.value=u;go(true)}});
})();
