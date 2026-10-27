'use strict';
// Data and readable chart definitions are embedded in index.html.
const CHART_FILES={'01':'01_salary','02':'02_bullet','03':'03_salary_employment','04':'04_parttime_heatmap','05':'05_waffle','06':'06_occupations','07':'07_gender_dumbbell','08':'08_gender_gap','09':'09_salary_trend','10':'10_waterfall','11':'11_earnings_map','12':'12_degree_symbols','13':'13_degree_cartogram','14':'14_salary_slope','15':'15_parallel_outcomes','16':'16_salary_change'};
const views=new Map();
let selectedField='',embeddedData,embeddedSpecs;
const weight=word=>(word.match(/[A-Za-z0-9]+(?:['’][A-Za-z]+)*/g)||[]).length||1;
function setLimitedText(element,text){
  element.replaceChildren();let words=[],count=0;
  const flush=()=>{if(!words.length)return;const line=document.createElement('span');line.className='reading-line';line.textContent=words.join(' ')+' ';element.append(line);words=[];count=0;};
  for(const word of text.trim().split(/\s+/)){const n=weight(word);if(count+n>10)flush();words.push(word);count+=n;}flush();
}
function loadScript(url){return new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=url;s.onload=resolve;s.onerror=()=>{s.remove();reject(new Error('Library unavailable'));};document.head.append(s);});}
async function loadLibraries(){
  for(const [name,local,remote] of [
    ['vega','vendor/vega.min.js','https://cdn.jsdelivr.net/npm/vega@5.33.0/build/vega.min.js'],
    ['vegaLite','vendor/vega-lite.min.js','https://cdn.jsdelivr.net/npm/vega-lite@5.23.0/build/vega-lite.min.js'],
    ['vegaEmbed','vendor/vega-embed.min.js','https://cdn.jsdelivr.net/npm/vega-embed@6.29.0/build/vega-embed.min.js']
  ]){if(window[name])continue;try{await loadScript(local);}catch{await loadScript(remote);}}
}
function inlineSources(node){
  if(!node||typeof node!=='object')return;
  if(typeof node.url==='string'&&node.url.startsWith('data/')){
    const name=node.url.slice(5);if(!Object.hasOwn(embeddedData,name))throw new Error('Missing embedded source: '+name);
    node.values=JSON.parse(JSON.stringify(embeddedData[name]));delete node.url;
  }
  for(const v of Object.values(node))if(v&&typeof v==='object')inlineSources(v);
}
function updateStatus(){
  const status=document.getElementById('selection-status');
  if(!selectedField){setLimitedText(status,'All study areas are visible. Select a field, or click a chart mark, to follow it across related charts.');return;}
  const row=embeddedData['study_outcomes.json'].find(d=>d.year===2025&&d.field===selectedField);
  const amount=new Intl.NumberFormat('en-AU',{style:'currency',currency:'AUD',maximumFractionDigits:0}).format(row.salary);
  let text=selectedField+'. 2025 median full-time salary: '+amount+'. Full-time employment rate: '+row.fulltime_rate.toFixed(1)+'%.';
  if(row.male===null||row.female===null)text+=' The paired gender comparison is unavailable for this field.';
  setLimitedText(status,text);
}
async function followField(field){
  selectedField=field;document.getElementById('study-selector').value=field;document.getElementById('clear-selection').disabled=!field;updateStatus();
  await Promise.all([...views.values()].filter(d=>d.linked).map(d=>d.view.signal('followField',field).runAsync()));
}
async function draw(id,file){
  const node=document.getElementById('chart-'+id);
  try{
    const spec=JSON.parse(JSON.stringify(embeddedSpecs[file+'.json']));inlineSources(spec);
    const linked=Boolean(spec.usermeta&&spec.usermeta.linkedField);
    if(linked)spec.params.find(p=>p.name==='followField').value=selectedField;
    if(typeof spec.width==='number')spec.width=Math.min(spec.width,Math.max(240,node.clientWidth));
    const result=await vegaEmbed(node,spec,{actions:false,renderer:'svg',tooltip:true});const view=result.view;views.set(id,{view,linked});
    if(linked)view.addEventListener('click',(_,item)=>{
      const field=item&&item.datum&&item.datum.field;
      if(typeof field==='string'&&embeddedData['study_outcomes.json'].some(d=>d.field===field))followField(field===selectedField?'':field);
    });
    if(spec.$schema.includes('/vega/v5'))new ResizeObserver(()=>view.width(Math.max(240,node.clientWidth-10)).runAsync()).observe(node);
    if(id==='01')await view.signal('yearChoice',Number(document.getElementById('salary-year').value)).runAsync();
    node.dataset.loaded='true';
  }catch(error){
    console.error('Chart '+id,error);const p=document.createElement('p');p.className='chart-error';
    setLimitedText(p,'This chart could not load. Refresh the page. Check your connection if using the standalone HTML.');
    node.replaceChildren(p);node.dataset.loaded='error';
  }
}
function portableLinks(){
  if(location.protocol!=='file:')return;
  for(const a of document.querySelectorAll('a[href^="data/"],a[href^="specs/"]')){
    const original=a.getAttribute('href'),name=original.split('/').pop();
    const source=original.startsWith('data/')?embeddedData[name]:embeddedSpecs[name];if(source===undefined)continue;
    a.href=URL.createObjectURL(new Blob([typeof source==='string'?source:JSON.stringify(source,null,2)],{type:name.endsWith('.csv')?'text/csv':'application/json'}));a.download=name;
  }
}
async function showSalaryView(mode){
  const changes=mode==='change';
  for(const button of document.querySelectorAll('[data-salary-view]'))button.setAttribute('aria-pressed',String(button.dataset.salaryView===mode));
  document.getElementById('salary-level-panel').hidden=changes;
  document.getElementById('salary-change-panel').hidden=!changes;
  // Render once the newly visible container has its actual width.
  const id=changes?'16':'01',entry=views.get(id);
  if(entry)entry.view.finalize();
  views.delete(id);
  if(window.vegaEmbed)await draw(id,CHART_FILES[id]);
}
async function highlightParallel(field){
  const entry=views.get('15');
  if(entry)await entry.view.signal('parallelField',field).runAsync();
  setLimitedText(document.getElementById('parallel-status'),field?field+' is highlighted. Other profiles remain visible for comparison.':'All three profiles are visible. Select a study area to follow its line.');
}
async function start(){
  embeddedData=JSON.parse(document.getElementById('embedded-data').textContent);embeddedSpecs=JSON.parse(document.getElementById('embedded-specs').textContent);
  const selector=document.getElementById('study-selector');
  for(const field of [...new Set(embeddedData['study_outcomes.json'].map(d=>d.field))].sort()){const option=document.createElement('option');option.value=field;option.textContent=field;selector.append(option);}
  selector.addEventListener('change',e=>followField(e.target.value));
  document.getElementById('clear-selection').addEventListener('click',()=>followField(''));
  for(const button of document.querySelectorAll('[data-salary-view]'))button.addEventListener('click',()=>showSalaryView(button.dataset.salaryView));
  document.getElementById('parallel-selector').addEventListener('change',e=>highlightParallel(e.target.value));
  document.getElementById('salary-year').addEventListener('change',async e=>{
    const year=Number(e.target.value),entry=views.get('01');if(entry)await entry.view.signal('yearChoice',year).runAsync();
    setLimitedText(document.getElementById('year-status'),year+' national median: '+(year===2024?'$75,000':'$77,000')+'. Other comparison charts show 2025.');
  });
  updateStatus();portableLinks();
  try{await loadLibraries();await Promise.all(Object.entries(CHART_FILES).filter(([id])=>id!=='16').map(([id,file])=>draw(id,file)));await highlightParallel(document.getElementById('parallel-selector').value);if(!document.getElementById('salary-change-panel').hidden&&!views.has('16'))await draw('16',CHART_FILES['16']);}
  catch(error){console.error(error);for(const node of document.querySelectorAll('.chart')){const p=document.createElement('p');p.className='chart-error';setLimitedText(p,'Chart libraries could not load. Use the complete project folder, or connect to the internet and refresh.');node.replaceChildren(p);}}
}
start();
