import json,os,time
from pathlib import Path
P=Path(__file__).parent/'data/history.json';MAX=20
def _r():
    if not P.exists():return {}
    try:return json.loads(P.read_text(encoding='utf-8'))
    except (json.JSONDecodeError,OSError):return {}
def _w(d):
    t=P.with_suffix(P.suffix+f'.tmp{os.getpid()}');P.parent.mkdir(parents=True,exist_ok=True);t.write_text(json.dumps(d,indent=2),encoding='utf-8');os.replace(t,P)
def record_opened(uid,r):
    if not uid:return
    d=_r();rows=[x for x in d.get(uid,[]) if x.get('resource_id')!=r.get('id')];rows.insert(0,{'resource_id':r.get('id'),'title':r.get('title','Untitled'),'file_type':r.get('file_type','link'),'course_code':r.get('course_code',''),'url':r.get('url'),'youtube_video_id':r.get('youtube_video_id'),'opened_at':time.time()});d[uid]=rows[:MAX];_w(d)
def recent_for_user(uid,limit=5):return _r().get(uid,[])[:limit] if uid else []
