import sys,os; sys.path.insert(0,'parts')
from shell import HEAD,FOOT,FONTS,SCRIPT
from urllib.parse import quote as UQ
WA='https://wa.me/918305449559'
IMG='/img/home/test.jpg'
GAL=['Reception corner','Living wall detail','Styling close-up','Atrium greens','Entry statement','Install day']
SERVICES={}
SERVICES['corporate']=dict(name='Corporate Greenery',eyebrow='For offices, hotels & workspaces',
 h1='Corporate greenery, <em>done end-to-end.</em>',
 lede='From one reception corner to a full living wall — we design, supply and set up planted spaces that make clients stop and your team feel better at work.',
 wa='Hi! We want corporate plant styling for our office in Indore.',
 kpis=[('110','+','installations delivered'),('40','+','offices & lobbies styled'),('12','','hotels & venues styled'),('98','%','clients who renew')],
 inc=[('🏢','Reception & lobby styling','Statement plants that set the tone the moment someone walks in.'),
 ('🌿','Living plant walls','Green walls sized to your wall, lit and irrigated to thrive indoors.'),
 ('🪴','Workstation & cabin plants','Desk-friendly greens in drip-free planters, delivered and placed.'),
 ('🎁','Corporate plant gifting','Branded plants and hampers for onboarding, festivals and clients.'),
 ('🎈','Festive & event styling','Seasonal and celebration plant decor for lobbies, lawns and launch days.'),
 ('🎡','Green branding','Plant-based backdrops and photo corners carrying your logo.')],
 pkgs=[('Lobby Statement','Tall statement planters, uplighting and a welcome-corner design.','From Rs 14,999','one-time install'),
 ('Living Wall','A fitted green wall, supplied and installed to your wall’s exact size.','From Rs 950','per sq.ft'),
 ('Festive Refresh','Seasonal plant swap for your lobby and workspaces — delivered and placed.','From Rs 4,999','per setup')],
 steps=[('Site visit','We measure light, space and footfall — free, anywhere in Indore.'),('Design & quote','A plant-by-plant plan with visuals and a fixed quote in 48 hours.'),('Install','Our crew installs before or after hours — zero disruption.'),('Delivery & setup','Our crew delivers and places every plant — ready before your day starts.')],
 faqs=[('Do you work after office hours?','Yes — most corporate installs happen early morning, late evening or weekends so your team is never disturbed.'),('Do you supply pots and planters too?','Yes — every setup includes planters matched to your interiors from our own pots collection.'),('Can we start with a small pilot?','Absolutely — many clients start with a reception or one floor, then expand after seeing the result.'),('Do you serve hotels and resorts?','Yes — lobbies, restaurants, banquet greens and outdoor areas, with smooth delivery and setup built for hospitality schedules.')],
 tst=[('Our lobby finally feels like a hotel. The living wall is the first thing every guest photographs.','Rohit Verma','Facilities Head'),('They handled a 3-floor install over one weekend. Delivered on schedule and set up beautifully — exactly what we needed.','Anita Deshmukh','Office Admin')],
 pk_lede='Popular starting points — every quote is custom-sized to your space.')
