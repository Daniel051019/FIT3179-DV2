"""Build the complete HTML, embedding CSS, app code, data and chart JSON.

Requires lxml (already available in the generation environment).
Visitors do not run this builder; open the generated index.html instead.
"""
import copy,html as escape_html,json,re
from pathlib import Path
from lxml import html,etree

ROOT=Path(__file__).resolve().parent
doc=html.document_fromstring((ROOT/'source/page.html').read_text())
for x in doc.xpath('//link[@rel="stylesheet"]|//script'):
    x.getparent().remove(x)
style=etree.SubElement(doc.find('head'),'style');style.text=(ROOT/'style.css').read_text()

def fragment(markup):return html.fragment_fromstring(markup)
first=doc.get_element_by_id('chart-01')
controls=fragment('''<div class="chart-controls"><div class="control-row"><label for="salary-year">Survey year</label><select id="salary-year"><option value="2025" selected="selected">2025</option><option value="2024">2024</option></select></div><p id="year-status" class="year-status" aria-live="polite">2025 national median: $77,000. Other comparison charts show 2025.</p></div>''')
first.addprevious(controls)
figure=first.getparent()
tabs=fragment('''<div class="salary-view-controls" role="group" aria-label="Salary comparison view"><button type="button" data-salary-view="level" aria-pressed="true" aria-controls="salary-level-panel">Salary levels</button><button type="button" data-salary-view="change" aria-pressed="false" aria-controls="salary-change-panel">Change: 2024–2025</button></div>''')
controls.addprevious(tabs)
level=etree.Element('div',{'id':'salary-level-panel'})
tabs.addnext(level)
level.append(controls);level.append(first)
level.append(figure.xpath('./p[@class="source"]')[0])
change=fragment('''<div id="salary-change-panel" hidden="hidden"><p class="chart-description">Compare both years without switching the year selector. Bars show the change in median annual salary. Left means a decrease; right means an increase. These are nominal changes between different graduating cohorts.</p><div class="comparison-scroll"><div id="chart-16" class="chart" aria-label="Change in median annual graduate salaries from 2024 to 2025 across all study areas"></div></div><p class="source">Change = 2025 median minus 2024 median. QILT GOS salary tables; different cohorts, not individual pay rises. <a href="specs/16_salary_change.json">Chart JSON</a> · <a href="data/study_outcomes.csv">Data CSV</a></p></div>''')
level.addnext(change)
compare=fragment('''<div class="comparison-controls" aria-label="Compare study areas"><div class="control-row"><label for="study-selector">Follow a study area</label><select id="study-selector"><option value="">All study areas</option></select><button id="clear-selection" type="button" disabled="disabled">Clear highlight</button></div><p id="selection-status" class="selection-status" aria-live="polite">All study areas are visible. Choose a field to highlight the same discipline across related charts.</p></div>''')
figure.addprevious(compare)

for p in doc.xpath('//p'):
    if 'Change the year to compare' in p.text_content():
        p.text='Choose salary levels or the change between both years. In salary levels, the dashed line marks the national median. Change view compares all disciplines directly. Click a bar to follow that study area.'
    if 'Positive values mean a higher male median.' in p.text_content():
        p.text='Indigo bars mean a higher male median. Coral bars mean a higher female median. Gap = (male median − female median) ÷ male median × 100.'
    if 'The orange series expresses' in p.text_content():
        p.text='The gold series expresses every year’s salary in 2025 dollars. It allows comparison of purchasing power across successive graduating cohorts.'
    if 'Orange ticks mark' in p.text_content():
        p.text='Thin teal bars show 2025 salaries. Grey ticks mark the national median; pale tracks provide a common scale.'
    if 'Both columns are percentages' in p.text_content():
        p.text='Both columns are percentages of employed graduates in each study area. “Want more hours” is the underemployed group: part-time workers seeking additional hours. It is a subset, not an additional employment category. Hover for exact values.'
    if p.get('class')=='byline':
        for span in p:span.set('class','date')
    if p.get('class')=='scope':
        # The survey and currency definitions remain unchanged.
        pass
