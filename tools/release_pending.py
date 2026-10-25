#!/usr/bin/env python3
"""Release collected drinks from pending/drinks.json into the app.

usage: release_pending.py [--date YYYY-MM-DD] [--status holiday] [--dry-run] PENDING_JSON APP.html [APP2.html ...]

Every drink with status "collected" is appended to RECIPES (under one
"// ---------- Release YYYY-MM-DD ----------" header) with added:'<date>', so
the app's "Just added" filter shows the batch. New ingredients listed in
newIngredients are appended to INGREDIENTS (or BRAND_INGREDIENTS when they
have substitutesFor) if not already present. The footer recipe count is
updated. Then the JSON is rewritten with status "released" and the date.
With --status holiday the held Holiday collection is released instead: those
recipes get holiday:'christmas' or 'newyear' (from "occasion") and no added:
date, so they show under the seasonal Holidays chip and not under Just added.
Pass both copies (the artifact source and the mirror's index.html) so they
stay identical.
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
if len(args) < 2:
    sys.exit(__doc__)
pending_path, apps = args[0], args[1:]
data = json.load(open(pending_path))
batch = [d for d in data['drinks'] if d.get('status') == status]
if not batch:
    sys.exit('nothing with status ' + status + ' to release')
HOLIDAY = status == 'holiday'


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
            (", holiday:'" + ('christmas' if d.get('occasion') == 'Christmas' else 'newyear') + "'" if HOLIDAY else ", added:'" + date + "'") + ',\n'
            '      items:[' + items + '],\n'
            '      garnish:' + js(d.get('garnish') or '—') + ', note:' + js(d.get('note', '')) + '}')


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
    at = close_array(s, 'RECIPES')
    block = ',\n    // ---------- ' + ('Holiday collection, released ' if HOLIDAY else 'Release ') + date + ' ----------\n' + ',\n'.join(recipe_js(d) for d in batch)
    s = s[:at] + block + s[at:]
    total = len(re.findall(r"\{name:\s*['\"]", s[s.index('var RECIPES = ['):close_array(s, 'RECIPES')]))
    s, n = re.subn(r'(\. )\d+( recipes[.,])', r'\g<1>' + str(total) + r'\2', s)
    if not dry:
        open(path, 'w').write(s)
    print(f'{path}: +{len(batch)} recipes, {total} total, footer updated: {bool(n)}')

if not dry:
    for d in batch:
        d['status'] = 'released'; d['released'] = date
    json.dump(data, open(pending_path, 'w'), indent=1, ensure_ascii=False)
print('released:', ', '.join(d['name'] for d in batch))
