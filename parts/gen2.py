CATS=[('Indoor Plants','indoor-plants'),('Outdoor Plants','outdoor-plants'),('Succulents','succulents'),('Pots','pots'),('Gifting Plants','gifting-plants'),('Soil & Fertilizer','soil-and-fertilizer')]
tiles=''
for name,slug in CATS:
    prod=next((p for p in bycat.get(name,[]) if p.get('image')),None)
    n=len(bycat.get(name,[]))
    tiles+=('<a class="tile" href="/category/'+slug+'/"><img loading="lazy" src="/'+loc(prod.get('image') if prod else None)+
            '" alt="'+H.escape(name)+'"><div class="tcap"><b>'+name+'</b><small>'+str(n)+' items &#8594;</small></div></a>')
RAIL=[];seen=set()
for name,slug in CATS+[('Creepers/Hanging','creepers-hanging'),('Seasonal Plants','seasonal-plants')]:
    for p in bycat.get(name,[]):
        if p.get('image') and p.get('price') and p['slug'] not in seen:
            RAIL.append(p);seen.add(p['slug']);break
rail=''.join(card(p) for p in RAIL[:8])
def good(f):
    m=re.search(r'-(\d+)x(\d+)\.',f)
    return (not m) or int(m.group(1))>=500
EV=[f for f in sorted(glob.glob('site/images/2022_05_013A*.jpg')) if good(f)][:6]
caps=['Corporate Greenery','Wedding Decor','Party Installations','Landscaping','Nursery Rows','Stage Styling']
evt=''.join('<a class="event" href="/events/"><img loading="lazy" src="/'+f[5:]+'" alt="Events and decor"><div class="cap">'+c+'</div></a>' for f,c in zip(EV,caps))
S1=('<span class="kicker">Indore&#8217;s Premium Plant Nursery</span><h1>Bring Nature Home.<br><em>Live Better.</em></h1>'
 '<p>Hand-nurtured plants, designer planters and complete garden care &#8212; hand-checked by our experts and delivered to your doorstep across Indore.</p>'
 '<a class="btn" href="/plants/">Explore Plants</a><a class="btn ghost" href="https://wa.me/918305449559?text=Hi%20Indore%20Nursery!" target="_blank">WhatsApp Us</a>'
 '<div class="chips"><span class="chip">&#127793; Grown at our nursery</span><span class="chip">&#128666; Free delivery in Indore</span><span class="chip">&#127881; Events &amp; decor studio</span></div>')
S2=('<span class="kicker">Corporate &#183; Weddings &#183; Parties</span><h1>Green Events, <em>Beautifully Styled.</em></h1>'
 '<p>From hotel lobbies to wedding stages &#8212; our events team designs, installs and maintains living decor across Indore.</p>'
 '<a class="btn" href="/events/">View Events &amp; Decor</a>')
S3=('<span class="kicker">Plant Gifting</span><h1>Give a Gift <em>That Grows.</em></h1>'
 '<p>Curated green gifting for every occasion &#8212; elegantly potted, personally messaged and delivered the same day in Indore.</p>'
 '<a class="btn" href="/category/gifting-plants/">Explore Gifting</a>')
hero=''.join('<div class="slide" style="background-image:url(/'+f[5:]+')"><div class="inner">'+s+'</div></div>' for f,s in zip(EV[:3],[S1,S2,S3]))
