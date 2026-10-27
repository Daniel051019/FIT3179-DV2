"""Regenerate the readable Vega / Vega-Lite chart specifications from included data."""
import json, pathlib
P=pathlib.Path(__file__).resolve().parent
D=P/'data'
S=P/'specs'
S.mkdir(exist_ok=True)
teal='#126b68';orange='#c56b3d';navy='#18354a';gray='#dce5e1';purple='#765b91'
config={'background':None,'view':{'stroke':None},'font':'Arial','axis':{'labelFontSize':11,'titleFontSize':12,'titleFontWeight':'normal','labelColor':'#40545d','titleColor':'#40545d','gridColor':'#e9eeeb','domain':False,'tickColor':'#c8d3d0','labelLimit':290},'legend':{'labelFontSize':11,'titleFontSize':11,'orient':'bottom','titleFontWeight':'normal','titleLimit':500,'labelLimit':350,'columns':1},'title':{'font':'Arial','fontSize':16,'anchor':'start'}}
def vl(name,spec):
    spec={'$schema':'https://vega.github.io/schema/vega-lite/v5.json','width':'container','autosize':{'type':'fit-x','contains':'padding'},'config':config,**spec}
    (S/(name+'.json')).write_text(json.dumps(spec,ensure_ascii=False,indent=2))
def tip(field,title=None,fmt=None,type='quantitative'):
    d={'field':field,'type':type}
    if title:d['title']=title
    if fmt:d['format']=fmt
    return d
