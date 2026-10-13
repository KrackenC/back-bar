# usage: add_user.py [--replace|--takeover] FITDIR  (--takeover: detach the name from stock photos so the new photo wins) 'Name|glass|color[|fizz,foam]' x3 -- FILES...
import sys,base64,json
a=sys.argv[1:]; rep=a[0]=='--replace'; tko=a[0]=='--takeover'; a=a[1:] if (rep or tko) else a; d=a[0]; k=a.index('--'); specs=a[1:k]; files=a[k+1:]
add=''
for i,sp in enumerate(specs):
    p=sp.split('|'); n,g,c=p[:3]; fl=p[3].split(',') if len(p)>3 and p[3] else []
    b=base64.b64encode(open(f'{d}/p{i}.jpg','rb').read()).decode()
    extra=''.join(f', "{f}": 1' for f in fl)
    add+=',\n    {"g": %s, "c": %s, "n": [%s], "by": "Back Bar", "u": ""%s, b64:"%s"}'%(json.dumps(g),json.dumps(c),json.dumps(n,ensure_ascii=False),extra,b)
for f in files:
    s=open(f).read()
    import re
    global hits
    for sp in specs:
        key='"n": [%s]'%json.dumps(sp.split('|')[0],ensure_ascii=False)
        if rep:
            pat=r',\n    \{"g": "[^"]*", "c": "[^"]*", '+re.escape(key)+r'[^\n]*?b64:"[^"]*"\}'
            s,k=re.subn(pat,'',s); assert k==1,(sp,k)
        elif tko:
            nm=sp.split('|')[0]; q=json.dumps(nm,ensure_ascii=False)
            i0=s.index('var DRINK_PHOTOS'); j0=s.index('\n  ];\n',i0)
            body=s[i0:j0]; hits=0
            def fix(m):
                global hits
                names=json.loads('['+m.group(1)+']')
                if nm not in names or m.group(2)=='Back Bar': return m.group(0)
                hits+=1; names=[x for x in names if x!=nm]
                return '"n": %s, "by": "%s"'%(json.dumps(names,ensure_ascii=False),m.group(2))
            body=re.sub(r'"n": \[([^\]]*)\], "by": "([^"]*)"',fix,body)
            assert hits>=1,(nm,'no stock photo held this name')
            assert key not in body, (nm,'already has a Back Bar photo')
            s=s[:i0]+body+s[j0:]
        else: assert key not in s, sp
    i=s.index('var DRINK_PHOTOS'); j=s.index('"}\n  ];\n',i)+2
    s=s[:j]+add+s[j:]; open(f,'w').write(s); print(f,len(s)//1024,'KB')
