import streamlit as st,local_auth
from local_client import fetch_active_courses
from ui_components import inject_base_css,bottom_nav,wordmark
st.set_page_config(page_title='My Courses | Switch',page_icon='📚',layout='centered',initial_sidebar_state='collapsed');inject_base_css();wordmark('1.1rem');st.markdown('### My Courses');st.caption('Browse into your course tree.');u=local_auth.current_user();uid=u['user_id'] if u else 'demo-student'
for c in fetch_active_courses(uid):
    st.markdown(f'<div class="card"><b>{c["code"]} --- {c["name"]}</b><div>Tap to browse</div></div>',unsafe_allow_html=True)
    if st.button('View resources',key=f'm_{c["id"]}',use_container_width=True):st.session_state['active_course']=c;st.switch_page('pages/3_Course_Detail.py')
bottom_nav('My Courses')
