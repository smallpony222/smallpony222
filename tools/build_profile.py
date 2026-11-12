"""Build transparent GitHub artwork with one semantic reveal per technology."""
from pathlib import Path
import html, json, math, textwrap
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'; OUT=ASSETS/'workflows'
CHAPTERS=json.loads((ROOT/'tools/chapters.json').read_text())
WORKFLOWS=json.loads((ROOT/'tools/workflows.json').read_text())
INK='#797979'; BLUE='#5976d4'; LINE='#828282'

def rgb(color):return [int(color[i:i+2],16)/255 for i in (1,3,5)]
def luminance(color):
 c=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb(color)]
 return sum(x*y for x,y in zip(c,[.2126,.7152,.0722]))
def balanced(color):
 # A bounded luminance is visible on both white and GitHub's dark canvas.
 c=rgb(color)
 for _ in range(100):
  value='#'+''.join(f'{round(v*255):02x}' for v in c)
  light=luminance(value)
  if .18<=light<=.23:return value
  c=[v*.96 if light>.23 else v+(1-v)*.035 for v in c]
 return '#797979'

def txt(x,y,value,size=20,color=INK,weight=600,extra=''):
 return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{html.escape(value)}</text>'

def icon(name,x,y,size,color):
 tree=ET.parse(ASSETS/'icons'/f'{name}.svg')
 paths=''.join('<path d="'+html.escape(p.attrib['d'],quote=True)+'"/>' for p in tree.iter() if p.tag.endswith('path'))
 return f'<g transform="translate({x} {y}) scale({size/24})" fill="{color}">{paths}</g>'

