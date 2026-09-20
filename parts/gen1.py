import json,glob,re,html as H
C=json.load(open('data/catalog.json'))
B=json.load(open('data/blogs.json'))
FALLBACK='images/2022_03_ALOCASIA-BLACK.jpg'
def loc(u):
    if not u: return FALLBACK
    m=re.search(r'wp-content/uploads/(.+)$',u)
    return 'images/'+m.group(1).replace('/','_') if m else FALLBACK
bycat={}
for p in C:
    for c in p['categories']: bycat.setdefault(c,[]).append(p)
def money(v): return format(v,',')
def card(p):
    pr=''
    if p.get('price'): pr='<span class="price">Rs '+money(p['price'])+'</span>'
    if p.get('regular_price') and p.get('price') and p['regular_price']>p['price']:
        pr+='<span class="old">Rs '+money(p['regular_price'])+'</span>'
    return ('<a class="card" href="/plants/'+p['slug']+'/"><img loading="lazy" src="/'+loc(p.get('image'))+
            '" alt="'+H.escape(H.unescape(p['name']))+'"><div class="body"><h3>'+H.escape(H.unescape(p['name']))+
            '</h3><p>'+pr+'</p></div><span class="wa-mini">Enquire &#8599;</span></a>')
def bimg(b):
    m=re.search(r'wp-content/uploads/[^"\')\s]+',b.get('content','') or '')
    return loc(m.group(0)) if m else FALLBACK
B.sort(key=lambda b:b.get('date',''),reverse=True)
def bcard(b):
    return ('<a class="blog-card" href="/blog/'+b['slug']+'/"><img loading="lazy" src="/'+bimg(b)+
            '" alt=""><div class="body"><p class="date">'+b['date'][:10]+'</p><h3>'+H.escape(H.unescape(b['title']))+'</h3></div></a>')
