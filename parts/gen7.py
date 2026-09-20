import sys,os,json; sys.path.insert(0,'parts')
exec(open('parts/gen1.py').read())
from shell import HEAD,FOOT,FONTS,SCRIPT
C=json.load(open('data/catalog.json')); byslug={p['slug']:p for p in C}
S=json.load(open('data/seasons.json'))
def card(p):
    return f"""<a class="card" href="/plants/{p['slug']}/"><img loading="lazy" src="/{loc(p.get('image'))}" alt="{esc(p['name'])}">
<div class="body"><h3>{esc(p['name'])}</h3>
<p><span class="price">{money(p.get('price'))}</span> {('<span class="old">'+money(p['regular_price'])+'</span>') if p.get('regular_price') and p['regular_price']!=p.get('price') else ''}</p></div></a>"""
SEASON_META={
 'summer':('Summer Plants','Heat-loving blooms &amp; growers','Built for Indore&#8217;s fierce summer sun — flowers that open daily, greens that shrug off 42&#176;C, and seeds to sow now for a monsoon harvest.'),
 'monsoon':('Monsoon Plants','Best time to plant','The rains are planting season in Indore. Vines, climbers and monsoon bloomers take root fastest now.'),
 'winter':('Winter Plants','Cool-season flowers','Indore winters are short and gentle — exactly what these cool-season flowers and winter vegetables are waiting for.'),
 'year':('Year-Round Plants','Evergreen favourites','No season needed — these evergreens, succulents and indoor classics thrive in Indore homes all twelve months.')}
def esc(t): return H.escape(t)
pages=[]
for key,(title,sub,desc) in SEASON_META.items():
    items=[byslug[s] for s in S if key in S[s]]
    items.sort(key=lambda p: p['name'])
    pages.append((key,title,sub,desc,items))
for key,title,sub,desc,items in pages:
    grid=''.join(card(p) for p in items)
    url=f'season/{key}/index.html'
    html=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} in Indore | Indore Nursery</title><meta name="description" content="{esc(title)} at Indore Nursery — {len(items)} picks that thrive in Indore&#8217;s {key} weather. Same-day delivery in Indore; enquire on WhatsApp.">
{FONTS}<link rel="stylesheet" href="/style.css"></head><body>
{HEAD}
<div class="container"><nav class="crumbs">Home / <a href="/">Seasons</a> / {title}</nav>
<section class="season-hero {key}"><h1>{title}</h1><p class="sub">{desc}</p>
<div class="season-tabs">'''+''.join(f'<a class="{"active" if k==key else ""}" href="/season/{k}/">{SEASON_META[k][0].split()[0]}</a>' for k in SEASON_META)+f'''</div></section>
<section><div class="grid">{grid}</div></section>
<section class="alt"><div class="container"><p>Not sure what suits your space right now? Message us on WhatsApp — we&#8217;ll pick for your balcony, terrace or garden. <a class="btn-wa" href="https://wa.me/918305449559?text=Hi%20Indore%20Nursery!%20What%20plants%20are%20best%20this%20season%3F" target="_blank">Ask on WhatsApp</a></p></div></section>
{FOOT}{SCRIPT}</body></html>'''
    os.makedirs(os.path.join('site','season',key),exist_ok=True)
    open(os.path.join('site','season',key,'index.html'),'w').write(html)
    print('wrote',url,len(items),'items')
