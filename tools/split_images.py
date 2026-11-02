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
# A renamed drink keeps its photo bytes, so its file still carries the old
# name; rename any file whose slug no longer matches the entry's first name.
def reslug(m):
    entry, old = m.group(0), m.group(1)
    names = json.loads('[' + re.search(r'"n": \[([^\]]*)\]', entry).group(1) + ']')
    slug = re.sub(r'[^a-z0-9]+', '-', (names[0] if names else 'photo').lower()).strip('-') or 'photo'
    h = re.search(r'-([0-9a-f]{8})\.jpg$', old)
    new = '%s-%s.jpg' % (slug, h.group(1) if h else hashlib.sha1(open(os.path.join(d, old), 'rb').read()).hexdigest()[:8])
    if new != old:
        os.replace(os.path.join(d, old), os.path.join(d, new)); renamed.append(new)
    return entry.replace('src:"img/d/%s"' % old, 'src:"img/d/%s"' % new)
renamed = []
body = re.sub(r'\{"g": [^\n]*?src:"img/d/([^"]*)"\}', reslug, body)
s = s[:i] + body + s[j:]
open(p, 'w').write(s)
used = set(re.findall(r'src:"img/d/([^"]+)"', s))
gone = [f for f in os.listdir(d) if f not in used]
for f in gone: os.remove(os.path.join(d, f))
print('split %d photo(s); renamed %d; %d files referenced; removed %d stale; index.html %d KB' % (n, len(renamed), len(used), len(gone), len(s)//1024))
