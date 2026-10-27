"""Final readability improvements; run after the feedback specifications."""
import json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def run():
 for p in (ROOT/'specs').glob('*.json'):
  s=json.loads(p.read_text())
  if 'vega-lite' in s['$schema']:
   for group in ('axis','legend'):
    for key in ('labelFontSize','titleFontSize'):s.setdefault('config',{}).setdefault(group,{})[key]=13
  if p.name=='06_occupations.json':
   for m in s['marks']:
    en=m.get('encode',{}).get('enter',{})
    if m['type']=='text' and en.get('fontSize',{}).get('value')==10:en['fontSize']['value']=13
  if p.name=='15_parallel_outcomes.json':
   s['padding']['top']=8
   for l in s['layer']:
    mark=l.get('mark',{})
    if mark.get('type')=='text':mark['fontSize']=max(mark.get('fontSize',12),13)
  if p.name=='14_salary_slope.json':
   mark=s.pop('mark');s['encoding']['color']['legend']=None
   s['encoding']['x']={'field':'year','type':'quantitative','scale':{'domain':[2023.85,2025.92],'zero':False,'nice':False},'axis':{'values':[2024,2025],'format':'d','title':None,'grid':False}}
   s['transform'].append({'calculate':"datum.field === 'Computing and information systems' ? 'Computing' : datum.field === 'Teacher education' ? 'Teaching' : datum.label",'as':'short_label'})
   s['layer']=[{'mark':mark},{'transform':[{'filter':'datum.year == 2025'}],'mark':{'type':'text','align':'left','dx':9,'fontSize':13,'fontWeight':'bold'},'encoding':{'text':{'field':'short_label'}}}]
  p.write_text(json.dumps(s,indent=2,ensure_ascii=False))
if __name__=='__main__':run()
