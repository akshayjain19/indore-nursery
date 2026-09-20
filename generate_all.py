import json, re, os
catalog=json.load(open('data/catalog.json'))
FACTS=json.load(open('data/facts.json'))
blogs=json.load(open('data/blogs.json'))
S='site'
WA='918305449559'
def img(u):
    return 'images/'+u.split('/wp-content/uploads/')[1].replace('/','_') if u else ''
def esc(s):
    return (s or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')
def slugify(s):
    s=(s or '').lower().replace('&','and').replace("'",'')
    return re.sub(r'-+','-',re.sub(r'[^a-z0-9]+','-',s)).strip('-')
def wa(name):
    return f"https://wa.me/{WA}?text=" + __import__('urllib.parse',fromlist=['quote']).quote("Hi Indore Nursery! I'm interested in: "+name)
byCat=lambda c:[p for p in catalog if c in p["categories"]]
cats=sorted({c for p in catalog for c in p['categories'] if c})
def fmt(n):
    return ('Rs '+format(int(n),',d')) if n else 'On Request'
def header(title,desc,canon=''):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="/style.css"></head><body>
<div class="announce"><div class="an-track"><span class="an-pill">🌱 <b>Free delivery</b> above Rs 599</span><span class="an-pill">🚚 <b>Delivery anywhere</b> in Indore</span><span class="an-pill">🌱 <b>5 plants</b> at Rs 1,399</span><span class="an-pill">📞 <a href="tel:+918305449559">+91 83054 49559</a></span><span class="an-pill">🎉 <b>Events &amp; decor</b> styling</span><span class="an-pill">🌱 <b>Free delivery</b> above Rs 599</span><span class="an-pill">🚚 <b>Delivery anywhere</b> in Indore</span><span class="an-pill">🌱 <b>5 plants</b> at Rs 1,399</span><span class="an-pill">📞 <a href="tel:+918305449559">+91 83054 49559</a></span><span class="an-pill">🎉 <b>Events &amp; decor</b> styling</span></div></div>
<header><div class="container hd"><a class="logo" href="/">Indore<span>Nursery</span></a>
<nav class="main"><a href="/plants/">Plants</a><a href="/category/indoor-plants/">Indoor</a><a href="/category/outdoor-plants/">Outdoor</a><a href="/category/succulents/">Succulents</a><a href="/category/pots/">Pots</a><a href="/category/soil-and-fertilizer/">Soil &amp; Fertilizer</a><a href="/category/gifting-plants/">Gifting</a><a href="/events/">Events &amp; Decor</a><a href="/blog/">Blog</a></nav></div></header>
<a class="wa-float" href="https://wa.me/{WA}?text=Hi%20Indore%20Nursery!" target="_blank" aria-label="Chat on WhatsApp">🟢</a>
<script src="/suggester.js" defer></script>
"""
FOOTER="""
<footer><div class="container">
<div class="cols">
<div><h4>Indore Nursery</h4><p>Best plant nursery in Indore. Quality plants, planters and garden supplies with expert guidance.</p></div>
<div><h4>Shop</h4>%s</div>
<div><h4>Company</h4><a href="/about/">About Us</a><br><a href="/events/">Events &amp; Decor</a><br><a href="/blog/">Blog</a><br><a href="/contact/">Contact</a></div>
<div><h4>Contact</h4><p>+91 83054 49559<br>Indore, Madhya Pradesh<br>Open all days</p></div>
</div>
<div class="copy">© 2026 Indore Nursery · All rights reserved</div>
</div></footer></body></html>"""
CAT_LINKS=''.join(f'<a href="/category/{slugify(c)}/">{esc(c)}</a><br>' for c in cats)
FOOTER=FOOTER % CAT_LINKS
def card(p):
    return f"""<a class="card" href="/plants/{p['slug']}/"><img loading="lazy" src="/{img(p.get('image'))}" alt="{esc(p['name'])}">
<div class="body"><h3>{esc(p['name'])}</h3>
<p><span class="price">{fmt(p.get('price'))}</span> {('<span class="old">'+fmt(p['regular_price'])+'</span>') if p.get('regular_price') and p['regular_price']!=p.get('price') else ''}</p></div></a>"""
def write(path,html):
    full=os.path.join(S,path)
    os.makedirs(os.path.dirname(full),exist_ok=True)
    open(full,'w').write(html)
CLIENTS=['PRIDE Hotels &amp; Resorts','Srijan','SAJDHAJ Marriage Decorator','Loshmi Sweets - Taste of Rajasthan','KA Kashiwal Honda']
EVENTS=[('Corporate Greenery','Office plantscapes and green walls'),('Wedding Decor','Stage and venue plant styling'),('Party &amp; Events','Temporary installations for functions'),('Landscape Projects','Gardens delivered end-to-end')]
# ---------- HOME ----------
def home():
    featured=catalog[:8]
    cards=''.join(card(p) for p in featured)
    seasons=f"""
<section class="hero"><h1>Bring Nature Home</h1><p>The best plant nursery in Indore — plants, planters &amp; garden care delivered to your door.</p>
<a class="btn" href="/plants/">Shop Plants</a></section>
<div class="container"><section><h2 class="sec">Shop by Season</h2><p class="sub">Plants that thrive in this season, picked for Indore's climate</p>
<div class="season-grid">
<a class="season summer" href="/season/summer/">Summer<small>Heat-loving blooms</small></a>
<a class="season monsoon" href="/season/monsoon/">Monsoon<small>Best time to plant</small></a>
<a class="season winter" href="/season/winter/">Winter<small>Cool-season flowers</small></a>
<a class="season year" href="/season/year/">Year-Round<small>Evergreen favourites</small></a>
</div></section>
<section><h2 class="sec">Our Premium Picks</h2><p class="sub">Hand-picked bestsellers from our nursery</p>
<div class="grid">{''.join(card(p) for p in catalog[80:88])}</div>
<div class="hint">🌿 Every plant page has its own care guide — and our <a href="/blog/" style="color:var(--green2);font-weight:600">blog</a> is full of helpful growing tips</div></section>
<section style="background:#fff;border-radius:14px"><h2 class="sec">Our Valued Clients</h2><p class="sub">Trusted by leading names across Indore</p>
<div class="strip"><b style="font-size:1.1rem;color:#7c6f56">PRIDE Hotels</b><b style="font-size:1.1rem;color:#c9622b">सृजन</b><b style="font-size:1.1rem;color:#d16ba5">SAJDHAJ</b><b style="font-size:1.1rem;color:#8d6e3f">लक्ष्मी Sweets</b><b style="font-size:1.1rem;color:#cc0000">Kashiwal Honda</b></div></section>
<section><h2 class="sec">Events &amp; Decor</h2><p class="sub">Corporate · Weddings · Parties · Landscaping</p>
<div class="event-grid">{''.join(f'<a class="event" href="/events/"><img loading="lazy" src="/images/2022_05_013A15{i}.jpg" alt="{t}"><div class="cap">{t}</div></a>' for i,t in [(19,'Corporate Greenery'),(25,'Wedding Decor'),(30,'Party Installations'),(49,'Landscaping')])}</div></section>
<section><h2 class="sec">From Our Blog</h2><p class="sub">Growing guides, plant care and green living</p>
<div class="blog-grid">{blogcards()}</div></section></div>"""
    return header('Best Plant Nursery in Indore | Online Plant Nursery Indore','Indore Nursery — shop indoor plants, outdoor plants, succulents, pots and garden care in Indore. Free shipping in Indore. Enquire on WhatsApp.')+seasons+FOOTER
def blogcards(n=3):
    out=[]
    for b in blogs[:n]:
        m=re.search(r'<img[^>]+src="([^"]+)"',b['content'])
        thumb='/'+img(m.group(1)) if m else '/images/2022_03_ALOCASIA-BLACK.jpg'
        d=b['date'][:10]
        blogcards_i=f"""<a class="blog-card" href="/blog/{b['slug']}/"><img loading="lazy" src="{thumb}" alt="{esc(b['title'])}">
<div class="body"><p class="date">{d}</p><h3>{esc(b['title'])}</h3></div></a>"""
        globals().setdefault('_bc',[]).append(blogcards_i)
    s=''.join(globals()['_bc']); globals()['_bc']=[]
    return s
# ---------- PLANT PAGE ----------
GUIDE_TPL={'uses':'Perfect for homes, offices and gifting — adds greenery and freshness to any space.',
'grow':'Water when the top soil feels dry. Place in bright, indirect light for best growth.',
'benefits':'Improves air quality, reduces stress and brings nature indoors.',
'season':'Grows year-round in Indore\'s climate; best planted in mild weather.'}
def plantpage(p):
    g=p.get('description') or p.get('short_description') or ''
    g=re.sub(r'<[^>]+>',' ',g); g=re.sub(r'\s+',' ',g).strip()
    cats_html=' · '.join(f'<a href="/category/{slugify(c)}/">{esc(c)}</a>' for c in p['categories'])
    return header(p['name']+' | Indore Nursery', (p.get('short_description') or 'Buy '+p['name']+' in Indore from Indore Nursery.')[:155],)+f"""
<div class="container listing-hd"><p class="crumbs"><a href="/">Home</a> / <a href="/plants/">Plants</a> / {esc(p['name'])}</p>
<div class="pd"><img class="main" src="/{img(p.get('image'))}" alt="{esc(p['name'])}">
<div><h1>{esc(p['name'])}</h1>
<p class="price">{fmt(p.get('price'))} {('<span class="old">'+fmt(p['regular_price'])+'</span>') if p.get('regular_price') and p['regular_price']!=p.get('price') else ''}</p>
<p style="margin-top:14px">{esc(g[:400])}</p>
<a class="btn btn-wa" href="{wa(p['name'])}" target="_blank">Enquire on WhatsApp</a>
<p style="margin-top:12px;font-size:.85rem;color:#5c6b5d">📞 Or call +91 83054 49559 · Free delivery in Indore</p></div></div>
<div class="funfact"><span class="ff-tag">✨ Did you know?</span><p>{esc(FACTS.get(p['slug'],''))}</p></div></div>""" + FOOTER
# ---------- CATEGORY ----------
def catpage(c):
    ps=byCat(c)
    return header(c+' in Indore | Indore Nursery','Buy '+c+' online in Indore from Indore Nursery — quality plants with free local delivery.')+f"""
<div class="container listing-hd"><h1>{esc(c)}</h1><p class="sub" style="text-align:left;margin:6px 0 24px">Enquire on WhatsApp for bulk orders</p>
<div class="grid">{''.join(card(p) for p in ps)}</div></div>""" + FOOTER
NON_PLANT={'Pots',"Stone's",'Soil & Fertilizer'}
plants_only=[p for p in catalog if not set(p['categories']) <= NON_PLANT]
def plants_index():
    return header('All Plants | Indore Nursery','Browse all plants grown at Indore Nursery — indoor, outdoor, succulents, creepers and more, with free delivery in Indore.')+f"""
<div class="container listing-hd"><h1>All Plants</h1><p class="sub" style="text-align:left;margin:6px 0 24px">Free delivery in Indore &middot; Enquire on WhatsApp</p>
<div class="grid">{''.join(card(p) for p in plants_only)}</div></div>""" + FOOTER
# ---------- BLOG ----------
def blog_index():
    items=[]
    for b in sorted(blogs,key=lambda x:x['date'],reverse=True):
        items.append(f"""<a class="blog-card" href="/blog/{b['slug']}/"><div class="body"><p class="date">{b['date'][:10]}</p><h3>{esc(b['title'])}</h3></div></a>""")
    return header('Plant Care Blog | Indore Nursery','Plant care guides, growing tips and green living articles by Indore Nursery.')+f"""
<div class="container listing-hd"><h1>Blog</h1><p class="sub" style="text-align:left;margin:6px 0 24px">{len(blogs)} articles on plants, gardens and nature</p>
<div class="blog-grid">{''.join(items)}</div></div>""" + FOOTER
def blogpage(b):
    c=b['content']
    # localize images
    c=re.sub(r'https://indorenursery\.com/wp-content/uploads/([^"\s\)\?]+)', lambda m:'/images/'+re.sub(r'-\d+x\d+(?=\.[a-zA-Z]+$)','',m.group(1)).replace('/','_'), c)
    return header(b['title']+' | Indore Nursery Blog',b['title'])+f"""
<div class="container listing-hd" style="max-width:860px"><p class="crumbs"><a href="/">Home</a> / <a href="/blog/">Blog</a></p>
<h1>{esc(b['title'])}</h1><p class="date" style="color:#8a9a8b;margin:8px 0 26px">{b['date'][:10]} · Indore Nursery Team</p>
<div class="guide" style="margin-top:0">{c}</div></div>""" + FOOTER
# ---------- STATIC PAGES ----------
def events_page():
    ev=''.join(f'<a class="event" href="https://wa.me/{WA}?text=Hi!%20I%20want%20a%20quote%20for%20event%20plant%20decor" target="_blank"><img loading="lazy" src="/images/2022_05_013A15{i}.jpg" alt="{t}"><div class="cap">{t}</div></a>' for i,t in [(19,'Corporate Greenery'),(25,'Wedding Decor'),(30,'Party Installations'),(49,'Landscaping')]) 
    return header('Corporate, Wedding & Event Plant Decor | Indore Nursery','Plant decor for corporate events, weddings, parties and landscaping in Indore. Get a quote on WhatsApp.')+f"""
<div class="container listing-hd"><h1>Events &amp; Decor</h1>
<p class="sub" style="text-align:left">We supply and style plants for corporate offices, weddings, parties, exhibitions and full landscaping projects. Trusted by PRIDE Hotels, Sajdhaj Marriage Decorator, Srijan, Laxmi Sweets and Kashiwal Honda.</p>
<div class="event-grid">{ev}</div>
<div style="text-align:center;margin-top:36px"><a class="btn btn-wa" href="https://wa.me/{WA}?text=Hi!%20I%20want%20a%20quote%20for%20event%20plant%20decor" target="_blank">Get a Quote on WhatsApp</a></div></div>""" + FOOTER
def simple_page(title,body):
    return header(title,title)+f'<div class="container listing-hd">{body}</div>'+FOOTER
# ---------- ROBOTS + SITEMAP ----------
def robots():
    return "User-agent: *\nAllow: /\nSitemap: /sitemap.xml"
def sitemap():
    urls=['/','/plants/','/blog/','/events/','/about/','/contact/']+['/events/corporate/','/events/weddings/','/events/parties/','/events/landscaping/']+[f'/plants/{p["slug"]}/' for p in catalog]+[f'/blog/{b["slug"]}/' for b in blogs]+[f'/category/{slugify(c)}/' for c in cats]
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://indorenursery.com{u}</loc></url>' for u in urls)+'</urlset>'
# ---------- RUN ----------
write('index.html',home())
write('plants/index.html',plants_index())
for p in catalog: write(f'plants/{p["slug"]}/index.html',plantpage(p))
for c in cats: write(f'category/{slugify(c)}/index.html',catpage(c))
write('blog/index.html',blog_index())
for b in blogs: write(f'blog/{b["slug"]}/index.html',blogpage(b))
write('events/index.html',events_page())
write('about/index.html',simple_page('About Us','<h1>About Indore Nursery</h1><p style="margin-top:14px">Indore Nursery is the leading plant nursery in Indore, serving homes, offices and events across Madhya Pradesh since 2018. We grow and supply quality plants, planters, soil and garden care with free delivery across Indore.</p>'))
write('contact/index.html',simple_page('Contact Us',f'<h1>Contact Us</h1><p style="margin-top:14px">📞 +91 83054 49559<br>📍 Indore, Madhya Pradesh<br>💬 <a href="https://wa.me/{WA}" target="_blank" style="color:var(--green2)">Chat on WhatsApp</a></p>'))
write('robots.txt',robots())
write('sitemap.xml',sitemap())
print('PAGES WRITTEN')
