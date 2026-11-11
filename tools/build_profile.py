from pathlib import Path
import html, math, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
INK='#151821'; MUTED='#67717e'; BLUE='#3158ed'; RED='#ef553d'
CHAPTERS=[
 {'n':'01','date':'BEFORE 2017','title':'The foundations.','subtitle':'Software engineering / PHP / JavaScript','color':'#7056bb','logos':[('php','PHP','#777BB4'),('javascript','JavaScript','#b38b00'),('html5','HTML5','#E34F26'),('css','CSS','#663399'),('mysql','MySQL','#4479A1'),('jquery','jQuery','#0769AD'),('laravel','Laravel','#ed4438'),('bootstrap','Bootstrap','#7952B3')],'effect':'CODE / COMPOSE / SHIP'},
 {'n':'02','date':'2017 - 2022','title':'Connected systems.','subtitle':'Full-stack / React / cloud / microservices','color':'#3158ed','logos':[('react','React','#1688a6'),('typescript','TypeScript','#3178C6'),('nodedotjs','Node.js','#4b8839'),('nextdotjs','Next.js','#151821'),('graphql','GraphQL','#d82798'),('redis','Redis','#c0392b'),('nginx','NGINX','#16843a'),('mongodb','MongoDB','#338746'),('postgresql','PostgreSQL','#4169a1'),('amazonwebservices','AWS','#b46a00'),('googlecloud','Google Cloud','#4285F4')],'effect':'INTERFACES / SERVICES / CLOUD'},
 {'n':'03','date':'2021 - 2024','title':'Built to keep running.','subtitle':'DevOps / CI/CD / deployment / cloud operations','color':'#c04a24','logos':[('docker','Docker','#2496ED'),('kubernetes','Kubernetes','#326CE5'),('githubactions','GitHub Actions','#2088FF'),('git','Git','#F05032'),('gitlab','GitLab','#c34c22'),('terraform','Terraform','#7B42BC'),('ansible','Ansible','#151821'),('linux','Linux','#a98100'),('prometheus','Prometheus','#E6522C'),('grafana','Grafana','#c86a15')],'effect':'BUILD / TEST / DEPLOY / OBSERVE'},
 {'n':'04','date':'2023 - 2025','title':'Data, in motion.','subtitle':'Data engineering / ETL / ELT / orchestration','color':'#097e72','logos':[('python','Python','#3776AB'),('apacheairflow','Airflow','#017CEE'),('apachespark','Spark','#cb6818'),('apachekafka','Kafka','#151821'),('pandas','pandas','#150458'),('dbt','dbt','#c55a42'),('snowflake','Snowflake','#2686af'),('databricks','Databricks','#e84931'),('postgresql','PostgreSQL','#4169a1')],'effect':'EXTRACT / TRANSFORM / DELIVER'},
 {'n':'05','date':'2024 - 2026','title':'Intelligence, applied.','subtitle':'AI/ML / LLMs / agentic coding / agentic workflows','color':'#ac376c','logos':[('openai','OpenAI','#151821'),('anthropic','Anthropic','#906b55'),('googlegemini','Gemini','#5279db'),('mistralai','Mistral AI','#c66a12'),('huggingface','Hugging Face','#a37a00'),('ollama','Ollama','#151821'),('langchain','LangChain','#1C3C3C'),('pytorch','PyTorch','#d4482f'),('tensorflow','TensorFlow','#c56b00'),('scikitlearn','scikit-learn','#c16b1c'),('python','Python','#3776AB')],'effect':'CONTEXT / REASON / ACT / VERIFY'},
]

def text(x,y,value,size=16,color=INK,weight=400,extra=''):
 return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{html.escape(value)}</text>'

def icon(name,x,y,size,color):
 tree=ET.parse(OUT/'icons'/f'{name}.svg')
 paths=''.join('<path d="'+html.escape(p.attrib['d'],quote=True)+'"/>' for p in tree.iter() if p.tag.endswith('path'))
 return f'<g transform="translate({x} {y}) scale({size/24})" fill="{color}">{paths}</g>'

def save(name,w,h,title,desc,body):
 output=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>
