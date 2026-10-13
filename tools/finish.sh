#!/bin/zsh
# finish.sh N "msg" 'A' 'B' 'C'  (names) — probe, bump, commit, push mirror
set -e
cd /private/tmp/claude-501/-Users-craigcorrell/b3d5a9e8-4c2f-47bf-8bdd-8855564ab06b/scratchpad
N=$1; MSG=$2; shift 2
python3 - "$N" "$@" <<'P'
import re,subprocess,sys,json
n=sys.argv[1]; want=sys.argv[2:]
s=open('back-bar-site/index.html').read()
for i,m in enumerate(re.findall(r'<script>(.*?)</script>',s,re.S)):
    open('chk_s.js','w').write(m); r=subprocess.run(['node','--check','chk_s.js'],capture_output=True,text=True)
    if r.returncode: sys.exit('syntax '+r.stderr[:300])
p='''<script>setTimeout(function(){var c=document.querySelectorAll('#grid .card');var st=document.querySelectorAll('#grid figcaption').length;var want=%s;var ok=[];c.forEach(function(k){var n=k.querySelector('h3').textContent;if(want.indexOf(n)>=0&&!k.querySelector('.stand-in'))ok.push(n)});document.body.setAttribute('data-probe',JSON.stringify({cards:c.length,exact:c.length-st,ok:ok}))},1500)</script></body>'''%json.dumps(want)
open(f'p{n}.html','w').write(s.replace('</body>',p,1))
P
perl -e 'alarm 60; exec @ARGV' "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --virtual-time-budget=4000 --dump-dom file://$PWD/p$N.html 2>/dev/null | grep -o 'data-probe="[^"]*' | sed 's/&quot;/"/g'
python3 tools/split_images.py back-bar-site
cd back-bar-site && git fetch -q && git log HEAD..origin/main --oneline
V=$(date -u +%Y-%m-%dT%H:%M:%SZ); sed -i '' "s/var CURRENT_VERSION = \"[^\"]*\"/var CURRENT_VERSION = \"$V\"/" index.html; printf '{"v": "%s"}\n' "$V" > version.json
cp ../tools/finish.sh tools/ 2>/dev/null || true
git add -A && git commit -qm "$MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git push -q && git rev-parse --short HEAD
