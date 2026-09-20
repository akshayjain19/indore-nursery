import sys; sys.path.insert(0,'parts')
exec(open('parts/gen1.py').read()); exec(open('parts/gen2.py').read())
from shell import HEAD,FOOT,FONTS,SCRIPT
SEASONS=('<a class="season summer" href="/season/summer/">Summer<small>Heat-loving blooms</small></a>'
 '<a class="season monsoon" href="/season/monsoon/">Monsoon<small>Best time to plant</small></a>'
 '<a class="season winter" href="/season/winter/">Winter<small>Cool-season flowers</small></a>'
 '<a class="season year" href="/season/year/">Year-Round<small>Evergreen favourites</small></a>')
BEN=[('&#127811;','Cleaner Air, Naturally','Indoor plants quietly freshen the air in your home and workspace &#8212; a more comfortable, healthier everyday environment.'),
('&#128522;','Calm That Grows','Greenery lowers stress. A leafy corner makes unwinding after a long Indore day feel effortless.'),
('&#128187;','Sharper Workspaces','A touch of green on the desk boosts focus, creativity and motivation all day.'),
('&#128167;','Natural Humidity','Plants release moisture into the air &#8212; fresher rooms, easier breathing.'),
('&#127807;','A Greener Planet','Every plant you bring home is a small, beautiful step toward a lighter footprint.'),
('&#128266;','Softer Spaces','Leaves absorb background noise and soften echoes &#8212; quieter, calmer rooms.')]
impact=''.join('<div class="benefit reveal"><div class="ico">'+i+'</div><h4>'+t+'</h4><p>'+p+'</p></div>' for i,t,p in BEN)
TRUST=[('&#10003;','Hand-checked plants','Only healthy, nursery-fresh stock leaves our gates'),('&#128172;','Expert guidance','Real advice on WhatsApp before and after you buy'),('&#128666;','Fast Indore delivery','Same-day doorstep delivery across the city'),('&#127942;','Trusted locally','The green partner behind Indore&#8217;s favourite venues')]
trust=''.join('<div class="t reveal"><div class="ico">'+i+'</div><b>'+t+'</b><span>'+s+'</span></div>' for i,t,s in TRUST)
blog3=''.join(bcard(b) for b in B[:3])
htmlpage=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Best Plant Nursery in Indore | Online Plant Nursery Indore</title><meta name="description" content="Indore Nursery — indoor &amp; outdoor plants, premium pots, gifting and event decor in Indore. Free delivery. Enquire on WhatsApp.">
{FONTS}<link rel="stylesheet" href="/style.css"></head><body>
{HEAD}
<section class="hero">{hero}</section>
<section><div class="container"><span class="eyebrow">Collections</span><h2 class="sec">Six Worlds, <em>One Green Home.</em></h2><p class="sub">Plants, planters, gifting and garden care — everything your space needs, in one nursery.</p><div class="tile-grid">{tiles}</div></div></section>
<section class="alt"><div class="container"><span class="eyebrow">Shop by Season</span><h2 class="sec">What Thrives <em>Right Now</em></h2><p class="sub">Plants picked for Indore&#8217;s climate, season by season.</p><div class="season-grid">{SEASONS}</div></div></section>
<section><div class="container"><span class="eyebrow">Bestsellers</span><h2 class="sec">Our Most-Loved <em>Plants &amp; Planters</em></h2><p class="sub">Hand-picked favourites from the nursery, updated every week.</p><div class="rail">{rail}</div></div></section>
<section class="impact"><div class="container"><span class="eyebrow" style="color:var(--lime)">Why Plants</span><h2 class="sec">Small Plants, <em>Big Impact.</em></h2><p class="sub">Plants do more than beautify your space — they nourish your well-being.</p><div class="impact-grid">{impact}</div></div></section>
<section><div class="container"><span class="eyebrow">Portfolio</span><h2 class="sec">Events &amp; Decor That <em>Steal the Show</em></h2><p class="sub">Corporate greenery, wedding stages, party installations and landscaping — styled by our team.</p><div class="event-grid">{evt}</div><div style="text-align:center;margin-top:34px"><a class="btn" href="/events/">See Our Events Portfolio</a></div></div></section>
<section class="alt"><div class="container"><div class="gifting"><div><span class="eyebrow" style="text-align:left;color:var(--lime)">Green Gifting</span><h2>Gift Green. <em>Grow Connections.</em></h2><p>Thoughtful plant gifts that inspire, appreciate and leave a lasting impact — for clients, employees and loved ones.</p><a class="btn" href="/category/gifting-plants/">Gift Green</a></div><ul class="pts"><li>&#127793; Premium plants, beautifully packaged</li><li>&#9997;&#65039; Personal messages &amp; bulk options</li><li>&#128666; Same-day delivery in Indore</li><li>&#127873; Perfect for every occasion</li></ul></div></div></section>
<section><div class="container"><div class="trust">{trust}</div></div></section>
<section class="alt"><div class="container"><span class="eyebrow">From the Blog</span><h2 class="sec">Growing Guides &amp; <em>Plant Care</em></h2><p class="sub">300+ articles written by plant people, for plant people.</p><div class="blog-grid">{blog3}</div><div class="hint">&#127793; Every plant page has its own care guide — and our <a href="/blog/">blog</a> is full of helpful growing tips</div></div></section>
{FOOT}{SCRIPT}</body></html>'''
open('site/index.html','w').write(htmlpage)
print('homepage bytes:',len(htmlpage))