def studies():return {'url':'data/study_outcomes.json'}
def curr():return [{'filter':'datum.year == 2025'}]
study_rows=json.loads((D/'study_outcomes.json').read_text())
salary_order=[x['label'] for x in sorted([x for x in study_rows if x['year']==2025],key=lambda x:-x['salary'])]
def y():return {'field':'label','type':'nominal','sort':salary_order,'title':None}
salarytips=[tip('field','Study area',type='nominal'),tip('year','Survey year','d'),tip('salary','Median full-time salary','$,.0f')]
vl('01_salary',{'height':630,'data':studies(),'params':[{'name':'yearChoice','value':2025,'bind':{'input':'select','options':[2025,2024],'name':'Survey year: '}}],'transform':[{'filter':'datum.year == yearChoice'}],'layer':[
 {'mark':{'type':'bar','cornerRadiusEnd':3,'color':teal},'encoding':{'y':y(),'x':{'field':'salary','type':'quantitative','title':'Median annual full-time salary (AUD)','axis':{'format':'$,.0f'}},'tooltip':salarytips}},
 {'mark':{'type':'rule','strokeDash':[5,4],'color':orange},'encoding':{'x':{'datum':77000,'title':'Annual salary (AUD)'}}},
 {'mark':{'type':'text','align':'left','dx':5,'color':navy,'fontSize':10},'encoding':{'y':y(),'x':{'field':'salary','type':'quantitative'},'text':{'field':'salary','format':'$,.0f'}}}
]})
selected=['Computing and information systems','Engineering','Nursing','Pharmacy','Teacher education','Creative arts']
vl('02_bullet',{'height':270,'data':studies(),'transform':curr()+[{'filter':{'field':'field','oneOf':selected}}],'layer':[
 {'mark':{'type':'bar','color':'#e7eeea','size':30},'encoding':{'y':y(),'x':{'datum':110000,'type':'quantitative','scale':{'domain':[0,110000]},'title':'Annual salary (AUD)','axis':{'format':'$,.0f'}}}},
 {'mark':{'type':'bar','color':teal,'size':13},'encoding':{'y':y(),'x':{'field':'salary','type':'quantitative','title':'Annual salary (AUD)'},'tooltip':salarytips}},
 {'mark':{'type':'tick','color':orange,'size':32,'thickness':3},'encoding':{'y':y(),'x':{'datum':77000,'title':'Annual salary (AUD)'}}}
]})
vl('03_salary_employment',{'height':360,'data':studies(),'transform':curr(),'encoding':{'x':{'field':'fulltime_rate','type':'quantitative','scale':{'domain':[45,100]},'title':'Full-time employment rate (%)'},'y':{'field':'salary','type':'quantitative','scale':{'domain':[55000,110000]},'title':'Median annual full-time salary (AUD)','axis':{'format':'$,.0f'}}},'layer':[
 {'mark':{'type':'rule','strokeDash':[4,4],'color':'#a8b8b4'},'encoding':{'x':{'datum':75.4},'y':None}},
 {'mark':{'type':'rule','strokeDash':[4,4],'color':'#a8b8b4'},'encoding':{'y':{'datum':77000},'x':None}},
 {'params':[{'name':'areaPick','select':{'type':'point','fields':['field'],'on':'pointerover','clear':'pointerout'}}],'mark':{'type':'circle','size':150,'color':teal,'stroke':'white','strokeWidth':1.5},'encoding':{'opacity':{'condition':{'param':'areaPick','value':1},'value':0.35},'tooltip':salarytips+[tip('fulltime_rate','Full-time employment rate','0.1f')]}},
 {'transform':[{'filter':{'field':'field','oneOf':['Dentistry','Pharmacy','Creative arts','Computing and information systems']}}],'mark':{'type':'text','align':'left','dx':8,'dy':-12,'fontSize':11,'color':navy},'encoding':{'text':{'field':'label'}}}
]})
vl('04_parttime_heatmap',{'height':600,'data':studies(),'transform':curr()+[{'fold':['parttime_share','underemployment_share'],'as':['measure','pct']},{'calculate':"datum.measure == 'parttime_share' ? 'Working part-time' : 'Want more hours'",'as':'metric'}],'encoding':{'y':{'field':'label','type':'nominal','title':None,'sort':'ascending'},'x':{'field':'metric','type':'nominal','sort':['Working part-time','Want more hours'],'title':None,'axis':{'orient':'top','labelAngle':0}},'tooltip':[tip('field','Study area',type='nominal'),tip('metric','Measure',type='nominal'),tip('pct','Share of employed graduates (%)','0.1f')]},'layer':[
 {'mark':{'type':'rect','stroke':'white','strokeWidth':2},'encoding':{'color':{'field':'pct','type':'quantitative','scale':{'domain':[0,65],'range':['#edf4f0',teal]},'legend':{'title':'Share of employed graduates (%)'}}}},
 {'mark':{'type':'text','fontSize':11},'encoding':{'text':{'field':'pct','format':'.1f'},'color':{'condition':{'test':'datum.pct > 35','value':'white'},'value':navy}}}
]})
waffle=[]
for i in range(100):
    # One square = one percentage point; partial final square encodes the decimal exactly.
    full=max(0,min(1,59.4-i));waffle.append({'x':i%10,'y':i//10,'start':i%10,'end':i%10+full,'share':full})
vl('05_waffle',{'width':360,'height':270,'data':{'values':waffle},'encoding':{'x':{'field':'x','type':'quantitative','scale':{'domain':[0,10]},'axis':None},'y':{'field':'y','type':'ordinal','axis':None}},'layer':[
 {'mark':{'type':'rect','color':gray,'stroke':'white','strokeWidth':3},'encoding':{'x':{'field':'start','type':'quantitative'},'x2':{'datum':0},'tooltip':{'value':'59.4% full-time; 40.6% part-time, among employed domestic undergraduate graduates (2025)'}}},
 {'transform':[{'calculate':'datum.x+1','as':'right'}],'mark':{'type':'rect','color':gray,'stroke':'white','strokeWidth':3},'encoding':{'x':{'field':'start','type':'quantitative'},'x2':{'field':'right'}}},
 {'mark':{'type':'rect','color':teal,'stroke':'white','strokeWidth':3},'encoding':{'x':{'field':'start','type':'quantitative'},'x2':{'field':'end'},'tooltip':{'value':'59.4% full-time; 40.6% part-time (2025). Each square represents one percentage point.'}}}
]})
# Treemap uses Vega's native hierarchy layout. Area represents published occupation shares.
occupations=json.loads((D/'occupations.json').read_text())
tree=[{'id':'root','parent':None,'share':0}]+[{'id':x['occupation'],'parent':'root','share':x['share']} for x in occupations]
treemap={'$schema':'https://vega.github.io/schema/vega/v5.json','width':530,'height':340,'padding':5,'autosize':'fit','background':None,'data':[{'name':'tree','values':tree,'transform':[{'type':'stratify','key':'id','parentKey':'parent'},{'type':'treemap','field':'share','sort':{'field':'value','order':'descending'},'size':[{'signal':'width'},{'signal':'height'}],'paddingInner':4,'round':True}]},{'name':'leaves','source':'tree','transform':[{'type':'filter','expr':'datum.depth == 1'}]}],'scales':[{'name':'color','type':'ordinal','domain':[x['occupation'] for x in occupations],'range':[navy,teal,'#73a4a0','#adbb99',orange,purple]}],'marks':[{'type':'rect','from':{'data':'leaves'},'encode':{'enter':{'fill':{'scale':'color','field':'id'},'x':{'field':'x0'},'y':{'field':'y0'},'x2':{'field':'x1'},'y2':{'field':'y1'},'tooltip':{'signal':"datum.id + ': ' + datum.share + '% of employed graduates'"}},'hover':{'fillOpacity':{'value':0.8}},'update':{'fillOpacity':{'value':1}}}},{'type':'text','from':{'data':'leaves'},'encode':{'enter':{'x':{'signal':'(datum.x0+datum.x1)/2'},'y':{'signal':'(datum.y0+datum.y1)/2-9'},'align':{'value':'center'},'baseline':{'value':'middle'},'font':{'value':'Arial'},'fontSize':{'value':10},'fill':{'signal':"datum.id == 'Community and Personal Service Workers' || datum.id == 'Technicians and Trades Workers' ? '#18354a' : 'white'"},'text':{'signal':"datum.id == 'Community and Personal Service Workers' ? ['Community','services'] : datum.id == 'Clerical and Administrative Workers' ? ['Clerical','& admin'] : datum.id == 'Technicians and Trades Workers' ? 'T&T' : datum.id == 'Other occupations' ? ['Other','jobs'] : datum.id == 'Managers' ? 'Mgmt' : datum.id"},'lineHeight':{'value':15},'limit':{'signal':'datum.x1-datum.x0-12'}}}},{'type':'text','from':{'data':'leaves'},'encode':{'enter':{'x':{'signal':'(datum.x0+datum.x1)/2'},'y':{'signal':'(datum.y0+datum.y1)/2+30'},'align':{'value':'center'},'font':{'value':'Arial'},'fontSize':{'value':18},'fill':{'value':'white'},'text':{'signal':"datum.share+'%'"}}}}]}
(S/'06_occupations.json').write_text(json.dumps(treemap,indent=2))
vl('07_gender_dumbbell',{'height':600,'data':studies(),'transform':curr()+[{'filter':'isValid(datum.male) && isValid(datum.female)'}],'encoding':{'y':{'field':'label','type':'nominal','sort':{'field':'gap_pct','order':'descending'},'title':None},'x':{'type':'quantitative','scale':{'domain':[55000,90000]},'title':'Median annual full-time salary (AUD)','axis':{'format':'$,.0f'}}},'layer':[
 {'mark':{'type':'rule','color':'#b9c7c2','strokeWidth':3},'encoding':{'x':{'field':'female'},'x2':{'field':'male'},'tooltip':[tip('field','Study area',type='nominal'),tip('female','Female','$,.0f'),tip('male','Male','$,.0f'),tip('gap_pct','Gender gap (%)','0.1f')]}},
 {'transform':[{'fold':['female','male'],'as':['gender','salary']}],'mark':{'type':'circle','size':100,'stroke':'white','strokeWidth':1},'encoding':{'x':{'field':'salary'},'color':{'field':'gender','type':'nominal','scale':{'domain':['female','male'],'range':[orange,teal]},'legend':{'title':None}},'tooltip':[tip('field','Study area',type='nominal'),tip('gender','Gender',type='nominal'),tip('salary','Median salary','$,.0f')]}}
]})
vl('08_gender_gap',{'height':600,'data':studies(),'transform':curr()+[{'filter':'isValid(datum.gap_pct)'}],'mark':{'type':'bar','cornerRadiusEnd':2},'encoding':{'y':{'field':'label','type':'nominal','sort':'-x','title':None},'x':{'field':'gap_pct','type':'quantitative','title':'Male–female median salary gap (% of male median)'},'color':{'condition':{'test':'datum.gap_pct >= 0','value':teal},'value':orange},'tooltip':[tip('field','Study area',type='nominal'),tip('gap_pct','Gender gap (%)','0.1f')]}})
vl('09_salary_trend',{'height':340,'data':{'url':'data/salary_trend.json'},'transform':[{'fold':['salary','real_2025'],'as':['measure','value']},{'calculate':"datum.measure == 'salary' ? 'Salary in year reported' : 'Salary in 2025 dollars'",'as':'series'}],'mark':{'type':'line','point':True,'strokeWidth':3},'encoding':{'x':{'field':'year','type':'ordinal','title':None,'axis':{'labelAngle':0}},'y':{'field':'value','type':'quantitative','scale':{'domain':[50000,82000]},'title':'Median annual full-time salary (AUD)','axis':{'format':'$,.0f'}},'color':{'field':'series','type':'nominal','scale':{'domain':['Salary in year reported','Salary in 2025 dollars'],'range':[teal,orange]},'legend':{'title':None}},'tooltip':[tip('year','Year','d'),tip('series','Measure',type='nominal'),tip('value','Salary','$,.0f')]}})
trend=json.loads((D/'salary_trend.json').read_text());base=57900;inflated=trend[0]['real_2025'];last=77000
water=[{'stage':'2016 salary','low':0,'high':base,'type':'Total','amount':base},{'stage':'Inflation','low':base,'high':inflated,'type':'Inflation','amount':inflated-base},{'stage':'Real gain','low':inflated,'high':last,'type':'Real gain','amount':last-inflated},{'stage':'2025 salary','low':0,'high':last,'type':'Total','amount':last}]
vl('10_waterfall',{'height':340,'data':{'values':water},'encoding':{'x':{'field':'stage','type':'ordinal','sort':None,'title':None,'axis':{'labelAngle':0,'labelLimit':160}},'y':{'field':'high','type':'quantitative','title':'Annual salary (AUD)','axis':{'format':'$,.0f'}},'y2':{'field':'low'}},'layer':[
 {'mark':{'type':'bar','size':60},'encoding':{'color':{'field':'type','scale':{'domain':['Total','Inflation','Real gain'],'range':[navy,orange,teal]},'legend':None},'tooltip':[tip('stage','Component',type='nominal'),tip('amount','Amount','$,.0f')]}},
 {'mark':{'type':'text','dy':-10,'fontSize':11,'color':navy},'encoding':{'y2':None,'text':{'field':'amount','format':'$,.0f'}}}
]})
projection={'type':'conicEqualArea','parallels':[-18,-36],'rotate':[-134,0,0],'center':[0,-27]}
geo={'url':'data/australia_states.geojson','format':{'type':'json','property':'features'}}
lookup={'lookup':'properties.state','from':{'data':{'url':'data/state_context.json'},'key':'state','fields':['code','weekly_earnings','bachelor_thousands','bachelor_pct']}}
mapbase={'mark':{'type':'geoshape','fill':'#edf1ed','stroke':'white','strokeWidth':1},'data':geo}
vl('11_earnings_map',{'height':400,'projection':projection,'layer':[
 {'data':geo,'transform':[lookup],'mark':{'type':'geoshape','stroke':'white','strokeWidth':1.5},'encoding':{'color':{'field':'weekly_earnings','type':'quantitative','scale':{'domain':[1250,1650],'range':['#e5efe8',teal]},'legend':{'title':'Median weekly earnings (AUD)','format':'$,.0f'}},'tooltip':[tip('properties.state','State',type='nominal'),tip('weekly_earnings','All-employee weekly median','$,.0f')]}},
 {'data':{'url':'data/state_context.json'},'mark':{'type':'text','fontSize':11,'fontWeight':'bold','color':navy,'stroke':'white','strokeWidth':0.2},'encoding':{'longitude':{'field':'longitude'},'latitude':{'field':'latitude'},'text':{'field':'code'}}}
]})
vl('12_degree_symbols',{'height':400,'projection':projection,'layer':[
 mapbase,
 {'data':{'url':'data/state_context.json'},'mark':{'type':'circle','color':teal,'opacity':0.65,'stroke':'white','strokeWidth':1.5},'encoding':{'longitude':{'field':'longitude'},'latitude':{'field':'latitude'},'size':{'field':'bachelor_thousands','type':'quantitative','scale':{'range':[0,4500]},'legend':{'title':'Bachelor as highest qualification (000s)','values':[100,500,1400]}},'tooltip':[tip('state','State',type='nominal'),tip('bachelor_thousands','Estimated people (thousands)','0.1f')]}},
 {'data':{'url':'data/state_context.json'},'mark':{'type':'text','fontSize':11,'dy':-12,'fontWeight':'bold','color':navy},'encoding':{'longitude':{'field':'longitude'},'latitude':{'field':'latitude'},'text':{'field':'code'}}}
]})
vl('13_degree_cartogram',{'width':500,'height':340,'data':{'url':'data/state_context.json'},'encoding':{'x':{'field':'tile_x','type':'ordinal','axis':None,'scale':{'domain':[0,1,2,3,4],'padding':0.08}},'y':{'field':'tile_y','type':'ordinal','axis':None,'scale':{'domain':[0,1,2,3],'padding':0.08}},'tooltip':[tip('state','State',type='nominal'),tip('bachelor_pct','Bachelor as highest qualification (%)','0.1f')]},'layer':[
 {'mark':{'type':'rect','cornerRadius':5},'encoding':{'color':{'field':'bachelor_pct','type':'quantitative','scale':{'domain':[15,28],'range':['#edf2e9',teal]},'legend':{'title':'Share of residents aged 15–74 (%)'}}}},
 {'mark':{'type':'text','dy':-8,'fontWeight':'bold','fontSize':13},'encoding':{'text':{'field':'code'},'color':{'condition':{'test':'datum.bachelor_pct > 22','value':'white'},'value':navy}}},
 {'transform':[{'calculate':"format(datum.bachelor_pct,'.1f')+'%'",'as':'pct_label'}],'mark':{'type':'text','dy':14,'fontSize':13},'encoding':{'text':{'field':'pct_label'},'color':{'condition':{'test':'datum.bachelor_pct > 22','value':'white'},'value':navy}}}
]})
vl('14_salary_slope',{'height':360,'data':studies(),'transform':[{'filter':{'field':'field','oneOf':['Computing and information systems','Nursing','Pharmacy','Teacher education']}}],'mark':{'type':'line','point':{'filled':True,'size':90},'strokeWidth':3},'encoding':{'x':{'field':'year','type':'ordinal','title':None,'axis':{'labelAngle':0}},'y':{'field':'salary','type':'quantitative','scale':{'domain':[55000,87000]},'title':'Median annual full-time salary (AUD)','axis':{'format':'$,.0f'}},'color':{'field':'label','type':'nominal','scale':{'range':[teal,orange,purple,navy]},'legend':{'title':None}},'tooltip':salarytips}})
# Parallel coordinates make the pay / access / hours trade-off visible without a composite score.
# Each axis has its own labelled units; the plotted positions are simple linear rescalings.
axes=[{'axis':0,'score':1,'title':'Salary (AUD)'},{'axis':1,'score':1,'title':'Full-time employment (%)'},{'axis':2,'score':1,'title':'Want more hours (%)'}]
ticks=[]
for axis,vals in [(0,[0,25000,50000,75000,100000]),(1,[0,25,50,75,100]),(2,[0,25,50,75,100])]:
    for value in vals:
        score=value/100000 if axis==0 else value/100
        ticks.append({'axis':axis,'score':score,'tick':f'${value:,.0f}' if axis==0 else f'{value:.0f}%'})
points=[]
for row in study_rows:
    if row['year']!=2025 or row['field'] not in ['Computing and information systems','Pharmacy','Creative arts']:continue
    for axis,key,score in [(0,'salary',row['salary']/100000),(1,'fulltime_rate',row['fulltime_rate']/100),(2,'underemployment_share',row['underemployment_share']/100)]:
        points.append({'axis':axis,'score':score,'study':row['field'],'label':'Computing' if row['field'].startswith('Computing') else row['field'],'measure':axes[axis]['title'],'value':row[key]})
vl('15_parallel_outcomes',{'height':310,'padding':{'top':38,'bottom':5,'left':5,'right':5},'encoding':{'x':{'field':'axis','type':'quantitative','scale':{'domain':[-0.28,2.28]},'axis':None},'y':{'field':'score','type':'quantitative','scale':{'domain':[0,1]},'axis':None}},'layer':[
 {'data':{'values':axes},'mark':{'type':'rule','color':'#cad6d1'},'encoding':{'y':{'datum':0},'y2':{'datum':1}}},
 {'data':{'values':ticks},'mark':{'type':'tick','orient':'horizontal','size':10,'color':'#9cafa6'}},
 {'data':{'values':ticks},'mark':{'type':'text','align':'right','dx':-9,'fontSize':11,'color':navy},'encoding':{'text':{'field':'tick'}}},
 {'data':{'values':axes},'mark':{'type':'text','dy':-25,'fontSize':12,'fontWeight':'bold','color':navy},'encoding':{'y':{'datum':1},'text':{'field':'title'}}},
 {'data':{'values':points},'mark':{'type':'line','point':{'filled':True,'size':80},'strokeWidth':3,'opacity':0.8},'encoding':{'detail':{'field':'study'},'order':{'field':'axis'},'color':{'field':'label','type':'nominal','scale':{'range':[teal,orange,purple]},'legend':{'title':None}},'tooltip':[tip('study','Study area',type='nominal'),tip('measure','Measure',type='nominal'),tip('value','Value',',.1f')]}}
]})
print('Wrote',len(list(S.glob('*.json'))),'chart specifications')

# Apply the feedback revision after generating the base charts.
from refine_specs import run as refine
refine()
from feedback_specs import run as studio_feedback
studio_feedback()

from polish_specs import run as polish
polish()
