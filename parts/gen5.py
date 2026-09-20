import sys; sys.path.insert(0,'parts')
exec(open('parts/gen4.py').read())
stories_html=open('parts/stories_html.txt').read()
page=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Best Plant Nursery in Indore | Online Plant Nursery Indore</title><meta name="description" content="Indore Nursery — a working nursery of indoor &amp; outdoor plants, planters, gifting and event decor. Same-day delivery across Indore. Enquire on WhatsApp.">
{FONTS}<link rel="stylesheet" href="/style.css"></head><body>
{HEAD}
<section class="hero">{hero}</section>
<section><div class="container"><span class="eyebrow">The collections</span><h2 class="sec">Browse the nursery</h2><p class="sub">Six aisles of green — from shade-loving indoor picks to garden staples, planters and care essentials.</p><div class="cats">{cats}</div></div></section>
<section class="alt"><div class="container"><span class="eyebrow">Season picks</span><h2 class="sec">In season now</h2><p class="sub">What&#8217;s thriving in Indore&#8217;s weather this month.</p><div class="season-strip">{SEASONS}</div></div></section>
<section><div class="container"><span class="eyebrow">Our bestsellers</span><h2 class="sec">The plants Indore loves most</h2><p class="sub">The trendiest, most-loved greens on our benches — hover any card to enquire.</p><div class="rail">{rail}</div></div></section>
{stories_html}
<section><div class="container"><span class="eyebrow">Our portfolio</span><h2 class="sec">Green rooms, styled by us</h2><p class="sub">Hotel lobbies, wedding stages and office corners we&#8217;ve dressed in living green.</p><div class="events-grid">{evt}</div><div style="text-align:center;margin-top:30px"><a class="btn" href="/events/">See events &amp; decor</a></div></div></section>
<section style="padding-top:0"><div class="container"><div class="gift-band"><div><h2>Say it with a <em style="font-style:italic;color:var(--lime)">sapling.</em></h2><p>Plants make honest gifts — they arrive alive, they keep growing, and nobody ever returns one. Same-day across Indore.</p></div><a class="btn" href="/category/gifting-plants/">Explore gifting</a></div></div></section>
<section style="padding-top:26px"><div class="container"><div class="trust2">{trust}</div></div></section>
<section class="alt"><div class="container"><span class="eyebrow">The journal</span><h2 class="sec">Notes from the nursery</h2><p class="sub">Care guides, growing tips and plant stories — 300 of them and counting.</p><div class="blog-grid">{blog3}</div><div class="hint">&#127793; Every plant page has its own care guide — and our <a href="/blog/">blog</a> is full of helpful growing tips</div></div></section>
{FOOT}{SCRIPT}</body></html>'''
page=page.replace('{cats}',cats)
page=page.replace('{stories_html}',stories_html)
open('site/index.html','w').write(page)
print('homepage bytes:',len(page))
