#!/usr/bin/env python3
"""Rebuild the guide SVG diagrams using bundled application-font outlines.

Optional publishing dependency: fonttools. Render each SVG to a 2200px-wide PNG
with an SVG renderer after editing. This script does not alter the skill core.
"""
from pathlib import Path
from html import escape
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
root=Path(__file__).resolve().parents[1]/'docs/user_guide'
fonts={s:TTFont(root/'fonts'/('GoogleSansFlex-'+s+'.ttf')) for s in ['Regular','Bold']}
def text(x,y,value,size=25,weight='Regular',color='#252522',center=False):
    f=fonts[weight]; gs=f.getGlyphSet(); cmap=f.getBestCmap(); scale=size/f['head'].unitsPerEm
    width=sum(f['hmtx'][cmap.get(ord(c),'space')][0] for c in value)*scale
    cursor=x-width/2 if center else x
    paths=[]
    for c in value:
        name=cmap.get(ord(c),'space'); pen=SVGPathPen(gs); gs[name].draw(pen)
        paths.append(f'<path d="{pen.getCommands()}" transform="translate({cursor:.3f},{y}) scale({scale},-{scale})"/>')
        cursor+=f['hmtx'][name][0]*scale
    return '<g fill="'+color+'" aria-label="'+escape(value,quote=True)+'">'+''.join(paths)+'</g>'
def rect(x,y,w,h,fill,stroke='#D3D3CC'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def arrow(x1,y1,x2,y2,color='#6C6C66'):
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="3" marker-end="url(#arrow)"/>'
def save(name,h,desc,body):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{h}" viewBox="0 0 1100 {h}" role="img"><title>{escape(desc)}</title><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 1 L8 5 L0 9" fill="none" stroke="#6C6C66" stroke-width="1.5"/></marker></defs><rect width="1100" height="{h}" fill="white"/>{body}</svg>'
    (root/'images'/(name+'.svg')).write_text(svg)
b=''
for x,n,title,lines in [(10,'1','Bring a brief',['State the business need','and the available evidence']),(385,'2','Answer questions',['Decide what is known','and what remains open']),(760,'3','Keep a draft',['Review the proposal','and save the record'])]:
    b+=rect(x,12,330,190,'#F3F3F0')+text(x+22,51,n,25,'Bold',color='#6750C7')+text(x+22,91,title,28,'Bold')+text(x+22,132,lines[0],23)+text(x+22,164,lines[1],23)
b+=arrow(345,106,377,106)+arrow(720,106,752,106)+text(550,246,'Return to questions whenever new uncertainty appears',25,center=True)
save('first-session-print',274,'First session: bring a brief, answer questions, keep a reviewed draft, and return to questions as needed.',b)
b=''
for y,n,title,body in [(10,'1','Adopt','Select or edit the proposal to create a draft'),(106,'2','Verify','Check that the cited source supports the meaning'),(202,'3','Approve','Authorised human approves identified revisions')]:
    b+=rect(12,y,1076,79,'#F3F3F0')+text(36,y+48,n,28,'Bold',color='#6750C7')+text(90,y+48,title,28,'Bold')+text(275,y+48,body,25)
    if y<202:b+=arrow(550,y+81,550,y+94)
b+=text(550,326,'Reject or revise when evidence does not support the proposal',25,center=True)
save('review-decisions-print',350,'Adoption creates a draft. Verification checks semantic support. Approval is a separate authorised human decision on identified revisions.',b)
b=rect(12,10,1076,88,'#EAF3FB')+text(38,46,'Historical baseline',26,'Bold')+text(38,79,'36 hour rule stays preserved with its original approval scope',25)
for x,title,sub in [(12,'Change request','Propose 48 hours'),(297,'Working draft','Revise artifacts'),(582,'Revalidation','Check impacts'),(867,'New approval','Selected scope')]:
    w=220 if x==867 else 245
    b+=rect(x,145,w,104,'#F3F3F0')+text(x+16,183,title,25,'Bold')+text(x+16,222,sub,23)
    if x<867:b+=arrow(x+w+4,196,x+277,196)
b+=text(550,301,'A request or revised draft does not replace an approved baseline',25,center=True)
save('change-print',325,'Preserve the 36 hour historical baseline. A proposed 48 hour rule needs revised drafts, revalidation and a new scoped approval.',b)
print('Created three diagrams using exact application-font outlines')