SERVICES['weddings']=dict(name='Wedding Stage Greenery',eyebrow='For weddings, mandaps & venues',
 h1='Wedding stages wrapped <em>in living green.</em>',
 lede='Mandap backdrops, entry archways and photo corners built from real plants — installed fresh, photographed beautifully, and cleared without a trace after your big day.',
 wa='Hi! We want plant decor for our wedding in Indore.',
 kpis=[('150','+','weddings styled'),('25','+','venues covered'),('48','hr','design to install'),('100','%','on-time setups')],
 inc=[('🌿','Mandap & stage backdrops','Lush green-floral walls that make every ritual frame-ready.'),
 ('🚪','Entry archways','Grand plant arches at the gate, with warm uplighting at dusk.'),
 ('📸','Photo corners','A green wall your guests will line up to shoot at.'),
 ('🪑','Venue dressing','Green table runners, aisle markers and hanging installs.')],
 pkgs=[('Mandap Green','Stage backdrop, side panels and entry arch — installed and removed.','From Rs 24,999','per event'),
 ('Photo Corner','An 8x8 ft living green wall with props and lighting.','From Rs 7,999','per event'),
 ('Full Venue Green','Stage, entry, dining and photo zones — one team, one look.','From Rs 49,999','per event')],
 steps=[('Share your date','Venue, timing and the look you want — we hold the slot immediately.'),('Design preview','A visual of your stage and entry before any booking amount.'),('Install day','We build before the haldi — and it holds through the reception.'),('Takedown','Next-morning removal; the venue is left spotless.')],
 faqs=[('How early should we book?','Peak-season dates go fast — 3 to 4 weeks ahead is safe, but call us for anything sooner.'),('Will the plants look fresh all day?','We pre-light and pre-hydrate everything; installs are built to look fresh through the full event.'),('Can you match our theme colours?','Yes — greens are paired with your palette through florals, fabrics and lighting.')],
 tst=[('The mandap backdrop looked straight out of a magazine. Guests kept asking who did the greenery.','Priya & Aman','Wedding, Indore'),('Zero stress — they installed overnight and left no mess for the morning function.','Meena Sharma','Wedding planner')],
 pk_lede='The three most-booked wedding packages.')
SERVICES['parties']=dict(name='Party & Celebration Installs',eyebrow='For birthdays, anniversaries & brand events',
 h1='Parties that feel <em>wildly alive.</em>',
 lede='Birthday backdrops, anniversary corners, café installations and brand activations — dramatic plant styling, set up in hours, cleared away the same night if you need.',
 wa='Hi! I want plant decor for a party in Indore.',
 kpis=[('200','+','events styled'),('6','hr','average install'),('50','+','theme setups'),('0','','post-event mess left')],
 inc=[('🎉','Birthday backdrops','A green wall with the name, balloons and shelf styling.'),
 ('🥂','Anniversary corners','Intimate table-and-greenery settings for two or twenty.'),
 ('☕','Café & restaurant installs','Permanent or seasonal plant styling that lifts every photo.'),
 ('🚀','Brand activations','Plant-built sets for launches and pop-ups, delivered on brief.')],
 pkgs=[('Party Green Wall','One feature wall styled to your theme with props and lights.','From Rs 5,999','per event'),
 ('Celebration Corner','Table and backdrop styling for home parties and cafés.','From Rs 3,499','per event'),
 ('Brand Activation Set','Custom plant-built stage and photo zone for launches.','From Rs 18,999','per event')],
 steps=[('Tell us the vibe','Theme, venue and guest count — one WhatsApp message.'),('Same-week slot','Design note and quote within 24 hours.'),('Setup in hours','We arrive, build and style — usually inside 6 hours.'),('Same-night clear','For one-day events, teardown happens the same night.')],
 faqs=[('Can you set up at home?','Yes — most party installs happen in homes, terraces and banquet halls across Indore.'),('How long does teardown take?','Under an hour for most setups; we carry everything away.'),('Do you provide props and lights?','Yes — fairy lights, name props, stands and shelving are part of the styling.')],
 tst=[('The green wall with my daughter’s name was the highlight of her birthday. Photos came out stunning.','Kavita Rao','Birthday, Indore'),('They built our café a plant corner that customers photograph daily. Best decor money we spent.','Zaid Khan','Café owner')],
 pk_lede='Most-loved celebration setups.')
