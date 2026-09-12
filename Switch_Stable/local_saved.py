import json,os
from pathlib import Path
P=Path(__file__).parent/'data/saved.json'
def _r():
    if not P.exists():return {}
    try:return json.loads(P.read_text(encoding='utf-8'))
    except (json.JSONDecodeError,OSError):return {}
def _w(d):
    t=P.with_suffix(P.suffix+f'.tmp{os.getpid()}');P.parent.mkdir(parents=True,exist_ok=True);t.write_text(json.dumps(d,indent=2),encoding='utf-8');os.replace(t,P)
def saved_for_user(uid):return _r().get(uid,[]) if uid else []
def save_for_user(uid,r):
    if not uid:return
    d=_r();rows=d.get(uid,[])
    if not any(x.get('id')==r.get('id') for x in rows):rows.append(r)
    d[uid]=rows;_w(d)
