import streamlit as st,local_auth
from local_client import fetch_resource,save_bookmark,record_resource_opened
from tree_store import youtube_video_id
from ui_components import inject_base_css,file_type_chip,youtube_embed
st.set_page_config(page_title='Viewer | Switch',page_icon='📄',layout='centered',initial_sidebar_state='collapsed');inject_base_css();rid=st.session_state.get('active_resource_id')
if not rid:st.warning('No resource selected.');st.stop()
r=fetch_resource(rid);r['youtube_video_id']=r.get('youtube_video_id') or youtube_video_id(r.get('url',''));u=local_auth.current_user();g=f'_viewer_history_{rid}'
if u and not st.session_state.get(g):record_resource_opened(u['user_id'],r);st.session_state[g]=True
if st.button('✕ Close'):st.switch_page('pages/1_Home.py')
st.markdown(f'**{r.get("title","Resource")}**');st.markdown(file_type_chip(r.get('file_type','')),unsafe_allow_html=True);st.caption(r.get('course_code',''))
if r.get('file_type')=='video' and r.get('youtube_video_id'):youtube_embed(r['youtube_video_id'],300)
else:st.info('Inline preview placeholder --- no download is forced to open this.')
a,b,c=st.columns(3)
if a.button('🔖 Save',use_container_width=True):save_bookmark(r,u['user_id'] if u else 'demo-student');st.toast('Saved')
if b.button('🔗 Copy Share Link',use_container_width=True):st.toast("Share links aren't available yet.")
c.button('Download',disabled=True,use_container_width=True)
