"""Split a 3-panel drink image into 480x300 card photos in the house style:
each glass (garnish top to foot) fills the same share of the frame, with equal
headroom above and below (FILL of the height); missing backdrop is extended
with the panel's own background colour and the seams faded.
usage: panels.py SRC OUTDIR 'x0,x1,top,bottom' x3"""
import sys, json, subprocess, re, base64, html, os
FILL=0.80
src, outdir = sys.argv[1], sys.argv[2]
panels=[]
MAXW=158   # glass width (output px of 480) that still fits the card's 9:16 window (~169px)
for spec in sys.argv[3:6]:
    v=[int(x) for x in spec.split(',')]
    x0,x1,t,b=v[:4]; gx0,gx1=(v[4],v[5]) if len(v)>5 else (x0,x1)
    fill=FILL
    if len(v)>5: fill=min(FILL, MAXW*(b-t)/(300*(gx1-gx0)))
    pad=(b-t)*(1-fill)/2/fill
    panels.append([x0,x1,round(t-pad),round(b+pad),(gx0+gx1)/2])
os.makedirs(outdir, exist_ok=True)
page='''<html><body><img id="s" src="%s"><script>
document.getElementById('s').onload=function(){
 var img=this,out=[],P=%s,W=480,H=300;
 P.forEach(function(p){
  var c=document.createElement('canvas');c.width=W;c.height=H;var g=c.getContext('2d');
  var sw=p[1]-p[0], y0=p[2], y1=p[3], sh=y1-y0, fs=H/sh, dw=sw*fs, dx=W/2-(p[4]-p[0])*fs;
  var t=document.createElement('canvas');t.width=1;t.height=1;var tg=t.getContext('2d');
  // backdrop colour: darkest of five samples along the panel's top edge (a soft
  // centre glow or a prop in a corner would otherwise give a lighter fill)
  var d=null;[.1,.3,.5,.7,.9].forEach(function(f){tg.clearRect(0,0,1,1);tg.drawImage(img,Math.round(p[0]+(p[1]-p[0])*f),4,1,1,0,0,1,1);
    var q=tg.getImageData(0,0,1,1).data; if(!d||q[0]+q[1]+q[2]<d[0]+d[1]+d[2]) d=[q[0],q[1],q[2]];});
  var rgba=function(a){return 'rgba('+d[0]+','+d[1]+','+d[2]+','+a+')';};
  g.fillStyle=rgba(1);g.fillRect(0,0,W,H);
  var cy0=Math.max(0,y0), cy1=Math.min(img.naturalHeight,y1), top=(cy0-y0)*fs, bot=(cy1-y0)*fs;
  g.drawImage(img,p[0],cy0,sw,cy1-cy0,dx,top,dw,bot-top);
  function fade(x,y,w,h,x2,y2){var G=g.createLinearGradient(x,y,x2,y2);G.addColorStop(0,rgba(1));G.addColorStop(1,rgba(0));g.fillStyle=G;g.fillRect(Math.min(x,x2)-(x2<x?0:0),Math.min(y,y2),w,h);}
  var f=26; fade(dx,0,f,H,dx+f,0); fade(dx+dw,0,f,H,dx+dw-f,0);
  if(top>0){var G=g.createLinearGradient(0,top,0,top+20);G.addColorStop(0,rgba(1));G.addColorStop(1,rgba(0));g.fillStyle=G;g.fillRect(dx,top,dw,20);}
  if(bot<H){var G2=g.createLinearGradient(0,bot,0,bot-20);G2.addColorStop(0,rgba(1));G2.addColorStop(1,rgba(0));g.fillStyle=G2;g.fillRect(dx,bot-20,dw,20);}
  out.push(c.toDataURL('image/jpeg',0.72));
 });
 document.body.setAttribute('data-out',JSON.stringify(out));
};</script></body></html>'''%(os.path.abspath(src), json.dumps(panels))
hp=os.path.join(outdir,'make.html'); open(hp,'w').write(page)
chrome="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
dom=subprocess.run(['perl','-e','alarm 60; exec @ARGV',chrome,'--headless=new','--disable-gpu','--allow-file-access-from-files','--virtual-time-budget=3000','--dump-dom','file://'+os.path.abspath(hp)],capture_output=True,text=True).stdout
out=json.loads(html.unescape(re.search(r'data-out="([^"]*)"',dom).group(1)))
for i,u in enumerate(out): open(os.path.join(outdir,f'p{i}.jpg'),'wb').write(base64.b64decode(u.split(',',1)[1]))
print(outdir, panels)