<defs><pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#d9dde4"/></pattern></defs>
<style>
text{{font-family:Inter,'Segoe UI',Arial,sans-serif}}
.mono{{font-family:Consolas,monospace;letter-spacing:2px}}
.flow{{stroke-dasharray:16 88;animation:flow 5s linear infinite}}
.float{{animation:float 5s ease-in-out infinite}}
.pulse{{animation:pulse 3.6s ease-in-out infinite}}
.rotate{{transform-box:fill-box;transform-origin:center;animation:rotate 32s linear infinite}}
.dot{{animation:particle 4s ease-in-out infinite}}
@keyframes flow{{to{{stroke-dashoffset:-208}}}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-5px)}}}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
@keyframes rotate{{to{{transform:rotate(360deg)}}}}
@keyframes particle{{0%,100%{{opacity:.25;transform:translateY(0)}}50%{{opacity:1;transform:translateY(-9px)}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<rect width="{w}" height="{h}" fill="#fff"/>
{body}
</svg>'''
 (OUT/name).write_text(output,encoding='utf-8')

def cover(mobile=False):
 w=480 if mobile else 960;h=566 if mobile else 510
 b=text(28 if mobile else 40,42,'SMALL PONY',14,INK,700,extra='letter-spacing="3"')
 b+=text(28 if mobile else 40,70,'ENGINEERING / A CONTINUING PRACTICE',9,MUTED,extra='class="mono"')
 x=28 if mobile else 40
 if mobile:
  for y,label in [(151,'Always'),(218,'building.')]:b+=text(x,y,label,64,weight=700,extra='letter-spacing="-3"')
  b+=text(x,264,'From the web to intelligent systems.',18,MUTED)
  cx,cy=350,375;radius=77
 else:
  b+=text(34,174,'Always',90,weight=700,extra='letter-spacing="-5"')
  b+=text(34,265,'building.',90,weight=700,extra='letter-spacing="-5"')
  b+=text(40,316,'From the web to intelligent systems.',21,MUTED)
  cx,cy=742,230;radius=140
 b+=f'<circle cx="{cx}" cy="{cy}" r="{radius+22}" fill="url(#grid)"/>'
 b+=f'<g transform="translate({cx} {cy})"><g class="rotate">'
 for r,c,rot in [(radius,BLUE,0),(radius*.69,RED,60),(radius*.37,INK,120)]:
  b+=f'<ellipse rx="{r}" ry="{r*.33}" fill="none" stroke="{c}" stroke-width="1.7" transform="rotate({rot})"/>'
 b+='</g><circle r="6" fill="#3158ed" class="pulse"/></g>'
 base=452 if mobile else 398
 labels=['SOFTWARE','SYSTEMS','DATA','INTELLIGENCE']
 for i,label in enumerate(labels):
  px=x+(i%2)*210 if mobile else x+i*226
  py=base+(i//2)*29 if mobile else base
  b+=f'<circle cx="{px+3}" cy="{py-4}" r="3" fill="{[INK,BLUE,RED,"#097e72"][i]}"/>'
  b+=text(px+14,py,label,10,MUTED,extra='letter-spacing="1.3"')
 y=h-55
 b+=f'<path d="M{x} {y}H{w-x}" stroke="#dce0e7"/>'
 b+=text(x,h-23,'SELECT A CHAPTER TO REVEAL ITS MOTION',9,BLUE,extra='letter-spacing="1.3"')
 save('cover-mobile.svg' if mobile else 'cover.svg',w,h,'Small Pony - always building','A white editorial profile. Software, systems, data, and intelligence. Select a chapter logo panel to reveal its animated visual.',b)

def panel(ch,mobile=False):
 w=480 if mobile else 960;cols=4 if mobile else 8
 rows=math.ceil(len(ch['logos'])/cols)
 top=163 if mobile else 151
 h=top+rows*91+27
 b=f'<path d="M24 1H{w-24}" stroke="#d8dde5"/>'
 b+=text(26,38,ch['date'],12,ch['color'],600,extra='letter-spacing="1.8"')
 b+=text(w-73,46,ch['n'],34,'#dce0e7',400)
 b+=text(24,86,ch['title'],31 if mobile else 43,weight=600,extra='letter-spacing="-1.5"')
 # Split long mobile subtitles on discipline boundaries.
 if mobile:
  bits=ch['subtitle'].split(' / ')
  line1=' / '.join(bits[:2]);line2=' / '.join(bits[2:])
  b+=text(26,116,line1,14,MUTED)
  if line2:b+=text(26,139,line2,14,MUTED)
 else:b+=text(26,120,ch['subtitle'],16,MUTED)
 cell=(w-48)/cols
 for i,(name,label,color) in enumerate(ch['logos']):
  x=24+(i%cols)*cell;y=top+(i//cols)*91
  b+=f'<rect x="{x+3}" y="{y}" width="{cell-9}" height="77" rx="12" fill="#fff" stroke="#e4e7ed"/>'
  b+=icon(name,x+(cell-34)/2-2,y+10,34,color)
  b+=text(x+cell/2-2,y+64,label,11.5,INK,extra='text-anchor="middle"')
 b+=f'<circle cx="{w-30}" cy="{h-9}" r="3" fill="{ch["color"]}" class="pulse"/>'
 save(f'chapter-{ch["n"]}{"-mobile" if mobile else ""}.svg',w,h,ch['title']+' '+ch['date'],ch['subtitle']+'. Representative technologies: '+', '.join(t[1] for t in ch['logos'])+'. Expand to reveal the animation.',b)

def motion(ch,mobile=False):
 w=480 if mobile else 960;h=365 if mobile else 330;cx=w/2;cy=160
 b=f'<rect x="24" y="12" width="{w-48}" height="{h-28}" rx="18" fill="#f8f9fc"/>'
 b+=text(44,43,'MOTION STUDY / '+ch['n'],10,ch['color'],extra='class="mono"')
 n=int(ch['n'])
 if n==1:
  left=66;right=w-66
  for j,length in enumerate([.4,.76,.56,.86,.36]):
   y=90+j*27
   b+=f'<path d="M{left} {y}H{left+(right-left)*length}" stroke="#e1e4ed" stroke-width="9" stroke-linecap="round"/>'
   b+=f'<path d="M{left} {y}H{left+(right-left)*length}" stroke="{ch["color"]}" stroke-width="3" stroke-linecap="round" class="flow" style="animation-delay:-{j*.6}s"/>'
 elif n==2:
  nodes=[(cx,cy),(cx-120,cy-45),(cx+120,cy-45),(cx-100,cy+65),(cx+100,cy+65)]
  for i,(x,y) in enumerate(nodes[1:]):
   b+=f'<path d="M{cx} {cy}L{x} {y}" stroke="#d1d9f7" stroke-width="2"/><path d="M{cx} {cy}L{x} {y}" stroke="{BLUE}" stroke-width="2" class="flow" style="animation-delay:-{i}s"/>'
  for i,(x,y) in enumerate(nodes):
   b+=f'<rect x="{x-22}" y="{y-22}" width="44" height="44" rx="12" fill="#fff" stroke="#ccd5f2"/>'
   b+=icon(['react','nodedotjs','googlecloud','postgresql','redis'][i],x-12,y-12,24,BLUE)
 elif n==3:
  b+=f'<path d="M{cx-137} {cy}H{cx+137}" stroke="#ead8d1" stroke-width="2"/><path d="M{cx-137} {cy}H{cx+137}" stroke="{RED}" stroke-width="3" class="flow"/>'
  for i,label in enumerate(['BUILD','TEST','DEPLOY','WATCH']):
   x=cx-132+i*88
   b+=f'<circle cx="{x}" cy="{cy}" r="22" fill="#fff" stroke="#dbb6a6"/>'
   b+=f'<circle cx="{x}" cy="{cy}" r="8" fill="{ch["color"]}" class="pulse" style="animation-delay:-{i*.6}s"/>'
   b+=text(x,cy+49,label,9,MUTED,extra='text-anchor="middle" letter-spacing="1"')
 elif n==4:
  for j in range(5):
   y=105+j*24
   b+=f'<path d="M65 {y}C{cx-60} {y},{cx-70} {cy},{cx} {cy}S{cx+80} {y},{w-65} {y}" fill="none" stroke="#d8e9e4" stroke-width="2"/>'
   b+=f'<path d="M65 {y}C{cx-60} {y},{cx-70} {cy},{cx} {cy}S{cx+80} {y},{w-65} {y}" fill="none" stroke="{ch["color"]}" stroke-width="2" class="flow" style="animation-delay:-{j*.8}s"/>'
  b+=f'<circle cx="{cx}" cy="{cy}" r="23" fill="#fff" stroke="#92bdb1"/>'
  b+=icon('apachespark',cx-13,cy-13,26,ch['color'])
 else:
  # A deterministic particle field around OpenAI; intentionally conceptual.
  for ring,count in [(63,12),(97,22),(133,30)]:
   for j in range(count):
    angle=2*math.pi*j/count
    x=cx+math.cos(angle)*ring*(1.65 if not mobile else 1.15)
    y=cy+math.sin(angle)*ring*.76
    b+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{2.2+(j%3)*.55}" fill="{[BLUE,ch["color"],"#a0acc8"][j%3]}" class="dot" style="animation-delay:-{j*.19:.2f}s"/>'
  b+=f'<circle cx="{cx}" cy="{cy}" r="36" fill="#fff" stroke="#e2d8e5"/>'
  b+=icon('openai',cx-22,cy-22,44,INK)
 b+=text(cx,h-45,ch['effect'],9 if mobile else 11,MUTED,extra='text-anchor="middle" letter-spacing="1.6"')
 save(f'motion-{ch["n"]}{"-mobile" if mobile else ""}.svg',w,h,ch['title']+' Animated motion study',ch['effect']+'. Decorative conceptual animation, not live metrics.',b)

def picture(file,alt):
 return f'<picture>\n  <source media="(max-width: 600px)" srcset="./assets/{file}-mobile.svg" />\n  <img src="./assets/{file}.svg" width="100%" alt="{html.escape(alt,quote=True)}" />\n</picture>'

def build():
 cover();cover(True)
 readme=picture('cover','Small Pony. Always building. Software, systems, data, and applied intelligence. Select a chapter logo panel to reveal its motion study.')+'\n\n'
 for ch in CHAPTERS:
  panel(ch);panel(ch,True);motion(ch);motion(ch,True)
  readme+='<details>\n<summary>\n'+picture('chapter-'+ch['n'],ch['date']+' - '+ch['title']+' '+ch['subtitle']+'. Expand this logo panel to reveal its animation.')+'\n</summary>\n\n'
  readme+=picture('motion-'+ch['n'],'Animated visual: '+ch['effect'])+'\n\n</details>\n\n'
 (ROOT/'README.md').write_text(readme.rstrip()+'\n',encoding='utf-8')
 print('Built white profile: 22 SVGs, five native logo-panel reveals, no navigation links.')
if __name__=='__main__':build()
