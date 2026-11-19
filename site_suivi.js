/* Suivi par canal + journal des recherches (19 nov. 2026, demande d'Alex : points 1 et 2 du plan).
   Configuration injectée par build.py dans window.RFQ depuis suivi_tags.json :
   - tags : identifiants de suivi Amazon Associés par canal ({"fb":"...-20","ig":"...","tt":"...","nl":"...","rech":"..."}).
     Un canal sans identifiant garde l'identifiant de base. Tant que tout est vide, les liens ne changent pas.
   - journal : formulaire Google qui reçoit les mots cherchés ({"url":".../formResponse","q":"entry.1","n":"entry.2","src":"entry.3"}).
     Vide = rien n'est envoyé.
   Vie privée : on garde seulement le mot cherché (nettoyé), le nombre de résultats et le canal. Jamais d'identité, de témoin ni d'adresse. */
(function(){
var C=window.RFQ||{},BASE="coupdecoeurqc-20",TAGS=C.tags||{},J=C.journal||{};
var CANAUX={fb:1,ig:1,tt:1,nl:1};
function mem(k,v){try{if(v===undefined)return sessionStorage.getItem(k);sessionStorage.setItem(k,v)}catch(e){}return null}

/* 1. Canal d'arrivée : ?src=fb|ig|tt|nl, sinon le site d'où le visiteur vient */
function detecte(){var s=null;
try{var u=new URL(location.href),p=(u.searchParams.get("src")||u.searchParams.get("utm_source")||"").toLowerCase();
if(CANAUX[p])s=p;else if(/^face|^fb/.test(p))s="fb";else if(/^insta/.test(p))s="ig";else if(/^tik/.test(p))s="tt";
if(u.searchParams.has("src")){u.searchParams.delete("src");try{history.replaceState(null,"",u.pathname+(u.search||"")+u.hash)}catch(e){}}}catch(e){}
if(!s){var r=document.referrer||"";if(/facebook\.com|fb\.com|fb\.me/i.test(r))s="fb";else if(/instagram\.com/i.test(r))s="ig";else if(/tiktok\.com/i.test(r))s="tt"}
if(s)mem("rfq_src",s);return s||mem("rfq_src")||""}
var SRC=detecte();
window.RFQ_SRC=SRC;

/* 2. Identifiant Amazon : celui du canal si Alex l'a créé, sinon l'identifiant de base. "rech" = continuer la recherche vers Amazon. */
window.rfqTag=function(genre){return TAGS[genre]||TAGS[SRC]||BASE};
function maj(a){var h=a.getAttribute("href")||"";if(h.indexOf("amazon.ca")<0||h.indexOf("tag="+BASE)<0)return;
var t=window.rfqTag(a.getAttribute("data-rfq")||"");if(t!==BASE)a.setAttribute("href",h.replace("tag="+BASE,"tag="+t))}
function tous(r){[].forEach.call((r||document).querySelectorAll('a[href*="amazon.ca"]'),maj)}
var actif=false;for(var k in TAGS)if(TAGS[k]&&TAGS[k]!==BASE)actif=true;
if(actif){
document.addEventListener("DOMContentLoaded",function(){tous();
try{new MutationObserver(function(ms){ms.forEach(function(m){[].forEach.call(m.addedNodes,function(n){if(n.nodeType===1){if(n.tagName==="A")maj(n);else tous(n)}})})}).observe(document.body,{childList:true,subtree:true})}catch(e){}});
["click","auxclick","touchstart","contextmenu"].forEach(function(ev){document.addEventListener(ev,function(e){var a=e.target.closest&&e.target.closest("a");if(a)maj(a)},true)})}

/* 3. Journal des recherches : un mot cherché est envoyé 1,5 s après la dernière frappe, une seule fois par session */
var VUS={},tm=null;
function propre(q){q=(q||"").toLowerCase().replace(/\s+/g," ").trim().slice(0,80);
if(q.length<3||/@|https?:|www\./.test(q)||/\d{7,}/.test(q.replace(/[\s.\-()]/g,"")))return"";return q}
function envoie(q,n){if(!J.url||!q)return;var k=q+"|"+(n?1:0);if(VUS[k])return;VUS[k]=1;
var f=new URLSearchParams();if(J.q)f.set(J.q,q);if(J.n)f.set(J.n,String(n));if(J.src)f.set(J.src,SRC||"direct");
try{fetch(J.url,{method:"POST",mode:"no-cors",body:f,keepalive:true})}catch(e){}}
window.rfqLog=function(q,n){q=propre(q);clearTimeout(tm);if(!q)return;tm=setTimeout(function(){envoie(q,n)},1500)};
})();
