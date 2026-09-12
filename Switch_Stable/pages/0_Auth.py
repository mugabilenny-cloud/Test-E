import streamlit as st,local_auth
from tree_store import get_store
from ui_components import inject_base_css,wordmark
st.set_page_config(page_title='Sign in | Switch',page_icon='🟠',layout='centered',initial_sidebar_state='collapsed');inject_base_css();wordmark();st.caption('Sign up or log in to see your courses.')
s=get_store();opts={}
for n in s.nodes_of_type('semester'):
    y=s.node_by_id(n.get('parent_id'));d=s.node_by_id(y.get('parent_id')) if y else None;opts[f'{d.get("name","?") if d else "?"} · {y.get("name","?") if y else "?"} · {n.get("name","?")}']=s.path(n)
a,b=st.tabs(['Log in','Sign up'])
with a:
    with st.form('login'):u=st.text_input('Username');p=st.text_input('Password',type='password');go=st.form_submit_button('Log in',use_container_width=True)
    if go:
        ok,r=local_auth.verify_login(u,p)
        if ok:st.query_params['session']=local_auth.create_session(r);st.session_state.pop('_resolved_user',None);st.switch_page('pages/1_Home.py')
        else:st.error(r)
with b:
    with st.form('signup'):u=st.text_input('Choose a username');p=st.text_input('Choose a password',type='password');sem=st.selectbox('Which semester are you currently in?',list(opts) or ['None']);go=st.form_submit_button('Sign up',use_container_width=True)
    if go:
        ok,r=local_auth.create_user(u,p,opts.get(sem,''))
        if ok:st.query_params['session']=local_auth.create_session(r);st.session_state.pop('_resolved_user',None);st.switch_page('pages/1_Home.py')
        else:st.error(r)
st.caption("You'll stay signed in on this device for up to 3 days.")
