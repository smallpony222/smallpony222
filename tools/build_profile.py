"""Build self-contained, animated SVG artwork for the GitHub profile."""
from pathlib import Path
import html
import textwrap
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ICONS = ASSETS / 'icons'
GOLD = '#d9bd83'
IVORY = '#f2eee5'
MUTED = '#a5abae'
TEAL = '#8bd2c6'

def text(x, y, value, size=16, color=IVORY, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{html.escape(value)}</text>'

def line(x1, y1, x2, y2, color='#333a3e', extra=''):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{color}" {extra}/>' if y1 == y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" {extra}/>'

def icon(name, x, y, size=24, color=GOLD):
    tree = ET.parse(ICONS / f'{name}.svg')
    paths = ''.join(f'<path d="{html.escape(p.attrib["d"], quote=True)}"/>' for p in tree.iter() if p.tag.endswith('path'))
    return f'<g transform="translate({x} {y}) scale({size / 24})" fill="{color}"><g class="logo">{paths}</g></g>'

def svg(name, height, title, description, body, extra_css=''):
    output = f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(description)}</desc>
<defs>
 <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#161d22"/><stop offset="1" stop-color="#0c1116"/></linearGradient>
 <linearGradient id="gold"><stop stop-color="#88734e"/><stop offset=".5" stop-color="#eddbb4"/><stop offset="1" stop-color="#ad9059"/></linearGradient>
 <radialGradient id="halo"><stop stop-color="#d9bd83" stop-opacity=".12"/><stop offset="1" stop-color="#d9bd83" stop-opacity="0"/></radialGradient>
