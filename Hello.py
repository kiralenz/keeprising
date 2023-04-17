import streamlit as st
import base64
import json
import openai

# getting keys
with open('config/config.json') as f:
    keys = json.load(f)
PATH = keys['path']
openai_organization = keys['openai_organization']
openai.organization = openai_organization
openai_api_key = keys['openai_api_key']
openai.api_key = openai_api_key
openai.Model.list()

# streamlit page
st.set_page_config(
    page_title="Hello",
)

st.write("# Welcome to keeprising!")
st.markdown(
    """
    keeprising is a sourdough monitoring tool.
    You can select an activity or the dashboard mode in the sidebar. 
    In the help page you can find the possibility to ask ChatGPT for
    bread support or find maybe FAQs in the future. 
"""
)

# add bg
def add_bg(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
    
add_bg('bread_loaf.png') 