SERVICES['landscaping']=dict(name='Terrace & Garden Landscaping',eyebrow='For homes, terraces & outdoors',
 h1='Outdoor spaces, <em>grown by us.</em>',
 lede='Terrace gardens, lawn styling, balcony makeovers and pathway planting — designed for Indore’s summers and monsoons, planted by our own field team.',
 wa='Hi! I want landscaping for my terrace or garden in Indore.',
 kpis=[('60','+','projects delivered'),('12','','terrace gardens built'),('300','+','plant varieties to pick from'),('100','%','plants from our nursery')],
 inc=[('🌾','Terrace gardens','Raised beds, drip lines and a vegetable-herb section that actually produces.'),
 ('🌴','Lawn & garden styling','Layered planting, borders and lighting for lawns and courtyards.'),
 ('🪟','Balcony makeovers','Compact, easy-care green balconies for apartments.'),
 ('💧','Drip irrigation','Drip lines and timers supplied and fitted so watering stays easy.')],
 pkgs=[('Balcony Makeover','20-30 plants, vertical rail planters and a care kit.','From Rs 12,999','per balcony'),
 ('Terrace Garden','Raised beds, drip irrigation, soil and seasonal planting.','From Rs 34,999','per terrace'),
 ('Seasonal Refills','New seasonal plants delivered and planted each season to keep beds fresh.','From Rs 3,999','per refill')],
 steps=[('Site measurement','Sun mapping and drainage check — we plan around Indore summers.'),('Layout plan','A planting layout with a plant list and budget before work starts.'),('Build & plant','Beds, soil, drip lines and planting by our own crew.'),('Handover','A finished, planted space — with a simple care sheet so your plants thrive.')],
 faqs=[('Will a terrace garden leak?','We install drainage mats, geotextile and proper outlets — built to keep your slab safe.'),('What survives Indore summers?','We plant hardy, heat-tested varieties from our own nursery, positioned by sun exposure.'),('Do you handle civil work?','Yes — raised beds, decking and trusted tiling partners are part of the package.')],
 tst=[('Our terrace now grows tomatoes, mint and chillies. The drip system means we travel without worry.','Suresh Patel','Villa, Indore'),('They turned a bare 300 sq.ft lawn into the best-looking garden in our lane.','Neha Joshi','Homeowner')],
 pk_lede='Starting points for every outdoor space.')