</defs>
<style>
 text{{font-family:Inter,'Segoe UI',Arial,sans-serif}}
 .mono{{font-family:'SFMono-Regular',Consolas,monospace;letter-spacing:2px}}
 .signal{{stroke-dasharray:12 140;animation:signal 9s linear infinite}}
 .orbit{{transform-box:fill-box;transform-origin:center;animation:orbit 40s linear infinite}}
 .breathe{{animation:breathe 6s ease-in-out infinite}}
 .logo{{animation:logo 7s ease-in-out infinite}}
 .draw{{stroke-dasharray:10 16;animation:signal 18s linear infinite}}
 @keyframes signal{{to{{stroke-dashoffset:-304}}}}
 @keyframes orbit{{to{{transform:rotate(360deg)}}}}
 @keyframes breathe{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
 @keyframes logo{{0%,100%{{opacity:.78;transform:translateY(0)}}50%{{opacity:1;transform:translateY(-1.5px)}}}}
 @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
{extra_css}
</style>
<rect x=".5" y=".5" width="959" height="{height-1}" rx="22" fill="url(#bg)" stroke="#30373b"/>
{body}
</svg>'''
    (ASSETS / name).write_text(output, encoding='utf-8')

def hero():
    b = '<circle cx="757" cy="240" r="222" fill="url(#halo)"/>'
    b += '<rect x="42" y="32" width="38" height="38" rx="11" fill="#d9bd83"/>'
    b += text(49,57,'SP',17,'#151a1e',700)
    b += text(95,57,'SMALL PONY',16,weight=600,extra='letter-spacing="3"')
    b += text(693,55,'ENGINEERING / 2026',12,MUTED,extra='class="mono"')
    b += line(42,90,918,90)
    b += text(48,133,'SOFTWARE · SYSTEMS · DATA · AI',12,GOLD,extra='class="mono"')
    b += text(44,212,'From code.',65,weight=600,extra='letter-spacing="-3"')
    b += text(44,286,'To systems.',65,weight=600,extra='letter-spacing="-3"')
    b += text(44,360,'To intelligence.',65,GOLD,600,extra='letter-spacing="-3"')
    b += '<g transform="translate(757 246)">'
    for r in [66,105,146]:
        b += f'<circle r="{r}" fill="none" stroke="#3a3d3a"/>'
    b += '<g class="orbit"><circle r="146" fill="none" stroke="url(#gold)" stroke-width="2" stroke-dasharray="100 818"/><circle cy="-146" r="5" fill="#ead9b6"/></g>'
    b += '<g class="orbit" style="animation-direction:reverse;animation-duration:28s"><circle r="105" fill="none" stroke="#8bd2c6" stroke-dasharray="25 635" stroke-width="2"/></g>'
    b += '<path d="M-146 0H146M0-146V146" stroke="#283333"/>'
    b += '<rect x="-47" y="-47" width="94" height="94" rx="26" fill="#1c2428" stroke="#8b7d61"/>'
    b += '<path d="M-22 0l-12 0 12-13M22 0h12L22 13M9-18-9 18" fill="none" stroke="#eddbb4" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    for x,y,label in [(-8,-146,'BUILD'),(146,0,'SHIP'),(0,146,'EVOLVE')]:
        b += f'<circle cx="{x}" cy="{y}" r="4" fill="{TEAL}" class="breathe"/>'
    b += '</g>'
    b += line(48,414,912,414)
    b += text(48,452,'FULL-STACK ROOTS. SYSTEMS THINKING. APPLIED INTELLIGENCE.',11,MUTED,extra='letter-spacing="1.5"')
    b += '<circle cx="793" cy="448" r="4" fill="#8bd2c6" class="breathe"/>'
    b += text(807,452,'STILL BUILDING',10,TEAL,extra='letter-spacing="1.4"')
    svg('hero.svg',484,'Small Pony — engineering in motion','From code to systems to intelligence. Software, systems, data, and applied AI.',b)

CHAPTERS = [
    ('BEFORE','2017','Software foundations','PHP and JavaScript. Building the fundamentals.','Web applications, business logic, and the craft of shipping.', [('php','PHP'),('javascript','JavaScript')]),
    ('2017','2022','Full-stack systems','From React interfaces to cloud architecture.','Backend services, microservices, and connected experiences.', [('react','React'),('javascript','JavaScript')]),
    ('2021','2024','Production & reliability','Build. Test. Deploy. Keep it running.','CI/CD, cloud deployments, operations, and maintenance.', [('docker','Docker'),('kubernetes','Kubernetes'),('githubactions','CI/CD')]),
    ('2023','2025','Data engineering','Turning raw inputs into dependable data flows.','ETL / ELT pipelines, orchestration, and transformation.', [('python','Python'),('apacheairflow','Airflow'),('apachespark','Spark')]),
    ('2024','2026','Applied AI & agents','From models and LLMs to useful, working systems.','AI/ML, agentic coding, and tool-connected workflows.', [('python','Python'),('pytorch','PyTorch')]),
]

def journey():
    b = text(44,48,'01 / THE JOURNEY',12,GOLD,extra='class="mono"')
    b += text(44,94,'A broader lens. Every chapter.',34,weight=600,extra='letter-spacing="-1"')
    b += text(44,126,'Overlapping chapters. Compounding capabilities.',16,MUTED)
    b += '<path d="M209 195V1197" stroke="#394244" stroke-width="2"/>'
    b += '<path d="M209 195V1197" stroke="#d9bd83" stroke-width="2" class="signal"/>'
    for i,(start,end,title,sub,detail,logos) in enumerate(CHAPTERS):
        y=164+i*213
        color = TEAL if i == 4 else GOLD
        b += text(44,y+30,f'CHAPTER 0{i+1}',10,MUTED,extra='letter-spacing="2"')
        b += text(44,y+69,start,24,color,500)
        b += text(44,y+99,('— '+end) if start!='BEFORE' else end,24,color,500)
        b += f'<circle cx="209" cy="{y+60}" r="10" fill="#131b20" stroke="{color}"/><circle cx="209" cy="{y+60}" r="3" fill="{color}" class="breathe" style="animation-delay:{i}s"/>'
        b += f'<rect x="245" y="{y}" width="671" height="192" rx="15" fill="#192126" stroke="#323c40"/>'
        b += f'<path d="M264 {y+1}H332" stroke="{color}" stroke-width="2"/>'
        b += text(270,y+40,title,27,weight=600,extra='letter-spacing="-.5"')
        b += text(270,y+76,sub,17,IVORY)
        b += text(270,y+102,detail,15,MUTED)
        x=270
        for name,label in logos:
            b += f'<rect x="{x}" y="{y+130}" width="{len(label)*8+50}" height="36" rx="9" fill="#10181d" stroke="#354044"/>'
            b += icon(name,x+10,y+138,20,color)
            b += text(x+38,y+154,label,13,IVORY)
            x += len(label)*8+62
        if i==4:
            b += text(x+6,y+154,'LLMs / TOOL USE / HUMAN REVIEW',11,color,extra='letter-spacing=".5"')
    b += text(44,1261,'Technology marks illustrate each discipline; dates describe areas of focus.',12,MUTED)
    svg('journey.svg',1286,'Engineering journey, before 2017 through 2026','Before 2017: PHP and JavaScript. 2017–2022: full-stack, React, cloud architecture, and microservices. 2021–2024: DevOps, CI/CD, cloud deployment and maintenance. 2023–2025: data engineering, ETL and ELT. 2024–2026: AI/ML, LLMs, agentic coding and workflows. Technology logos are illustrative.',b)

def workflow():
    b=text(44,48,'02 / HOW I BUILD',12,GOLD,extra='class="mono"')
    b+=text(44,96,'Intent → working systems.',34,weight=600,extra='letter-spacing="-1"')
    b+=text(44,130,'Applied AI, grounded in engineering.',16,MUTED)
    b+='<path d="M118 235H839" stroke="#3a484b" stroke-width="2"/><path d="M118 235H839" stroke="#8bd2c6" stroke-width="2" class="signal"/>'
    stages=[('01','FRAME','Context & constraints'),('02','BUILD','Code & connected tools'),('03','VERIFY','Tests & human review'),('04','DELIVER','Deploy & observe')]
    for i,(n,title,sub) in enumerate(stages):
        x=44+i*225
        b+=f'<rect x="{x}" y="177" width="197" height="133" rx="14" fill="#192126" stroke="#3b474a"/>'
        b+=text(x+18,205,n,11,GOLD,extra='class="mono"')
        b+=text(x+18,249,title,21,weight=600,extra='letter-spacing="1"')
        b+=text(x+18,279,sub,12,MUTED)
        if i<3:
            b+=text(x+207,242,'›',25,TEAL)
    b+='<path d="M837 314V349H141V314" stroke="#4c625d" fill="none"/>'
    b+='<path d="M837 314V349H141V314" stroke="#8bd2c6" fill="none" class="signal" style="animation-direction:reverse"/>'
    b+=text(359,379,'OBSERVE · LEARN · REFINE',11,TEAL,extra='letter-spacing="2"')
    svg('workflow.svg',410,'An engineering approach to agentic workflows','Frame context and constraints, build code and connected tools, verify with tests and human review, deliver through deployment and observation. Iterate with feedback. This is a conceptual workflow, not live telemetry.',b)

def actions():
    for filename,kicker,title,sub in [
        ('explore.svg','THE WORK','Explore repositories','Code, tools & experiments'),
        ('systems.svg','FULL-STACK','Explore microservices','Services & connected interfaces'),
        ('connect.svg','LET’S TALK','Start a conversation','Engineering, systems & applied AI')]:
        b=f'<rect x=".5" y=".5" width="309" height="141" rx="16" fill="#172025" stroke="#3a4548"/>'
        b+=text(22,31,kicker,9,GOLD,extra='letter-spacing="2"')
        b+=text(22,72,title,20,weight=600,extra='letter-spacing="-.5"')
        b+=text(22,101,sub,11,MUTED)
        b+='<path d="M270 26h15v15M285 26l-17 17" stroke="#d9bd83" stroke-width="1.5" fill="none"/>'
        (ASSETS/filename).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="310" height="142" viewBox="0 0 310 142" role="img"><title>{html.escape(title)}</title><style>text{{font-family:Inter,Segoe UI,Arial,sans-serif}}</style>{b}</svg>',encoding='utf-8')

def mobile_svg(name, height, title, description, body):
    svg(name,height,title,description,body)
    path=ASSETS/name
    content=path.read_text(encoding='utf-8')
    content=content.replace(f'width="960" height="{height}" viewBox="0 0 960 {height}"',f'width="480" height="{height}" viewBox="0 0 480 {height}"')
    content=content.replace('width="959"','width="479"')
    path.write_text(content,encoding='utf-8')

def mobile():
    b=text(28,46,'SMALL PONY / ENGINEERING',12,GOLD,extra='letter-spacing="2"')
    b+=line(28,70,452,70)
    b+=text(28,126,'SOFTWARE · SYSTEMS · DATA · AI',11,MUTED,extra='letter-spacing="1"')
    for y,s in [(205,'From code.'),(270,'To systems.'),(335,'To intelligence.')]:
        b+=text(25,y,s,49,GOLD if y==335 else IVORY,600,extra='letter-spacing="-2"')
    b+='<g transform="translate(366 432)"><circle r="58" fill="none" stroke="#3a4344"/><circle r="39" fill="none" stroke="#3a4344"/><g class="orbit"><circle r="58" fill="none" stroke="#d9bd83" stroke-width="2" stroke-dasharray="50 315"/></g><path d="M-16 0l-9 0 9-9M16 0h9l-9 9M6-13-6 13" stroke="#d9bd83" stroke-width="2" fill="none"/></g>'
    b+=text(28,407,'FULL-STACK ROOTS.',13,MUTED,extra='letter-spacing="1"')
    b+=text(28,435,'SYSTEMS THINKING.',13,MUTED,extra='letter-spacing="1"')
    b+=text(28,463,'APPLIED INTELLIGENCE.',13,MUTED,extra='letter-spacing="1"')
    b+='<circle cx="32" cy="518" r="4" fill="#8bd2c6" class="breathe"/>'
    b+=text(46,522,'STILL BUILDING / 2026',11,TEAL,extra='letter-spacing="1.5"')
    mobile_svg('hero-mobile.svg',554,'Small Pony — engineering in motion','From code to systems to intelligence. Full-stack roots, systems thinking, applied AI.',b)
    b=text(24,43,'01 / THE JOURNEY',11,GOLD,extra='class="mono"')
    b+=text(24,88,'A broader lens.',31,weight=600)
    b+=text(24,125,'Every chapter.',31,weight=600)
    b+=text(24,162,'Overlapping chapters. Compounding capabilities.',14,MUTED)
    for i,(start,end,title,sub,detail,logos) in enumerate(CHAPTERS):
        y=195+i*277
        color=TEAL if i==4 else GOLD
        b+=f'<rect x="20" y="{y}" width="440" height="255" rx="16" fill="#192126" stroke="#364247"/>'
        b+=text(38,y+30,('BEFORE 2017' if start=='BEFORE' else start+' — '+end),13,color,extra='letter-spacing="1.5"')
        b+=text(402,y+30,f'0{i+1}',12,MUTED)
        b+=text(38,y+66,title,25,weight=600,extra='letter-spacing="-.7"')
        for k,row in enumerate(textwrap.wrap(sub,43)):
            b+=text(38,y+99+k*23,row,16)
        for k,row in enumerate(textwrap.wrap(detail,47)):
            b+=text(38,y+153+k*22,row,14,MUTED)
        x=38
        for name,label in logos:
            b+=icon(name,x,y+213,21,color)
            b+=text(x+29,y+230,label,13)
            x+=len(label)*8+51
    b+=text(24,1608,'A journey across disciplines. Always evolving.',13,MUTED)
    mobile_svg('journey-mobile.svg',1636,'Engineering journey, before 2017 through 2026','Five overlapping career chapters: software foundations, full-stack systems, DevOps, data engineering, and applied AI. Technology logos are illustrative.',b)
    b=text(24,43,'02 / HOW I BUILD',11,GOLD,extra='class="mono"')
    b+=text(24,88,'Intent → impact.',31,weight=600)
    b+=text(24,122,'Applied AI, grounded in engineering.',15,MUTED)
    for i,(title,detail) in enumerate([('FRAME','Context & constraints'),('BUILD','Code & connected tools'),('VERIFY','Tests & human review'),('DELIVER','Deploy & observe')]):
        y=157+i*107
        b+=f'<rect x="24" y="{y}" width="432" height="86" rx="13" fill="#192126" stroke="#3b474a"/>'
        b+=text(40,y+30,f'0{i+1}',12,GOLD)
        b+=text(85,y+34,title,20,weight=600,extra='letter-spacing="1"')
        b+=text(85,y+61,detail,15,MUTED)
        if i<3:
            b+=f'<path d="M240 {y+86}v21" stroke="#8bd2c6" class="breathe"/>'
    b+=text(66,610,'OBSERVE · LEARN · REFINE',13,TEAL,extra='letter-spacing="2"')
    mobile_svg('workflow-mobile.svg',639,'An engineering approach to agentic workflows','Frame, build, verify, and deliver. Iterate through observation, learning, and refinement.',b)

if __name__ == '__main__':
    ASSETS.mkdir(exist_ok=True)
    hero(); journey(); workflow(); actions(); mobile()
    print('Built nine self-contained SVG assets, including three mobile compositions.')
