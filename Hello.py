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


# Functions
def add_bg():
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(https://gist.githubusercontent.com/kiralenz/8fa216a5ab87e92944129da83d84dd5b/raw/806c89b90ee9c6eaf75f833eb9482c9cbca7dec1/bread_loaf.svg);
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
    
def add_logo(height):
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: url(https://gist.githubusercontent.com/kiralenz/16203a45856cfb596741f24f85e82fbe/raw/c9d93e3336730e77132d40df4eb8d758471bcfd8/keeprising_logo.svg);
                background-repeat: no-repeat;
                padding-top: {height - 40}px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def add_vertical_space(num_lines: int = 1):
    """Add vertical space to your Streamlit app."""
    for _ in range(num_lines):
        st.write("")

# streamlit page
st.set_page_config(
    page_title="Hello",
)

add_bg() 
add_logo(height=160)

st.write("# Welcome to keeprising!")
add_vertical_space()
st.markdown(
    """
    keeprising is a sourdough monitoring tool.
    You can select an activity or the dashboard mode in the sidebar. 
    In the help page you can find the possibility to ask ChatGPT for
    bread support or find maybe FAQs in the future. 
"""
)
add_vertical_space(num_lines=3)

# inspirational quote by ChatGPT
question = "Give me an inspirational quote about baking by a famous baker or cook, please"
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "user", "content": question},
    ]
)
answer = response['choices'][0]['message']['content']

st.header(answer)