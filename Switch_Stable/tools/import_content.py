import json,sys,uuid
from pathlib import Path
import pandas as pd
MAP={'youtube':'youtube','drive_notes':'drive_notes','drive-notes':'drive_notes','drive questions':'drive_questions','drive_questions':'drive_questions','drive-questions':'drive_questions'};T=['university','faculty','department','year','semester','course_unit','leaf']
def norm(x):
    if not isinstance(x,str):return None
    return MAP.get(x.strip().lower().replace('-','_').replace(' ','_'))
def sid(*p):return str(uuid.uuid5(uuid.uuid5(uuid.NAMESPACE_URL,'switch-app://tree'),'/'.join(p)))
def build(src):
    df=pd.read_excel(src);df['path']=df['path'].ffill();df['Class Title']=df.groupby('path')['Class Title'].ffill();nodes={};links=[];counts={}
    def node(parts,d,parent):
        i=sid(*parts[:d+1])
        if i not in nodes:counts[parent]=counts.get(parent,0);nodes[i]={'id':i,'name':parts[d].strip(),'node_type':T[d] if d<len(T) else 'node','parent_id':parent,'sort_order':counts[parent]};counts[parent]+=1
        return i
    for _,r in df.iterrows():
        p=r.get('path');k=norm(r.get('link_kind'));url=r.get('url')
        if not isinstance(p,str) or not p.strip() or not k or not isinstance(url,str) or not url.strip():continue
        parts=[x.strip() for x in p.split('/') if x.strip()];parent=None
        for d in range(len(parts)):parent=node(parts,d,parent)
        title=r.get('Class Title');title=title.strip() if isinstance(title,str) and title.strip() else None;links.append({'id':sid('link',p,k,url.strip()),'node_id':parent,'link_kind':k,'url':url.strip(),'title':title})
    return {'nodes':list(nodes.values()),'links':links}
src=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent.parent/'repo_5.xlsx';out=Path(__file__).parent.parent/'data/tree.json';out.write_text(json.dumps(build(src),indent=2),encoding='utf-8');print('Wrote',out)
