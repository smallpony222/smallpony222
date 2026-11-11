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

def cover(mobile):
 w=480 if mobile else 960;h=380 if mobile else 330
 b=txt(25,50,'SMALL PONY',20,INK,700,extra='letter-spacing="4"')
 b+=txt(22,127,'Always building.',48 if mobile else 72,INK,700,extra='letter-spacing="-2"')
 b+=txt(26,176,'Software. Systems. Data. Applied AI.',19 if mobile else 24,INK,600)
 cx,cy=(355,278) if mobile else (800,159)
 b+=f'<g transform="translate({cx} {cy})"><g class="orbit">'
 r=64 if mobile else 110
 for angle,c in [(0,BLUE),(60,balanced('#e56f40')),(120,INK)]:b+=f'<ellipse rx="{r}" ry="{r*.32}" transform="rotate({angle})" fill="none" stroke="{c}" stroke-width="2"/>'
 b+='</g></g>'
 b+=txt(26,h-36,'SELECT A LOGO TO EXPLORE ITS WORKFLOW',19,BLUE)
 save('cover-mobile.svg' if mobile else 'cover.svg',w,h,'Small Pony - engineering journey','Always building. Select individual technology logos for their conceptual workflows.',b)

def chapter_art(ch,mobile):
 w=480 if mobile else 960;h=174 if mobile else 160
 c=balanced(ch['color'])
 b=f'<path d="M18 24V{h-24}" stroke="{c}" stroke-width="3"/>'
 b+=txt(40,47,ch['date'],18,c,700,extra='letter-spacing="2"')
 b+=txt(38,96,ch['title'],30 if mobile else 39,INK,700,extra='letter-spacing="-1"')
 b+=txt(w-37,47,ch['n'],22,c,600,extra='text-anchor="end"')
 subtitles={
 '01':'Software engineering / PHP / JavaScript',
 '02':'Full-stack / cloud architecture / microservices',
 '03':'DevOps / delivery / cloud operations',
 '04':'Data engineering / ETL / ELT',
 '05':'AI/ML / LLMs / agentic workflows'}
 for i,row in enumerate(textwrap.wrap(subtitles[ch['n']],41 if mobile else 80)):
  b+=txt(40,130+i*23,row,18,INK)
 save(f'chapter-{ch["n"]}{"-mobile" if mobile else ""}.svg',w,h,ch['date']+' / '+ch['title'],subtitles[ch['n']],b)

def build():
 OUT.mkdir(exist_ok=True)
 cover(False);cover(True)
 readme=picture('cover','Small Pony. Always building. Software, systems, data, and applied AI. Select any technology logo for its own conceptual workflow.')+'\n\n'
 count=0
 for ch in CHAPTERS:
  chapter_art(ch,False);chapter_art(ch,True)
  readme+=picture('chapter-'+ch['n'],ch['date']+' / '+ch['title'])+'\n\n<table width="100%" align="center">\n<tbody>\n'
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
  readme+='</tbody>\n</table>\n\n'
 (ROOT/'README.md').write_text(readme.rstrip()+'\n',encoding='utf-8')
 print(f'Built {count} independent technology reveals; {len(WORKFLOWS)} distinct logos. Transparent, theme-neutral assets.')
if __name__=='__main__':build()
