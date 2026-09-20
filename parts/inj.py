import sys,glob,re,os
sys.path.insert(0,'parts')
from shell import HEAD,FOOT,FONTS,SCRIPT
files=[f for f in glob.glob('site/**/*.html',recursive=True) if not f.endswith('site/index.html') or f=='site/index.html']
files=[f for f in files if f!='site/index.html']
n=0;nf=[]
for f in files:
    s=open(f,encoding='utf-8').read();orig=s
    s=re.sub(r'<div class="announce">.*?</header>', lambda m:HEAD, s, flags=re.S)
    s=re.sub(r'<footer>.*?</footer>', lambda m:FOOT, s, flags=re.S)
    if '<meta name="viewport"' in s:
        s=re.sub(r'(<meta name="viewport"[^>]*>)', lambda m:m.group(1)+'\n'+FONTS, s, count=1)
    elif '</head>' in s:
        s=s.replace('</head>',FONTS+'</head>',1)
    if '</body>' in s and '/main.js' not in s:
        s=s.replace('</body>',SCRIPT+'</body>',1)
    if s!=orig: open(f,'w',encoding='utf-8').write(s);n+=1
    else: nf.append(f)
print('updated:',n,'unchanged:',len(nf),nf[:5])
