import streamlit as st,local_auth
from local_client import fetch_active_courses,fetch_recently_viewed,fetch_feed,search_courses
from ui_components import inject_base_css,resource_card,video_resource_card,bottom_nav,wordmark
st.set_page_config(page_title='Home | Switch',page_icon='🟠',layout='centered',initial_sidebar_state='collapsed');inject_base_css();wordmark();u=local_auth.current_user();uid=u['user_id'] if u else 'demo-student'
with st.expander(f'Account · {u["username"]}' if u else 'Account'):
    if st.button('Sign out',use_container_width=True):local_auth.destroy_session(st.query_params.get('session'));st.query_params.pop('session',None);st.session_state.pop('_resolved_user',None);st.switch_page('pages/0_Auth.py')
q=st.text_input('Search',placeholder='Search course code, e.g. PHA 2101',label_visibility='collapsed')
if q:
    for c in search_courses(q):
        if st.button(f'{c["code"]} --- {c["name"]} · {c["matched_level"]}',key=f's_{c["id"]}',use_container_width=True):st.session_state['active_course']=c;st.switch_page('pages/3_Course_Detail.py')
st.divider();st.markdown('#### My Active Courses');courses=fetch_active_courses(uid)
for i in range(0,len(courses),2):
    cs=st.columns(2)
    for j,c in enumerate(courses[i:i+2]):
        with cs[j]:
            st.markdown(f'<div class="course-tile"><div>{c["name"]}</div><small>{c["code"]}</small></div>',unsafe_allow_html=True)
            if st.button('Open course',key=f'c_{c["id"]}',use_container_width=True):st.session_state['active_course']=c;st.switch_page('pages/3_Course_Detail.py')
recent=fetch_recently_viewed(uid)
if recent:
    st.markdown('###### Pick up where you left off')
    for r in recent:
        c=st.columns([4,1]);c[0].write(f'{r["title"]} · {r["course_code"]}')
        if c[1].button('Open',key=f'r_{r["resource_id"]}'):st.session_state['active_resource_id']=r['resource_id'];st.session_state['_last_opened_resource']=r;st.switch_page('pages/6_Viewer.py')
st.divider();st.markdown("#### What's New on Campus")
for r in fetch_feed():(video_resource_card if r.get('file_type')=='video' else resource_card)(r,'feed')
bottom_nav('Home')
