import streamlit as st,local_auth
from local_client import fetch_saved
from ui_components import inject_base_css,resource_card,video_resource_card,bottom_nav
st.set_page_config(page_title='Saved | Switch',page_icon='🔖',layout='centered',initial_sidebar_state='collapsed');inject_base_css();st.markdown('### Saved');st.caption('Bookmarked notes for quick review.');u=local_auth.current_user();uid=u['user_id'] if u else 'demo-student';saved=fetch_saved(uid)
if not saved:st.info('Nothing saved yet. Tap Save on any resource card to add it here.')
for r in saved:(video_resource_card if r.get('file_type')=='video' else resource_card)(r,'saved')
bottom_nav('Saved')
