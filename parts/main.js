(function(){
var d=document;
var b=d.querySelector('.burger'),dr=d.querySelector('.drawer');
if(b&&dr){
  b.addEventListener('click',function(){dr.classList.add('open')});
  var x=dr.querySelector('.x');
  if(x)x.addEventListener('click',function(){dr.classList.remove('open')});
}
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}});
  },{threshold:.1});
  d.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
}else{
  d.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')});
}
var t=d.getElementById('top');
if(t){
  window.addEventListener('scroll',function(){t.style.display=window.scrollY>600?'flex':'none'});
  t.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'})});
}
})();
