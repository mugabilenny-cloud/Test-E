import hashlib,json,os,secrets,time
from pathlib import Path
import streamlit as st
BASE=Path(__file__).parent; USERS=BASE/'data/users.json'; SESSIONS=BASE/'data/sessions.json'
ITERATIONS=260_000; TTL=3*24*60*60
def _read(p):
    if not p.exists(): return {}
    try:return json.loads(p.read_text(encoding='utf-8'))
    except (json.JSONDecodeError,OSError):return {}
def _write(p,d):
    p.parent.mkdir(parents=True,exist_ok=True); t=p.with_suffix(p.suffix+f'.tmp{os.getpid()}'); t.write_text(json.dumps(d,indent=2),encoding='utf-8'); os.replace(t,p)
def _hash(password,salt=None):
    salt=salt or secrets.token_bytes(16); h=hashlib.pbkdf2_hmac('sha256',password.encode(),salt,ITERATIONS); return salt.hex(),h.hex()
def create_user(username,password,semester):
    username=username.strip()
    if not username or not password:return False,'Username and password are required.'
    d=_read(USERS); k=username.lower()
    if k in d:return False,'That username is already taken.'
    salt,h=_hash(password); uid=secrets.token_hex(8); d[k]={'user_id':uid,'username':username,'salt':salt,'password_hash':h,'semester':semester,'created_at':time.time()}; _write(USERS,d); return True,uid
def verify_login(username,password):
    r=_read(USERS).get(username.strip().lower())
    if not r:return False,'No account with that username.'
    try:salt=bytes.fromhex(r['salt'])
    except (KeyError,ValueError,TypeError):return False,'Account record is invalid.'
    _,h=_hash(password,salt)
    return (True,r['user_id']) if secrets.compare_digest(h,r.get('password_hash','')) else (False,'Incorrect password.')
def get_user_by_id(uid):
    return next((r for r in _read(USERS).values() if r.get('user_id')==uid),None)
def create_session(uid):
    token=secrets.token_urlsafe(24); d=_read(SESSIONS); now=time.time(); d[token]={'user_id':uid,'created_at':now,'expires_at':now+TTL}; _write(SESSIONS,d); return token
def resolve_session(token):
    r=_read(SESSIONS).get(token) if token else None
    return r.get('user_id') if r and time.time()<=r.get('expires_at',0) else None
def destroy_session(token):
    if not token:return
    d=_read(SESSIONS)
    if token in d:del d[token];_write(SESSIONS,d)
def current_user():
    if '_resolved_user' in st.session_state:return st.session_state['_resolved_user']
    uid=resolve_session(st.query_params.get('session')); u=get_user_by_id(uid) if uid else None; st.session_state['_resolved_user']=u; return u
