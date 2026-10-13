# usage: which_photo.py FILE [names...]  - shows who supplies each drink's photo (first exact match wins, as in pickDrinkPhoto)
import re,sys,json
s=open(sys.argv[1]).read(); i=s.index('var DRINK_PHOTOS'); j=s.index('\n  ];\n',i)
E=[(json.loads('['+m.group(1)+']'),m.group(2)) for m in re.finditer(r'"n": \[([^\]]*)\], "by": "([^"]*)"',s[i:j])]
names=sys.argv[2:]
if not names:
    k=s.index('var RECIPES'); names=[n.replace("\\'","'") for q,n in re.findall(r"\{\s*name:\s*(['\"])((?:\\.|(?!\1).)*)\1",s[k:])]
src={}
for n in names: src[n]=next((by for ns,by in E if n in ns),None)
from collections import Counter
print(Counter(src.values()))
if len(sys.argv)>2: print(src)
