import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "parts"))
from shell import HEAD, FOOT, FONTS, SCRIPT
from urllib.parse import quote as UQ

from lib.events_imagery import OCCASION_CARDS, STYLING_GALLERY, gallery_src, occ_src

WA = "https://wa.me/918305449559"
occ = "".join(
    '<a class="occ" href="'
    + WA
    + "?text="
    + UQ("Hi! I'm interested in " + n.lower() + " plant decor.")
    + '" target="_blank"><img loading="lazy" src="'
    + occ_src(fn)
    + '" alt="'
    + alt
    + '" style="object-position:'
    + pos
    + '"><span class="t"><em>'
    + tag
    + "</em><b>"
    + n
    + "</b><p>"
    + d
    + "</p></span></a>"
    for n, tag, d, fn, alt, pos in OCCASION_CARDS
)
quick = "".join(
    '<a href="/events/' + sl + '/">' + n + "</a>"
    for n, sl in [
        ("Corporate Greenery", "corporate"),
        ("Wedding Stages", "weddings"),
        ("Party Installs", "parties"),
        ("Landscaping", "landscaping"),
    ]
)
items = "".join(
    '<figure class="item" data-cap="'
    + c
    + '"><img loading="lazy" src="'
    + gallery_src(fn)
    + '" alt="'
    + alt
    + '" style="object-position:'
    + pos
    + '"><span>'
    + c
    + "</span></figure>"
    for c, fn, alt, pos in STYLING_GALLERY
)
grid = '<div class="ev-grid mgal">' + items + "</div>"
names = ["PRIDE Hotels", "\u0938\u0943\u091c\u0928", "SAJDHAJ", "\u0932\u0915\u094d\u0937\u094d\u092e\u0940 Sweets", "Kashiwal Honda"]
half = "".join("<b>" + n + '</b><span class="dot"></span>' for n in names)
marquee = '<div class="marquee"><div class="mtrack">' + half + half + "</div></div>"
page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Events &amp; Decor Plant Styling in Indore | Indore Nursery</title><meta name="description" content="Plant decor for corporate gifting, hotels, weddings, parties and big events in Indore \u2014 designed, delivered and set up by Indore Nursery. Enquire on WhatsApp.">
{FONTS}<link rel="stylesheet" href="/style.css"></head><body>
{HEAD}
<section class="ev-hero"><div class="container"><div class="inner" style="padding:0"><span class="kicker">Events &amp; Decor</span><h1 style="font-size:clamp(2rem,4.5vw,3.2rem);margin:14px 0">Plant decor for occasions <em style="font-style:italic;color:var(--lime)">that matter.</em></h1><p style="opacity:.9;max-width:560px">From corporate gifting to wedding stages \u2014 we help you pick the plants, design the look, deliver everything and set it up, anywhere in Indore.</p><div class="hstats" style="max-width:560px"><div><b>110+</b>events &amp; spaces styled</div><div><b>25+</b>venues &amp; hotels supplied</div><div><b>100%</b>plants from our nursery</div></div></div></div></section>
<section><div class="container">
<div class="ev-quick">{quick}</div>
</div></section>
<section style="padding-top:8px"><div class="container"><span class="eyebrow" style="display:block;text-align:center">Where plants do the talking</span><h2 class="sec">Occasions we style</h2><div class="occ-grid">{occ}</div></div></section>
<section class="alt" style="background:var(--cream2)"><div class="container"><span class="eyebrow" style="display:block;text-align:center">Looks we&#8217;ve created</span><h2 class="sec">A peek at our styling</h2><p class="sub" style="text-align:center;margin-left:auto;margin-right:auto">Tap any look to view it full-screen \u2014 then tell us which one is yours.</p>
{grid}
<div style="text-align:center;margin-top:40px"><a class="btn" href="{WA}?text={UQ('Hi! I want plant decor for my event in Indore.')}" target="_blank">Plan my event on WhatsApp</a></div>
</div></section>
<div class="mhead" style="margin-top:34px"><span class="eyebrow">Venues &amp; brands we&#8217;ve supplied</span></div>
{marquee}
<section style="padding:56px 0"><div class="container"><div class="svc-band"><h2>Have an event coming up?</h2><p>Share your date, venue and the look you have in mind \u2014 we&#8217;ll reply with a design note and quote the same day.</p><a class="btn-wa" href="{WA}?text={UQ('Hi! I want plant decor for my event in Indore.')}" target="_blank">WhatsApp us now</a></div></div></section>
{FOOT}{SCRIPT}
<div class="lb" id="lb"><button class="x">&#10005;</button><button class="prev">&#8592;</button><img id="lbimg" src="" alt=""><button class="next">&#8594;</button><div class="cap" id="lbcap"></div></div>
<script>
(function(){{
var g=document.querySelector('.ev-grid'),lb=document.getElementById('lb'),im=document.getElementById('lbimg'),cap=document.getElementById('lbcap'),cur=0,vis=[];
function show(n){{cur=(n+vis.length)%vis.length;im.src=vis[cur].querySelector('img').src;cap.textContent=vis[cur].dataset.cap;}}
g.addEventListener('click',function(e){{var it=e.target.closest('.item');if(!it)return;vis=[].slice.call(g.querySelectorAll('.item'));show(vis.indexOf(it));lb.classList.add('open');}});
document.querySelector('.lb .x').onclick=function(){{lb.classList.remove('open')}};
document.querySelector('.lb .prev').onclick=function(e){{e.stopPropagation();show(cur-1)}};
document.querySelector('.lb .next').onclick=function(e){{e.stopPropagation();show(cur+1)}};
lb.addEventListener('click',function(e){{if(e.target===lb)lb.classList.remove('open')}});
document.addEventListener('keydown',function(e){{if(!lb.classList.contains('open'))return;if(e.key==='Escape')lb.classList.remove('open');if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1);}});
}})();
</script></body></html>"""
open(os.path.join(ROOT, "site", "events", "index.html"), "w", encoding="utf-8").write(page)
print("events page bytes:", len(page))
