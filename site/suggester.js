(function(){
var WA='https://wa.me/918305449559';
var OWNER_PHONE='+918305449559', OWNER_LABEL='+91 83054 49559';
/* Owner email — leads are mailed here via formsubmit.co (no backend needed). */
var OWNER_EMAIL='prakhar@indorenursery.com';
var d=document;
var CSS='.pf-btn{position:fixed;left:18px;bottom:18px;z-index:98;background:var(--forest);color:#fff;border:none;border-radius:999px;padding:13px 20px;font-family:Jost,sans-serif;font-size:.95rem;font-weight:600;cursor:pointer;box-shadow:0 10px 28px rgba(22,48,31,.3);display:flex;align-items:center;gap:8px}.pf-btn:hover{background:var(--forest2)}.pf-ov{position:fixed;inset:0;background:rgba(10,24,13,.55);backdrop-filter:blur(3px);z-index:1000;display:none;align-items:center;justify-content:center;padding:16px}.pf-ov.open{display:flex}.pf-box{background:var(--cream);border-radius:26px;max-width:520px;width:100%;max-height:92vh;overflow:auto;padding:30px 30px 26px;position:relative;box-shadow:0 30px 80px rgba(0,0,0,.35)}.pf-x{position:absolute;top:14px;right:16px;border:none;background:none;font-size:1.5rem;color:#5c6b5d;cursor:pointer}.pf-kick{font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:var(--pine);font-weight:600}.pf-box h3{font-family:Fraunces,serif;color:var(--forest);font-size:1.5rem;margin:8px 0 4px}.pf-sub{font-size:.9rem;color:#5c6b5d;margin-bottom:18px}.pf-step label{display:block;font-weight:600;color:var(--forest);margin:12px 0 6px;font-size:.9rem}.pf-step input,.pf-step textarea{width:100%;box-sizing:border-box;border:1px solid #d9d4c2;border-radius:12px;padding:11px 14px;font-family:Jost,sans-serif;font-size:.95rem;background:#fff}.pf-step textarea{min-height:70px;resize:vertical}.pf-chips{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 4px}.pf-chip{border:1px solid #d9d4c2;background:#fff;border-radius:999px;padding:8px 15px;font-size:.85rem;cursor:pointer;color:var(--forest)}.pf-chip.on{background:var(--forest);color:#fff;border-color:var(--forest)}.pf-nav{display:flex;gap:10px;margin-top:20px}.pf-b{flex:1;border:none;border-radius:999px;padding:12px 18px;font-weight:600;font-family:Jost,sans-serif;font-size:.95rem;cursor:pointer;background:var(--lime);color:var(--forest)}.pf-b.ghost{background:transparent;border:1px solid #d9d4c2;color:#5c6b5d;flex:0 0 auto}.pf-b:hover{filter:brightness(1.05)}';
var st=d.createElement('style');st.textContent=CSS;d.head.appendChild(st);
var CHIPS1=[['air','Air-purifying'],['low','Low-maintenance'],['decor','Home decor'],['gift','Gifting'],['office','Office greens'],['outdoor','Outdoor / terrace']];
var CHIPS2=[['event','Wedding / big event'],['bulk','Bulk / corporate order'],['talk','Just want to talk']];
var KW={air:['snake','peace','spider','money','areca','rubber','zz','bamboo','pothos','palm'],low:['snake','zz','jade','cactus','lucky','bamboo','succulent'],decor:['monstera','rubber','areca','dracaena','aglaonema','fiddle','palm','jade'],gift:['lucky','jade','peace','syngonium','aglaonema','succulent'],office:['snake','zz','jade','peace','rubber','dracaena'],outdoor:['croton','hibiscus','rose','jasmine','palm','bougainvillea','kalanchoe']};
var CATBOOST={air:['Indoor Plants','Semi Indoor Plants'],low:['Succulents','Indoor Plants'],decor:['Indoor Plants'],gift:['Gifting Plants'],office:['Indoor Plants'],outdoor:['Outdoor Plants','Landscaping Plants','Seasonal Plants']};
function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function btn(){
 if(d.querySelector('.pf-btn'))return;
 var b=d.createElement('button');b.className='pf-btn';b.innerHTML='\uD83C\uDF3F Find your plant';
 b.onclick=function(){open()};d.body.appendChild(b);
}
function open(){
 var ov=d.getElementById('pf');
 if(!ov){build();ov=d.getElementById('pf')}
 ov.classList.add('open');
 show('pf-s1');
}
function close(){d.getElementById('pf').classList.remove('open')}
function build(){
 var ov=d.createElement('div');ov.className='pf-ov';ov.id='pf';
 var c1=CHIPS1.map(function(c){return '<button type="button" class="pf-chip" data-k="'+c[0]+'">'+c[1]+'</button>'}).join('');
 var c2=CHIPS2.map(function(c){return '<button type="button" class="pf-chip" data-k="'+c[0]+'">'+c[1]+'</button>'}).join('');
 ov.innerHTML='<div class="pf-box"><button class="pf-x" aria-label="Close">\u00d7</button>'
 +'<div class="pf-step" id="pf-s1"><span class="pf-kick">\uD83C\uDF3F Plant finder</span><h3>Let\u2019s find your perfect green</h3><p class="pf-sub">Three quick questions \u2014 we\u2019ll suggest plants that actually fit you.</p>'
 +'<label>Your name</label><input id="pf-name" placeholder="e.g. Rohit" autocomplete="name">'
 +'<div class="pf-nav"><button class="pf-b pf-next">Continue</button></div></div>'
 +'<div class="pf-step" id="pf-s2" hidden><span class="pf-kick">Hi <span id="pf-hi"></span>!</span><h3>What\u2019s the best number to reach you?</h3><p class="pf-sub">We\u2019ll only use it to confirm your enquiry \u2014 no spam, ever.</p>'
 +'<label>Phone number</label><input id="pf-phone" inputmode="numeric" maxlength="10" placeholder="10-digit mobile">'
 +'<div class="pf-nav"><button class="pf-b ghost pf-back">\u2190 Back</button><button class="pf-b pf-next">Continue</button></div></div>'
  +'<div class="pf-step" id="pf-s3" hidden><span class="pf-kick">Almost there</span><h3>What are you looking for?</h3><p class="pf-sub">Pick anything that fits \u2014 or write it in your own words.</p>'
 +'<div class="pf-chips">'+c1+'</div><div class="pf-chips" style="margin-top:8px">'+c2+'</div>'
 +'<label>Tell us more <span style="font-weight:400;color:#8a9a8b">(optional)</span></label><textarea id="pf-note" placeholder="e.g. need plants for a shop opening next month"></textarea>'
 +'<div class="pf-nav"><button class="pf-b ghost pf-back">\u2190 Back</button><button class="pf-b pf-next">Show my matches</button></div></div>'
 +'<div class="pf-step" id="pf-s4" hidden></div>'
 +'</div>';
 d.body.appendChild(ov);
 ov.querySelector('.pf-x').onclick=close;
 ov.addEventListener('click',function(e){if(e.target===ov)close()});
 ov.querySelectorAll('.pf-chip').forEach(function(ch){ch.onclick=function(){ch.classList.toggle('on')}});
 ov.querySelectorAll('.pf-back').forEach(function(b){b.onclick=function(){var s=d.querySelector('.pf-step:not([hidden])').id;show(s=='pf-s2'?'pf-s1':'pf-s2')}});
 ov.querySelectorAll('.pf-next').forEach(function(nb){nb.onclick=next});
}
function show(id){d.querySelectorAll('.pf-step').forEach(function(s){s.hidden=s.id!=id})}
function next(){
 var ov=d.getElementById('pf'),cur=d.querySelector('.pf-step:not([hidden])').id;
 if(cur=='pf-s1'){
  var n=d.getElementById('pf-name').value.trim();
  if(!n){d.getElementById('pf-name').style.borderColor='#c0392b';return}
  d.getElementById('pf-hi').textContent=n.split(' ')[0];show('pf-s2');
 }else if(cur=='pf-s2'){
  var p=d.getElementById('pf-phone').value.replace(/\D/g,'');
  if(p.length!=10){d.getElementById('pf-phone').style.borderColor='#c0392b';return}
  show('pf-s3');
 }else{finish()}
}
function picks(){
 var ks=[].slice.call(d.querySelectorAll('.pf-chip.on')).map(function(c){return c.dataset.k});
 var ks1=ks.filter(function(k){return KW[k]}),sp=ks.filter(function(k){return !KW[k]});
 var note=d.getElementById('pf-note').value.toLowerCase();
 if(/event|wedding|bulk|corporat|talk|party|landscap|garden|office decor|opening/.test(note))sp.push('note');
 if(/plant|flower|indoor|outdoor|green|pot|terrace|balcony|air|gift/.test(note)&&!ks1.length)ks1.push('decor');
 return {ks1:ks1,sp:sp};
}
function score(p,ks1,note){
 var n=p.name.toLowerCase(),s=0;
 ks1.forEach(function(k){KW[k].forEach(function(w){if(n.indexOf(w)>-1)s+=3});
 (p.categories||[]).forEach(function(c){if(CATBOOST[k].indexOf(c)>-1)s+=1})});
 if(note)note.split(/[^a-z]+/).forEach(function(w){if(w.length>3&&n.indexOf(w)>-1)s+=4});
 return s;
}
function saveLead(sp){
 var ks=[].slice.call(d.querySelectorAll('.pf-chip.on')).map(function(c){return c.textContent});
 var lead={name:d.getElementById('pf-name').value.trim(),phone:d.getElementById('pf-phone').value,need:ks,note:d.getElementById('pf-note').value.trim(),page:location.pathname,at:new Date().toLocaleString('en-IN')};
 try{var L=JSON.parse(localStorage.getItem('pf_leads')||'[]');L.push(lead);localStorage.setItem('pf_leads',JSON.stringify(L))}catch(e){}
 var msg='New enquiry from website ('+location.pathname+')%0A%0AName: '+encodeURIComponent(lead.name)+'%0APhone: '+encodeURIComponent(lead.phone)+'%0ALooking for: '+encodeURIComponent(ks.join(', ')||'-')+'%0ANote: '+encodeURIComponent(lead.note||'-');
 fetch('https://formsubmit.co/ajax/'+OWNER_EMAIL,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify({name:lead.name,phone:lead.phone,looking_for:ks.join(', '),note:lead.note,page:location.pathname,_subject:'New website enquiry \u2014 '+lead.name})}).catch(function(e){});
 return msg;
}
function finish(){
 var p=picks(),msg=saveLead(p.sp);
 var out=d.getElementById('pf-s4'),h='';
 var ownerBit='<div class="pf-owner" style="margin:16px 0;background:#fff;border:1px solid #d9d4c2;border-radius:16px;padding:16px">'
 +'<b style="font-family:Fraunces,serif;color:var(--forest)">Talk to the owner directly</b>'
 +'<p style="font-size:.88rem;color:#5c6b5d;margin:6px 0 12px">For events, bulk orders or a quick chat \u2014 the nursery owner personally handles these.</p>'
 +'<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="pf-b" style="flex:0 0 auto;text-decoration:none" href="tel:'+OWNER_PHONE+'">\uD83D\uDCDE Call '+OWNER_LABEL+'</a>'
 +'<a class="pf-b ghost" style="flex:0 0 auto;text-decoration:none" href="'+WA+'?text='+msg+'" target="_blank">WhatsApp owner</a></div></div>';
 if(p.sp.length){h+=ownerBit}
 h+='<div id="pf-sug" style="margin-top:6px"></div>';
 out.innerHTML=h;show('pf-s4');
 if(p.ks1.length){
  fetch('/data/catalog.json').then(function(r){return r.json()}).then(function(cat){
   var note=d.getElementById('pf-note').value.toLowerCase();
   var ranked=cat.filter(function(p2){return p2.image&&p2.price}).map(function(p2){return [p2,score(p2,p.ks1,note)]}).filter(function(x){return x[1]>0}).sort(function(a,b){return b[1]-a[1]}).slice(0,4);
   if(!ranked.length)return;
   var cards='';
   ranked.forEach(function(x){
    var p2=x[0];
    var img=p2.image.split('uploads/')[1].split('/').join('_');
    cards+='<a href="/plants/'+p2.slug+'/" style="text-decoration:none"><div style="background:#fff;border:1px solid #d9d4c2;border-radius:14px;overflow:hidden"><img loading="lazy" src="/images/'+img+'" alt="" style="width:100%;height:90px;object-fit:cover"><div style="padding:10px 12px"><b style="font-size:.85rem;color:var(--forest)">'+p2.name+'</b><div style="font-size:.85rem;color:#5c6b5d;margin-top:2px">Rs '+Number(p2.price).toLocaleString('en-IN')+'</div></div></div></a>';
   });
   d.getElementById('pf-sug').innerHTML='<span class="pf-kick">Suggested for you</span><div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:10px;margin-top:10px">'+cards+'</div><p style="font-size:.8rem;color:#8a9a8b;margin-top:10px">Your details were saved and shared with the nursery.</p>';
  });
 }
}
if(d.readyState=='loading'){d.addEventListener('DOMContentLoaded',btn)}else{btn()}
try{if(!sessionStorage.getItem('pf_shown')){setTimeout(function(){if(!d.getElementById('pf').classList.contains('open')){open();sessionStorage.setItem('pf_shown','1')}},12000)}}catch(e){}
})();
