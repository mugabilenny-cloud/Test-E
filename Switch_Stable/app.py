import streamlit as st,local_auth
from local_client import get_or_create_device_token,register_device
st.set_page_config(page_title='Switch',page_icon='🟠',layout='centered',initial_sidebar_state='collapsed')
register_device(get_or_create_device_token())
if local_auth.current_user():st.switch_page('pages/1_Home.py')
else:st.switch_page('pages/0_Auth.py')
