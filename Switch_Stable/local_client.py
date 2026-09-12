import uuid
from typing import Optional
import streamlit as st
import local_auth,local_history,local_saved
from tree_store import get_store
def get_or_create_device_token():
    t=st.query_params.get('device')
    if not t:t=str(uuid.uuid4());st.query_params['device']=t
    return t
def register_device(device_token,home_node_id:Optional[str]=None):return None
def _uid(s):return s if s and s!='demo-student' else None
def fetch_active_courses(student_id='demo-student'):
    store=get_store();home=st.session_state.get('home_node_id')
    if home:return [store.course(n) for n in store.children_of(home)]
    u=local_auth.get_user_by_id(student_id) if _uid(student_id) else None
    n=store.find_path(u.get('semester')) if u and u.get('semester') else None
    return [store.course(x) for x in store.children_of(n['id'])] if n and store.children_of(n['id']) else [store.course(x) for x in store.roots()]
def fetch_recently_viewed(student_id='demo-student'):return local_history.recent_for_user(student_id) if _uid(student_id) else []
def record_resource_opened(student_id,resource):
    if _uid(student_id):local_history.record_opened(student_id,resource)
def fetch_feed(department:Optional[str]=None):return []
def fetch_saved(student_id='demo-student'):return local_saved.saved_for_user(student_id) if _uid(student_id) else st.session_state.get('_session_bookmarks',[])
def save_bookmark(resource,student_id='demo-student'):
    if _uid(student_id):local_saved.save_for_user(student_id,resource)
    else:
        rows=st.session_state.get('_session_bookmarks',[])
        if not any(r.get('id')==resource.get('id') for r in rows):rows.append(resource)
        st.session_state['_session_bookmarks']=rows
def fetch_resource(resource_id):
    for k in ('_last_opened_resource','_session_bookmarks'):
        b=st.session_state.get(k)
        if isinstance(b,dict) and b.get('id')==resource_id:return b
        if isinstance(b,list):
            for r in b:
                if r.get('id')==resource_id:return r
    s=get_store();l=s.link_by_id(resource_id)
    if l:n=s.node_by_id(l['node_id']);return s.resource(l,n.get('name','') if n else '')
    return {'id':resource_id,'title':'Resource','course_code':'---','file_type':'link'}
def search_courses(q):
    if not q:return []
    s=get_store();nh,_=s.search(q);return [{'id':n['id'],'code':s.path(n)[:12],'name':n.get('name',''),'matched_level':n.get('matched_level','node')} for n in nh]
def search_tree(q):return get_store().search(q) if q else ([],[])
def fetch_children_as_resources(node_id):
    s=get_store();children=s.children_of(node_id)
    if children:return 'nodes',[s.course(n) for n in children]
    n=s.node_by_id(node_id);name=n.get('name','') if n else ''
    return 'groups',[(title,[s.resource(l,name) for l in links]) for title,links in s.grouped(node_id)]
