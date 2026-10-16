"""Apply the lecturer-feedback revision to the chart specifications."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
S=ROOT/'specs'
PAY='#126b68';EMP='#3569a0';FEMALE='#bb6656';MALE='#4b55a3';REAL='#9d6a1d';DEGREE='#77568e';INK='#18354a';REFERENCE='#68757d'
FIELD_DOMAIN=['Computing','Computing & information systems','Nursing','Pharmacy','Teacher education','Creative arts']
FIELD_RANGE=['#8767ab','#8767ab','#c67a18','#6d6f75','#2c718c','#536784']

def load(n):return json.loads((S/n).read_text())
def save(n,s):(S/n).write_text(json.dumps(s,indent=2,ensure_ascii=False))
def linked(s):
    s.setdefault('params',[]).append({'name':'followField','value':''})
    s.setdefault('usermeta',{})['linkedField']=True
def fade():return {'condition':{'test':"followField === '' || datum.field === followField",'value':1},'value':0.16}

def run():
    for f in S.glob('*.json'):
        s=load(f.name)
        if 'vega-lite' in s['$schema']:
            s['config']['axis'].update(labelFontSize=12,titleFontSize=12,labelPadding=6,gridOpacity=0.65,labelLimit=420)
            s['config']['legend'].update(labelFontSize=12,titleFontSize=12)
        save(f.name,s)

    n='01_salary.json';s=load(n)
    s['params'][0].pop('bind',None)
    s['params'].append({'name':'nationalMedian','expr':'yearChoice === 2024 ? 75000 : 77000'})
    linked(s);s['height']=650;s['padding']={'top':32,'left':5,'right':10,'bottom':5}
    s['layer'][0]['encoding']['opacity']=fade()
    s['layer'][1]={'data':{'values':[{}]},'mark':{'type':'rule','strokeDash':[5,4],'color':REFERENCE,'strokeWidth':1.5},'encoding':{'x':{'datum':{'expr':'nationalMedian'},'type':'quantitative'}}}
    s['layer'][2]['transform']=[{'filter':"datum.field === 'Dentistry' || datum.field === 'Pharmacy' || datum.field === followField"}]
    s['layer'][2]['mark']['fontSize']=12
    s['layer'].append({'data':{'values':[{}]},'mark':{'type':'text','align':'center','baseline':'bottom','dy':-10,'fontSize':12,'color':REFERENCE},'encoding':{'x':{'datum':{'expr':'nationalMedian'},'type':'quantitative'},'y':{'value':0},'text':{'value':{'expr':"yearChoice + ' national median: ' + format(nationalMedian, '$,.0f')"}}}})
    save(n,s)

    n='02_bullet.json';s=load(n);linked(s)
    s['layer'][1]['encoding']['opacity']=fade();s['layer'][2]['mark']['color']=REFERENCE
    save(n,s)

    n='03_salary_employment.json';s=load(n);linked(s);s['height']=400
    s['layer'][2].pop('params',None)
    s['layer'][2]['mark']['color']=INK
    s['layer'][2]['encoding']['opacity']=fade()
    s['layer'][2]['encoding']['size']={'condition':{'test':'datum.field === followField','value':260},'value':130}
    s['layer'][3]['encoding']['opacity']=fade()
    s['layer'][3]['mark']['fontSize']=12
    s['layer'].append({'transform':[{'filter':"datum.field === followField && indexof(['Dentistry','Pharmacy','Creative arts','Computing and information systems'],datum.field) < 0"}],'mark':{'type':'text','align':'left','dx':9,'dy':-13,'fontSize':12,'fontWeight':'bold','color':INK},'encoding':{'text':{'field':'label'}}})
    save(n,s)

    n='04_parttime_heatmap.json';s=load(n);linked(s)
    s['height']=630;s['layer'][0]['encoding']['color']['scale']['range']=['#edf3fb',EMP]
    s['layer'][0]['encoding']['color']['legend']['values']=[0,20,40,60]
    s['layer'][0]['encoding']['opacity']=fade()
    s['layer'][1]['transform']=[{'filter':"datum.field === followField || datum.field === 'Creative arts' || datum.field === 'Pharmacy'"}]
    s['layer'][1]['encoding']['color']['condition']['test']='datum.pct > 48'
    s['layer'][1]['mark']['fontSize']=12
    save(n,s)

    n='05_waffle.json';s=load(n)
    s['layer']=s['layer'][1:]
    s['layer'][0]['mark']['color']='#e3ebf6';s['layer'][1]['mark']['color']=EMP
    save(n,s)

    n='06_occupations.json';s=load(n)
    s['scales'][0]['range']=['#314b63','#455f7d','#b3c0cf','#9887ad','#c8b5d2','#ded7e7']
    for mark in s['marks'][1:]:
        mark['encode']['enter']['fill']={'signal':"datum.id === 'Managers' || datum.id === 'Professionals' ? 'white' : '#18354a'"}
    save(n,s)

    n='07_gender_dumbbell.json';s=load(n);linked(s)
    for layer in s['layer']:layer['encoding']['opacity']=fade()
    s['layer'][1]['encoding']['color']['scale']={'domain':['female','male'],'range':[FEMALE,MALE]}
    s['layer'][1]['encoding']['color']['legend']['labelExpr']="datum.label === 'female' ? 'Female graduates' : 'Male graduates'"
    save(n,s)

    n='08_gender_gap.json';s=load(n);linked(s)
    s['encoding']['opacity']=fade();s['encoding']['color']['condition']['value']=MALE;s['encoding']['color']['value']=FEMALE
    save(n,s)

    n='09_salary_trend.json';s=load(n)
    s['encoding']['color']['scale']['range']=[PAY,REAL]
    # Endpoint labels are selective: only the first and latest years.
    encoding=s.pop('encoding');mark=s.pop('mark');transform=s.pop('transform')
    s['encoding']=encoding;s['transform']=transform
    s['layer']=[{'mark':mark},{'transform':[{'filter':"datum.series === 'Salary in 2025 dollars' && (datum.year === 2016 || datum.year === 2025)"}],'mark':{'type':'text','dy':-15,'fontSize':12,'fontWeight':'bold','color':REAL},'encoding':{'text':{'field':'value','format':'$,.0f'}}}]
    save(n,s)

    n='10_waterfall.json';s=load(n)
    s['layer'][0]['encoding']['color']['scale']['range']=[INK,REAL,PAY]
    save(n,s)

    n='11_earnings_map.json';s=load(n)
    s['layer'][0]['encoding']['color']['legend']['values']=[1300,1400,1500,1600]
    label=s['layer'].pop()
    label['mark'].update(fontSize=13,stroke=None,strokeWidth=0,color=INK)
    label['mark']['dx']={'expr':"datum.code === 'ACT' ? 18 : 0"}
    label['mark']['dy']={'expr':"datum.code === 'ACT' ? 13 : 0"}
    halo=json.loads(json.dumps(label));halo['mark'].update(color='white',stroke='white',strokeWidth=4,strokeJoin='round')
    s['layer'].extend([halo,label]);save(n,s)

    n='12_degree_symbols.json';s=load(n)
    s['layer'][1]['mark'].update(color=DEGREE,opacity=0.75)
    s['layer'][1]['encoding']['size']['scale']={'domain':[0,1500],'range':[0,3000]}
    s['layer'][1]['encoding']['size']['legend'].update(direction='horizontal',columns=3,title='Bachelor as highest qualification (000s)')
    s['layer'][2]['mark']['fontSize']=13
    save(n,s)

    n='13_degree_cartogram.json';s=load(n)
    s['layer'][0]['encoding']['color']['scale']['range']=['#f0edf7',DEGREE]
    for layer in s['layer'][1:]:
        layer['encoding']['color']['condition']['test']='datum.bachelor_pct > 25'
        layer['mark']['fontSize']=14
    save(n,s)

    n='14_salary_slope.json';s=load(n)
    s['encoding']['color']['scale']={'domain':FIELD_DOMAIN[1:5],'range':FIELD_RANGE[1:5]}
    save(n,s)

    n='15_parallel_outcomes.json';s=load(n)
    s['layer'][-1]['encoding']['color']['scale']={'domain':[FIELD_DOMAIN[i] for i in [0,5,3]],'range':[FIELD_RANGE[i] for i in [0,5,3]]}
    save(n,s)

if __name__=='__main__':run()