for chapter in doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," chapter ")]'):
    number=chapter.xpath('.//span[@class="chapter-no"]')[0].text
    eyebrow=chapter.xpath('.//div[@class="chapter-heading"]//p[@class="eyebrow"]')[0]
    eyebrow.text=number+' / '+eyebrow.text

# Preserve bold, links and inline semantics while introducing bounded lines.
# Hyphenated words and numbers are counted conservatively as multiple words.
word_re=re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)*")
def weight(word):return len(word_re.findall(word)) or 1
def text_parts(element,path=()):
    if element.text:yield element.text,path
    for child in element:
        if child.tag=='br':yield '\n',()
        else:
            child_path=path+((child.tag,tuple(child.attrib.items())),)
            yield from text_parts(child,child_path)
        if child.tail:yield child.tail,path

def tokenize(element):
    # Tokenize across inline element boundaries, keeping attached punctuation.
    text='';paths=[]
    for part,path in text_parts(element):
        text+=part;paths.extend([path]*len(part))
    for match in re.finditer(r'\S+',text):
        yield match.group(),paths[match.start()]

def append_text(parent,text):
    if len(parent):parent[-1].tail=(parent[-1].tail or '')+text
    else:parent.text=(parent.text or '')+text

def line_element(tokens):
    root=etree.Element('span',{'class':'reading-line'})
    previous=();parents=[root]
    for i,(word,path) in enumerate(tokens):
        common=0
        for a,b in zip(previous,path):
            if a!=b:break
            common+=1
        parents=parents[:common+1]
        if i:append_text(parents[-1],' ')
        for tag,attrs in path[common:]:parents.append(etree.SubElement(parents[-1],tag,dict(attrs)))
        append_text(parents[-1],word);previous=path
    root.tail='\n'
    return root

line_count=0
for element in doc.xpath('//p|//footer/ol/li'):
    if element.get('class')=='key':
        # Retain the empty, decorative colour swatches in this short legend.
        assert sum(weight(w) for w in element.text_content().split())<=10
        continue
    tokens=list(tokenize(element))
    grouped=[];i=0
    while i<len(tokens):
        word,path=tokens[i];j=i+1
        if any(tag=='a' for tag,attrs in path):
            while j<len(tokens) and tokens[j][1]==path:
                word+=' '+tokens[j][0];j+=1
        grouped.append((word,path));i=j
    tokens=grouped
    original=' '.join(element.text_content().split())
    lines=[];current=[];count=0
    for word,path in tokens:
        if word=='\n':
            if current:lines.append(current);current=[];count=0
            continue
        n=weight(word)
        if count+n>10 and current:lines.append(current);current=[];count=0
        current.append((word,path));count+=n
    if current:lines.append(current)
    for child in list(element):element.remove(child)
    element.text=None
    for line in lines:
        assert sum(weight(word) for word,_ in line)<=10
        element.append(line_element(line));line_count+=1
    assert ' '.join(element.text_content().split())==original,(original,element.text_content())

catalog={}
for p in sorted((ROOT/'data').iterdir()):
    if p.suffix in ['.json','.geojson']:catalog[p.name]=json.loads(p.read_text())
    elif p.suffix=='.csv':catalog[p.name]=p.read_text()
specs={p.name:json.loads(p.read_text()) for p in sorted((ROOT/'specs').glob('*.json'))}
body=doc.find('body')
for id_,value in [('embedded-data',catalog),('embedded-specs',specs)]:
    el=etree.SubElement(body,'script',{'type':'application/json','id':id_})
    el.text=json.dumps(value,ensure_ascii=False,indent=2).replace('</','<\\/')
app=etree.SubElement(body,'script');app.text=(ROOT/'app.js').read_text()
result='<!doctype html>\n'+html.tostring(doc,encoding='unicode',pretty_print=True)
(ROOT/'index.html').write_text(result)
(ROOT.parent/'DV2_Graduate_Salaries.html').write_text(result)
print('Built complete HTML:',len(result.encode()),'bytes;',line_count,'bounded paragraph lines; maximum 10 words.')