def page(s,slug):
 others=''.join('<a href="/events/'+o+'/">'+n+'</a>' for o,n in [('corporate','Corporate'),('weddings','Weddings'),('parties','Parties'),('landscaping','Landscaping')] if o!=slug)
 kpis=''.join('<div class="kpi"><b data-n="'+n+'" data-s="'+suf+'">0</b><span>'+l+'</span></div>' for n,suf,l in s['kpis'])
 inc=''.join('<div class="inc"><div class="ico">'+i+'</div><h4>'+t+'</h4><p>'+d+'</p></div>' for i,t,d in s['inc'])
 pkgs=''.join('<div class="pkg"><img loading="lazy" src="'+IMG+'" alt="'+t+'"><div class="pk-b"><span class="pk-tag">Popular</span><h4>'+t+'</h4><p>'+d+'</p><div class="pk-price">'+pr+' <small>&#183; '+sub+'</small></div><a class="btn-wa" href="'+WA+'?text='+UQ(s['wa'])+'" target="_blank">Enquire on WhatsApp</a></div></div>' for t,d,pr,sub in s['pkgs'])
 steps=''.join('<div class="step"><span class="no">'+str(n)+'</span><h4>'+t+'</h4><p>'+d+'</p></div>' for n,(t,d) in enumerate(s['steps'],1))
 gal=''.join('<figure><img loading="lazy" src="'+IMG+'" alt="'+c+'" style="object-position:'+pos+'"><figcaption>'+c+'</figcaption></figure>' for c,pos in zip(GAL,['50% 20%','20% 50%','80% 40%','50% 80%','30% 30%','70% 70%']))
 tst=''.join('<div class="tst"><div class="q">&#8220;'+q+'&#8221;</div><div class="who"><span class="av">'+n[0]+'</span><span><b>'+n+'</b><br>'+r+'</span></div></div>' for q,n,r in s['tst'])
 faqs=''.join('<details><summary>'+q+'</summary><p>'+a+'</p></details>' for q,a in s['faqs'])
 title=s['name']+' in Indore | Indore Nursery'
 return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{s['name']} by Indore Nursery — design, supply and setup across Indore. Free site visit, fixed quote, expert care. Enquire on WhatsApp.">
{FONTS}<link rel="stylesheet" href="/style.css"></head><body>
{HEAD}
<div style="background:var(--cream)"><div class="container"><nav class="crumbs"><a href="/">Home</a> / <a href="/events/">Events &amp; Decor</a> / {s['name']}</nav></div></div>
<section class="svc-hero"><div class="container svc-wrap">
<div><span class="eyebrow">{s['eyebrow']}</span><h1>{s['h1']}</h1><p class="lede">{s['lede']}</p>
<div class="svc-cta"><a class="btn-wa" href="{WA}?text={UQ(s['wa'])}" target="_blank">Get a free site visit</a><a class="btn ghost" style="color:var(--forest);border-color:var(--forest)" href="tel:+918305449559">Call +91 83054 49559</a></div></div>
<div class="svc-img"><img src="{IMG}" alt="{s['name']} by Indore Nursery"></div>
</div></section>
<section style="padding-top:0"><div class="container"><div class="svc-dash"><span class="eyebrow">By the numbers</span><div class="kpis">{kpis}</div></div></div></section>
<section class="svc-sec alt"><div class="container"><span class="eyebrow">What&#8217;s included</span><h2 class="sec">What we do</h2><div class="inc-grid">{inc}</div></div></section>
<section class="svc-sec"><div class="container"><span class="eyebrow">Packages</span><h2 class="sec">Ready when you are</h2><p class="sub" style="text-align:center;margin:0 auto 4px">{s['pk_lede']}</p><div class="pkg-grid">{pkgs}</div></div></section>
<section class="svc-sec alt"><div class="container"><span class="eyebrow">How it works</span><h2 class="sec">Four steps, zero stress</h2><div class="steps">{steps}</div></div></section>
<section class="svc-sec"><div class="container"><span class="eyebrow">Recent work</span><h2 class="sec">From our installs</h2><div class="gal">{gal}</div></div></section>
<section class="svc-sec alt"><div class="container"><span class="eyebrow">Client words</span><h2 class="sec">What hosts and managers say</h2><div class="tst-grid">{tst}</div></div></section>
<section class="svc-sec" style="padding-top:0"><div class="container"><span class="eyebrow">FAQs</span><h2 class="sec">Questions, answered</h2><div class="faq">{faqs}</div></div></section>
<section style="padding-bottom:64px"><div class="container"><div class="svc-band"><h2>Ready to green your space?</h2><p>Tell us about your site — we&#8217;ll visit, measure and quote. Free, anywhere in Indore.</p><a class="btn-wa" href="{WA}?text={UQ(s['wa'])}" target="_blank">WhatsApp us now</a><div class="svc-other"><span style="opacity:.7;font-size:.85rem;width:100%">Also explore:</span>{others}</div></div></div></section>
{FOOT}{SCRIPT}
{JS}
</body></html>'''

JS=('<script>(function(){var K=document.querySelectorAll(".kpi b");K.forEach(function(el){var n=+el.dataset.n,s=el.dataset.s||"";if(!n)return;var t0=null;'
 'function f(t){if(!t0)t0=t;var p=Math.min((t-t0)/900,1);el.textContent=Math.round(n*(p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2))+s;if(p<1)requestAnimationFrame(f)}requestAnimationFrame(f)});})();</script>')

for slug,s in SERVICES.items():
    os.makedirs('site/events/'+slug,exist_ok=True)
    open('site/events/'+slug+'/index.html','w').write(page(s,slug))
print('service pages written:',', '.join(SERVICES))
