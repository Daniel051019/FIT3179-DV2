"""Apply the four studio-feedback revisions after the original chart build."""
import copy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
S=ROOT/'specs'

def run():
    base=json.loads((S/'01_salary.json').read_text())
    change={k:copy.deepcopy(base[k]) for k in ['$schema','width','autosize','config']}
    change.update({
        'height':650,'padding':{'top':12,'left':5,'right':16,'bottom':5},
        'data':{'url':'data/study_outcomes.json'},
        'params':[{'name':'followField','value':''}],
        'usermeta':{'linkedField':True},
        'transform':[
            {'pivot':'year','value':'salary','groupby':['field','label']},
            {'calculate':"datum['2025'] - datum['2024']",'as':'change'},
            {'calculate':"datum.change / datum['2024'] * 100",'as':'change_pct'},
            {'calculate':'max(datum.change, 0)','as':'label_x'}
        ]
    })
    rows=json.loads((ROOT/'data/study_outcomes.json').read_text())
    old={r['field']:r['salary'] for r in rows if r['year']==2024}
    order=[r['label'] for r in sorted([r for r in rows if r['year']==2025],key=lambda r:-(r['salary']-old[r['field']]))]
    y={'field':'label','type':'nominal','sort':order,'title':None}
    x={'field':'change','type':'quantitative','scale':{'domain':[-2000,7500]},
       'title':'Change in median annual salary, 2024–2025 (AUD)',
       'axis':{'format':'$,.0f','values':[-2000,0,2000,4000,6000]}}
    fade={'condition':{'test':"followField === '' || datum.field === followField",'value':1},'value':0.16}
    tips=[{'field':'field','type':'nominal','title':'Study area'},
          {'field':'2024','type':'quantitative','title':'2024 annual median','format':'$,.0f'},
          {'field':'2025','type':'quantitative','title':'2025 annual median','format':'$,.0f'},
          {'field':'change','type':'quantitative','title':'Change (AUD)','format':'+$,.0f'},
          {'field':'change_pct','type':'quantitative','title':'Change (%)','format':'+.1f'}]
    change['layer']=[
        {'mark':{'type':'bar','color':'#126b68','cornerRadiusEnd':2},
         'encoding':{'x':x,'y':y,'opacity':fade,'tooltip':tips}},
        {'data':{'values':[{}]},'mark':{'type':'rule','color':'#68757d','strokeWidth':1.5},
         'encoding':{'x':{'datum':0,'type':'quantitative'}}},
        {'mark':{'type':'text','align':'left','dx':7,'color':'#18354a','fontSize':12},
         'encoding':{'x':{**x,'field':'label_x'},'y':y,'text':{'field':'change','format':'+$,.0f'},'opacity':fade,'tooltip':tips}}
    ]
    (S/'16_salary_change.json').write_text(json.dumps(change,indent=2,ensure_ascii=False))

    parallel=json.loads((S/'15_parallel_outcomes.json').read_text())
    parallel['height']=330
    parallel['padding']={'top':76,'left':5,'right':5,'bottom':5}
    parallel['params']=[{'name':'parallelField','value':''}]
    titles=['Annual salary\nAUD / year','Full-time work\n% available for full-time work','Want more hours\n% of employed graduates']
    for layer in parallel['layer']:
        for row in layer.get('data',{}).get('values',[]):
            if 'title' in row:row['title']=titles[row['axis']]
        if layer.get('mark',{}).get('type')=='text' and 'title' in layer.get('encoding',{}).get('text',{}).get('field',''):
            layer['mark'].update(dy=-61,fontSize=13,lineBreak='\n',lineHeight=17)
    directions=[{'axis':i,'score':1,'direction':t} for i,t in enumerate(['↑ Higher pay','↑ More access to work','↑ More wanting extra hours'])]
    parallel['layer'].insert(4,{'data':{'values':directions},'mark':{'type':'text','dy':-15,'fontSize':12,'fontWeight':'bold','color':'#126b68'},'encoding':{'text':{'field':'direction'}}})
    profiles=parallel['layer'][-1]
    for row in profiles['data']['values']:
        row['value_label']=f"${row['value']:,.0f} a year" if row['axis']==0 else f"{row['value']:.1f}%"
    profiles['mark'].pop('opacity',None)
    profiles['mark']['strokeWidth']={'expr':"parallelField !== '' && datum.study === parallelField ? 4.5 : 2.5"}
    profiles['encoding']['opacity']={'condition':{'test':"parallelField === '' || datum.study === parallelField",'value':1},'value':0.16}
    profiles['encoding']['tooltip']=[{'field':'study','type':'nominal','title':'Study area'},
        {'field':'measure','type':'nominal','title':'Measure'},
        {'field':'value_label','type':'nominal','title':'Observed value'}]
    selected=copy.deepcopy(profiles)
    selected['transform']=[{'filter':"parallelField !== '' && datum.study === parallelField"}]
    selected['mark']={'type':'text','align':'left','dx':10,'dy':12,'fontSize':12,'fontWeight':'bold','color':'#18354a'}
    selected['encoding'].pop('order',None)
    selected['encoding'].pop('color',None)
    selected['encoding']['text']={'field':'value_label'}
    parallel['layer'].append(selected)
    (S/'15_parallel_outcomes.json').write_text(json.dumps(parallel,indent=2,ensure_ascii=False))

if __name__=='__main__':run()
