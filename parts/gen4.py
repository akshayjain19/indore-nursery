import sys,glob,re; sys.path.insert(0,'parts')
exec(open('parts/gen1.py').read())
from shell import HEAD,FOOT,FONTS,SCRIPT
week=next((p for p in C if 'pachira' in p['slug']),None) or next((p for p in C if 'money' in p['slug'].lower()),None) or C[0]
CATS=[('Indoor Plants','indoor-plants'),('Outdoor Plants','outdoor-plants'),('Succulents','succulents'),('Pots','pots'),('Gifting Plants','gifting-plants'),('Soil & Fertilizer','soil-and-fertilizer')]
CATIMG={'Indoor Plants':'img/home/indoor.jpg','Outdoor Plants':'img/home/outdoor.jpg','Succulents':'img/home/succulents.jpg'}
cats=''.join('<a class="cat" href="/category/'+s+'/"><img loading="lazy" src="/'+(CATIMG[n] if n in CATIMG else loc(next((p.get('image') for p in bycat.get(n,[]) if p.get('image')),None)))+'" alt="'+H.escape(n)+'"><b>'+n+'</b></a>' for n,s in CATS)
hero=('<div class="inner"><span class="kicker">A working nursery in Indore &#8212; now online</span>'
 '<h1>Where Indore comes <em>to go green.</em></h1>'
 '<p>Not a warehouse. A real nursery &#8212; every plant raised, hand-picked and packed by our own team before it reaches your door.</p>'
 '<a class="btn" href="/plants/">Browse the Nursery</a><a class="btn ghost" href="https://wa.me/918305449559?text=Hi%20Indore%20Nursery!" target="_blank">Ask us on WhatsApp</a>'
 '<div class="hstats"><div><b>Real nursery</b>grown by our own team</div><div><b>Same day</b>delivery in Indore</div><div><b>Expert</b>guidance on WhatsApp</div></div></div>')
SEASONS=('<a class="season summer" href="/season/summer/">Summer<small>Heat-loving blooms</small></a>'
 '<a class="season monsoon" href="/season/monsoon/">Monsoon<small>Best time to plant</small></a>'
 '<a class="season winter" href="/season/winter/">Winter<small>Cool-season flowers</small></a>'
 '<a class="season year" href="/season/year/">Year-round<small>Evergreen favourites</small></a>')
BEN=[('Fresher air','Leaves quietly filter the air you breathe, all day, for free.'),
('Quieter minds','Green corners soften a room the way music does &#8212; you feel it before you notice it.'),
('Better workdays','A plant on the desk keeps long hours at the screen a little kinder.'),
('Comfortable rooms','Plants release moisture, easing dry air in every season.'),
('A gentler footprint','Living decor instead of plastic &#8212; the simplest green choice there is.'),
('Warmer welcomes','Nothing makes a home or office feel settled like something alive in it.')]
impact=''.join('<div class="why-item reveal"><h4>'+t+'</h4><p>'+p+'</p></div>' for t,p in BEN)
def good(f):
    m=re.search(r'-(\d+)x(\d+)\.',f); return (not m) or int(m.group(1))>=500
EV=[f for f in sorted(glob.glob('site/images/2022_05_013A*.jpg')) if good(f)][3:7]
caps=['Corporate greenery','Wedding stages','Party installs','Landscaping']
MAP={"Corporate greenery":"corporate","Wedding stages":"weddings","Party installs":"parties","Landscaping":"landscaping"}
evt=''.join('<a class="event" href="/events/'+MAP[c]+'/"><img loading="lazy" src="/img/home/test.jpg" alt="'+c+'"><div class="cap">'+c+'</div></a>' for f,c in zip(EV,caps))
BEST=['snake-plant-senseveria','zamia-zz-small','jade-plant-m','lucky-bamboo','peace-lily','aglaonema-snow-white','rubber-plant-2','spider-plant']
byslug={p['slug']:p for p in C}
RAIL=[byslug[s] for s in BEST if s in byslug and byslug[s].get('image') and byslug[s].get('price')]
rail=''.join(card(p) for p in RAIL)
wkimg=loc(week.get('image'))
week_html=('<div class="wimg"><img src="/'+wkimg+'" alt="'+H.escape(H.unescape(week['name']))+'"></div>'
 '<div><span class="eyebrow">This week at the nursery</span><h2>'+H.escape(H.unescape(week['name']))+'</h2>'
 '<p>The money tree&#8217;s braided trunk and glossy leaves make it the easiest statement plant we grow &#8212; happy in bright indirect light, content with a drink once a week, and (if you believe the legend) quietly prosperous.</p>'
 '<p><span class="price" style="font-size:1.3rem">Rs '+format(week['price'],',')+'</span>'+(('<span class="old">Rs '+format(week['regular_price'],',')+'</span>') if week.get('regular_price','') and week['regular_price']>week['price'] else '')+'</p>'
 '<div style="margin-top:18px"><a class="btn-wa" href="https://wa.me/918305449559?text='+('I%27m%20interested%20in%3A%20'+week['name'].replace(' ','%20'))+'" target="_blank">Enquire on WhatsApp</a> <a class="btn" style="margin-left:10px" href="/plants/'+week['slug']+'/">Full details</a></div></div>')
TRUST=[('&#10003;','Hand-checked plants','Nothing unhealthy leaves the nursery'),('&#128172;','Real advice','We help you pick, plant and keep it alive'),('&#128666;','Same-day Indore delivery','Order by evening, green by dinner'),('&#127942;','Trusted locally','The green partner behind Indore&#8217;s venues')]
trust=''.join('<div class="t"><span class="ico">'+i+'</span><b>'+t+'</b><br><span>'+s+'</span></div>' for i,t,s in TRUST)
blog3=''.join(bcard(b) for b in B[:3])
