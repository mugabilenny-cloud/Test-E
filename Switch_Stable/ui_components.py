import streamlit as st
import local_auth
from local_client import save_bookmark,record_resource_opened
from tree_store import youtube_video_id
STYLE={'video':('#DC2626','VIDEO','▶️'),'ppt':('#F97316','PPT','📊'),'pdf':('#EF4444','PDF','📄'),'note':('#3B82F6','NOTE','📝'),'doc':('#3B82F6','DOC','📃')}
def inject_base_css():st.markdown('<style>.card{border:1px solid #E5E7EB;border-radius:12px;padding:.9rem 1rem;margin-bottom:.6rem;background:#fff}.course-tile{border:1px solid #E85D2C;border-radius:14px;padding:1rem;background:#FBF3EC;min-height:90px}.switch-wordmark{font-weight:800;color:#E85D2C}.switch-wordmark .dot{color:#1A1A2E}.bottom-nav{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:1px solid #E5E7EB;padding:.4rem;z-index:999}</style>',unsafe_allow_html=True)
def wordmark(size='1.4rem'):st.markdown(f'<div class="switch-wordmark" style="font-size:{size}">switch<span class="dot">.</span></div>',unsafe_allow_html=True)
def file_type_chip(ft):
    c,l,i=STYLE.get(ft,('#6B7280','FILE','📎'));return f'<span style="display:inline-block;background:{c};color:#fff;border-radius:6px;padding:.1rem .5rem;font-size:.7rem;font-weight:700">{i} {l}</span>'
def _uid():u=local_auth.current_user();return u['user_id'] if u else 'demo-student'
def resource_card(r,key_prefix):
    c=STYLE.get(r.get('file_type'),('#6B7280','FILE','📎'))[0];st.markdown(f'<div class="card" style="border-left:4px solid {c}"><div>{file_type_chip(r.get("file_type"))} <span style="color:#6B7280">{r.get("course_code","")}</span></div><b>{r.get("title","Untitled")}</b></div>',unsafe_allow_html=True);cols=st.columns(3)
    if cols[0].button('Open',key=f'{key_prefix}_open_{r["id"]}',use_container_width=True):st.session_state['active_resource_id']=r['id'];st.session_state['_last_opened_resource']=r;st.switch_page('pages/6_Viewer.py')
    if cols[1].button('🔖 Save',key=f'{key_prefix}_save_{r["id"]}',use_container_width=True):save_bookmark(r,_uid());st.toast('Saved')
    if cols[2].button('🔗 Share',key=f'{key_prefix}_share_{r["id"]}',use_container_width=True):st.toast('Share link copied (placeholder)')
def youtube_embed(video_id,height=220):st.markdown(f'<div style="border-radius:12px;overflow:hidden;border:1px solid #E5E7EB"><iframe width="100%" height="{height}" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allowfullscreen></iframe></div>',unsafe_allow_html=True)
def video_resource_card(r,key_prefix):
    st.markdown(f'<div class="card" style="border-left:4px solid #DC2626">{file_type_chip("video")} <b>{r.get("title","Untitled")}</b></div>',unsafe_allow_html=True);vid=r.get('youtube_video_id') or youtube_video_id(r.get('url',''))
    if vid:youtube_embed(vid)
    else:st.caption('Couldn’t embed this video because its URL has no recognizable YouTube video ID.')
    a,b=st.columns(2)
    if a.button('🔖 Save',key=f'{key_prefix}_save_{r["id"]}',use_container_width=True):save_bookmark(r,_uid());st.toast('Saved')
    if b.button('🔗 Share',key=f'{key_prefix}_share_{r["id"]}',use_container_width=True):st.toast('Share link copied (placeholder)')
    if vid and local_auth.current_user():
        k=f'_history_recorded_{r["id"]}'
        if not st.session_state.get(k):record_resource_opened(local_auth.current_user()['user_id'],r);st.session_state[k]=True
def bottom_nav(active):
    st.markdown('<div class="bottom-nav">',unsafe_allow_html=True);cols=st.columns(4);tabs=[('Home','🏠','pages/1_Home.py'),('My Courses','📚','pages/2_My_Courses.py'),('Upload','⬆️','pages/4_Upload.py'),('Saved','🔖','pages/5_Saved.py')]
    for c,(lab,ico,page) in zip(cols,tabs):
        if c.button(f'{ico} {lab}',key=f'nav_{lab}',use_container_width=True):st.switch_page(page)
    st.markdown('</div>',unsafe_allow_html=True)