def save(name,w,h,title,desc,body):
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M1 1L7 4L1 7" fill="none" stroke="{LINE}" stroke-width="1.2"/></marker></defs>
<style>
text{{font-family:Inter,'Segoe UI',Arial,sans-serif}}
.flow{{stroke-dasharray:8 28;animation:flow 4s linear infinite}}
.stage{{animation:stage 8s ease-in-out infinite}}
.orbit{{transform-box:fill-box;transform-origin:center;animation:orbit 32s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-144}}}}
@keyframes stage{{0%,20%{{stroke-width:3}}40%,100%{{stroke-width:1.2}}}}
@keyframes orbit{{to{{transform:rotate(360deg)}}}}
@keyframes grid{{0%,100%{{transform:scaleX(1)}}50%{{transform:scaleX(.58)}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
{body}
</svg>'''
 (OUT/name).write_text(svg,encoding='utf-8')

def node(x,y,label,color,i,width=174):
 b=f'<rect x="{x-width/2}" y="{y-37}" width="{width}" height="74" rx="14" fill="none" stroke="{color}" class="stage" style="animation-delay:-{i*1.9}s"/>'
 rows=textwrap.wrap(label,17)
 for j,row in enumerate(rows):b+=txt(x,y+7+(j-(len(rows)-1)/2)*23,row,20,color=INK,extra='text-anchor="middle"')
 return b

def edge(a,b,color,feedback=False,bend=0):
 x,y=a;X,Y=b
 dx,dy=X-x,Y-y;length=math.hypot(dx,dy)
 inset=46 if abs(dy)>abs(dx) else 91
 sx=x+dx/length*inset;sy=y+dy/length*inset
 ex=X-dx/length*inset;ey=Y-dy/length*inset
 path=f'M{sx:.2f} {sy:.2f}Q{(sx+ex)/2+bend:.2f} {(sy+ey)/2+bend:.2f} {ex:.2f} {ey:.2f}'
 return f'<path d="{path}" fill="none" stroke="{LINE}" stroke-width="1.2" marker-end="url(#arrow)"/><path d="{path}" fill="none" stroke="{color}" stroke-width="2.5" class="flow"/>'

def graph(spec,color,mobile):
 kind=spec['kind'];labels=spec['nodes'];w=480 if mobile else 960
 # Different topologies model fan-out, feedback, branches, trees, and sequencing.
 seq=[(240,153+i*112) for i in range(4)] if mobile else [(144+224*i,204) for i in range(4)]
 square=[(130,163),(350,163),(350,343),(130,343)] if mobile else [(218,151),(742,151),(742,312),(218,312)]
 diamond=[(240,126),(130,267),(350,267),(240,414)] if mobile else [(126,225),(440,132),(440,318),(830,225)]
 family='sequence';points=seq;edges=[(0,1),(1,2),(2,3)]
 if kind in {'eventloop','controller','training','agent','infrastructure'}:
  points=square;edges=[(0,1),(1,2),(2,3),(3,0)];family='feedback'
  if kind in {'controller','agent','infrastructure'}:edges=[(0,1),(1,2),(2,3),(3,1)]
  if spec.get('tech')=='tensorflow':edges=[(0,1),(1,2),(2,1),(1,3)]
 if kind in {'fan','resolver','balance','cloud','containers','inventory','dag','partitions','modelhub','warehouse','evaluate'}:
  points=diamond;edges=[(0,1),(0,2),(1,3),(2,3)];family='fan-out'
 if kind in {'cache'}:
  points=square;edges=[(0,1),(1,2),(2,3),(3,1),(1,3)];family='cache'
 if kind in {'multimodal'}:
  points=[(105,145),(240,145),(375,145),(240,355)] if mobile else [(180,120),(180,235),(180,350),(720,235)]
  edges=[(0,3),(1,3),(2,3)];family='fusion'
 if kind in {'branch'}:
  points=diamond;edges=[(0,1),(1,3),(0,2),(2,3)];family='branch'
 if kind in {'lineage'}:
  points=diamond;edges=[(0,1),(1,2),(1,3),(2,3)];family='lineage'
 if kind=='tree':
  points=[(240,128),(130,250),(350,250),(75,383),(240,383),(405,383)] if mobile else [(480,115),(270,225),(690,225),(160,335),(480,335),(800,335)]
  edges=[(0,1),(0,2),(1,3),(2,4),(2,5)];family='tree'
 h=590 if mobile and family=='sequence' else (510 if mobile else 420)
 b=''
 if kind=='kernel':
  by=320 if mobile else 204
  b+=f'<path d="M24 {by}H{w-24}" stroke="{LINE}" stroke-width="1" stroke-dasharray="2 10"/>'
 if kind=='broker':
  points=diamond;edges=[(0,1),(0,2),(1,3),(2,3)];family='partition log'
 if family=='fusion':width=112 if mobile else 184
 elif kind=='tree':width=116 if mobile else 166
 else:width=174
 for a,c in edges:b+=edge(points[a],points[c],color,bend=15 if kind=='branch' and a==0 and c==2 else 0)
 for i,((x,y),label) in enumerate(zip(points,labels)):
  b+=node(x,y,label,color,i,width)
 # Technology-specific visual structures beyond a relabeled shared pipeline.
 if kind in {'query','documents'}:
  x,y=points[2]
  for i in range(3):
   b+=f'<path d="M{x-35+i*35} {y+42}v12" stroke="{color}" class="flow"/>'
 elif kind=='containers':
  x,y=points[0]
  for k in range(3):b+=f'<path d="M{x-42} {y+43+k*7}h84" stroke="{color}" stroke-width="3"/>'
 elif kind=='responsive':
  x,y=points[1]
  b+=f'<g style="transform-box:fill-box;transform-origin:center;animation:grid 5s ease-in-out infinite">'
  for k in range(4):b+=f'<rect x="{x-52+k*27}" y="{y+47}" width="22" height="18" rx="3" fill="none" stroke="{color}"/>'
  b+='</g>'
 elif kind in {'dataframe','selector'}:
  x,y=points[1]
  for row in range(3):
   for col in range(4):b+=f'<rect x="{x-46+col*24}" y="{y+43+row*9}" width="19" height="5" fill="{color}" class="stage" style="animation-delay:-{row}s"/>'
 elif kind in {'metrics','dashboard'}:
  x,y=points[2]
  b+=f'<path d="M{x-60} {y+65}l18-12 15 8 18-28 18 10 18-23 20 6" stroke="{color}" stroke-width="2" fill="none" class="flow"/>'
 elif kind=='broker':
  for j in [1,2]:
   x,y=points[j]
   for k in range(4):b+=f'<rect x="{x-43+k*23}" y="{y+43}" width="16" height="9" fill="none" stroke="{color}" class="stage" style="animation-delay:-{k}s"/>'
 elif kind in {'agent','training'}:
  x,y=points[3]
  b+=txt(x,y+73,'tool result' if kind=='agent' else 'weight update',19,color,extra='text-anchor="middle"')
 elif kind=='medallion':
  for i,medal in enumerate(['#a37955','#818b98','#b18b35']):
   x,y=points[i];b+=f'<circle cx="{x}" cy="{y+53}" r="7" fill="{balanced(medal)}"/>'
 return b,h,family

def effect(ch,name,label,color,spec,mobile):
 w=480 if mobile else 960
 color=balanced(color)
 body,h,family=graph(spec,color,mobile)
 header=icon(name,28,23,30,color)+txt(73,47,label,24,weight=700)
 # No vendor internals are claimed: these are clearly labeled conceptual workflows.
 if mobile:
  header+=txt(28,85,spec['hint'].upper(),19,color)
 else:
  header+=txt(w-28,46,spec['hint'].upper(),19,color,extra='text-anchor="end"')
 caption=textwrap.wrap(spec['concept'],41 if mobile else 85)
 for i,row in enumerate(caption):body+=txt(28,h-10+i*26,row,19,INK)
 h+=max(1,len(caption))*26+10
 save(f'{ch["n"]}-{name}{"-mobile" if mobile else ""}.svg',w,h,label+' - '+spec['concept'],spec['concept']+'. '+' -> '.join(spec['nodes'])+'. Illustrative workflow.',header+body)

def compact_effect(ch,name,label,color,spec):
 # A narrow, readable composition for a gallery cell on a phone.
 color=balanced(color);width=180;labels=spec['nodes'];count=len(labels)
 ys=[65+i*107 for i in range(count)]
 b=''
 kind=spec['kind'];links=[(i,i+1) for i in range(count-1)]
 if kind in {'agent','controller','infrastructure','training','eventloop'}:
  links=[(0,1),(1,2),(2,3),(3,1 if kind in {'agent','controller','infrastructure'} else 0)]
 if kind in {'fan','resolver','balance','cloud','containers','inventory','dag','partitions','modelhub','warehouse','evaluate','branch','broker'}:links=[(0,1),(0,2),(1,3),(2,3)]
 if kind=='cache':links=[(0,1),(1,2),(2,3),(3,1),(1,3)]
 if kind=='multimodal':links=[(0,3),(1,3),(2,3)]
 if kind=='lineage':links=[(0,1),(1,2),(1,3),(2,3)]
 if kind=='tree':links=[(0,1),(0,2),(1,3),(2,4),(2,5)]
 if spec.get('tech')=='tensorflow':links=[(0,1),(1,2),(2,1),(1,3)]
 for i,(a,z) in enumerate(links):
  if z==a+1:path=f'M86 {ys[a]+34}V{ys[z]-34}'
  elif i%2:path=f'M158 {ys[a]}H174V{ys[z]}H158'
  else:path=f'M14 {ys[a]}H5V{ys[z]}H14'
  b+=f'<path d="{path}" stroke="{LINE}" fill="none" stroke-width="1.2" marker-end="url(#arrow)"/><path d="{path}" stroke="{color}" fill="none" stroke-width="2.5" class="flow"/>'
 for i,(y,text) in enumerate(zip(ys,labels)):
  b+=f'<rect x="14" y="{y-34}" width="144" height="68" rx="10" fill="none" stroke="{color}" class="stage" style="animation-delay:-{i*1.9}s"/>'
  rows=textwrap.wrap(text,14)
  for j,row in enumerate(rows):b+=txt(86,y+6+(j-(len(rows)-1)/2)*20,row,16,INK,extra='text-anchor="middle"')
 h=ys[-1]+63
 save(f'{ch["n"]}-{name}-mobile.svg',width,h,label+' - '+spec['concept'],spec['concept']+'. Compact stacked layout preserves dependencies and feedback paths.',b)

def picture(file,alt):
 return '<picture>\n<source media="(max-width: 600px)" srcset="./assets/workflows/'+file+'-mobile.svg" />\n<img src="./assets/workflows/'+file+'.svg" width="100%" alt="'+html.escape(alt,quote=True)+'" />\n</picture>'



def circular_journey(mobile):
 w=480 if mobile else 960;h=564 if mobile else 640
 cx,cy=(240,270) if mobile else (480,310)
 r=132 if mobile else 190
 b=txt(24 if mobile else 32,28,'SMALL PONY / ENGINEERING JOURNEY',13 if mobile else 16,INK,700,extra='letter-spacing="1.5"')
 b+=f'<g transform="translate({cx} {cy})">'
 # Fine orbit lines give the ring depth without a solid light-theme background.
 for radius in [r-35,r+24]:
  b+=f'<circle r="{radius}" fill="none" stroke="{LINE}" stroke-width=".7" stroke-dasharray="1 7"/>'
 for i,ch in enumerate(CHAPTERS):
  color=balanced(ch['color']);start=math.radians(-76+i*72);end=math.radians(-32+i*72)
  x,y=math.cos(start)*r,math.sin(start)*r;X,Y=math.cos(end)*r,math.sin(end)*r
  arc=f'M{x:.3f} {y:.3f}A{r} {r} 0 0 1 {X:.3f} {Y:.3f}'
  b+=f'<path d="{arc}" fill="none" stroke="{color}" stroke-width="{9 if mobile else 13}" stroke-linecap="round" opacity=".26"/>'
  b+=f'<path d="{arc}" fill="none" stroke="{color}" stroke-width="{3 if mobile else 4}" stroke-linecap="round" class="flow" style="animation-duration:8s;animation-delay:-{i*1.6}s"/>'
  # Arrow chevrons make the chronological direction explicit.
  angle=end-.04;ax,ay=math.cos(angle)*r,math.sin(angle)*r
  b+=f'<path d="M{ax-5} {ay-7}L{ax} {ay}L{ax+5} {ay-7}" transform="rotate({math.degrees(angle)} {ax} {ay})" fill="none" stroke="{color}" stroke-width="2"/>'
 # A visible traveler follows the whole orbit; the bounds keep its center stable.
 b+=f'<g class="orbit"><circle r="{r}" stroke="none" fill="none"/><circle cy="-{r}" r="{4 if mobile else 6}" fill="{BLUE}"/><circle cy="{r}" r="3" fill="{balanced("#df7755")}"/></g>'
 inner=72 if mobile else 117
 b+=f'<circle r="{inner}" fill="none" stroke="{LINE}" stroke-width=".7"/>'
 b+=f'<circle r="{inner-8}" fill="none" stroke="{LINE}" stroke-width=".7" stroke-dasharray="1 9"/>'
 b+=txt(0,-16,'ENGINEERING',13 if mobile else 18,INK,600,extra='text-anchor="middle" letter-spacing="2"')
 b+=txt(0,17,'IN MOTION',23 if mobile else 32,INK,700,extra='text-anchor="middle" letter-spacing=".5"')
 b+=f'<path d="M-30 {32 if mobile else 42}H30" stroke="{BLUE}" stroke-width="2" class="flow"/>'
 b+='</g>'
 pairs=[('php','javascript'),('react','nodedotjs'),('docker','kubernetes'),('python','apachespark'),('openai','pytorch')]
 roles=['SOFTWARE','FULL-STACK','DEVOPS','DATA','AI / AGENTS']
 if mobile:
  labels=[(240,61,'middle'),(454,175,'end'),(350,445,'middle'),(130,445,'middle'),(26,175,'start')]
 else:
  labels=[(480,46,'middle'),(756,232,'start'),(620,535,'middle'),(340,535,'middle'),(204,232,'end')]
 for i,ch in enumerate(CHAPTERS):
  a=math.radians(-90+i*72);x=cx+math.cos(a)*r;y=cy+math.sin(a)*r;color=balanced(ch['color'])
  bw=70 if mobile else 98;bh=46 if mobile else 62
  b+=f'<rect x="{x-bw/2}" y="{y-bh/2}" width="{bw}" height="{bh}" rx="{bh/2}" fill="none" stroke="{color}" stroke-width="1.5"/>'
  # Arc gaps leave the technology marks clear without an opaque card surface.
  size=22 if mobile else 30
  for j,name in enumerate(pairs[i]):b+=icon(name,x-(size+5)+j*(size+10),y-size/2,size,color)
  lx,ly,anchor=labels[i]
  b+=txt(lx,ly,ch['date'],16 if mobile else 20,color,700,extra=f'text-anchor="{anchor}" letter-spacing=".5"')
  b+=txt(lx,ly+24 if mobile else ly+28,roles[i],16 if mobile else 20,INK,700,extra=f'text-anchor="{anchor}" letter-spacing=".5"')
 footer=532 if mobile else 610
 b+=txt(w/2,footer,'CHOOSE A CHAPTER TO EXPLORE ITS SYSTEM',14 if mobile else 17,BLUE,600,extra='text-anchor="middle" letter-spacing="1"')
 save('circle-mobile.svg' if mobile else 'circle.svg',w,h,'Small Pony - circular engineering journey','Clockwise journey: before 2017 software; 2017-2022 full-stack; 2021-2024 DevOps; 2023-2025 data engineering; 2024-2026 applied AI and agents. This animated circle is an overview; select a chapter in the controls below.',b)

def constellation(ch,mobile):
 w=480 if mobile else 960;h=790 if mobile else 650
 cx,cy=(240,390) if mobile else (480,326)
 rx,ry=(158,235) if mobile else (300,190)
 color=balanced(ch['color'])
 names={'01':'SOFTWARE','02':'FULL-STACK','03':'DEVOPS','04':'DATA','05':'APPLIED AI'}
 b=txt(24 if mobile else 32,32,ch['n']+' / TECHNOLOGY CONSTELLATION',14 if mobile else 16,color,700,extra='letter-spacing="1.2"')
 b+=txt(24 if mobile else 32,72 if mobile else 80,ch['title'],28 if mobile else 32,INK,700,extra='letter-spacing="-.5"')
 b+=f'<g transform="translate({cx} {cy})">'
 b+=f'<ellipse rx="{rx}" ry="{ry}" fill="none" stroke="{LINE}" stroke-width="1" opacity=".5"/>'
 b+=f'<ellipse rx="{rx-14}" ry="{ry-14}" fill="none" stroke="{LINE}" stroke-width=".7" stroke-dasharray="1 9" opacity=".6"/>'
 # A traveler follows the ellipse while logos remain stationary and readable.
 frames=[]
 for k in range(37):
  a=math.radians(-90+k*10)
  frames.append(f'{k/36*100:.4f}%{{transform:translate({math.cos(a)*rx:.3f}px,{math.sin(a)*ry:.3f}px)}}')
 b+='<style>@keyframes constellation-travel{'+''.join(frames)+'}.constellation-traveler{animation:constellation-travel 28s linear infinite}</style>'
 b+=f'<circle r="4" fill="{color}" class="constellation-traveler" style="transform:translate(0px,{-ry}px)"/>'
 b+='</g>'
 # Spokes are illustrative connections within a chapter, not dependency claims.
 for i,(_,_,brand) in enumerate(ch['logos']):
  a=math.radians(-90+i*360/len(ch['logos']));x=cx+rx*math.cos(a);y=cy+ry*math.sin(a)
  dx,dy=x-cx,y-cy;length=math.hypot(dx,dy)
  sx,sy=cx+dx/length*86,cy+dy/length*86
  ex,ey=x-dx/length*28,y-dy/length*28
  d=f'M{sx:.3f} {sy:.3f}L{ex:.3f} {ey:.3f}'
  b+=f'<path d="{d}" stroke="{LINE}" stroke-width=".6" opacity=".32"/>'
  b+=f'<path d="{d}" stroke="{color}" stroke-width="1.4" class="flow" style="animation-delay:-{i*.7:.2f}s" opacity=".65"/>'
 # Chapter hub: a star and label, with a clear 80-unit exclusion zone for spokes.
 b+=f'<circle cx="{cx}" cy="{cy}" r="80" fill="none" stroke="{color}" stroke-width="1"/>'
 star=[]
 for i in range(16):
  a=math.radians(-90+i*22.5);radius=20 if i%2==0 else 7
  star.append(f'{cx+math.cos(a)*radius:.2f},{cy-24+math.sin(a)*radius:.2f}')
 b+=f'<polygon points="{" ".join(star)}" fill="{color}" class="stage"/>'
 b+=txt(cx,cy+22,names[ch['n']],20 if mobile else 22,INK,700,extra='text-anchor="middle" letter-spacing="1"')
 b+=txt(cx,cy+49,ch['date'],14 if mobile else 17,color,600,extra='text-anchor="middle"')
 for i,(name,label,brand) in enumerate(ch['logos']):
  a=math.radians(-90+i*360/len(ch['logos']));x=cx+rx*math.cos(a);y=cy+ry*math.sin(a);brand=balanced(brand)
  b+=f'<circle cx="{x:.3f}" cy="{y:.3f}" r="27" fill="none" stroke="{brand}" stroke-width="1.2" class="stage" style="animation-delay:-{i*.7:.2f}s"/>'
  b+=icon(name,x-18,y-18,36,brand)
  lx=max(84,min(w-84,x))
  b+=txt(lx,y+49,label,18 if mobile else 20,INK,600,extra='text-anchor="middle"')
 footer=h-35
 b+=txt(w/2,footer,'EXPLORE INDIVIDUAL WORKFLOWS BELOW',13 if mobile else 16,color,600,extra='text-anchor="middle" letter-spacing=".6"')
 save('constellation-'+ch['n']+('-mobile' if mobile else '')+'.svg',w,h,ch['title']+' Technology constellation','Illustrative star system for '+ch['date']+'. Technology satellites: '+', '.join(v[1] for v in ch['logos'])+'. Satellite positions are decorative, not proficiency or dependency measurements.',b)


def build():
 OUT.mkdir(exist_ok=True)
 circular_journey(False);circular_journey(True)
 readme=picture('circle','Small Pony. An animated, clockwise circle connects five overlapping career chapters. Select a chapter using the controls below. Applied AI is open by default.')+'\n\n'
 count=0
 for ch in CHAPTERS:
  stage_labels={'01':'Software engineering','02':'Full-stack engineering','03':'DevOps and cloud','04':'Data engineering','05':'Applied AI and agents'}
  lead=ch['logos'][0][0];color=balanced(ch['color'])
  save('stage-'+ch['n']+'.svg',28,28,stage_labels[ch['n']],ch['date'],icon(lead,2,2,24,color))
  constellation(ch,False);constellation(ch,True)
  readme+='<details name="engineering-chapter"'+(' open' if ch['n']=='05' else '')+'>\n<summary><picture><img src="./assets/workflows/stage-'+ch['n']+'.svg" width="24" height="24" alt="'+stage_labels[ch['n']]+'" /></picture> &nbsp; <strong>'+ch['date']+'</strong> / '+stage_labels[ch['n']]+'</summary>\n\n'
  readme+=picture('constellation-'+ch['n'],ch['date']+' / '+stage_labels[ch['n']]+'. Technology logos arranged as satellites around the chapter star.')+'\n\n'
  readme+='<details>\n<summary><strong>Explore '+str(len(ch['logos']))+' technology workflows</strong></summary>\n\n<table width="100%" align="center">\n<tbody>\n'
  tiles=[]
  for name,label,color in ch['logos']:
   spec=dict(WORKFLOWS[name]);spec['nodes']=list(spec['nodes'])
   if ch['n']=='05' and name=='python':spec={'kind':'eventloop','concept':'Python orchestrates async model and tool calls','hint':'Async model and tool calls','nodes':['Task input','Async model call','Tool coroutine','Collected results']}
   if ch['n']=='04' and name=='postgresql':spec={'kind':'query','concept':'Analytical SQL groups and aggregates rows','hint':'Analytical aggregation','nodes':['Analytical SQL','Partition scan','Aggregate','Result set']}
   spec['tech']=name
   color=balanced(color)
   save(f'tile-{name}.svg',430,64,label,label+' technology mark',icon(name,192,6,46,color))
   save(f'tile-{name}-mobile.svg',150,64,label,label+' technology mark',icon(name,52,6,46,color))
   effect(ch,name,label,color,spec,False);effect(ch,name,label,color,spec,True)
   compact_effect(ch,name,label,color,spec)
   tile='<td width="50%" align="center" valign="top">\n<details>\n<summary>'+picture('tile-'+name,label+' logo')+'<br /><strong>'+html.escape(label)+'</strong><br /><sub>'+html.escape(spec['hint'])+'</sub></summary>\n\n'
   tile+=picture(ch['n']+'-'+name,label+': '+spec['concept'])+'\n\n</details>\n</td>\n'
   tiles.append(tile);count+=1
  for i in range(0,len(tiles),2):
   row=tiles[i:i+2]
   if len(row)==1:row=[row[0].replace('<td width="50%"','<td colspan="2"').replace('width="100%"','width="50%"',1)]
   readme+='<tr>\n'+''.join(row)+'</tr>\n'
  readme+='</tbody>\n</table>\n\n</details>\n</details>\n\n'
 (ROOT/'README.md').write_text(readme.rstrip()+'\n',encoding='utf-8')
 print(f'Built circular overview, five exclusive chapter controls, and {count} technology reveals; {len(WORKFLOWS)} distinct logos.')
if __name__=='__main__':build()
