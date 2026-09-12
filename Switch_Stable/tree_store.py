import json,re
from pathlib import Path
from typing import Optional
import streamlit as st
P=Path(__file__).parent/'data/tree.json';RX=re.compile(r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([A-Za-z0-9_-]{11})')
def youtube_video_id(url):
    if not isinstance(url,str):return None
    m=RX.search(url);return m.group(1) if m else None
class TreeStore:
    def __init__(self,nodes,links):
        self.nodes={n['id']:n for n in nodes};self.links={l['id']:l for l in links};self.children={};self.by_node={}
        for n in nodes:self.children.setdefault(n.get('parent_id'),[]).append(n)
        for b in self.children.values():b.sort(key=lambda x:x.get('sort_order',0))
        for l in links:self.by_node.setdefault(l['node_id'],[]).append(l)
    def roots(self):return list(self.children.get(None,[]))
    def children_of(self,i):return list(self.children.get(i,[]))
    def node_by_id(self,i):return self.nodes.get(i)
    def link_by_id(self,i):return self.links.get(i)
    def links_for_node(self,i):return list(self.by_node.get(i,[]))
    def path(self,n):
        out=[n['name']];cur=n
        while cur.get('parent_id'):
            cur=self.nodes.get(cur['parent_id'])
            if not cur:break
            out.append(cur['name'])
        return '/'.join(reversed(out))
    def nodes_of_type(self,t):return [n for n in self.nodes.values() if n.get('node_type')==t]
    def find_path(self,p):return next((n for n in self.nodes.values() if self.path(n)==p),None)
    def grouped(self,i):
        g={}
        for l in self.links_for_node(i):g.setdefault(l.get('title'),[]).append(l)
        return list(g.items())
    def search(self,q):
        q=q.strip().lower();nh=[];lh=[]
        if not q:return nh,lh
        for n in self.nodes.values():
            if q in n.get('name','').lower():x=dict(n);x['matched_level']=n.get('node_type','node');nh.append(x)
        for l in self.links.values():
            tm=q in (l.get('title') or '').lower();um=q in (l.get('url') or '').lower()
            if tm or um:x=dict(l);x['matched_in']='title' if tm else 'url';lh.append(x)
        return nh,lh
    def course(self,n):return {'id':n['id'],'code':n.get('node_type','').upper()[:4] or 'NODE','name':n.get('name','Untitled'),'resource_count':None,'matched_level':n.get('node_type','node')}
    def resource(self,l,node_name=''):
        ft={'youtube':'video','drive_notes':'note','drive_questions':'doc'}.get(l.get('link_kind'),'link');r={'id':l.get('id'),'title':l.get('title') or l.get('url','Untitled link'),'course_code':node_name,'file_type':ft,'url':l.get('url')}
        if ft=='video':r['youtube_video_id']=youtube_video_id(l.get('url',''))
        return r
@st.cache_resource
def get_store():
    raw=json.loads(P.read_text(encoding='utf-8'));return TreeStore(raw['nodes'],raw['links'])
