import streamlit as st
from local_client import fetch_children_as_resources
from ui_components import inject_base_css,resource_card,video_resource_card,bottom_nav
st.set_page_config(page_title='Course | Switch',page_icon='📚',layout='centered',initial_sidebar_state='collapsed');inject_base_css();course=st.session_state.get('active_course',{'id':None,'code':'---','name':'Unknown course'})
if st.button('← Back'):st.switch_page('pages/1_Home.py')
st.markdown(f'### {course.get("code")}');st.caption(course.get('name',''));st.divider();kind,items=fetch_children_as_resources(course.get('id'))
if kind=='nodes':
    st.markdown('#### Browse further')
    for n in items:
        st.markdown(f'<div class="card"><b>{n["code"]} --- {n["name"]}</b></div>',unsafe_allow_html=True)
        if st.button('Open',key=f'd_{n["id"]}',use_container_width=True):st.session_state['active_course']=n;st.rerun()
elif kind=='groups':
    st.markdown('#### Resources')
    for title,links in items:
        st.markdown(f'##### {title or "Untitled topic"}')
        for r in links:(video_resource_card if r.get('file_type')=='video' else resource_card)(r,f't_{r["id"]}')
else:st.info('No links added here yet.')
bottom_nav('My Courses')
