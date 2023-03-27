# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import json
import openai
import base64

# getting keys
with open('config/config.json') as f:
    keys = json.load(f)
openai_api_key = keys['openai_api_key']
openai_organization = keys['openai_organization']
openai.organization = openai_organization
openai.api_key = openai_api_key
openai.Model.list()

# Variables
PATH = ('/Users/kiralenz/Documents/keeprising/data/')

# Functions
# better read functions from utils, but not yet working
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

# Loading data
notes_history = pd.read_parquet(PATH + 'notes_history.parquet')
    
# streamlit page
st.set_page_config(page_title="Keeprising")
add_bg('bread_loaf.png')  
st.title('Keeprising - Here to help you')

# Notes
st.header("Your observations - Misstakes are there to learn")
latest_note = st.text_input('Type your observation here')
latest_date = st.date_input('Date')

latest_note = pd.DataFrame(data={
    'date':latest_date, 
    'notes':latest_note,
}, index=[0])

latest_note['date'] = latest_note['date'].astype(str)
notes_history['date'] = notes_history['date'].astype(str)
notes_history = pd.concat([latest_note, notes_history], ignore_index=True)
notes_history['date'] = pd.to_datetime(notes_history['date'])
notes_history['date'] = notes_history['date'].dt.strftime('%Y-%m-%d')
notes_history = notes_history.set_index('date')
st.dataframe(notes_history)
    
# Help area
st.header("Ask for help")
question = st.text_input('Ask your question here')
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a bakery educator."},
        {"role": "user", "content": question},
    ]
)
answer = response['choices'][0]['message']['content']
# helper code which is not necessary anymore
# response = 'Answer to question: ' + question
# answer=response

st.write(answer)
