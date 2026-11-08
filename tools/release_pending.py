#!/usr/bin/env python3
"""Release collected drinks from pending/drinks.json into the app.

usage: release_pending.py [--date YYYY-MM-DD] [--status holiday] [--dry-run] PENDING_JSON APP.html [APP2.html ...]

Every drink with status "collected" is appended to RECIPES (under one
"// ---------- Release YYYY-MM-DD ----------" header) with added:'<date>', so
the app's "Just added" filter shows the batch. New ingredients listed in
newIngredients are appended to INGREDIENTS (or BRAND_INGREDIENTS when they
have substitutesFor) if not already present. The footer recipe count is
updated. Then the JSON is rewritten with status "released" and the date.
At most 10 drinks are released per calendar month (counted from "released"
dates); extra drinks stay queued, oldest first, for the next month. Drinks
with a future "holdUntil" are skipped unless --early is passed.
With --status holiday the held Holiday collection is released instead: those
recipes get holiday:'christmas' or 'newyear' (from "occasion") and no added:
date, so they show under the seasonal Holidays chip and not under Just added.
With --status dryjan the Dry January module is released: recipes get
dryJan:<day> (1-31) and no added: date, sorted by day; drinks already in the
app listed in "dryJanuaryExisting" {name: day} get dryJan:<day> added in place.
Pass both copies (the artifact source and the mirror's index.html) so they
stay identical.
House style (applied on every release): items are re-sorted into Back Bar's
own order — spirits, liqueurs and fortified wine, juices and mixers, syrups,
bitters, then toppers ("top"), then optional extras — and each released
drink's "source" is deleted from the JSON so the public holding list keeps
no trail back to where the recipe was checked.
"""
import json, re, sys, datetime

args = sys.argv[1:]
date = datetime.date.today().isoformat()
dry = False
if '--date' in args:
    i = args.index('--date'); date = args[i + 1]; del args[i:i + 2]
status = 'collected'
if '--status' in args:
    i = args.index('--status'); status = args[i + 1]; del args[i:i + 2]
if '--dry-run' in args:
    args.remove('--dry-run'); dry = True
early = '--early' in args   # release drinks whose holdUntil is still in the future
if early:
    args.remove('--early')
if len(args) < 2:
    sys.exit(__doc__)
pending_path, apps = args[0], args[1:]
data = json.load(open(pending_path))
MONTHLY_CAP = 10   # user rule 2026-11-08: at most 10 drinks reach the app per month
cand = [d for d in data['drinks'] if d.get('status') == status]
today = datetime.date.today().isoformat()
held = [d for d in cand if d.get('holdUntil', '') > today]
if held and not early:
    print('held (holdUntil): ' + ', '.join(d['name'] + ' until ' + d['holdUntil'] for d in held))
    cand = [d for d in cand if d not in held]
month = date[:7]
already = sum(1 for d in data['drinks'] if d.get('status') == 'released' and str(d.get('released', '')).startswith(month))
room = max(0, MONTHLY_CAP - already)
# oldest first: by collected date, then queue order
order = sorted(range(len(cand)), key=lambda i: (cand[i].get('collected', ''), i))
batch = [cand[i] for i in order[:room]]
waiting = [cand[i] for i in order[room:]]
if waiting:
    print(f'monthly cap {MONTHLY_CAP}: {already} already released in {month}; holding for next month: ' + ', '.join(d['name'] for d in waiting))
if not batch:
    sys.exit('nothing to release with status ' + status + (' this month (cap reached)' if cand and not room else ''))
HOLIDAY = status == 'holiday'
DRYJAN = status == 'dryjan'
if DRYJAN:
    batch.sort(key=lambda d: d['day'])


def js(v):
    """A JS string literal in the file's own style: single quotes, or double
    quotes when the text has an apostrophe."""
    v = str(v)
    if "'" in v and '"' not in v:
        return '"' + v + '"'
    return "'" + v.replace('\\', '\\\\').replace("'", "\\'") + "'"


