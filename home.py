import streamlit as st
import streamlit_antd_components as sac
from views import bulk_meta, about
from PIL import Image

favicon = Image.open("./assets/favicon.png")

st.set_page_config(
    page_title="Bulk Meta Tags Creator",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state='collapsed',
)

st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

with st.sidebar:    
    menu = sac.menu([
        sac.MenuItem('Bulk Meta', icon='google'),
        sac.MenuItem('About Me', icon='file-person-fill',),
    ], index=0, format_func='upper', size='middle', indent=30, open_index=None, open_all=True, return_index=False)
           
if menu == 'Bulk Meta':
    bulk_meta.createPage()
   
elif menu == 'About Me':
    about.createPage()