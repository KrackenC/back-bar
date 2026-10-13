# split_images.py SITE_DIR — website only: move every embedded drink photo
# (b64:"...") in SITE_DIR/index.html into SITE_DIR/img/d/<slug>-<hash>.jpg and
# point the entry at it (src:"img/d/..."). Safe to run repeatedly; removes
# image files nothing references any more. The artifact keeps base64.
import sys, os, re, json, base64, hashlib
site = sys.argv[1]
p = os.path.join(site, 'index.html'); s = open(p).read()
d = os.path.join(site, 'img', 'd'); os.makedirs(d, exist_ok=True)
i = s.index('var DRINK_PHOTOS'); j = s.index('\n  ];\n', i)
body = s[i:j]; n = 0
def conv(m):
    global n
    entry = m.group(0)
    names = json.loads('[' + re.search(r'"n": \[([^\]]*)\]', entry).group(1) + ']')
    raw = base64.b64decode(m.group(1))
    slug = re.sub(r'[^a-z0-9]+', '-', (names[0] if names else 'photo').lower()).strip('-') or 'photo'
    fn = '%s-%s.jpg' % (slug, hashlib.sha1(raw).hexdigest()[:8])
    open(os.path.join(d, fn), 'wb').write(raw); n += 1
    return entry.replace('b64:"%s"' % m.group(1), 'src:"img/d/%s"' % fn)
body = re.sub(r'\{"g": [^\n]*?b64:"([^"]*)"\}', lambda m: conv(m), body)
s = s[:i] + body + s[j:]
open(p, 'w').write(s)
used = set(re.findall(r'src:"img/d/([^"]+)"', s))
gone = [f for f in os.listdir(d) if f not in used]
for f in gone: os.remove(os.path.join(d, f))
print('split %d photo(s); %d files referenced; removed %d stale; index.html %d KB' % (n, len(used), len(gone), len(s)//1024))