def recipe_js(d):
    items = ','.join('{id:' + js(it['id']) + ', amt:' + js(it['amt']) +
                     (', familyOk:true' if it.get('familyOk') else '') +
                     (', optional:true' if it.get('optional') else '') + '}' for it in d['items'])
    return ('    {name:' + js(d['name']) + ', base:' + js(d['base']) + ', glass:' + js(d['glass']) +
            ', method:' + js(d['method']) +
            (", holiday:'" + ('christmas' if d.get('occasion') == 'Christmas' else 'newyear') + "'" if HOLIDAY else ', dryJan:%d' % d['day'] if DRYJAN else ", added:'" + date + "'") + ',\n'
            '      items:[' + items + '],\n'
            '      garnish:' + js(d.get('garnish') or '—') + ', note:' + js(d.get('note', '')) + '}')


ORDER = ['Spirits', 'Liqueurs & Fortified Wine', 'Juice & Mixers', 'Syrups', 'Bitters']


def house_order(items, groups):
    def key(it):
        g = groups.get(it['id'], 'Juice & Mixers')
        return (bool(it.get('optional')), 'top' in it['amt'].lower(), ORDER.index(g) if g in ORDER else 2)
    return sorted(items, key=key)  # stable, so ties keep their order


def ing_js(g):
    keys = ['id', 'name', 'category', 'group'] + [k for k in ('family', 'substitutesFor') if g.get(k)]
    return '    {' + ', '.join(k + ':' + js(g[k]) for k in keys) + '}'


def close_array(s, var):
    """Index of the '\n  ];' that closes `var NAME = [`."""
    start = s.index('var ' + var + ' = [')
    return s.index('\n  ];', start)


for path in apps:
    s = open(path).read()
    names = {(a or b).lower() for a, b in re.findall(r"\{name:\s*(?:'((?:[^'\\]|\\.)*)'|\"([^\"]*)\")", s)}
    for d in batch:
        if d['name'].lower() in names:
            sys.exit(f'{path}: {d["name"]} is already in RECIPES')
    known = set(re.findall(r"\{id:\s*'([^']+)'", s))
    groups = dict(re.findall(r"\{id:\s*'([^']+)'[^}]*?group:\s*'([^']+)'", s))
    groups.update({g['id']: g['group'] for g in data.get('newIngredients', [])})
    for d in batch:
        d['items'] = house_order(d['items'], groups)
    for d in batch:
        for it in d['items']:
            if it['id'] not in known and it['id'] not in {g['id'] for g in data.get('newIngredients', [])}:
                sys.exit(f'{path}: {d["name"]} uses unknown ingredient {it["id"]}')
    for g in data.get('newIngredients', []):
        if g['id'] in known:
            continue
        var = 'BRAND_INGREDIENTS' if g.get('substitutesFor') else 'INGREDIENTS'
        at = close_array(s, var)
        s = s[:at] + ',\n' + ing_js(g) + s[at:]
    if DRYJAN:
        for name, day in data.get('dryJanuaryExisting', {}).items():
            m = re.search(r"\{name:\s*(?:'%s'|\"%s\")[^\n]*?method:'[^']*'" % (re.escape(name.replace("'", "\\'")), re.escape(name)), s)
            if not m:
                sys.exit(f'{path}: existing Dry January drink {name} not found')
            if 'dryJan:' not in m.group(0):
                s = s[:m.end()] + ', dryJan:%d' % day + s[m.end():]
    at = close_array(s, 'RECIPES')
    block = ',\n    // ---------- ' + ('Holiday collection, released ' if HOLIDAY else 'Dry January module, released ' if DRYJAN else 'Release ') + date + ' ----------\n' + ',\n'.join(recipe_js(d) for d in batch)
    s = s[:at] + block + s[at:]
    total = len(re.findall(r"\{name:\s*['\"]", s[s.index('var RECIPES = ['):close_array(s, 'RECIPES')]))
    s, n = re.subn(r'(\. )\d+( recipes[.,])', r'\g<1>' + str(total) + r'\2', s)
    if not dry:
        open(path, 'w').write(s)
    print(f'{path}: +{len(batch)} recipes, {total} total, footer updated: {bool(n)}')

if not dry:
    for d in batch:
        d['status'] = 'released'; d['released'] = date
    for d in data['drinks']:
        if d.get('status') not in ('collected', 'holiday'):  # already in the app
            d.pop('source', None); d.pop('holdUntil', None)
    json.dump(data, open(pending_path, 'w'), indent=1, ensure_ascii=False)
print('released:', ', '.join(d['name'] for d in batch))
